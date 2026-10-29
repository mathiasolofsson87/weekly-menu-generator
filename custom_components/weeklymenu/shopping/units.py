"""Unit handling: merge amounts in a common unit, show them as something you can buy."""

from __future__ import annotations

import math

# unit -> millilitres
VOLUME = {"ml": 1, "cl": 10, "dl": 100, "l": 1000, "msk": 15, "tsk": 5, "krm": 1}
# unit -> grams
WEIGHT = {"g": 1, "kg": 1000}
# Counted things. A missing unit counts as "st".
COUNT = {"st", None}


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
