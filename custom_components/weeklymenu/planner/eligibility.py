"""Can these people eat this recipe, and if not, can it be cooked in more than one version.

A member who breaks a rule on specific ingredient lines gets an adjusted version in
which exactly those lines are swapped. Members with the same needs share a version.
Anyone with no conflict eats the recipe as written. Nothing is split when the title
alone objects, when stock, anchovies or gelatin are involved, when egg, soy or nuts
would have to be swapped, or when no replacement is safe for the group.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from ..const import PORTION_WEIGHTS
from .constraints import hard_violations
from .models import FamilyMember, Ingredient, Recipe, Split, SplitGroup, Substitution
from .substitutes import FLAVOURING, Replacement, SwapKind, kind_of

MAX_GROUPS = 2  # alternative versions beside the original


@dataclass(frozen=True)
class Eligibility:
    ok: bool
    split: Split | None = None


def _text(ingredient: Ingredient) -> str:
    return ingredient.raw or ingredient.name


def _weight(member: FamilyMember) -> float:
    return PORTION_WEIGHTS.get(member.portion, 1.0)


def _bare(ingredients: list[Ingredient]) -> Recipe:
    """A recipe stub without a title, so only ingredient lines are judged."""
    return Recipe(id="", source="", title="", ingredients=ingredients)


def _safe_for(option: Replacement, members: Sequence[FamilyMember], name: str) -> bool:
    """True when `option` breaks no allergy or diet of `members`, by name or declared contents."""
    if hard_violations(_bare([Ingredient(name=name)]), members):
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
    original: Ingredient, kind: SwapKind, members: Sequence[FamilyMember]
) -> Ingredient | None:
    """The first substitute for `original` that every member of the group can eat."""
    for option in kind.replacements:
        name = option.name.format(name=original.name)
        if not _safe_for(option, members, name):
            continue
        amount, unit = original.amount, original.unit
        if amount is not None:
            if unit == "st" and kind.piece_grams and not kind.keep_pieces:
                amount, unit = amount * kind.piece_grams, "g"
            amount = round(amount * option.factor, 3)
        text = " ".join(
            part
            for part in (f"{amount:g}" if amount is not None else "", unit or "", name)
            if part
        )
        return Ingredient(name=name, amount=amount, unit=unit, raw=text)
    return None


def _group(
    recipe: Recipe, lines: tuple[int, ...], members: list[FamilyMember], total: float
) -> SplitGroup | None:
    swaps: list[Substitution] = []
    adjusted = list(recipe.ingredients)
    for index in lines:
        original = recipe.ingredients[index]
        if FLAVOURING.match(_text(original)):
            return None
        kind = kind_of(_text(original))
        new = _replacement(original, kind, members) if kind else None
        if new is None:
            return None
        swaps.append(Substitution(original, new))
        adjusted[index] = new
    # Whatever the swaps missed, the adjusted version itself must be clean for the group.
    if hard_violations(_bare(adjusted), members):
        return None
    return SplitGroup(
        members=[m.name for m in members],
        substitutions=swaps,
        share=round(sum(_weight(m) for m in members) / total, 6),
        separate_pans=any(
            v.kind == "allergy" for v in hard_violations(recipe, members)
        ),
    )


def _plan_split(recipe: Recipe, attendees: Sequence[FamilyMember]) -> Split | None:
    needs: dict[tuple[int, ...], list[FamilyMember]] = {}
    for member in attendees:
        if not hard_violations(recipe, [member]):
            continue
        lines = tuple(
            i
            for i, ingredient in enumerate(recipe.ingredients)
            if hard_violations(_bare([ingredient]), [member])
        )
        if not lines:
            return None  # only the title objects, so the listing may be incomplete
        needs.setdefault(lines, []).append(member)

    served = sum(len(members) for members in needs.values())
    if not needs or served == len(attendees) or len(needs) > MAX_GROUPS:
        return None  # nothing to split, nobody eats the original, or too many versions

    total = sum(_weight(m) for m in attendees)
    groups = [_group(recipe, lines, members, total) for lines, members in needs.items()]
    if any(g is None for g in groups):
        return None
    return Split(groups=[g for g in groups if g])


def assess(recipe: Recipe, attendees: Sequence[FamilyMember]) -> Eligibility:
    """Whether the recipe can be served to `attendees`, and as one dinner or several versions."""
    violations = hard_violations(recipe, attendees)
    if not violations:
        return Eligibility(True)
    strict = {m.name for m in attendees if not m.cook_separately}
    if any(v.kind == "allergy" and v.member in strict for v in violations):
        return Eligibility(False)
    split = _plan_split(recipe, attendees)
    return Eligibility(split is not None, split)
