"""Registry of recipe sources. The only module that imports concrete providers.

Core code asks the registry for sources by id and never names a provider itself, so
a new store (Coop, Willys, ...) is added here and nowhere else.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

from homeassistant.core import HomeAssistant

from ..const import CONF_AI_TASK
from .ai_task import AiTaskSource
from .base import RecipeSource
from .ica import IcaRecipeSource

# Builds a source from the merged config, or returns None when it is not set up.
SourceFactory = Callable[[HomeAssistant, Mapping[str, Any]], RecipeSource | None]


@dataclass(frozen=True)
class SourceInfo:
    id: str
    factory: SourceFactory


class SourceRegistry:
    """Sources in priority order: earlier registrations are asked first."""

    def __init__(self) -> None:
        self._sources: dict[str, SourceInfo] = {}

    def register(self, source_id: str, factory: SourceFactory) -> None:
        self._sources[source_id] = SourceInfo(source_id, factory)

    @property
    def ids(self) -> list[str]:
        return list(self._sources)

    def create(
        self,
        hass: HomeAssistant,
        config: Mapping[str, Any],
        enabled: list[str] | None = None,
    ) -> list[RecipeSource]:
        """Build the enabled, configured sources in priority order."""
        built = []
        for info in self._sources.values():
            if enabled is not None and info.id not in enabled:
                continue
            if source := info.factory(hass, config):
                built.append(source)
        return built


def _ica(hass: HomeAssistant, config: Mapping[str, Any]) -> RecipeSource | None:
    return IcaRecipeSource(hass)


def _ai_task(hass: HomeAssistant, config: Mapping[str, Any]) -> RecipeSource | None:
    entity_id = config.get(CONF_AI_TASK)
    return AiTaskSource(hass, entity_id) if entity_id else None


def build_default_registry() -> SourceRegistry:
    """Priority: store recipes first, then AI."""
    registry = SourceRegistry()
    registry.register(IcaRecipeSource.id, _ica)
    registry.register(AiTaskSource.id, _ai_task)
    return registry
