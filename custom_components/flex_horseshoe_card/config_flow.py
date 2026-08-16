from homeassistant import config_entries

from .const import DOMAIN


class FlexHorseshoeCardConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Configure Flex Horseshoe Card."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Create the single FHS config entry."""

        return self.async_create_entry(
            title="Flex Horseshoe Card",
            data={},
        )
