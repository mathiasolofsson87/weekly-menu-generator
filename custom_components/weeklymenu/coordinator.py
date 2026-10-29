"""Owns the menus: generates them from the source chain, stores them, notifies entities."""

from __future__ import annotations

import asyncio
import logging
from datetime import date
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError, ServiceValidationError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from .const import (
    CANDIDATES_PER_DAY,
    CONF_FISH_MIN,
    CONF_LANGUAGE,
    CONF_MAX_SPLIT_DAYS,
    CONF_PANTRY,
    CONF_REVIEW_LIST,
    CONF_SOURCES,
    CONF_STYLE_TAGS,
    CONF_UNITS,
    CONF_VEGETARIAN_DAYS,
    DEFAULT_FISH_MIN,
    DEFAULT_LANGUAGE,
    DEFAULT_MAX_SPLIT_DAYS,
    DEFAULT_VEGETARIAN_DAYS,
    DOMAIN,
    EVENT_CONFIRMED,
    EVENT_MENU_READY,
)
from .planner.eligibility import assess
from .planner.generator import (
    PlannerSettings,
    async_generate_day,
    async_generate_menu,
    attendees_for,
    week_start_of,
)
from .planner.models import (
    Menu,
    MenuDay,
    Recipe,
    dinner_days_from_options,
    members_from_options,
)
from .shopping.aggregate import DEFAULT_PANTRY, aggregate
from .shopping.delivery import async_deliver, to_retry
from .shopping.models import ShoppingResult
from .shopping.registry import ShoppingRegistry
from .sources.base import RecipeSource
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
        shopping_registry: ShoppingRegistry,
    ) -> None:
        super().__init__(
            hass, _LOGGER, config_entry=entry, name=DOMAIN, update_interval=None
        )
        self.store = store
        self.registry = registry
        self.shopping_registry = shopping_registry
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

    # --- helpers -------------------------------------------------------------

    def _sources(self) -> list[RecipeSource]:
        return self.registry.create(
            self.hass, self.config, self.config.get(CONF_SOURCES)
        )

    def _find(self, day: date) -> tuple[Menu, MenuDay]:
        """The menu and dinner for a date, or a validation error."""
        iso = day.isoformat()
        for menu in self.store.menus.values():
            if found := menu.day(iso):
                return menu, found
        raise ServiceValidationError(
            translation_domain=DOMAIN,
            translation_key="no_such_day",
            translation_placeholders={"date": iso},
        )

    @staticmethod
    def _editable(menu: Menu) -> None:
        if menu.status == "confirmed":
            raise ServiceValidationError(
                translation_domain=DOMAIN,
                translation_key="menu_confirmed",
                translation_placeholders={"week": menu.week_start},
            )

    @staticmethod
    def _unlocked(day: MenuDay) -> None:
        if day.locked:
            raise ServiceValidationError(
                translation_domain=DOMAIN,
                translation_key="day_locked",
                translation_placeholders={"date": day.date},
            )

    async def _commit(self, menu: Menu) -> None:
        await self.store.async_save(menu, dt_util.now().date())
        self.async_set_updated_data(dict(self.store.menus))

    def _place(
        self, target: MenuDay, recipe: Recipe, alternatives: list[Recipe]
    ) -> None:
        """Put `recipe` on `target`, re-checking it against who eats that day."""
        who = attendees_for(self._settings(), target.weekday) or []
        eligibility = assess(recipe, who)
        if not eligibility.ok:
            raise ServiceValidationError(
                translation_domain=DOMAIN,
                translation_key="not_allowed",
                translation_placeholders={"recipe_id": recipe.id, "date": target.date},
            )
        target.recipe = recipe
        target.split = eligibility.split
        target.candidates = [recipe] + [c for c in alternatives if c.id != recipe.id]

    # --- operations ----------------------------------------------------------

    async def async_generate(self, week_start: date, hint: str | None = None) -> Menu:
        """Draft a menu for the week of `week_start`. Locked days of an earlier draft stay."""
        week = week_start_of(week_start).isoformat()
        async with self._lock:
            existing = self.store.menus.get(week)
            if existing:
                self._editable(existing)
            menu = await async_generate_menu(
                self._sources(),
                self._settings(),
                date.fromisoformat(week),
                self.store.recent_recipe_ids(before=week),
                keep=[d for d in existing.days if d.locked and d.recipe]
                if existing
                else (),
                hint=hint,
            )
            await self._commit(menu)
        self.hass.bus.async_fire(
            EVENT_MENU_READY, {"week_start": week, "warnings": list(menu.warnings)}
        )
        return menu

    async def async_regenerate_day(self, day: date, hint: str | None = None) -> MenuDay:
        """Replace one dinner with a new one that fits the rest of the week."""
        async with self._lock:
            menu, current = self._find(day)
            self._editable(menu)
            self._unlocked(current)
            new, warnings = await async_generate_day(
                self._sources(),
                self._settings(),
                menu,
                current.weekday,
                self.store.recent_recipe_ids(before=menu.week_start),
                hint,
            )
            if new is None:
                raise HomeAssistantError(
                    f"No other recipe was found for {current.date}"
                )
            menu.days = [new if d.date == current.date else d for d in menu.days]
            menu.warnings += [w for w in warnings if w not in menu.warnings]
            await self._commit(menu)
            return new

    async def async_lock_day(self, day: date, locked: bool = True) -> MenuDay:
        """Lock a dinner so that regenerating the menu keeps it."""
        async with self._lock:
            menu, current = self._find(day)
            self._editable(menu)
            current.locked = locked
            await self._commit(menu)
            return current

    async def async_set_recipe(self, day: date, recipe_id: str) -> MenuDay:
        """Pick one of the day's alternatives. This locks the day."""
        async with self._lock:
            menu, current = self._find(day)
            self._editable(menu)
            recipe = next((r for r in current.candidates if r.id == recipe_id), None)
            if recipe is None:
                raise ServiceValidationError(
                    translation_domain=DOMAIN,
                    translation_key="not_a_candidate",
                    translation_placeholders={
                        "recipe_id": recipe_id,
                        "date": current.date,
                    },
                )
            self._place(current, recipe, current.candidates)
            current.locked = True
            await self._commit(menu)
            return current

    async def async_swap_days(self, first: date, second: date) -> None:
        """Swap two dinners of the same week. Both are re-checked for their new day."""
        if first == second:
            raise ServiceValidationError(
                translation_domain=DOMAIN, translation_key="swap_same_day"
            )
        async with self._lock:
            menu_a, a = self._find(first)
            menu_b, b = self._find(second)
            if menu_a is not menu_b:
                raise ServiceValidationError(
                    translation_domain=DOMAIN, translation_key="swap_other_week"
                )
            self._editable(menu_a)
            for day in (a, b):
                self._unlocked(day)
                if day.recipe is None:
                    raise ServiceValidationError(
                        translation_domain=DOMAIN,
                        translation_key="swap_empty_day",
                        translation_placeholders={"date": day.date},
                    )
            recipe_a, recipe_b = a.recipe, b.recipe
            before = (a.recipe, a.split, a.candidates, b.recipe, b.split, b.candidates)
            try:
                self._place(a, recipe_b, a.candidates)
                self._place(b, recipe_a, b.candidates)
            except ServiceValidationError:
                a.recipe, a.split, a.candidates = before[:3]
                b.recipe, b.split, b.candidates = before[3:]
                raise
            await self._commit(menu_a)

    async def async_confirm(self, week_start: date | None = None) -> Menu:
        """Lock the menu. Shopping lists are built from a confirmed menu (phase 4)."""
        async with self._lock:
            if week_start is None:
                drafts = [m for m in self.store.menus.values() if m.status == "draft"]
                if not drafts:
                    raise ServiceValidationError(
                        translation_domain=DOMAIN, translation_key="no_draft"
                    )
                menu = max(drafts, key=lambda m: m.week_start)
            else:
                found = self.store.menus.get(week_start_of(week_start).isoformat())
                if found is None:
                    raise ServiceValidationError(
                        translation_domain=DOMAIN,
                        translation_key="no_such_day",
                        translation_placeholders={"date": week_start.isoformat()},
                    )
                menu = found
            self._editable(menu)
            menu.status = "confirmed"
            menu.confirmed_at = dt_util.utcnow().isoformat()
            await self._commit(
                menu
            )  # confirmed first: shopping trouble must not undo it
            await self._shop(menu)
        self.hass.bus.async_fire(
            EVENT_CONFIRMED,
            {
                "week_start": menu.week_start,
                "warnings": list(menu.warnings),
                "shopping": self.shopping_counts(menu),
            },
        )
        return menu

    # --- shopping --------------------------------------------------------------

    @staticmethod
    def shopping_counts(menu: Menu) -> dict[str, int] | None:
        return ShoppingResult.from_dict(menu.shopping).counts if menu.shopping else None

    @property
    def shopping_menu(self) -> Menu | None:
        """The menu whose shopping was done last."""
        done = [m for m in self.data.values() if m.shopping]
        return max(done, key=lambda m: m.week_start) if done else None

    async def _shop(self, menu: Menu, retry_only: bool = False) -> None:
        """Build the lists for a confirmed menu and deliver them. Never raises: trouble is
        recorded in the result, and the items can be retried with add_to_shopping."""
        config = self.config
        language = config.get(CONF_LANGUAGE, DEFAULT_LANGUAGE)
        previous = ShoppingResult.from_dict(menu.shopping) if menu.shopping else None
        try:
            if retry_only and previous:
                result, items = previous, to_retry(previous)
            else:
                built = aggregate(
                    menu,
                    self._settings(),
                    list(
                        DEFAULT_PANTRY
                        if config.get(CONF_PANTRY) is None
                        else config[CONF_PANTRY]
                    ),
                    metric_only=config.get(CONF_UNITS) == "metric",
                )
                result = ShoppingResult(
                    items=built.items + built.skipped, language=language
                )
                items = built.items
            result.errors = []
            await async_deliver(
                self.hass,
                self.shopping_registry.create(self.hass, config),
                config.get(CONF_REVIEW_LIST),
                items,
                result,
            )
            result.touch()
            menu.shopping = result.as_dict()
        except Exception:
            _LOGGER.exception("Building the shopping lists failed")
            failed = previous or ShoppingResult(language=language)
            failed.errors = ["unexpected"]
            menu.shopping = failed.as_dict()
        await self._commit(menu)

    async def async_add_to_shopping(
        self, week_start: date | None = None, everything: bool = False
    ) -> ShoppingResult:
        """Retry what failed for a confirmed menu, or (everything=True) build and push it all again."""
        async with self._lock:
            menus = [m for m in self.store.menus.values() if m.status == "confirmed"]
            if week_start is not None:
                menus = [
                    m
                    for m in menus
                    if m.week_start == week_start_of(week_start).isoformat()
                ]
            if not menus:
                raise ServiceValidationError(
                    translation_domain=DOMAIN, translation_key="no_confirmed_menu"
                )
            menu = max(menus, key=lambda m: m.week_start)
            await self._shop(menu, retry_only=not everything and bool(menu.shopping))
            return ShoppingResult.from_dict(menu.shopping or {})
