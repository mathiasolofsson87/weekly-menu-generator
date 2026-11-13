"""Menu -> shopping items: scaling, split shares, merging, rounding and pantry."""

import pytest

from custom_components.weeklymenu.planner.eligibility import assess
from custom_components.weeklymenu.planner.generator import PlannerSettings
from custom_components.weeklymenu.planner.models import Menu, MenuDay
from custom_components.weeklymenu.shopping.aggregate import (
    DEFAULT_PANTRY,
    aggregate,
    clean_name,
    is_pantry,
    portions_factor,
)
from custom_components.weeklymenu.shopping.models import SKIPPED, ShoppingItem
from tests.helpers import member, recipe

WEEK = ["mon", "tue", "wed", "thu", "fri"]


def menu_of(*recipes_and_splits) -> Menu:
    days = []
    for index, entry in enumerate(recipes_and_splits):
        rec, split = entry if isinstance(entry, tuple) else (entry, None)
        days.append(
            MenuDay(f"2026-11-0{2 + index}", WEEK[index], rec, [rec], split=split)
        )
    return Menu("2026-11-02", status="confirmed", days=days)


def servings(rec, n):
    rec.servings = n
    return rec


def settings(*members) -> PlannerSettings:
    return PlannerSettings(dinner_days=WEEK, members=list(members))


def lines(result):
    return {i.name: i.text("en") for i in result.items}


# --- names -------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("raw", "short", "note"),
    [
        (
            "nötfärs gärna icas nötfärs 12% eller hushållsfärs",
            "nötfärs",
            "nötfärs gärna icas nötfärs 12% eller hushållsfärs",
        ),
        (
            "falukorv eller kycklingstekkorv",
            "falukorv",
            "falukorv eller kycklingstekkorv",
        ),
        ("hela tomater", "hela tomater", ""),
        ("gul lök", "gul lök", ""),
        ("mjölk 3%", "mjölk", "mjölk 3%"),
        ("riven ost, gärna lagrad", "riven ost", "riven ost, gärna lagrad"),
        # a hyphen joins the alternatives: "udon-" alone would be no product
        ("udon- eller äggnudlar", "udon- eller äggnudlar", ""),
        ("solrosskott eller ärtskott", "solrosskott", "solrosskott eller ärtskott"),
        # preparation is cut
        ("hackad dill", "dill", "hackad dill"),
        ("finskurna salladslök", "salladslök", "finskurna salladslök"),
        ("fint hackad persilja", "persilja", "fint hackad persilja"),
        ("citron i klyftor", "citron", "citron i klyftor"),
        ("fisk i tärningar", "fisk", "fisk i tärningar"),
        ("ost i skivor", "ost", "ost i skivor"),
        ("rostade sesamfrön", "sesamfrön", "rostade sesamfrön"),
        ("kokt potatis i bitar", "potatis", "kokt potatis i bitar"),
        # ...but not what makes it a different product
        ("rostad lök", "rostad lök", ""),
        ("krossade tomater", "krossade tomater", ""),
        ("kräftstjärtar i lake", "kräftstjärtar i lake", ""),
        ("vita bönor i tomatsås", "vita bönor i tomatsås", ""),
        ("frysta laxtärningar", "frysta laxtärningar", ""),
        ("färsk bladspenat", "färsk bladspenat", ""),
        ("grovt salt", "grovt salt", ""),
        ("tofu", "tofu", ""),
        ("hackad", "hackad", ""),  # nothing would be left
    ],
)
def test_clean_name(raw, short, note) -> None:
    assert clean_name(raw) == (short, note)


@pytest.mark.parametrize(
    ("name", "staple"),
    [
        ("salt", True),
        ("salt och peppar", True),
        ("svartpeppar", True),
        ("rapsolja", True),
        ("olivolja", True),
        ("vetemjöl", True),
        ("saltgurka", False),
        ("sojasås", False),
        ("smör", False),
        ("kokosmjölk", False),
    ],
)
def test_pantry_matches_whole_words(name, staple) -> None:
    assert is_pantry(name, DEFAULT_PANTRY) is staple


# --- scaling ------------------------------------------------------------------------


def test_portions_factor() -> None:
    assert portions_factor(4, [member("A"), member("B")]) == 0.5
    mixed = [member("A", portion="large"), member("B"), member("C", portion="small")]
    assert portions_factor(4, mixed) == 0.75  # (1.4 + 1 + 0.6) / 4
    assert portions_factor(None, [member("A")]) == 1.0  # recipe does not say
    assert portions_factor(4, []) == 1.0  # nobody configured


def test_amounts_follow_who_eats() -> None:
    rec = servings(recipe("Köttfärssås", "400 g nötfärs", "2 st gul lök"), 4)
    result = aggregate(menu_of(rec), settings(member("A"), member("B")), ())
    assert lines(result) == {"gul lök": "1 st gul lök", "nötfärs": "200 g nötfärs"}


def test_without_members_the_recipe_is_bought_as_written() -> None:
    rec = servings(recipe("Sås", "400 g nötfärs"), 4)
    assert lines(aggregate(menu_of(rec), settings(), ())) == {
        "nötfärs": "400 g nötfärs"
    }


# --- merging --------------------------------------------------------------------------


def test_same_ingredient_in_two_recipes_is_added_up() -> None:
    a = servings(recipe("A", "2 dl grädde", "300 g potatis"), 2)
    b = servings(recipe("B", "1 dl grädde", "700 g potatis"), 2)
    result = aggregate(menu_of(a, b), settings(member("X"), member("Y")), ())
    assert lines(result) == {"grädde": "3 dl grädde", "potatis": "1 kg potatis"}
    assert result.items[0].recipes == ["A", "B"]


def test_units_of_one_kind_are_converted_before_adding() -> None:
    a = servings(recipe("A", "1 dl buljong", "1 msk smör", "1 kg potatis"), 1)
    b = servings(recipe("B", "5 msk buljong", "100 g smör", "300 g potatis"), 1)
    result = aggregate(menu_of(a, b), settings(member("X")), ())
    # 100 ml + 75 ml = 175 ml, rounded up to the next half dl; butter is weighed
    # (15 ml at 0.9 g/ml + 100 g), rounded up to 5 g
    assert sorted(i.text("en") for i in result.items) == [
        "1.3 kg potatis",
        "115 g smör",
        "2 dl buljong",
    ]


def test_volume_and_weight_stay_separate_without_a_known_density() -> None:
    a = servings(recipe("A", "3 dl kimchi"), 1)
    b = servings(recipe("B", "100 g kimchi"), 1)
    result = aggregate(menu_of(a, b), settings(member("X")), ())
    assert sorted(i.text("en") for i in result.items) == ["100 g kimchi", "3 dl kimchi"]


def test_packs_take_in_amounts_of_unknown_size() -> None:
    # 1 pack, nothing left over, so the 2 dl needs one more pack; the note keeps it.
    a = servings(recipe("A", "2 dl grädde"), 1)
    b = servings(recipe("B", "1 förp grädde"), 1)
    [item] = aggregate(menu_of(a, b), settings(member("X")), ()).items
    assert item.text("en") == "2 förp grädde"
    assert item.note == "+ 2 dl grädde" and item.recipes == ["B", "A"]


def test_packs_count_measured_amounts_by_their_size() -> None:
    a = servings(recipe("A", "1 förp tofu (à 400 g)"), 1)
    b = servings(recipe("B", "100 g tofu"), 1)
    c = servings(recipe("C", "1 burk tofu"), 1)
    result = aggregate(menu_of(a, b), settings(member("X")), ())
    assert lines(result) == {"tofu": "2 förp tofu"}  # 1 + 100/400 packs, rounded up
    # Any pack unit counts as a pack; pieces and grams of unknown size fit in the
    # half pack that rounding up leaves over.
    d = servings(recipe("D", "1/2 förp salladslök", "2 salladslökar"), 1)
    result = aggregate(menu_of(c, d), settings(member("X")), ())
    assert lines(result) == {"tofu": "1 burk tofu", "salladslök": "1 förp salladslök"}
    result = aggregate(menu_of(a, c), settings(member("X")), ())
    assert lines(result) == {"tofu": "2 förp tofu"}


def test_substitute_tofu_from_three_kinds_of_fish_is_one_line() -> None:
    # Fish in grams, in packs and in a tin, each with its size: all become grams.
    rec = servings(
        recipe(
            "Fiskpasta",
            "400 g fisk i tärningar",
            "1 förp frysta laxtärningar (à 300 g)",
            "1 burk kräftstjärtar i lake (à 170 g)",
            "4 port spaghetti",
        ),
        4,
    )
    anna, olle = member("Anna", diet="vegetarian"), member("Olle")
    split = assess(rec, [olle, anna]).split
    result = aggregate(menu_of((rec, split)), settings(olle, anna), ())
    assert lines(result)["tofu"] == "220 g tofu"  # (400 + 300 + 170) g / 4, rounded up
    assert [i.name for i in result.items].count("tofu") == 1


def test_counted_things_are_rounded_up() -> None:
    rec = servings(recipe("A", "1 st gul lök", "3 ägg"), 4)
    result = aggregate(menu_of(rec), settings(member("X")), ())
    assert lines(result) == {
        "gul lök": "1 st gul lök",
        "ägg": "1 ägg",
    }  # 0.25 onion, 0.75 egg


def test_swedish_and_metric_units() -> None:
    rec = servings(recipe("A", "3 dl grädde", "2 msk smör"), 1)
    assert lines(aggregate(menu_of(rec), settings(member("X")), ())) == {
        "grädde": "3 dl grädde",
        "smör": "2 msk smör",
    }
    metric = aggregate(menu_of(rec), settings(member("X")), (), metric_only=True)
    assert lines(metric) == {"grädde": "300 ml grädde", "smör": "30 ml smör"}


def test_items_without_an_amount_are_merged_by_name() -> None:
    a = servings(recipe("A", "hackad persilja", "1 st lök"), 1)
    b = servings(recipe("B", "persilja"), 1)
    result = aggregate(menu_of(a, b), settings(member("X")), ())
    parsley = next(i for i in result.items if i.name == "persilja")
    assert parsley.amount is None and parsley.recipes == ["A", "B"]


def test_a_line_without_an_amount_joins_one_with_an_amount() -> None:
    a = servings(recipe("A", "dill"), 1)
    b = servings(recipe("B", "1 kruka dill"), 1)
    assert lines(aggregate(menu_of(a, b), settings(member("X")), ())) == {
        "dill": "1 kruka dill"
    }


def test_preparation_is_cut_and_the_same_product_merges() -> None:
    a = servings(
        recipe("A", "1/2 citron i klyftor", "1 msk rostade sesamfrön", "2 tomater"),
        1,
    )
    b = servings(
        recipe("B", "1 citron", "1 1/2 msk sesamfrö", "1 tomat", "100 g ost i skivor"),
        1,
    )
    result = aggregate(menu_of(a, b), settings(member("X")), ())
    assert lines(result) == {
        "citroner": "2 citroner",  # 0.5 + 1, rounded up, in the plural
        "sesamfrön": "2.5 msk sesamfrön",
        "tomater": "3 tomater",
        "ost": "100 g ost",
    }
    lemon = next(i for i in result.items if i.name == "citroner")
    assert lemon.note == "citron i klyftor"  # the recipe's wording is kept


def test_singular_and_plural_merge_into_the_right_number() -> None:
    a = servings(recipe("A", "2 gula lökar", "3 vitlöksklyftor"), 4)
    b = servings(recipe("B", "1 gul lök", "1 vitlöksklyfta"), 2)
    result = aggregate(menu_of(a, b), settings(member("X")), ())
    assert lines(result) == {
        "gul lök": "1 gul lök",  # 0.5 + 0.5
        "vitlöksklyftor": "2 vitlöksklyftor",  # 0.75 + 0.5, rounded up
    }


def test_liquids_are_rounded_up_to_whole_packs() -> None:
    a = servings(recipe("A", "2 1/2 dl mjölk", "1 dl vispgrädde", "2 dl buljong"), 1)
    b = servings(recipe("B", "4 dl mjölk", "3 dl kokosmjölk"), 1)
    result = aggregate(menu_of(a, b), settings(member("X")), ())
    assert lines(result) == {
        "mjölk": "1 l mjölk",  # 6.5 dl; sold as 1 l and 1.5 l
        "vispgrädde": "2 dl vispgrädde",
        "kokosmjölk": "4 dl kokosmjölk",  # one tin
        "buljong": "2 dl buljong",  # no known pack: as needed
    }
    more = servings(recipe("C", "1 1/2 l mjölk"), 1)
    assert (
        lines(aggregate(menu_of(a, b, more), settings(member("X")), ()))["mjölk"]
        == "2.5 l mjölk"
    )  # 2.15 l: one 1 l and one 1.5 l pack


def test_a_shortened_name_keeps_the_original_wording() -> None:
    rec = servings(recipe("A", "350 g nötfärs gärna 12% eller hushållsfärs"), 1)
    [item] = aggregate(menu_of(rec), settings(member("X")), ()).items
    assert item.name == "nötfärs" and "hushållsfärs" in item.note


def test_days_without_a_recipe_are_ignored() -> None:
    menu = Menu("2026-11-02", days=[MenuDay("2026-11-02", "mon", None, [])])
    assert aggregate(menu, settings(member("X")), ()).items == []


# --- pantry --------------------------------------------------------------------------


def test_pantry_staples_are_reported_not_bought() -> None:
    rec = servings(
        recipe("A", "1 tsk salt", "1 krm svartpeppar", "2 msk olivolja", "400 g pasta"),
        1,
    )
    result = aggregate(menu_of(rec), settings(member("X")), DEFAULT_PANTRY)
    assert [i.name for i in result.items] == ["pasta"]
    assert sorted(i.name for i in result.skipped) == ["olivolja", "salt", "svartpeppar"]
    assert all(i.status == SKIPPED for i in result.skipped)


def test_salt_and_pepper_are_split_and_listed_once() -> None:
    a = servings(recipe("A", "salt och peppar", "1/2 tsk salt", "1 krm peppar"), 1)
    b = servings(recipe("B", "salt", "peppar", "1 krm peppar", "dill och persilja"), 1)
    result = aggregate(menu_of(a, b), settings(member("X")), DEFAULT_PANTRY)
    assert sorted(i.text("en") for i in result.skipped) == [
        "0.5 tsk peppar",  # 2 krm
        "0.5 tsk salt",
    ]
    # only staples are split: other lines are bought as written
    assert [i.name for i in result.items] == ["dill och persilja"]


def test_an_empty_pantry_buys_everything() -> None:
    rec = servings(recipe("A", "1 tsk salt"), 1)
    assert [
        i.name for i in aggregate(menu_of(rec), settings(member("X")), ()).items
    ] == ["salt"]


def test_substitutes_are_never_skipped_as_staples() -> None:
    pasta = servings(recipe("Bakverk", "3 dl vetemjöl", "1 st ägg"), 2)
    gita = member("Gita", allergies=["gluten"])
    eligibility = assess(pasta, [member("Olle"), gita])
    assert eligibility.ok
    result = aggregate(
        menu_of((pasta, eligibility.split)),
        settings(member("Olle"), gita),
        DEFAULT_PANTRY,
    )
    assert "glutenfritt mjöl" in [i.name for i in result.items if i.special]
    assert [i.name for i in result.skipped] == [
        "vetemjöl"
    ]  # the ordinary flour is a staple


# --- split dinners -----------------------------------------------------------------------


def test_a_split_buys_the_original_and_the_substitute_for_their_shares() -> None:
    steak = servings(recipe("Biff", "600 g entrecote", "800 g potatis"), 2)
    olle, anna = member("Olle"), member("Anna", diet="vegetarian")
    split = assess(steak, [olle, anna]).split
    result = aggregate(menu_of((steak, split)), settings(olle, anna), ())
    assert lines(result) == {
        "entrecote": "300 g entrecote",  # Olle's half
        "potatis": "800 g potatis",
        "tofu": "300 g tofu",  # Anna's half
    }
    assert next(i for i in result.items if i.name == "tofu").special is True


def test_two_groups_replacing_the_same_line_share_it() -> None:
    steak = servings(recipe("Biff", "600 g entrecote", "800 g potatis"), 3)
    olle, anna, vera = (
        member("Olle"),
        member("Anna", diet="vegetarian"),
        member("Vera", diet="vegan"),
    )
    split = assess(steak, [olle, anna, vera]).split
    assert len(split.groups) == 1  # same needs, one version
    result = aggregate(menu_of((steak, split)), settings(olle, anna, vera), ())
    assert lines(result)["entrecote"] == "200 g entrecote"  # only Olle eats it
    assert lines(result)["tofu"] == "400 g tofu"  # Anna and Vera


def test_diet_and_allergy_versions_each_get_their_swap() -> None:
    steak = servings(recipe("Biff", "600 g entrecote", "2 dl grädde"), 3)
    olle, anna, kim = (
        member("Olle"),
        member("Anna", diet="vegetarian"),
        member("Kim", allergies=["milk"]),
    )
    split = assess(steak, [olle, anna, kim]).split
    result = aggregate(menu_of((steak, split)), settings(olle, anna, kim), ())
    assert lines(result) == {
        "entrecote": "400 g entrecote",  # Olle and Kim
        "grädde": "2 dl grädde",  # Olle and Anna: 2 dl * 2/3, a 2 dl pack
        "tofu": "200 g tofu",
        "havregrädde": "1 dl havregrädde",  # 67 ml, rounded up
    }


def test_shopping_item_text_follows_the_language() -> None:
    item = ShoppingItem("grädde", 1.5, "dl")
    assert item.text("sv") == "1,5 dl grädde" and item.text("en") == "1.5 dl grädde"
    assert ShoppingItem("salt").text("sv") == "salt"
    assert ShoppingItem("ägg", 3).text("sv") == "3 ägg"


def test_small_spice_amounts_become_teaspoons() -> None:
    rec = servings(recipe("A", "1 tsk chilipulver", "1 krm kanel", "3 krm kummin"), 4)
    result = aggregate(
        menu_of(rec),
        settings(member("X"), member("Y"), member("Z", portion="small")),
        (),
    )
    assert lines(result) == {
        "chilipulver": "1 tsk chilipulver",  # 0.65 tsk
        "kanel": "1 krm kanel",
        "kummin": "2 krm kummin",  # 1.95 ml stays in krm
    }
