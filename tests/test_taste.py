"""Ratings and favorites per family member, and how the planner uses them."""

import random
from datetime import date

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ServiceValidationError

from custom_components.weeklymenu.planner.generator import (
    PlannerSettings,
    async_generate_day,
    async_generate_menu,
)
from custom_components.weeklymenu.planner.taste import Taste
from custom_components.weeklymenu.sources.base import CandidateRequest
from custom_components.weeklymenu.sources.favorites import FavoritesSource
from custom_components.weeklymenu.taste import TasteStore
from tests.helpers import FakeSource, call, generate, member, recipe, state

MONDAY = date(2026, 11, 2)


class _NoJitter(random.Random):
    def random(self) -> float:
        return 0.0


def _settings(taste: Taste, members, **kwargs) -> PlannerSettings:
    kwargs.setdefault("dinner_days", ["mon"])
    return PlannerSettings(members=members, taste=taste, rng=_NoJitter(), **kwargs)


# --- how a day's score is made -------------------------------------------------------


def test_unrated_recipes_are_neutral() -> None:
    assert Taste().score("r", [member("A"), member("B")]) == 0


def test_stars_above_and_below_three_move_the_score() -> None:
    a = member("A", id="a")
    assert Taste(ratings={"r": {"a": 5}}).score("r", [a]) == pytest.approx(3.0)
    assert Taste(ratings={"r": {"a": 3}}).score("r", [a]) == 0
    assert Taste(ratings={"r": {"a": 4}}).score("r", [a]) == pytest.approx(1.5)


def test_a_dislike_weighs_more_than_a_like_of_the_same_size() -> None:
    a = member("A", id="a")
    like = Taste(ratings={"r": {"a": 4}}).score("r", [a])
    dislike = Taste(ratings={"r": {"a": 2}}).score("r", [a])
    assert dislike == pytest.approx(-1.5 * like)


def test_only_the_people_eating_that_day_count() -> None:
    a, b = member("A", id="a"), member("B", id="b")
    taste = Taste(ratings={"r": {"a": 5, "b": 1}})
    assert taste.score("r", [a]) > 0 > taste.score("r", [b])


def test_a_childs_rating_counts_half() -> None:
    adult, child = member("A", id="a"), member("K", id="k", child=True)
    both = Taste(ratings={"r": {"a": 4, "k": 2}})  # +1 and -1, the dislike is 1.5x
    # (1 * 1 + 0.5 * -1.5) / 1.5 = 0.1667, times the 1.5 scale
    assert both.score("r", [adult, child]) == pytest.approx(0.25)
    # as two adults: (1 - 1.5) / 2 = -0.25, times 1.5
    assert both.score("r", [adult, member("K", id="k")]) == pytest.approx(-0.375)


def test_favorites_add_by_share_of_the_table() -> None:
    a, b = member("A", id="a"), member("B", id="b")
    one = Taste(favorites={"r": {"a"}}).score("r", [a, b])
    everyone = Taste(favorites={"r": {"a", "b"}}).score("r", [a, b])
    assert 0 < one < everyone
    assert everyone == pytest.approx(1.5)
    assert Taste(favorites={"r": {"a"}}).score("r", [b]) == 0  # not eating


def test_the_lowest_rating_from_someone_eating_is_a_veto() -> None:
    a, b = member("A", id="a"), member("B", id="b")
    taste = Taste(ratings={"r": {"a": 1, "b": 5}})
    assert taste.vetoed("r", [a, b]) and taste.vetoed("r", [a])
    assert not taste.vetoed("r", [b])  # A is not at the table
    assert not Taste(ratings={"r": {"a": 2}}).vetoed("r", [a])


# --- the planner ---------------------------------------------------------------------


async def test_a_well_rated_recipe_beats_an_unrated_one() -> None:
    a = member("A", id="a")
    pool = [recipe(f"Rätt {n}", "1 st lök") for n in range(6)]
    taste = Taste(ratings={pool[4].id: {"a": 5}})
    menu = await async_generate_menu(
        [FakeSource(pool)], _settings(taste, [a]), MONDAY, set()
    )
    assert menu.days[0].recipe.id == pool[4].id


async def test_a_favorite_beats_an_unrated_one() -> None:
    a = member("A", id="a")
    pool = [recipe(f"Rätt {n}", "1 st lök") for n in range(6)]
    taste = Taste(favorites={pool[5].id: {"a"}})
    menu = await async_generate_menu(
        [FakeSource(pool)], _settings(taste, [a]), MONDAY, set()
    )
    assert menu.days[0].recipe.id == pool[5].id


async def test_a_one_star_recipe_is_left_out_when_something_else_fits() -> None:
    a = member("A", id="a")
    hated = recipe("Aaa först", "1 st lök")  # first by title, so it would win a tie
    pool = [hated, recipe("Bbb", "1 st lök"), recipe("Ccc", "1 st lök")]
    taste = Taste(ratings={hated.id: {"a": 1}})
    menu = await async_generate_menu(
        [FakeSource(pool)], _settings(taste, [a]), MONDAY, set()
    )
    assert menu.days[0].recipe.title != "Aaa först"


async def test_a_one_star_recipe_is_used_when_nothing_else_fits() -> None:
    a = member("A", id="a")
    only = recipe("Enda", "1 st lök")
    menu = await async_generate_menu(
        [FakeSource([only])],
        _settings(Taste(ratings={only.id: {"a": 1}}), [a]),
        MONDAY,
        set(),
    )
    assert menu.days[0].recipe.id == only.id


async def test_a_one_star_from_someone_away_does_not_matter() -> None:
    a = member("A", id="a", attends=["tue"])
    b = member("B", id="b")  # eats on Monday
    disliked = recipe("Aaa", "1 st lök")
    pool = [disliked, recipe("Bbb", "1 st lök")]
    menu = await async_generate_menu(
        [FakeSource(pool)],
        _settings(Taste(ratings={disliked.id: {"a": 1}}), [a, b]),
        MONDAY,
        set(),
    )
    assert menu.days[0].recipe.id == disliked.id  # title wins the tie


async def test_new_dinner_uses_the_ratings_too() -> None:
    a = member("A", id="a")
    pool = [recipe(f"Rätt {n}", "1 st lök") for n in range(8)]
    settings = _settings(Taste(), [a])
    source = FakeSource(pool)
    menu = await async_generate_menu([source], settings, MONDAY, set())
    settings.taste = Taste(ratings={pool[7].id: {"a": 5}})
    new, _ = await async_generate_day([source], settings, menu, "mon", set())
    assert new.recipe.id == pool[7].id


async def test_favorites_are_spread_over_the_people_at_the_table() -> None:
    a, b = member("A", id="a"), member("B", id="b")
    a1, a2 = recipe("Aaa1", "1 st lök"), recipe("Aaa2", "1 st lök")
    b1 = recipe("Bbb", "1 st lök")
    taste = Taste(favorites={a1.id: {"a"}, a2.id: {"a"}, b1.id: {"b"}})
    menu = await async_generate_menu(
        [FakeSource([a1, a2, b1])],
        _settings(taste, [a, b], dinner_days=["mon", "tue"]),
        MONDAY,
        set(),
    )
    assert {d.recipe.id for d in menu.days} == {a1.id, b1.id}


def test_a_favorite_new_to_the_week_scores_more() -> None:
    a = member("A", id="a")
    taste = Taste(favorites={"r": {"a"}})
    assert taste.score("r", [a], served=set()) > taste.score("r", [a], served={"a"})


async def test_the_week_keeps_room_for_a_new_dinner() -> None:
    a = member("A", id="a")
    liked = [recipe(f"Kand {n}", "1 st lök") for n in range(3)]
    fresh = recipe("Ny", "1 st lök")
    taste = Taste(ratings={r.id: {"a": 5} for r in liked})
    days = ["mon", "tue", "wed"]
    menu = await async_generate_menu(
        [FakeSource([*liked, fresh])],
        _settings(taste, [a], dinner_days=days, explore_days=1),
        MONDAY,
        set(),
    )
    assert fresh.id in {d.recipe.id for d in menu.days}
    menu = await async_generate_menu(
        [FakeSource([*liked, fresh])],
        _settings(taste, [a], dinner_days=days, explore_days=0),
        MONDAY,
        set(),
    )
    assert fresh.id not in {d.recipe.id for d in menu.days}


async def test_a_new_dinner_that_is_rated_low_is_still_known() -> None:
    a = member("A", id="a")
    low = recipe("Aaa", "1 st lök")
    other = recipe("Bbb", "1 st lök")
    taste = Taste(ratings={low.id: {"a": 2}, other.id: {"a": 4}})
    assert taste.known(low.id) and taste.known(other.id) and not taste.known("x")
    menu = await async_generate_menu(
        [FakeSource([low, other])],
        _settings(taste, [a], explore_days=1),
        MONDAY,
        set(),
    )  # nothing is new, so the quota cannot be met and the best-rated one wins
    assert menu.days[0].recipe.id == other.id


# --- the store and the favorites source ------------------------------------------------


async def test_store_keeps_recipes_only_while_somebody_refers_to_them(
    hass: HomeAssistant,
) -> None:
    store = TasteStore(hass, "e1")
    r = recipe("Gryta", "400 g nötfärs")
    store.set_favorite("a", r, True)
    store.set_rating("b", r, 4)
    await store.async_save()
    assert store.favorite_of(r.id) == ["a"] and store.ratings_of(r.id) == {"b": 4}

    store.set_favorite("a", r, False)
    await store.async_save()
    assert r.id in store.recipes  # b still has a rating
    store.set_rating("b", r, None)
    await store.async_save()
    assert store.recipes == {} and store.ratings == {} and store.favorites == {}


async def test_store_lets_go_of_recipes_that_are_only_rated_low(
    hass: HomeAssistant,
) -> None:
    store = TasteStore(hass, "e1")
    r = recipe("Gryta", "400 g nötfärs")
    store.set_rating("a", r, 2)
    store.set_rating("b", r, 1)
    await store.async_save()
    assert store.recipes == {} and store.ratings_of(r.id) == {"a": 2, "b": 1}
    assert store.snapshot().vetoed(r.id, [member("B", id="b")])

    store.set_rating("b", r, 4)  # someone likes it: the copy is kept again
    await store.async_save()
    assert r.id in store.recipes
    store.set_rating("b", r, 2)
    store.set_favorite("a", r, True)  # a favorite is always kept
    await store.async_save()
    assert r.id in store.recipes


async def test_store_survives_a_restart(hass: HomeAssistant) -> None:
    store = TasteStore(hass, "e2")
    r = recipe("Gryta", "400 g nötfärs")
    store.set_favorite("a", r, True)
    store.set_rating("a", r, 5)
    await store.async_save()
    again = TasteStore(hass, "e2")
    await again.async_load()
    assert again.favorites_of("a")[0].title == "Gryta"
    assert again.rating("a", r.id) == 5


async def test_removed_members_take_their_taste_with_them(hass: HomeAssistant) -> None:
    store = TasteStore(hass, "e3")
    r = recipe("Gryta", "400 g nötfärs")
    store.set_favorite("gone", r, True)
    store.set_rating("gone", r, 5)
    store.set_rating("kept", r, 4)
    assert store.prune(["kept"]) is True
    await store.async_save()
    assert store.ratings_of(r.id) == {"kept": 4} and store.favorite_of(r.id) == []
    assert store.prune(["kept"]) is False


async def test_favorites_source_offers_liked_recipes_only(hass: HomeAssistant) -> None:
    store = TasteStore(hass, "e4")
    loved, good, meh = (recipe(n, "1 st lök") for n in ("Loved", "Good", "Meh"))
    store.set_favorite("a", loved, True)
    store.set_rating("a", good, 4)
    store.set_rating("a", meh, 3)
    got = await FavoritesSource(store).async_candidates(CandidateRequest(count=12))
    assert {r.title for r in got} == {"Loved", "Good"}


async def test_favorites_source_keeps_to_a_third_and_honours_excludes(
    hass: HomeAssistant,
) -> None:
    store = TasteStore(hass, "e5")
    recipes = [recipe(f"F{n}", "1 st lök") for n in range(9)]
    for r in recipes:
        store.set_favorite("a", r, True)
    source = FavoritesSource(store)
    assert len(await source.async_candidates(CandidateRequest(count=6))) == 2
    got = await source.async_candidates(
        CandidateRequest(
            count=30, exclude_ids={recipes[0].id}, accept=lambda r: r.title != "F1"
        )
    )
    assert {r.title for r in got}.isdisjoint({"F0", "F1"})


async def test_favorites_do_not_replace_the_real_sources() -> None:
    """A favorite is offered next to what the source returns, which is still asked."""
    a = member("A", id="a")
    fav = recipe("Favoriten", "1 st lök")
    source = FakeSource([recipe(f"Ny {n}", "1 st lök") for n in range(6)])
    store_taste = Taste(favorites={fav.id: {"a"}})

    class Favs(FavoritesSource):
        def __init__(self) -> None:  # no store needed for this check
            pass

        async def async_candidates(self, request):
            return [fav]

    menu = await async_generate_menu(
        [Favs(), source], _settings(store_taste, [a]), MONDAY, set()
    )
    assert source.requests  # still asked although the favorite alone was enough
    assert menu.days[0].recipe.id == fav.id


# --- services, sensors and the cool-down -----------------------------------------------


async def _first_recipe_id(hass, entry) -> str:
    await generate(hass)
    return entry.runtime_data.coordinator.latest.days[0].recipe.id


async def test_rate_and_favorite_through_services(hass: HomeAssistant, entry) -> None:
    recipe_id = await _first_recipe_id(hass, entry)
    await call(hass, "rate_recipe", member="anna", recipe_id=recipe_id, rating=4)
    await call(hass, "favorite_recipe", member="1", recipe_id=recipe_id)

    monday = state(hass, entry, "weekday_mon")
    assert monday.attributes["ratings"] == {"1": 4}
    assert monday.attributes["favorite_of"] == ["1"]
    [favorite] = state(hass, entry, "family").attributes["members"][0]["favorites"]
    assert favorite["id"] == recipe_id and favorite["rating"] == 4

    await call(hass, "rate_recipe", member="1", recipe_id=recipe_id, rating=0)
    await call(hass, "favorite_recipe", member="1", recipe_id=recipe_id, favorite=False)
    monday = state(hass, entry, "weekday_mon")
    assert monday.attributes["ratings"] == {} and monday.attributes["favorite_of"] == []
    assert state(hass, entry, "family").attributes["members"][0]["favorites"] == []


async def test_a_favorite_can_be_removed_after_the_menu_is_gone(
    hass: HomeAssistant, entry
) -> None:
    recipe_id = await _first_recipe_id(hass, entry)
    await call(hass, "favorite_recipe", member="1", recipe_id=recipe_id)
    coordinator = entry.runtime_data.coordinator
    coordinator.store.menus.clear()  # the menu has aged out of the history
    await call(hass, "favorite_recipe", member="1", recipe_id=recipe_id, favorite=False)
    assert coordinator.taste.favorites_of("1") == []


async def test_rating_checks_member_recipe_and_range(
    hass: HomeAssistant, entry
) -> None:
    recipe_id = await _first_recipe_id(hass, entry)
    with pytest.raises(ServiceValidationError):
        await call(hass, "rate_recipe", member="Nobody", recipe_id=recipe_id, rating=3)
    with pytest.raises(ServiceValidationError):
        await call(hass, "rate_recipe", member="1", recipe_id="nope", rating=3)
    with pytest.raises(Exception, match="rating"):
        await call(hass, "rate_recipe", member="1", recipe_id=recipe_id, rating=6)


async def test_ratings_survive_a_restart(hass: HomeAssistant, entry) -> None:
    recipe_id = await _first_recipe_id(hass, entry)
    await call(hass, "rate_recipe", member="1", recipe_id=recipe_id, rating=5)
    await call(hass, "favorite_recipe", member="1", recipe_id=recipe_id)
    await hass.config_entries.async_reload(entry.entry_id)
    await hass.async_block_till_done()
    assert state(hass, entry, "weekday_mon").attributes["ratings"] == {"1": 5}
    assert entry.runtime_data.coordinator.taste.favorites_of("1")


async def test_removing_a_member_removes_their_taste(
    hass: HomeAssistant, entry
) -> None:
    recipe_id = await _first_recipe_id(hass, entry)
    await call(hass, "rate_recipe", member="1", recipe_id=recipe_id, rating=5)
    await call(hass, "set_member", name="Olle")
    await call(hass, "remove_member", id="1")
    await hass.async_block_till_done()
    assert entry.runtime_data.coordinator.taste.ratings == {}


async def test_child_flag_is_stored(hass: HomeAssistant, entry) -> None:
    await call(hass, "set_member", name="Kim", child=True)
    await hass.async_block_till_done()
    members = {m["name"]: m for m in entry.options["members"]}
    assert members["Kim"]["child"] is True
    assert not members["Anna"].get("child", False)  # an older member is an adult


async def test_a_favorite_is_kept_out_of_the_next_week_only(
    hass: HomeAssistant, entry, fake
) -> None:
    from custom_components.weeklymenu.const import CONF_FAVORITE_GAP_WEEKS

    coordinator = entry.runtime_data.coordinator
    await generate(hass, "2026-10-19")
    old = coordinator.store.menus["2026-10-19"].days[0].recipe
    await generate(hass, "2026-10-26")
    await call(hass, "favorite_recipe", member="1", recipe_id=old.id)

    # next to where it was cooked: kept out; two weeks later: allowed again
    assert old.id in coordinator._recent_ids("2026-10-26")
    assert old.id not in coordinator._recent_ids("2026-11-09")
    # a recipe nobody favorited stays out for the whole history, as before
    other = coordinator.store.menus["2026-10-26"].days[0].recipe
    assert other.id in coordinator._recent_ids("2026-11-09")

    hass.config_entries.async_update_entry(
        entry, options={**entry.options, CONF_FAVORITE_GAP_WEEKS: 3}
    )
    await hass.async_block_till_done()
    coordinator = entry.runtime_data.coordinator
    assert old.id in coordinator._recent_ids("2026-11-09")
