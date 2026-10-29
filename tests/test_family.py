"""Editing the family through services, which is what the family card does."""

import pytest
import voluptuous as vol
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ServiceValidationError

from tests.helpers import call, generate, state


def members(entry) -> dict[str, dict]:
    return {m["name"]: m for m in entry.options["members"]}


async def edit(hass: HomeAssistant, service: str, **data):
    result = await call(hass, service, **data)
    await hass.async_block_till_done()  # saving reloads the entry
    return result


async def test_the_family_sensor_lists_the_members(hass: HomeAssistant, entry) -> None:
    sensor = state(hass, entry, "family")
    assert sensor.state == "1"
    [anna] = sensor.attributes["members"]
    assert (
        anna["name"] == "Anna"
        and anna["allergies"] == ["fish"]
        and anna["attends"] == ["mon", "tue", "wed"]
    )
    assert sensor.attributes["dinner_days"] == ["mon", "tue", "wed"]


async def test_add_a_member(hass: HomeAssistant, entry) -> None:
    result = await edit(
        hass,
        "set_member",
        name="  Olle ",
        allergies=["Milk", " milk ", "kiwi"],
        dislikes=["Svamp"],
        diet="vegetarian",
        portion="small",
        cook_separately=False,
    )
    olle = members(entry)["Olle"]
    assert result == {"id": olle["id"], "name": "Olle"} and olle["id"]
    assert olle["allergies"] == ["milk", "kiwi"] and olle["dislikes"] == [
        "svamp"
    ]  # tidied
    assert (olle["diet"], olle["portion"], olle["cook_separately"]) == (
        "vegetarian",
        "small",
        False,
    )
    assert olle["attends"] == ["mon", "tue", "wed"]  # the dinner days, by default
    assert state(hass, entry, "family").state == "2"


async def test_a_new_member_needs_a_name(hass: HomeAssistant, entry) -> None:
    with pytest.raises(ServiceValidationError, match="needs a name"):
        await call(hass, "set_member", diet="vegan")


async def test_changing_a_member_by_name_keeps_the_other_fields(
    hass: HomeAssistant, entry
) -> None:
    before = members(entry)["Anna"]
    await edit(hass, "set_member", name="anna", portion="large")
    anna = members(entry)["Anna"]
    assert anna["portion"] == "large"
    # everything that was set before is unchanged (the rest is filled with defaults)
    assert all(anna[k] == v for k, v in before.items())
    assert (anna["id"], anna["name"], anna["allergies"], anna["attends"]) == (
        "1",
        "Anna",
        ["fish"],
        ["mon", "tue", "wed"],
    )
    assert len(entry.options["members"]) == 1  # updated, not duplicated


async def test_a_member_can_be_renamed_through_the_id(
    hass: HomeAssistant, entry
) -> None:
    await edit(hass, "set_member", id="1", name="Anna-Lisa", allergies=[])
    assert list(members(entry)) == ["Anna-Lisa"]
    assert (
        members(entry)["Anna-Lisa"]["id"] == "1"
        and members(entry)["Anna-Lisa"]["allergies"] == []
    )


async def test_names_stay_unique(hass: HomeAssistant, entry) -> None:
    await edit(hass, "set_member", name="Olle")
    with pytest.raises(
        ServiceValidationError, match="already a family member called olle"
    ):
        await call(hass, "set_member", id="1", name="olle")
    assert list(members(entry)) == ["Anna", "Olle"]


async def test_unknown_member(hass: HomeAssistant, entry) -> None:
    with pytest.raises(ServiceValidationError, match="no family member nope"):
        await call(hass, "set_member", id="nope", name="X")
    with pytest.raises(ServiceValidationError, match="no family member Nobody"):
        await call(hass, "remove_member", name="Nobody")


async def test_a_member_must_eat_on_some_day(hass: HomeAssistant, entry) -> None:
    with pytest.raises(ServiceValidationError, match="at least one day"):
        await call(hass, "set_member", name="Olle", attends=[])
    assert list(members(entry)) == ["Anna"]


@pytest.mark.parametrize(
    "bad",
    [
        {"diet": "carnivore"},
        {"portion": "huge"},
        {"attends": ["funday"]},
        {"cook_separately": "maybe"},
    ],
)
async def test_bad_values_are_refused(hass: HomeAssistant, entry, bad) -> None:
    with pytest.raises(vol.Invalid):
        await call(hass, "set_member", name="Olle", **bad)


async def test_remove_a_member(hass: HomeAssistant, entry) -> None:
    await edit(hass, "set_member", name="Olle")
    await edit(hass, "remove_member", name="olle")
    assert list(members(entry)) == ["Anna"]
    await edit(hass, "remove_member", id="1")
    assert entry.options["members"] == [] and state(hass, entry, "family").state == "0"


async def test_a_change_applies_to_the_next_menu(hass: HomeAssistant, entry) -> None:
    """A member added through the service is respected by the next menu."""
    await edit(hass, "set_member", name="Eva", allergies=["egg"], cook_separately=False)
    response = await generate(hass)
    lines = [
        line
        for weekday in ("mon", "tue", "wed")
        if state(hass, entry, f"weekday_{weekday}").state != "unknown"
        for line in state(hass, entry, f"weekday_{weekday}").attributes["ingredients"]
    ]
    assert response["days"] and lines and not any("ägg" in line for line in lines)
