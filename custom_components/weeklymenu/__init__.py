"""Weekly Menu: suggests a weekly dinner menu and builds the shopping list."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .scheduler import MenuScheduler

type WeeklyMenuConfigEntry = ConfigEntry[MenuScheduler]


async def async_setup_entry(hass: HomeAssistant, entry: WeeklyMenuConfigEntry) -> bool:
    """Set up Weekly Menu from a config entry."""
    scheduler = MenuScheduler(hass, entry)
    scheduler.async_start()
    entry.async_on_unload(scheduler.async_stop)
    entry.async_on_unload(entry.add_update_listener(_async_reload_on_update))
    entry.runtime_data = scheduler
    return True


async def async_unload_entry(hass: HomeAssistant, entry: WeeklyMenuConfigEntry) -> bool:
    """Unload a config entry."""
    return True


async def _async_reload_on_update(
    hass: HomeAssistant, entry: WeeklyMenuConfigEntry
) -> None:
    """Reload when options change so the schedule and members are picked up."""
    await hass.config_entries.async_reload(entry.entry_id)
