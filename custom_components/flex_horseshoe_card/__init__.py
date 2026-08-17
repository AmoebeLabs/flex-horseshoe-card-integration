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
    DEMO_SOURCE_DIR,
    DEMO_TARGET_DIR,
    DOMAIN,
    FRONTEND_FILE,
    FRONTEND_PATH,
)
from .demo import (
    generate_demo,
    remove_demo,
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
    #
    # /fhs/flex-horseshoe-card.js
    # maps to:
    # custom_components/flex_horseshoe_card/frontend/flex-horseshoe-card.js
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

    # Load FHS automatically in the Home Assistant frontend.
    frontend_url = f"{FRONTEND_PATH}/{FRONTEND_FILE}"

    add_extra_js_url(
        hass,
        frontend_url,
    )

    # Demo source delivered inside the integration ZIP.
    demo_source = integration_path / DEMO_SOURCE_DIR

    # Generated demo dashboard under the Home Assistant config directory.
    demo_target = Path(
        hass.config.path(DEMO_TARGET_DIR)
    )

    # Generate or remove the demo depending on the integration option.
    if entry.options.get(CONF_DEMO_DASHBOARD, False):
        await hass.async_add_executor_job(
            generate_demo,
            demo_source,
            demo_target,
            dict(entry.options),
        )
    else:
        await hass.async_add_executor_job(
            remove_demo,
            demo_target,
        )

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload Flex Horseshoe Card."""

    frontend_url = f"{FRONTEND_PATH}/{FRONTEND_FILE}"

    remove_extra_js_url(
        hass,
        frontend_url,
    )

    return True
