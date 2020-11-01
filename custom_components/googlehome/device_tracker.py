"""Support for Google Home Bluetooth tacker."""
from datetime import timedelta
import logging
from pychromecast.socket_client import (
    CONNECTION_STATUS_CONNECTED,
    CONNECTION_STATUS_DISCONNECTED,
)

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
from .helpers import ChromecastMonitor


_LOGGER = logging.getLogger(__name__)

DEFAULT_SCAN_INTERVAL = timedelta(seconds=10)

monitors = []
async def async_setup_entry(hass, config_entry, async_see):
    """Setup the Google Home scanner platform"""
    monitor = DeviceTrackerMonitor()
    await monitor.async_init(hass, config_entry, async_see)
    monitors.append(monitor)

class DeviceTrackerMonitor(ChromecastMonitor):
    async def async_init(self, hass, config_entry, async_see):
        self._config_entry = config_entry
        self._async_see = async_see
        await super().async_init(hass)

    async def supported(self, discover: ChromecastInfo) -> bool:
        info = self._hass.data[DOMAIN][discover.uuid]["info"]
        return info["device_info"]["capabilities"].get("bluetooth_supported", False)

    async def setup(self, discover: ChromecastInfo):
        scanner = GoogleHomeDeviceScanner(
            self._hass, self._hass.data[CLIENT], self._config_entry, discover, self._async_see
        )
        await scanner.async_init()
        return [scanner]

    async def cleanup(self, discover):
        info = self._hass.data[DOMAIN][discover]["info"]
        for entity in self._active_devices[info["device_info"]["cloud_device_id"]]:
            await entity.async_deinit()


class GoogleHomeDeviceScanner():
    """This class queries a Google Home unit."""

    def __init__(self, hass, client, config, device, async_see):
        """Initialize the scanner."""
        self.async_see = async_see
        self.hass = hass
        self.rssi = config.options.get(CONF_RSSI_THRESHOLD, DEFAULT_RSSI_THRESHOLD),
        self.device_types = config.options.get(CONF_DEVICE_TYPES, DEFAULT_DEVICE_TYPES),
        self.host = device.host
        self.uuid = device.uuid
        self.name = device.friendly_name
        self.client = client
        self.config_entry = config
        self.removal = None
        self.active = True

    def new_connection_status(self, connection_status):
        if connection_status == CONNECTION_STATUS_CONNECTED:
            self.active = True
        elif connection_status == CONNECTION_STATUS_DISCONNECTED:
            self.active = False

    async def async_init(self):
        """Further initialize connection to Google Home."""
        data = self.hass.data[DOMAIN][self.uuid]
        info = data.get("info", {})
        await self.async_update()
        self.removal = async_track_time_interval(
            self.hass, self.async_update, DEFAULT_SCAN_INTERVAL
        )
        self.active = True

    async def async_deinit(self):
        if self.removal:
            self.removal()
        self.removal = None
        self.active = False

    async def async_remove(self):
        self.async_deinit()

    async def async_update(self, now=None):
        """Ensure the information from Google Home is up to date."""
        if not self.active:
            return

        _LOGGER.debug("Checking Devices on %s", self.host)
        await self.client.update_bluetooth(self.host, self.uuid, self.config_entry)
        data = self.hass.data[DOMAIN][self.uuid]
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
