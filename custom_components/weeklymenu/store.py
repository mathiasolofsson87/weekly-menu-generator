"""Persistent storage of generated menus."""

from __future__ import annotations

from datetime import date, timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from .const import DOMAIN, HISTORY_WEEKS
from .planner.models import Menu

STORAGE_VERSION = 1


class MenuStore:
    """Menus keyed by the ISO date of their Monday."""

    def __init__(self, hass: HomeAssistant, entry_id: str) -> None:
        self._store: Store[dict] = Store(
            hass, STORAGE_VERSION, f"{DOMAIN}.{entry_id}.menus"
        )
        self.menus: dict[str, Menu] = {}

    async def async_load(self) -> None:
        data = await self._store.async_load() or {}
        self.menus = {k: Menu.from_dict(v) for k, v in data.get("menus", {}).items()}

    async def async_save(self, menu: Menu, today: date) -> None:
        """Store `menu` and drop menus older than the history window."""
        self.menus[menu.week_start] = menu
        cutoff = (today - timedelta(weeks=HISTORY_WEEKS)).isoformat()
        self.menus = {k: m for k, m in self.menus.items() if k >= cutoff}
        await self._store.async_save(
            {"menus": {k: m.as_dict() for k, m in self.menus.items()}}
        )

    def recent_recipe_ids(self, before: str) -> set[str]:
        """Ids of recipes used in weeks other than `before`, for variety."""
        return {
            day.recipe.id
            for week, menu in self.menus.items()
            if week != before
            for day in menu.days
            if day.recipe
        }
