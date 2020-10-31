"""Support for Google Home alarm sensor."""
from datetime import timedelta
import logging

from homeassistant.const import DEVICE_CLASS_TIMESTAMP
from homeassistant.helpers.entity import Entity
import homeassistant.util.dt as dt_util

# borrow some cast functionality
from homeassistant.components.cast.const import (
    SIGNAL_CAST_DISCOVERED,
    SIGNAL_CAST_REMOVED,
    KNOWN_CHROMECAST_INFO_KEY,
    DOMAIN as CAST_DOMAIN,
)
from homeassistant.components.cast.helpers import ChromecastInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import CLIENT, DOMAIN, NAME

SCAN_INTERVAL = timedelta(seconds=10)

_LOGGER = logging.getLogger(__name__)

ICON = "mdi:alarm"

SENSOR_TYPES = {"timer": "Timer", "alarm": "Alarm"}

active_devices = {}

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the googlehome sensor platform."""

    async def async_cast_discovered(discover: ChromecastInfo):
        if discover.is_audio_group():
            return
        hass.data[DOMAIN].setdefault(discover.host, {})

        if await hass.data[CLIENT].update_info(discover.host):
            info = hass.data[DOMAIN][discover.host]["info"]
            if info["device_info"]["cloud_device_id"] not in active_devices and info["device_info"]["capabilities"].get("assistant_supported", False):
                devices = []
                for condition in SENSOR_TYPES:
                    device = GoogleHomeAlarm(
                        hass.data[CLIENT],
                        config_entry,
                        condition,
                        discover,
                        info.get("name", NAME),
                        info["device_info"]["cloud_device_id"]
                    )
                    devices.append(device)
                active_devices[info["device_info"]["cloud_device_id"]] = devices
                async_add_entities(devices, True)

    async def async_cast_removed(info: ChromecastInfo):
        if info["device_info"]["cloud_device_id"] in active_devices:
            for entity in active_devices[info["device_info"]["cloud_device_id"]]:
                await entity.async_remove()
            del active_devices[info["device_info"]["cloud_device_id"]]

    async_dispatcher_connect(hass, SIGNAL_CAST_REMOVED, async_cast_removed)
    async_dispatcher_connect(hass, SIGNAL_CAST_DISCOVERED, async_cast_discovered)
    for chromecast in hass.data[KNOWN_CHROMECAST_INFO_KEY].values():
        await async_cast_discovered(chromecast)

class GoogleHomeAlarm(Entity):
    """Representation of a GoogleHomeAlarm."""

    def __init__(self, client, config_entry, condition, device, name, cloud_device_id):
        """Initialize the GoogleHomeAlarm sensor."""
        self._host = device.host
        self._device = device
        self._client = client
        self._config_entry = config_entry
        self._condition = condition
        self._name = None
        self._state = None
        self._available = True
        self._name = "{} {}".format(name, SENSOR_TYPES[self._condition])
        self._unique_id = cloud_device_id + '_' + condition

    async def async_update(self):
        """Update the data."""
        await self._client.update_alarms(self._host, self._config_entry)
        data = self.hass.data[DOMAIN][self._host]

        alarms = data.get("alarms", {})
        if self._condition not in alarms or not alarms[self._condition]:
            self._available = False
            return
        self._available = True
        time_date = dt_util.utc_from_timestamp(
            min(element["fire_time"] for element in alarms[self._condition]) / 1000
        )
        self._state = time_date.isoformat()

    @property
    def state(self):
        """Return the state."""
        return self._state

    @property
    def name(self):
        """Return the name."""
        return self._name

    @property
    def device_class(self):
        """Return the device class."""
        return DEVICE_CLASS_TIMESTAMP

    @property
    def device_info(self):
        """Return information about the device."""
        cast_info = self._device

        if cast_info.model_name == "Google Cast Group":
            return None

        return {
            "name": cast_info.friendly_name,
            "identifiers": {(CAST_DOMAIN, cast_info.uuid.replace("-", ""))},
            "model": cast_info.model_name,
            "manufacturer": cast_info.manufacturer,
        }
    
    @property
    def unique_id(self):
        """Return the unique_id of the device."""
        return self._unique_id

    @property
    def available(self):
        """Return the availability state."""
        return self._available

    @property
    def icon(self):
        """Return the icon."""
        return ICON
