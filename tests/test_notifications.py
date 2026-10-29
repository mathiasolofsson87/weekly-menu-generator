"""Notifications, their buttons and the Saturday reminder."""

from datetime import UTC, datetime

import pytest
from freezegun.api import FrozenDateTimeFactory
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import async_fire_time_changed

from custom_components.weeklymenu.notifications import MOBILE_ACTION_EVENT
from tests.helpers import generate, state


@pytest.fixture
def sent(hass: HomeAssistant, entry) -> list[dict]:
    """Capture what is sent through notify.mobile_app_test, and turn notifications on."""
    calls: list[dict] = []

    async def handler(call) -> None:
        calls.append(dict(call.data))

    hass.services.async_register("notify", "mobile_app_test", handler)
    hass.config_entries.async_update_entry(
        entry, options={**entry.options, "notify_targets": ["mobile_app_test"]}
    )
    return calls


async def settle(hass: HomeAssistant) -> None:
    await hass.async_block_till_done()


async def tap(hass: HomeAssistant, action: str) -> None:
    hass.bus.async_fire(MOBILE_ACTION_EVENT, {"action": action})
    await settle(hass)


def actions(note: dict) -> dict[str, str]:
    return {a["title"]: a["action"] for a in note["data"]["actions"]}


async def test_menu_ready_notification(hass: HomeAssistant, entry, sent) -> None:
    response = await generate(hass)
    await settle(hass)

    [note] = sent
    assert note["title"] == "Veckomenyn är klar"
    first = response["days"]["2026-11-02"]
    assert f"Mån: {first}" in note["message"] and "Ons:" in note["message"]
    assert actions(note) == {
        "Öppna": "URI",
        "Bekräfta": "WEEKLYMENU_CONFIRM:2026-11-02",
        "Skapa om": "WEEKLYMENU_REGENERATE:2026-11-02",
    }
    assert (
        note["data"]["actions"][0]["uri"] == "/"
        and note["data"]["tag"] == "weeklymenu_2026-11-02"
    )


async def test_english_text_and_a_custom_open_path(
    hass: HomeAssistant, entry, sent
) -> None:
    hass.config_entries.async_update_entry(
        entry,
        options={**entry.options, "language": "en", "open_path": "/lovelace/menu"},
    )
    await settle(hass)
    await generate(hass)
    await settle(hass)
    [note] = sent
    assert note["title"] == "The weekly menu is ready" and "Mon:" in note["message"]
    assert actions(note) == {
        "Open": "URI",
        "Confirm": "WEEKLYMENU_CONFIRM:2026-11-02",
        "Regenerate": "WEEKLYMENU_REGENERATE:2026-11-02",
    }
    assert note["data"]["actions"][0]["uri"] == "/lovelace/menu"


async def test_the_confirm_button_confirms_and_reports(
    hass: HomeAssistant, entry, sent
) -> None:
    await generate(hass)
    await settle(hass)
    sent.clear()
    await tap(hass, "WEEKLYMENU_CONFIRM:2026-11-02")
    assert state(hass, entry, "status").state == "confirmed"
    [note] = sent
    assert note["title"] == "Menyn är bekräftad" and "2026-11-02" in note["message"]


async def test_the_regenerate_button_makes_a_new_draft_and_notifies_again(
    hass: HomeAssistant, entry, sent, fake
) -> None:
    await generate(hass)
    await settle(hass)
    requests = len(fake.requests)
    sent.clear()
    await tap(hass, "WEEKLYMENU_REGENERATE:2026-11-02")
    assert len(fake.requests) > requests
    [note] = sent
    assert note["title"] == "Veckomenyn är klar"


async def test_a_button_on_a_confirmed_menu_reports_the_problem(
    hass: HomeAssistant, entry, sent
) -> None:
    await generate(hass)
    await tap(hass, "WEEKLYMENU_CONFIRM:2026-11-02")
    sent.clear()
    await tap(hass, "WEEKLYMENU_REGENERATE:2026-11-02")
    [note] = sent
    assert (
        note["title"] == "Veckomenyn behöver uppmärksamhet"
        and "bekräftad" in note["message"]
    )


@pytest.mark.parametrize(
    "action",
    ["SOMETHING_ELSE:2026-11-02", "WEEKLYMENU_CONFIRM", "", "WEEKLYMENU_CONFIRM:"],
)
async def test_other_buttons_are_ignored(
    hass: HomeAssistant, entry, sent, action
) -> None:
    await generate(hass)
    await settle(hass)
    sent.clear()
    await tap(hass, action)
    assert sent == [] and state(hass, entry, "status").state == "draft"


async def test_problems_are_reported_separately(
    hass: HomeAssistant, entry, sent, fake
) -> None:
    fake.recipes = []
    await generate(hass)
    await settle(hass)
    titles = [n["title"] for n in sent]
    assert titles == ["Veckomenyn är klar", "Veckomenyn behöver uppmärksamhet"]
    assert "Inget recept hittades för Mån." in sent[1]["message"]


async def test_a_failing_source_is_a_problem(
    hass: HomeAssistant, entry, sent, fake
) -> None:
    fake.fail = True
    await generate(hass)
    await settle(hass)
    assert "Receptkällan fake fungerade inte." in sent[-1]["message"]


async def test_events_can_be_switched_off(
    hass: HomeAssistant, entry, sent, fake
) -> None:
    hass.config_entries.async_update_entry(
        entry, options={**entry.options, "notify_events": ["confirmed"]}
    )
    await settle(hass)
    fake.recipes = []
    await generate(hass)
    await settle(hass)
    assert sent == []  # neither "ready" nor "problems" is on
    await tap(hass, "WEEKLYMENU_CONFIRM:2026-11-02")
    assert [n["title"] for n in sent] == ["Menyn är bekräftad"]


async def test_without_targets_nothing_is_sent(hass: HomeAssistant, entry) -> None:
    calls = []

    async def handler(call) -> None:
        calls.append(call)

    hass.services.async_register("notify", "mobile_app_test", handler)
    await generate(hass)
    await settle(hass)
    assert calls == []


async def test_a_missing_notify_service_does_not_break_generation(
    hass: HomeAssistant, entry
) -> None:
    hass.config_entries.async_update_entry(
        entry, options={**entry.options, "notify_targets": ["gone"]}
    )
    await settle(hass)
    response = await generate(hass)
    await settle(hass)
    assert response["status"] == "draft"


# --- the Saturday reminder ---------------------------------------------------------------


async def saturday_noon(
    hass: HomeAssistant, entry, freezer: FrozenDateTimeFactory
) -> None:
    freezer.move_to("2026-11-07 11:59:59+00:00")  # Saturday
    await hass.config_entries.async_reload(entry.entry_id)  # timers plan from "now"
    await settle(hass)
    freezer.move_to("2026-11-07 12:00:00+00:00")
    async_fire_time_changed(hass, datetime(2026, 11, 7, 12, 0, 0, tzinfo=UTC))
    await settle(hass)


async def test_reminder_when_the_draft_is_not_confirmed(
    hass: HomeAssistant, entry, sent, freezer: FrozenDateTimeFactory
) -> None:
    await generate(hass, week="2026-11-09")
    await settle(hass)
    sent.clear()
    await saturday_noon(hass, entry, freezer)
    [note] = sent
    assert note["title"] == "Menyn väntar på dig" and "2026-11-09" in note["message"]
    assert "WEEKLYMENU_CONFIRM:2026-11-09" in actions(note).values()


async def test_no_reminder_once_confirmed_or_when_switched_off(
    hass: HomeAssistant, entry, sent, freezer: FrozenDateTimeFactory
) -> None:
    await generate(hass, week="2026-11-09")
    await tap(hass, "WEEKLYMENU_CONFIRM:2026-11-09")
    sent.clear()
    await saturday_noon(hass, entry, freezer)
    assert sent == []


async def test_no_reminder_on_other_days(
    hass: HomeAssistant, entry, sent, freezer: FrozenDateTimeFactory
) -> None:
    await generate(hass, week="2026-11-09")
    await settle(hass)
    sent.clear()
    freezer.move_to("2026-11-05 11:59:59+00:00")  # Thursday
    await hass.config_entries.async_reload(entry.entry_id)
    await settle(hass)
    freezer.move_to("2026-11-05 12:00:00+00:00")
    async_fire_time_changed(hass, datetime(2026, 11, 5, 12, 0, 0, tzinfo=UTC))
    await settle(hass)
    assert sent == []


# --- options ------------------------------------------------------------------------------


async def test_notification_options(hass: HomeAssistant, entry) -> None:
    async def handler(call) -> None: ...

    hass.services.async_register("notify", "mobile_app_pixel", handler)
    result = await hass.config_entries.options.async_init(entry.entry_id)
    result = await hass.config_entries.options.async_configure(
        result["flow_id"], {"next_step_id": "notifications"}
    )
    assert result["step_id"] == "notifications"
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        {
            "notify_targets": ["notify.mobile_app_pixel"],
            "notify_events": ["menu_ready", "problems"],
            "open_path": "  ",
        },
    )
    assert result["type"] is FlowResultType.MENU
    assert entry.options["notify_targets"] == ["mobile_app_pixel"]  # prefix removed
    assert entry.options["notify_events"] == ["menu_ready", "problems"]
    assert entry.options["open_path"] == "/"  # blank falls back to the default
