"""Data models for shopping."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

# What happened to an item
PENDING = "pending"
ADDED = "added"
REVIEW = "review"  # a provider could not place it; it is on the review list
FAILED = "failed"  # could not be delivered anywhere; retry with add_to_shopping
SKIPPED = "skipped"  # a pantry staple, not bought


def format_number(value: float, language: str) -> str:
    """12, 1.5 (en) or 1,5 (sv); never 12.0."""
    text = f"{value:.2f}".rstrip("0").rstrip(".")
    return text.replace(".", ",") if language == "sv" else text


@dataclass
class ShoppingItem:
    """One line on a shopping list."""

    name: str
    amount: float | None = None
    unit: str | None = None
    recipes: list[str] = field(default_factory=list)  # titles of the recipes needing it
    note: str = ""  # the original wording when the name was shortened
    special: bool = (
        False  # a substitute for someone's diet or allergy: never a pantry staple
    )
    status: str = PENDING

    def text(self, language: str = "sv") -> str:
        """The line as written on a list: "350 g nötfärs"."""
        parts = []
        if self.amount is not None:
            parts.append(format_number(self.amount, language))
            if self.unit:
                parts.append(self.unit)
        parts.append(self.name)
        return " ".join(parts)

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "amount": self.amount,
            "unit": self.unit,
            "recipes": list(self.recipes),
            "note": self.note,
            "special": self.special,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> ShoppingItem:
        return cls(
            name=data["name"],
            amount=data.get("amount"),
            unit=data.get("unit"),
            recipes=list(data.get("recipes", [])),
            note=data.get("note", ""),
            special=data.get("special", False),
            status=data.get("status", PENDING),
        )


@dataclass
class ShoppingResult:
    """What was bought for a menu and where it went."""

    items: list[ShoppingItem] = field(default_factory=list)
    targets: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    updated_at: str = ""
    language: str = "sv"

    def with_status(self, status: str) -> list[ShoppingItem]:
        return [i for i in self.items if i.status == status]

    @property
    def counts(self) -> dict[str, int]:
        return {
            s: len(self.with_status(s))
            for s in (ADDED, REVIEW, FAILED, SKIPPED, PENDING)
        }

    def touch(self) -> None:
        self.updated_at = datetime.now().astimezone().isoformat()

    def as_dict(self) -> dict[str, Any]:
        return {
            "items": [i.as_dict() for i in self.items],
            "targets": list(self.targets),
            "errors": list(self.errors),
            "updated_at": self.updated_at,
            "language": self.language,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> ShoppingResult:
        return cls(
            items=[ShoppingItem.from_dict(i) for i in data.get("items", [])],
            targets=list(data.get("targets", [])),
            errors=list(data.get("errors", [])),
            updated_at=data.get("updated_at", ""),
            language=data.get("language", "sv"),
        )
