"""What each family member thinks of the recipes, as the planner reads it.

Ratings are 1 to 5 stars per member. For a day, only the people eating count, a child
counts half of an adult, a dislike weighs more than a like of the same size, and a 1-star
rating from anyone eating is close to a veto. Allergies and diets are checked elsewhere
first, so nothing here can make an unsafe recipe eligible.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field

from .models import FamilyMember

CHILD_WEIGHT = 0.5
DISLIKE_FACTOR = 1.5  # stars below 3 count this much more than stars above 3
RATING_SCALE = 1.5  # points per star away from 3, on the planner's score scale
FAVORITE_BONUS = 1.5  # when every attendee has the recipe as a favorite
SPREAD_PENALTY = (
    1.0  # off when everyone who loves the favorite already has one this week
)
VETO_STARS = 1


@dataclass
class Taste:
    """Ratings and favorites keyed by recipe id, then member id."""

    ratings: dict[str, dict[str, int]] = field(default_factory=dict)
    favorites: dict[str, set[str]] = field(default_factory=dict)

    def favorite_ids(self) -> set[str]:
        return {r for r, who in self.favorites.items() if who}

    def known(self, recipe_id: str) -> bool:
        """True when anyone has rated the recipe or has it as a favorite."""
        return bool(self.ratings.get(recipe_id)) or bool(self.favorites.get(recipe_id))

    def vetoed(self, recipe_id: str, attendees: Iterable[FamilyMember]) -> bool:
        """True when someone eating that day gave the recipe the lowest rating."""
        given = self.ratings.get(recipe_id, {})
        return any(given.get(m.id) == VETO_STARS for m in attendees)

    def score(
        self,
        recipe_id: str,
        attendees: Iterable[FamilyMember],
        served: Iterable[str] = (),
    ) -> float:
        """Bonus or penalty for the people eating. Unrated and unloved recipes score 0.

        `served` are the members who already have a favorite on this week's menu: a favorite
        that only repeats them scores less, so each gets one in turn."""
        people = list(attendees)
        weight = {m.id: CHILD_WEIGHT if m.child else 1.0 for m in people}
        total = 0.0

        given = self.ratings.get(recipe_id, {})
        rated = [(weight[m.id], given[m.id] - 3) for m in people if m.id in given]
        if rated:
            points = sum(w * (p * DISLIKE_FACTOR if p < 0 else p) for w, p in rated)
            total += RATING_SCALE * points / sum(w for w, _ in rated)

        loved = self.favorites.get(recipe_id, set())
        everyone = sum(weight.values())
        if loved and everyone:
            share = sum(w for m_id, w in weight.items() if m_id in loved) / everyone
            total += FAVORITE_BONUS * share
            again = sum(
                w for m_id, w in weight.items() if m_id in loved and m_id in served
            )
            total -= SPREAD_PENALTY * again / everyone
        return total
