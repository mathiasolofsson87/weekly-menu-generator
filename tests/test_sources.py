"""Recipe source contract, run against every provider, plus registry and AI Task specifics."""

import pytest
import voluptuous as vol
from homeassistant.components.ai_task import (
    STRUCTURE_FIELD_SCHEMA,
    _validate_structure_fields,
)
from homeassistant.core import HomeAssistant, ServiceCall, SupportsResponse
from homeassistant.exceptions import HomeAssistantError

from custom_components.weeklymenu.planner.models import Recipe
from custom_components.weeklymenu.sources.ai_task import (
    STRUCTURE,
    AiTaskSource,
    build_instructions,
    parse_recipes,
)
from custom_components.weeklymenu.sources.base import (
    CandidateRequest,
    RecipeSource,
    SourceError,
)
from custom_components.weeklymenu.sources.registry import (
    SourceRegistry,
    build_default_registry,
)
from tests.helpers import CURRY, LAX, PASTA, FakeSource

AI_ANSWER = {
    "recipes": [
        {
            "title": "Köttbullar med potatis",
            "time_minutes": 45,
            "servings": 4,
            "tags": ["Family_Friendly", "easy"],
            "ingredients": ["500 g blandfärs", "1 kg potatis", "2 dl grädde"],
        },
        {"title": "Linssoppa", "ingredients": ["3 dl röda linser", "1 st gul lök"]},
        {"title": "Utan ingredienser", "ingredients": []},  # unusable
        {"ingredients": ["1 st ägg"]},  # no title
        "not a recipe",
    ]
}


def _register_ai_task(
    hass: HomeAssistant, answer=AI_ANSWER, error=None
) -> list[ServiceCall]:
    calls: list[ServiceCall] = []

    async def generate_data(call: ServiceCall):
        calls.append(call)
        if error:
            raise error
        return {"conversation_id": "x", "data": answer}

    hass.services.async_register(
        "ai_task",
        "generate_data",
        generate_data,
        supports_response=SupportsResponse.ONLY,
    )
    return calls


async def check_contract(source: RecipeSource) -> None:
    """What the planner relies on from every RecipeSource, whoever provides it."""
    assert source.id and ":" not in source.id
    request = CandidateRequest(count=5, language="sv", avoid=["mjölk"], tags=["easy"])
    recipes = await source.async_candidates(request)
    assert isinstance(recipes, list) and len(recipes) <= request.count
    assert len({r.id for r in recipes}) == len(recipes)
    for recipe in recipes:
        assert isinstance(recipe, Recipe)
        assert recipe.id.startswith(f"{source.id}:")
        assert recipe.source == source.id
        assert recipe.title and recipe.ingredients
        assert all(i.name for i in recipe.ingredients)
    if recipes:
        again = await source.async_candidates(
            CandidateRequest(count=5, exclude_ids={recipes[0].id})
        )
        assert recipes[0].id not in {r.id for r in again}


async def test_fake_source_meets_contract() -> None:
    fake = FakeSource([PASTA, CURRY, LAX])
    fake.id = "fake"
    for recipe in fake.recipes:
        assert recipe.id.startswith("fake:")
    await check_contract(fake)


async def test_ai_task_source_meets_contract(hass: HomeAssistant) -> None:
    _register_ai_task(hass)
    await check_contract(AiTaskSource(hass, "ai_task.gemini"))


async def test_ai_task_structure_is_accepted_by_home_assistant() -> None:
    _validate_structure_fields(vol.Schema({str: STRUCTURE_FIELD_SCHEMA})(STRUCTURE))


async def test_ai_task_sends_entity_structure_and_prompt(hass: HomeAssistant) -> None:
    calls = _register_ai_task(hass)
    source = AiTaskSource(hass, "ai_task.gemini")
    await source.async_candidates(
        CandidateRequest(
            count=4,
            language="sv",
            avoid=["mjölk", "svamp"],
            diets=["vegetarian"],
            hint="snabbt",
        )
    )
    [call] = calls
    assert call.data["entity_id"] == "ai_task.gemini"
    assert call.data["structure"] == STRUCTURE
    text = call.data["instructions"]
    assert "4 olika middagsrecept" in text and "mjölk, svamp" in text
    assert "vegetarian" in text and "snabbt" in text


async def test_ai_task_failure_becomes_source_error(hass: HomeAssistant) -> None:
    _register_ai_task(hass, error=HomeAssistantError("quota"))
    with pytest.raises(SourceError, match="quota"):
        await AiTaskSource(hass, "ai_task.gemini").async_candidates(
            CandidateRequest(count=3)
        )


def test_parse_recipes_skips_unusable_entries() -> None:
    recipes = parse_recipes(AI_ANSWER)
    assert [r.title for r in recipes] == ["Köttbullar med potatis", "Linssoppa"]
    first = recipes[0]
    assert first.id == Recipe.make_id(
        "ai_task", Recipe.key_from_title("Köttbullar med potatis")
    )
    assert (first.total_time, first.servings) == (45, 4)
    assert first.tags == ["family_friendly", "easy"]
    top = first.ingredients[0]
    assert (top.name, top.amount, top.unit) == (
        "blandfärs",
        500,
        "g",
    )
    assert parse_recipes(None) == [] and parse_recipes({"recipes": "x"}) == []


def test_same_title_gives_same_id() -> None:
    assert Recipe.key_from_title(" Linssoppa ") == Recipe.key_from_title("linssoppa")


def test_english_prompt() -> None:
    text = build_instructions(CandidateRequest(count=2, language="en", avoid=["milk"]))
    assert "Answer in English" in text and "milk" in text


def test_registry_builds_enabled_configured_sources_in_order(
    hass: HomeAssistant,
) -> None:
    registry = SourceRegistry()
    registry.register("a", lambda hass, cfg: FakeSource())
    registry.register("b", lambda hass, cfg: None)  # not configured
    registry.register("c", lambda hass, cfg: FakeSource())
    assert registry.ids == ["a", "b", "c"]
    assert len(registry.create(hass, {})) == 2
    assert len(registry.create(hass, {}, enabled=["c"])) == 1
    assert registry.create(hass, {}, enabled=[]) == []


def test_default_registry(hass: HomeAssistant) -> None:
    registry = build_default_registry()
    assert registry.ids == ["ica", "ai_task"]  # store recipes first, then AI
    assert [type(s).__name__ for s in registry.create(hass, {})] == ["IcaRecipeSource"]
    both = registry.create(hass, {"ai_task_entity": "ai_task.gemini"})
    assert [s.id for s in both] == ["ica", "ai_task"] and isinstance(
        both[1], AiTaskSource
    )
    assert [s.id for s in registry.create(hass, {}, enabled=["ai_task"])] == []


def test_prompt_asks_for_separable_only_when_needed() -> None:
    plain = build_instructions(CandidateRequest(count=2, language="sv"))
    split = build_instructions(CandidateRequest(count=2, language="sv", separable=True))
    assert "egna ingrediensrader" not in plain and "egna ingrediensrader" in split
    assert "their own ingredient lines" in build_instructions(
        CandidateRequest(count=2, language="en", separable=True)
    )


async def test_no_family_member_name_ever_reaches_a_recipe_source() -> None:
    """The README promises the AI is sent words (allergies, diets, styles) and never names."""
    from dataclasses import asdict
    from datetime import date

    from custom_components.weeklymenu.planner.generator import (
        PlannerSettings,
        async_generate_menu,
    )
    from custom_components.weeklymenu.sources.ai_task import build_instructions
    from tests.helpers import member

    family = [
        member("Zzyzx", allergies=["milk"], dislikes=["svamp"], diet="vegetarian"),
        member("Qwertyuiop", likes=["pasta"]),
    ]
    source = FakeSource([PASTA, CURRY])
    settings = PlannerSettings(
        dinner_days=["mon", "tue"],
        members=family,
        style_tags=["quick"],
        max_split_days=2,
    )
    await async_generate_menu(
        [source], settings, date(2026, 11, 2), set(), hint="more fish"
    )

    for request in source.requests:
        fields = {k: v for k, v in asdict(request).items() if k != "accept"}
        for language in ("sv", "en"):
            sent = repr(fields) + build_instructions(request)
            assert "Zzyzx" not in sent and "Qwertyuiop" not in sent
        assert "milk" in request.avoid and "svamp" in request.avoid
