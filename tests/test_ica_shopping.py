"""ICA shopping: the login, the list API (all mocked), the provider and its setup."""

import base64
import hashlib
import re
from unittest.mock import AsyncMock, patch

import pytest
from aiohttp import ClientError
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.test_util.aiohttp import (
    AiohttpClientMocker,
    AiohttpClientMockResponse,
)

from custom_components.weeklymenu.shopping.base import PushResult
from custom_components.weeklymenu.shopping.ica import setup as ica_setup
from custom_components.weeklymenu.shopping.ica.auth import (
    IcaAuthError,
    IcaConnectionError,
    IcaGeoBlockedError,
    Tokens,
    async_login,
    normalize_personnummer,
)
from custom_components.weeklymenu.shopping.ica.provider import (
    IcaShoppingProvider,
    list_title,
)
from custom_components.weeklymenu.shopping.models import ShoppingItem

IMS = "https://ims.icagruppen.se"
LISTS = (
    "https://apimgw-pub.ica.se/sverige/digx/mobile/shoppinglistservice/v1/shoppinglists"
)
WEEK = "2026-11-02"  # ISO week 45

ITEMS = [
    ShoppingItem("nötfärs", 230, "g"),
    ShoppingItem("grädde", 1.5, "dl"),
    ShoppingItem("gul lök", 2, None),
    ShoppingItem("hackad persilja"),
]


class IcaSite:
    """The login conversation and the list API, as far as the integration uses them."""

    def __init__(self, aioclient_mock: AiohttpClientMocker) -> None:
        self.mock = aioclient_mock
        self.lists: dict[str, dict] = {}  # id -> {"title", "rows": [...]}
        self.posted_rows: list[dict] = []
        self.token_requests: list[dict] = []
        self.login_attempts: list[dict] = []
        self.accept_password = "hunter2"
        self.api_status: int | None = None  # make the list API fail
        self._install()

    def _install(self) -> None:
        mock = self.mock

        async def token(method, url, data):
            self.token_requests.append(dict(data))
            if data["grant_type"] == "client_credentials":
                return AiohttpClientMockResponse(
                    method, url, json={"access_token": "boot"}
                )
            return AiohttpClientMockResponse(
                method, url, json={"access_token": "ACCESS"}
            )

        async def authenticate(method, url, data):
            self.login_attempts.append(dict(data))
            ok = data["password"] == self.accept_password
            page = (
                '<form><input type="hidden" name="token" value="TOK"/></form>'
                if ok
                else "<p>Fel</p>"
            )
            return AiohttpClientMockResponse(method, url, text=page)

        mock.post(f"{IMS}/oauth/v2/token", side_effect=token)
        mock.post(
            f"{IMS}/register",
            json={
                "client_id": "cid",
                "client_secret": "csecret",
                "scope": "openid ica",
            },
        )
        mock.get(
            f"{IMS}/oauth/v2/authorize",
            status=302,
            headers={"Location": f"{IMS}/authn/page?state=STATE1"},
        )
        mock.get(f"{IMS}/authn/page", text="<html>login</html>")
        mock.post(f"{IMS}/authn/authenticate/IcaCustomers", side_effect=authenticate)
        mock.post(
            f"{IMS}/oauth/v2/authorize",
            status=302,
            headers={"Location": "icacurity://app?code=CODE1&state=STATE1"},
        )

        async def lists(method, url, data):
            if self.api_status:
                return AiohttpClientMockResponse(method, url, status=self.api_status)
            body = {
                "shoppingLists": [
                    {"offlineId": i, "title": v["title"]} for i, v in self.lists.items()
                ]
            }
            return AiohttpClientMockResponse(method, url, json=body)

        async def create(method, url, data):
            if self.api_status:
                return AiohttpClientMockResponse(method, url, status=self.api_status)
            self.lists[data["offlineId"]] = {"title": data["title"], "rows": []}
            return AiohttpClientMockResponse(method, url, json={})

        async def one(method, url, data):
            list_id = str(url).rsplit("/", 1)[-1]
            return AiohttpClientMockResponse(
                method, url, json={"rows": self.lists[list_id]["rows"]}
            )

        async def sync(method, url, data):
            list_id = str(url).split("/")[-2]
            self.lists[list_id]["rows"] += data["createdRows"]
            self.posted_rows += data["createdRows"]
            return AiohttpClientMockResponse(method, url, json={})

        mock.get(LISTS, side_effect=lists)
        mock.post(LISTS, side_effect=create)
        mock.get(re.compile(rf"^{re.escape(LISTS)}/[0-9A-F-]+$"), side_effect=one)
        mock.post(
            re.compile(rf"^{re.escape(LISTS)}/[0-9A-F-]+/sync$"), side_effect=sync
        )

    def provider(self, hass, **kwargs) -> IcaShoppingProvider:
        return IcaShoppingProvider(hass, "199001011234", self.accept_password, **kwargs)


@pytest.fixture
def ica(aioclient_mock: AiohttpClientMocker) -> IcaSite:
    return IcaSite(aioclient_mock)


# --- login --------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("typed", "expected"),
    [
        ("199001011234", "199001011234"),
        ("900101-1234", "199001011234"),
        ("9001011234", "199001011234"),
        ("1111111111", "201111111111"),
        (" 19900101 1234 ", "199001011234"),
    ],
)
def test_normalize_personnummer(typed, expected) -> None:
    assert normalize_personnummer(typed) == expected


async def test_login_follows_the_app_flow(hass: HomeAssistant, ica) -> None:
    tokens = await async_login(hass, "900101-1234", "hunter2")
    assert tokens == Tokens("ACCESS")
    assert ica.login_attempts == [{"userName": "199001011234", "password": "hunter2"}]

    final = ica.token_requests[-1]
    assert final["grant_type"] == "authorization_code" and final["code"] == "CODE1"
    assert final["client_id"] == "cid" and final["client_secret"] == "csecret"
    # PKCE: the challenge sent when authorising is the hash of the verifier sent now
    challenge = next(c for c in ica.mock.mock_calls if "code_challenge" in str(c[1]))
    sent = re.search(r"code_challenge=([^&]+)", str(challenge[1])).group(1)
    expected = base64.urlsafe_b64encode(
        hashlib.sha256(final["code_verifier"].encode()).digest()
    )
    assert sent == expected.decode().rstrip("=")


async def test_wrong_password_is_an_auth_error(hass: HomeAssistant, ica) -> None:
    with pytest.raises(IcaAuthError):
        await async_login(hass, "199001011234", "wrong")


async def test_outside_sweden_is_reported_as_geo_blocking(
    hass: HomeAssistant, aioclient_mock
) -> None:
    aioclient_mock.post(f"{IMS}/oauth/v2/token", status=451)
    with pytest.raises(IcaGeoBlockedError):
        await async_login(hass, "199001011234", "hunter2")


@pytest.mark.parametrize(
    "failure", [{"status": 503}, {"exc": ClientError("down")}, {"exc": TimeoutError()}]
)
async def test_a_dead_site_is_a_connection_error(
    hass: HomeAssistant, aioclient_mock, failure
) -> None:
    aioclient_mock.post(f"{IMS}/oauth/v2/token", **failure)
    with pytest.raises(IcaConnectionError):
        await async_login(hass, "199001011234", "hunter2")


# --- the provider ----------------------------------------------------------------------


@pytest.mark.parametrize(
    ("mode", "name", "language", "title"),
    [
        ("weekly", None, "sv", "Veckomeny vecka 45"),
        ("weekly", "ignored", "en", "Weekly menu week 45"),
        ("named", "Matlistan", "sv", "Matlistan"),
        ("named", "  ", "sv", "Veckomeny"),
        ("named", None, "en", "Weekly menu"),
    ],
)
def test_list_title(mode, name, language, title) -> None:
    assert list_title(mode, name, WEEK, language) == title


async def test_push_creates_the_week_list_and_writes_rows(
    hass: HomeAssistant, ica
) -> None:
    result = await ica.provider(hass).async_push(ITEMS, "sv", WEEK)
    assert result.added == ITEMS and result.failed == [] and result.errors == []
    [created] = ica.lists.values()
    assert created["title"] == "Veckomeny vecka 45"
    rows = {r["productName"]: (r["quantity"], r["unit"]) for r in created["rows"]}
    assert rows == {
        "nötfärs": (230, "g"),
        "grädde": (1.5, "dl"),
        "gul lök": (2, "st"),  # counted things are written as pieces
        "hackad persilja": (1.0, ""),  # no amount
    }
    first = created["rows"][0]
    assert (
        first["isStrikedOver"] is False
        and first["sourceId"] < 0
        and first["offlineId"].isupper()
    )


async def test_a_retry_finds_the_list_and_adds_nothing_twice(
    hass: HomeAssistant, ica
) -> None:
    await ica.provider(hass).async_push(ITEMS, "sv", WEEK)
    again = await ica.provider(hass).async_push(
        [*ITEMS, ShoppingItem("pasta", 400, "g")], "sv", WEEK
    )
    assert len(ica.lists) == 1  # the same list
    assert [r["productName"] for r in ica.posted_rows].count("nötfärs") == 1
    assert [r["productName"] for r in ica.posted_rows][-1] == "pasta"
    assert len(again.added) == 5 and again.failed == []  # present rows count as added


async def test_an_existing_list_is_found_by_title_ignoring_case(
    hass: HomeAssistant, ica
) -> None:
    ica.lists["ABC"] = {"title": "matlistan", "rows": []}
    await ica.provider(hass, mode="named", list_name="Matlistan").async_push(
        ITEMS[:1], "sv", WEEK
    )
    assert list(ica.lists) == ["ABC"] and len(ica.lists["ABC"]["rows"]) == 1


async def test_the_target_names_the_list(hass: HomeAssistant, ica) -> None:
    provider = ica.provider(hass)
    await provider.async_push(ITEMS[:1], "sv", WEEK)
    assert provider.targets == ["ICA: Veckomeny vecka 45"]


async def test_a_bad_login_asks_for_reauth(hass: HomeAssistant, ica) -> None:
    ica.accept_password = "changed"
    provider = IcaShoppingProvider(hass, "199001011234", "old")
    result = await provider.async_push(ITEMS, "sv", WEEK)
    assert (
        result.needs_reauth
        and result.failed == ITEMS
        and result.errors == ["auth_failed"]
    )
    assert ica.lists == {}


async def test_a_refused_token_asks_for_reauth_too(hass: HomeAssistant, ica) -> None:
    ica.api_status = 401
    result = await ica.provider(hass).async_push(ITEMS, "sv", WEEK)
    assert result.needs_reauth and result.errors == ["auth_failed"]


async def test_outside_sweden_nothing_is_lost(hass: HomeAssistant, ica) -> None:
    ica.api_status = 451
    result = await ica.provider(hass).async_push(ITEMS, "sv", WEEK)
    assert (
        result.errors == ["geo_blocked"]
        and result.failed == ITEMS
        and not result.needs_reauth
    )


async def test_a_server_error_leaves_the_items_for_a_retry(
    hass: HomeAssistant, ica
) -> None:
    ica.api_status = 500
    result = await ica.provider(hass).async_push(ITEMS, "sv", WEEK)
    assert (
        result.failed == ITEMS and "500" in result.errors[0] and not result.needs_reauth
    )


# --- account setup -----------------------------------------------------------------------


async def validate(hass, config=None, **form):
    return await ica_setup.SETUP.validate(hass, config or {}, form)


async def test_setup_saves_a_working_login(hass: HomeAssistant, ica) -> None:
    changes, errors = await validate(
        hass,
        ica_personnummer="900101-1234",
        ica_password="hunter2",
        ica_list_mode="named",
        ica_list_name=" Mat ",
    )
    assert errors == {}
    assert changes == {
        "ica_personnummer": "199001011234",
        "ica_password": "hunter2",
        "ica_list_mode": "named",
        "ica_list_name": "Mat",
    }


async def test_setup_keeps_the_saved_password_when_left_empty(
    hass: HomeAssistant, ica
) -> None:
    changes, errors = await validate(
        hass,
        {"ica_password": "hunter2"},
        ica_personnummer="199001011234",
        ica_list_mode="weekly",
    )
    assert errors == {} and changes["ica_password"] == "hunter2"


async def test_setup_explains_what_is_wrong(hass: HomeAssistant, ica) -> None:
    assert (await validate(hass, ica_personnummer="123", ica_password="x"))[1] == {
        "ica_personnummer": "invalid_personnummer"
    }
    assert (await validate(hass, ica_personnummer="199001011234"))[1] == {
        "ica_password": "password_required"
    }
    assert (await validate(hass, ica_personnummer="199001011234", ica_password="nope"))[
        1
    ] == {"base": "invalid_auth"}


@pytest.mark.parametrize(
    ("error", "code"),
    [
        (IcaGeoBlockedError("x"), "geo_blocked"),
        (IcaConnectionError("x"), "cannot_connect"),
    ],
)
async def test_setup_reports_network_problems(hass: HomeAssistant, error, code) -> None:
    with patch.object(ica_setup, "async_login", AsyncMock(side_effect=error)):
        _, errors = await validate(
            hass, ica_personnummer="199001011234", ica_password="x"
        )
    assert errors == {"base": code}


async def test_an_empty_personnummer_switches_ica_off(hass: HomeAssistant) -> None:
    changes, errors = await validate(hass, {"ica_password": "x"}, ica_personnummer="  ")
    assert errors == {} and changes == dict.fromkeys(ica_setup.KEYS)


def test_ica_is_a_registered_provider_with_its_own_setup(hass: HomeAssistant) -> None:
    from custom_components.weeklymenu.shopping.registry import (
        build_default_shopping_registry,
    )

    registry = build_default_shopping_registry()
    assert registry.ids == ["todo", "ica"] and list(registry.setups) == ["ica"]
    assert registry.create(hass, {}) == []
    [provider] = registry.create(hass, {"ica_personnummer": "1", "ica_password": "x"})
    assert isinstance(provider, IcaShoppingProvider) and provider.capabilities == {
        "list"
    }
    assert (
        len(
            registry.create(
                hass,
                {
                    "ica_personnummer": "1",
                    "ica_password": "x",
                    "shopping_targets": ["todo.a"],
                },
            )
        )
        == 2
    )


def test_push_result_defaults() -> None:
    assert PushResult().needs_reauth is False


# --- through the integration -------------------------------------------------------------------

from homeassistant.config_entries import SOURCE_REAUTH

from tests.helpers import call, generate, recipe, state

ICA_DATA = {
    "ica_personnummer": "199001011234",
    "ica_password": "hunter2",
    "ica_list_mode": "weekly",
}


@pytest.fixture
def ica_menu(hass: HomeAssistant, entry, fake, ica):
    """A one-dinner menu for two, with ICA configured as the only shopping target."""
    fake.recipes = [recipe("Pasta med sås", "400 g pasta", "2 dl grädde", "1 tsk salt")]
    fake.recipes[0].servings = 2
    members = [
        {"id": "1", "name": "Olle", "attends": ["mon"]},
        {"id": "2", "name": "Anna", "attends": ["mon"]},
    ]
    hass.config_entries.async_update_entry(
        entry,
        data={**entry.data, **ICA_DATA},
        options={**entry.options, "dinner_days": ["mon"], "members": members},
    )
    return entry


async def confirm(hass: HomeAssistant):
    await generate(hass)
    return await call(hass, "confirm_menu")


async def test_confirming_fills_the_ica_list(
    hass: HomeAssistant, ica_menu, ica
) -> None:
    await hass.async_block_till_done()
    await confirm(hass)
    [created] = ica.lists.values()
    assert created["title"] == "Veckomeny vecka 45"
    assert sorted(r["productName"] for r in created["rows"]) == [
        "grädde",
        "pasta",
    ]  # salt is a staple
    sensor = state(hass, ica_menu, "shopping")
    assert sensor.attributes["targets"] == ["ICA: Veckomeny vecka 45"]
    assert sensor.state == "2"


async def test_a_login_that_stops_working_starts_reauth_and_can_be_fixed(
    hass: HomeAssistant, ica_menu, ica
) -> None:
    sent = []

    async def notify(service_call) -> None:
        sent.append(service_call.data)

    hass.services.async_register("notify", "mobile_app_test", notify)
    hass.config_entries.async_update_entry(
        ica_menu, options={**ica_menu.options, "notify_targets": ["mobile_app_test"]}
    )
    await hass.async_block_till_done()
    ica.accept_password = "new-password"  # changed since it was saved

    await confirm(hass)
    await hass.async_block_till_done()

    # the menu is confirmed, the items wait, and the user is told
    assert state(hass, ica_menu, "status").state == "confirmed"
    assert state(hass, ica_menu, "shopping").attributes["counts"]["failed"] == 2
    confirmed = next(n for n in sent if n["title"] == "Menyn är bekräftad")
    assert "Inloggningen till ICA fungerar inte längre" in confirmed["message"]

    [flow] = [
        f
        for f in hass.config_entries.flow.async_progress()
        if f["context"]["source"] == SOURCE_REAUTH
    ]
    assert (
        flow["context"]["provider_id"] == "ica" and flow["step_id"] == "reauth_confirm"
    )

    # wrong password again: the form explains
    form = await hass.config_entries.flow.async_configure(
        flow["flow_id"],
        {"ica_personnummer": "199001011234", "ica_password": "still-wrong"},
    )
    assert form["type"] is FlowResultType.FORM and form["errors"] == {
        "base": "invalid_auth"
    }

    # the right one: the entry is updated and reloaded
    done = await hass.config_entries.flow.async_configure(
        flow["flow_id"],
        {"ica_personnummer": "199001011234", "ica_password": "new-password"},
    )
    await hass.async_block_till_done()
    assert (
        done["type"] is FlowResultType.ABORT and done["reason"] == "reauth_successful"
    )
    assert ica_menu.data["ica_password"] == "new-password"

    # and what waited can be delivered, once
    outcome = await call(hass, "add_to_shopping")
    assert outcome["counts"]["added"] == 2 and outcome["errors"] == []
    assert len(ica.posted_rows) == 2


async def test_geo_blocking_is_explained_in_the_notification(
    hass: HomeAssistant, ica_menu, ica
) -> None:
    sent = []

    async def notify(service_call) -> None:
        sent.append(service_call.data)

    hass.services.async_register("notify", "mobile_app_test", notify)
    hass.config_entries.async_update_entry(
        ica_menu, options={**ica_menu.options, "notify_targets": ["mobile_app_test"]}
    )
    await hass.async_block_till_done()
    ica.api_status = 451
    await confirm(hass)
    await hass.async_block_till_done()
    confirmed = next(n for n in sent if n["title"] == "Menyn är bekräftad")
    assert "ICA svarar bara på anslutningar från Sverige." in confirmed["message"]
    assert not [
        f
        for f in hass.config_entries.flow.async_progress()
        if f["context"]["source"] == SOURCE_REAUTH
    ]


# --- the options page -----------------------------------------------------------------------------


async def open_account_page(hass: HomeAssistant, entry):
    result = await hass.config_entries.options.async_init(entry.entry_id)
    assert "accounts" in result["menu_options"]
    # one provider with an account: the choice is skipped
    return await hass.config_entries.options.async_configure(
        result["flow_id"], {"next_step_id": "accounts"}
    )


async def test_account_page_saves_a_working_login(
    hass: HomeAssistant, entry, ica
) -> None:
    page = await open_account_page(hass, entry)
    assert page["step_id"] == "account"
    done = await hass.config_entries.options.async_configure(
        page["flow_id"],
        {
            "ica_personnummer": "900101-1234",
            "ica_password": "hunter2",
            "ica_list_mode": "weekly",
        },
    )
    assert done["type"] is FlowResultType.MENU
    assert (
        entry.data["ica_personnummer"] == "199001011234"
        and entry.data["ica_password"] == "hunter2"
    )


async def test_account_page_rejects_a_bad_login_and_saves_nothing(
    hass: HomeAssistant, entry, ica
) -> None:
    page = await open_account_page(hass, entry)
    bad = await hass.config_entries.options.async_configure(
        page["flow_id"],
        {
            "ica_personnummer": "199001011234",
            "ica_password": "nope",
            "ica_list_mode": "weekly",
        },
    )
    assert bad["type"] is FlowResultType.FORM and bad["errors"] == {
        "base": "invalid_auth"
    }
    assert "ica_password" not in entry.data


async def test_account_page_leaves_the_password_empty_and_keeps_it(
    hass: HomeAssistant, entry, ica
) -> None:
    hass.config_entries.async_update_entry(entry, data={**entry.data, **ICA_DATA})
    page = await open_account_page(hass, entry)
    schema_keys = {str(k) for k in page["data_schema"].schema}
    assert "ica_password" in schema_keys
    done = await hass.config_entries.options.async_configure(
        page["flow_id"],
        {
            "ica_personnummer": "199001011234",
            "ica_list_mode": "named",
            "ica_list_name": "Mat",
        },
    )
    assert done["type"] is FlowResultType.MENU
    assert (
        entry.data["ica_password"] == "hunter2" and entry.data["ica_list_name"] == "Mat"
    )


async def test_account_page_switches_ica_off(hass: HomeAssistant, entry, ica) -> None:
    hass.config_entries.async_update_entry(entry, data={**entry.data, **ICA_DATA})
    page = await open_account_page(hass, entry)
    await hass.config_entries.options.async_configure(
        page["flow_id"], {"ica_personnummer": "", "ica_list_mode": "weekly"}
    )
    assert not any(key.startswith("ica_") for key in entry.data)
    assert entry.data["language"] == "sv"  # the rest is untouched
