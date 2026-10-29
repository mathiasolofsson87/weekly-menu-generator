"""Registry of shopping providers. The only module that imports concrete providers."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from homeassistant.core import HomeAssistant

from ..const import CONF_SHOPPING_TARGETS
from .base import ShoppingProvider
from .todo import TodoProvider

ProviderFactory = Callable[[HomeAssistant, Mapping[str, Any]], ShoppingProvider | None]


class ShoppingRegistry:
    """Providers in registration order. A factory returns None when it is not set up."""

    def __init__(self) -> None:
        self._factories: dict[str, ProviderFactory] = {}

    def register(self, provider_id: str, factory: ProviderFactory) -> None:
        self._factories[provider_id] = factory

    @property
    def ids(self) -> list[str]:
        return list(self._factories)

    def create(
        self, hass: HomeAssistant, config: Mapping[str, Any]
    ) -> list[ShoppingProvider]:
        return [
            p for factory in self._factories.values() if (p := factory(hass, config))
        ]


def _todo(hass: HomeAssistant, config: Mapping[str, Any]) -> ShoppingProvider | None:
    targets = list(config.get(CONF_SHOPPING_TARGETS) or [])
    return TodoProvider(hass, targets) if targets else None


def build_default_shopping_registry() -> ShoppingRegistry:
    registry = ShoppingRegistry()
    registry.register(TodoProvider.id, _todo)
    return registry
