"""ICA's shopping list API (as used by the ICA app)."""

from __future__ import annotations

import datetime as dt
import json
import random
import uuid
from typing import Any

from aiohttp import ClientError, ClientSession, ClientTimeout

from .auth import (
    API,
    USER_AGENT,
    IcaAuthError,
    IcaConnectionError,
    IcaError,
    IcaGeoBlockedError,
    Tokens,
)

LISTS = "sverige/digx/mobile/shoppinglistservice/v1/shoppinglists"
TIMEOUT = ClientTimeout(total=30)


def row(name: str, quantity: float, unit: str) -> dict[str, Any]:
    """A free-text row, in the shape the app sends."""
    return {
        "offlineId": str(uuid.uuid4()).upper(),
        "productName": name,
        "quantity": quantity,
        "unit": unit,
        "sourceId": -random.randint(10**6, 10**9),
        "isStrikedOver": False,
        "recipes": [],
    }


class IcaApi:
    """Lists and rows. Every call needs a fresh login; see `auth.async_login`."""

    def __init__(self, session: ClientSession, tokens: Tokens) -> None:
        self._session = session
        self._headers = {
            "Authorization": f"Bearer {tokens.access_token}",
            "User-Agent": USER_AGENT,
        }

    async def _call(self, method: str, path: str, body: dict | None = None) -> Any:
        try:
            async with self._session.request(
                method,
                f"{API}/{path}",
                json=body,
                headers=self._headers,
                timeout=TIMEOUT,
            ) as response:
                if response.status == 451:
                    raise IcaGeoBlockedError("ICA only answers connections from Sweden")
                if response.status in (401, 403):
                    raise IcaAuthError(
                        f"ICA refused the access token (HTTP {response.status})"
                    )
                if response.status >= 400:
                    raise IcaConnectionError(
                        f"{method} {path} answered HTTP {response.status}"
                    )
                text = await response.text()
                try:
                    return json.loads(text) if text.strip() else None
                except ValueError as err:
                    raise IcaConnectionError(
                        f"{method} {path} answered something that is not JSON"
                    ) from err
        except (ClientError, TimeoutError) as err:
            raise IcaConnectionError(f"Could not reach ICA: {err}") from err

    async def async_find_list(self, title: str) -> str | None:
        """Id of the list with this title, or None."""
        data = await self._call("GET", LISTS) or {}
        for found in data.get("shoppingLists", []):
            if str(found.get("title", "")).casefold() == title.casefold():
                return found.get("offlineId") or found.get("id")
        return None

    async def async_create_list(self, title: str) -> str:
        list_id = str(uuid.uuid4()).upper()
        await self._call(
            "POST",
            LISTS,
            {
                "offlineId": list_id,
                "title": title,
                "commentText": "",
                "sortingStore": 0,
                "rows": [],
                "latestChange": dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
            },
        )
        return list_id

    async def async_row_names(self, list_id: str) -> set[str]:
        """Names already on the list, lower case."""
        data = await self._call("GET", f"{LISTS}/{list_id}") or {}
        return {str(r.get("productName", "")).casefold() for r in data.get("rows", [])}

    async def async_add_rows(self, list_id: str, rows: list[dict[str, Any]]) -> None:
        if rows:
            await self._call("POST", f"{LISTS}/{list_id}/sync", {"createdRows": rows})


__all__ = ["IcaApi", "IcaError", "row"]
