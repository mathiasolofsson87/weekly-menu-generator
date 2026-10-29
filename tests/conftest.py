"""Shared fixtures."""

from unittest.mock import patch

import pytest
from freezegun.api import FrozenDateTimeFactory
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.weeklymenu.const import DOMAIN
from custom_components.weeklymenu.sources.registry import SourceRegistry
from tests.helpers import ALL_RECIPES, FakeSource

OPTIONS = {
    "dinner_days": ["mon", "tue", "wed"],
    "vegetarian_days": 0,
    "fish_min": 0,
    "members": [
        {
            "id": "1",
            "name": "Anna",
            "allergies": ["fish"],
            "attends": ["mon", "tue", "wed"],
        }
    ],
}


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Let Home Assistant load custom_components/ in every test."""
    yield


@pytest.fixture
def fake() -> FakeSource:
    """The only recipe source in integration tests; nothing touches the network."""
    return FakeSource(ALL_RECIPES)


@pytest.fixture
async def entry(hass: HomeAssistant, fake: FakeSource, freezer: FrozenDateTimeFactory):
    """A set-up config entry. The clock stands at Wednesday 2026-11-04 12:00 UTC."""
    await hass.config.async_set_time_zone("UTC")
    freezer.move_to("2026-11-04 12:00:00+00:00")
    registry = SourceRegistry()
    registry.register("fake", lambda hass, config: fake)
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={"language": "sv", "units": "swedish"},
        options=dict(OPTIONS),
    )
    entry.add_to_hass(hass)
    with patch(
        "custom_components.weeklymenu.build_default_registry", return_value=registry
    ):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
        yield entry
