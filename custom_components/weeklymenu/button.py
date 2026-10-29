"""Buttons: draft next week's menu on demand."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.util import dt as dt_util

from . import WeeklyMenuConfigEntry
from .const import DOMAIN
from .coordinator import WeeklyMenuCoordinator
from .scheduler import next_week_start


class _MenuButton(ButtonEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator: WeeklyMenuCoordinator, key: str) -> None:
        self._coordinator = coordinator
        self._attr_translation_key = key
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            name="Weekly Menu Generator",
        )


class GenerateButton(_MenuButton):
    """Draft next week's menu now."""

    def __init__(self, coordinator: WeeklyMenuCoordinator) -> None:
        super().__init__(coordinator, "generate")

    async def async_press(self) -> None:
        await self._coordinator.async_generate(next_week_start(dt_util.now().date()))


class ConfirmButton(_MenuButton):
    """Confirm the latest draft."""

    def __init__(self, coordinator: WeeklyMenuCoordinator) -> None:
        super().__init__(coordinator, "confirm")

    async def async_press(self) -> None:
        await self._coordinator.async_confirm()


async def async_setup_entry(
    hass: HomeAssistant,
    entry: WeeklyMenuConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    coordinator = entry.runtime_data.coordinator
    async_add_entities([GenerateButton(coordinator), ConfirmButton(coordinator)])
