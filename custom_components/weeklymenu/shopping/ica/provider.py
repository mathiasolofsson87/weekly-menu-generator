"""Shopping provider that writes to a list in the ICA app."""

from __future__ import annotations

import logging
from datetime import date

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from ..base import PushResult, ShoppingProvider
from ..models import ShoppingItem
from .api import IcaApi, row
from .auth import IcaAuthError, IcaError, IcaGeoBlockedError, async_login

_LOGGER = logging.getLogger(__name__)

PROVIDER_ID = "ica"
MODE_WEEKLY = "weekly"  # a new list for each week's menu
MODE_NAMED = "named"  # always the same list, appended to

# How a row without an amount is written. Checked against the real app (spikes/ica_rows_spike.py):
# ICA reads a quantity of 0 back as "no quantity", so the row shows only its name. A quantity of 1
# would show up as a stray "1".
NO_AMOUNT_QUANTITY = 0.0
NO_AMOUNT_UNIT = ""

TITLES = {
    "sv": ("Veckomeny vecka {week}", "Veckomeny"),
    "en": ("Weekly menu week {week}", "Weekly menu"),
}

AUTH_FAILED = "auth_failed"
GEO_BLOCKED = "geo_blocked"


def list_title(mode: str, name: str | None, week_start: str, language: str) -> str:
    """The ICA list to use: one per week, or a fixed name."""
    weekly, default = TITLES.get(language, TITLES["en"])
    if mode == MODE_NAMED:
        return (name or "").strip() or default
    try:
        week = date.fromisoformat(week_start).isocalendar().week
    except ValueError:
        week = date.today().isocalendar().week
    return weekly.format(week=week)


def to_row(item: ShoppingItem) -> dict:
    if item.amount is None:
        return row(item.name, NO_AMOUNT_QUANTITY, NO_AMOUNT_UNIT)
    return row(item.name, item.amount, item.unit or "st")


class IcaShoppingProvider(ShoppingProvider):
    """Free-text rows on an ICA shopping list. No product matching: ICA's online cart
    is not used, so there is nothing to match against."""

    id = PROVIDER_ID
    capabilities = frozenset({"list"})

    def __init__(
        self,
        hass: HomeAssistant,
        personnummer: str,
        password: str,
        mode: str = MODE_WEEKLY,
        list_name: str | None = None,
    ) -> None:
        self.hass = hass
        self._personnummer = personnummer
        self._password = password
        self._mode = mode
        self._list_name = list_name
        self._title = "ICA"

    @property
    def targets(self) -> list[str]:
        return [f"ICA: {self._title}"]

    async def async_push(
        self, items: list[ShoppingItem], language: str, week_start: str = ""
    ) -> PushResult:
        result = PushResult()
        self._title = list_title(self._mode, self._list_name, week_start, language)
        try:
            tokens = await async_login(self.hass, self._personnummer, self._password)
            api = IcaApi(async_get_clientsession(self.hass), tokens)
            list_id = await api.async_find_list(
                self._title
            ) or await api.async_create_list(self._title)
            present = await api.async_row_names(list_id)
            # Rows already on the list count as added, so a retry never duplicates them.
            await api.async_add_rows(
                list_id, [to_row(i) for i in items if i.name.casefold() not in present]
            )
        except IcaAuthError:
            result.failed, result.needs_reauth = list(items), True
            result.errors.append(AUTH_FAILED)
        except IcaGeoBlockedError:
            result.failed = list(items)
            result.errors.append(GEO_BLOCKED)
        except IcaError as err:
            _LOGGER.warning("ICA shopping list failed: %s", err)
            result.failed = list(items)
            result.errors.append(str(err))
        else:
            result.added = list(items)
        return result
