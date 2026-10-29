"""Recipe source backed by ica.se.

Discovery: the `/recept/middag/` page lists dish-type pages (pasta, soup, tacos...);
each such page lists about twenty popular recipes. A few random ones are read per
run, so the pool changes from week to week. Recipe pages are read once and kept in
a persistent cache. Requests are rate limited, budgeted per run and sent with an
honest User-Agent.
"""

from __future__ import annotations

import asyncio
import logging
import random
from datetime import datetime, timedelta
from typing import Any

from aiohttp import ClientError, ClientTimeout
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.storage import Store
from homeassistant.util import dt as dt_util

from ...const import DOMAIN
from ...planner.models import Recipe
from ..base import CandidateRequest, RecipeSource, SourceError
from .parser import (
    SOURCE_ID,
    absolute,
    parse_dish_paths,
    parse_listing,
    parse_recipe,
    recipe_id_from_url,
)

_LOGGER = logging.getLogger(__name__)

USER_AGENT = (
    "WeeklyMenuGenerator/0.1 (+https://github.com/mathiasolofsson87/weekly-menu-generator; "
    "Home Assistant integration; planning family dinners)"
)
DINNER_ROOT = "/recept/middag/"
REQUEST_INTERVAL = 1.0  # seconds between requests
REQUEST_TIMEOUT = ClientTimeout(total=30)
MAX_LISTING_FETCHES = 6  # listing pages read per run
MAX_RECIPE_FETCHES = 40  # recipe pages read per run
MAX_FAILURES = 3  # consecutive failed requests before giving up
PATHS_TTL = timedelta(days=30)
LISTING_TTL = timedelta(days=14)
RECIPE_TTL = timedelta(days=90)
MAX_CACHED_DINNERS = 600
MAX_CACHED_SKIPS = 3000
STORAGE_VERSION = 1


def _fresh(entry: dict[str, Any] | None, ttl: timedelta, now: datetime) -> bool:
    if not entry:
        return False
    try:
        return now - datetime.fromisoformat(entry["fetched"]) < ttl
    except (KeyError, ValueError):
        return False


class IcaRecipeSource(RecipeSource):
    """Dinner recipes from ica.se."""

    id = SOURCE_ID

    def __init__(
        self,
        hass: HomeAssistant,
        *,
        rng: random.Random | None = None,
        min_interval: float = REQUEST_INTERVAL,
    ) -> None:
        self.hass = hass
        self._rng = rng or random.Random()
        self._min_interval = min_interval
        self._store: Store[dict[str, Any]] = Store(
            hass, STORAGE_VERSION, f"{DOMAIN}.ica_cache"
        )
        self._cache: dict[str, Any] = {}
        self._last_request = 0.0
        self._failures = 0

    # --- network -------------------------------------------------------------

    async def _get(self, url: str) -> str:
        """One polite GET. Raises SourceError, and gives up after repeated failures."""
        if self._failures >= MAX_FAILURES:
            raise SourceError("ica.se keeps failing, giving up for now")
        loop = asyncio.get_running_loop()
        wait = self._last_request + self._min_interval - loop.time()
        if wait > 0:
            await asyncio.sleep(wait)
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(
                url,
                headers={"User-Agent": USER_AGENT, "Accept-Language": "sv-SE,sv;q=0.9"},
                timeout=REQUEST_TIMEOUT,
            ) as response:
                self._last_request = loop.time()
                if response.status != 200:
                    raise SourceError(
                        f"ica.se answered HTTP {response.status} for {url}"
                    )
                text = await response.text()
        except (ClientError, TimeoutError) as err:
            self._last_request = loop.time()
            self._failures += 1
            raise SourceError(f"Could not reach ica.se: {err}") from err
        except SourceError:
            self._failures += 1
            raise
        self._failures = 0
        return text

    # --- cache -------------------------------------------------------------------

    async def _load(self) -> None:
        data = await self._store.async_load() or {}
        self._cache = {
            "paths": data.get("paths"),
            "listings": data.get("listings", {}),
            "recipes": data.get("recipes", {}),
        }

    def _prune(self, now: datetime) -> None:
        recipes: dict[str, Any] = self._cache["recipes"]
        stale = [k for k, v in recipes.items() if not _fresh(v, RECIPE_TTL, now)]
        for key in stale:
            del recipes[key]
        for dinner, limit in ((True, MAX_CACHED_DINNERS), (False, MAX_CACHED_SKIPS)):
            kept = sorted(
                (k for k, v in recipes.items() if v["dinner"] is dinner),
                key=lambda k: recipes[k]["fetched"],
            )
            for key in kept[: max(0, len(kept) - limit)]:
                del recipes[key]
        self._cache["listings"] = {
            k: v
            for k, v in self._cache["listings"].items()
            if _fresh(v, LISTING_TTL, now)
        }

    async def _save(self) -> None:
        self._prune(dt_util.utcnow())
        await self._store.async_save(self._cache)

    # --- discovery -------------------------------------------------------------

    async def _dish_paths(self, now: datetime) -> list[str]:
        if not _fresh(self._cache["paths"], PATHS_TTL, now):
            html = await self._get(absolute(DINNER_ROOT))
            slugs = parse_dish_paths(html)
            if not slugs:
                raise SourceError(
                    "Found no dish-type pages on ica.se: the page layout may have changed"
                )
            self._cache["paths"] = {"fetched": now.isoformat(), "slugs": slugs}
        return list(self._cache["paths"]["slugs"])

    async def _listing(self, path: str, now: datetime) -> list[str]:
        entry = self._cache["listings"].get(path)
        if not _fresh(entry, LISTING_TTL, now):
            urls = parse_listing(await self._get(absolute(path)))
            entry = self._cache["listings"][path] = {
                "fetched": now.isoformat(),
                "urls": urls,
            }
        return list(entry["urls"])

    async def _recipe(self, url: str, now: datetime) -> Recipe | None:
        """The dinner recipe at `url`, from cache or ica.se. None if it is not a dinner."""
        key = recipe_id_from_url(url) or url
        entry = self._cache["recipes"].get(key)
        if not _fresh(entry, RECIPE_TTL, now):
            parsed = parse_recipe(await self._get(url), url)
            dinner = bool(parsed and parsed.is_dinner)
            entry = self._cache["recipes"][key] = {
                "fetched": now.isoformat(),
                "dinner": dinner,
                "recipe": parsed.recipe.as_dict() if dinner and parsed else None,
            }
        return Recipe.from_dict(entry["recipe"]) if entry["recipe"] else None

    def _usable(self, urls: list[str], request: CandidateRequest) -> list[str]:
        skipped = {k for k, v in self._cache["recipes"].items() if not v["dinner"]}
        return [
            u
            for u in urls
            if (rid := recipe_id_from_url(u))
            and rid not in skipped
            and Recipe.make_id(SOURCE_ID, rid) not in request.exclude_ids
        ]

    # --- RecipeSource ------------------------------------------------------------

    async def async_candidates(self, request: CandidateRequest) -> list[Recipe]:
        await self._load()
        self._failures = 0
        now = dt_util.utcnow()
        result: list[Recipe] = []
        error: SourceError | None = None
        try:
            result = await self._collect(request, now)
        except SourceError as err:
            error = err
            _LOGGER.warning("ICA recipes: %s", err)
        finally:
            await self._save()
        if not result and error:
            raise error
        return result

    async def _collect(self, request: CandidateRequest, now: datetime) -> list[Recipe]:
        slugs = await self._dish_paths(now)
        paths = [DINNER_ROOT] + [f"{DINNER_ROOT}{slug}/" for slug in slugs]

        # Gather enough recipe URLs: cached listings first, then a few fresh random pages.
        pool: dict[str, None] = {}
        for path in paths:
            if _fresh(self._cache["listings"].get(path), LISTING_TTL, now):
                pool.update(dict.fromkeys(self._cache["listings"][path]["urls"]))
        wanted = request.count * 4
        fetched = 0
        unread = [
            p
            for p in paths
            if not _fresh(self._cache["listings"].get(p), LISTING_TTL, now)
        ]
        self._rng.shuffle(unread)
        try:
            while (
                len(self._usable(list(pool), request)) < wanted
                and unread
                and fetched < MAX_LISTING_FETCHES
            ):
                fetched += 1
                pool.update(dict.fromkeys(await self._listing(unread.pop(), now)))
        except SourceError:
            if not pool:
                raise

        urls = self._usable(list(pool), request)
        self._rng.shuffle(urls)
        # Recipes we already know cost nothing, so try them before spending requests.
        urls.sort(key=lambda u: recipe_id_from_url(u) not in self._cache["recipes"])

        result: list[Recipe] = []
        reads = 0
        for url in urls:
            if len(result) >= request.count:
                break
            known = recipe_id_from_url(url) in self._cache["recipes"]
            if not known:
                if reads >= MAX_RECIPE_FETCHES:
                    break
                reads += 1
            try:
                recipe = await self._recipe(url, now)
            except SourceError:
                if self._failures < MAX_FAILURES:
                    continue  # one bad page is not the end of the run
                if result:
                    break  # keep what we have
                raise
            if recipe and (request.accept is None or request.accept(recipe)):
                result.append(recipe)
        return result
