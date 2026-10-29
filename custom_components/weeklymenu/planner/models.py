"""Data models for the planner."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import asdict, dataclass, field
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
