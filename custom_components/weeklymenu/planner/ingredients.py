"""Parse free-text ingredient lines ("350 g nötfärs") into structured ingredients."""

from __future__ import annotations

import re

from .models import Ingredient

# unit text -> (canonical unit, factor to apply to the amount)
_UNITS: dict[str, tuple[str, float]] = {
    "g": ("g", 1),
    "gr": ("g", 1),
    "gram": ("g", 1),
    "kg": ("kg", 1),
    "hg": ("g", 100),
    "ml": ("ml", 1),
    "cl": ("cl", 1),
    "dl": ("dl", 1),
    "l": ("l", 1),
    "liter": ("l", 1),
    "msk": ("msk", 1),
    "tsk": ("tsk", 1),
    "krm": ("krm", 1),
    "st": ("st", 1),
    "stycken": ("st", 1),
    "styck": ("st", 1),
    "förp": ("förp", 1),
    "förpackning": ("förp", 1),
    "burk": ("burk", 1),
    "burkar": ("burk", 1),
    "klyfta": ("klyfta", 1),
    "klyftor": ("klyfta", 1),
    "port": ("port", 1),
    "nypa": ("nypa", 1),
    "knippe": ("knippe", 1),
    "tbsp": ("msk", 1),
    "tsp": ("tsk", 1),
    "cup": ("dl", 2.4),
    "cups": ("dl", 2.4),
    "oz": ("g", 28.35),
    "lb": ("g", 453.6),
    "lbs": ("g", 453.6),
    "pinch": ("nypa", 1),
    "clove": ("klyfta", 1),
    "cloves": ("klyfta", 1),
}
_FRACTIONS = {"½": 0.5, "¼": 0.25, "¾": 0.75, "⅓": 1 / 3, "⅔": 2 / 3}

_NUM = r"(?:\d+\s+\d+/\d+|\d+/\d+|\d+(?:[.,]\d+)?|[½¼¾⅓⅔])"
_LINE = re.compile(
    rf"^\s*(?:ca\.?\s+|cirka\s+|about\s+)?(?P<a>{_NUM})(?:\s*[-–]\s*(?P<b>{_NUM}))?\s*(?P<rest>.*)$",
    re.IGNORECASE,
)


def _number(text: str) -> float:
    text = text.strip()
    if text in _FRACTIONS:
        return _FRACTIONS[text]
    if "/" in text:
        whole, _, frac = text.rpartition(" ")
        num, den = frac.split("/")
        return (float(whole) if whole else 0.0) + float(num) / float(den)
    return float(text.replace(",", "."))


def _clean_name(text: str) -> str:
    text = re.sub(r"\(.*?\)", " ", text)  # notes such as "(ca 200 g)"
    text = text.split(",")[0]  # drop preparation such as ", finhackad"
    return re.sub(r"\s+", " ", text).strip().casefold()


def parse_ingredient(line: str) -> Ingredient:
    """Parse one line. Lines without an amount keep only a name."""
    raw = line.strip()
    match = _LINE.match(raw)
    if not match:
        return Ingredient(name=_clean_name(raw) or raw.casefold(), raw=raw)

    # A range such as "2-3" is planned for at its upper end.
    amount = _number(match["b"] or match["a"])
    rest = match["rest"].strip()
    unit: str | None = None

    first, _, remainder = rest.partition(" ")
    key = first.rstrip(".").casefold()
    if key in _UNITS and remainder.strip():
        unit, factor = _UNITS[key]
        amount *= factor
        rest = remainder.strip()

    name = _clean_name(rest)
    if not name:  # a bare number is not an ingredient
        return Ingredient(name=raw.casefold(), raw=raw)
    return Ingredient(name=name, amount=round(amount, 3), unit=unit, raw=raw)
