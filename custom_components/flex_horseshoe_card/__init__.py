"""Flex Horseshoe Card integration."""

from pathlib import Path
import logging

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
from .demo import (
    async_load_demo_dashboard,
    async_register_demo_websocket,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up Flex Horseshoe Card."""

    integration_path = Path(__file__).parent
    frontend_path = integration_path / "frontend"

    data = hass.data.setdefault(DOMAIN, {})

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

    # Load and parse the complete demo only once.
    if data["demo_enabled"]:
        data["demo_config"] = await async_load_demo_dashboard(
            hass,
            data["demo_source"],
            data["demo_options"],
        )
    else:
        data["demo_config"] = None

    # WebSocket only returns the cached config.
    if not data.get("websocket_registered"):
        async_register_demo_websocket(hass)
        data["websocket_registered"] = True

    frontend_url = f"{FRONTEND_PATH}/{FRONTEND_FILE}"

    add_extra_js_url(
        hass,
        frontend_url,
    )

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

    data["demo_enabled"] = False
    data["demo_options"] = {}
    data["demo_config"] = None
    data["strategy_loaded"] = False

    return True
