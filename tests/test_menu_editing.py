"""Regenerate a day, lock, swap and confirm."""

from datetime import date

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError, ServiceValidationError
from pytest_homeassistant_custom_component.common import async_capture_events

from custom_components.weeklymenu.const import EVENT_CONFIRMED
from custom_components.weeklymenu.planner.generator import (
    PlannerSettings,
    async_generate_day,
    async_generate_menu,
)
from tests.helpers import (
    ALL_RECIPES,
    CURRY,
    LAX,
    PASTA,
    SOUP,
    STIR,
    TACOS,
    FakeSource,
    call,
    generate,
    member,
    recipe,
    state,
)

MON, TUE, WED = "2026-11-02", "2026-11-03", "2026-11-04"


def titles(response) -> dict[str, str]:
    return response["days"]


MANY = [
    *ALL_RECIPES,
    *(recipe(f"Extra {n}", f"{n} g tofu", "1 st lök") for n in range(100, 110)),
]


def settings(**kwargs) -> PlannerSettings:
    kwargs.setdefault("dinner_days", ["mon", "tue", "wed", "thu", "fri"])
    return PlannerSettings(**kwargs)


# --- the planner ---------------------------------------------------------------------


async def test_one_day_is_replaced_and_the_rest_of_the_week_is_untouched() -> None:
    source = FakeSource(MANY)
    menu = await async_generate_menu([source], settings(), date(2026, 11, 2), set())
    before = {d.weekday: d.recipe.id for d in menu.days}
    new, _ = await async_generate_day([source], settings(), menu, "wed", set())
    assert (
        new.recipe.id not in before.values()
    )  # a different recipe, not used elsewhere
    assert new.date == "2026-11-04" and new.recipe in new.candidates


async def test_regenerating_a_day_does_not_reuse_its_old_alternatives() -> None:
    source = FakeSource(MANY)
    menu = await async_generate_menu(
        [source], settings(dinner_days=["mon"]), date(2026, 11, 2), set()
    )
    old = {c.id for c in menu.days[0].candidates}
    new, _ = await async_generate_day(
        [source], settings(dinner_days=["mon"]), menu, "mon", set()
    )
    assert new is None or new.recipe.id not in old


async def test_nothing_new_means_none_so_the_old_dinner_stays() -> None:
    source = FakeSource([PASTA])
    menu = await async_generate_menu(
        [source], settings(dinner_days=["mon"]), date(2026, 11, 2), set()
    )
    new, _ = await async_generate_day(
        [source], settings(dinner_days=["mon"]), menu, "mon", set()
    )
    assert new is None


async def test_hint_reaches_the_source() -> None:
    source = FakeSource(MANY)
    menu = await async_generate_menu([source], settings(), date(2026, 11, 2), set())
    await async_generate_day([source], settings(), menu, "tue", set(), hint="fisk")
    assert source.requests[-1].hint == "fisk"


async def test_regenerated_day_respects_the_vegetarian_quota_of_the_rest() -> None:
    """Mon and Tue are meat dishes and one vegetarian dinner is wanted, so Wed must be it."""
    from custom_components.weeklymenu.planner.constraints import is_vegetarian
    from custom_components.weeklymenu.planner.models import Menu, MenuDay

    days = [
        MenuDay("2026-11-02", "mon", PASTA, [PASTA]),
        MenuDay("2026-11-03", "tue", TACOS, [TACOS]),
        MenuDay("2026-11-04", "wed", SOUP, [SOUP]),
    ]
    menu = Menu("2026-11-02", days=days)
    cfg = settings(dinner_days=["mon", "tue", "wed"], vegetarian_days=1)
    new, _ = await async_generate_day(
        [FakeSource([LAX, STIR, CURRY, PASTA])], cfg, menu, "wed", set()
    )
    assert new and is_vegetarian(new.recipe)


async def test_locked_days_survive_a_full_regeneration() -> None:
    source = FakeSource(MANY)
    menu = await async_generate_menu(
        [source], settings(dinner_days=["mon", "tue", "wed"]), date(2026, 11, 2), set()
    )
    tue = menu.day("2026-11-03")
    tue.locked = True
    again = await async_generate_menu(
        [source],
        settings(dinner_days=["mon", "tue", "wed"]),
        date(2026, 11, 2),
        set(),
        keep=[tue],
    )
    kept = again.day("2026-11-03")
    assert kept.recipe == tue.recipe and kept.locked
    others = [d.recipe.id for d in again.days if d.weekday != "tue"]
    assert tue.recipe.id not in others  # and it is not served twice


async def test_a_kept_day_no_longer_planned_is_dropped() -> None:
    source = FakeSource(MANY)
    menu = await async_generate_menu(
        [source], settings(dinner_days=["mon", "tue"]), date(2026, 11, 2), set()
    )
    again = await async_generate_menu(
        [source],
        settings(dinner_days=["mon"]),
        date(2026, 11, 2),
        set(),
        keep=menu.days,
    )
    assert [d.weekday for d in again.days] == ["mon"]


# --- services ----------------------------------------------------------------------------


async def test_regenerate_day_service(hass: HomeAssistant, entry, fake) -> None:
    before = await generate(hass)
    result = await call(hass, "regenerate_day", date=TUE, hint="something light")
    assert result["date"] == TUE and result["recipe"] != before["days"][TUE]
    assert state(hass, entry, "weekday_tue").state == result["recipe"]
    assert (
        state(hass, entry, "weekday_mon").state == before["days"][MON]
    )  # others untouched
    assert fake.requests[-1].hint == "something light"


async def test_regenerate_day_refuses_locked_and_unknown_days(
    hass: HomeAssistant, entry
) -> None:
    await generate(hass)
    await call(hass, "lock_day", date=TUE)
    with pytest.raises(ServiceValidationError, match="locked"):
        await call(hass, "regenerate_day", date=TUE)
    with pytest.raises(ServiceValidationError, match="no dinner planned"):
        await call(hass, "regenerate_day", date="2030-01-01")
    await call(hass, "lock_day", date=TUE, locked=False)
    await call(hass, "regenerate_day", date=TUE)


async def test_lock_day_keeps_the_dinner_through_regeneration(
    hass: HomeAssistant, entry
) -> None:
    first = await generate(hass)
    await call(hass, "lock_day", date=WED)
    assert state(hass, entry, "weekday_wed").attributes["locked"] is True
    second = await generate(hass)
    assert titles(second)[WED] == titles(first)[WED]


async def test_swap_days(hass: HomeAssistant, entry) -> None:
    first = await generate(hass)
    await call(hass, "swap_days", date=MON, other_date=WED)
    assert state(hass, entry, "weekday_mon").state == first["days"][WED]
    assert state(hass, entry, "weekday_wed").state == first["days"][MON]
    assert state(hass, entry, "weekday_tue").state == first["days"][TUE]


async def test_swap_days_refuses_locked_same_day_and_other_weeks(
    hass: HomeAssistant, entry
) -> None:
    await generate(hass)
    await generate(hass, week="2026-11-09")
    with pytest.raises(ServiceValidationError, match="different days"):
        await call(hass, "swap_days", date=MON, other_date=MON)
    with pytest.raises(ServiceValidationError, match="same week"):
        await call(hass, "swap_days", date=MON, other_date="2026-11-10")
    await call(hass, "lock_day", date=MON)
    with pytest.raises(ServiceValidationError, match="locked"):
        await call(hass, "swap_days", date=MON, other_date=TUE)


async def test_swap_is_refused_when_the_recipe_does_not_suit_the_other_day(
    hass: HomeAssistant, entry, fake
) -> None:
    """Eva is allergic to fish (strictly) and eats on Monday only; salmon cannot move there."""
    eva = {
        "id": "2",
        "name": "Eva",
        "allergies": ["fish"],
        "cook_separately": False,
        "attends": ["mon"],
    }
    olle = {"id": "3", "name": "Olle", "attends": ["mon", "tue", "wed"]}
    hass.config_entries.async_update_entry(
        entry, options={**entry.options, "members": [eva, olle]}
    )
    await hass.async_block_till_done()
    fake.recipes = [LAX, CURRY, STIR]
    first = await generate(hass)
    lax_day = next(d for d, t in first["days"].items() if t == LAX.title)
    if lax_day == MON:  # the planner never puts fish on Eva's day
        pytest.fail("salmon was planned on the day of the fish-allergic member")
    mon_recipe = first["days"][MON]
    with pytest.raises(ServiceValidationError, match="cannot be served"):
        await call(hass, "swap_days", date=MON, other_date=lax_day)
    assert state(hass, entry, "weekday_mon").state == mon_recipe  # nothing half-swapped


async def test_confirm_menu(hass: HomeAssistant, entry) -> None:
    confirmed = async_capture_events(hass, EVENT_CONFIRMED)
    await generate(hass)
    result = await call(hass, "confirm_menu")
    await hass.async_block_till_done()
    assert result["status"] == "confirmed" and result["week_start"] == "2026-11-02"
    assert state(hass, entry, "status").state == "confirmed"
    assert [e.data["week_start"] for e in confirmed] == ["2026-11-02"]
    assert entry.runtime_data.coordinator.latest.confirmed_at


async def test_a_confirmed_menu_can_no_longer_be_edited(
    hass: HomeAssistant, entry
) -> None:
    first = await generate(hass)
    await call(hass, "confirm_menu", week_start=MON)
    alternative = entry.runtime_data.coordinator.latest.day(TUE).candidates[-1].id
    for service, data in (
        ("regenerate_day", {"date": TUE}),
        ("lock_day", {"date": TUE}),
        ("swap_days", {"date": MON, "other_date": TUE}),
        ("set_recipe", {"date": TUE, "recipe_id": alternative}),
        ("generate_menu", {"week_start": MON}),
    ):
        with pytest.raises(ServiceValidationError, match="confirmed"):
            await call(hass, service, **data)
    assert state(hass, entry, "weekday_tue").state == first["days"][TUE]


async def test_confirm_without_a_draft_fails(hass: HomeAssistant, entry) -> None:
    with pytest.raises(ServiceValidationError, match="no draft"):
        await call(hass, "confirm_menu")


async def test_confirm_button(hass: HomeAssistant, entry) -> None:
    from tests.helpers import entity_id

    await generate(hass)
    await hass.services.async_call(
        "button",
        "press",
        {"entity_id": entity_id(hass, entry, "button", "confirm")},
        blocking=True,
    )
    assert state(hass, entry, "status").state == "confirmed"


async def test_failed_edits_leave_the_menu_as_it_was(
    hass: HomeAssistant, entry, fake
) -> None:
    first = await generate(hass)
    fake.recipes = []  # nothing left to offer
    with pytest.raises(HomeAssistantError, match="No other recipe"):
        await call(hass, "regenerate_day", date=MON)
    assert state(hass, entry, "weekday_mon").state == first["days"][MON]


def test_unused_imports_are_for_fixtures() -> None:
    assert SOUP and TACOS and member and recipe  # keep helpers imported for readability
