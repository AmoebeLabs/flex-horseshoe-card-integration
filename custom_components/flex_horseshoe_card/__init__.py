"""Flex Horseshoe Card integration."""

from pathlib import Path
import logging

_LOGGER = logging.getLogger(__name__)

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

    _LOGGER.warning(
        "FHS setup: integration_path=%s frontend_path=%s exists=%s",
        integration_path,
        frontend_path,
        frontend_path.exists(),
    )

    data = hass.data.setdefault(DOMAIN, {})

    if not data.get("static_registered"):
        _LOGGER.warning(
            "FHS registering static path: %s -> %s",
            FRONTEND_PATH,
            frontend_path,
        )

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

    _LOGGER.warning(
        "FHS demo_enabled=%s entry.options=%s",
        data["demo_enabled"],
        dict(entry.options),
    )

    data["demo_options"] = dict(entry.options)

    data["demo_source"] = (
        integration_path
        / DEMO_SOURCE_DIR
        / DEMO_DASHBOARD_FILE
    )

    _LOGGER.warning(
        "FHS demo source: %s exists=%s",
        data["demo_source"],
        data["demo_source"].exists(),
    )

    if not data.get("websocket_registered"):
        _LOGGER.warning("FHS registering demo websocket")
        async_register_demo_websocket(hass)
        data["websocket_registered"] = True

    frontend_url = f"{FRONTEND_PATH}/{FRONTEND_FILE}"

    _LOGGER.warning(
        "FHS loading frontend JS: %s file=%s exists=%s",
        frontend_url,
        frontend_path / FRONTEND_FILE,
        (frontend_path / FRONTEND_FILE).exists(),
    )

    add_extra_js_url(
        hass,
        frontend_url,
    )

    strategy_url = f"{FRONTEND_PATH}/{DEMO_STRATEGY_FILE}"

    _LOGGER.warning(
        "FHS strategy: enabled=%s url=%s file=%s exists=%s",
        data["demo_enabled"],
        strategy_url,
        frontend_path / DEMO_STRATEGY_FILE,
        (frontend_path / DEMO_STRATEGY_FILE).exists(),
    )

    if data["demo_enabled"]:
        _LOGGER.warning(
            "FHS loading demo strategy JS: %s",
            strategy_url,
        )

        add_extra_js_url(
            hass,
            strategy_url,
        )

        data["strategy_loaded"] = True
    else:
        _LOGGER.warning("FHS demo strategy NOT loaded because demo_enabled=False")
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
