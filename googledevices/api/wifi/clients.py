"""Get clients connected to the network."""
from ..wifi.info import Info
from ...utils.const import API, WIFIAPIPREFIX
from ...utils import log


class Clients(object):
    """A class for devices."""

    def __init__(self, host=None, loop=None, session=None):
        """Initialize the class."""
        self.session = session
        self.loop = loop
        self.host = host
        self._wifi_host = None
        self._clients = []
        self.info = Info(host=self.host, loop=self.loop, session=self.session)

    async def get_clients(self):
        """Return clients form the network."""
        import requests
        import asyncio
        import aiohttp
        from socket import gaierror

        self._clients = []
        if self.info.wifi_host is None:
            async with self.session:
                await self.info.get_host()
        if self.info.wifi_host is None:
            await log.error("Host is 'None', host can not be 'None'")
            return self._clients
        endpoint = WIFIAPIPREFIX + "diagnostic-report"
        url = API.format(schema="http", host=self.info.wifi_host, port=":80", endpoint=endpoint)
        try:
            response = requests.request("GET", url)
            all_clients = response.text
            all_clients = all_clients.split("/proc/net/arp")[1]
            all_clients = all_clients.split("/proc/slabinfo")[0]
            all_clients = all_clients.splitlines()
            for device in all_clients[1:-2]:
                host = device.split()[0]
                mac = device.split()[3]
                info = {"ip": host, "mac": mac}
                self._clients.append(info)
        except (TypeError, KeyError, IndexError) as error:
            msg = "Error parsing information - {}".format(error)
            log.error(msg)
        except (
            asyncio.TimeoutError,
            aiohttp.ClientError,
            gaierror,
            asyncio.CancelledError,
        ) as error:
            msg = "{} - {}".format(url, error)
            log.error(msg)
        except Exception as error:  # pylint: disable=W0703
            log.error(error)
        return self._clients

    @property
    def clients(self):
        """Return devices form the network."""
        return self._clients
