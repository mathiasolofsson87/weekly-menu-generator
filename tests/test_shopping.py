"""Confirming a menu builds the shopping lists and delivers them."""

import pytest
from homeassistant.components.todo import TodoListEntityFeature
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.exceptions import HomeAssistantError, ServiceValidationError
from pytest_homeassistant_custom_component.common import async_capture_events

from custom_components.weeklymenu.const import DOMAIN, EVENT_CONFIRMED
from custom_components.weeklymenu.shopping.base import PushResult, ShoppingProvider
from custom_components.weeklymenu.shopping.delivery import async_deliver
from custom_components.weeklymenu.shopping.models import (
    ADDED,
    FAILED,
    PENDING,
    REVIEW,
    ShoppingItem,
    ShoppingResult,
)
from tests.helpers import call, generate, recipe, state

GROCERIES = "todo.groceries"
REVIEW_LIST = "todo.review"
DESCRIPTION = (
    TodoListEntityFeature.CREATE_TODO_ITEM
    | TodoListEntityFeature.SET_DESCRIPTION_ON_ITEM
)


class Lists:
    """A stand-in for todo.add_item that records what it is given."""

    def __init__(self, hass: HomeAssistant) -> None:
        self.calls: list[dict] = []
        self.broken: set[str] = set()
        hass.services.async_register("todo", "add_item", self._add)

    async def _add(self, service_call: ServiceCall) -> None:
        data = dict(service_call.data)
        if data["entity_id"] in self.broken:
            raise HomeAssistantError(f"{data['entity_id']} is unavailable")
        self.calls.append(data)

    def items(self, entity_id: str = GROCERIES) -> list[str]:
        return [c["item"] for c in self.calls if c["entity_id"] == entity_id]


@pytest.fixture
def lists(hass: HomeAssistant) -> Lists:
    for entity_id in (GROCERIES, REVIEW_LIST):
        hass.states.async_set(entity_id, "0", {"supported_features": int(DESCRIPTION)})
    return Lists(hass)


@pytest.fixture
def shop(hass: HomeAssistant, entry, fake, lists: Lists):
    """A family of two with a menu of one known recipe, and shopping to the groceries list."""
    fake.recipes = [
        recipe(
            "Pasta med sås",
            "400 g pasta",
            "1 tsk salt",
            "2 dl grädde",
            "350 g nötfärs gärna 12%",
        )
    ]
    fake.recipes[0].servings = 2
    members = [
        {"id": "1", "name": "Olle", "attends": ["mon"]},
        {"id": "2", "name": "Anna", "attends": ["mon"]},
    ]
    hass.config_entries.async_update_entry(
        entry,
        options={
            **entry.options,
            "dinner_days": ["mon"],
            "members": members,
            "shopping_targets": [GROCERIES],
        },
    )
    return entry


async def confirm(hass: HomeAssistant, week="2026-11-02"):
    await generate(hass, week=week)
    return await call(hass, "confirm_menu", week_start=week)


async def test_confirming_puts_the_ingredients_on_the_list(hass, shop, lists) -> None:
    await hass.async_block_till_done()
    result = await confirm(hass)
    assert sorted(lists.items()) == [
        "2 dl grädde",
        "350 g nötfärs",
        "400 g pasta",
    ]  # salt is a staple
    assert result["status"] == "confirmed"


async def test_items_carry_their_recipe_and_original_wording(hass, shop, lists) -> None:
    await hass.async_block_till_done()
    await confirm(hass)
    by_item = {c["item"]: c.get("description", "") for c in lists.calls}
    assert by_item["350 g nötfärs"] == "Pasta med sås\nnötfärs gärna 12%"
    assert by_item["400 g pasta"] == "Pasta med sås"


async def test_lists_without_description_support_still_work(hass, shop, lists) -> None:
    hass.states.async_set(
        GROCERIES,
        "0",
        {"supported_features": int(TodoListEntityFeature.CREATE_TODO_ITEM)},
    )
    await hass.async_block_till_done()
    await confirm(hass)
    assert lists.calls and all("description" not in c for c in lists.calls)


async def test_the_result_is_kept_and_shown(hass, shop, lists, entry) -> None:
    await hass.async_block_till_done()
    done = async_capture_events(hass, EVENT_CONFIRMED)
    await confirm(hass)
    await hass.async_block_till_done()

    sensor = state(hass, entry, "shopping")
    assert sensor.state == "3"
    assert sensor.attributes["added"] == ["2 dl grädde", "350 g nötfärs", "400 g pasta"]
    assert (
        sensor.attributes["skipped"] == ["salt"] and sensor.attributes["errors"] == []
    )
    assert sensor.attributes["targets"] == [GROCERIES]
    assert done[0].data["shopping"] == {
        "added": 3,
        "review": 0,
        "failed": 0,
        "skipped": 1,
        "pending": 0,
    }

    await hass.config_entries.async_reload(entry.entry_id)  # stored with the menu
    await hass.async_block_till_done()
    assert state(hass, entry, "shopping").state == "3"


async def test_the_confirmed_notification_reports_the_shopping(
    hass, shop, lists, entry
) -> None:
    sent = []

    async def notify(service_call) -> None:
        sent.append(service_call.data)

    hass.services.async_register("notify", "mobile_app_test", notify)
    hass.config_entries.async_update_entry(
        entry, options={**entry.options, "notify_targets": ["mobile_app_test"]}
    )
    await hass.async_block_till_done()
    await confirm(hass)
    await hass.async_block_till_done()
    confirmed = next(n for n in sent if n["title"] == "Menyn är bekräftad")
    assert "3 varor lades på inköpslistan." in confirmed["message"]
    assert "1 skafferivaror hoppades över." in confirmed["message"]


async def test_without_a_list_the_menu_is_still_confirmed_and_items_wait(
    hass, shop, lists, entry
) -> None:
    hass.config_entries.async_update_entry(
        entry, options={**entry.options, "shopping_targets": []}
    )
    await hass.async_block_till_done()
    await confirm(hass)
    sensor = state(hass, entry, "shopping")
    assert sensor.attributes["counts"]["pending"] == 3 and sensor.attributes[
        "errors"
    ] == ["no_targets"]
    assert lists.calls == [] and state(hass, entry, "status").state == "confirmed"

    # Once a list is set up, add_to_shopping delivers what waited.
    hass.config_entries.async_update_entry(
        entry, options={**entry.options, "shopping_targets": [GROCERIES]}
    )
    await hass.async_block_till_done()
    outcome = await call(hass, "add_to_shopping")
    assert outcome["counts"]["added"] == 3 and len(lists.calls) == 3


async def test_a_broken_list_keeps_the_items_for_a_retry(
    hass, shop, lists, entry
) -> None:
    lists.broken.add(GROCERIES)
    await hass.async_block_till_done()
    await confirm(hass)
    sensor = state(hass, entry, "shopping")
    assert sensor.state == "0" and sensor.attributes["counts"]["failed"] == 3
    assert "unavailable" in sensor.attributes["errors"][0]
    assert (
        state(hass, entry, "status").state == "confirmed"
    )  # shopping trouble does not undo it

    lists.broken.clear()
    outcome = await call(hass, "add_to_shopping")
    assert outcome["counts"]["added"] == 3 and outcome["errors"] == []
    again = await call(
        hass, "add_to_shopping"
    )  # nothing left to retry, nothing is duplicated
    assert again["counts"]["added"] == 3 and len(lists.calls) == 3


async def test_one_working_list_is_enough(hass, shop, lists, entry) -> None:
    hass.config_entries.async_update_entry(
        entry, options={**entry.options, "shopping_targets": [GROCERIES, "todo.other"]}
    )
    hass.states.async_set("todo.other", "0", {"supported_features": 1})
    lists.broken.add("todo.other")
    await hass.async_block_till_done()
    await confirm(hass)
    sensor = state(hass, entry, "shopping")
    assert (
        sensor.attributes["counts"]["added"] == 3
        and len(sensor.attributes["errors"]) == 1
    )


async def test_add_everything_again_resends_the_whole_list(hass, shop, lists) -> None:
    await hass.async_block_till_done()
    await confirm(hass)
    await call(hass, "add_to_shopping", everything=True)
    assert len(lists.calls) == 6


async def test_add_to_shopping_needs_a_confirmed_menu(hass, shop, lists) -> None:
    await hass.async_block_till_done()
    await generate(hass)  # a draft only
    with pytest.raises(ServiceValidationError, match="confirmed menu"):
        await call(hass, "add_to_shopping")


async def test_split_dinners_are_bought_for_each_version(
    hass, shop, lists, entry, fake
) -> None:
    fake.recipes = [recipe("Biff", "600 g entrecote", "800 g potatis")]
    fake.recipes[0].servings = 2
    members = [
        {"id": "1", "name": "Olle", "attends": ["mon"]},
        {"id": "2", "name": "Anna", "diet": "vegetarian", "attends": ["mon"]},
    ]
    hass.config_entries.async_update_entry(
        entry, options={**entry.options, "members": members, "max_split_days": 2}
    )
    await hass.async_block_till_done()
    await confirm(hass)
    assert sorted(lists.items()) == ["300 g entrecote", "300 g tofu", "800 g potatis"]


# --- a second provider, and the review list ------------------------------------------------


class FussyProvider(ShoppingProvider):
    """Takes everything except items it 'cannot find', like a store with product matching."""

    id = "fussy"
    capabilities = frozenset({"product_matching"})

    def __init__(self, unmatched_names: set[str]) -> None:
        self._unmatched = unmatched_names
        self.pushed: list[str] = []

    @property
    def targets(self) -> list[str]:
        return ["fussy-store"]

    async def async_push(self, items, language) -> PushResult:
        result = PushResult()
        for item in items:
            if item.name in self._unmatched:
                result.unmatched.append(item)
            else:
                self.pushed.append(item.text(language))
                result.added.append(item)
        return result


def register_fussy(hass: HomeAssistant, provider: FussyProvider) -> None:
    hass.data[DOMAIN]["shopping_registry"].register(
        "fussy", lambda hass, config: provider
    )


async def test_unmatched_items_go_to_the_review_list(hass, shop, lists, entry) -> None:
    provider = FussyProvider({"pasta"})
    register_fussy(hass, provider)
    hass.config_entries.async_update_entry(
        entry,
        options={**entry.options, "shopping_targets": [], "review_list": REVIEW_LIST},
    )
    await hass.async_block_till_done()
    await confirm(hass)
    assert lists.items(REVIEW_LIST) == ["400 g pasta"]
    sensor = state(hass, entry, "shopping")
    assert sensor.attributes["review"] == ["400 g pasta"]
    assert sensor.attributes["counts"]["added"] == 2 and sensor.attributes[
        "targets"
    ] == ["fussy-store"]


async def test_unmatched_without_a_review_list_is_reported_not_lost(
    hass, shop, lists, entry
) -> None:
    register_fussy(hass, FussyProvider({"pasta"}))
    hass.config_entries.async_update_entry(
        entry, options={**entry.options, "shopping_targets": []}
    )
    await hass.async_block_till_done()
    await confirm(hass)
    sensor = state(hass, entry, "shopping")
    assert (
        sensor.attributes["failed"] == ["400 g pasta"]
        and "no_review_list" in sensor.attributes["errors"]
    )


async def test_providers_can_be_combined(hass, shop, lists, entry) -> None:
    provider = FussyProvider(set())
    register_fussy(hass, provider)
    await hass.async_block_till_done()
    await confirm(hass)
    assert len(lists.calls) == 3 and len(provider.pushed) == 3
    assert state(hass, entry, "shopping").attributes["targets"] == [
        GROCERIES,
        "fussy-store",
    ]


async def test_every_item_ends_up_in_exactly_one_state(
    hass: HomeAssistant, lists
) -> None:
    """The delivery contract: nothing is dropped, nothing counted twice."""
    items = [ShoppingItem(n) for n in ("a", "b", "c", "d")]
    result = ShoppingResult(items=items)
    provider = FussyProvider({"b", "c"})
    lists.broken.add(REVIEW_LIST)  # the review list is down too, so "c"... and "b" fail
    await async_deliver(hass, [provider], REVIEW_LIST, items, result)
    assert [i.status for i in items] == [ADDED, FAILED, FAILED, ADDED]
    assert sum(result.counts.values()) == 4

    lists.broken.clear()
    retry = [i for i in items if i.status == FAILED]
    await async_deliver(hass, [provider], REVIEW_LIST, retry, result)
    assert [i.status for i in items] == [ADDED, REVIEW, REVIEW, ADDED]
    assert PENDING not in {i.status for i in items}


# --- options ------------------------------------------------------------------------------------


async def test_shopping_options(hass: HomeAssistant, entry) -> None:
    result = await hass.config_entries.options.async_init(entry.entry_id)
    result = await hass.config_entries.options.async_configure(
        result["flow_id"], {"next_step_id": "shopping"}
    )
    assert result["step_id"] == "shopping"
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        {
            "shopping_targets": [GROCERIES],
            "review_list": REVIEW_LIST,
            "pantry_staples": ["Salt", " salt ", "Kryddmix"],
        },
    )
    assert result["type"] is FlowResultType.MENU
    assert entry.options["shopping_targets"] == [GROCERIES]
    assert entry.options["review_list"] == REVIEW_LIST
    assert entry.options["pantry_staples"] == ["salt", "kryddmix"]


async def test_saving_general_settings_keeps_the_shopping_lists(
    hass: HomeAssistant, entry
) -> None:
    hass.config_entries.async_update_entry(
        entry, options={**entry.options, "shopping_targets": [GROCERIES]}
    )
    result = await hass.config_entries.options.async_init(entry.entry_id)
    result = await hass.config_entries.options.async_configure(
        result["flow_id"], {"next_step_id": "general"}
    )
    await hass.config_entries.options.async_configure(
        result["flow_id"], {"language": "en", "units": "metric"}
    )
    assert entry.options["shopping_targets"] == [GROCERIES]


async def test_an_empty_pantry_list_means_no_staples(hass, shop, lists, entry) -> None:
    hass.config_entries.async_update_entry(
        entry, options={**entry.options, "pantry_staples": []}
    )
    await hass.async_block_till_done()
    await confirm(hass)
    assert "1 tsk salt" in lists.items()
