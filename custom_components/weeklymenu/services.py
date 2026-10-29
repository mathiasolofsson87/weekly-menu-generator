"""Integration services."""

from __future__ import annotations

from datetime import date

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.core import (
    HomeAssistant,
    ServiceCall,
    ServiceResponse,
    SupportsResponse,
)
from homeassistant.exceptions import ServiceValidationError
from homeassistant.util import dt as dt_util

from .const import DOMAIN
from .coordinator import WeeklyMenuCoordinator
from .planner.models import Menu
from .scheduler import next_week_start

SERVICE_GENERATE_MENU = "generate_menu"
SERVICE_SET_RECIPE = "set_recipe"
SERVICE_REGENERATE_DAY = "regenerate_day"
SERVICE_SWAP_DAYS = "swap_days"
SERVICE_LOCK_DAY = "lock_day"
SERVICE_CONFIRM_MENU = "confirm_menu"
SERVICE_ADD_TO_SHOPPING = "add_to_shopping"


def _coordinator(hass: HomeAssistant) -> WeeklyMenuCoordinator:
    for entry in hass.config_entries.async_entries(DOMAIN):
        if hasattr(entry, "runtime_data") and entry.runtime_data:
            return entry.runtime_data.coordinator
    raise ServiceValidationError(
        translation_domain=DOMAIN, translation_key="not_loaded"
    )


def _summary(menu: Menu) -> dict:
    return {
        "week_start": menu.week_start,
        "status": menu.status,
        "warnings": menu.warnings,
        "days": {d.date: (d.recipe.title if d.recipe else None) for d in menu.days},
    }


def async_register_services(hass: HomeAssistant) -> None:
    """Register services once, from async_setup."""

    async def generate_menu(call: ServiceCall) -> ServiceResponse:
        week: date = call.data.get("week_start") or next_week_start(
            dt_util.now().date()
        )
        menu = await _coordinator(hass).async_generate(week, call.data.get("hint"))
        return _summary(menu)

    async def regenerate_day(call: ServiceCall) -> ServiceResponse:
        day = await _coordinator(hass).async_regenerate_day(
            call.data["date"], call.data.get("hint")
        )
        return {"date": day.date, "recipe": day.recipe.title if day.recipe else None}

    async def swap_days(call: ServiceCall) -> None:
        await _coordinator(hass).async_swap_days(
            call.data["date"], call.data["other_date"]
        )

    async def lock_day(call: ServiceCall) -> None:
        await _coordinator(hass).async_lock_day(call.data["date"], call.data["locked"])

    async def set_recipe(call: ServiceCall) -> None:
        await _coordinator(hass).async_set_recipe(
            call.data["date"], call.data["recipe_id"]
        )

    async def confirm_menu(call: ServiceCall) -> ServiceResponse:
        return _summary(
            await _coordinator(hass).async_confirm(call.data.get("week_start"))
        )

    async def add_to_shopping(call: ServiceCall) -> ServiceResponse:
        result = await _coordinator(hass).async_add_to_shopping(
            call.data.get("week_start"), call.data["everything"]
        )
        return {"counts": result.counts, "errors": result.errors}

    day = {vol.Required("date"): cv.date}
    for name, handler, schema, response in (
        (
            SERVICE_GENERATE_MENU,
            generate_menu,
            {vol.Optional("week_start"): cv.date, vol.Optional("hint"): cv.string},
            True,
        ),
        (
            SERVICE_REGENERATE_DAY,
            regenerate_day,
            {**day, vol.Optional("hint"): cv.string},
            True,
        ),
        (
            SERVICE_SWAP_DAYS,
            swap_days,
            {**day, vol.Required("other_date"): cv.date},
            False,
        ),
        (
            SERVICE_LOCK_DAY,
            lock_day,
            {**day, vol.Optional("locked", default=True): cv.boolean},
            False,
        ),
        (
            SERVICE_SET_RECIPE,
            set_recipe,
            {**day, vol.Required("recipe_id"): cv.string},
            False,
        ),
        (
            SERVICE_CONFIRM_MENU,
            confirm_menu,
            {vol.Optional("week_start"): cv.date},
            True,
        ),
        (
            SERVICE_ADD_TO_SHOPPING,
            add_to_shopping,
            {
                vol.Optional("week_start"): cv.date,
                vol.Optional("everything", default=False): cv.boolean,
            },
            True,
        ),
    ):
        hass.services.async_register(
            DOMAIN,
            name,
            handler,
            schema=vol.Schema(schema),
            supports_response=SupportsResponse.OPTIONAL
            if response
            else SupportsResponse.NONE,
        )
