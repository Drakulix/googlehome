"""Support for Google Home Bluetooth tacker."""
from datetime import timedelta
import logging

from homeassistant.components.device_tracker import DeviceScanner
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.util import slugify

# borrow some cast functionality
from homeassistant.components.cast.const import (
    SIGNAL_CAST_DISCOVERED,
    SIGNAL_CAST_REMOVED,
    KNOWN_CHROMECAST_INFO_KEY,
)
from homeassistant.components.cast.helpers import ChromecastInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import CLIENT, DOMAIN, NAME, CONF_RSSI_THRESHOLD, CONF_DEVICE_TYPES, DEFAULT_RSSI_THRESHOLD, DEFAULT_DEVICE_TYPES

_LOGGER = logging.getLogger(__name__)

DEFAULT_SCAN_INTERVAL = timedelta(seconds=10)

active_devices = {}

async def async_setup_entry(hass, config_entry, async_see):
    """Setup the Google Home scanner platform"""
    async def async_cast_discovered(discover: ChromecastInfo):
        if discover.is_audio_group:
            return
        hass.data[DOMAIN].setdefault(discover.host, {})

        if await hass.data[CLIENT].update_info(discover.host):
            info = hass.data[DOMAIN][discover.host]["info"]
            if info["device_info"]["cloud_device_id"] not in active_devices and info["device_info"]["capabilities"].get("bluetooth_supported", False):
                scanner = GoogleHomeDeviceScanner(
                    hass, hass.data[CLIENT], config_entry, discover, async_see
                )
                active_devices[info["device_info"]["cloud_device_id"]] = scanner
                await scanner.async_init()

    async def async_cast_removed(info: ChromecastInfo):
        if info["device_info"]["cloud_device_id"] in active_devices:
            await active_devices[info["device_info"]["cloud_device_id"]].async_deinit()
            del active_devices[info["device_info"]["cloud_device_id"]]

    async_dispatcher_connect(hass, SIGNAL_CAST_REMOVED, async_cast_removed)
    async_dispatcher_connect(hass, SIGNAL_CAST_DISCOVERED, async_cast_discovered)
    for chromecast in hass.data[KNOWN_CHROMECAST_INFO_KEY].values():
        await async_cast_discovered(chromecast)

class GoogleHomeDeviceScanner():
    """This class queries a Google Home unit."""

    def __init__(self, hass, client, config, device, async_see):
        """Initialize the scanner."""
        self.async_see = async_see
        self.hass = hass
        self.rssi = config.options.get(CONF_RSSI_THRESHOLD, DEFAULT_RSSI_THRESHOLD),
        self.device_types = config.options.get(CONF_DEVICE_TYPES, DEFAULT_DEVICE_TYPES),
        self.host = device.host
        self.name = device.friendly_name
        self.client = client
        self.config_entry = config
        self.removal = None

    async def async_init(self):
        """Further initialize connection to Google Home."""
        data = self.hass.data[DOMAIN][self.host]
        info = data.get("info", {})
        await self.async_update()
        self.removal = self.async_track_time_interval(
            self.hass, self.async_update, DEFAULT_SCAN_INTERVAL
        )

    async def async_deinit(self):
        if self.removal:
            self.removal()
        self.removal = None

    async def async_update(self, now=None):
        """Ensure the information from Google Home is up to date."""
        _LOGGER.debug("Checking Devices on %s", self.host)
        await self.client.update_bluetooth(self.host, self.config_entry)
        data = self.hass.data[DOMAIN][self.host]
        info = data.get("info")
        bluetooth = data.get("bluetooth")
        if info is None or bluetooth is None:
            return

        for device in bluetooth:
            if (
                device["device_type"] not in self.device_types
                or device["rssi"] < self.rssi
            ):
                continue

            name = "{} {}".format(self.host, device["mac_address"])

            attributes = {}
            attributes["btle_mac_address"] = device["mac_address"]
            attributes["ghname"] = self.name
            attributes["rssi"] = device["rssi"]
            attributes["source_type"] = "bluetooth"
            if device["name"]:
                attributes["name"] = device["name"]

            await self.async_see(dev_id=slugify(name), attributes=attributes)
