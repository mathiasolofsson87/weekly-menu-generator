"""Ranking of eligible recipes. Deterministic code: the LLM proposes, this decides.

Waste, cost and variety terms follow PLAN.md section 14. Cost terms are skipped
until prices exist, never guessed.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from .constraints import preference_hits
from .models import FamilyMember, Recipe

STYLE_WEIGHT = 3.0
REPEAT_PENALTY = 6.0
DISLIKE_PENALTY = 2.0
LIKE_BONUS = 0.5
REUSE_BONUS = 0.4
REUSE_CAP = 2.0


@dataclass
class ScoreContext:
    """What a recipe is scored against."""

    style_tags: list[str]
    recent_ids: set[str]
    picked: list[Recipe]  # recipes already chosen for other days this week


def _names(recipe: Recipe) -> set[str]:
    return {i.name for i in recipe.ingredients if i.name}


def score(
    recipe: Recipe, attendees: Iterable[FamilyMember], ctx: ScoreContext
) -> float:
    total = 0.0
    if ctx.style_tags:
        matched = len(set(ctx.style_tags) & set(recipe.tags))
        total += STYLE_WEIGHT * matched / len(ctx.style_tags)
    if recipe.id in ctx.recent_ids:
        total -= REPEAT_PENALTY
    dislikes, likes = preference_hits(recipe, attendees)
    total += LIKE_BONUS * likes - DISLIKE_PENALTY * dislikes
    # Waste: sharing ingredients with other days means packages get finished.
    shared = sum(len(_names(recipe) & _names(other)) for other in ctx.picked)
    total += min(REUSE_CAP, REUSE_BONUS * shared)
    return total
