"""Hands shopping items to the providers and keeps count of where each one ended up."""

from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .base import ShoppingProvider
from .models import ADDED, FAILED, PENDING, REVIEW, ShoppingItem, ShoppingResult

_LOGGER = logging.getLogger(__name__)

NO_TARGETS = "no_targets"
NO_REVIEW_LIST = "no_review_list"
REAUTH = "reauth_required"


async def async_deliver(
    hass: HomeAssistant,
    providers: list[ShoppingProvider],
    review_list: str | None,
    items: list[ShoppingItem],
    result: ShoppingResult,
    week_start: str = "",
) -> list[str]:
    """Push `items` through every provider and set each item's status. Returns the ids of
    providers whose login stopped working, so the caller can ask the user to sign in again.

    An item is ADDED if any provider took it. Otherwise, if a provider could not match
    it, it goes to the review list (REVIEW); if nobody could deliver it, it is FAILED
    and can be retried. With no provider at all nothing is lost: items stay PENDING."""
    if not providers:
        result.targets = []
        _note(result, NO_TARGETS)
        return []

    added: set[int] = set()
    reauth: list[str] = []
    unmatched: dict[int, ShoppingItem] = {}
    for provider in providers:
        pushed = await provider.async_push(items, result.language, week_start)
        if pushed.needs_reauth:
            reauth.append(provider.id)
            _note(result, REAUTH)
        added |= {id(i) for i in pushed.added}
        unmatched |= {id(i): i for i in pushed.unmatched}
        for error in pushed.errors:
            _note(result, f"{provider.id}: {error}")

    # Read after pushing: a provider may only know its target (a list's name) by then.
    result.targets = [t for p in providers for t in p.targets]
    for_review = [i for i in items if id(i) in unmatched and id(i) not in added]
    review_ok = await _to_review_list(hass, review_list, for_review, result)
    for item in items:
        if id(item) in added:
            item.status = ADDED
        elif id(item) in unmatched:
            item.status = REVIEW if review_ok else FAILED
        else:
            item.status = FAILED
    return reauth


async def _to_review_list(
    hass: HomeAssistant,
    review_list: str | None,
    items: list[ShoppingItem],
    result: ShoppingResult,
) -> bool:
    """Put items on the review list. False means they could not be placed anywhere."""
    if not items:
        return True
    if not review_list:
        _note(result, NO_REVIEW_LIST)
        return False
    try:
        for item in items:
            await hass.services.async_call(
                "todo",
                "add_item",
                {"entity_id": review_list, "item": item.text(result.language)},
                blocking=True,
            )
    except HomeAssistantError as err:
        _LOGGER.warning("Could not use the review list %s: %s", review_list, err)
        _note(result, f"{review_list}: {err}")
        return False
    return True


def _note(result: ShoppingResult, error: str) -> None:
    if error not in result.errors:
        result.errors.append(error)


def to_retry(result: ShoppingResult) -> list[ShoppingItem]:
    """Items that still need delivering."""
    return [i for i in result.items if i.status in (FAILED, PENDING)]
