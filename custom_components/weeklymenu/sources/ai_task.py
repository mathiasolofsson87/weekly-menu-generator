"""Recipe suggestions from a Home Assistant AI Task entity (Gemini, for example)."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from ..planner.ingredients import parse_ingredient
from ..planner.models import Recipe
from .base import CandidateRequest, RecipeSource, SourceError

_LOGGER = logging.getLogger(__name__)

STYLE_TAGS = [
    "quick",
    "easy",
    "fancy",
    "family_friendly",
    "budget",
    "vegetarian",
    "fish",
]

# Passed to ai_task.generate_data so the answer comes back as data, not prose.
STRUCTURE: dict[str, Any] = {
    "recipes": {
        "description": "Dinner recipes",
        "required": True,
        "selector": {
            "object": {
                "multiple": True,
                "fields": {
                    "title": {"required": True, "selector": {"text": {}}},
                    "time_minutes": {"selector": {"number": {"min": 1, "max": 600}}},
                    "servings": {"selector": {"number": {"min": 1, "max": 20}}},
                    "tags": {"selector": {"text": {"multiple": True}}},
                    "ingredients": {
                        "required": True,
                        "selector": {"text": {"multiple": True}},
                    },
                },
            }
        },
    }
}

_PROMPTS = {
    "sv": {
        "intro": "Föreslå {count} olika middagsrecept för en familj. Svara på svenska.",
        "avoid": "Använd aldrig och undvik helt: {terms}.",
        "diets": "Alla måste kunna äta rätterna. Kost som ska respekteras: {terms}.",
        "tags": "Önskad stil: {terms}.",
        "use_up": "Använd gärna dessa ingredienser: {terms}.",
        "hint": "Extra önskemål: {text}",
        "separable": (
            "Om en rätt innehåller kött, fisk, mejeriprodukter eller gluten: skriv dem som egna "
            "ingrediensrader och blanda inte in dem i såser, buljonger eller kryddblandningar, så "
            "att de kan bytas mot ett alternativ åt den som inte kan äta dem."
        ),
        "format": (
            "Skriv varje ingrediens på en rad med mängd och enhet (g, kg, dl, msk, tsk, st), "
            "till exempel '350 g nötfärs' eller '2 st gul lök'. Ange tid i minuter, "
            "antal portioner och taggar. Välj taggar bland: {tags}. "
            "Alla recept ska vara vanliga rätter som går att handla i en svensk matbutik."
        ),
    },
    "en": {
        "intro": "Suggest {count} different dinner recipes for a family. Answer in English.",
        "avoid": "Never use and fully avoid: {terms}.",
        "diets": "Everyone must be able to eat the dishes. Diets to respect: {terms}.",
        "tags": "Preferred style: {terms}.",
        "use_up": "Please use these ingredients: {terms}.",
        "hint": "Extra wishes: {text}",
        "separable": (
            "If a dish contains meat, fish, dairy or gluten: write them on their own ingredient "
            "lines and do not hide them in sauces, stocks or spice mixes, so they can be swapped "
            "for an alternative for anyone who cannot eat them."
        ),
        "format": (
            "Write each ingredient on one line with amount and unit (g, kg, dl, msk, tsk, st), "
            "for example '350 g minced beef' or '2 st yellow onion'. Give the time in minutes, "
            "the number of servings and tags. Choose tags from: {tags}. "
            "All recipes should be ordinary dishes available in a Swedish supermarket."
        ),
    },
}


def build_instructions(request: CandidateRequest) -> str:
    """Prompt text in the integration language."""
    text = _PROMPTS.get(request.language, _PROMPTS["en"])
    parts = [text["intro"].format(count=request.count)]
    if request.avoid:
        parts.append(text["avoid"].format(terms=", ".join(request.avoid)))
    if diets := [d for d in request.diets if d != "omnivore"]:
        parts.append(text["diets"].format(terms=", ".join(diets)))
    if request.tags:
        parts.append(text["tags"].format(terms=", ".join(request.tags)))
    if request.use_up:
        parts.append(text["use_up"].format(terms=", ".join(request.use_up)))
    if request.hint:
        parts.append(text["hint"].format(text=request.hint))
    if request.separable:
        parts.append(text["separable"])
    parts.append(text["format"].format(tags=", ".join(STYLE_TAGS)))
    return " ".join(parts)


def _int(value: Any) -> int | None:
    try:
        return round(float(value))
    except (TypeError, ValueError):
        return None


def parse_recipes(data: Any) -> list[Recipe]:
    """Turn the AI Task answer into recipes, skipping entries that are unusable."""
    recipes: list[Recipe] = []
    items = data.get("recipes") if isinstance(data, dict) else None
    for item in items if isinstance(items, list) else []:
        title = str(item.get("title", "")).strip() if isinstance(item, dict) else ""
        lines = item.get("ingredients") if isinstance(item, dict) else None
        if not title or not isinstance(lines, list) or not lines:
            _LOGGER.debug("Skipping unusable AI recipe: %s", item)
            continue
        recipes.append(
            Recipe(
                id=Recipe.make_id(AiTaskSource.id, Recipe.key_from_title(title)),
                source=AiTaskSource.id,
                title=title,
                ingredients=[
                    parse_ingredient(str(line)) for line in lines if str(line).strip()
                ],
                total_time=_int(item.get("time_minutes")),
                servings=_int(item.get("servings")),
                tags=[
                    str(t).strip().casefold()
                    for t in item.get("tags") or []
                    if str(t).strip()
                ],
            )
        )
    return recipes


class AiTaskSource(RecipeSource):
    """Asks an `ai_task` entity for recipes through the `ai_task.generate_data` service."""

    id = "ai_task"

    def __init__(self, hass: HomeAssistant, entity_id: str) -> None:
        self.hass = hass
        self.entity_id = entity_id

    async def async_candidates(self, request: CandidateRequest) -> list[Recipe]:
        try:
            response = await self.hass.services.async_call(
                "ai_task",
                "generate_data",
                {
                    "task_name": "Weekly menu recipes",
                    "entity_id": self.entity_id,
                    "instructions": build_instructions(request),
                    "structure": STRUCTURE,
                },
                blocking=True,
                return_response=True,
            )
        except HomeAssistantError as err:
            raise SourceError(f"AI Task failed: {err}") from err
        recipes = parse_recipes((response or {}).get("data"))
        return [r for r in recipes if r.id not in request.exclude_ids][: request.count]
