"""The interface every recipe source implements."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar

from ..planner.models import Recipe


class SourceError(Exception):
    """A source could not deliver. The generator logs it and tries the next source."""


@dataclass
class CandidateRequest:
    """What the planner asks a source for. Sources may ignore what they cannot use."""

    count: int
    language: str = "sv"
    tags: list[str] = field(default_factory=list)
    avoid: list[str] = field(default_factory=list)  # allergies and dislikes
    diets: list[str] = field(default_factory=list)
    exclude_ids: set[str] = field(default_factory=set)
    use_up: list[str] = field(default_factory=list)
    hint: str | None = None


class RecipeSource(ABC):
    """Returns candidate recipes. It never decides what is safe to eat: the planner
    runs every candidate through the deterministic checks."""

    id: ClassVar[str]
    # Optional features the core may check for, never the provider id itself.
    capabilities: ClassVar[frozenset[str]] = frozenset()

    @abstractmethod
    async def async_candidates(self, request: CandidateRequest) -> list[Recipe]:
        """Return up to `request.count` candidates. Raise SourceError on failure."""
