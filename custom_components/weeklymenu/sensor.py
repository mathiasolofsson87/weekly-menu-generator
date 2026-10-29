"""Sensors: menu status, today's dinner and one per weekday."""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.event import async_track_time_change
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from . import WeeklyMenuConfigEntry
from .const import DOMAIN, WEEKDAYS
from .coordinator import WeeklyMenuCoordinator
from .planner.models import MenuDay
from .shopping.models import ADDED, FAILED, PENDING, REVIEW, SKIPPED, ShoppingResult


def _day_attributes(day: MenuDay | None) -> dict[str, Any]:
    """Attributes describing one dinner, for dashboards and automations."""
    if day is None or day.recipe is None:
        return {}
    recipe = day.recipe
    return {
        "date": day.date,
        "recipe_id": recipe.id,
        "source": recipe.source,
        "url": recipe.url,
        "image": recipe.image,
        "total_time": recipe.total_time,
        "servings": recipe.servings,
        "tags": recipe.tags,
        "ingredients": [i.raw or i.name for i in recipe.ingredients],
        "locked": day.locked,
        "split": day.split.as_dict() if day.split else None,
        "alternatives": [{"id": c.id, "title": c.title} for c in day.candidates[1:]],
    }


class _MenuSensor(CoordinatorEntity[WeeklyMenuCoordinator], SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator: WeeklyMenuCoordinator, key: str) -> None:
        super().__init__(coordinator)
        self._attr_translation_key = key
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            name="Weekly Menu Generator",
        )


class StatusSensor(_MenuSensor):
    """none / draft / confirmed for the furthest-ahead week."""

    def __init__(self, coordinator: WeeklyMenuCoordinator) -> None:
        super().__init__(coordinator, "status")

    @property
    def native_value(self) -> str:
        menu = self.coordinator.latest
        return menu.status if menu else "none"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        menu = self.coordinator.latest
        if menu is None:
            return {}
        return {
            "week_start": menu.week_start,
            "generated_at": menu.generated_at,
            "warnings": menu.warnings,
            "menu": {d.date: d.recipe.title if d.recipe else None for d in menu.days},
        }


class ShoppingSensor(_MenuSensor):
    """How the last confirmed menu's shopping went: items added, with the details as attributes."""

    def __init__(self, coordinator: WeeklyMenuCoordinator) -> None:
        super().__init__(coordinator, "shopping")

    def _result(self) -> ShoppingResult | None:
        menu = self.coordinator.shopping_menu
        return (
            ShoppingResult.from_dict(menu.shopping) if menu and menu.shopping else None
        )

    @property
    def native_value(self) -> int | None:
        result = self._result()
        return result.counts[ADDED] if result else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        result, menu = self._result(), self.coordinator.shopping_menu
        if result is None or menu is None:
            return {}
        text = lambda status: [
            i.text(result.language) for i in result.with_status(status)
        ]
        return {
            "week_start": menu.week_start,
            "counts": result.counts,
            "added": text(ADDED),
            "review": text(REVIEW),
            "failed": text(FAILED),
            "pending": text(PENDING),
            "skipped": [i.name for i in result.with_status(SKIPPED)],
            "targets": result.targets,
            "errors": result.errors,
            "updated_at": result.updated_at,
        }


class DinnerSensor(_MenuSensor):
    """Title of one dinner. `lookup` picks the day from the stored menus."""

    def __init__(
        self,
        coordinator: WeeklyMenuCoordinator,
        key: str,
        lookup: Callable[[], MenuDay | None],
    ) -> None:
        super().__init__(coordinator, key)
        self._lookup = lookup

    @property
    def native_value(self) -> str | None:
        day = self._lookup()
        return day.recipe.title if day and day.recipe else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return _day_attributes(self._lookup())


class TodaySensor(DinnerSensor):
    """Tonight's dinner. Re-evaluated just after midnight, when the date changes."""

    def __init__(self, coordinator: WeeklyMenuCoordinator) -> None:
        super().__init__(
            coordinator, "today", lambda: coordinator.day_for(dt_util.now().date())
        )

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()

        @callback
        def _new_day(_: datetime) -> None:
            self.async_write_ha_state()

        self.async_on_remove(
            async_track_time_change(self.hass, _new_day, hour=0, minute=0, second=5)
        )


def _weekday_lookup(
    coordinator: WeeklyMenuCoordinator, weekday: str
) -> Callable[[], MenuDay | None]:
    def lookup() -> MenuDay | None:
        menu = coordinator.latest
        return (
            next((d for d in menu.days if d.weekday == weekday), None) if menu else None
        )

    return lookup


async def async_setup_entry(
    hass: HomeAssistant,
    entry: WeeklyMenuConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        [
            StatusSensor(coordinator),
            TodaySensor(coordinator),
            ShoppingSensor(coordinator),
            *(
                DinnerSensor(
                    coordinator, f"weekday_{wd}", _weekday_lookup(coordinator, wd)
                )
                for wd in WEEKDAYS
            ),
        ]
    )
