from datetime import timedelta
from homeassistant.const import CONF_DOMAIN, CONF_PASSWORD, CONF_TIMEOUT, CONF_USERNAME

import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.selector import TextSelector, TextSelectorConfig, TextSelectorType, NumberSelector, NumberSelectorConfig, NumberSelectorMode

DOMAIN = "domeneshop_ddns"
update_base_google = "domains.google.com/nic"
update_base_domeneshop = "api.domeneshop.no/v0/dyndns"
UPDATE_BASE = update_base_domeneshop

INTERVAL = timedelta(minutes=5)

DEFAULT_TIMEOUT = 10

DOMAIN_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_DOMAIN): TextSelector(
            TextSelectorConfig(type=TextSelectorType.TEXT, autocomplete="host")
        ),

        vol.Required(CONF_USERNAME): TextSelector(
            TextSelectorConfig(type=TextSelectorType.EMAIL, autocomplete="username")
        ),
        vol.Required(CONF_PASSWORD): TextSelector(
            TextSelectorConfig(type=TextSelectorType.PASSWORD, autocomplete="password")
        ),
        vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): NumberSelector(
            NumberSelectorConfig(min=5, max=60, step=5, unit_of_measurement="s",
                                 mode=NumberSelectorMode("slider"))
        ),
    }
)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: DOMAIN_SCHEMA
    },
    extra=vol.ALLOW_EXTRA,
)
