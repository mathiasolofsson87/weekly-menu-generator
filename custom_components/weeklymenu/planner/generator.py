"""Plans a whole week: asks the source chain for candidates, filters, ranks, picks."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

from homeassistant.util import dt as dt_util

from ..const import WEEKDAYS
from ..sources.base import CandidateRequest, RecipeSource, SourceError
from .constraints import has_fish, is_vegetarian
from .eligibility import assess
from .models import FamilyMember, Menu, MenuDay, Recipe, Split
from .scoring import SPLIT_PENALTY, ScoreContext, score

_LOGGER = logging.getLogger(__name__)


@dataclass
class PlannerSettings:
    """Everything the generator needs, independent of Home Assistant."""

    dinner_days: list[str]
    members: list[FamilyMember] = field(default_factory=list)
    language: str = "sv"
    style_tags: list[str] = field(default_factory=list)
    vegetarian_days: int = 0
    fish_min: int = 0
    candidates_per_day: int = 3
    max_split_days: int = 0  # dinners where some members get a substitute protein


def attendees_for(settings: PlannerSettings, weekday: str) -> list[FamilyMember] | None:
    """Members eating on `weekday`. None means nobody does, so the day is skipped.
    With no members configured, every dinner day is planned without constraints."""
    if not settings.members:
        return []
    present = [m for m in settings.members if weekday in m.attends]
    return present or None


def _enough(
    pool: list[Recipe], days: list[tuple[str, list[FamilyMember]]], want: int
) -> bool:
    """True when each day has `want` eligible recipes and the pool can fill the week."""
    eligible = [{r.id for r in pool if assess(r, who).ok} for _, who in days]
    union = set().union(*eligible) if eligible else set()
    return all(len(e) >= want for e in eligible) and len(union) >= len(days)


async def async_generate_menu(
    sources: list[RecipeSource],
    settings: PlannerSettings,
    week_start: date,
    recent_ids: set[str],
) -> Menu:
    """Build a draft menu for the week starting `week_start` (a Monday)."""
    menu = Menu(
        week_start=week_start.isoformat(),
        generated_at=dt_util.utcnow().isoformat(),
    )
    days: list[tuple[str, list[FamilyMember]]] = []
    for weekday in WEEKDAYS:
        if (
            weekday in settings.dinner_days
            and (who := attendees_for(settings, weekday)) is not None
        ):
            days.append((weekday, who))
    if not days:
        menu.warnings.append("no_days")
        return menu

    everyone = settings.members
    request = CandidateRequest(
        count=len(days) * settings.candidates_per_day,
        language=settings.language,
        tags=settings.style_tags,
        avoid=sorted({t for m in everyone for t in (*m.allergies, *m.dislikes)}),
        diets=sorted({m.diet for m in everyone}),
        separable=settings.max_split_days > 0
        and (
            len({m.diet for m in everyone}) > 1
            or any(m.allergies and m.cook_separately for m in everyone)
        ),
        exclude_ids=set(recent_ids),
        accept=lambda recipe: any(assess(recipe, who).ok for _, who in days),
    )

    # Ask sources in priority order; fall through while the week cannot be filled.
    pool: dict[str, Recipe] = {}
    for source in sources:
        try:
            for recipe in await source.async_candidates(request):
                pool.setdefault(recipe.id, recipe)
        except SourceError as err:
            _LOGGER.warning("Recipe source %s failed: %s", source.id, err)
            menu.warnings.append(f"source_failed:{source.id}")
            continue
        if _enough(list(pool.values()), days, settings.candidates_per_day):
            break
    if not sources:
        menu.warnings.append("no_sources")

    picked: list[Recipe] = []
    chosen: dict[str, tuple[Recipe, Split | None]] = {}
    veg_left, fish_left = settings.vegetarian_days, settings.fish_min
    splits_used = 0

    for index, (weekday, who) in enumerate(days):
        days_left = len(days) - index
        taken = {p.id for p in picked}
        options = [
            (r, a.split)
            for r in pool.values()
            if r.id not in taken and (a := assess(r, who)).ok
        ]
        # The split limit is kept unless it would leave the day empty.
        within_limit = [
            o for o in options if o[1] is None or splits_used < settings.max_split_days
        ]
        if within_limit:
            options = within_limit
        elif options:
            menu.warnings.append(f"split_limit_exceeded:{weekday}")
        # A quota that needs every remaining day is a hard filter, if anything qualifies.
        for needed, test in ((veg_left, is_vegetarian), (fish_left, has_fish)):
            if needed >= days_left and any(test(r) for r, _ in options):
                options = [o for o in options if test(o[0])]
        ctx = ScoreContext(settings.style_tags, recent_ids, picked)
        ranked = sorted(
            options,
            key=lambda o: (
                -(score(o[0], who, ctx) - (SPLIT_PENALTY if o[1] else 0)),
                o[0].title,
            ),
        )
        if not ranked:
            menu.warnings.append(f"no_recipe:{weekday}")
            continue
        best, split = ranked[0]
        chosen[weekday] = (best, split)
        picked.append(best)
        splits_used += split is not None
        veg_left -= is_vegetarian(best)
        fish_left -= has_fish(best)

    for weekday, who in days:
        recipe, split = chosen.get(weekday, (None, None))
        offset = timedelta(days=WEEKDAYS.index(weekday))
        alternatives = [
            r
            for r in pool.values()
            if r.id not in {p.id for p in picked} and assess(r, who).ok
        ]
        ctx = ScoreContext(
            settings.style_tags, recent_ids, [p for p in picked if p is not recipe]
        )
        alternatives.sort(key=lambda r: (-score(r, who, ctx), r.title))
        menu.days.append(
            MenuDay(
                date=(week_start + offset).isoformat(),
                weekday=weekday,
                recipe=recipe,
                candidates=([recipe] if recipe else [])
                + alternatives[: settings.candidates_per_day - 1],
                split=split,
            )
        )
    return menu


def week_start_of(day: date | datetime) -> date:
    """The Monday of the week containing `day`."""
    d = day.date() if isinstance(day, datetime) else day
    return d - timedelta(days=d.weekday())
