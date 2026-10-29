"""Can these people eat this recipe, and if only the protein is in the way, how to split it."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from ..const import PORTION_WEIGHTS
from .allergens import DIET_EXCLUDES
from .constraints import hard_violations
from .models import FamilyMember, Ingredient, Recipe, Split, Substitution
from .substitutes import (
    FLAVOURING,
    PROTEIN_RULES,
    ProteinKind,
    Replacement,
    kind_of,
)

_GRAMS_UNITS = {"g": 1.0, "kg": 1000.0}


@dataclass(frozen=True)
class Eligibility:
    ok: bool
    split: Split | None = None


def _text(ingredient: Ingredient) -> str:
    return ingredient.raw or ingredient.name


def _weight(member: FamilyMember) -> float:
    return PORTION_WEIGHTS.get(member.portion, 1.0)


def _safe_for(option: Replacement, members: Sequence[FamilyMember]) -> bool:
    """True when `option` breaks no allergy or diet of `members`, by name or declared contents."""
    stub = Recipe(
        id="", source="", title="", ingredients=[Ingredient(name=option.name)]
    )
    if hard_violations(stub, members):
        return False
    contains = set(option.contains)
    for member in members:
        allergies = set(member.allergies) | (
            {"milk"} if "lactose" in member.allergies else set()
        )
        if contains & allergies or (
            member.diet == "vegan" and contains & {"milk", "egg"}
        ):
            return False
    return True


def _replacement(
    original: Ingredient, kind: ProteinKind, restricted: Sequence[FamilyMember]
) -> Ingredient | None:
    """The first substitute for `original` that every restricted member can eat."""
    for option in kind.replacements:
        if not _safe_for(option, restricted):
            continue
        amount, unit = original.amount, original.unit
        if amount is not None:
            if unit == "st" and kind.piece_grams and not kind.keep_pieces:
                amount, unit = amount * kind.piece_grams, "g"
            amount = round(amount * option.factor, 3)
        text = " ".join(
            part
            for part in (
                f"{amount:g}" if amount is not None else "",
                unit or "",
                option.name,
            )
            if part
        )
        return Ingredient(name=option.name, amount=amount, unit=unit, raw=text)
    return None


def _plan_split(recipe: Recipe, attendees: Sequence[FamilyMember]) -> Split | None:
    # Which attendees break a diet rule on an ingredient line (the title does not count).
    restricted = [
        m
        for m in attendees
        if any(
            r.match(_text(i))
            for i in recipe.ingredients
            for r in DIET_EXCLUDES.get(m.diet, ())
        )
    ]
    if not restricted or len(restricted) == len(attendees):
        return None  # nothing to split, or nobody would eat the original protein

    swaps: list[Substitution] = []
    for ingredient in recipe.ingredients:
        text = _text(ingredient)
        broken = any(
            r.match(text) for m in restricted for r in DIET_EXCLUDES.get(m.diet, ())
        )
        if not broken:
            continue
        if FLAVOURING.match(text) or not any(
            rule.match(text) for rule in PROTEIN_RULES
        ):
            return None  # stock, anchovies, dairy, egg...: more than a protein is in the way
        kind = kind_of(text)
        replacement = _replacement(ingredient, kind, restricted) if kind else None
        if replacement is None:
            return None
        swaps.append(Substitution(ingredient, replacement))

    total = sum(_weight(m) for m in attendees)
    share = round(sum(_weight(m) for m in restricted) / total, 3)
    return Split(members=[m.name for m in restricted], substitutions=swaps, share=share)


def assess(recipe: Recipe, attendees: Sequence[FamilyMember]) -> Eligibility:
    """Allergies are never negotiable. A diet conflict is fine if it is only a swappable protein."""
    violations = hard_violations(recipe, attendees)
    if not violations:
        return Eligibility(True)
    if any(v.kind == "allergy" for v in violations):
        return Eligibility(False)
    split = _plan_split(recipe, attendees)
    return Eligibility(split is not None, split)
