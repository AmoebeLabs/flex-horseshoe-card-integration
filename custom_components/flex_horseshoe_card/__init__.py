from pathlib import Path

from homeassistant.components.frontend import (
    add_extra_js_url,
    remove_extra_js_url,
)
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, FRONTEND_FILE, FRONTEND_PATH


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

    frontend_url = f"{FRONTEND_PATH}/{FRONTEND_FILE}"

    add_extra_js_url(hass, frontend_url)

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload Flex Horseshoe Card."""

    frontend_url = f"{FRONTEND_PATH}/{FRONTEND_FILE}"

    remove_extra_js_url(hass, frontend_url)

    return True
