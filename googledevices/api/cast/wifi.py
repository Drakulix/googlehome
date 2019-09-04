"""Wifi handling on Google Home units."""
from ...helpers import gdh_request
from ...utils.const import HEADERS, CASTSECPORT
from ...utils import log


class Wifi(object):
    """A class for Wifi."""

    def __init__(self, host, loop, session):
        """Initialize the class."""
        self.loop = loop
        self.host = host
        self.session = session
        self._configured_networks = None
        self._nearby_networks = None

    async def get_configured_networks(self, token):
        """Get the configured networks of the device."""
        endpoint = "setup/configured_networks"
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
        self._configured_networks = response
        log.debug(self._configured_networks)
        return self._configured_networks

    async def get_wifi_scan_result(self, token):
        """Get the result of a wifi scan."""
        endpoint = "setup/configured_networks"
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
        self._configured_networks = response
        log.debug(self._configured_networks)
        return self._configured_networks

    async def scan_for_wifi(self, token):
        """Scan for nearby wifi networks."""
        endpoint = "setup/scan_wifi"
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

    async def forget_network(self, token, wpa_id):
        """Forget a network."""
        endpoint = "setup/forget_wifi"
        returnvalue = False
        data = {"wpa_id": int(wpa_id)}
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
    def configured_networks(self):
        """Return the configured networks of the device."""
        return self._configured_networks

    @property
    def nearby_networks(self):
        """Return the nearby networks of the device."""
        return self._nearby_networks
