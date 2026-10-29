"""Login to ICA with personnummer and password (OAuth2 + PKCE), as the ICA app does.

The flow is the one proven by `spikes/ica_spike.py`, ported from the open-source
LazyTarget/ha-ica-todo and kanylbullen/ica-mcp (both MIT). It needs a session with
its own cookie jar, so it never uses Home Assistant's shared one. Nothing is kept
between uses: tokens last about 15 minutes and this integration shops once a week,
so it simply logs in each time.
"""

from __future__ import annotations

import base64
import datetime as dt
import hashlib
import json
import os
import re
from dataclasses import dataclass
from urllib.parse import parse_qs, urljoin, urlparse

from aiohttp import ClientError, ClientSession, ClientTimeout, CookieJar
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_create_clientsession

IMS = "https://ims.icagruppen.se"
API = "https://apimgw-pub.ica.se"
ACR = "urn:se:curity:authentication:html-form:IcaCustomers"
REDIRECT = "icacurity://app"
USER_AGENT = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
)
# The public client registration the ICA app itself uses (published in open-source clients).
DCR_ID = "ica-app-dcr-registration"
DCR_SECRET = "uxLHTBvZ-Z2fV-SbrHl1E-tz7vB3jQFrwAdSLlbVMMu1rxDdvJU0s8KGu9d1wLS4"
TIMEOUT = ClientTimeout(total=30)


class IcaError(Exception):
    """Anything that stops us talking to ICA."""


class IcaAuthError(IcaError):
    """Wrong personnummer or password, or an account that needs BankID."""


class IcaGeoBlockedError(IcaError):
    """ICA answers HTTP 451 to connections from outside Sweden."""


class IcaConnectionError(IcaError):
    """ICA could not be reached or answered with a server error."""


@dataclass(frozen=True)
class Tokens:
    access_token: str


def normalize_personnummer(value: str) -> str:
    """12 digits: a ten-digit number gets its century."""
    digits = "".join(c for c in value if c.isdigit())
    if len(digits) == 10:
        century = "20" if int(digits[:2]) <= dt.date.today().year % 100 else "19"
        digits = century + digits
    return digits


def _query(location: str, key: str) -> str:
    values = parse_qs(urlparse(location).query).get(key)
    if not values:
        raise IcaConnectionError(f"ICA's login answered without {key!r}")
    return values[0]


def _check(status: int) -> None:
    if status == 451:
        raise IcaGeoBlockedError("ICA only answers connections from Sweden")
    if status >= 500:
        raise IcaConnectionError(f"ICA answered HTTP {status}")
    if status >= 400:
        raise IcaConnectionError(f"ICA's login answered HTTP {status}")


async def async_login(hass: HomeAssistant, personnummer: str, password: str) -> Tokens:
    """Log in and return an access token. Raises IcaError subclasses."""
    session = async_create_clientsession(
        hass, cookie_jar=CookieJar(), auto_cleanup=False
    )
    try:
        return await _login(session, normalize_personnummer(personnummer), password)
    except (ClientError, TimeoutError) as err:
        raise IcaConnectionError(f"Could not reach ICA: {err}") from err
    finally:
        await session.close()


async def _login(session: ClientSession, user: str, password: str) -> Tokens:
    headers = {"User-Agent": USER_AGENT}

    async def post(url: str, **kwargs) -> tuple[int, dict | str, dict]:
        extra = kwargs.pop("headers", {})
        async with session.post(
            url, headers={**headers, **extra}, timeout=TIMEOUT, **kwargs
        ) as response:
            _check(response.status)
            body = await response.text()
            try:  # JSON where ICA sends JSON (whatever it labels it), the page text otherwise
                parsed: dict | str = json.loads(body)
            except ValueError:
                parsed = body
            return response.status, parsed, dict(response.headers)

    async def get(url: str, **kwargs) -> tuple[int, dict]:
        async with session.get(
            url, headers=headers, timeout=TIMEOUT, allow_redirects=False, **kwargs
        ) as response:
            _check(response.status)
            await response.read()
            return response.status, dict(response.headers)

    # 1-2: register as a client, the way the app does
    _, boot, _ = await post(
        f"{IMS}/oauth/v2/token",
        data={
            "client_id": DCR_ID,
            "client_secret": DCR_SECRET,
            "grant_type": "client_credentials",
            "scope": "dcr",
            "response_type": "token",
        },
    )
    _, client, _ = await post(
        f"{IMS}/register",
        json={"software_id": "dcr-ica-app-template"},
        headers={**headers, "Authorization": f"Bearer {boot['access_token']}"},
    )

    # 3-4: start the authorisation (PKCE)
    verifier = re.sub(
        "[^a-zA-Z0-9]+", "", base64.urlsafe_b64encode(os.urandom(40)).decode()
    )
    challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest())
        .decode()
        .replace("=", "")
    )
    _, redirect = await get(
        f"{IMS}/oauth/v2/authorize",
        params={
            "client_id": client["client_id"],
            "scope": client["scope"],
            "redirect_uri": REDIRECT,
            "response_type": "code",
            "code_challenge": challenge,
            "code_challenge_method": "S256",
            "prompt": "login",
            "acr": ACR,
        },
    )
    location = urljoin(f"{IMS}/", redirect["Location"])
    state = _query(location, "state")
    await get(location)

    # 5: the password step. A wrong password, or an account that needs BankID, gives no token.
    _, page, _ = await post(
        f"{IMS}/authn/authenticate/IcaCustomers",
        data={"userName": user, "password": password},
    )
    match = re.search(r'name="token"[^>]*value="([^"]*)"', str(page)) or re.search(
        r'value="([^"]*)"[^>]*name="token"', str(page)
    )
    if not match:
        raise IcaAuthError("ICA did not accept the personnummer and password")

    # 6-7: exchange the result for an access token
    async with session.post(
        f"{IMS}/oauth/v2/authorize",
        params={"client_id": client["client_id"], "forceAuthN": "true", "acr": ACR},
        data={"token": match.group(1), "state": state},
        headers=headers,
        timeout=TIMEOUT,
        allow_redirects=False,
    ) as response:
        _check(response.status)
        code = _query(urljoin(f"{IMS}/", response.headers.get("Location", "")), "code")
    _, tokens, _ = await post(
        f"{IMS}/oauth/v2/token",
        data={
            "code": code,
            "client_id": client["client_id"],
            "client_secret": client["client_secret"],
            "grant_type": "authorization_code",
            "scope": client["scope"],
            "response_type": "token",
            "code_verifier": verifier,
            "redirect_uri": REDIRECT,
        },
    )
    return Tokens(access_token=tokens["access_token"])
