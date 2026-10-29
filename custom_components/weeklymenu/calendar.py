"""Calendar of planned dinners, one all-day event per day."""

from __future__ import annotations

from datetime import date, datetime, timedelta

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from . import WeeklyMenuConfigEntry
from .const import DOMAIN
from .coordinator import WeeklyMenuCoordinator
from .planner.models import MenuDay


def _event(day: MenuDay) -> CalendarEvent | None:
    if day.recipe is None:
        return None
    start = date.fromisoformat(day.date)
    lines = [i.raw or i.name for i in day.recipe.ingredients]
    return CalendarEvent(
        start=start,
        end=start + timedelta(days=1),
        summary=day.recipe.title,
        description="\n".join(lines),
        uid=f"{DOMAIN}-{day.date}",
    )


class MenuCalendar(CoordinatorEntity[WeeklyMenuCoordinator], CalendarEntity):
    _attr_has_entity_name = True
    _attr_translation_key = "menu"

    def __init__(self, coordinator: WeeklyMenuCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_calendar"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            name="Weekly Menu Generator",
        )

    def _events(self) -> list[tuple[date, CalendarEvent]]:
        days = sorted(
            (d for menu in self.coordinator.data.values() for d in menu.days),
            key=lambda d: d.date,
        )
        return [(date.fromisoformat(d.date), e) for d in days if (e := _event(d))]

    @property
    def event(self) -> CalendarEvent | None:
        """Today's dinner, or the next planned one."""
        today = dt_util.now().date()
        return next((e for day, e in self._events() if day >= today), None)

    async def async_get_events(
        self, hass: HomeAssistant, start_date: datetime, end_date: datetime
    ) -> list[CalendarEvent]:
        first, last = (
            dt_util.as_local(start_date).date(),
            dt_util.as_local(end_date).date(),
        )
        return [e for day, e in self._events() if first <= day < last]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: WeeklyMenuConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    async_add_entities([MenuCalendar(entry.runtime_data.coordinator)])
