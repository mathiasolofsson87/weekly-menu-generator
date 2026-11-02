"""The family's own favorites and well-rated recipes, offered again from the local store."""

from __future__ import annotations

import random

from ..planner.models import Recipe
from ..taste import TasteStore
from .base import CandidateRequest, RecipeSource


class FavoritesSource(RecipeSource):
    """Known good dinners. A third of a request at most, so the menu stays a mix of old and new.

    Like every source it is untrusted: the planner runs the same allergy and diet checks on it."""

    id = "favorites"
    # Adds to what the real sources offer and never counts as "enough" on its own.
    capabilities = frozenset({"supplement"})

    def __init__(self, taste: TasteStore, rng: random.Random | None = None) -> None:
        self._taste = taste
        self._rng = rng or random.Random()

    async def async_candidates(self, request: CandidateRequest) -> list[Recipe]:
        usable = [
            r
            for r in self._taste.liked_recipes()
            if r.id not in request.exclude_ids
            and (request.accept is None or request.accept(r))
        ]
        self._rng.shuffle(usable)
        return usable[: max(1, request.count // 3)]
