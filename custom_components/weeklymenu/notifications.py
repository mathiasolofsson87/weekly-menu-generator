"""Notifications: menu ready, confirmed, problems and the Saturday reminder.

Messages go through `notify.<target>` services (the mobile app, for example) and
carry action buttons. The mobile app reports a tapped button as a
`mobile_app_notification_action` event, which is handled here. Notifications are
driven by the integration's own events, so automations see the same things.
"""

from __future__ import annotations

import logging
from datetime import date, datetime
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError, ServiceNotFound
from homeassistant.helpers.event import async_track_time_change

from .const import (
    CONF_LANGUAGE,
    CONF_NOTIFY_EVENTS,
    CONF_NOTIFY_TARGETS,
    CONF_OPEN_PATH,
    DEFAULT_LANGUAGE,
    DEFAULT_OPEN_PATH,
    EVENT_CONFIRMED,
    EVENT_MENU_READY,
    NOTIFY_EVENTS,
    WEEKDAYS,
)
from .coordinator import WeeklyMenuCoordinator
from .planner.models import Menu
from .scheduler import next_week_start

_LOGGER = logging.getLogger(__name__)

MOBILE_ACTION_EVENT = "mobile_app_notification_action"
ACTION_CONFIRM = "WEEKLYMENU_CONFIRM"
ACTION_REGENERATE = "WEEKLYMENU_REGENERATE"
TAG = "weeklymenu"
# Warnings worth a "problems" notification, with a message per language.
PROBLEM_WARNINGS = ("source_failed", "no_recipe", "no_sources", "no_days")

TEXT = {
    "sv": {
        "ready_title": "Veckomenyn är klar",
        "ready_split": "{n} middag(ar) lagas i flera versioner.",
        "confirmed_title": "Menyn är bekräftad",
        "confirmed": "Veckan som börjar {week} är låst.",
        "reminder_title": "Menyn väntar på dig",
        "reminder": "Utkastet för veckan som börjar {week} är inte bekräftat.",
        "problems_title": "Veckomenyn behöver uppmärksamhet",
        "open": "Öppna",
        "confirm": "Bekräfta",
        "regenerate": "Skapa om",
        "source_failed": "Receptkällan {detail} fungerade inte.",
        "no_recipe": "Inget recept hittades för {detail}.",
        "no_sources": "Inga receptkällor är aktiva eller inställda.",
        "no_days": "Inga middagsdagar att planera.",
        "days": ["Mån", "Tis", "Ons", "Tors", "Fre", "Lör", "Sön"],
        "action_failed": "Åtgärden gick inte att genomföra.",
        "errors": {
            "menu_confirmed": "Menyn för veckan {week} är redan bekräftad.",
            "no_such_day": "Det finns ingen meny för {date}.",
            "no_draft": "Det finns inget menyutkast att bekräfta.",
        },
    },
    "en": {
        "ready_title": "The weekly menu is ready",
        "ready_split": "{n} dinner(s) are cooked in more than one version.",
        "confirmed_title": "Menu confirmed",
        "confirmed": "The week starting {week} is locked.",
        "reminder_title": "Your menu is waiting",
        "reminder": "The draft for the week starting {week} is not confirmed.",
        "problems_title": "The weekly menu needs attention",
        "open": "Open",
        "confirm": "Confirm",
        "regenerate": "Regenerate",
        "source_failed": "The recipe source {detail} did not work.",
        "no_recipe": "No recipe was found for {detail}.",
        "no_sources": "No recipe sources are active or set up.",
        "no_days": "There are no dinner days to plan.",
        "days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "action_failed": "The action could not be completed.",
        "errors": {
            "menu_confirmed": "The menu for the week of {week} is already confirmed.",
            "no_such_day": "There is no menu for {date}.",
            "no_draft": "There is no draft menu to confirm.",
        },
    },
}


class Notifier:
    """Sends the notifications and handles the buttons on them."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        coordinator: WeeklyMenuCoordinator,
    ) -> None:
        self.hass = hass
        self.entry = entry
        self.coordinator = coordinator

    # --- configuration ---------------------------------------------------------

    @property
    def _config(self) -> dict[str, Any]:
        return {**self.entry.data, **self.entry.options}

    @property
    def _text(self) -> dict[str, Any]:
        language = self._config.get(CONF_LANGUAGE, DEFAULT_LANGUAGE)
        return TEXT.get(language, TEXT["en"])

    def _enabled(self, event: str) -> bool:
        return event in self._config.get(CONF_NOTIFY_EVENTS, NOTIFY_EVENTS)

    # --- wiring ----------------------------------------------------------------

    @callback
    def async_start(self) -> None:
        bus = self.hass.bus
        for unsub in (
            bus.async_listen(EVENT_MENU_READY, self._on_menu_ready),
            bus.async_listen(EVENT_CONFIRMED, self._on_confirmed),
            bus.async_listen(MOBILE_ACTION_EVENT, self._on_action),
            async_track_time_change(
                self.hass, self._on_reminder_time, hour=12, minute=0, second=0
            ),
        ):
            self.entry.async_on_unload(unsub)

    # --- events ------------------------------------------------------------------

    def _menu(self, event: Event) -> Menu | None:
        return self.coordinator.data.get(event.data.get("week_start", ""))

    async def _on_menu_ready(self, event: Event) -> None:
        if menu := self._menu(event):
            if self._enabled("menu_ready"):
                await self._send_menu(
                    menu, "ready_title", self._summary(menu), actions=True
                )
            if self._enabled("problems") and (problems := self._problems(menu)):
                await self._send(self._text["problems_title"], problems)

    async def _on_confirmed(self, event: Event) -> None:
        if (menu := self._menu(event)) and self._enabled("confirmed"):
            await self._send(
                self._text["confirmed_title"],
                self._text["confirmed"].format(week=menu.week_start),
                tag=f"{TAG}_{menu.week_start}",
            )

    async def _on_reminder_time(self, now: datetime) -> None:
        """Saturday noon: nudge if next week's draft is still unconfirmed."""
        if WEEKDAYS[now.weekday()] != "sat" or not self._enabled("reminder"):
            return
        menu = self.coordinator.data.get(next_week_start(now.date()).isoformat())
        if menu and menu.status == "draft":
            message = self._text["reminder"].format(week=menu.week_start)
            await self._send_menu(menu, "reminder_title", message, actions=True)

    async def _on_action(self, event: Event) -> None:
        """A button on one of our notifications was tapped."""
        name, _, week = str(event.data.get("action", "")).partition(":")
        if name not in (ACTION_CONFIRM, ACTION_REGENERATE) or not week:
            return
        try:
            if name == ACTION_CONFIRM:
                await self.coordinator.async_confirm(date.fromisoformat(week))
            else:
                await self.coordinator.async_generate(date.fromisoformat(week))
        except HomeAssistantError as err:
            _LOGGER.warning("Notification action %s failed: %s", name, err)
            await self._send(self._text["problems_title"], self._explain(err))

    # --- messages ----------------------------------------------------------------

    def _explain(self, err: HomeAssistantError) -> str:
        """An error in the integration language (Home Assistant's own text follows its language)."""
        template = self._text["errors"].get(getattr(err, "translation_key", None) or "")
        if template:
            return template.format_map(
                getattr(err, "translation_placeholders", None) or {}
            )
        return self._text["action_failed"]

    def _summary(self, menu: Menu) -> str:
        days = self._text["days"]
        lines = [
            f"{days[WEEKDAYS.index(d.weekday)]}: {d.recipe.title}"
            for d in menu.days
            if d.recipe
        ]
        if splits := sum(d.split is not None for d in menu.days):
            lines.append(self._text["ready_split"].format(n=splits))
        return "\n".join(lines)

    def _problems(self, menu: Menu) -> str:
        days = dict(zip(WEEKDAYS, self._text["days"], strict=True))
        lines = []
        for warning in menu.warnings:
            kind, _, detail = warning.partition(":")
            if kind in PROBLEM_WARNINGS:
                lines.append(self._text[kind].format(detail=days.get(detail, detail)))
        return "\n".join(lines)

    async def _send_menu(
        self, menu: Menu, title_key: str, message: str, *, actions: bool
    ) -> None:
        text = self._text
        data: dict[str, Any] = {"tag": f"{TAG}_{menu.week_start}"}
        if actions:
            path = self._config.get(CONF_OPEN_PATH) or DEFAULT_OPEN_PATH
            data["actions"] = [
                {"action": "URI", "title": text["open"], "uri": path},
                {
                    "action": f"{ACTION_CONFIRM}:{menu.week_start}",
                    "title": text["confirm"],
                },
                {
                    "action": f"{ACTION_REGENERATE}:{menu.week_start}",
                    "title": text["regenerate"],
                },
            ]
            data["clickAction"] = path
        await self._send(text[title_key], message, **data)

    async def _send(self, title: str, message: str, **data: Any) -> None:
        for target in self._config.get(CONF_NOTIFY_TARGETS, []):
            try:
                await self.hass.services.async_call(
                    "notify", target, {"title": title, "message": message, "data": data}
                )
            except (ServiceNotFound, HomeAssistantError) as err:
                _LOGGER.warning("Could not notify through notify.%s: %s", target, err)
