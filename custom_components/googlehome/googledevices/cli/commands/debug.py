"""Get debug information."""
from googledevices.helpers import gdh_session


def debug(host, loop, test, timeout):
    """Get debug information."""
    from googledevices.utils.debug import Debug

    async def connectivity():
        """Test connectivity a Google Home unit."""
        async with gdh_session():
            googledevices = Debug(host)
            await googledevices.connectivity(timeout)

    if test == "connectivity":
        loop.run_until_complete(connectivity())
