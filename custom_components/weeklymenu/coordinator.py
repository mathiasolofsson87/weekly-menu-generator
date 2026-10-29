"""Owns the menus: generates them from the source chain, stores them, notifies entities."""

from __future__ import annotations

import asyncio
import logging
from datetime import date
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from .const import (
    CANDIDATES_PER_DAY,
    CONF_FISH_MIN,
    CONF_LANGUAGE,
    CONF_MAX_SPLIT_DAYS,
    CONF_SOURCES,
    CONF_STYLE_TAGS,
    CONF_VEGETARIAN_DAYS,
    DEFAULT_FISH_MIN,
    DEFAULT_LANGUAGE,
    DEFAULT_MAX_SPLIT_DAYS,
    DEFAULT_VEGETARIAN_DAYS,
    DOMAIN,
    EVENT_MENU_READY,
)
from .planner.generator import PlannerSettings, async_generate_menu, week_start_of
from .planner.models import (
    Menu,
    MenuDay,
    dinner_days_from_options,
    members_from_options,
)
from .sources.registry import SourceRegistry
from .store import MenuStore

_LOGGER = logging.getLogger(__name__)


class WeeklyMenuCoordinator(DataUpdateCoordinator[dict[str, Menu]]):
    """Holds all stored menus. There is no polling: data changes when a menu does."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        store: MenuStore,
        registry: SourceRegistry,
    ) -> None:
        super().__init__(
            hass, _LOGGER, config_entry=entry, name=DOMAIN, update_interval=None
        )
        self.store = store
        self.registry = registry
        self._lock = asyncio.Lock()

    async def _async_update_data(self) -> dict[str, Menu]:
        return dict(self.store.menus)

    @property
    def config(self) -> dict[str, Any]:
        return {**self.config_entry.data, **self.config_entry.options}

    def settings(self) -> PlannerSettings:
        return self._settings()

    @property
    def latest(self) -> Menu | None:
        """The menu for the furthest-ahead week."""
        return self.data[max(self.data)] if self.data else None

    def day_for(self, day: date) -> MenuDay | None:
        """Today's (or any date's) dinner, preferring a confirmed menu over a draft."""
        menus = sorted(self.data.values(), key=lambda m: m.status != "confirmed")
        for menu in menus:
            if found := menu.day(day.isoformat()):
                return found
        return None

    def _settings(self) -> PlannerSettings:
        config = self.config
        return PlannerSettings(
            dinner_days=dinner_days_from_options(config),
            members=members_from_options(config),
            language=config.get(CONF_LANGUAGE, DEFAULT_LANGUAGE),
            style_tags=list(config.get(CONF_STYLE_TAGS, [])),
            vegetarian_days=int(
                config.get(CONF_VEGETARIAN_DAYS, DEFAULT_VEGETARIAN_DAYS)
            ),
            fish_min=int(config.get(CONF_FISH_MIN, DEFAULT_FISH_MIN)),
            candidates_per_day=CANDIDATES_PER_DAY,
            max_split_days=int(config.get(CONF_MAX_SPLIT_DAYS, DEFAULT_MAX_SPLIT_DAYS)),
        )

    async def async_generate(self, week_start: date) -> Menu:
        """Draft a menu for the week starting on Monday `week_start`, replacing any draft."""
        week = week_start_of(week_start).isoformat()
        async with self._lock:
            existing = self.store.menus.get(week)
            if existing and existing.status == "confirmed":
                raise HomeAssistantError(
                    f"The menu for the week of {week} is already confirmed"
                )
            sources = self.registry.create(
                self.hass, self.config, self.config.get(CONF_SOURCES)
            )
            menu = await async_generate_menu(
                sources,
                self._settings(),
                date.fromisoformat(week),
                self.store.recent_recipe_ids(before=week),
            )
            await self.store.async_save(menu, dt_util.now().date())
            self.async_set_updated_data(dict(self.store.menus))
        self.hass.bus.async_fire(EVENT_MENU_READY, {"week_start": week})
        return menu
