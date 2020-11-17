from homeassistant.components.cast.const import (
    SIGNAL_CAST_DISCOVERED,
    SIGNAL_CAST_REMOVED,
    KNOWN_CHROMECAST_INFO_KEY,
    DOMAIN as CAST_DOMAIN,
)
from homeassistant.components.cast.helpers import ChromecastInfo, ChromeCastZeroconf
from homeassistant.helpers.dispatcher import async_dispatcher_connect

import asyncio
import pychromecast
import logging

from .const import CLIENT, DOMAIN

_LOGGER = logging.getLogger(__name__)

class ChromecastMonitor:
    async def async_init(self, hass):
        self._hass = hass
        self._active_devices = {}
        
        _LOGGER.debug("Setting up signals")
        async_dispatcher_connect(hass, SIGNAL_CAST_REMOVED, self.async_cast_removed)
        async_dispatcher_connect(hass, SIGNAL_CAST_DISCOVERED, self.async_cast_discovered)
        for chromecast in hass.data[KNOWN_CHROMECAST_INFO_KEY].copy().values():
            await self.async_cast_discovered(chromecast, True)

    async def async_cast_discovered(self, discover: ChromecastInfo, likely_already_started=False):
        _LOGGER.debug("Discovered {}".format(discover.host))
        if discover.is_audio_group:
            return

        if not likely_already_started:
            # eureka_info might not return something, if the device just started up
            await asyncio.sleep(10)

        self._hass.data[DOMAIN].setdefault(discover.uuid, {})
        if await self._hass.data[CLIENT].update_info(discover.host, discover.uuid):
            info = self._hass.data[DOMAIN][discover.uuid]["info"]
            if info["device_info"]["cloud_device_id"] not in self._active_devices and await self.supported(discover):
                chromecast = await self._hass.async_add_executor_job(
                    pychromecast.get_chromecast_from_service,
                    (
                        discover.services,
                        discover.uuid,
                        discover.model_name,
                        discover.friendly_name,
                        None,
                        None,
                    ),
                    ChromeCastZeroconf.get_zeroconf(),
                )
                chromecast.register_connection_listener(self)
                self._active_devices[info["device_info"]["cloud_device_id"]] = await self.setup(discover)

    async def async_cast_removed(self, discover: ChromecastInfo):
        _LOGGER.debug("Removed {}".format(discover.uuid))
        if discover.is_audio_group:
            return

        info = self._hass.data[DOMAIN][discover.uuid]["info"]
        if info["device_info"]["cloud_device_id"] in self._active_devices:
            await self.cleanup(discover.uuid)
            del self._active_devices[info["device_info"]["cloud_device_id"]]
    
    async def supported(self, discover: ChromecastInfo) -> bool:
        return True

    async def setup(self, discover: ChromecastInfo):
        return []

    async def cleanup(self, discover: ChromecastInfo):
        pass

    def new_connection_status(self, connection_status):
        """Handle reception of a new ConnectionStatus."""
        for entity in self._active_devices.values():
            entity.connection_status(connection_status.status)