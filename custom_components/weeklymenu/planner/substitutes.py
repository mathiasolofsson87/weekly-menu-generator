"""What can stand in for an ingredient someone cannot eat.

Each `ProteinKind`/`SwapKind` recognises a kind of ingredient line and lists
replacements in preference order. The first one that is safe for everyone who gets
it wins, so tofu is skipped for a soy allergy and halloumi for a vegan. A name with
`{name}` is filled in with the original ("laktosfri {name}" -> "laktosfri grädde").
Amounts are converted by `factor`; counted pieces become grams via `piece_grams`.
"""

from __future__ import annotations

from dataclasses import dataclass

from .allergens import (
    ALLERGEN_RULES,
    DAIRY_EXCEPTIONS,
    MEAT,
    PLANT_BASED,
    Rule,
)

# Ingredients that carry meat or fish flavour but cannot be swapped on their own:
# a recipe with beef stock or anchovies is not "fine apart from the steak".
FLAVOURING = Rule(
    terms=(
        "buljong", "fond", "bouillon", "stock", "broth", "kraft", "extrakt", "extract",
        "ister", "ansjovis", "anchov", "sardell", "worcester", "fisksås", "fish sauce",
        "ostronsås", "oyster sauce", "skmalz", "fett", "tallow", "lard", "gelatin",
    ),
)  # fmt: skip


@dataclass(frozen=True)
class Replacement:
    name: str
    factor: float = 1.0
    # Allergens the product may contain, declared on purpose and over-cautiously: a
    # name like "vegofärs" does not reveal that it is usually made of soy and wheat.
    contains: tuple[str, ...] = ()


@dataclass(frozen=True)
class SwapKind:
    key: str
    rule: Rule
    replacements: tuple[Replacement, ...]
    piece_grams: float | None = None  # grams per counted piece, for converting "st"
    keep_pieces: bool = False  # replacement is counted in pieces too (sausages)


_TOFU = Replacement("tofu", contains=("soy",))
_CHICKPEAS = Replacement("kikärtor")
_PORTOBELLO = Replacement("portobellosvamp")
_HALLOUMI = Replacement("halloumi", contains=("milk",))
_LACTOSE_FREE = Replacement("laktosfri {name}")
_PLANT = Replacement("växtbaserad {name}", contains=("soy", "gluten", "tree_nuts"))

_DAIRY_FREE_FROM = PLANT_BASED + ("mjölkfri", "dairy-free")
_GLUTEN = ALLERGEN_RULES["gluten"]


def _dairy(*terms: str) -> Rule:
    return Rule(terms=terms, exceptions=DAIRY_EXCEPTIONS, free_from=_DAIRY_FREE_FROM)


def _gluten(*terms: str) -> Rule:
    return Rule(terms=terms, exceptions=_GLUTEN.exceptions, free_from=_GLUTEN.free_from)


# Order matters: the first kind that matches wins, so mince is tested before steak.
KINDS: tuple[SwapKind, ...] = (
    # --- meat and fish
    SwapKind(
        "mince",
        Rule(terms=("färs", "mince")),
        (
            Replacement("vegofärs", contains=("soy", "gluten")),
            Replacement("röda linser", 0.5),
            _CHICKPEAS,
        ),
    ),
    SwapKind(
        "sausage",
        Rule(terms=("korv", "sausage")),
        (Replacement("vegokorv", contains=("soy", "gluten", "egg", "milk")),),
        keep_pieces=True,
    ),
    SwapKind(
        "cured",
        Rule(terms=("bacon", "skinka", "pancetta", "prosciutto", "salami", "chorizo", "kassler", r"\bham\b")),
        (Replacement("rökt tofu", 0.7, contains=("soy",)), Replacement("portobellosvamp", 0.7)),
    ),
    SwapKind(
        "poultry",
        Rule(terms=("kyckling", "kalkon", r"\bank|anka\b", "chicken", "turkey", "duck")),
        (_TOFU, _CHICKPEAS, _HALLOUMI),
        piece_grams=150,
    ),
    SwapKind("fish", ALLERGEN_RULES["fish"], (_TOFU, _CHICKPEAS, _HALLOUMI), piece_grams=150),
    SwapKind(
        "shellfish",
        Rule(terms=ALLERGEN_RULES["crustaceans"].terms + ALLERGEN_RULES["molluscs"].terms),
        (_TOFU, _CHICKPEAS),
    ),
    SwapKind("meat", MEAT, (_TOFU, _PORTOBELLO, _HALLOUMI, _CHICKPEAS), piece_grams=200),
    # --- dairy (lactose-free first: it suits lactose intolerance but not milk allergy)
    SwapKind(
        "cream",
        _dairy("grädde", "cream", "gräddfil", "crème fraîche", "creme fraiche", "crème fraiche", "mascarpone"),
        (_LACTOSE_FREE, Replacement("havregrädde"), _PLANT),
    ),
    SwapKind(
        "milk",
        _dairy("mjölk", "milk", "kefir", "vassle"),
        (_LACTOSE_FREE, Replacement("havredryck"), Replacement("sojadryck", contains=("soy",))),
    ),
    SwapKind(
        "butter",
        _dairy("smör", "butter", "ghee"),
        (Replacement("laktosfritt smör"), Replacement("växtbaserat margarin", contains=("soy",))),
    ),
    SwapKind(
        "yoghurt",
        _dairy("yoghurt", "yogurt", "kvarg", "quark", "keso", "cottage"),
        (_LACTOSE_FREE, Replacement("sojayoghurt", contains=("soy",)), Replacement("havreyoghurt")),
    ),
    SwapKind("dairy", ALLERGEN_RULES["milk"], (_LACTOSE_FREE, _PLANT)),  # cheese and the rest
    # --- gluten
    SwapKind(
        "grain",
        _gluten("couscous", "bulgur"),
        (Replacement("quinoa"), Replacement("ris")),
    ),
    SwapKind("noodles", _gluten("nudl", "noodle"), (Replacement("risnudlar"),)),
    SwapKind(
        "flour",
        _gluten("mjöl", "flour"),
        (Replacement("glutenfritt mjöl"), Replacement("majsmjöl")),
    ),
    SwapKind("gluten", _GLUTEN, (Replacement("glutenfri {name}"),)),  # pasta, bread, tortilla
)  # fmt: skip


def kind_of(text: str) -> SwapKind | None:
    """The kind of swap an ingredient text calls for."""
    return next((k for k in KINDS if k.rule.match(text)), None)
