"""Plans a whole week: asks the source chain for candidates, filters, ranks, picks."""

from __future__ import annotations

import logging
from collections.abc import Sequence
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


@dataclass
class _Planned:
    recipe: Recipe | None
    split: Split | None
    candidates: list[Recipe]


async def _plan(
    sources: list[RecipeSource],
    settings: PlannerSettings,
    targets: list[tuple[str, list[FamilyMember]]],
    kept: list[MenuDay],
    recent_ids: set[str],
    warnings: list[str],
    hint: str | None = None,
    avoid_ids: set[str] | None = None,
) -> dict[str, _Planned]:
    """Fill `targets` (weekday, attendees) around the already settled `kept` days.

    Kept days count towards variety, shared ingredients, the vegetarian and fish
    quotas and the split limit, so a regenerated day fits the rest of the week."""
    everyone = settings.members
    kept_recipes = [d.recipe for d in kept if d.recipe]
    request = CandidateRequest(
        count=max(len(targets), 2) * settings.candidates_per_day,
        language=settings.language,
        tags=settings.style_tags,
        avoid=sorted({t for m in everyone for t in (*m.allergies, *m.dislikes)}),
        diets=sorted({m.diet for m in everyone}),
        separable=settings.max_split_days > 0
        and (
            len({m.diet for m in everyone}) > 1
            or any(m.allergies and m.cook_separately for m in everyone)
        ),
        hint=hint,
        exclude_ids=set(recent_ids)
        | {r.id for r in kept_recipes}
        | (avoid_ids or set()),
        accept=lambda recipe: any(assess(recipe, who).ok for _, who in targets),
    )

    # Ask sources in priority order; fall through while the days cannot be filled.
    pool: dict[str, Recipe] = {}
    for source in sources:
        try:
            for recipe in await source.async_candidates(request):
                if recipe.id not in request.exclude_ids:
                    pool.setdefault(recipe.id, recipe)
        except SourceError as err:
            _LOGGER.warning("Recipe source %s failed: %s", source.id, err)
            warnings.append(f"source_failed:{source.id}")
            continue
        if _enough(list(pool.values()), targets, settings.candidates_per_day):
            break
    if not sources:
        warnings.append("no_sources")

    picked: list[Recipe] = list(kept_recipes)
    chosen: dict[str, tuple[Recipe, Split | None]] = {}
    veg_left = max(0, settings.vegetarian_days - sum(map(is_vegetarian, kept_recipes)))
    fish_left = max(0, settings.fish_min - sum(map(has_fish, kept_recipes)))
    splits_used = sum(d.split is not None for d in kept)

    for index, (weekday, who) in enumerate(targets):
        days_left = len(targets) - index
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
            warnings.append(f"split_limit_exceeded:{weekday}")
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
            warnings.append(f"no_recipe:{weekday}")
            continue
        best, split = ranked[0]
        chosen[weekday] = (best, split)
        picked.append(best)
        splits_used += split is not None
        veg_left -= is_vegetarian(best)
        fish_left -= has_fish(best)

    planned: dict[str, _Planned] = {}
    for weekday, who in targets:
        recipe, split = chosen.get(weekday, (None, None))
        alternatives = [
            r
            for r in pool.values()
            if r.id not in {p.id for p in picked} and assess(r, who).ok
        ]
        ctx = ScoreContext(
            settings.style_tags, recent_ids, [p for p in picked if p is not recipe]
        )
        alternatives.sort(key=lambda r: (-score(r, who, ctx), r.title))
        planned[weekday] = _Planned(
            recipe,
            split,
            ([recipe] if recipe else [])
            + alternatives[: settings.candidates_per_day - 1],
        )
    return planned


def planned_days(settings: PlannerSettings) -> list[tuple[str, list[FamilyMember]]]:
    """Dinner weekdays that someone eats, with who eats them."""
    days = []
    for weekday in WEEKDAYS:
        if (
            weekday in settings.dinner_days
            and (who := attendees_for(settings, weekday)) is not None
        ):
            days.append((weekday, who))
    return days


async def async_generate_menu(
    sources: list[RecipeSource],
    settings: PlannerSettings,
    week_start: date,
    recent_ids: set[str],
    keep: Sequence[MenuDay] = (),
    hint: str | None = None,
) -> Menu:
    """Build a draft menu for the week starting `week_start` (a Monday).

    Days in `keep` (the locked ones of an earlier draft) are carried over untouched."""
    menu = Menu(
        week_start=week_start.isoformat(),
        generated_at=dt_util.utcnow().isoformat(),
    )
    days = planned_days(settings)
    if not days:
        menu.warnings.append("no_days")
        return menu

    wanted = {weekday for weekday, _ in days}
    kept = [d for d in keep if d.weekday in wanted]
    targets = [(wd, who) for wd, who in days if wd not in {d.weekday for d in kept}]
    planned = (
        await _plan(sources, settings, targets, kept, recent_ids, menu.warnings, hint)
        if targets
        else {}
    )

    by_weekday = {d.weekday: d for d in kept}
    for weekday, result in planned.items():
        by_weekday[weekday] = MenuDay(
            date=(week_start + timedelta(days=WEEKDAYS.index(weekday))).isoformat(),
            weekday=weekday,
            recipe=result.recipe,
            candidates=result.candidates,
            split=result.split,
        )
    menu.days = [by_weekday[wd] for wd, _ in days]
    return menu


async def async_generate_day(
    sources: list[RecipeSource],
    settings: PlannerSettings,
    menu: Menu,
    weekday: str,
    recent_ids: set[str],
    hint: str | None = None,
) -> tuple[MenuDay | None, list[str]]:
    """A new dinner for one day of `menu`, planned around the rest of the week.

    Returns None when nothing better than "no recipe" was found; the caller keeps the old one."""
    current = next(d for d in menu.days if d.weekday == weekday)
    who = attendees_for(settings, weekday)
    if who is None:
        return None, ["no_days"]
    warnings: list[str] = []
    planned = await _plan(
        sources,
        settings,
        [(weekday, who)],
        [d for d in menu.days if d.weekday != weekday],
        recent_ids,
        warnings,
        hint,
        avoid_ids={c.id for c in current.candidates},
    )
    result = planned[weekday]
    if result.recipe is None:
        return None, warnings
    return (
        MenuDay(
            date=current.date,
            weekday=weekday,
            recipe=result.recipe,
            candidates=result.candidates,
            split=result.split,
        ),
        warnings,
    )


def week_start_of(day: date | datetime) -> date:
    """The Monday of the week containing `day`."""
    d = day.date() if isinstance(day, datetime) else day
    return d - timedelta(days=d.weekday())
