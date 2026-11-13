"""Vegetarian substitutes: they suit the dish and the ingredient, and vary over a week."""

import random
from datetime import date

import pytest

from custom_components.weeklymenu.const import WEEKDAYS
from custom_components.weeklymenu.planner.eligibility import assess, substitutes_in
from custom_components.weeklymenu.planner.generator import (
    PlannerSettings,
    async_generate_menu,
)
from custom_components.weeklymenu.planner.models import Menu, MenuDay
from custom_components.weeklymenu.planner.substitutes import (
    KINDS,
    kind_of,
    substitute_note,
)
from custom_components.weeklymenu.shopping.aggregate import aggregate
from tests.helpers import FakeSource, member, recipe

OLLE, ANNA = member("Olle"), member("Anna", diet="vegetarian")


def swaps(rec, used=(), *members):
    result = assess(rec, [OLLE, *(members or [ANNA])], used)
    assert result.ok and len(result.split.groups) == 1
    return [
        (s.original.name, s.replacement.raw)
        for s in result.split.groups[0].substitutions
    ]


# --- one dish at a time: the category and the dish decide ------------------------


@pytest.mark.parametrize(
    ("rec", "expected"),
    [
        # mince: vegofärs, but beans in tacos
        (recipe("Pasta bolognese", "500 g nötfärs"), ("nötfärs", "500 g vegofärs")),
        (recipe("Tacos", "500 g nötfärs"), ("nötfärs", "500 g svarta bönor")),
        # ready meatballs: vegobullar, counted like the meatballs
        (recipe("Köttbullar med mos", "24 st köttbullar"), ("köttbullar", "24 st vegobullar")),
        # sausage
        (recipe("Korvstroganoff", "500 g falukorv"), ("falukorv", "500 g vegokorv")),
        # bacon: vegetarian bacon; ham: smoked tofu
        (recipe("Carbonara", "140 g bacon"), ("bacon", "140 g vegetariskt bacon")),
        (recipe("Skinkpaj", "200 g kokt skinka"), ("kokt skinka", "140 g rökt tofu")),
        # chicken: vegetarian pieces by default, tofu in a wok, chickpeas in a stew,
        # halloumi on the grill
        (recipe("Kycklingpasta", "600 g kycklingfilé"), ("kycklingfilé", "600 g vegetariska kycklingbitar")),
        (recipe("Kycklingwok", "600 g kycklingfilé"), ("kycklingfilé", "600 g tofu")),
        (recipe("Marockansk kycklinggryta", "600 g kycklinglårfilé"), ("kycklinglårfilé", "600 g kikärtor")),
        (recipe("Grillspett med kyckling", "600 g kycklingfilé"), ("kycklingfilé", "360 g halloumi")),
        # fish: tofu in a soup, halloumi from the oven or for fish fingers,
        # cauliflower in a gratin
        (recipe("Fisksoppa", "400 g torskfilé"), ("torskfilé", "400 g tofu")),
        (recipe("Lax i ugn", "600 g laxfilé"), ("laxfilé", "360 g halloumi")),
        (recipe("Fiskgratäng", "600 g sejfilé"), ("sejfilé", "600 g blomkål")),
        (recipe("Fiskpinnar med mos", "16 st fiskpinnar"), ("fiskpinnar", "240 g halloumi")),
        # shellfish
        (recipe("Räkwok", "300 g räkor"), ("räkor", "300 g tofu")),
        # other meat: by the dish
        (recipe("Biff med potatis", "600 g entrecote"), ("entrecote", "600 g portobellosvamp")),
        (recipe("Köttgryta", "800 g högrev"), ("högrev", "800 g champinjoner")),
        (recipe("Pulled pork-burgare", "1 kg fläskkarré"), ("fläskkarré", "1 kg jackfrukt")),
        (recipe("Fläskwok", "500 g fläskfilé"), ("fläskfilé", "500 g vegetariska strimlor")),
    ],
    ids=lambda v: v.title if hasattr(v, "title") else "",
)  # fmt: skip
def test_each_category_gets_a_substitute_that_suits_the_dish(rec, expected) -> None:
    assert swaps(rec) == [expected]


def test_fresh_fish_is_not_mince() -> None:
    # "färsk laxfilé" holds "färs": it was swapped for vegofärs
    assert kind_of("1 kg färsk laxfilé").key == "fish"
    assert swaps(recipe("Lax", "1 kg färsk laxfilé"))[0][1] != "1000 g vegofärs"


def test_one_dish_uses_one_substitute_for_its_lines() -> None:
    rec = recipe(
        "Fiskpasta",
        "400 g fisk i tärningar",
        "1 förp frysta laxtärningar (à 300 g)",
        "1 burk kräftstjärtar i lake (à 170 g)",
    )
    assert [new for _, new in swaps(rec)] == ["400 g tofu", "300 g tofu", "170 g tofu"]


def test_stock_keeps_its_form() -> None:
    rec = recipe(
        "Kalops", "1 kg nötkött", "1 st köttbuljongtärning", "2 msk konc kalvfond"
    )
    assert swaps(rec)[1:] == [
        ("köttbuljongtärning", "1 st grönsaksbuljongtärning"),
        ("konc kalvfond", "2 msk konc grönsaksfond"),
    ]
    assert not assess(
        recipe("Pad thai", "400 g kyckling", "2 msk fisksås"), [OLLE, ANNA]
    ).ok


# --- a week: variety, deterministic -----------------------------------------------


def test_a_substitute_used_this_week_is_passed_over_when_another_suits() -> None:
    pasta = recipe("Kycklingpasta", "600 g kycklingfilé")
    assert swaps(pasta) == [("kycklingfilé", "600 g vegetariska kycklingbitar")]
    assert swaps(pasta, {"vegetariska kycklingbitar"}) == [
        ("kycklingfilé", "600 g tofu")
    ]
    assert swaps(pasta, {"vegetariska kycklingbitar", "tofu"}) == [
        ("kycklingfilé", "360 g halloumi")
    ]
    # all used: the first that suits the dish again
    every = {"vegetariska kycklingbitar", "tofu", "halloumi", "kikärtor"}
    assert swaps(pasta, every) == [("kycklingfilé", "600 g vegetariska kycklingbitar")]


def test_an_unsuitable_substitute_is_never_chosen_for_variety() -> None:
    burgers = recipe("Hamburgare", "500 g nötfärs")
    # lentils, beans and chickpeas make no burger: vegofärs again rather than those
    assert swaps(burgers, {"vegofärs"}) == [("nötfärs", "500 g vegofärs")]


def test_variety_never_changes_whether_a_recipe_can_be_served() -> None:
    rec = recipe("Tacos", "500 g nötfärs")
    every = {r.name for k in KINDS for r in k.replacements}
    assert assess(rec, [OLLE, ANNA], every).ok


THREE_CHICKEN = [
    recipe("Kycklingpasta", "600 g kycklingfilé", "400 g pasta"),
    recipe("Krämig kyckling med ris", "600 g kycklingfilé", "3 dl ris"),
    recipe("Kyckling i ugn", "600 g kycklingfilé", "1 kg potatis"),
]


async def test_a_week_of_chicken_does_not_become_tofu_three_times() -> None:
    settings = PlannerSettings(
        dinner_days=["mon", "tue", "wed"], members=[OLLE, ANNA], max_split_days=3
    )
    menu = await async_generate_menu(
        [FakeSource(THREE_CHICKEN)], settings, date(2026, 11, 2), set()
    )
    names = [d.split.groups[0].substitutions[0].replacement.name for d in menu.days]
    assert len(set(names)) == 3, names
    assert substitutes_in(menu.days) == set(names)


async def test_the_same_week_gives_the_same_substitutes() -> None:
    # The planner's jitter is the only randomness: with the same seed, same choices.
    async def run():
        settings = PlannerSettings(
            rng=random.Random(7),
            dinner_days=["mon", "tue", "wed"],
            members=[OLLE, ANNA],
            max_split_days=3,
        )
        menu = await async_generate_menu(
            [FakeSource(THREE_CHICKEN)], settings, date(2026, 11, 2), set()
        )
        return {
            d.recipe.title: d.split.groups[0].substitutions[0].replacement.raw
            for d in menu.days
        }

    assert await run() == await run()


# --- the shopping list ---------------------------------------------------------------


def test_brands_go_in_the_note_never_in_the_name() -> None:
    rec = recipe("Pasta bolognese", "500 g nötfärs", "400 g pasta")
    rec.servings = 2
    split = assess(rec, [OLLE, ANNA]).split
    menu = Menu(
        "2026-11-02", days=[MenuDay("2026-11-02", "mon", rec, [rec], split=split)]
    )
    result = aggregate(
        menu, PlannerSettings(dinner_days=WEEKDAYS, members=[OLLE, ANNA]), ()
    )
    item = next(i for i in result.items if i.special)
    assert item.text("sv") == "250 g vegofärs"
    assert "Anamma" in item.note and "Anamma" not in item.name
    for kind in KINDS:
        for option in kind.replacements:
            assert not any(
                b in option.name.casefold() for b in ("anamma", "hälsans", "quorn")
            )
    assert substitute_note("tofu") == ""


def test_a_substitute_joins_the_same_product_bought_anyway() -> None:
    a = recipe("Kycklingwok", "400 g kycklingfilé")
    b = recipe("Wok med tofu", "200 g tofu")
    a.servings = b.servings = 2
    split = assess(a, [OLLE, ANNA]).split
    menu = Menu(
        "2026-11-02",
        days=[
            MenuDay("2026-11-02", "mon", a, [a], split=split),
            MenuDay("2026-11-03", "tue", b, [b]),
        ],
    )
    result = aggregate(
        menu, PlannerSettings(dinner_days=WEEKDAYS, members=[OLLE, ANNA]), ()
    )
    tofu = [i for i in result.items if i.name == "tofu"]
    assert [i.text("sv") for i in tofu] == ["400 g tofu"]  # 200 for Anna + 200
