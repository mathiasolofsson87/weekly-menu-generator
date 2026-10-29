"""Turns ica.se pages into data. Pure functions: no network, no Home Assistant.

Recipe pages carry a schema.org `Recipe` in JSON-LD. Listing pages carry an
`ItemList` of recipe URLs and, in their embedded page state, the filter paths
(dish types, diets, ingredients) that become further listing pages.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

from ...planner.ingredients import parse_ingredient
from ...planner.models import Recipe

BASE_URL = "https://www.ica.se"
SOURCE_ID = "ica"

_LD_BLOCK = re.compile(
    r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', re.DOTALL
)
_RECIPE_URL = re.compile(r"/recept/[^/\s\"'<>]*?-(\d+)/?$")
_RECIPE_HREF = re.compile(
    r'href="((?:https://www\.ica\.se)?/recept/[^/\s"\'<>]*?-\d+/)"'
)
# Embedded page state escapes slashes as the six characters /.
_FILTER_PATH = re.compile(
    r'"actionUrl":"(?:\\u002F|/)middag(?:\\u002F|/)([a-z0-9åäöé\-]+)(?:\\u002F|/)"'
)
_DURATION = re.compile(r"^P(?:\d+D)?T?(?:(\d+)H)?(?:(\d+)M)?")

# Dish-type pages that only hold things nobody eats for dinner.
NOT_DINNER_PATHS = frozenset(
    {
        "bakverk", "muffins", "tarta", "smorgastarta", "baklava", "biscotti", "biskvier",
        "brod", "scones", "focaccia", "cake-pop", "chiapudding", "churros", "cookie",
        "croissant", "dessert", "dressing", "ceasardressing", "hamburgerdressing",
        "vinagrett", "dryck", "cocktail", "drink", "mojito", "drommar", "frosting",
        "ganache", "glass", "glasyr", "glaze", "godis", "grot", "havreflarn", "kristyr",
        "kryddsmor", "kram", "macaron", "marinad", "mazarin", "munk", "musli", "pavlova",
        "petit-choux", "pudding", "ris-a-la-malta", "rocky-road", "rub", "sylt",
        "kladdkaka", "semlor", "vafflor", "efterratt", "frukost", "fika", "mellanmal",
        "forratt", "brunch", "snacks", "snittar", "tilltugg", "te", "kaffe", "choklad",
        "alla-hjartans-dag", "jul", "pask", "midsommar", "nyar", "halloween", "advent",
    }
)  # fmt: skip
_BAD_CATEGORIES = ("dessert", "efterrätt", "bakverk", "dryck", "sötsak", "bröd", "fika")


@dataclass(frozen=True)
class ParsedRecipe:
    recipe: Recipe
    is_dinner: bool


def recipe_id_from_url(url: str) -> str | None:
    """The numeric id at the end of a recipe URL, or None if it is not a recipe URL."""
    match = _RECIPE_URL.search(url.split("?")[0])
    return match.group(1) if match else None


def absolute(path_or_url: str) -> str:
    return path_or_url if path_or_url.startswith("http") else BASE_URL + path_or_url


def _ld_objects(html: str) -> list[dict[str, Any]]:
    """Every JSON-LD object on the page, with lists and @graph flattened."""
    found: list[dict[str, Any]] = []

    def add(node: Any) -> None:
        if isinstance(node, list):
            for item in node:
                add(item)
        elif isinstance(node, dict):
            found.append(node)
            add(node.get("@graph"))

    for block in _LD_BLOCK.findall(html):
        try:
            add(json.loads(block))
        except ValueError:
            continue
    return found


def _has_type(node: dict[str, Any], wanted: str) -> bool:
    kind = node.get("@type")
    return kind == wanted or (isinstance(kind, list) and wanted in kind)


def parse_listing(html: str) -> list[str]:
    """Recipe URLs on a listing page, in page order."""
    urls: list[str] = []
    for node in _ld_objects(html):
        if _has_type(node, "ItemList"):
            urls += [
                item["url"]
                for item in node.get("itemListElement", [])
                if isinstance(item, dict) and item.get("url")
            ]
    if not urls:  # markup changed: fall back to plain links
        urls = [absolute(href) for href in _RECIPE_HREF.findall(html)]
    seen: dict[str, None] = {}
    for url in urls:
        if recipe_id_from_url(url):
            seen.setdefault(absolute(url), None)
    return list(seen)


def parse_dish_paths(html: str) -> list[str]:
    """Slugs of the dish-type pages (`/recept/middag/<slug>/`) that look like dinner."""
    slugs: dict[str, None] = {}
    for slug in _FILTER_PATH.findall(html):
        if slug not in NOT_DINNER_PATHS:
            slugs.setdefault(slug, None)
    return list(slugs)


def _minutes(value: Any) -> int | None:
    match = _DURATION.match(str(value)) if value else None
    if not match or not (match.group(1) or match.group(2)):
        return None
    return int(match.group(1) or 0) * 60 + int(match.group(2) or 0)


def _servings(value: Any) -> int | None:
    if isinstance(value, list):
        value = value[0] if value else None
    match = re.search(r"\d+", str(value)) if value is not None else None
    return int(match.group(0)) if match else None


def _image(value: Any) -> str | None:
    if isinstance(value, list):
        value = value[0] if value else None
    if isinstance(value, dict):
        value = value.get("url")
    return value if isinstance(value, str) and value else None


def _words(*values: Any) -> str:
    parts: list[str] = []
    for value in values:
        parts += (
            [str(v) for v in value] if isinstance(value, list) else [str(value or "")]
        )
    return ",".join(parts).casefold()


def derive_tags(total_time: int | None, categories: str) -> list[str]:
    """Map ICA's own labels to the style tags the planner understands."""
    tags = []
    if total_time is not None and total_time <= 30:
        tags.append("quick")
    if "enkel" in categories or "lättlagad" in categories:
        tags.append("easy")
    if "fest" in categories or "helg" in categories:
        tags.append("fancy")
    if "barn" in categories:
        tags.append("family_friendly")
    if "billig" in categories:
        tags.append("budget")
    if "vegetarisk" in categories or "vegan" in categories:
        tags.append("vegetarian")
    if "fisk" in categories:
        tags.append("fish")
    return tags


def parse_recipe(html: str, url: str) -> ParsedRecipe | None:
    """The recipe on a page, or None if the page has no usable Recipe data."""
    external_id = recipe_id_from_url(url)
    node = next((n for n in _ld_objects(html) if _has_type(n, "Recipe")), None)
    if node is None or external_id is None:
        return None
    title = str(node.get("name") or "").strip()
    lines = [
        str(line).strip()
        for line in node.get("recipeIngredient") or []
        if str(line).strip()
    ]
    if not title or not lines:
        return None

    categories = _words(
        node.get("recipeCategory"), node.get("recipeCuisine"), node.get("keywords")
    )
    total_time = _minutes(node.get("totalTime"))
    is_dinner = ("middag" in categories or "huvudrätt" in categories) and not any(
        bad in categories for bad in _BAD_CATEGORIES
    )
    return ParsedRecipe(
        Recipe(
            id=Recipe.make_id(SOURCE_ID, external_id),
            source=SOURCE_ID,
            title=title,
            ingredients=[parse_ingredient(line) for line in lines],
            external_id=external_id,
            url=absolute(str(node.get("url") or url)),
            image=_image(node.get("image")),
            total_time=total_time,
            servings=_servings(node.get("recipeYield")),
            tags=derive_tags(total_time, categories),
        ),
        is_dinner,
    )
