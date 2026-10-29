"""Registry of shopping providers. The only module that imports concrete providers."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from homeassistant.core import HomeAssistant

from ..const import CONF_SHOPPING_TARGETS
from .base import ProviderSetup, ShoppingProvider
from .ica import IcaShoppingProvider
from .ica import setup as ica_setup
from .todo import TodoProvider

ProviderFactory = Callable[[HomeAssistant, Mapping[str, Any]], ShoppingProvider | None]


class ShoppingRegistry:
    """Providers in registration order. A factory returns None when it is not set up."""

    def __init__(self) -> None:
        self._factories: dict[str, ProviderFactory] = {}
        self._setups: dict[str, ProviderSetup] = {}

    def register(
        self,
        provider_id: str,
        factory: ProviderFactory,
        setup: ProviderSetup | None = None,
    ) -> None:
        self._factories[provider_id] = factory
        if setup:
            self._setups[provider_id] = setup

    @property
    def setups(self) -> dict[str, ProviderSetup]:
        """Providers that have an account of their own to set up."""
        return dict(self._setups)

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


def _ica(hass: HomeAssistant, config: Mapping[str, Any]) -> ShoppingProvider | None:
    user, password = (
        config.get(ica_setup.CONF_USER),
        config.get(ica_setup.CONF_PASSWORD),
    )
    if not (user and password):
        return None
    return IcaShoppingProvider(
        hass,
        user,
        password,
        config.get(ica_setup.CONF_LIST_MODE) or "weekly",
        config.get(ica_setup.CONF_LIST_NAME),
    )


def build_default_shopping_registry() -> ShoppingRegistry:
    registry = ShoppingRegistry()
    registry.register(TodoProvider.id, _todo)
    registry.register(IcaShoppingProvider.id, _ica, ica_setup.SETUP)
    return registry
