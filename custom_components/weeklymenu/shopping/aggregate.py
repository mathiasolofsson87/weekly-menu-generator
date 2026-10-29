"""Menu -> shopping items. Pure code: scaling, split shares, merging, pantry."""

from __future__ import annotations

import re
from collections import defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field

from ..const import PORTION_WEIGHTS
from ..planner.generator import PlannerSettings, attendees_for
from ..planner.models import FamilyMember, Ingredient, Menu, MenuDay
from .models import SKIPPED, ShoppingItem
from .units import dimension, display, to_base

DEFAULT_PANTRY = (
    "salt", "peppar", "svartpeppar", "vitpeppar", "vatten", "olja", "olivolja", "rapsolja",
    "matolja", "socker", "strösocker", "vetemjöl", "mjöl", "bakpulver", "lagerblad",
    "pepper", "water", "oil", "sugar", "flour",
)  # fmt: skip

# Where the shopping wording ends and remarks begin ("nötfärs gärna 12%...", "A eller B").
_CUT = re.compile(
    r"\s+(?:gärna|eller|alt\.?|alternativt|t\.?\s?ex\.?|typ|à|ca\.?|helst|or|such as|preferably)\s+",
)
_PERCENT = re.compile(r"\s*\d+([.,]\d+)?\s*%")
_MIN_SHARE = 0.001


@dataclass
class Aggregation:
    items: list[ShoppingItem] = field(default_factory=list)  # to buy
    skipped: list[ShoppingItem] = field(default_factory=list)  # pantry staples


def clean_name(name: str) -> tuple[str, str]:
    """(short name, note). The note keeps the original wording when something was cut."""
    short = _PERCENT.sub("", name).strip()
    short = _CUT.split(f" {short} ", maxsplit=1)[0].strip(" ,;:.")
    short = re.sub(r"\s+", " ", short)
    return (
        (short, name.strip()) if short and short != name.strip() else (name.strip(), "")
    )


def is_pantry(name: str, pantry: Iterable[str]) -> bool:
    """True when `name` is, or starts or contains a word that is, a staple."""
    lowered = name.casefold()
    words = set(re.split(r"[\s,/]+", lowered))
    return any(
        s == lowered or s in words or lowered.startswith(f"{s} ") for s in pantry
    )


def portions_factor(
    recipe_servings: int | None, attendees: Sequence[FamilyMember]
) -> float:
    """How much of the recipe to make: portions eaten / portions the recipe gives."""
    if not attendees or not recipe_servings:
        return 1.0
    return sum(PORTION_WEIGHTS.get(m.portion, 1.0) for m in attendees) / recipe_servings


def _lines(day: MenuDay, factor: float) -> list[tuple[Ingredient, float, bool]]:
    """(ingredient, amount multiplier, is substitute) for what this dinner needs.

    A line swapped for some members is bought for the share that keeps it, and its
    replacement for the share of each group that gets it."""
    assert day.recipe is not None
    swapped: dict[Ingredient, float] = defaultdict(float)  # original -> share replaced
    extra: list[tuple[Ingredient, float, bool]] = []
    if day.split:
        for group in day.split.groups:
            for swap in group.substitutions:
                swapped[swap.original] += group.share
                extra.append((swap.replacement, group.share * factor, True))
    lines = []
    for ingredient in day.recipe.ingredients:
        keep = 1.0 - swapped.get(ingredient, 0.0)
        if keep > _MIN_SHARE:
            lines.append((ingredient, keep * factor, False))
    return lines + extra


def aggregate(
    menu: Menu,
    settings: PlannerSettings,
    pantry: Sequence[str] = DEFAULT_PANTRY,
    *,
    metric_only: bool = False,
) -> Aggregation:
    """Everything the menu's dinners need, merged and rounded up."""
    # key -> [total in base units, first unit, item skeleton]
    merged: dict[tuple[str, str, bool], list] = {}
    for day in menu.days:
        if day.recipe is None:
            continue
        who = attendees_for(settings, day.weekday) or []
        factor = portions_factor(day.recipe.servings, who)
        for ingredient, multiplier, special in _lines(day, factor):
            name, note = clean_name(ingredient.name)
            if not name:
                continue
            dim = (
                dimension(ingredient.unit) if ingredient.amount is not None else "none"
            )
            key = (name.casefold(), dim, special)
            entry = merged.get(key)
            if entry is None:
                entry = merged[key] = [
                    0.0,
                    ingredient.unit,
                    ShoppingItem(name=name, special=special),
                    True,  # every contribution so far was counted with "st"
                ]
            item: ShoppingItem = entry[2]
            if day.recipe.title not in item.recipes:
                item.recipes.append(day.recipe.title)
            if note and note not in item.note:
                item.note = f"{item.note}; {note}" if item.note else note
            if ingredient.amount is not None:
                entry[0] += to_base(ingredient.amount * multiplier, ingredient.unit)
                entry[3] = entry[3] and ingredient.unit == "st"

    result = Aggregation()
    for (_, dim, _), (total, unit, item, all_st) in merged.items():
        if dim != "none":
            item.amount, item.unit = display(total, dim, unit, metric_only)
            if dim == "count":
                item.unit = "st" if all_st else None
        if not item.special and is_pantry(item.name, pantry):
            item.status = SKIPPED
            result.skipped.append(item)
        else:
            result.items.append(item)
    result.items.sort(key=lambda i: i.name.casefold())
    result.skipped.sort(key=lambda i: i.name.casefold())
    return result
