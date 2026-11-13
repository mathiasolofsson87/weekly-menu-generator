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
from ..planner.substitutes import substitute_note
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
# "ev bröd": optional, but still worth having on the list.
_OPTIONAL = re.compile(r"^(?:ev\.?|eventuellt|valfritt|optional)\s+", re.IGNORECASE)
# A line without an amount often lists several things: "bröd, stekt bacon, persilja",
# "limeklyftor och riven ost". Not after a hyphen ("ärt- och nötfärs").
_LIST = re.compile(r"\s*,\s*|(?<!-)\s+(?:och|and|&)\s+")
# Zest and wedges are bought as the fruit: about 1 msk zest or 6 wedges from one.
_FRUIT_PART = re.compile(r"^(citron|lime|apelsin)s?(skal|klyfta|klyftor)$")
ZEST_ML_PER_FRUIT = 15
WEDGES_PER_FRUIT = 6
_MIN_SHARE = 0.001


@dataclass
class Aggregation:
    items: list[ShoppingItem] = field(default_factory=list)  # to buy
    skipped: list[ShoppingItem] = field(default_factory=list)  # pantry staples


def clean_name(name: str) -> tuple[str, str]:
    """(short name, note). The note keeps the original wording when something was cut.

    Remarks ("gärna ...", "eller ...") and preparation ("hackad", "i klyftor") are cut."""
    short = _OPTIONAL.sub("", _PERCENT.sub("", name).strip())
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


def _names(ingredient: Ingredient, pantry: Iterable[str]) -> list[tuple[str, str]]:
    """(shopping name, note) for each product on the line.

    A line without an amount is split into its listed parts; "salt och peppar" is
    split when every part is a staple."""
    if ingredient.amount is None and ingredient.raw:
        text = re.sub(r"\(.*?\)", " ", ingredient.raw).casefold()
        parts = [p for p in _LIST.split(text) if p.strip()]
        if len(parts) > 1:
            return [cleaned for part in parts if (cleaned := clean_name(part))[0]]
    full, note = clean_name(ingredient.name)
    return [(name, note) for name in (_split_staples(full, pantry) if full else ())]


def _fruit(name: str, amount: float | None, unit: str | None):
    """ "1 msk citronskal", "limeklyftor": bought as the fruit. (name, amount, unit, note)"""
    match = _FRUIT_PART.match(name)
    if not match:
        return name, amount, unit, ""
    zest = match[2] == "skal"
    if amount is not None:
        if zest and dimension(unit) == "volume":
            amount = to_base(amount, unit) / ZEST_ML_PER_FRUIT
        elif not zest and dimension(unit) == "count":
            amount /= WEDGES_PER_FRUIT
        else:
            return name, amount, unit, ""
    return match[1], amount, None, name


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
            for name, note in _names(ingredient, pantry):
                amount = ingredient.amount
                if amount is not None:
                    amount *= multiplier
                name, amount, unit, part_of = _fruit(name, amount, ingredient.unit)
                note = note or part_of
                # A substitute joins the same product bought anyway ("tofu"), but is
                # kept apart from staples, so "glutenfritt mjöl" is never skipped.
                key = (singular(name), special and is_pantry(name, pantry))
                product = products.setdefault(key, _Product(name))
                dim = dimension(unit) if amount is not None else "none"
                part = product.parts.get(dim)
                if part is None:
                    item = ShoppingItem(name=name, special=special)
                    part = product.parts[dim] = _Part(item, unit)
                part.item.special = part.item.special or special
                if day.recipe.title not in part.item.recipes:
                    part.item.recipes.append(day.recipe.title)
                _add_note(part.item, note)
                if special:
                    _add_note(part.item, substitute_note(name))
                if amount is not None:
                    part.total += to_base(amount, unit)
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
