"""Config and options flow tests."""

from homeassistant.config_entries import SOURCE_USER
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.weeklymenu.const import DOMAIN


async def _menu(hass, flow_id, choice):
    result = await hass.config_entries.options.async_configure(
        flow_id, {"next_step_id": choice}
    )
    return result


async def _setup_entry(hass: HomeAssistant) -> MockConfigEntry:
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={"language": "sv", "units": "swedish"},
        title="Weekly Menu Generator",
    )
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    return entry


async def test_user_flow_creates_entry(hass: HomeAssistant) -> None:
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {"language": "en", "units": "metric"}
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"] == {"language": "en", "units": "metric"}


async def test_single_instance(hass: HomeAssistant) -> None:
    await _setup_entry(hass)
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "single_instance_allowed"


async def test_options_schedule(hass: HomeAssistant) -> None:
    entry = await _setup_entry(hass)
    result = await hass.config_entries.options.async_init(entry.entry_id)
    result = await _menu(hass, result["flow_id"], "schedule")
    assert result["step_id"] == "schedule"

    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        {
            "generation_day": "thu",
            "generation_time": "07:30:00",
            "dinner_days": ["mon", "wed"],
        },
    )
    assert result["type"] is FlowResultType.MENU
    assert entry.options["generation_day"] == "thu"
    assert entry.options["dinner_days"] == ["mon", "wed"]


async def test_options_schedule_needs_a_day(hass: HomeAssistant) -> None:
    entry = await _setup_entry(hass)
    result = await hass.config_entries.options.async_init(entry.entry_id)
    result = await _menu(hass, result["flow_id"], "schedule")
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        {"generation_day": "fri", "generation_time": "06:00:00", "dinner_days": []},
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"dinner_days": "no_days"}


async def test_options_general_clears_optional_fields(hass: HomeAssistant) -> None:
    entry = await _setup_entry(hass)
    hass.config_entries.async_update_entry(
        entry, data={**entry.data, "ai_task_entity": "ai_task.gemini"}
    )
    await hass.async_block_till_done()
    result = await hass.config_entries.options.async_init(entry.entry_id)
    result = await _menu(hass, result["flow_id"], "general")
    result = await hass.config_entries.options.async_configure(
        result["flow_id"], {"language": "en", "units": "swedish"}
    )
    assert result["type"] is FlowResultType.MENU
    assert entry.options["language"] == "en"
    assert entry.options["ai_task_entity"] is None  # overrides the value from setup


async def _add_member(hass, flow_id, **overrides):
    await _menu(hass, flow_id, "member_add")
    data = {
        "name": "Anna",
        "diet": "omnivore",
        "portion": "normal",
        "attends": ["mon"],
        "cook_separately": True,
    }
    return await hass.config_entries.options.async_configure(
        flow_id, {**data, **overrides}
    )


async def test_add_member_normalises_input(hass: HomeAssistant) -> None:
    entry = await _setup_entry(hass)
    result = await hass.config_entries.options.async_init(entry.entry_id)
    flow_id = result["flow_id"]
    result = await _menu(hass, flow_id, "family")
    assert "member_edit" not in result["menu_options"]  # nobody to edit yet

    result = await _add_member(
        hass,
        flow_id,
        name="  Anna ",
        allergies=["Milk", "milk", "kiwi"],
        dislikes=["Svamp"],
        diet="vegetarian",
    )
    assert result["type"] is FlowResultType.MENU
    [anna] = entry.options["members"]
    assert anna["name"] == "Anna"
    assert anna["allergies"] == ["milk", "kiwi"]  # lowercased, de-duplicated
    assert anna["dislikes"] == ["svamp"]
    assert anna["person"] is None
    assert anna["id"]


async def test_duplicate_member_name_rejected(hass: HomeAssistant) -> None:
    entry = await _setup_entry(hass)
    result = await hass.config_entries.options.async_init(entry.entry_id)
    flow_id = result["flow_id"]
    await _menu(hass, flow_id, "family")
    await _add_member(hass, flow_id)

    result = await _add_member(hass, flow_id, name="anna")
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"name": "name_exists"}
    assert len(entry.options["members"]) == 1


async def test_edit_and_remove_member(hass: HomeAssistant) -> None:
    entry = await _setup_entry(hass)
    result = await hass.config_entries.options.async_init(entry.entry_id)
    flow_id = result["flow_id"]
    await _menu(hass, flow_id, "family")
    await _add_member(hass, flow_id)
    member_id = entry.options["members"][0]["id"]

    await _menu(hass, flow_id, "member_edit")
    await hass.config_entries.options.async_configure(flow_id, {"id": member_id})
    result = await hass.config_entries.options.async_configure(
        flow_id,
        {
            "name": "Anna B",
            "diet": "omnivore",
            "portion": "large",
            "attends": ["fri"],
            "cook_separately": True,
        },
    )
    assert result["type"] is FlowResultType.MENU
    [anna] = entry.options["members"]
    assert (anna["id"], anna["name"], anna["portion"]) == (member_id, "Anna B", "large")

    await _menu(hass, flow_id, "member_remove")
    await hass.config_entries.options.async_configure(flow_id, {"id": member_id})
    assert entry.options["members"] == []


async def test_options_styles(hass: HomeAssistant) -> None:
    entry = await _setup_entry(hass)
    result = await hass.config_entries.options.async_init(entry.entry_id)
    result = await _menu(hass, result["flow_id"], "styles")
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        {
            "style_tags": ["quick", "budget"],
            "vegetarian_days": 2.0,
            "fish_min": 1.0,
            "max_split_days": 3.0,
        },
    )
    assert result["type"] is FlowResultType.MENU
    assert entry.options["style_tags"] == ["quick", "budget"]
    assert entry.options["max_split_days"] == 3
    assert entry.options["vegetarian_days"] == 2 and isinstance(
        entry.options["vegetarian_days"], int
    )


async def test_options_sources_offers_registered_sources(hass: HomeAssistant) -> None:
    entry = await _setup_entry(hass)
    result = await hass.config_entries.options.async_init(entry.entry_id)
    result = await _menu(hass, result["flow_id"], "sources")
    assert result["step_id"] == "sources"
    result = await hass.config_entries.options.async_configure(
        result["flow_id"], {"sources": []}
    )
    assert result["type"] is FlowResultType.MENU
    assert entry.options["sources"] == []
