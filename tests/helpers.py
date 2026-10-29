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
