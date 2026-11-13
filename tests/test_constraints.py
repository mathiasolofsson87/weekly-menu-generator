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
from custom_components.weeklymenu.planner.eligibility import assess
from custom_components.weeklymenu.planner.substitutes import kind_of
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
        ("1 kruka färsk timjan", False),
        ("1 kruka färsk oregano", False),
        ("2 msk färska örter", False),
        ("500 g färsk spenat", False),
        ("500 g färs", True),
        ("500 g blandfärs", True),
        ("500 g färsk nötfärs", True),
        ("2 st färsk kyckling", True),
        ("1 st hönsbuljongtärning", True),
        ("5 dl hönsbuljong", True),
        ("1 st grönsaksbuljongtärning", False),
        ("400 g vegetariska kycklingbitar", False),
        ("300 g vegobullar", False),
        ("140 g vegetariskt bacon", False),
    ],
)
def test_meat_cuts_and_lookalikes(text, is_meat) -> None:
    assert (MEAT.match(text) is not None) is is_meat


@pytest.mark.parametrize(
    ("wish", "wanted", "unwanted"),
    [
        ("not fish", (), ("fish",)),
        ("inte fisk", (), ("fisk",)),
        ("gärna något med pasta, men inte fisk", ("pasta",), ("fisk",)),
        ("something with chicken and no shellfish", ("chicken",), ("shellfish",)),
        ("", (), ()),
        (None, (), ()),
    ],
)
def test_wishes_are_split_into_wanted_and_unwanted(wish, wanted, unwanted) -> None:
    from custom_components.weeklymenu.planner.wishes import Wishes

    parsed = Wishes.parse(wish)
    assert (parsed.wanted, parsed.unwanted) == (wanted, unwanted)


def test_wish_groups_use_the_food_rules() -> None:
    from custom_components.weeklymenu.planner.wishes import Wishes

    assert not Wishes.parse("no fish").allows(recipe("Gryta", "400 g torsk"))
    assert not Wishes.parse("inte kött").allows(recipe("Gryta", "400 g nötfärs"))
    assert Wishes.parse("inte fisk").allows(recipe("Gryta", "400 g nötfärs"))
    assert Wishes.parse("pasta").bonus(recipe("Pastagratäng", "400 g pasta")) > 0


# --- substitutes respect the allergen filter (planner/substitutes.py) -------------


def _swaps(rec, *members):
    """(original, replacement) of the split, or None when the recipe is refused."""
    result = assess(rec, [member("Olle"), *members])
    if not result.ok:
        return None
    return [
        (s.original, s.replacement)
        for g in result.split.groups
        for s in g.substitutions
    ]


def _swapped(rec, *members):
    """Every replacement name the split gives, or None when the recipe is refused."""
    swaps = _swaps(rec, *members)
    return None if swaps is None else [new.name for _, new in swaps]


SPLIT_DISHES = [
    recipe("Pasta bolognese", "500 g nötfärs", "400 g pasta"),
    recipe("Tacos", "500 g nötfärs", "8 st tortillabröd"),
    recipe("Pasta med köttbullar", "20 st köttbullar", "400 g pasta"),
    recipe("Korvstroganoff", "500 g falukorv", "3 dl ris"),
    recipe("Carbonara", "2 förp bacon (à 140 g)", "400 g pasta"),
    recipe("Kycklingwok", "600 g kycklingfilé", "300 g broccoli"),
    recipe("Kycklinggryta", "600 g kycklinglårfilé", "2 dl kokosmjölk"),
    recipe("Lax i ugn", "600 g laxfilé", "1 kg potatis"),
    recipe("Räkpasta", "300 g räkor", "400 g pasta"),
    recipe("Kalops", "1 kg nötkött", "2 msk konc kalvfond"),
    recipe("Fiskpinnar med mos", "16 st fiskpinnar", "1 kg potatis"),
]


@pytest.mark.parametrize("rec", SPLIT_DISHES, ids=lambda r: r.title)
@pytest.mark.parametrize(
    "allergy", ["soy", "gluten", "egg", "milk", "celery", "sesame"]
)
def test_a_substitute_never_holds_the_vegetarians_allergen(rec, allergy) -> None:
    swaps = _swaps(rec, member("Anna", diet="vegetarian", allergies=[allergy]))
    if swaps is None:
        return  # refused is safe
    rule = ALLERGEN_RULES[allergy]
    for original, new in swaps:
        assert not rule.match(new.name), new.name
        option = next(
            o
            for o in kind_of(original.raw).replacements
            if o.render(original.name) == new.name
        )
        assert allergy not in option.contains + option.traces, new.name


@pytest.mark.parametrize(
    ("allergy", "never"),
    [
        ("soy", {"tofu", "rökt tofu", "vegofärs", "vegetariska kycklingbitar", "vegokorv",
                 "vegobullar", "vegetariskt bacon", "vegetariska fiskpinnar"}),
        ("gluten", {"vegofärs", "vegetariska kycklingbitar", "vegokorv", "vegobullar",
                    "vegetariskt bacon", "falafel"}),
        ("egg", {"vegofärs", "vegetariska kycklingbitar", "vegokorv", "vegobullar"}),
        ("milk", {"halloumi", "vegetariska kycklingbitar"}),
        ("celery", {"grönsaksbuljongtärning", "konc grönsaksfond"}),
    ],
)  # fmt: skip
def test_processed_substitutes_are_kept_from_allergies_by_what_they_declare(
    allergy, never
) -> None:
    for rec in SPLIT_DISHES:
        names = _swapped(rec, member("Anna", diet="vegetarian", allergies=[allergy]))
        assert not set(names or ()) & never, (rec.title, names)


def test_celery_allergy_refuses_a_meat_stock_swap() -> None:
    # vegetable stock usually holds celery, and the stock cannot be left out
    kalops = recipe("Kalops", "1 kg nötkött", "1 st köttbuljongtärning")
    vegetarian = member("Anna", diet="vegetarian", allergies=["celery"])
    assert _swapped(kalops, vegetarian) is None


def test_a_vegan_may_get_a_vegan_brand_but_never_halloumi() -> None:
    vegan = member("Vera", diet="vegan")
    assert _swapped(SPLIT_DISHES[0], vegan) == ["vegofärs"]  # traces are not a diet
    grill = recipe("Grillad kyckling", "600 g kycklingfilé")
    assert "halloumi" not in (_swapped(grill, vegan) or [])
