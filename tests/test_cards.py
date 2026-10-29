"""The dashboard cards are served and registered by the integration."""

from unittest.mock import AsyncMock, MagicMock, patch

from homeassistant.core import HomeAssistant

from custom_components.weeklymenu import cards


async def test_cards_are_served_and_added_to_every_dashboard(
    hass: HomeAssistant,
) -> None:
    hass.config.components.add("frontend")
    hass.http = MagicMock(async_register_static_paths=AsyncMock())
    with patch("homeassistant.components.frontend.add_extra_js_url") as add:
        await cards.async_register_cards(hass)

    [(paths,), _] = hass.http.async_register_static_paths.call_args
    assert [(p.url_path, p.path) for p in paths] == [
        ("/weeklymenu_cards/weeklymenu-cards.js", str(cards.BUNDLE))
    ]
    [(_, url), _] = add.call_args
    assert (
        url.startswith("/weeklymenu_cards/weeklymenu-cards.js?v=")
        and len(url.split("=")[1]) == 10
    )


async def test_a_new_build_gets_a_new_address(tmp_path, hass: HomeAssistant) -> None:
    first, second = tmp_path / "a.js", tmp_path / "b.js"
    first.write_text("one")
    second.write_text("two")
    assert cards._fingerprint(first) != cards._fingerprint(second)
    assert cards._fingerprint(first) == cards._fingerprint(first)
    assert cards._fingerprint(tmp_path / "missing.js") is None


async def test_nothing_happens_without_a_frontend(hass: HomeAssistant) -> None:
    hass.http = MagicMock(async_register_static_paths=AsyncMock())
    with patch("homeassistant.components.frontend.add_extra_js_url") as add:
        await cards.async_register_cards(hass)  # "frontend" is not set up
    hass.http.async_register_static_paths.assert_not_called()
    add.assert_not_called()


async def test_nothing_happens_without_http(hass: HomeAssistant) -> None:
    hass.config.components.add("frontend")
    hass.http = None
    with patch("homeassistant.components.frontend.add_extra_js_url") as add:
        await cards.async_register_cards(hass)
    add.assert_not_called()


async def test_a_missing_bundle_is_reported_not_fatal(
    hass: HomeAssistant, caplog
) -> None:
    hass.config.components.add("frontend")
    hass.http = MagicMock(async_register_static_paths=AsyncMock())
    with (
        patch.object(cards, "BUNDLE", cards.BUNDLE.with_name("nope.js")),
        patch("homeassistant.components.frontend.add_extra_js_url") as add,
    ):
        await cards.async_register_cards(hass)
    add.assert_not_called()
    assert "dashboard cards are missing" in caplog.text


def test_the_built_bundle_is_in_the_repository() -> None:
    """HACS users get the cards with the integration, so the build must be committed."""
    bundle = cards.BUNDLE.read_text(encoding="utf-8")
    for element in (
        "weeklymenu-menu-card",
        "weeklymenu-today-card",
        "weeklymenu-shopping-card",
        "weeklymenu-family-card",
        "weeklymenu-menu-card-editor",
        "weeklymenu-shopping-card-editor",
        "weeklymenu-family-card-editor",
    ):
        assert element in bundle
    assert len(bundle) > 10_000


async def test_setting_up_the_integration_registers_the_cards(
    hass: HomeAssistant,
) -> None:
    from homeassistant.setup import async_setup_component

    with patch(
        "custom_components.weeklymenu.async_register_cards", AsyncMock()
    ) as register:
        assert await async_setup_component(hass, "weeklymenu", {})
    register.assert_awaited_once_with(hass)
