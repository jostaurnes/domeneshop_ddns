"""Support for DomeneShop DDNS."""
import asyncio

import logging

import aiohttp
from homeassistant.const import CONF_DOMAIN, CONF_PASSWORD, CONF_TIMEOUT, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN, INTERVAL, UPDATE_BASE

_LOGGER = logging.getLogger(__name__)
#_LOGGER.setLevel(logging.INFO)



async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    _LOGGER.info("runnint async_setup_entry")
    domain = config_entry.data[CONF_DOMAIN]
    user = config_entry.data[CONF_USERNAME]
    password = config_entry.data[CONF_PASSWORD]
    timeout = config_entry.options[CONF_TIMEOUT]
    return await setup(hass, domain, user, password, timeout)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """not in use"""
    _LOGGER.info("runnint async_setup")
    return True

async def _not_used(hass: HomeAssistant, config: ConfigType) -> bool:
    """Initialize the DDNS component."""
    domain = config[DOMAIN].get(CONF_DOMAIN)
    user = config[DOMAIN].get(CONF_USERNAME)
    password = config[DOMAIN].get(CONF_PASSWORD)
    timeout = config[DOMAIN].get(CONF_TIMEOUT)
    return await setup(hass, domain, user, password, timeout)

async def setup(hass: HomeAssistant, domain, user, password, timeout) -> bool:
    session = async_get_clientsession(hass)

    result = await _update_ddns_domains(
        hass, session, domain, user, password, timeout
    )

    if not result:
        return False

    async def update_domain_interval(now):
        """Update the DDNS Domains entry."""
        await _update_ddns_domains(hass, session, domain, user, password, timeout)

    async_track_time_interval(hass, update_domain_interval, INTERVAL)

    return True


async def _update_ddns_domains(hass, session, domain, user, password, timeout):
    """Update DDNS Domains."""
    url = f"https://{user}:{password}@{UPDATE_BASE}/update"

    params = {"hostname": domain}

    _LOGGER.info("Connecting to url: %s, with param %s", url, params)

    try:
        async with asyncio.timeout(timeout):
            resp = await session.get(url, params=params)
            body = await resp.text()

            if resp.status == 200 or resp.status == 204:
                _LOGGER.info("Successfully updated DDNS for domain: %s", domain)
                return True

            _LOGGER.warning("Updating DomeneShop DDSS failed: %s => %d,%s", domain, resp.status, body)
            return False

    except aiohttp.ClientError:
        _LOGGER.warning("Can't connect to DDNS Update API: %s", url)

    except asyncio.TimeoutError:
        _LOGGER.warning("Timeout from DDNS Update API for domain: %s", domain)

    return False
