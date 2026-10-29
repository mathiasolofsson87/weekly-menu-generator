"""Setup, services, sensors and scheduling, end to end with a fake provider."""

from datetime import UTC, datetime
from unittest.mock import patch

import pytest
from freezegun.api import FrozenDateTimeFactory
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError, ServiceValidationError
from homeassistant.helpers import entity_registry as er
from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
    async_capture_events,
    async_fire_time_changed,
)

from custom_components.weeklymenu.const import (
    DOMAIN,
    EVENT_GENERATION_DUE,
    EVENT_MENU_READY,
)
from custom_components.weeklymenu.sources.registry import SourceRegistry
from tests.helpers import ALL_RECIPES, FakeSource, recipe

OPTIONS = {
    "dinner_days": ["mon", "tue", "wed"],
    "vegetarian_days": 0,
    "fish_min": 0,
    "members": [
        {
            "id": "1",
            "name": "Anna",
            "allergies": ["fish"],
            "attends": ["mon", "tue", "wed"],
        }
    ],
}


@pytest.fixture
def fake() -> FakeSource:
    return FakeSource(ALL_RECIPES)


@pytest.fixture
async def entry(hass: HomeAssistant, fake: FakeSource, freezer: FrozenDateTimeFactory):
    await hass.config.async_set_time_zone("UTC")
    freezer.move_to("2026-11-04 12:00:00+00:00")  # Wednesday
    registry = SourceRegistry()
    registry.register("fake", lambda hass, config: fake)
    entry = MockConfigEntry(
        domain=DOMAIN, data={"language": "sv", "units": "swedish"}, options=OPTIONS
    )
    entry.add_to_hass(hass)
    with patch(
        "custom_components.weeklymenu.build_default_registry", return_value=registry
    ):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
        yield entry


def _state(hass: HomeAssistant, entry, key: str):
    entity_id = er.async_get(hass).async_get_entity_id(
        "sensor", DOMAIN, f"{entry.entry_id}_{key}"
    )
    assert entity_id, key
    return hass.states.get(entity_id)


async def _generate(hass: HomeAssistant, week="2026-11-02"):
    return await hass.services.async_call(
        DOMAIN,
        "generate_menu",
        {"week_start": week},
        blocking=True,
        return_response=True,
    )


async def test_sensors_start_empty(hass: HomeAssistant, entry) -> None:
    assert _state(hass, entry, "status").state == "none"
    assert _state(hass, entry, "today").state == "unknown"


async def test_generate_menu_service(hass: HomeAssistant, entry) -> None:
    ready = async_capture_events(hass, EVENT_MENU_READY)
    response = await _generate(hass)
    await hass.async_block_till_done()

    assert response["week_start"] == "2026-11-02"
    assert set(response["days"]) == {"2026-11-02", "2026-11-03", "2026-11-04"}
    assert all(response["days"].values()) and response["warnings"] == []
    assert [e.data for e in ready] == [{"week_start": "2026-11-02"}]

    status = _state(hass, entry, "status")
    assert status.state == "draft" and status.attributes["week_start"] == "2026-11-02"
    monday = _state(hass, entry, "weekday_mon")
    assert monday.state == response["days"]["2026-11-02"]
    assert monday.attributes["ingredients"] and monday.attributes["locked"] is False
    assert _state(hass, entry, "weekday_thu").state == "unknown"  # not a dinner day
    assert _state(hass, entry, "today").state == response["days"]["2026-11-04"]


async def test_allergen_never_reaches_a_menu_or_its_alternatives(
    hass: HomeAssistant, entry
) -> None:
    await _generate(hass)
    for key in ("weekday_mon", "weekday_tue", "weekday_wed"):
        state = _state(hass, entry, key)
        titles = [state.state] + [a["title"] for a in state.attributes["alternatives"]]
        assert "Ugnsbakad lax" not in titles
        assert not any("lax" in i for i in state.attributes["ingredients"])


async def test_menus_survive_a_restart(hass: HomeAssistant, entry) -> None:
    response = await _generate(hass)
    await hass.config_entries.async_reload(entry.entry_id)
    await hass.async_block_till_done()
    assert _state(hass, entry, "status").state == "draft"
    assert _state(hass, entry, "weekday_mon").state == response["days"]["2026-11-02"]


async def test_set_recipe_picks_a_candidate_and_locks(
    hass: HomeAssistant, entry
) -> None:
    await _generate(hass)
    coordinator = entry.runtime_data.coordinator
    day = coordinator.latest.day("2026-11-03")
    alternative = day.candidates[1]

    await hass.services.async_call(
        DOMAIN,
        "set_recipe",
        {"date": "2026-11-03", "recipe_id": alternative.id},
        blocking=True,
    )
    tuesday = _state(hass, entry, "weekday_tue")
    assert tuesday.state == alternative.title and tuesday.attributes["locked"] is True

    with pytest.raises(ServiceValidationError):
        await hass.services.async_call(
            DOMAIN,
            "set_recipe",
            {"date": "2026-11-03", "recipe_id": "nope"},
            blocking=True,
        )
    with pytest.raises(ServiceValidationError):
        await hass.services.async_call(
            DOMAIN,
            "set_recipe",
            {"date": "2030-01-01", "recipe_id": "x"},
            blocking=True,
        )


async def test_confirmed_menu_is_not_overwritten(hass: HomeAssistant, entry) -> None:
    await _generate(hass)
    entry.runtime_data.coordinator.latest.status = "confirmed"
    with pytest.raises(HomeAssistantError, match="already confirmed"):
        await _generate(hass)


async def test_generation_due_event_creates_next_weeks_draft(
    hass: HomeAssistant, entry, freezer: FrozenDateTimeFactory
) -> None:
    hass.config_entries.async_update_entry(
        entry,
        options={
            **entry.options,
            "generation_day": "wed",
            "generation_time": "06:00:00",
        },
    )
    await hass.async_block_till_done()
    freezer.move_to("2026-11-04 05:59:59+00:00")  # Wednesday morning
    # The scheduler plans from "now", so restart it after setting the clock.
    await hass.config_entries.async_reload(entry.entry_id)
    await hass.async_block_till_done()
    due = async_capture_events(hass, EVENT_GENERATION_DUE)
    freezer.move_to("2026-11-04 06:00:00+00:00")
    async_fire_time_changed(hass, datetime(2026, 11, 4, 6, 0, 0, tzinfo=UTC))
    await hass.async_block_till_done()

    assert [e.data["week_start"] for e in due] == ["2026-11-09"]
    assert _state(hass, entry, "status").attributes["week_start"] == "2026-11-09"


async def test_service_without_entry_fails_cleanly(hass: HomeAssistant) -> None:
    from homeassistant.setup import async_setup_component

    assert await async_setup_component(hass, DOMAIN, {})
    with pytest.raises(ServiceValidationError):
        await hass.services.async_call(DOMAIN, "generate_menu", {}, blocking=True)


async def test_split_shows_up_on_the_weekday_sensor(
    hass: HomeAssistant, entry, fake
) -> None:

    steak = recipe("Biff med potatis", "600 g entrecote", "1 kg potatis")
    fake.recipes = [steak]
    hass.config_entries.async_update_entry(
        entry,
        options={
            **entry.options,
            "dinner_days": ["mon"],
            "max_split_days": 2,
            "members": [
                {"id": "1", "name": "Olle", "attends": ["mon"]},
                {"id": "2", "name": "Anna", "diet": "vegetarian", "attends": ["mon"]},
            ],
        },
    )
    await hass.async_block_till_done()
    await _generate(hass)

    monday = _state(hass, entry, "weekday_mon")
    assert monday.state == "Biff med potatis"
    [group] = monday.attributes["split"]["groups"]
    assert group["members"] == ["Anna"] and group["share"] == 0.5
    assert group["substitutions"][0]["replacement"]["raw"] == "600 g tofu"


def _entity_id(hass: HomeAssistant, entry, domain: str, key: str) -> str:
    entity_id = er.async_get(hass).async_get_entity_id(
        domain, DOMAIN, f"{entry.entry_id}_{key}"
    )
    assert entity_id, key
    return entity_id


async def test_button_generates_next_weeks_menu(hass: HomeAssistant, entry) -> None:
    await hass.services.async_call(
        "button",
        "press",
        {"entity_id": _entity_id(hass, entry, "button", "generate")},
        blocking=True,
    )
    assert (
        _state(hass, entry, "status").attributes["week_start"] == "2026-11-09"
    )  # today is Wed 11-04


async def test_calendar_lists_dinners(hass: HomeAssistant, entry) -> None:
    response = await _generate(hass)
    calendar_id = _entity_id(hass, entry, "calendar", "calendar")
    result = await hass.services.async_call(
        "calendar",
        "get_events",
        {
            "entity_id": calendar_id,
            "start_date_time": "2026-11-01T00:00:00+00:00",
            "end_date_time": "2026-11-10T00:00:00+00:00",
        },
        blocking=True,
        return_response=True,
    )
    events = result[calendar_id]["events"]
    assert [e["summary"] for e in events] == [
        response["days"][d] for d in sorted(response["days"])
    ]
    assert events[0]["start"] == "2026-11-02" and events[0]["description"]

    state = hass.states.get(calendar_id)  # the event on or after today (Wed 11-04)
    assert state.attributes["message"] == response["days"]["2026-11-04"]
