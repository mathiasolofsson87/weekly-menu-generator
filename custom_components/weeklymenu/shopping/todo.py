"""Shopping provider that writes to Home Assistant to-do lists."""

from __future__ import annotations

import logging

from homeassistant.components.todo import TodoListEntityFeature
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .base import PushResult, ShoppingProvider
from .models import ShoppingItem

_LOGGER = logging.getLogger(__name__)


class TodoProvider(ShoppingProvider):
    """One line per item on each chosen `todo.*` list."""

    id = "todo"

    def __init__(self, hass: HomeAssistant, entity_ids: list[str]) -> None:
        self.hass = hass
        self._entity_ids = entity_ids

    @property
    def targets(self) -> list[str]:
        return list(self._entity_ids)

    def _supports_description(self, entity_id: str) -> bool:
        state = self.hass.states.get(entity_id)
        features = state.attributes.get("supported_features", 0) if state else 0
        return bool(features & TodoListEntityFeature.SET_DESCRIPTION_ON_ITEM)

    async def async_push(
        self, items: list[ShoppingItem], language: str, week_start: str = ""
    ) -> PushResult:
        result = PushResult()
        delivered: set[int] = set()  # positions of items that reached at least one list
        for entity_id in self._entity_ids:
            describe = self._supports_description(entity_id)
            for index, item in enumerate(items):
                data = {"entity_id": entity_id, "item": item.text(language)}
                if describe and (description := _description(item)):
                    data["description"] = description
                try:
                    await self.hass.services.async_call(
                        "todo", "add_item", data, blocking=True
                    )
                except HomeAssistantError as err:
                    _LOGGER.warning(
                        "Could not add %r to %s: %s", data["item"], entity_id, err
                    )
                    message = f"{entity_id}: {err}"
                    if message not in result.errors:
                        result.errors.append(message)
                else:
                    delivered.add(index)
        for index, item in enumerate(items):
            (result.added if index in delivered else result.failed).append(item)
        return result


def _description(item: ShoppingItem) -> str:
    parts = []
    if item.recipes:
        parts.append(", ".join(item.recipes))
    if item.note:
        parts.append(item.note)
    return "\n".join(parts)
