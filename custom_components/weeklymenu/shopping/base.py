"""The interface every shopping provider implements."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass, field
from typing import Any, ClassVar

import voluptuous as vol
from homeassistant.core import HomeAssistant

from .models import ShoppingItem


@dataclass
class PushResult:
    """What a provider did with the items it was given. Every item lands in exactly one list."""

    added: list[ShoppingItem] = field(default_factory=list)
    unmatched: list[ShoppingItem] = field(
        default_factory=list
    )  # needs a human: goes to the review list
    failed: list[ShoppingItem] = field(
        default_factory=list
    )  # not delivered: can be retried
    errors: list[str] = field(default_factory=list)
    needs_reauth: bool = (
        False  # the login stopped working: ask the user to sign in again
    )


class ShoppingProvider(ABC):
    """Puts items on a shopping list or into a cart."""

    id: ClassVar[str]
    # Optional features the core may check for, never the provider id itself
    # (for example "product_matching", "cart", "offers").
    capabilities: ClassVar[frozenset[str]] = frozenset()

    @property
    @abstractmethod
    def targets(self) -> list[str]:
        """Where items go, for display (list names or entity ids)."""

    @abstractmethod
    async def async_push(
        self, items: list[ShoppingItem], language: str, week_start: str = ""
    ) -> PushResult:
        """Deliver `items` for the menu of the week starting `week_start` (ISO date).
        Never raise for a single bad item; report it in the result."""


@dataclass(frozen=True)
class ProviderSetup:
    """How a provider is set up from the options and signed in again from the re-auth flow.

    The core renders `schema` and calls `validate` without knowing which provider it is,
    so account forms never leak provider details into the core config flow. Field labels
    come from the translations under the field keys, which are unique per provider."""

    id: str
    keys: tuple[str, ...]  # every config entry key the provider owns
    schema: Callable[[Mapping[str, Any]], vol.Schema]
    # (hass, current config, form input) -> (changes to the entry data, form errors).
    # A None value in the changes removes the key; an empty result with no errors is "no change".
    validate: Callable[
        [HomeAssistant, Mapping[str, Any], Mapping[str, Any]],
        Awaitable[tuple[dict[str, Any], dict[str, str]]],
    ]
    reauth_keys: tuple[
        str, ...
    ] = ()  # form fields asked again when the login stops working
    secret_keys: tuple[str, ...] = ()  # never shown again; left empty means "keep"
