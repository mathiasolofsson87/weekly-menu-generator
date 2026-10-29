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
from .planner.eligibility import assess
from .planner.generator import attendees_for
from .scheduler import next_week_start

SERVICE_GENERATE_MENU = "generate_menu"
SERVICE_SET_RECIPE = "set_recipe"


def _coordinator(hass: HomeAssistant) -> WeeklyMenuCoordinator:
    for entry in hass.config_entries.async_entries(DOMAIN):
        if hasattr(entry, "runtime_data") and entry.runtime_data:
            return entry.runtime_data.coordinator
    raise ServiceValidationError(
        translation_domain=DOMAIN, translation_key="not_loaded"
    )


def async_register_services(hass: HomeAssistant) -> None:
    """Register services once, from async_setup."""

    async def generate_menu(call: ServiceCall) -> ServiceResponse:
        coordinator = _coordinator(hass)
        week: date = call.data.get("week_start") or next_week_start(
            dt_util.now().date()
        )
        menu = await coordinator.async_generate(week)
        return {
            "week_start": menu.week_start,
            "warnings": menu.warnings,
            "days": {d.date: (d.recipe.title if d.recipe else None) for d in menu.days},
        }

    async def set_recipe(call: ServiceCall) -> None:
        coordinator = _coordinator(hass)
        iso = call.data["date"].isoformat()
        menu = next((m for m in coordinator.data.values() if m.day(iso)), None)
        day = menu.day(iso) if menu else None
        if menu is None or day is None:
            raise ServiceValidationError(
                translation_domain=DOMAIN,
                translation_key="no_such_day",
                translation_placeholders={"date": iso},
            )
        recipe = next(
            (r for r in day.candidates if r.id == call.data["recipe_id"]), None
        )
        if recipe is None:
            raise ServiceValidationError(
                translation_domain=DOMAIN,
                translation_key="not_a_candidate",
                translation_placeholders={
                    "recipe_id": call.data["recipe_id"],
                    "date": iso,
                },
            )
        settings = coordinator.settings()
        eligibility = assess(recipe, attendees_for(settings, day.weekday) or [])
        if not eligibility.ok:  # the settings changed since this menu was drafted
            raise ServiceValidationError(
                translation_domain=DOMAIN,
                translation_key="not_allowed",
                translation_placeholders={"recipe_id": recipe.id, "date": iso},
            )
        day.recipe = recipe
        day.split = eligibility.split
        day.locked = True
        day.candidates = [recipe] + [c for c in day.candidates if c.id != recipe.id]
        await coordinator.store.async_save(menu, dt_util.now().date())
        coordinator.async_set_updated_data(dict(coordinator.store.menus))

    hass.services.async_register(
        DOMAIN,
        SERVICE_GENERATE_MENU,
        generate_menu,
        schema=vol.Schema({vol.Optional("week_start"): cv.date}),
        supports_response=SupportsResponse.OPTIONAL,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_RECIPE,
        set_recipe,
        schema=vol.Schema(
            {vol.Required("date"): cv.date, vol.Required("recipe_id"): cv.string}
        ),
    )
