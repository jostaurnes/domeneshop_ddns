from datetime import timedelta
from homeassistant.const import CONF_DOMAIN, CONF_PASSWORD, CONF_TIMEOUT, CONF_USERNAME

import voluptuous as vol
import homeassistant.helpers.config_validation as cv

DOMAIN = "domeneshop_ddns"
update_base_google = "domains.google.com/nic"
update_base_domeneshop = "api.domeneshop.no/v0/dyndns"
UPDATE_BASE = update_base_domeneshop

INTERVAL = timedelta(minutes=5)

DEFAULT_TIMEOUT = 10

DOMAIN_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_DOMAIN): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): cv.positive_int,
    }
)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: DOMAIN_SCHEMA
    },
    extra=vol.ALLOW_EXTRA,
)
