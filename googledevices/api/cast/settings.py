"""Controll device settings on the unit."""
from ...utils.const import CASTSECPORT, HEADERS
from ...helpers import gdh_request
from ...utils import log


class Settings(object):
    """A class for device settings."""

    def __init__(self, host, loop, session):
        """Initialize the class."""
        self.host = host
        self.loop = loop
        self.session = session

    async def reboot(self, token, mode="now"):
        """Reboot the device."""
        endpoint = "setup/reboot"
        supported_modes = ["now", "fdr"]
        returnvalue = False
        if mode not in supported_modes:
            log_msg = "Mode {} is not supported.".format(mode)
            log.error(log_msg)
            return returnvalue
        data = {"params": mode}
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

    async def set_eureka_info(self, token, data):
        """Set eureka info."""
        endpoint = "setup/set_eureka_info"
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

    async def control_notifications(self, token, active):
        """Set control_notifications option."""
        endpoint = "setup/set_eureka_info"
        value = 1 if active else 2
        data = {"settings": {"control_notifications": value}}
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
