"""Deterministic recipe checks. Nothing from any source reaches a menu without this."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from .allergens import ALLERGEN_RULES, DIET_EXCLUDES, Rule
from .models import FamilyMember, Recipe


@dataclass(frozen=True)
class Violation:
    """A hard-rule break: a member cannot eat this recipe."""

    member: str
    kind: str  # "allergy" | "diet"
    term: str  # the allergen key, free-text allergy or diet
    text: str  # the ingredient text (or title) that matched


def _texts(recipe: Recipe) -> list[str]:
    """Every string worth checking. The title counts too, in case a listing is incomplete."""
    texts = [recipe.title]
    for ingredient in recipe.ingredients:
        texts.append(ingredient.raw or ingredient.name)
        if ingredient.name not in texts[-1].casefold():
            texts.append(ingredient.name)
    return texts


def _first_match(rule: Rule, texts: Iterable[str]) -> str | None:
    return next((t for t in texts if rule.match(t)), None)


def hard_violations(recipe: Recipe, members: Iterable[FamilyMember]) -> list[Violation]:
    """Allergies and diets of the given members that this recipe breaks."""
    texts = _texts(recipe)
    found: list[Violation] = []
    for member in members:
        for allergy in member.allergies:
            # A known allergen uses its rule; anything else is a plain substring.
            rule = ALLERGEN_RULES.get(allergy) or Rule(
                terms=(allergy.replace("\\", ""),)
            )
            if hit := _first_match(rule, texts):
                found.append(Violation(member.name, "allergy", allergy, hit))
        for rule in DIET_EXCLUDES.get(member.diet, ()):
            if hit := _first_match(rule, texts):
                found.append(Violation(member.name, "diet", member.diet, hit))
                break
    return found


def is_allowed(recipe: Recipe, members: Iterable[FamilyMember]) -> bool:
    """True when nobody in `members` has a hard-rule break."""
    return not hard_violations(recipe, members)


def preference_hits(recipe: Recipe, members: Iterable[FamilyMember]) -> tuple[int, int]:
    """(dislike hits, like hits) summed over members. Soft rules only affect ranking."""
    haystack = " ".join(_texts(recipe)).casefold()
    dislikes = likes = 0
    for member in members:
        dislikes += sum(term in haystack for term in member.dislikes)
        likes += sum(term in haystack for term in member.likes)
    return dislikes, likes


def is_vegetarian(recipe: Recipe) -> bool:
    texts = _texts(recipe)
    return not any(_first_match(rule, texts) for rule in DIET_EXCLUDES["vegetarian"])


def has_fish(recipe: Recipe) -> bool:
    return _first_match(ALLERGEN_RULES["fish"], _texts(recipe)) is not None
