"""Cooking one dinner in more than one version so everyone can eat it."""

import pytest

from custom_components.weeklymenu.planner.eligibility import assess
from custom_components.weeklymenu.planner.models import Split
from tests.helpers import member, recipe

STEAK = recipe(
    "Biff med råstekt potatis",
    "600 g entrecote",
    "800 g potatis",
    "200 g haricots verts",
    "2 msk olivolja",
)
STEAK_CREAM = recipe(
    "Biff med gräddsås", "600 g entrecote", "800 g potatis", "2 dl grädde"
)
CHICKEN_WOK = recipe("Kycklingwok", "4 st kycklingfilé", "300 g broccoli", "3 dl ris")
MINCE_SAUCE = recipe(
    "Pasta bolognese", "500 g nötfärs", "400 g pasta", "1 burk krossade tomater"
)
SAUSAGE = recipe("Korv med bröd", "6 st korv", "6 st korvbröd")
ALFREDO = recipe("Pasta alfredo", "400 g pasta", "2 dl grädde", "100 g parmesan")
SALMON = recipe("Lax med potatis", "600 g laxfilé", "1 kg potatis", "1 st citron")

ANNA_VEG = member("Anna", diet="vegetarian")
OLLE = member("Olle")


def only_group(result):
    assert result.ok and len(result.split.groups) == 1
    return result.split.groups[0]


def swaps(group):
    return [(s.original.name, s.replacement.raw) for s in group.substitutions]


# --- diets -----------------------------------------------------------------


def test_everyone_can_eat_it_means_no_split() -> None:
    result = assess(STEAK, [OLLE, member("Kim")])
    assert result.ok and result.split is None


def test_steak_with_vegetarian_sides_is_split() -> None:
    group = only_group(assess(STEAK, [OLLE, ANNA_VEG]))
    assert group.members == ["Anna"] and group.share == 0.5
    assert swaps(group) == [("entrecote", "600 g tofu")]
    assert group.separate_pans is False  # a diet, not an allergy


def test_pieces_are_converted_to_weight() -> None:
    group = only_group(assess(CHICKEN_WOK, [OLLE, ANNA_VEG]))
    assert swaps(group) == [("kycklingfilé", "600 g tofu")]  # 4 x 150 g


def test_mince_and_sausage_get_matching_substitutes() -> None:
    assert swaps(only_group(assess(MINCE_SAUCE, [OLLE, ANNA_VEG]))) == [
        ("nötfärs", "500 g vegofärs")
    ]
    assert swaps(only_group(assess(SAUSAGE, [OLLE, ANNA_VEG]))) == [
        ("korv", "6 st vegokorv")
    ]


def test_split_share_follows_portion_sizes() -> None:
    kid = member("Kid", diet="vegetarian", portion="small")
    group = only_group(assess(STEAK, [member("Big", portion="large"), kid]))
    assert group.share == pytest.approx(0.3)


def test_nobody_eating_the_original_is_not_a_split() -> None:
    assert not assess(STEAK, [ANNA_VEG, member("Eva", diet="vegan")]).ok


def test_meat_stock_or_anchovies_block_the_split() -> None:
    assert not assess(
        recipe("Gryta", "600 g nötkött", "1 st kalvfond"), [OLLE, ANNA_VEG]
    ).ok
    assert not assess(
        recipe("Soppa", "300 g kycklingfilé", "1 st kycklingbuljongtärning"),
        [OLLE, ANNA_VEG],
    ).ok
    assert not assess(
        recipe("Pasta", "400 g pasta", "4 st ansjovisfilé"), [OLLE, ANNA_VEG]
    ).ok


def test_vegan_dairy_is_swapped_but_egg_is_not() -> None:
    vegan = member("Vera", diet="vegan")
    group = only_group(assess(STEAK_CREAM, [OLLE, vegan]))
    assert swaps(group) == [("entrecote", "600 g tofu"), ("grädde", "2 dl havregrädde")]
    assert not assess(recipe("Stek", "400 g oxfilé", "3 ägg"), [OLLE, vegan]).ok


def test_pescatarian_only_swaps_meat() -> None:
    pesc = member("Pia", diet="pescatarian")
    assert assess(SALMON, [OLLE, pesc]).split is None
    assert only_group(assess(STEAK, [OLLE, pesc])).members == ["Pia"]


def test_title_alone_never_justifies_a_split() -> None:
    assert not assess(
        recipe("Kycklinggryta", "500 g bönor", "2 st lök"), [OLLE, ANNA_VEG]
    ).ok


# --- replacements are safe for who gets them ---------------------------------


def test_replacement_is_safe_for_the_people_getting_it() -> None:
    steak = recipe("Biff", "400 g entrecote", "1 kg potatis")
    soy = member("Anna", diet="vegetarian", allergies=["soy"])
    assert swaps(only_group(assess(steak, [OLLE, soy]))) == [
        ("entrecote", "400 g portobellosvamp")
    ]
    vegan = member("Vera", diet="vegan")
    assert swaps(only_group(assess(steak, [OLLE, vegan]))) == [
        ("entrecote", "400 g tofu")
    ]
    dairy_soy = member("Dan", diet="vegetarian", allergies=["soy", "milk"])
    assert swaps(only_group(assess(steak, [OLLE, dairy_soy]))) == [
        ("entrecote", "400 g portobellosvamp")
    ]


def test_declared_allergens_exclude_a_product_whose_name_does_not_show_them() -> None:
    mince = recipe("Färsbiffar", "500 g nötfärs")
    soy = member("Anna", diet="vegetarian", allergies=["soy"])
    assert swaps(only_group(assess(mince, [OLLE, soy]))) == [
        ("nötfärs", "250 g röda linser")
    ]
    assert swaps(only_group(assess(mince, [OLLE, ANNA_VEG]))) == [
        ("nötfärs", "500 g vegofärs")
    ]
    egg_free = member("Eva", diet="vegetarian", allergies=["egg"])
    assert not assess(
        recipe("Korv", "6 st korv"), [OLLE, egg_free]
    ).ok  # vegokorv may hold egg


# --- allergies: cooked separately -------------------------------------------------


def test_fish_allergy_is_cooked_separately_with_a_substitute() -> None:
    group = only_group(assess(SALMON, [OLLE, member("Eva", allergies=["fish"])]))
    assert group.members == ["Eva"] and group.separate_pans is True
    assert swaps(group) == [("laxfilé", "600 g tofu")]


def test_milk_allergy_gets_dairy_free_versions() -> None:
    group = only_group(assess(ALFREDO, [OLLE, member("Kim", allergies=["milk"])]))
    assert group.separate_pans is True
    assert swaps(group) == [
        ("grädde", "2 dl havregrädde"),
        ("parmesan", "100 g växtbaserad parmesan"),
    ]


def test_lactose_intolerance_gets_lactose_free_not_plant_based() -> None:
    group = only_group(assess(ALFREDO, [OLLE, member("Lars", allergies=["lactose"])]))
    assert swaps(group) == [
        ("grädde", "2 dl laktosfri grädde"),
        ("parmesan", "100 g laktosfri parmesan"),
    ]


def test_gluten_allergy_gets_gluten_free_versions() -> None:
    group = only_group(
        assess(MINCE_SAUCE, [OLLE, member("Gita", allergies=["gluten"])])
    )
    assert swaps(group) == [("pasta", "400 g glutenfri pasta")]


def test_an_allergy_can_be_marked_as_never_cook_separately() -> None:
    strict = member("Eva", allergies=["fish"], cook_separately=False)
    assert not assess(SALMON, [OLLE, strict]).ok
    # The switch only concerns allergies: a diet is still handled.
    assert assess(
        STEAK, [OLLE, member("Anna", diet="vegetarian", cook_separately=False)]
    ).ok


def test_allergens_that_cannot_be_swapped_exclude_the_recipe() -> None:
    assert not assess(
        recipe("Omelett", "6 ägg", "1 kg potatis"),
        [OLLE, member("A", allergies=["egg"])],
    ).ok
    assert not assess(
        recipe("Wok", "2 msk sojasås", "300 g broccoli"),
        [OLLE, member("A", allergies=["soy"])],
    ).ok
    assert not assess(
        recipe("Sallad", "50 g valnötter", "1 st sallad"),
        [OLLE, member("A", allergies=["tree_nuts"])],
    ).ok


def test_a_swap_that_leaves_the_allergen_behind_is_rejected() -> None:
    # Cream is swapped, but the cheese sauce is still dairy and has no safe plant option for soy+nuts.
    picky = member("Kim", allergies=["milk", "soy", "gluten", "tree_nuts"])
    assert not assess(ALFREDO, [OLLE, picky]).ok


# --- several versions at once -------------------------------------------------


def test_diet_and_allergy_can_need_two_different_versions() -> None:
    kim = member("Kim", allergies=["milk"])
    result = assess(STEAK_CREAM, [OLLE, ANNA_VEG, kim])
    assert result.ok
    by_member = {g.members[0]: g for g in result.split.groups}
    assert (
        swaps(by_member["Anna"]) == [("entrecote", "600 g tofu")]
        and not by_member["Anna"].separate_pans
    )
    assert (
        swaps(by_member["Kim"]) == [("grädde", "2 dl havregrädde")]
        and by_member["Kim"].separate_pans
    )
    assert sorted(g.share for g in result.split.groups) == pytest.approx([1 / 3, 1 / 3])


def test_members_with_the_same_needs_share_a_version() -> None:
    result = assess(SALMON, [OLLE, ANNA_VEG, member("Eva", allergies=["fish"])])
    group = only_group(result)
    assert group.members == ["Anna", "Eva"] and group.share == pytest.approx(2 / 3)
    assert group.separate_pans is True  # one of them is allergic


def test_three_versions_is_too_many() -> None:
    members = [
        OLLE,
        ANNA_VEG,
        member("Kim", allergies=["milk"]),
        member("Vera", diet="vegan"),
    ]
    assert not assess(STEAK_CREAM, members).ok


def test_split_round_trips_through_storage() -> None:
    split = assess(
        STEAK_CREAM, [OLLE, ANNA_VEG, member("Kim", allergies=["milk"])]
    ).split
    assert Split.from_dict(split.as_dict()) == split


def test_yoghurt_is_swapped_for_a_plant_based_one() -> None:
    curry = recipe(
        "Linsgryta", "2 dl röda linser", "400 ml kokosmjölk", "2 dl matyoghurt (10%)"
    )
    group = only_group(assess(curry, [OLLE, member("Kim", allergies=["milk"])]))
    assert swaps(group) == [("matyoghurt", "2 dl sojayoghurt")]
