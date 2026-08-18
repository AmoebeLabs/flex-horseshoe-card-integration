"""Config flow for Flex Horseshoe Card."""

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry, ConfigFlowResult, OptionsFlowWithReload
from homeassistant.core import callback
from homeassistant.helpers.selector import selector

from .const import (
    DOMAIN,
    CONF_DEMO_DASHBOARD,
    CONF_TEMPERATURE_ENTITY,
    CONF_HUMIDITY_ENTITY,
    CONF_PRESSURE_ENTITY,
    CONF_POWER_ENTITY_1,
    CONF_POWER_ENTITY_2,
    CONF_POWER_ENTITY_3,
    CONF_POWER_ENTITY_4,
    CONF_BATTERY_ENTITY,
    CONF_SWITCH_ENTITY,
)


DEMO_ENABLE_SCHEMA = vol.Schema(
    {
        vol.Required(
            CONF_DEMO_DASHBOARD,
            default=False,
        ): bool,
    }
)


DEMO_ENTITIES_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_TEMPERATURE_ENTITY): selector(
            {
                "entity": {
                    "filter": [
                        {
                            "domain": "sensor",
                            "device_class": "temperature",
                        }
                    ]
                }
            }
        ),

        vol.Optional(CONF_HUMIDITY_ENTITY): selector(
            {
                "entity": {
                    "filter": [
                        {
                            "domain": "sensor",
                            "device_class": "humidity",
                        }
                    ]
                }
            }
        ),

        vol.Optional(CONF_PRESSURE_ENTITY): selector(
            {
                "entity": {
                    "filter": [
                        {
                            "domain": "sensor",
                            "device_class": "pressure",
                        }
                    ]
                }
            }
        ),
        
        vol.Optional(CONF_POWER_ENTITY_1): selector(
            {
                "entity": {
                    "filter": [
                        {
                            "domain": "sensor",
                            "device_class": "power",
                        }
                    ]
                }
            }
        ),

        vol.Optional(CONF_POWER_ENTITY_2): selector(
            {
                "entity": {
                    "filter": [
                        {
                            "domain": "sensor",
                            "device_class": "power",
                        }
                    ]
                }
            }
        ),

        vol.Optional(CONF_POWER_ENTITY_3): selector(
            {
                "entity": {
                    "filter": [
                        {
                            "domain": "sensor",
                            "device_class": "power",
                        }
                    ]
                }
            }
        ),

        vol.Optional(CONF_POWER_ENTITY_4): selector(
            {
                "entity": {
                    "filter": [
                        {
                            "domain": "sensor",
                            "device_class": "power",
                        }
                    ]
                }
            }
        ),


        vol.Optional(CONF_BATTERY_ENTITY): selector(
            {
                "entity": {
                    "filter": [
                        {
                            "domain": "sensor",
                            "device_class": "battery",
                        }
                    ]
                }
            }
        ),

        vol.Optional(CONF_SWITCH_ENTITY): selector(
            {
                "entity": {
                    "filter": [
                        {
                            "domain": [
                                "switch",
                                "light",
                            ]
                        }
                    ]
                }
            }
        ),
    }
)


class FlexHorseshoeCardConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Handle the Flex Horseshoe Card config flow."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize config flow."""
        self._options: dict[str, Any] = {}

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle initial setup."""

        if user_input is not None:
            self._options.update(user_input)

            if user_input[CONF_DEMO_DASHBOARD]:
                return await self.async_step_demo_entities()

            return self.async_create_entry(
                title="Flex Horseshoe Card",
                data={},
                options=self._options,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=DEMO_ENABLE_SCHEMA,
        )

    async def async_step_demo_entities(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Select entities used by the community demo dashboard."""

        if user_input is not None:
            self._options.update(user_input)

            return self.async_create_entry(
                title="Flexible Horseshoe Card",
                data={},
                options=self._options,
            )

        return self.async_show_form(
            step_id="demo_entities",
            data_schema=DEMO_ENTITIES_SCHEMA,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> "FlexHorseshoeCardOptionsFlow":
        """Return options flow."""
        return FlexHorseshoeCardOptionsFlow()


class FlexHorseshoeCardOptionsFlow(OptionsFlowWithReload):
    """Handle Flex Horseshoe Card options."""

    def __init__(self) -> None:
        """Initialize options flow."""
        self._options: dict[str, Any] = {}

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Configure demo dashboard."""

        if user_input is not None:
            self._options = dict(self.config_entry.options)
            self._options.update(user_input)

            if user_input[CONF_DEMO_DASHBOARD]:
                return await self.async_step_demo_entities()

            return self.async_create_entry(
                data=self._options,
            )

        current = dict(self.config_entry.options)

        schema = self.add_suggested_values_to_schema(
            DEMO_ENABLE_SCHEMA,
            current,
        )

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
        )

    async def async_step_demo_entities(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Configure entities for demo dashboard."""

        if user_input is not None:
            self._options.update(user_input)

            return self.async_create_entry(
                data=self._options,
            )

        schema = self.add_suggested_values_to_schema(
            DEMO_ENTITIES_SCHEMA,
            self._options,
        )

        return self.async_show_form(
            step_id="demo_entities",
            data_schema=schema,
        )
