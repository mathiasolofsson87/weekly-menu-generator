"""Persistent ratings and favorites, per family member.

Kept apart from the menus, which are dropped after a few weeks. A recipe is stored in full
as long as anyone has it as a favorite or has rated it, so it can be offered again even when
its source no longer lists it. When nobody refers to a recipe any more, or everyone who rated
it gave 2 stars or less and nobody favorited it, the copy goes (the ratings stay).
"""

from __future__ import annotations

from collections.abc import Iterable

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from .const import DOMAIN
from .planner.models import Recipe
from .planner.taste import Taste

STORAGE_VERSION = 1
LIKED_STARS = 4  # a rating at or above this makes a recipe worth offering again
DISLIKED_STARS = 2  # a recipe rated this or lower by everyone who rated it is let go


class TasteStore:
    def __init__(self, hass: HomeAssistant, entry_id: str) -> None:
        self._store: Store[dict] = Store(
            hass, STORAGE_VERSION, f"{DOMAIN}.{entry_id}.taste"
        )
        self.ratings: dict[str, dict[str, int]] = {}  # member -> recipe -> stars
        self.favorites: dict[str, list[str]] = {}  # member -> recipe ids, oldest first
        self.recipes: dict[str, Recipe] = {}

    async def async_load(self) -> None:
        data = await self._store.async_load() or {}
        self.ratings = {
            m: {r: int(n) for r, n in given.items() if 1 <= int(n) <= 5}
            for m, given in data.get("ratings", {}).items()
        }
        self.favorites = {m: list(ids) for m, ids in data.get("favorites", {}).items()}
        self.recipes = {
            r: Recipe.from_dict(v) for r, v in data.get("recipes", {}).items()
        }

    async def async_save(self) -> None:
        self._collect_garbage()
        await self._store.async_save(
            {
                "ratings": self.ratings,
                "favorites": self.favorites,
                "recipes": {r: v.as_dict() for r, v in self.recipes.items()},
            }
        )

    # --- changes (the caller saves) ----------------------------------------------

    def set_rating(self, member_id: str, recipe: Recipe, stars: int | None) -> None:
        """Rate a recipe 1 to 5, or clear the rating with None."""
        given = self.ratings.setdefault(member_id, {})
        if stars is None:
            given.pop(recipe.id, None)
        else:
            given[recipe.id] = stars
            self.recipes[recipe.id] = recipe

    def set_favorite(self, member_id: str, recipe: Recipe, favorite: bool) -> None:
        ids = self.favorites.setdefault(member_id, [])
        if favorite:
            if recipe.id not in ids:
                ids.append(recipe.id)
            self.recipes[recipe.id] = recipe
        elif recipe.id in ids:
            ids.remove(recipe.id)

    def prune(self, member_ids: Iterable[str]) -> bool:
        """Forget members that no longer exist. True when something was removed."""
        keep = set(member_ids)
        gone = (set(self.ratings) | set(self.favorites)) - keep
        for member_id in gone:
            self.ratings.pop(member_id, None)
            self.favorites.pop(member_id, None)
        return bool(gone)

    def _collect_garbage(self) -> None:
        self.ratings = {m: g for m, g in self.ratings.items() if g}
        self.favorites = {m: ids for m, ids in self.favorites.items() if ids}
        # A recipe that is only rated low is not worth keeping a copy of. The ratings stay,
        # so the planner still avoids it when a source offers it again.
        best: dict[str, int] = {}
        for given in self.ratings.values():
            for recipe_id, stars in given.items():
                best[recipe_id] = max(stars, best.get(recipe_id, 0))
        used = {r for r, stars in best.items() if stars > DISLIKED_STARS} | {
            r for ids in self.favorites.values() for r in ids
        }
        self.recipes = {r: v for r, v in self.recipes.items() if r in used}

    # --- reading -----------------------------------------------------------------

    def rating(self, member_id: str, recipe_id: str) -> int | None:
        return self.ratings.get(member_id, {}).get(recipe_id)

    def ratings_of(self, recipe_id: str) -> dict[str, int]:
        """member id -> stars, for one recipe."""
        return {m: g[recipe_id] for m, g in self.ratings.items() if recipe_id in g}

    def favorite_of(self, recipe_id: str) -> list[str]:
        """Ids of the members that have the recipe as a favorite."""
        return [m for m, ids in self.favorites.items() if recipe_id in ids]

    def favorites_of(self, member_id: str) -> list[Recipe]:
        return [
            self.recipes[r]
            for r in self.favorites.get(member_id, [])
            if r in self.recipes
        ]

    def favorite_ids(self) -> set[str]:
        return {r for ids in self.favorites.values() for r in ids}

    def liked_recipes(self) -> list[Recipe]:
        """Favorites of anyone, and recipes someone rated 4 or 5 stars."""
        wanted = self.favorite_ids() | {
            r for g in self.ratings.values() for r, n in g.items() if n >= LIKED_STARS
        }
        return [self.recipes[r] for r in wanted if r in self.recipes]

    def recipe(self, recipe_id: str) -> Recipe | None:
        return self.recipes.get(recipe_id)

    def snapshot(self) -> Taste:
        """The planner's view."""
        taste = Taste()
        for member_id, given in self.ratings.items():
            for recipe_id, stars in given.items():
                taste.ratings.setdefault(recipe_id, {})[member_id] = stars
        for member_id, ids in self.favorites.items():
            for recipe_id in ids:
                taste.favorites.setdefault(recipe_id, set()).add(member_id)
        return taste
