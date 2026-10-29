"""A free-text wish ("inte fisk", "not fish", "något med pasta") as deterministic rules.

Sources other than AI Task cannot read a wish, so the planner applies it itself:
what the wish rules out is filtered away, what it asks for ranks higher. Words that
name a food group (fish, meat, shellfish ...) use the same Swedish and English term
lists as the allergen filter; any other word is a plain substring match.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .allergens import ALLERGEN_RULES, MEAT, Rule
from .constraints import _first_match, _texts
from .models import Recipe

WISH_BONUS = 2.0  # per wanted word that the recipe contains

NEGATIONS = frozenset(
    [
        "not",
        "no",
        "never",
        "without",
        "avoid",
        "exclude",
        "inte",
        "ingen",
        "inget",
        "inga",
        "utan",
        "ej",
        "aldrig",
        "undvik",
    ]
)
STOPWORDS = frozenset(
    [
        "a",
        "an",
        "the",
        "some",
        "any",
        "something",
        "anything",
        "with",
        "and",
        "or",
        "please",
        "dinner",
        "food",
        "dish",
        "meal",
        "i",
        "want",
        "would",
        "like",
        "maybe",
        "more",
        "less",
        "något",
        "någon",
        "några",
        "gärna",
        "med",
        "och",
        "eller",
        "tack",
        "middag",
        "mat",
        "rätt",
        "vill",
        "jag",
        "lite",
        "mer",
        "kanske",
        "på",
        "till",
        "en",
        "ett",
        "att",
    ]
)
_CLAUSES = re.compile(r"[,;.!\n]|\b(?:and|but|och|men)\b")
_WORD = re.compile(r"[\wåäöÅÄÖéèü-]+")

_GROUPS: dict[str, tuple[Rule, ...]] = {
    "fish": (ALLERGEN_RULES["fish"],),
    "fisk": (ALLERGEN_RULES["fish"],),
    "shellfish": (ALLERGEN_RULES["crustaceans"], ALLERGEN_RULES["molluscs"]),
    "skaldjur": (ALLERGEN_RULES["crustaceans"], ALLERGEN_RULES["molluscs"]),
    "meat": (MEAT,),
    "kött": (MEAT,),
    "egg": (ALLERGEN_RULES["egg"],),
    "ägg": (ALLERGEN_RULES["egg"],),
    "dairy": (ALLERGEN_RULES["milk"],),
    "mejeri": (ALLERGEN_RULES["milk"],),
    "gluten": (ALLERGEN_RULES["gluten"],),
    "nuts": (ALLERGEN_RULES["tree_nuts"], ALLERGEN_RULES["peanuts"]),
    "nötter": (ALLERGEN_RULES["tree_nuts"], ALLERGEN_RULES["peanuts"]),
}


def _hit(word: str, recipe: Recipe) -> bool:
    texts = _texts(recipe)
    if rules := _GROUPS.get(word):
        return any(_first_match(rule, texts) for rule in rules)
    return (
        any(word in t.casefold() for t in texts)
        or word in " ".join(recipe.tags).casefold()
    )


@dataclass(frozen=True)
class Wishes:
    wanted: tuple[str, ...] = ()
    unwanted: tuple[str, ...] = ()

    @classmethod
    def parse(cls, text: str | None) -> Wishes:
        wanted: list[str] = []
        unwanted: list[str] = []
        for clause in _CLAUSES.split((text or "").casefold()):
            words = _WORD.findall(clause)
            negated = any(w in NEGATIONS for w in words)
            content = [w for w in words if w not in NEGATIONS | STOPWORDS]
            (unwanted if negated else wanted).extend(content)
        return cls(tuple(wanted), tuple(unwanted))

    def allows(self, recipe: Recipe) -> bool:
        """False when the recipe contains something the wish rules out."""
        return not any(_hit(word, recipe) for word in self.unwanted)

    def bonus(self, recipe: Recipe) -> float:
        return WISH_BONUS * sum(_hit(word, recipe) for word in self.wanted)
