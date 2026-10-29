"""Weekly Menu Generator: suggests a weekly dinner menu and builds the shopping list."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import homeassistant.helpers.config_validation as cv
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import Event, HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, EVENT_GENERATION_DUE
from .coordinator import WeeklyMenuCoordinator
from .notifications import Notifier
from .scheduler import MenuScheduler
from .services import async_register_services
from .shopping.registry import ShoppingRegistry, build_default_shopping_registry
from .sources.registry import SourceRegistry, build_default_registry
from .store import MenuStore

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)
PLATFORMS = [Platform.BUTTON, Platform.CALENDAR, Platform.SENSOR]


@dataclass
class WeeklyMenuData:
    """Runtime data of a config entry."""

    coordinator: WeeklyMenuCoordinator
    scheduler: MenuScheduler
    notifier: Notifier


type WeeklyMenuConfigEntry = ConfigEntry[WeeklyMenuData]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Register services and the provider registry."""
    data = hass.data.setdefault(DOMAIN, {})
    data["registry"] = build_default_registry()
    data["shopping_registry"] = build_default_shopping_registry()
    async_register_services(hass)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: WeeklyMenuConfigEntry) -> bool:
    """Set up Weekly Menu Generator from a config entry."""
    registry: SourceRegistry = hass.data[DOMAIN]["registry"]
    shopping_registry: ShoppingRegistry = hass.data[DOMAIN]["shopping_registry"]
    store = MenuStore(hass, entry.entry_id)
    await store.async_load()
    coordinator = WeeklyMenuCoordinator(hass, entry, store, registry, shopping_registry)
    await coordinator.async_config_entry_first_refresh()

    scheduler = MenuScheduler(hass, entry)
    scheduler.async_start()
    entry.async_on_unload(scheduler.async_stop)
    notifier = Notifier(hass, entry, coordinator)
    notifier.async_start()
    entry.runtime_data = WeeklyMenuData(coordinator, scheduler, notifier)

    async def _generation_due(event: Event) -> None:
        if event.data.get("entry_id") == entry.entry_id:
            await coordinator.async_generate(
                date.fromisoformat(event.data["week_start"])
            )

    entry.async_on_unload(hass.bus.async_listen(EVENT_GENERATION_DUE, _generation_due))
    entry.async_on_unload(entry.add_update_listener(_async_reload_on_update))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: WeeklyMenuConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def _async_reload_on_update(
    hass: HomeAssistant, entry: WeeklyMenuConfigEntry
) -> None:
    """Reload when options change so the schedule and members are picked up."""
    await hass.config_entries.async_reload(entry.entry_id)
