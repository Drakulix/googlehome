"""Support Google Home units."""
import logging

import asyncio
import grpc

from homeassistant import config_entries
from homeassistant.helpers import discovery
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession


from .auth import get_access_token
from .const import CLIENT, DOMAIN, TOKENS, CONF_TRACK_ALARMS, CONF_TRACK_DEVICES, CONF_USERNAME, CONF_MASTER_TOKEN
from .grpc.google.internal.home.foyer.v1_pb2_grpc import StructuresServiceStub

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    """Set up the Google Home component."""
    hass.data[DOMAIN] = {}
    hass.data[TOKENS] = {}
    hass.data[CLIENT] = GoogleHomeClient(hass)

    return True

async def async_setup_entry(hass, entry: config_entries.ConfigEntry):
    await refresh_tokens(hass, entry)

    if entry[CONF_TRACK_ALARMS]:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, "sensor")
        )
    if entry[CONF_TRACK_DEVICES]:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, "device_tracker")
        )

    return True

async def refresh_tokens(hass, entry):
    access_token = get_access_token(entry[CONF_USERNAME], entry[CONF_MASTER_TOKEN])
    channel = grpc.channel('googlehomefoyer-pa.googleapis.com:443')
    service = StructuresServiceStub(channel)
    resp = service.GetHomeGraph()
    data = resp.value['home']['devices']
    for device in data:
        # this is the 'cloud device id'
        hass.data[TOKENS][device['deviceInfo']['projectInfo']['string2']] = device['localAuthToken']

class GoogleHomeClient:
    """Handle all communication with the Google Home unit."""

    def __init__(self, hass, host):
        """Initialize the Google Home Client."""
        self.hass = hass
        self._connected = None

    async def update_info(self, host):
        """Update data from Google Home."""
        from .googledevices.api.connect import Cast

        _LOGGER.debug("Updating Google Home info for %s", host)
        session = async_get_clientsession(self.hass)

        device_info = await Cast(host, self.hass.loop, session).info()
        device_info_data = await device_info.get_device_info()
        self._connected = bool(device_info_data)

        self.hass.data[DOMAIN][host]["info"] = device_info_data

    async def update_bluetooth(self, host):
        """Update bluetooth from Google Home."""
        from .googledevices.api.connect import Cast

        _LOGGER.debug("Updating Google Home bluetooth for %s", host)
        session = async_get_clientsession(self.hass)
        
        try:
            info = self.hass.data[DOMAIN][host]
            token = self.hass.data[TOKENS][info['device_info']['cloud_device_id']]
        except KeyError:
            return

        bluetooth = await Cast(host, self.hass.loop, session).bluetooth()
        await bluetooth.scan_for_devices(token)
        await asyncio.sleep(5)
        bluetooth_data = await bluetooth.get_scan_result(token)
        if not bluetooth_data:
            print("Scan failed, scheduling token update")
            hass.async_create_task(refresh_tokens(self.hass))
            return

        self.hass.data[DOMAIN][host]["bluetooth"] = bluetooth_data

    async def update_alarms(self, host):
        """Update alarms from Google Home."""
        from .googledevices.api.connect import Cast

        _LOGGER.debug("Updating Google Home bluetooth for %s", host)
        session = async_get_clientsession(self.hass)

        try:
            info = self.hass.data[DOMAIN][host]
            token = self.hass.data[TOKENS][info['device_info']['cloud_device_id']]
        except KeyError:
            if not self.hass.data[DOMAIN][host].get("alarms"):
                self.hass.data[DOMAIN][host]["alarms"] = {"timer": [], "alarm": []}
            return
        
        assistant = await Cast(host, self.hass.loop, session).assistant()
        alarms_data = await assistant.get_alarms(token)
        if not alarms_data:
            print("Getting alarms failed, scheduling token update")
            hass.async_create_task(refresh_tokens(self.hass))
            return

        self.hass.data[DOMAIN][host]["alarms"] = alarms_data
