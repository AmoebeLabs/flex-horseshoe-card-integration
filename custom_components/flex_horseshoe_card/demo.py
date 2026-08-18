"""Flex Horseshoe Card demo dashboard."""

from pathlib import Path
from typing import Any

import voluptuous as vol

from homeassistant.components import websocket_api
from homeassistant.components.websocket_api import ActiveConnection
from homeassistant.core import HomeAssistant, callback
from homeassistant.util.yaml import load_yaml_dict

from .const import (
    CONF_BATTERY_ENTITY,
    CONF_POWER_ENTITY,
    CONF_HUMIDITY_ENTITY,
    CONF_SWITCH_ENTITY,
    CONF_TEMPERATURE_ENTITY,
    DOMAIN,
    WS_DEMO_DASHBOARD,
)


ENTITY_PLACEHOLDERS = {
    "__FHS_TEMPERATURE__": CONF_TEMPERATURE_ENTITY,
    "__FHS_HUMIDITY__": CONF_HUMIDITY_ENTITY,
    "__FHS_ENERGY__": CONF_ENERGY_ENTITY,
    "__FHS_BATTERY__": CONF_BATTERY_ENTITY,
    "__FHS_SWITCH__": CONF_SWITCH_ENTITY,
}


DISABLED_PLACEHOLDERS = {
    "__FHS_TEMPERATURE_DISABLED__": CONF_TEMPERATURE_ENTITY,
    "__FHS_HUMIDITY_DISABLED__": CONF_HUMIDITY_ENTITY,
    "__FHS_POWER_DISABLED__": CONF_POWER_ENTITY,
    "__FHS_BATTERY_DISABLED__": CONF_BATTERY_ENTITY,
    "__FHS_SWITCH_DISABLED__": CONF_SWITCH_ENTITY,
}


@callback
def async_register_demo_websocket(
    hass: HomeAssistant,
) -> None:
    """Register the demo dashboard WebSocket command."""

    websocket_api.async_register_command(
        hass,
        websocket_demo_dashboard,
    )


@websocket_api.websocket_command(
    {
        vol.Required("type"): WS_DEMO_DASHBOARD,
    }
)
@websocket_api.async_response
async def websocket_demo_dashboard(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return the cached FHS demo dashboard."""

    data = hass.data.get(DOMAIN, {})

    if not data.get("demo_enabled"):
        connection.send_error(
            msg["id"],
            "demo_disabled",
            "The Flex Horseshoe Card demo dashboard is disabled.",
        )
        return

    dashboard = data.get("demo_config")

    if dashboard is None:
        connection.send_error(
            msg["id"],
            "demo_config_missing",
            "The Flex Horseshoe Card demo dashboard is unavailable.",
        )
        return

    connection.send_result(
        msg["id"],
        dashboard,
    )


def load_demo_dashboard(
    source: Path,
    options: dict[str, Any],
) -> dict[str, Any]:
    """Load and prepare the FHS demo dashboard."""

    dashboard = load_yaml_dict(source)

    return replace_placeholders(
        dashboard,
        options,
    )


def replace_placeholders(
    value: Any,
    options: dict[str, Any],
) -> Any:
    """Replace FHS demo placeholders recursively."""

    if isinstance(value, dict):
        return {
            key: replace_placeholders(
                item,
                options,
            )
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            replace_placeholders(
                item,
                options,
            )
            for item in value
        ]

    if not isinstance(value, str):
        return value

    if value in ENTITY_PLACEHOLDERS:
        option_name = ENTITY_PLACEHOLDERS[value]

        entity_id = options.get(
            option_name,
        )

        if entity_id:
            return entity_id

        return ""

    if value in DISABLED_PLACEHOLDERS:
        option_name = DISABLED_PLACEHOLDERS[value]

        entity_id = options.get(
            option_name,
        )

        return not bool(entity_id)

    return value
