"""Get device information for the unit."""
from ...utils.const import DEFAULT_DEVICE_NAME, CASTPORT, CASTSECPORT, HEADERS
from ...utils import log
from ...helpers import gdh_request


class Info(object):  # pylint: disable=R0902
    """A class for device info."""

    def __init__(self, host, loop, session):
        """Initialize the class."""
        self.loop = loop
        self.host = host
        self.session = session
        self._name = "GoogleDevice"
        self._device_info = {}
        self._offer = {}
        self._timezones = []
        self._locales = []
        self._app_device_id = {}

    async def get_device_info(self):
        """Get device information for the unit."""
        endpoint = "setup/eureka_info"
        params = (
            "params=version,audio,name,build_info,detail,device_info,"
            "net,wifi,setup,settings,opt_in,opencast,multizone,proxy,"
            "night_mode_params,user_eq,room_equalizer&options=detail"
        )
        response = await gdh_request(
            host=self.host,
            port=CASTPORT,
            loop=self.loop,
            session=self.session,
            endpoint=endpoint,
            params=params,
            headers=HEADERS,
        )
        self._device_info = response
        log.debug(self._device_info)
        return self._device_info

    async def get_offer(self, token):
        """Get offer token."""
        endpoint = "setup/offer"
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
        self._offer = response
        log.debug(self._offer)
        return self._offer

    async def get_timezones(self, token):
        """Get supported timezones."""
        endpoint = "setup/supported_timezones"
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
        self._timezones = response
        log.debug(self._timezones)
        return self._timezones

    async def get_locales(self, token):
        """Get supported locales."""
        endpoint = "setup/supported_locales"
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
        self._locales = response
        log.debug(self._locales)
        return self._locales

    async def speedtest(self, token):
        """Run speedtest."""
        endpoint = "setup/test_internet_download_speed"
        url = "https://storage.googleapis.com/reliability-speedtest/random.txt"
        data = {"url": url}
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

    async def get_app_device_id(self, token):
        """Run speedtest."""
        endpoint = "setup/get_app_device_id"
        data = {"app_id": "E8C28D3C"}
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

    @property
    def offer(self):
        """Return the offer token."""
        return self._offer

    @property
    def timezones(self):
        """Return supported timezones."""
        return self._timezones

    @property
    def locales(self):
        """Return supported timezones."""
        return self._locales

    @property
    def app_device_id(self):
        """Return app_device_id."""
        return self._app_device_id

    @property
    def device_info(self):
        """Return the device info if any."""
        return self._device_info

    @property
    def name(self):
        """Return the device name."""
        return self._device_info.get("name", DEFAULT_DEVICE_NAME)
