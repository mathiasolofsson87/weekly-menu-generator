"""Can these people eat this recipe, and if not, can it be cooked in more than one version.

A member who breaks a rule on specific ingredient lines gets an adjusted version in
which exactly those lines are swapped. Members with the same needs share a version.
Anyone with no conflict eats the recipe as written. Nothing is split when the title
alone objects, when anchovies, fish sauce or gelatin are involved, when egg, soy or
nuts would have to be swapped, or when no replacement is safe for the group. Meat or
fish stock is swapped for vegetable stock.
"""

from __future__ import annotations

from collections.abc import Collection, Iterable, Sequence
from dataclasses import dataclass

from ..const import PORTION_WEIGHTS
from .constraints import hard_violations
from .ingredients import PACK_UNITS, pack_size
from .models import (
    FamilyMember,
    Ingredient,
    MenuDay,
    Recipe,
    Split,
    SplitGroup,
    Substitution,
)
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
        if (contains | set(option.traces)) & allergies or (
            member.diet == "vegan" and contains & {"milk", "egg"}
        ):
            return False
    return True


def _replacement(
    original: Ingredient,
    kind: SwapKind,
    members: Sequence[FamilyMember],
    title: str,
    used: Collection[str],
    dish: Collection[str] = (),
) -> Ingredient | None:
    """The substitute for `original` in the dish `title`, safe for every member.

    Candidates that suit the dish come first. One already chosen for another line of
    the same `dish` is taken again (one fish substitute for a fish pasta, not three);
    otherwise one already `used` this week is passed over when an unused one suits
    as well (see `substitutes`)."""
    safe = [
        (option.rank(title), option, name)
        for option in kind.replacements
        if _safe_for(option, members, name := option.render(original.name))
    ]
    if not safe:
        return None
    safe.sort(key=lambda entry: entry[0])  # stable: table order within a rank
    _, option, name = next(
        (entry for entry in safe if entry[0] < 2 and entry[2] in dish),
        next(
            (entry for entry in safe if entry[0] < 2 and entry[2] not in used), safe[0]
        ),
    )
    amount, unit = original.amount, original.unit
    size = pack_size(original.raw) if unit in PACK_UNITS else None
    if amount is not None:
        if unit == "st" and kind.piece_grams and not option.pieces:
            amount, unit = amount * kind.piece_grams, "g"
        elif size:  # "1 burk kräftstjärtar (à 170 g)" -> 170 g tofu, not "1 burk tofu"
            amount, unit = amount * size[0], size[1]
        amount = round(amount * option.factor, 3)
    text = " ".join(
        part
        for part in (f"{amount:g}" if amount is not None else "", unit or "", name)
        if part
    )
    return Ingredient(name=name, amount=amount, unit=unit, raw=text)


def substitutes_in(days: Iterable[MenuDay]) -> frozenset[str]:
    """Names of the replacements already planned on `days`, for variety in the week."""
    return frozenset(
        swap.replacement.name
        for day in days
        if day.split
        for group in day.split.groups
        for swap in group.substitutions
    )


def _group(
    recipe: Recipe,
    lines: tuple[int, ...],
    members: list[FamilyMember],
    total: float,
    used: Collection[str],
    dish: set[str],
) -> SplitGroup | None:
    swaps: list[Substitution] = []
    adjusted = list(recipe.ingredients)
    for index in lines:
        original = recipe.ingredients[index]
        if FLAVOURING.match(_text(original)):
            return None
        kind = kind_of(_text(original))
        new = (
            _replacement(original, kind, members, recipe.title, used, dish)
            if kind
            else None
        )
        if new is None:
            return None
        dish.add(new.name)
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


def _plan_split(
    recipe: Recipe, attendees: Sequence[FamilyMember], used: Collection[str]
) -> Split | None:
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
    dish: set[str] = set()  # chosen for this recipe so far
    groups = [
        _group(recipe, lines, members, total, used, dish)
        for lines, members in needs.items()
    ]
    if any(g is None for g in groups):
        return None
    return Split(groups=[g for g in groups if g])


def assess(
    recipe: Recipe, attendees: Sequence[FamilyMember], used: Collection[str] = ()
) -> Eligibility:
    """Whether the recipe can be served to `attendees`, and as one dinner or several versions.

    `used` names substitutes already on the week's other days; it only changes which
    substitute is picked, never whether the recipe can be served."""
    violations = hard_violations(recipe, attendees)
    if not violations:
        return Eligibility(True)
    strict = {m.name for m in attendees if not m.cook_separately}
    if any(v.kind == "allergy" and v.member in strict for v in violations):
        return Eligibility(False)
    split = _plan_split(recipe, attendees, used)
    return Eligibility(split is not None, split)
