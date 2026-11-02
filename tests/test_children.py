"""Children can rate and favorite, but not generate, edit or confirm menus, or edit the family."""

from datetime import date

import pytest
from homeassistant.core import Context, HomeAssistant, SupportsResponse
from homeassistant.exceptions import ServiceValidationError

from tests.helpers import entity_id, generate

KIM, ANNA, STRANGER = (
    Context(user_id="u-kim"),
    Context(user_id="u-anna"),
    Context(user_id="u-other"),
)
MON, TUE = "2026-11-02", "2026-11-03"


@pytest.fixture
async def family(hass: HomeAssistant, entry):
    """Anna (an adult) and Kim (a child), each linked to a person with a Home Assistant user."""
    hass.states.async_set("person.anna", "home", {"user_id": "u-anna"})
    hass.states.async_set("person.kim", "home", {"user_id": "u-kim"})
    hass.config_entries.async_update_entry(
        entry,
        options={
            **entry.options,
            "members": [
                {
                    "id": "1",
                    "name": "Anna",
                    "person": "person.anna",
                    "attends": ["mon", "tue", "wed"],
                },
                {
                    "id": "2",
                    "name": "Kim",
                    "person": "person.kim",
                    "child": True,
                    "attends": ["mon", "tue", "wed"],
                },
            ],
        },
    )
    await hass.async_block_till_done()
    await generate(hass)  # something to edit
    return entry


async def act(hass, service: str, context: Context | None, **data):
    has_response = (
        hass.services.supports_response("weeklymenu", service)
        is not SupportsResponse.NONE
    )
    return await hass.services.async_call(
        "weeklymenu",
        service,
        data,
        blocking=True,
        context=context,
        return_response=has_response,
    )


EDITS = [
    ("generate_menu", {}),
    ("regenerate_day", {"date": TUE}),
    ("swap_days", {"date": MON, "other_date": TUE}),
    ("lock_day", {"date": MON, "locked": True}),
    ("set_recipe", {"date": MON, "recipe_id": "x"}),
    ("confirm_menu", {}),
    ("add_to_shopping", {}),
    ("set_member", {"name": "Eva"}),
    ("remove_member", {"id": "1"}),
]


@pytest.mark.parametrize(("service", "data"), EDITS)
async def test_a_child_cannot_change_things(
    hass: HomeAssistant, family, service, data
) -> None:
    before = family.options
    with pytest.raises(ServiceValidationError, match="Kim is a child"):
        await act(hass, service, KIM, **data)
    assert family.options == before
    assert family.runtime_data.coordinator.latest.status == "draft"


@pytest.mark.parametrize("context", [ANNA, STRANGER, None])
async def test_adults_and_unlinked_users_can(
    hass: HomeAssistant, family, context
) -> None:
    await act(hass, "lock_day", context, date=MON, locked=True)
    await act(hass, "regenerate_day", context, date=TUE)
    assert family.runtime_data.coordinator.latest.days[0].locked is True


async def test_a_child_can_rate_and_favorite(hass: HomeAssistant, family) -> None:
    recipe_id = family.runtime_data.coordinator.latest.days[0].recipe.id
    await act(hass, "rate_recipe", KIM, member="Kim", recipe_id=recipe_id, rating=5)
    await act(hass, "favorite_recipe", KIM, member="Kim", recipe_id=recipe_id)
    taste = family.runtime_data.coordinator.taste
    assert taste.rating("2", recipe_id) == 5 and taste.favorites_of("2")


async def _real_user(hass: HomeAssistant, person: str, name: str) -> Context:
    """Entity services check that the user exists, so the button tests use real users."""
    user = await hass.auth.async_create_user(name, group_ids=["system-admin"])
    hass.states.async_set(person, "home", {"user_id": user.id})
    return Context(user_id=user.id)


async def test_a_child_cannot_press_the_buttons(hass: HomeAssistant, family) -> None:
    kim = await _real_user(hass, "person.kim", "Kim")
    for key in ("generate", "confirm"):
        with pytest.raises(ServiceValidationError, match="Kim is a child"):
            await hass.services.async_call(
                "button",
                "press",
                {"entity_id": entity_id(hass, family, "button", key)},
                blocking=True,
                context=kim,
            )
    assert family.runtime_data.coordinator.latest.status == "draft"


async def test_pressing_a_button_as_an_adult_works(hass: HomeAssistant, family) -> None:
    anna = await _real_user(hass, "person.anna", "Anna")
    await hass.services.async_call(
        "button",
        "press",
        {"entity_id": entity_id(hass, family, "button", "generate")},
        blocking=True,
        context=anna,
    )
    assert family.runtime_data.coordinator.latest.week_start == "2026-11-09"


async def test_the_scheduler_and_automations_are_not_restricted(
    hass: HomeAssistant, family
) -> None:
    menu = await family.runtime_data.coordinator.async_generate(date(2026, 11, 16))
    assert menu.week_start == "2026-11-16"
