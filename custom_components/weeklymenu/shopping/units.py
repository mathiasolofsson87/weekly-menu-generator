"""Unit handling: merge amounts in a common unit, show them as something you can buy."""

from __future__ import annotations

import math

# unit -> millilitres
VOLUME = {"ml": 1, "cl": 10, "dl": 100, "l": 1000, "msk": 15, "tsk": 5, "krm": 1}
# unit -> grams
WEIGHT = {"g": 1, "kg": 1000}
# Counted things. A missing unit counts as "st".
COUNT = {"st", None}


# Grams per millilitre, for products bought by weight but measured with spoons too.
# Only where it is safe to say; anything else keeps volume and weight as two lines.
DENSITY = {"smör": 0.9, "margarin": 0.9}
# The sizes (ml) a product is sold in, matched on its last word. Only common products
# whose packs are the same in every shop; a liquid amount is rounded up to whole packs.
PACK_SIZES = {
    "mjölk": (1000, 1500), "filmjölk": (1000,), "yoghurt": (500, 1000),
    "matyoghurt": (500, 1000),
    "vispgrädde": (200, 300, 500), "grädde": (200, 300, 500),
    "matlagningsgrädde": (250, 500), "gräddfil": (300, 500),
    "kokosmjölk": (400,), "havredryck": (1000,),
}  # fmt: skip


def last_word(name: str) -> str:
    return name.casefold().rsplit(" ", 1)[-1]


def to_packs(total_ml: float, name: str) -> float:
    """The least you can buy of `name` that holds `total_ml`; `total_ml` if unknown."""
    sizes = PACK_SIZES.get(last_word(name))
    if not sizes or total_ml <= 0:
        return total_ml
    best, sums, seen = math.inf, [0], set()
    while sums:  # every mix of packs below the total, one more pack at a time
        grown = [s + size for s in sums for size in sizes]
        best = min([best] + [s for s in grown if s >= total_ml - 0.001])
        sums = [s for s in grown if s < total_ml - 0.001 and s not in seen]
        seen.update(sums)
    return best


def dimension(unit: str | None) -> str:
    """Which amounts can be added together."""
    if unit in VOLUME:
        return "volume"
    if unit in WEIGHT:
        return "weight"
    if unit in COUNT:
        return "count"
    return f"unit:{unit}"  # förp, burk, klyfta...: only added to the same unit


def to_base(amount: float, unit: str | None) -> float:
    return amount * (VOLUME.get(unit) or WEIGHT.get(unit) or 1)


def _ceil_to(value: float, step: float) -> float:
    # The tolerance keeps 400.0002 g (a one-third share of 1.2 kg) from rounding up to 405.
    return round(math.ceil(round(value / step, 3)) * step, 6)


def display(
    total: float, dim: str, unit: str | None, metric_only: bool
) -> tuple[float, str | None]:
    """A bought amount for `total` base units, rounded up (you cannot buy 0.3 of a pack).

    `unit` is the unit of the first contribution; it is kept for counted things and for
    units that cannot be converted."""
    if dim == "weight":
        if total >= 1000:
            return _ceil_to(total / 1000, 0.1), "kg"
        return _ceil_to(total, 5 if total >= 50 else 1), "g"
    if dim == "volume":
        if total >= 1000:
            return _ceil_to(total / 1000, 0.1), "l"
        if metric_only:
            return _ceil_to(total, 10 if total >= 100 else 5), "ml"
        if total >= 50:
            return _ceil_to(total / 100, 0.5), "dl"
        if total >= 15:
            return _ceil_to(total / 15, 0.5), "msk"
        if total >= 2:  # 3 ml is "1 tsk" on a list, not "3 krm"
            return _ceil_to(total / 5, 0.5), "tsk"
        return _ceil_to(total, 1), "krm"
    return float(math.ceil(round(total, 6))), unit
