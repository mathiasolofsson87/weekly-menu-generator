"""Protein kinds and what can stand in for them when someone cannot eat the original.

`factor` converts the original amount to the replacement amount (usually 1:1 by
weight). `piece_grams` is used when the recipe counts pieces ("4 st kycklingfilé")
and the replacement is weighed. Candidates are tried in order and the first one that
is safe for everyone who needs it wins, so tofu is skipped for a soy allergy and
halloumi for a vegan.
"""

from __future__ import annotations

from dataclasses import dataclass

from .allergens import ALLERGEN_RULES, MEAT, Rule

# Ingredients that carry meat or fish flavour but are not a protein you can swap:
# a recipe with beef stock or anchovies is not "vegetarian apart from the steak".
FLAVOURING = Rule(
    terms=(
        "buljong", "fond", "bouillon", "stock", "broth", "kraft", "extrakt", "extract",
        "ister", "ansjovis", "anchov", "sardell", "worcester", "fisksås", "fish sauce",
        "ostronsås", "oyster sauce", "skmalz", "fett", "tallow", "lard", "gelatin",
    ),
)  # fmt: skip

# What counts as a protein in the diet sense.
PROTEIN_RULES: tuple[Rule, ...] = (
    MEAT,
    ALLERGEN_RULES["fish"],
    ALLERGEN_RULES["crustaceans"],
    ALLERGEN_RULES["molluscs"],
)


@dataclass(frozen=True)
class Replacement:
    name: str
    factor: float = 1.0
    # Allergens the product may contain, declared on purpose and over-cautiously: a
    # name like "vegofärs" does not reveal that it is usually made of soy and wheat.
    contains: tuple[str, ...] = ()


@dataclass(frozen=True)
class ProteinKind:
    key: str
    rule: Rule
    replacements: tuple[Replacement, ...]
    piece_grams: float | None = None  # grams per counted piece, for converting "st"
    keep_pieces: bool = False  # replacement is counted in pieces too (sausages)


# Order matters: the first kind that matches wins, so mince is tested before steak.
KINDS: tuple[ProteinKind, ...] = (
    ProteinKind(
        "mince",
        Rule(terms=("färs", "mince")),
        (Replacement("vegofärs", contains=("soy", "gluten")), Replacement("röda linser", 0.5), Replacement("kikärtor")),
    ),
    ProteinKind(
        "sausage",
        Rule(terms=("korv", "sausage")),
        (Replacement("vegokorv", contains=("soy", "gluten", "egg", "milk")),),
        keep_pieces=True,
    ),
    ProteinKind(
        "cured",
        Rule(terms=("bacon", "skinka", "pancetta", "prosciutto", "salami", "chorizo", "kassler", r"\bham\b")),
        (Replacement("rökt tofu", 0.7, contains=("soy",)), Replacement("portobellosvamp", 0.7)),
    ),
    ProteinKind(
        "poultry",
        Rule(terms=("kyckling", "kalkon", r"\bank|anka\b", "chicken", "turkey", "duck")),
        (Replacement("tofu", contains=("soy",)), Replacement("kikärtor"), Replacement("halloumi", contains=("milk",))),
        piece_grams=150,
    ),
    ProteinKind(
        "fish",
        ALLERGEN_RULES["fish"],
        (Replacement("tofu", contains=("soy",)), Replacement("kikärtor"), Replacement("halloumi", contains=("milk",))),
        piece_grams=150,
    ),
    ProteinKind(
        "shellfish",
        Rule(terms=ALLERGEN_RULES["crustaceans"].terms + ALLERGEN_RULES["molluscs"].terms),
        (Replacement("tofu", contains=("soy",)), Replacement("kikärtor")),
    ),
    ProteinKind(
        "meat",
        MEAT,  # steak, pork, lamb, anything else with meat
        (
            Replacement("tofu", contains=("soy",)),
            Replacement("portobellosvamp"),
            Replacement("halloumi", contains=("milk",)),
            Replacement("kikärtor"),
        ),
        piece_grams=200,
    ),
)  # fmt: skip


def kind_of(text: str) -> ProteinKind | None:
    """The protein kind an ingredient text belongs to."""
    return next((k for k in KINDS if k.rule.match(text)), None)
