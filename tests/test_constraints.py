"""Allergen, diet and preference checks. These protect people, so they are thorough."""

import pytest

from custom_components.weeklymenu.planner.allergens import ALLERGEN_RULES, MEAT
from custom_components.weeklymenu.planner.constraints import (
    hard_violations,
    has_fish,
    is_allowed,
    is_vegetarian,
    preference_hits,
)
from tests.helpers import CURRY, LAX, PASTA, STEW, STIR, TACOS, member, recipe


@pytest.mark.parametrize(
    ("allergen", "text", "expected"),
    [
        ("milk", "2 dl mjölk", True),
        ("milk", "100 g fetaost", True),
        ("milk", "riven ost", True),
        ("milk", "1 dl kokosmjölk", False),
        ("milk", "2 dl sojayoghurt", False),
        ("milk", "2 dl matyoghurt (10%)", True),
        ("milk", "2 dl havrefraiche", False),
        ("milk", "3 msk jordnötssmör", False),
        ("milk", "växtbaserad grädde", False),
        ("milk", "rostade nötter", False),
        ("milk", "laktosfri mjölk", True),  # still milk
        ("lactose", "laktosfri mjölk", False),
        ("lactose", "2 dl mjölk", True),
        ("egg", "3 ägg", True),
        ("egg", "2 eggs", True),
        ("egg", "1 aubergine", False),
        ("egg", "1 äggplanta", False),
        ("egg", "veggie burgare", False),
        ("gluten", "2 dl vetemjöl", True),
        ("gluten", "400 g spaghetti", True),
        ("gluten", "2 dl mandelmjöl", False),
        ("gluten", "glutenfri pasta", False),
        ("gluten", "1 tsk pepparkorn", False),
        ("gluten", "250 g risnudlar", False),
        ("fish", "600 g laxfilé", True),
        ("fish", "1 burk tonfisk", True),
        ("fish", "1 klass", False),
        ("crustaceans", "300 g räkor", True),
        ("crustaceans", "10 rädisor", False),
        ("molluscs", "500 g musslor", True),
        ("peanuts", "jordnötssmör", True),
        ("tree_nuts", "50 g valnötter", True),
        ("tree_nuts", "500 g nötfärs", False),
        ("tree_nuts", "1 krm muskotnöt", False),
        ("soy", "2 msk sojasås", True),
        ("sesame", "1 msk tahini", True),
        ("celery", "1 stjälk selleri", True),
        ("mustard", "1 msk dijonsenap", True),
    ],
)
def test_allergen_rules(allergen, text, expected) -> None:
    assert (ALLERGEN_RULES[allergen].match(text) is not None) is expected


def test_every_selectable_allergen_has_a_rule() -> None:
    from custom_components.weeklymenu.const import ALLERGENS

    assert set(ALLERGENS) <= set(ALLERGEN_RULES)


def test_allergy_blocks_only_that_member() -> None:
    anna, olle = member("Anna", allergies=["milk"]), member("Olle")
    assert not is_allowed(TACOS, [anna, olle])
    assert is_allowed(TACOS, [olle])
    [violation] = hard_violations(TACOS, [anna])
    assert (violation.member, violation.kind, violation.term) == (
        "Anna",
        "allergy",
        "milk",
    )


def test_allergen_in_title_counts() -> None:
    assert not is_allowed(
        recipe("Räkpasta", "400 g pasta"), [member("A", allergies=["crustaceans"])]
    )


def test_custom_allergy_is_substring_match() -> None:
    assert not is_allowed(
        recipe("Fruktsallad", "2 st kiwi"), [member("A", allergies=["kiwi"])]
    )
    assert is_allowed(
        recipe("Fruktsallad", "2 st banan"), [member("A", allergies=["kiwi"])]
    )


@pytest.mark.parametrize(
    ("diet", "rec", "allowed"),
    [
        ("vegetarian", STEW, False),
        ("vegetarian", LAX, False),
        ("vegetarian", CURRY, True),
        ("vegetarian", STIR, True),
        ("vegetarian", recipe("Vegogryta", "400 g vegofärs", "1 st lök"), True),
        ("vegetarian", recipe("Gelé", "4 blad gelatin"), False),
        ("pescatarian", LAX, True),
        ("pescatarian", STEW, False),
        ("vegan", recipe("Gryta", "1 burk kikärtor", "1 dl kokosmjölk"), True),
        ("vegan", recipe("Pannkaka", "3 ägg", "3 dl mjölk"), False),
        ("vegan", recipe("Sallad", "2 msk honung"), False),
        ("omnivore", STEW, True),
    ],
)
def test_diets(diet, rec, allowed) -> None:
    assert is_allowed(rec, [member("A", diet=diet)]) is allowed


def test_meat_rule_ignores_vegetarian_products() -> None:
    assert MEAT.match("1 st vegetarisk korv") is None
    assert MEAT.match("400 g sojafärs") is None
    assert MEAT.match("400 g köttfärs") == "kött"


def test_vegetarian_and_fish_helpers() -> None:
    assert is_vegetarian(CURRY) and not is_vegetarian(PASTA)
    assert has_fish(LAX) and not has_fish(CURRY)


def test_preferences_are_soft() -> None:
    fan = member("Anna", likes=["tomat"], dislikes=["lök"])
    assert is_allowed(CURRY, [fan])
    assert preference_hits(CURRY, [fan]) == (1, 0)
    assert preference_hits(TACOS, [fan]) == (0, 1)


@pytest.mark.parametrize(
    ("text", "is_meat"),
    [
        ("600 g entrecote", True),
        ("2 st entrecôte", True),
        ("500 g oxfilé", True),
        ("800 g högrev", True),
        ("4 st fläskkarré", True),
        ("6 st korv", True),
        ("6 st korvbröd", False),
        ("4 st hamburgerbröd", False),
        ("4 st hamburgare", True),
        ("1 pkt vegofärs", False),
    ],
)
def test_meat_cuts_and_lookalikes(text, is_meat) -> None:
    assert (MEAT.match(text) is not None) is is_meat
