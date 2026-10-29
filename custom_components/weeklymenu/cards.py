"""Serves the dashboard cards and tells Home Assistant to load them."""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path

from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

BUNDLE = Path(__file__).parent / "www" / "weeklymenu-cards.js"
URL_BASE = "/weeklymenu_cards"
URL = f"{URL_BASE}/{BUNDLE.name}"


def _fingerprint(path: Path) -> str | None:
    """A short hash of the bundle, so a new build is never served from the browser cache."""
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()[:10]
    except OSError:
        return None


async def async_register_cards(hass: HomeAssistant) -> None:
    """Make the cards available on every dashboard. Quietly does nothing when there is no
    frontend (a headless install) or no built bundle (a checkout that was never built)."""
    if "frontend" not in hass.config.components or getattr(hass, "http", None) is None:
        _LOGGER.debug("No frontend to add the dashboard cards to")
        return
    version = await hass.async_add_executor_job(_fingerprint, BUNDLE)
    if version is None:
        _LOGGER.warning(
            "The dashboard cards are missing (%s). Build them with `npm run build` in frontend/",
            BUNDLE,
        )
        return

    from homeassistant.components.frontend import add_extra_js_url
    from homeassistant.components.http import StaticPathConfig

    await hass.http.async_register_static_paths(
        [StaticPathConfig(URL, str(BUNDLE), cache_headers=True)]
    )
    add_extra_js_url(hass, f"{URL}?v={version}")
