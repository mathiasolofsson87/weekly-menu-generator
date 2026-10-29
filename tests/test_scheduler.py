"""Scheduler and model tests."""

from datetime import date, datetime

from freezegun.api import FrozenDateTimeFactory
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
    async_capture_events,
    async_fire_time_changed,
)

from custom_components.weeklymenu.const import DOMAIN, EVENT_GENERATION_DUE
from custom_components.weeklymenu.planner.models import FamilyMember
from custom_components.weeklymenu.scheduler import next_week_start


def test_next_week_start() -> None:
    assert next_week_start(date(2026, 10, 30)) == date(2026, 11, 2)  # Friday
    assert next_week_start(date(2026, 11, 2)) == date(2026, 11, 9)  # Monday
    assert next_week_start(date(2026, 11, 1)) == date(2026, 11, 2)  # Sunday


def test_member_round_trip_drops_bad_days() -> None:
    member = FamilyMember.from_dict(
        {"name": "Olle", "allergies": [" Nötter "], "attends": ["mon", "funday"]}
    )
    assert member.allergies == ["nötter"]
    assert member.attends == ["mon"]
    assert FamilyMember.from_dict(member.as_dict()) == member


async def test_fires_only_on_generation_day(
    hass: HomeAssistant, freezer: FrozenDateTimeFactory
) -> None:
    await hass.config.async_set_time_zone("UTC")
    freezer.move_to("2026-10-29 05:59:59+00:00")  # Thursday
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={"language": "sv", "units": "swedish"},
        options={"generation_day": "fri", "generation_time": "06:00:00"},
    )
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    events = async_capture_events(hass, EVENT_GENERATION_DUE)

    freezer.move_to("2026-10-29 06:00:00+00:00")  # Thursday 06:00: wrong day
    async_fire_time_changed(hass, datetime.fromisoformat("2026-10-29T06:00:00+00:00"))
    await hass.async_block_till_done()
    assert events == []

    freezer.move_to("2026-10-30 06:00:00+00:00")  # Friday 06:00
    async_fire_time_changed(hass, datetime.fromisoformat("2026-10-30T06:00:00+00:00"))
    await hass.async_block_till_done()
    assert len(events) == 1
    assert events[0].data == {"entry_id": entry.entry_id, "week_start": "2026-11-02"}

    assert await hass.config_entries.async_unload(entry.entry_id)
