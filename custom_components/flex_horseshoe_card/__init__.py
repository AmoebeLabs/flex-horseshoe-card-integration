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
from .demo import (
    load_demo_dashboard,
    async_register_demo_websocket,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up Flex Horseshoe Card."""

    integration_path = Path(__file__).parent
    frontend_path = integration_path / "frontend"

    data = hass.data.setdefault(DOMAIN, {})

    # Register the integration frontend directory once.
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

    # Store integration configuration.
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

    # Load and parse the complete demo dashboard once.
    #
    # YAML file access and include processing are blocking,
    # so run the synchronous loader in Home Assistant's executor.
    if data["demo_enabled"]:
        data["demo_config"] = await hass.async_add_executor_job(
            load_demo_dashboard,
            data["demo_source"],
            data["demo_options"],
        )
    else:
        data["demo_config"] = None

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
    # the demo dashboard has been enabled.
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
