"""Get Google devices on the local network."""
import socket
import ipaddress
from ..api.cast.info import Info as CastInfo
from ..api.wifi.info import Info as WifiInfo
from .const import CASTPORT
from ..helpers import gdh_session


class NetworkScan(object):
    """A class nettwork scan."""

    def __init__(self, loop, session):
        """Initialize the class."""
        self.session = session
        self.loop = loop

    async def scan_for_units(self, iprange):
        """Scan local network for Google devices."""
        units = []
        async with gdh_session() as session:
            googlewifi = WifiInfo(loop=self.loop, session=session)
            await googlewifi.get_wifi_info()
        if googlewifi.wifi_host is not None:
            wifi = {
                "assistant": False,
                "bluetooth": False,
                "host": googlewifi.wifi_host,
                "model": googlewifi.wifi_info.get("system", {}).get("modelId"),
                "name": "Google WiFi",
            }
            units.append(wifi)
        for host in ipaddress.IPv4Network(iprange):
            sock = socket.socket()
            sock.settimeout(0.2)
            host = str(host)
            try:
                scan_result = sock.connect((host, CASTPORT))
            except socket.error:
                scan_result = 1
            if scan_result is None:
                async with gdh_session() as session:
                    googledevices = CastInfo(host, self.loop, session)
                    await googledevices.get_device_info()
                data = googledevices.device_info
                if data is not None:
                    info = data.get("device_info", {})
                    cap = info.get("capabilities", {})
                    units.append(
                        {
                            "host": host,
                            "name": data.get("name"),
                            "model": info.get("model_name"),
                            "assistant": cap.get("assistant_supported", False),
                            "bluetooth": cap.get("bluetooth_supported", False),
                        }
                    )
            sock.close()
        return units
