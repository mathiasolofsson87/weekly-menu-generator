"""ICA's account setup: the form, the checks, and the keys it owns in the config entry."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import voluptuous as vol
from homeassistant.core import HomeAssistant
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)

from ..base import ProviderSetup
from .auth import (
    IcaAuthError,
    IcaConnectionError,
    IcaGeoBlockedError,
    async_login,
    normalize_personnummer,
)
from .provider import MODE_NAMED, MODE_WEEKLY

CONF_USER = "ica_personnummer"
CONF_PASSWORD = "ica_password"
CONF_LIST_MODE = "ica_list_mode"
CONF_LIST_NAME = "ica_list_name"
KEYS = (CONF_USER, CONF_PASSWORD, CONF_LIST_MODE, CONF_LIST_NAME)


def _schema(config: Mapping[str, Any]) -> vol.Schema:
    return vol.Schema(
        {
            vol.Optional(CONF_USER): TextSelector(),
            vol.Optional(CONF_PASSWORD): TextSelector(
                TextSelectorConfig(type=TextSelectorType.PASSWORD)
            ),
            vol.Required(CONF_LIST_MODE, default=MODE_WEEKLY): SelectSelector(
                SelectSelectorConfig(
                    options=[MODE_WEEKLY, MODE_NAMED],
                    translation_key=CONF_LIST_MODE,
                    mode=SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Optional(CONF_LIST_NAME): TextSelector(),
        }
    )


async def _validate(
    hass: HomeAssistant, config: Mapping[str, Any], user_input: Mapping[str, Any]
) -> tuple[dict[str, Any], dict[str, str]]:
    """(changes to the config entry data, form errors). A None value removes a key."""
    user = (user_input.get(CONF_USER) or "").strip()
    if not user:  # an empty personnummer switches ICA off
        return dict.fromkeys(KEYS), {}

    personnummer = normalize_personnummer(user)
    password = user_input.get(CONF_PASSWORD) or config.get(CONF_PASSWORD)
    if len(personnummer) != 12:
        return {}, {CONF_USER: "invalid_personnummer"}
    if not password:
        return {}, {CONF_PASSWORD: "password_required"}
    try:
        await async_login(hass, personnummer, password)
    except IcaAuthError:
        return {}, {"base": "invalid_auth"}
    except IcaGeoBlockedError:
        return {}, {"base": "geo_blocked"}
    except IcaConnectionError:
        return {}, {"base": "cannot_connect"}
    return {
        CONF_USER: personnummer,
        CONF_PASSWORD: password,
        CONF_LIST_MODE: user_input.get(CONF_LIST_MODE, MODE_WEEKLY),
        CONF_LIST_NAME: (user_input.get(CONF_LIST_NAME) or "").strip() or None,
    }, {}


SETUP = ProviderSetup(
    id="ica",
    keys=KEYS,
    schema=_schema,
    validate=_validate,
    reauth_keys=(CONF_USER, CONF_PASSWORD),
    secret_keys=(CONF_PASSWORD,),
)
