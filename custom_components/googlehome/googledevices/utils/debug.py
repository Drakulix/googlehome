"""Tools to debug with."""
import socket
import asyncio
import time
from .const import CASTPORT


class Debug(object):
    """A class for debug."""

    def __init__(self, host):
        """Initialize the class."""
        self.host = host

    async def connectivity(self, timeout):
        """Test connectivity."""
        host = str(self.host)
        stop_timeout = time.time() + timeout
        while True:  # Yes I know this is bad...
            if time.time() > stop_timeout:
                try:
                    sock = socket.socket()
                    sock.settimeout(0.02)
                    scan_result = sock.connect((host, CASTPORT))
                    sock.close()
                except socket.error:
                    scan_result = 1
                now = time.time()
                if scan_result is None:
                    print(now, "- OK")
                else:
                    print(now, "- ERROR")
                asyncio.sleep(1)
