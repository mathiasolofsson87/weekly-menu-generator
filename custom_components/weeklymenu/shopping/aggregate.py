"""Menu -> shopping items. Pure code: scaling, split shares, merging, pantry."""

from __future__ import annotations

import math
import re
from collections import defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field

from ..const import PORTION_WEIGHTS
from ..planner.generator import PlannerSettings, attendees_for
from ..planner.ingredients import PACK_UNITS, pack_size
from ..planner.models import FamilyMember, Ingredient, Menu, MenuDay
from .models import SKIPPED, ShoppingItem
from .names import counted, singular, strip_preparation
from .units import DENSITY, dimension, display, last_word, to_base, to_packs

DEFAULT_PANTRY = (
    "salt", "peppar", "svartpeppar", "vitpeppar", "vatten", "olja", "olivolja", "rapsolja",
    "matolja", "socker", "strösocker", "vetemjöl", "mjöl", "bakpulver", "lagerblad",
    "pepper", "water", "oil", "sugar", "flour",
)  # fmt: skip

# Where the shopping wording ends and remarks begin ("nötfärs gärna 12%...", "A eller B").
# Not after a hyphen: "udon- eller äggnudlar" is one wording, not "udon-".
_CUT = re.compile(
    r"(?<!-)\s+(?:gärna|eller|alt\.?|alternativt|t\.?\s?ex\.?|typ|à|ca\.?|helst|or|such as|preferably)\s+",
)
_PERCENT = re.compile(r"\s*\d+([.,]\d+)?\s*%")
_MIN_SHARE = 0.001


@dataclass
class Aggregation:
    items: list[ShoppingItem] = field(default_factory=list)  # to buy
    skipped: list[ShoppingItem] = field(default_factory=list)  # pantry staples


def clean_name(name: str) -> tuple[str, str]:
    """(short name, note). The note keeps the original wording when something was cut.

    Remarks ("gärna ...", "eller ...") and preparation ("hackad", "i klyftor") are cut."""
    short = _PERCENT.sub("", name).strip()
    short = _CUT.split(f" {short} ", maxsplit=1)[0].strip(" ,;:.")
    short = strip_preparation(re.sub(r"\s+", " ", short))
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


@dataclass
class _Part:
    """One product's amounts that add up in one dimension (weight, volume, a unit)."""

    item: ShoppingItem
    unit: str | None = None  # of the first contribution
    total: float = 0.0  # in base units
    all_st: bool = True  # every contribution was counted with "st"


@dataclass
class _Product:
    name: str  # as first written
    parts: dict[str, _Part] = field(default_factory=dict)
    pack: dict[str, float] = field(default_factory=dict)  # dimension -> one pack


def _split_staples(name: str, pantry: Iterable[str]) -> list[str]:
    """ "salt och peppar" -> ["salt", "peppar"], when every part is a staple."""
    parts = re.split(r"\s+(?:och|and|&)\s+", name)
    if len(parts) > 1 and all(is_pantry(part, pantry) for part in parts):
        return parts
    return [name]


def _add_note(item: ShoppingItem, note: str) -> None:
    if note and note not in item.note:
        item.note = f"{item.note}; {note}" if item.note else note


def _fold(parts: dict[str, _Part], source: str, target: str, amount: float) -> None:
    """Move `source` into `target`, which grows by `amount` (in its own base units)."""
    gone, into = parts.pop(source), parts[target]
    into.total += amount
    into.all_st = into.all_st and gone.all_st
    for title in gone.item.recipes:
        if title not in into.item.recipes:
            into.item.recipes.append(title)
    _add_note(into.item, gone.item.note)


def _finish(product: _Product, metric_only: bool) -> list[ShoppingItem]:
    """The product's lines: as few as can be bought without inventing amounts."""
    parts = product.parts
    if len(parts) > 1 and "none" in parts:  # "salt" beside "1 tsk salt" adds nothing
        _fold(parts, "none", next(d for d in parts if d != "none"), 0.0)
    density = DENSITY.get(last_word(product.name))
    if density and "volume" in parts and "weight" in parts:  # spoons of butter
        _fold(parts, "volume", "weight", parts["volume"].total * density)
    packs = [d for d in parts if d.removeprefix("unit:") in PACK_UNITS]
    if packs:
        # Packs take in everything else: by the pack's size when a recipe gave it.
        # Amounts of unknown size (kept in the note) fit in what rounding up leaves
        # over when that is at least half a pack; otherwise they take one more pack.
        unknown = False
        for dim in [d for d in parts if d != packs[0]]:
            part, size = parts[dim], product.pack.get(dim)
            if dim in packs:
                amount = part.total
            else:
                shown = ShoppingItem(part.item.name)
                shown.amount, shown.unit = display(
                    part.total, dim, part.unit, metric_only
                )
                if dim == "count":
                    shown.name = counted(shown.name, shown.amount)
                _add_note(part.item, f"+ {shown.text()}")
                amount = part.total / size if size else 0.0
                unknown = unknown or not size
            _fold(parts, dim, packs[0], amount)
        main = parts[packs[0]]
        if unknown and math.ceil(round(main.total, 6)) - main.total < 0.5:
            main.total += 1

    items = []
    for dim, part in parts.items():
        item = part.item
        if dim != "none":
            total = to_packs(part.total, item.name) if dim == "volume" else part.total
            item.amount, item.unit = display(total, dim, part.unit, metric_only)
            if dim == "count":
                item.unit = "st" if part.all_st else None
                item.name = counted(item.name, item.amount)
        items.append(item)
    return items


def aggregate(
    menu: Menu,
    settings: PlannerSettings,
    pantry: Sequence[str] = DEFAULT_PANTRY,
    *,
    metric_only: bool = False,
) -> Aggregation:
    """Everything the menu's dinners need, merged and rounded up.

    Lines are merged by product (singular and plural alike), whatever their units."""
    products: dict[tuple[str, bool], _Product] = {}
    for day in menu.days:
        if day.recipe is None:
            continue
        who = attendees_for(settings, day.weekday) or []
        factor = portions_factor(day.recipe.servings, who)
        for ingredient, multiplier, special in _lines(day, factor):
            full, note = clean_name(ingredient.name)
            for name in _split_staples(full, pantry) if full else ():
                product = products.setdefault((singular(name), special), _Product(name))
                unit = ingredient.unit
                dim = dimension(unit) if ingredient.amount is not None else "none"
                part = product.parts.get(dim)
                if part is None:
                    item = ShoppingItem(name=name, special=special)
                    part = product.parts[dim] = _Part(item, unit)
                if day.recipe.title not in part.item.recipes:
                    part.item.recipes.append(day.recipe.title)
                _add_note(part.item, note)
                if ingredient.amount is not None:
                    part.total += to_base(ingredient.amount * multiplier, unit)
                    part.all_st = part.all_st and unit == "st"
                if unit in PACK_UNITS and (size := pack_size(ingredient.raw or "")):
                    product.pack.setdefault(dimension(size[1]), to_base(*size))

    result = Aggregation()
    for (_, special), product in products.items():
        for item in _finish(product, metric_only):
            if not special and is_pantry(item.name, pantry):
                item.status = SKIPPED
                result.skipped.append(item)
            else:
                result.items.append(item)
    result.items.sort(key=lambda i: i.name.casefold())
    result.skipped.sort(key=lambda i: i.name.casefold())
    return result
