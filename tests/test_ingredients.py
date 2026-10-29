"""Ingredient parsing."""

import pytest

from custom_components.weeklymenu.planner.ingredients import parse_ingredient


@pytest.mark.parametrize(
    ("line", "name", "amount", "unit"),
    [
        ("350 g nötfärs", "nötfärs", 350, "g"),
        ("2 st gul lök", "gul lök", 2, "st"),
        ("1,5 dl grädde", "grädde", 1.5, "dl"),
        ("1/2 dl olja", "olja", 0.5, "dl"),
        ("1 1/2 msk smör", "smör", 1.5, "msk"),
        ("½ tsk salt", "salt", 0.5, "tsk"),
        ("2-3 klyftor vitlök", "vitlök", 3, "klyfta"),
        ("ca 2 dl ris", "ris", 2, "dl"),
        ("2 gula lökar", "gula lökar", 2, None),
        ("3 ägg", "ägg", 3, None),
        ("400 g spaghetti (ca 4 port)", "spaghetti", 400, "g"),
        ("1 gul lök, finhackad", "gul lök", 1, None),
        ("2 tbsp olive oil", "olive oil", 2, "msk"),
        ("1 cup milk", "milk", 2.4, "dl"),
        ("4 oz cheese", "cheese", 113.4, "g"),
        ("salt", "salt", None, None),
        ("Salt och peppar", "salt och peppar", None, None),
    ],
)
def test_parse(line, name, amount, unit) -> None:
    parsed = parse_ingredient(line)
    assert (parsed.name, parsed.amount, parsed.unit) == (name, amount, unit)
    assert parsed.raw == line


def test_bare_number_is_not_an_ingredient() -> None:
    parsed = parse_ingredient("4")
    assert parsed.amount is None
    assert parsed.name == "4"
