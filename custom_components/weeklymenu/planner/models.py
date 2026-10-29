"""Data models for the planner."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import asdict, dataclass, field
from hashlib import sha1
from typing import Any
from uuid import uuid4

from ..const import (
    CONF_DINNER_DAYS,
    CONF_MEMBERS,
    DEFAULT_DINNER_DAYS,
    MEMBER_ALLERGIES,
    MEMBER_ATTENDS,
    MEMBER_DIET,
    MEMBER_DISLIKES,
    MEMBER_ID,
    MEMBER_LIKES,
    MEMBER_NAME,
    MEMBER_PERSON,
    MEMBER_PORTION,
    WEEKDAYS,
)


def clean_terms(values: Iterable[str] | None) -> list[str]:
    """Strip, lowercase and de-duplicate free-text terms, keeping order."""
    seen: dict[str, None] = {}
    for value in values or ():
        term = str(value).strip().casefold()
        if term:
            seen.setdefault(term, None)
    return list(seen)


@dataclass
class FamilyMember:
    """A person eating dinner. Allergies are hard constraints, the rest are soft."""

    name: str
    id: str = field(default_factory=lambda: uuid4().hex)
    person: str | None = None
    allergies: list[str] = field(default_factory=list)
    dislikes: list[str] = field(default_factory=list)
    likes: list[str] = field(default_factory=list)
    diet: str = "omnivore"
    portion: str = "normal"
    attends: list[str] = field(default_factory=lambda: list(DEFAULT_DINNER_DAYS))

    def as_dict(self) -> dict[str, Any]:
        """Serialize for storage in the config entry options."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> FamilyMember:
        """Build from stored data, tolerating missing keys and bad values."""
        return cls(
            name=data[MEMBER_NAME],
            id=data.get(MEMBER_ID) or uuid4().hex,
            person=data.get(MEMBER_PERSON) or None,
            allergies=clean_terms(data.get(MEMBER_ALLERGIES)),
            dislikes=clean_terms(data.get(MEMBER_DISLIKES)),
            likes=clean_terms(data.get(MEMBER_LIKES)),
            diet=data.get(MEMBER_DIET) or "omnivore",
            portion=data.get(MEMBER_PORTION) or "normal",
            attends=[
                d
                for d in data.get(MEMBER_ATTENDS, DEFAULT_DINNER_DAYS)
                if d in WEEKDAYS
            ],
        )


def members_from_options(options: Mapping[str, Any]) -> list[FamilyMember]:
    """Return the family members stored in the options."""
    return [FamilyMember.from_dict(m) for m in options.get(CONF_MEMBERS, [])]


def dinner_days_from_options(options: Mapping[str, Any]) -> list[str]:
    """Return the configured dinner weekdays in week order."""
    chosen = set(options.get(CONF_DINNER_DAYS, DEFAULT_DINNER_DAYS))
    return [d for d in WEEKDAYS if d in chosen]


@dataclass(frozen=True)
class Ingredient:
    """One structured ingredient line. `raw` keeps the original text."""

    name: str
    amount: float | None = None
    unit: str | None = None
    category: str | None = None
    raw: str = ""

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Ingredient:
        return cls(
            name=data["name"],
            amount=data.get("amount"),
            unit=data.get("unit"),
            category=data.get("category"),
            raw=data.get("raw", ""),
        )


@dataclass
class Recipe:
    """A recipe from any source. Only metadata and ingredients are stored."""

    id: str
    source: str
    title: str
    ingredients: list[Ingredient] = field(default_factory=list)
    external_id: str | None = None
    url: str | None = None
    image: str | None = None
    total_time: int | None = None  # minutes
    servings: int | None = None
    tags: list[str] = field(default_factory=list)

    @staticmethod
    def make_id(source: str, key: str) -> str:
        """Stable id from the provider id and a provider-side key."""
        return f"{source}:{key}"

    @staticmethod
    def key_from_title(title: str) -> str:
        """Key for sources without their own ids (for example AI suggestions)."""
        return sha1(title.strip().casefold().encode()).hexdigest()[:12]

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["ingredients"] = [i.as_dict() for i in self.ingredients]
        return data

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Recipe:
        return cls(
            id=data["id"],
            source=data["source"],
            title=data["title"],
            ingredients=[Ingredient.from_dict(i) for i in data.get("ingredients", [])],
            external_id=data.get("external_id"),
            url=data.get("url"),
            image=data.get("image"),
            total_time=data.get("total_time"),
            servings=data.get("servings"),
            tags=list(data.get("tags", [])),
        )


@dataclass
class Substitution:
    """One protein swapped for another, at the recipe's full scale."""

    original: Ingredient
    replacement: Ingredient

    def as_dict(self) -> dict[str, Any]:
        return {
            "original": self.original.as_dict(),
            "replacement": self.replacement.as_dict(),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Substitution:
        return cls(
            Ingredient.from_dict(data["original"]),
            Ingredient.from_dict(data["replacement"]),
        )


@dataclass
class Split:
    """Members who cannot eat the recipe's protein get a substitute instead.

    `share` is the fraction of the dinner's portions eaten by `members`, so shopping
    buys the original protein for the rest and the substitute for this share."""

    members: list[str]
    substitutions: list[Substitution]
    share: float

    def as_dict(self) -> dict[str, Any]:
        return {
            "members": list(self.members),
            "substitutions": [s.as_dict() for s in self.substitutions],
            "share": self.share,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Split:
        return cls(
            members=list(data["members"]),
            substitutions=[Substitution.from_dict(s) for s in data["substitutions"]],
            share=data["share"],
        )


@dataclass
class MenuDay:
    """One dinner. `candidates` holds the alternatives (the chosen recipe first)."""

    date: str  # ISO date
    weekday: str  # key from WEEKDAYS
    recipe: Recipe | None = None
    candidates: list[Recipe] = field(default_factory=list)
    locked: bool = False
    split: Split | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "split": self.split.as_dict() if self.split else None,
            "date": self.date,
            "weekday": self.weekday,
            "recipe": self.recipe.as_dict() if self.recipe else None,
            "candidates": [r.as_dict() for r in self.candidates],
            "locked": self.locked,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> MenuDay:
        recipe = data.get("recipe")
        return cls(
            date=data["date"],
            weekday=data["weekday"],
            recipe=Recipe.from_dict(recipe) if recipe else None,
            candidates=[Recipe.from_dict(r) for r in data.get("candidates", [])],
            locked=data.get("locked", False),
            split=Split.from_dict(data["split"]) if data.get("split") else None,
        )


@dataclass
class Menu:
    """A week of dinners. Starts as a draft; confirming comes in phase 4."""

    week_start: str  # ISO date of the Monday
    status: str = "draft"  # draft | confirmed
    days: list[MenuDay] = field(default_factory=list)
    generated_at: str = ""
    warnings: list[str] = field(default_factory=list)

    def day(self, iso_date: str) -> MenuDay | None:
        return next((d for d in self.days if d.date == iso_date), None)

    def as_dict(self) -> dict[str, Any]:
        return {
            "week_start": self.week_start,
            "status": self.status,
            "days": [d.as_dict() for d in self.days],
            "generated_at": self.generated_at,
            "warnings": list(self.warnings),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Menu:
        return cls(
            week_start=data["week_start"],
            status=data.get("status", "draft"),
            days=[MenuDay.from_dict(d) for d in data.get("days", [])],
            generated_at=data.get("generated_at", ""),
            warnings=list(data.get("warnings", [])),
        )
