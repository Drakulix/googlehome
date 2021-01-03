"""Support for Google Home alarm sensor."""
from datetime import timedelta
import logging
import pychromecast
from pychromecast.socket_client import (
    CONNECTION_STATUS_CONNECTED,
    CONNECTION_STATUS_DISCONNECTED,
)

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
from homeassistant.components.cast.helpers import ChromecastInfo, ChromeCastZeroconf
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import CLIENT, DOMAIN, NAME, STATUS_NONE, STATUS_SET, STATUS_ACTIVE
from .helpers import ChromecastMonitor

SCAN_INTERVAL = timedelta(seconds=10)
_LOGGER = logging.getLogger(__name__)
ICON = "mdi:alarm"
SENSOR_TYPES = {"timer": "Timer", "alarm": "Alarm"}

monitors = []
async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the googlehome sensor platform."""
    monitor = SensorMonitor()
    await monitor.async_init(hass, config_entry, async_add_entities)
    monitors.append(monitor)


class SensorMonitor(ChromecastMonitor):
    async def async_init(self, hass, config_entry, async_add_entities):
        self._config_entry = config_entry
        self._async_add_entities = async_add_entities
        await super().async_init(hass)

    async def supported(self, discover: ChromecastInfo) -> bool:
        info = self._hass.data[DOMAIN][discover.uuid]["info"]
        return info["device_info"]["capabilities"].get("assistant_supported", False)

    async def setup(self, discover: ChromecastInfo):
        info = self._hass.data[DOMAIN][discover.uuid]["info"]
        devices = []
        for condition in SENSOR_TYPES:
            device = GoogleHomeAlarm(
                self._hass.data[CLIENT],
                self._config_entry,
                condition,
                discover,
                info.get("name", NAME),
                info["device_info"]["cloud_device_id"]
            )
            devices.append(device)
        self._async_add_entities(devices, True)
        return devices

    async def cleanup(self, discover):
        info = self._hass.data[DOMAIN][discover]["info"]
        for entity in self._active_devices[info["device_info"]["cloud_device_id"]]:
            await entity.async_remove()


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
        self._state = STATUS_NONE
        self._attributes = []
        self._name = "{} {}".format(name, SENSOR_TYPES[self._condition])
        self._unique_id = cloud_device_id + '_' + condition
        self._connected = True

    async def async_update(self):
        """Update the data."""
        await self._client.update_alarms(self._host, self._device.uuid, self._config_entry)
        data = self.hass.data[DOMAIN][self._device.uuid]

        alarms = data.get("alarms", {})
        if self._condition not in alarms or not alarms[self._condition]:
            self._state = STATUS_NONE
            self._attributes = []
            return

        elements = sorted(alarms[self._condition], key=lambda element: element["fire_time"])
        state = STATUS_SET if elements[0]["status"] == 1 else STATUS_ACTIVE
        attributes = [{
            "status": STATUS_SET if x["status"] == 1 else STATUS_ACTIVE,
            "fire_time": dt_util.utc_from_timestamp(x["fire_time"] / 1000).isoformat(),
        } for x in elements]

        self._attributes = { "pending": attributes }
        self._state = state

    @property
    def state(self):
        """Return the state."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return the attributes."""
        return self._attributes

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
        return self._connected

    @property
    def icon(self):
        """Return the icon."""
        return ICON

    def new_connection_status(self, connection_status):
        if connection_status == CONNECTION_STATUS_CONNECTED:
            _LOGGER.info("Disconnected")
            self._connected = True
        elif connection_status == CONNECTION_STATUS_DISCONNECTED:
            _LOGGER.info("Connected")
            self._connected = False