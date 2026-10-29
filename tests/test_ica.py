"""ICA recipe source: parsers (on pages saved from ica.se) and the source (HTTP mocked)."""

import json
import random
import re
from pathlib import Path

import pytest
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.test_util.aiohttp import (
    AiohttpClientMocker,
    AiohttpClientMockResponse,
)

from custom_components.weeklymenu.sources.base import CandidateRequest, SourceError
from custom_components.weeklymenu.sources.ica import IcaRecipeSource
from custom_components.weeklymenu.sources.ica import source as ica_source
from custom_components.weeklymenu.sources.ica.parser import (
    parse_dish_paths,
    parse_listing,
    parse_recipe,
    recipe_id_from_url,
)

FIXTURES = Path(__file__).parent / "fixtures"
RECIPE_HTML = (FIXTURES / "ica_recipe.html").read_text(encoding="utf-8")
LISTING_HTML = (FIXTURES / "ica_listing.html").read_text(encoding="utf-8")
CHILI_URL = "https://www.ica.se/recept/chili-con-carne-424/"
LISTING_URLS = parse_listing(LISTING_HTML)


def recipe_page(
    title: str,
    ingredients: list[str],
    categories: str = "Huvudrätt,Middag",
    time="PT45M",
) -> str:
    node = {
        "@context": "https://schema.org/",
        "@type": "Recipe",
        "name": title,
        "recipeCategory": categories,
        "totalTime": time,
        "recipeYield": "4",
        "recipeIngredient": ingredients,
    }
    return (
        f'<html><script type="application/ld+json">{json.dumps(node)}</script></html>'
    )


# --- parsers on real pages ----------------------------------------------------


def test_parse_real_recipe_page() -> None:
    parsed = parse_recipe(RECIPE_HTML, CHILI_URL)
    assert parsed and parsed.is_dinner
    recipe = parsed.recipe
    assert (
        recipe.id == "ica:424"
        and recipe.source == "ica"
        and recipe.external_id == "424"
    )
    assert recipe.title == "Chili con carne"
    assert recipe.url == CHILI_URL and recipe.image.startswith(
        "https://assets.icanet.se/"
    )
    assert (recipe.total_time, recipe.servings) == (45, 4)
    assert len(recipe.ingredients) == 17
    first = recipe.ingredients[0]
    assert (first.name, first.amount) == ("gula lökar", 2)
    assert any("köttbuljongtärning" in i.raw for i in recipe.ingredients)
    assert recipe.tags == []  # 45 minutes, no quick/easy label


def test_parse_real_listing_page() -> None:
    assert len(LISTING_URLS) == 20
    assert all(
        u.startswith("https://www.ica.se/recept/") and recipe_id_from_url(u)
        for u in LISTING_URLS
    )
    assert CHILI_URL in LISTING_URLS and len(set(LISTING_URLS)) == 20


def test_dish_paths_skip_desserts_and_baking() -> None:
    slugs = parse_dish_paths(LISTING_HTML)
    assert slugs == [
        "pasta",
        "gryta",
        "soppa",
        "kottbullar",
    ]  # not bakverk, dessert, dressing


def test_listing_falls_back_to_links_when_the_structured_list_is_gone() -> None:
    html = '<a href="/recept/pasta-carbonara-1234/">x</a><a href="/recept/pasta-carbonara-1234/">y</a><a href="/butiker/x/">z</a>'
    assert parse_listing(html) == ["https://www.ica.se/recept/pasta-carbonara-1234/"]


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("https://www.ica.se/recept/chili-con-carne-424/", "424"),
        ("/recept/kramig-carbonara-722780/", "722780"),
        ("https://www.ica.se/recept/middag/pasta/", None),
        ("https://www.ica.se/recept/", None),
    ],
)
def test_recipe_id_from_url(url, expected) -> None:
    assert recipe_id_from_url(url) == expected


@pytest.mark.parametrize(
    ("time", "minutes"),
    [
        ("PT45M", 45),
        ("PT1H30M", 90),
        ("PT2H", 120),
        ("PT0M", 0),
        (None, None),
        ("soon", None),
    ],
)
def test_total_time(time, minutes) -> None:
    html = (
        recipe_page("X", ["1 st lök"], time=time)
        if time
        else recipe_page("X", ["1 st lök"]).replace('"totalTime": "PT45M", ', "")
    )
    assert (
        parse_recipe(html, "https://www.ica.se/recept/x-1/").recipe.total_time
        == minutes
    )


def test_categories_decide_what_is_dinner() -> None:
    url = "https://www.ica.se/recept/x-1/"
    assert parse_recipe(recipe_page("X", ["1 st lök"], "Huvudrätt"), url).is_dinner
    assert not parse_recipe(
        recipe_page("X", ["1 dl socker"], "Dessert,Efterrätt"), url
    ).is_dinner
    assert not parse_recipe(
        recipe_page("X", ["1 dl socker"], "Bakverk,Middag"), url
    ).is_dinner
    assert not parse_recipe(recipe_page("X", ["1 st lök"], "Frukost"), url).is_dinner


def test_tags_from_categories_and_time() -> None:
    url = "https://www.ica.se/recept/x-1/"
    quick = parse_recipe(
        recipe_page("X", ["1 st lök"], "Middag,Enkel,Vegetarisk,Barn", "PT20M"), url
    ).recipe
    assert set(quick.tags) == {"quick", "easy", "vegetarian", "family_friendly"}


def test_unusable_pages_give_none() -> None:
    url = "https://www.ica.se/recept/x-1/"
    assert parse_recipe("<html>no data</html>", url) is None
    assert parse_recipe(recipe_page("X", []), url) is None
    assert parse_recipe(recipe_page("", ["1 st lök"]), url) is None
    assert (
        parse_recipe(
            recipe_page("X", ["1 st lök"]), "https://www.ica.se/recept/middag/"
        )
        is None
    )


# --- the source, with ica.se mocked -------------------------------------------------


def mock_site(aioclient_mock: AiohttpClientMocker, *, dinner=lambda n: True) -> None:
    """Listing pages return the real listing; every recipe page is generated."""
    aioclient_mock.get(
        re.compile(r"^https://www\.ica\.se/recept/middag/[a-z0-9-]*/?$"),
        text=LISTING_HTML,
    )

    async def recipe_response(method, url, data):
        number = int(recipe_id_from_url(str(url)))
        return AiohttpClientMockResponse(
            method,
            url,
            text=recipe_page(
                f"Recept {number}",
                [f"{number} g ingrediens {number}", "2 st gul lök"],
                "Huvudrätt,Middag" if dinner(number) else "Dessert",
            ),
        )

    aioclient_mock.get(
        re.compile(r"^https://www\.ica\.se/recept/[a-z0-9-]+-\d+/$"),
        side_effect=recipe_response,
    )


def make_source(hass: HomeAssistant, seed=1) -> IcaRecipeSource:
    return IcaRecipeSource(hass, rng=random.Random(seed), min_interval=0)


def recipe_calls(aioclient_mock: AiohttpClientMocker) -> list[str]:
    return [
        str(c[1]) for c in aioclient_mock.mock_calls if recipe_id_from_url(str(c[1]))
    ]


async def test_returns_dinner_recipes(hass: HomeAssistant, aioclient_mock) -> None:
    mock_site(aioclient_mock)
    recipes = await make_source(hass).async_candidates(CandidateRequest(count=5))
    assert len(recipes) == 5 and len({r.id for r in recipes}) == 5
    assert all(r.id.startswith("ica:") and r.ingredients and r.url for r in recipes)


async def test_requests_are_honest_and_polite(
    hass: HomeAssistant, aioclient_mock
) -> None:
    mock_site(aioclient_mock)
    await make_source(hass).async_candidates(CandidateRequest(count=3))
    agents = {c[3]["User-Agent"] for c in aioclient_mock.mock_calls}
    assert len(agents) == 1
    [agent] = agents
    assert (
        agent.startswith("WeeklyMenuGenerator/")
        and "github.com/mathiasolofsson87" in agent
    )
    assert all(
        str(c[1]).startswith("https://www.ica.se/recept/")
        for c in aioclient_mock.mock_calls
    )


async def test_second_run_is_served_from_the_cache(
    hass: HomeAssistant, aioclient_mock
) -> None:
    mock_site(aioclient_mock)
    first = await make_source(hass).async_candidates(CandidateRequest(count=5))
    calls = len(aioclient_mock.mock_calls)
    again = await make_source(hass, seed=2).async_candidates(CandidateRequest(count=5))
    assert (
        len(again) == 5 and len(aioclient_mock.mock_calls) == calls
    )  # no new requests
    assert {r.id for r in first} | {r.id for r in again}


async def test_excluded_recipes_are_not_returned(
    hass: HomeAssistant, aioclient_mock
) -> None:
    mock_site(aioclient_mock)
    first = await make_source(hass).async_candidates(CandidateRequest(count=10))
    rest = await make_source(hass).async_candidates(
        CandidateRequest(count=24, exclude_ids={r.id for r in first})
    )
    assert not {r.id for r in first} & {r.id for r in rest}


async def test_non_dinner_pages_are_skipped_and_remembered(
    hass: HomeAssistant, aioclient_mock
) -> None:
    ids = [int(recipe_id_from_url(u)) for u in LISTING_URLS]
    desserts = set(ids[:12])
    mock_site(aioclient_mock, dinner=lambda n: n not in desserts)
    recipes = await make_source(hass).async_candidates(CandidateRequest(count=24))
    assert {int(r.external_id) for r in recipes} == set(ids) - desserts
    before = len(recipe_calls(aioclient_mock))
    await make_source(hass).async_candidates(CandidateRequest(count=24))
    assert len(recipe_calls(aioclient_mock)) == before  # desserts are not fetched again


async def test_accept_predicate_skips_hopeless_recipes(
    hass: HomeAssistant, aioclient_mock
) -> None:
    mock_site(aioclient_mock)
    ids = {int(recipe_id_from_url(u)) for u in LISTING_URLS}
    odd = {n for n in ids if n % 2}
    recipes = await make_source(hass).async_candidates(
        CandidateRequest(count=5, accept=lambda r: int(r.external_id) in odd)
    )
    assert recipes and all(int(r.external_id) in odd for r in recipes)


async def test_fetch_budget_is_respected(
    hass: HomeAssistant, aioclient_mock, monkeypatch
) -> None:
    mock_site(aioclient_mock)
    monkeypatch.setattr(ica_source, "MAX_RECIPE_FETCHES", 7)
    recipes = await make_source(hass).async_candidates(
        CandidateRequest(count=20, accept=lambda r: False)
    )
    assert recipes == [] and len(recipe_calls(aioclient_mock)) == 7


async def test_site_down_is_a_source_error(hass: HomeAssistant, aioclient_mock) -> None:
    aioclient_mock.get(re.compile(r"^https://www\.ica\.se/.*"), status=503)
    with pytest.raises(SourceError, match="503"):
        await make_source(hass).async_candidates(CandidateRequest(count=3))


async def test_changed_layout_is_reported(hass: HomeAssistant, aioclient_mock) -> None:
    aioclient_mock.get(
        re.compile(r"^https://www\.ica\.se/.*"), text="<html>something new</html>"
    )
    with pytest.raises(SourceError, match="layout"):
        await make_source(hass).async_candidates(CandidateRequest(count=3))


async def test_failure_midway_keeps_what_was_found(
    hass: HomeAssistant, aioclient_mock
) -> None:
    served = {"n": 0}
    aioclient_mock.get(
        re.compile(r"^https://www\.ica\.se/recept/middag/[a-z0-9-]*/?$"),
        text=LISTING_HTML,
    )

    async def flaky(method, url, data):
        served["n"] += 1
        if served["n"] > 3:
            return AiohttpClientMockResponse(method, url, status=500)
        number = int(recipe_id_from_url(str(url)))
        return AiohttpClientMockResponse(
            method, url, text=recipe_page(f"R{number}", ["1 st lök"])
        )

    aioclient_mock.get(
        re.compile(r"^https://www\.ica\.se/recept/[a-z0-9-]+-\d+/$"), side_effect=flaky
    )
    recipes = await make_source(hass).async_candidates(CandidateRequest(count=10))
    assert len(recipes) == 3


async def test_repeated_failures_stop_the_run(
    hass: HomeAssistant, aioclient_mock
) -> None:
    aioclient_mock.get(
        re.compile(r"^https://www\.ica\.se/recept/middag/[a-z0-9-]*/?$"),
        text=LISTING_HTML,
    )
    aioclient_mock.get(
        re.compile(r"^https://www\.ica\.se/recept/[a-z0-9-]+-\d+/$"), status=500
    )
    with pytest.raises(SourceError):
        await make_source(hass).async_candidates(CandidateRequest(count=10))
    assert len(recipe_calls(aioclient_mock)) == ica_source.MAX_FAILURES


async def test_meets_the_source_contract(hass: HomeAssistant, aioclient_mock) -> None:
    from tests.test_sources import check_contract

    mock_site(aioclient_mock)
    await check_contract(make_source(hass))


async def test_planner_skips_unusable_recipes_without_asking_another_source(
    hass: HomeAssistant, aioclient_mock
) -> None:
    """Half of ICA's recipes contain cream. For a strict milk allergy the planner passes a
    predicate, so the source keeps reading until it has usable ones and no fallback is needed."""
    from datetime import date

    from custom_components.weeklymenu.planner.generator import (
        PlannerSettings,
        async_generate_menu,
    )
    from tests.helpers import FakeSource, member

    aioclient_mock.get(
        re.compile(r"^https://www\.ica\.se/recept/middag/[a-z0-9-]*/?$"),
        text=LISTING_HTML,
    )

    async def page(method, url, data):
        number = int(recipe_id_from_url(str(url)))
        lines = ["400 g pasta", "2 dl grädde" if number % 2 else "2 dl vatten"]
        return AiohttpClientMockResponse(
            method, url, text=recipe_page(f"Recept {number}", lines)
        )

    aioclient_mock.get(
        re.compile(r"^https://www\.ica\.se/recept/[a-z0-9-]+-\d+/$"), side_effect=page
    )
    fallback = FakeSource([])
    strict = member("Kim", allergies=["milk"], cook_separately=False)
    settings = PlannerSettings(dinner_days=["mon", "tue", "wed"], members=[strict])
    menu = await async_generate_menu(
        [make_source(hass), fallback], settings, date(2026, 11, 2), set()
    )
    assert all(d.recipe and int(d.recipe.external_id) % 2 == 0 for d in menu.days)
    assert fallback.requests == []
