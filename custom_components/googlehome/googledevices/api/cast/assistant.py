"""Controll Assistant settings on the unit."""
from ...utils.const import CASTSECPORT, HEADERS
from ...helpers import gdh_request
from ...utils import log


class Assistant(object):
    """A class for Assistant settings."""

    def __init__(self, host, loop, session):
        """Initialize the class."""
        self.host = host
        self.loop = loop
        self.session = session
        self._alarms = []
        self._alarmvolume = None

    async def set_night_mode_params(self, token, data):
        """Set night mode options."""
        endpoint = "setup/assistant/set_night_mode_params"
        result = await gdh_request(
            schema="https",
            host=self.host,
            port=CASTSECPORT,
            token=token,
            endpoint=endpoint,
            method="post",
            loop=self.loop,
            session=self.session,
            json_data=data,
            headers=HEADERS,
        )
        return result

    async def notifications_enabled(self, token, mode=True):
        """Set notifications_enabled True/False."""
        endpoint = "setup/assistant/notifications"
        data = {"notifications_enabled": mode}
        result = await gdh_request(
            schema="https",
            host=self.host,
            port=CASTSECPORT,
            token=token,
            endpoint=endpoint,
            method="post",
            loop=self.loop,
            session=self.session,
            json_data=data,
            headers=HEADERS,
        )
        return result

    async def set_accessibility(self, token, start=True, end=False):
        """Set accessibility True/False."""
        endpoint = "setup/assistant/a11y_mode"
        data = {"endpoint_enabled": end, "hotword_enabled": start}
        result = await gdh_request(
            schema="https",
            host=self.host,
            port=CASTSECPORT,
            token=token,
            endpoint=endpoint,
            method="post",
            loop=self.loop,
            session=self.session,
            json_data=data,
            headers=HEADERS,
        )
        return result

    async def delete_alarms(self, token, data):
        """Delete active alarms and timers."""
        endpoint = "setup/assistant/alarms/delete"
        result = await gdh_request(
            schema="https",
            host=self.host,
            port=CASTSECPORT,
            token=token,
            endpoint=endpoint,
            method="post",
            loop=self.loop,
            session=self.session,
            json_data=data,
            headers=HEADERS,
        )
        return result

    async def set_equalizer(self, token, low_gain=0, high_gain=0):
        """Set equalizer db gain."""
        endpoint = "setup/user_eq/set_equalizer"
        returnvalue = False
        data = {
            "low_shelf": {"gain_db": low_gain},
            "high_shelf": {"gain_db": high_gain},
        }
        result = await gdh_request(
            schema="https",
            host=self.host,
            port=CASTSECPORT,
            token=token,
            endpoint=endpoint,
            method="post",
            loop=self.loop,
            session=self.session,
            json_data=data,
            headers=HEADERS,
            json=False,
        )
        try:
            if result.status == 200:
                returnvalue = True
        except AttributeError:
            msg = "Error connecting to - {}".format(self.host)
            log.error(msg)
        return returnvalue

    async def get_alarms(self, token):
        """Get the alarms from the device."""
        endpoint = "setup/assistant/alarms"
        response = await gdh_request(
            schema="https",
            host=self.host,
            port=CASTSECPORT,
            token=token,
            loop=self.loop,
            session=self.session,
            endpoint=endpoint,
            headers=HEADERS,
        )
        self._alarms = response
        log.debug(self._alarms)
        return self._alarms

    async def get_alarm_volume(self, token):
        """Get the alarm volume for the device."""
        endpoint = "setup/assistant/alarms/volume"
        response = await gdh_request(
            schema="https",
            host=self.host,
            port=CASTSECPORT,
            token=token,
            loop=self.loop,
            session=self.session,
            endpoint=endpoint,
            headers=HEADERS,
            method="post",
        )
        self._alarmvolume = response
        log.debug(self._alarmvolume)
        return self._alarmvolume

    async def set_alarm_volume(self, token, volume):
        """Set the alarm volume for the device."""
        data = {"volume": volume}
        endpoint = "setup/assistant/alarms/volume"
        returnvalue = False
        result = await gdh_request(
            schema="https",
            host=self.host,
            port=CASTSECPORT,
            token=token,
            endpoint=endpoint,
            method="post",
            loop=self.loop,
            session=self.session,
            json_data=data,
            headers=HEADERS,
            json=False,
        )
        try:
            if result.status == 200:
                returnvalue = True
        except AttributeError:
            msg = "Error connecting to - {}".format(self.host)
            log.error(msg)
        return returnvalue

    @property
    def alarms(self):
        """Return the alarms."""
        return self._alarms

    @property
    def alarm_volume(self):
        """Return the alarm volume."""
        return self._alarmvolume
