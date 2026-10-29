"""Test helpers: recipe builders and a fake recipe source."""

from custom_components.weeklymenu.planner.ingredients import parse_ingredient
from custom_components.weeklymenu.planner.models import FamilyMember, Recipe
from custom_components.weeklymenu.sources.base import (
    CandidateRequest,
    RecipeSource,
    SourceError,
)


def recipe(
    title: str, *lines: str, tags: tuple[str, ...] = (), source: str = "fake"
) -> Recipe:
    """A recipe with ingredients parsed from text lines."""
    return Recipe(
        id=Recipe.make_id(source, Recipe.key_from_title(title)),
        source=source,
        title=title,
        ingredients=[parse_ingredient(line) for line in lines],
        tags=list(tags),
    )


def member(name: str, **kwargs) -> FamilyMember:
    kwargs.setdefault("attends", ["mon", "tue", "wed", "thu", "fri", "sat", "sun"])
    return FamilyMember(name=name, **kwargs)


class FakeSource(RecipeSource):
    """A second provider, to prove nothing in the core depends on a specific one."""

    id = "fake"

    def __init__(self, recipes: list[Recipe] | None = None, fail: bool = False) -> None:
        self.recipes = recipes or []
        self.fail = fail
        self.requests: list[CandidateRequest] = []

    async def async_candidates(self, request: CandidateRequest) -> list[Recipe]:
        self.requests.append(request)
        if self.fail:
            raise SourceError("boom")
        return [r for r in self.recipes if r.id not in request.exclude_ids][
            : request.count
        ]


PASTA = recipe(
    "Pasta carbonara", "400 g spaghetti", "150 g bacon", "3 ägg", "1 dl parmesan"
)
TACOS = recipe(
    "Tacos", "500 g nötfärs", "8 st tortilla", "1 dl crème fraîche", "2 st tomat"
)
CURRY = recipe(
    "Linscurry", "3 dl röda linser", "1 burk kokosmjölk", "2 st gul lök", tags=("easy",)
)
LAX = recipe("Ugnsbakad lax", "600 g laxfilé", "1 kg potatis", "2 dl gräddfil")
SOUP = recipe("Tomatsoppa", "800 g krossade tomater", "2 st gul lök", "1 dl grädde")
STEW = recipe("Köttgryta", "600 g nötkött", "2 st gul lök", "3 st morot")
STIR = recipe(
    "Wok med tofu", "300 g tofu", "2 st morot", "2 msk sojasås", "2 st gul lök"
)

ALL_RECIPES = [PASTA, TACOS, CURRY, LAX, SOUP, STEW, STIR]


def entity_id(hass, entry, domain: str, key: str) -> str:
    from homeassistant.helpers import entity_registry as er

    found = er.async_get(hass).async_get_entity_id(
        domain, "weeklymenu", f"{entry.entry_id}_{key}"
    )
    assert found, key
    return found


def state(hass, entry, key: str):
    """State of one of the integration's sensors."""
    return hass.states.get(entity_id(hass, entry, "sensor", key))


async def generate(hass, week="2026-11-02", **extra):
    """Call weeklymenu.generate_menu and return its response."""
    return await hass.services.async_call(
        "weeklymenu",
        "generate_menu",
        {"week_start": week, **extra},
        blocking=True,
        return_response=True,
    )


async def call(hass, service: str, **data):
    """Call a weeklymenu service; returns its response if it has one."""
    from homeassistant.core import SupportsResponse

    has_response = (
        hass.services.supports_response("weeklymenu", service)
        is not SupportsResponse.NONE
    )
    return await hass.services.async_call(
        "weeklymenu", service, data, blocking=True, return_response=has_response
    )
