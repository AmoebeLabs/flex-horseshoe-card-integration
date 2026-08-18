"""Flex Horseshoe Card integration."""

from pathlib import Path

from homeassistant.components.frontend import (
    add_extra_js_url,
    remove_extra_js_url,
)
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    CONF_DEMO_DASHBOARD,
    DEMO_DASHBOARD_FILE,
    DEMO_SOURCE_DIR,
    DEMO_STRATEGY_FILE,
    DOMAIN,
    FRONTEND_FILE,
    FRONTEND_PATH,
)
from .demo import async_register_demo_websocket


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up Flex Horseshoe Card."""

    integration_path = Path(__file__).parent
    frontend_path = integration_path / "frontend"

    data = hass.data.setdefault(DOMAIN, {})

    # Register the integration frontend directory once.
    #
    # /fhs/flex-horseshoe-card.js
    # /fhs/fhs-demo-strategy.js
    #
    # map to:
    #
    # custom_components/flex_horseshoe_card/frontend/
    if not data.get("static_registered"):
        await hass.http.async_register_static_paths(
            [
                StaticPathConfig(
                    FRONTEND_PATH,
                    str(frontend_path),
                    False,
                )
            ]
        )

        data["static_registered"] = True

    # Store the current integration configuration for the
    # demo dashboard WebSocket handler.
    data["demo_enabled"] = entry.options.get(
        CONF_DEMO_DASHBOARD,
        False,
    )

    data["demo_options"] = dict(entry.options)

    data["demo_source"] = (
        integration_path
        / DEMO_SOURCE_DIR
        / DEMO_DASHBOARD_FILE
    )

    # Register the demo dashboard WebSocket command once.
    if not data.get("websocket_registered"):
        async_register_demo_websocket(hass)
        data["websocket_registered"] = True

    # Load FHS automatically in the Home Assistant frontend.
    frontend_url = f"{FRONTEND_PATH}/{FRONTEND_FILE}"

    add_extra_js_url(
        hass,
        frontend_url,
    )

    # Only load/register the demo dashboard strategy when
    # the demo dashboard has been enabled in the integration.
    strategy_url = f"{FRONTEND_PATH}/{DEMO_STRATEGY_FILE}"

    if data["demo_enabled"]:
        add_extra_js_url(
            hass,
            strategy_url,
        )

        data["strategy_loaded"] = True
    else:
        data["strategy_loaded"] = False

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload Flex Horseshoe Card."""

    data = hass.data.get(DOMAIN, {})

    frontend_url = f"{FRONTEND_PATH}/{FRONTEND_FILE}"

    remove_extra_js_url(
        hass,
        frontend_url,
    )

    if data.get("strategy_loaded"):
        strategy_url = f"{FRONTEND_PATH}/{DEMO_STRATEGY_FILE}"

        remove_extra_js_url(
            hass,
            strategy_url,
        )

    # Keep the one-time registrations in hass.data, because
    # Home Assistant can unload and reload a config entry.
    data["demo_enabled"] = False
    data["demo_options"] = {}
    data["strategy_loaded"] = False

    return True
