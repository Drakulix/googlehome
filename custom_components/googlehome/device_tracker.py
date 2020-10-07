"""Support for Google Home Bluetooth tacker."""
from datetime import timedelta
import logging

from homeassistant.components.device_tracker import DeviceScanner
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.util import slugify

# borrow some cast functionality
from homeassistant.components.cast.const import (
    SIGNAL_CAST_DISCOVERED,
    KNOWN_CHROMECAST_INFO_KEY,
)
from homeassistant.components.cast.helpers import ChromecastInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import CLIENT, DOMAIN, NAME, CONF_RSSI_THRESHOLD, CONF_DEVICE_TYPES

_LOGGER = logging.getLogger(__name__)

DEFAULT_SCAN_INTERVAL = timedelta(seconds=10)


async def async_setup_entry(hass, config_entry, async_see):
    """Setup the Google Home scanner platform"""
    async def async_cast_discovered(discover: ChromecastInfo):
        print(discover.uuid)
        hass.data[DOMAIN].setdefault(discover.host, {})

        await hass.data[CLIENT].update_info(discover.host)
        info = hass.data[DOMAIN][discover.host].get("info", { "device_info": {} })
        if info["device_info"]["capabilities"]["bluetooth_supported"]:
            scanner = GoogleHomeDeviceScanner(
                hass, hass.data[CLIENT], config_entry, discover, async_see
            )
            return await scanner.async_init()

    async_dispatcher_connect(hass, SIGNAL_CAST_DISCOVERED, async_cast_discovered)
    for chromecast in hass.data[KNOWN_CHROMECAST_INFO_KEY].values():
        await async_cast_discovered(chromecast)

class GoogleHomeDeviceScanner(DeviceScanner):
    """This class queries a Google Home unit."""

    def __init__(self, hass, client, config, device, async_see):
        """Initialize the scanner."""
        self.async_see = async_see
        self.hass = hass
        self.rssi = config[CONF_RSSI_THRESHOLD]
        self.device_types = config[CONF_DEVICE_TYPES]
        self.host = device.host
        self.client = client
        self.config_entry = config

    async def async_init(self):
        """Further initialize connection to Google Home."""
        await self.client.update_info(self.host)
        data = self.hass.data[DOMAIN][self.host]
        info = data.get("info", {})
        connected = bool(info)
        if connected:
            await self.async_update()
            async_track_time_interval(
                self.hass, self.async_update, DEFAULT_SCAN_INTERVAL
            )
        return connected

    async def async_update(self, now=None):
        """Ensure the information from Google Home is up to date."""
        _LOGGER.debug("Checking Devices on %s", self.host)
        await self.client.update_bluetooth(self.host, self.config_entry)
        data = self.hass.data[DOMAIN][self.host]
        info = data.get("info")
        bluetooth = data.get("bluetooth")
        if info is None or bluetooth is None:
            return
        google_home_name = info.get("name", NAME)

        for device in bluetooth:
            if (
                device["device_type"] not in self.device_types
                or device["rssi"] < self.rssi
            ):
                continue

            name = "{} {}".format(self.host, device["mac_address"])

            attributes = {}
            attributes["btle_mac_address"] = device["mac_address"]
            attributes["ghname"] = google_home_name
            attributes["rssi"] = device["rssi"]
            attributes["source_type"] = "bluetooth"
            if device["name"]:
                attributes["name"] = device["name"]

            await self.async_see(dev_id=slugify(name), attributes=attributes)
