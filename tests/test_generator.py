"""Week planning."""

from datetime import date

from custom_components.weeklymenu.planner.generator import (
    PlannerSettings,
    async_generate_menu,
    week_start_of,
)
from tests.helpers import (
    CURRY,
    LAX,
    PASTA,
    SOUP,
    STEW,
    STIR,
    TACOS,
    FakeSource,
    member,
    recipe,
)

MONDAY = date(2026, 11, 2)
ALL = [PASTA, TACOS, CURRY, LAX, SOUP, STEW, STIR]


def _settings(**kwargs) -> PlannerSettings:
    kwargs.setdefault("dinner_days", ["mon", "tue", "wed", "thu", "fri"])
    return PlannerSettings(**kwargs)


async def test_fills_every_dinner_day_with_distinct_recipes() -> None:
    menu = await async_generate_menu([FakeSource(ALL)], _settings(), MONDAY, set())
    assert [d.weekday for d in menu.days] == ["mon", "tue", "wed", "thu", "fri"]
    assert menu.days[0].date == "2026-11-02"
    titles = [d.recipe.title for d in menu.days]
    assert len(set(titles)) == 5
    assert menu.status == "draft" and menu.warnings == []


async def test_candidates_start_with_the_chosen_recipe() -> None:
    menu = await async_generate_menu([FakeSource(ALL)], _settings(), MONDAY, set())
    for day in menu.days:
        assert day.candidates[0] == day.recipe
        assert 1 <= len(day.candidates) <= 3
        assert len({c.id for c in day.candidates}) == len(day.candidates)


async def test_allergy_is_never_violated() -> None:
    anna = member("Anna", allergies=["milk", "gluten"])
    settings = _settings(members=[anna])
    menu = await async_generate_menu([FakeSource(ALL)], settings, MONDAY, set())
    served = {c.title for d in menu.days for c in d.candidates}
    # Everything else contains milk (carbonara, tacos, lax, soup) or gluten.
    assert served == {"Linscurry", "Köttgryta", "Wok med tofu"}
    assert (
        sum(w.startswith("no_recipe") for w in menu.warnings) == 2
    )  # 3 safe recipes, 5 days


async def test_only_attendees_constrain_a_day() -> None:
    anna = member("Anna", allergies=["milk"], attends=["mon"])
    olle = member("Olle", attends=["mon", "tue", "wed", "thu", "fri"])
    menu = await async_generate_menu(
        [FakeSource([TACOS, PASTA, CURRY, STEW, STIR])],
        _settings(members=[anna, olle]),
        MONDAY,
        set(),
    )
    monday = menu.day("2026-11-02")
    assert monday.recipe.title in {"Linscurry", "Köttgryta", "Wok med tofu"}  # no dairy
    assert {"Tacos", "Pasta carbonara"} & {d.recipe.title for d in menu.days[1:]}


async def test_days_nobody_attends_are_skipped() -> None:
    anna = member("Anna", attends=["mon", "wed"])
    menu = await async_generate_menu(
        [FakeSource(ALL)], _settings(members=[anna]), MONDAY, set()
    )
    assert [d.weekday for d in menu.days] == ["mon", "wed"]


async def test_vegetarian_and_fish_quotas() -> None:
    settings = _settings(vegetarian_days=2, fish_min=1)
    menu = await async_generate_menu([FakeSource(ALL)], settings, MONDAY, set())
    chosen = [d.recipe for d in menu.days]
    from custom_components.weeklymenu.planner.constraints import has_fish, is_vegetarian

    assert sum(is_vegetarian(r) for r in chosen) >= 2
    assert sum(has_fish(r) for r in chosen) >= 1


async def test_quota_is_dropped_when_nothing_qualifies() -> None:
    settings = _settings(vegetarian_days=3)
    menu = await async_generate_menu(
        [FakeSource([PASTA, TACOS, STEW])], settings, MONDAY, set()
    )
    assert (
        len([d for d in menu.days if d.recipe]) == 3
    )  # filled anyway, with what exists


async def test_recent_recipes_are_avoided() -> None:
    settings = _settings(dinner_days=["mon", "tue"])
    menu = await async_generate_menu(
        [FakeSource(ALL)],
        settings,
        MONDAY,
        {PASTA.id, TACOS.id, CURRY.id, LAX.id, SOUP.id},
    )
    # exclude_ids is passed to the source, so repeats never come back at all
    assert {d.recipe.title for d in menu.days} == {"Köttgryta", "Wok med tofu"}


async def test_style_tags_rank_matching_recipes_first() -> None:
    settings = _settings(dinner_days=["mon"], style_tags=["easy"])
    menu = await async_generate_menu([FakeSource(ALL)], settings, MONDAY, set())
    assert menu.days[0].recipe.title == "Linscurry"


async def test_shared_ingredients_are_preferred_to_cut_waste() -> None:
    a = recipe("A", "2 st gul lök", "300 g tofu")
    b = recipe("B", "2 st gul lök", "300 g tofu", "1 st morot")
    c = recipe("C", "1 st fänkål", "2 dl bulgur")
    settings = _settings(dinner_days=["mon", "tue"], candidates_per_day=2)
    menu = await async_generate_menu([FakeSource([a, c, b])], settings, MONDAY, set())
    assert {d.recipe.title for d in menu.days} == {"A", "B"}


async def test_falls_through_to_the_next_source() -> None:
    broken, good = FakeSource(fail=True), FakeSource(ALL)
    good.id = "second"
    menu = await async_generate_menu([broken, good], _settings(), MONDAY, set())
    assert "source_failed:fake" in menu.warnings
    assert all(d.recipe for d in menu.days)


async def test_second_source_only_asked_when_first_is_not_enough() -> None:
    first, second = FakeSource(ALL), FakeSource(ALL)
    await async_generate_menu([first, second], _settings(), MONDAY, set())
    assert first.requests and not second.requests


async def test_unsafe_recipes_from_first_source_trigger_the_next() -> None:
    anna = member("Anna", allergies=["milk"])
    first, second = (
        FakeSource([TACOS, PASTA, SOUP, LAX]),
        FakeSource([CURRY, STIR, STEW]),
    )
    second.id = "second"
    menu = await async_generate_menu(
        [first, second],
        _settings(members=[anna], dinner_days=["mon", "tue"]),
        MONDAY,
        set(),
    )
    assert second.requests
    assert {d.recipe.title for d in menu.days} <= {
        "Linscurry",
        "Wok med tofu",
        "Köttgryta",
    }


async def test_no_sources_or_days_gives_warnings_not_errors() -> None:
    menu = await async_generate_menu([], _settings(), MONDAY, set())
    assert "no_sources" in menu.warnings and all(d.recipe is None for d in menu.days)
    empty = await async_generate_menu(
        [FakeSource(ALL)], _settings(dinner_days=[]), MONDAY, set()
    )
    assert empty.warnings == ["no_days"] and empty.days == []


def test_week_start_of() -> None:
    assert week_start_of(date(2026, 11, 5)) == date(2026, 11, 2)
    assert week_start_of(date(2026, 11, 8)) == date(2026, 11, 2)


STEAK = recipe(
    "Biff med potatis",
    "600 g entrecote",
    "1 kg potatis",
    "200 g bönor",
    tags=("fancy",),
)
FAMILY = [member("Olle"), member("Anna", diet="vegetarian")]


async def test_a_meat_recipe_is_used_with_a_split_when_it_ranks_best() -> None:
    settings = _settings(
        dinner_days=["mon"], members=FAMILY, max_split_days=2, style_tags=["fancy"]
    )
    menu = await async_generate_menu(
        [FakeSource([STEAK, CURRY])], settings, MONDAY, set()
    )
    [day] = menu.days
    assert day.recipe.title == "Biff med potatis"
    [group] = day.split.groups
    assert group.members == ["Anna"]
    assert group.substitutions[0].replacement.raw == "600 g tofu"


async def test_recipes_everyone_can_eat_win_over_splits() -> None:
    settings = _settings(
        dinner_days=["mon"], members=FAMILY, max_split_days=2, style_tags=["fancy"]
    )
    plain = recipe("Fin pasta", "400 g pasta", "1 st zucchini", tags=("fancy",))
    menu = await async_generate_menu(
        [FakeSource([STEAK, plain])], settings, MONDAY, set()
    )
    assert menu.days[0].recipe.title == "Fin pasta" and menu.days[0].split is None


async def test_split_limit_is_respected() -> None:
    steaks = [recipe(f"Biff {n}", "600 g entrecote", "1 kg potatis") for n in "ABC"]
    settings = _settings(
        dinner_days=["mon", "tue", "wed"], members=FAMILY, max_split_days=1
    )
    menu = await async_generate_menu(
        [FakeSource([*steaks, CURRY, STIR])], settings, MONDAY, set()
    )
    assert sum(d.split is not None for d in menu.days) == 1
    assert all(d.recipe for d in menu.days)


async def test_split_limit_is_not_allowed_to_leave_a_day_empty() -> None:
    steaks = [recipe(f"Biff {n}", "600 g entrecote", "1 kg potatis") for n in "AB"]
    settings = _settings(dinner_days=["mon", "tue"], members=FAMILY, max_split_days=0)
    menu = await async_generate_menu([FakeSource(steaks)], settings, MONDAY, set())
    assert all(d.recipe and d.split for d in menu.days)
    assert any(w.startswith("split_limit_exceeded") for w in menu.warnings)


async def test_allergy_is_served_as_a_separately_cooked_version() -> None:
    allergic = member("Eva", allergies=["fish"])
    settings = _settings(
        dinner_days=["mon"], members=[member("Olle"), allergic], max_split_days=2
    )
    menu = await async_generate_menu([FakeSource([LAX])], settings, MONDAY, set())
    assert menu.days[0].recipe.title == "Ugnsbakad lax"
    assert menu.days[0].split.groups[0].separate_pans is True


async def test_allergy_that_must_not_be_cooked_separately_excludes_the_recipe() -> None:
    strict = member("Eva", allergies=["fish"], cook_separately=False)
    settings = _settings(
        dinner_days=["mon"], members=[member("Olle"), strict], max_split_days=2
    )
    menu = await async_generate_menu([FakeSource([LAX])], settings, MONDAY, set())
    assert menu.days[0].recipe is None


async def test_source_is_told_to_keep_proteins_separable_only_when_diets_differ() -> (
    None
):
    mixed, same = FakeSource([CURRY]), FakeSource([CURRY])
    await async_generate_menu(
        [mixed], _settings(members=FAMILY, max_split_days=2), MONDAY, set()
    )
    await async_generate_menu(
        [same],
        _settings(members=[member("A"), member("B")], max_split_days=2),
        MONDAY,
        set(),
    )
    assert mixed.requests[0].separable is True
    assert same.requests[0].separable is False
