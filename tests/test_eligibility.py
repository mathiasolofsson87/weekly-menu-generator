"""Splitting a dinner so that a meat recipe still works for a vegetarian."""

from custom_components.weeklymenu.planner.eligibility import assess
from custom_components.weeklymenu.planner.models import Split
from tests.helpers import member, recipe

STEAK = recipe(
    "Biff med råstekt potatis",
    "600 g entrecote",
    "800 g potatis",
    "200 g haricots verts",
    "2 msk olivolja",
    "1 dl smör",
)
CHICKEN_WOK = recipe(
    "Kycklingwok", "4 st kycklingfilé", "300 g broccoli", "2 msk sojasås", "3 dl ris"
)
MINCE_SAUCE = recipe(
    "Pasta bolognese", "500 g nötfärs", "400 g pasta", "1 burk krossade tomater"
)
SAUSAGE = recipe("Korv med bröd", "6 st korv", "6 st korvbröd")

ANNA_VEG = member("Anna", diet="vegetarian")
OLLE = member("Olle")


def test_everyone_can_eat_it_means_no_split() -> None:
    result = assess(STEAK, [OLLE, member("Kim")])
    assert result.ok and result.split is None


def test_steak_with_vegetarian_sides_is_split() -> None:
    result = assess(STEAK, [OLLE, ANNA_VEG])
    assert result.ok
    split = result.split
    assert split.members == ["Anna"] and split.share == 0.5
    [swap] = split.substitutions
    assert swap.original.raw == "600 g entrecote"
    assert (swap.replacement.name, swap.replacement.amount, swap.replacement.unit) == (
        "tofu",
        600,
        "g",
    )
    assert swap.replacement.raw == "600 g tofu"


def test_pieces_are_converted_to_weight() -> None:
    result = assess(CHICKEN_WOK, [OLLE, ANNA_VEG])
    [swap] = result.split.substitutions
    assert (swap.replacement.amount, swap.replacement.unit) == (600, "g")  # 4 x 150 g


def test_mince_and_sausage_get_matching_substitutes() -> None:
    [mince] = assess(MINCE_SAUCE, [OLLE, ANNA_VEG]).split.substitutions
    assert mince.replacement.name == "vegofärs" and mince.replacement.amount == 500
    [sausage] = assess(SAUSAGE, [OLLE, ANNA_VEG]).split.substitutions
    assert (
        sausage.replacement.name,
        sausage.replacement.amount,
        sausage.replacement.unit,
    ) == (
        "vegokorv",
        6,
        "st",
    )


def test_split_share_follows_portion_sizes() -> None:
    kid = member("Kid", diet="vegetarian", portion="small")
    big = member("Big", portion="large")
    split = assess(STEAK, [big, kid]).split
    assert split.share == round(0.6 / 2.0, 3)


def test_nobody_eating_the_original_is_not_a_split() -> None:
    assert not assess(STEAK, [ANNA_VEG, member("Eva", diet="vegan")]).ok


def test_meat_stock_blocks_the_split() -> None:
    stew = recipe("Gryta", "600 g nötkött", "1 st kalvfond", "2 st morot")
    assert not assess(stew, [OLLE, ANNA_VEG]).ok
    soup = recipe(
        "Soppa", "300 g kycklingfilé", "1 st kycklingbuljongtärning", "1 st lök"
    )
    assert not assess(soup, [OLLE, ANNA_VEG]).ok


def test_fish_sauce_or_anchovies_block_the_split() -> None:
    assert not assess(
        recipe("Pasta", "400 g pasta", "4 st ansjovisfilé"), [OLLE, ANNA_VEG]
    ).ok


def test_dairy_or_egg_is_not_a_swappable_protein_for_vegans() -> None:
    vegan = member("Vera", diet="vegan")
    assert not assess(
        recipe("Stek", "400 g oxfilé", "1 dl grädde"), [OLLE, vegan]
    ).ok  # cream
    assert not assess(STEAK, [OLLE, vegan]).ok  # butter in the sides
    assert assess(
        recipe("Stek", "400 g oxfilé", "1 kg potatis", "2 msk olja"), [OLLE, vegan]
    ).ok


def test_replacement_is_safe_for_the_people_getting_it() -> None:
    steak = recipe("Biff", "400 g entrecote", "1 kg potatis")
    soy = member("Anna", diet="vegetarian", allergies=["soy"])
    assert (
        assess(steak, [OLLE, soy]).split.substitutions[0].replacement.name
        == "portobellosvamp"
    )
    vegan = member("Vera", diet="vegan")
    assert (
        assess(steak, [OLLE, vegan]).split.substitutions[0].replacement.name == "tofu"
    )
    dairy = member("Dan", diet="vegetarian", allergies=["soy", "milk"])
    assert (
        assess(steak, [OLLE, dairy]).split.substitutions[0].replacement.name
        == "portobellosvamp"
    )


def test_declared_allergens_exclude_a_product_whose_name_does_not_show_them() -> None:
    mince = recipe("Färsbiffar", "500 g nötfärs")
    soy = member("Anna", diet="vegetarian", allergies=["soy"])
    # vegofärs is soy-based, so a soy allergy must get lentils instead
    [swap] = assess(mince, [OLLE, soy]).split.substitutions
    assert swap.replacement.name == "röda linser" and swap.replacement.amount == 250
    assert (
        assess(mince, [OLLE, ANNA_VEG]).split.substitutions[0].replacement.name
        == "vegofärs"
    )
    sausage = recipe("Korv", "6 st korv")
    egg_free = member("Eva", diet="vegetarian", allergies=["egg"])
    assert not assess(
        sausage, [OLLE, egg_free]
    ).ok  # no vegokorv without egg, so no split


def test_allergies_are_never_split() -> None:
    allergic = member("Anna", allergies=["fish"])
    salmon = recipe("Lax", "600 g laxfilé", "1 kg potatis")
    assert not assess(salmon, [OLLE, allergic]).ok
    assert not assess(salmon, [allergic, member("Eva", diet="vegetarian")]).ok


def test_title_alone_never_justifies_a_split() -> None:
    assert not assess(
        recipe("Kycklinggryta", "500 g bönor", "2 st lök"), [OLLE, ANNA_VEG]
    ).ok


def test_pescatarian_only_swaps_meat() -> None:
    pesc = member("Pia", diet="pescatarian")
    assert assess(recipe("Lax", "600 g laxfilé"), [OLLE, pesc]).split is None
    split = assess(STEAK, [OLLE, pesc]).split
    assert split.members == ["Pia"]


def test_split_round_trips_through_storage() -> None:
    split = assess(STEAK, [OLLE, ANNA_VEG]).split
    assert Split.from_dict(split.as_dict()) == split
