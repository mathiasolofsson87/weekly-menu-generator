"""Fires the weekly generation event at the configured day and time."""

from __future__ import annotations

import logging
from datetime import date, datetime, time, timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import CALLBACK_TYPE, HomeAssistant, callback
from homeassistant.helpers.event import async_track_time_change

from .const import (
    CONF_GENERATION_DAY,
    CONF_GENERATION_TIME,
    DEFAULT_GENERATION_DAY,
    DEFAULT_GENERATION_TIME,
    EVENT_GENERATION_DUE,
    WEEKDAYS,
)

_LOGGER = logging.getLogger(__name__)


def next_week_start(today: date) -> date:
    """Return the Monday of the week after `today`."""
    return today + timedelta(days=7 - today.weekday())


class MenuScheduler:
    """Calls the generator once a week. The generator itself arrives in phase 2."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self.entry = entry
        self._unsub: CALLBACK_TYPE | None = None
        self._day = DEFAULT_GENERATION_DAY

    @callback
    def async_start(self) -> None:
        """Start listening for the configured time."""
        config: dict[str, Any] = {**self.entry.data, **self.entry.options}
        self._day = config.get(CONF_GENERATION_DAY, DEFAULT_GENERATION_DAY)
        at = time.fromisoformat(
            config.get(CONF_GENERATION_TIME, DEFAULT_GENERATION_TIME)
        )
        self._unsub = async_track_time_change(
            self.hass,
            self._async_tick,
            hour=at.hour,
            minute=at.minute,
            second=at.second,
        )

    @callback
    def async_stop(self) -> None:
        """Stop listening."""
        if self._unsub:
            self._unsub()
            self._unsub = None

    @callback
    def _async_tick(self, now: datetime) -> None:
        if WEEKDAYS[now.weekday()] != self._day:
            return
        week_start = next_week_start(now.date())
        _LOGGER.debug("Menu generation due for the week starting %s", week_start)
        self.hass.bus.async_fire(
            EVENT_GENERATION_DUE,
            {"entry_id": self.entry.entry_id, "week_start": week_start.isoformat()},
        )
