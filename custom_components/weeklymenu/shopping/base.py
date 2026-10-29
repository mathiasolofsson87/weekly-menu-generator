"""The interface every shopping provider implements."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar

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
    async def async_push(self, items: list[ShoppingItem], language: str) -> PushResult:
        """Deliver `items`. Never raise for a single bad item; report it in the result."""
