"""Get device information for the unit."""
from ...helpers import gdh_request, gdh_session, gdh_loop
from ...utils.const import WIFIAPIPREFIX, WIFIHOSTS, API
from ...utils import log


class Info(object):
    """A class for device info."""

    def __init__(self, host=None, loop=None, session=None):
        """Initialize the class."""
        self.session = session
        self.loop = loop
        self.endpoint = WIFIAPIPREFIX + "status"
        self.host = host
        self._wifi_host = None
        self._wifi_info = {}
        self._devices = []

    async def get_host(self):
        """Get the hostname/IP of the WiFi unit."""
        if self.host is not None:
            self._wifi_host = self.host
        else:
            import async_timeout

            for host in WIFIHOSTS:
                try:
                    if self.loop is None:
                        self.loop = gdh_loop()
                    if self.session is None:
                        self.session = gdh_session()
                    url = API.format(schema="http", host=host, port="", endpoint=self.endpoint)
                    async with async_timeout.timeout(5, loop=self.loop):
                        await self.session.get(url)
                        self._wifi_host = host
                        return self._wifi_host
                # pylint: disable=W0703
                except Exception:
                    self._wifi_host = self._wifi_host
        return self._wifi_host

    async def get_wifi_info(self):
        """Get the Wi-Fi status of the device."""
        if self.wifi_host is None:
            await self.get_host()
        try:
            response = await gdh_request(
                host=self.wifi_host,
                endpoint=self.endpoint,
                session=self.session,
                loop=self.loop,
            )
            self._wifi_info = response
        # pylint: disable=W0703
        except Exception as error:  # pylint: disable=W0703
            log.error(error)
        return self._wifi_info

    @property
    def wifi_host(self):
        """Return the hostname or IP of the device."""
        return self._wifi_host

    @property
    def wifi_info(self):
        """Return the device info if any."""
        return self._wifi_info
