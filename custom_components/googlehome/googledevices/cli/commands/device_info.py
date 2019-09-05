"""Get information about a Google device on your network."""
from googledevices.helpers import gdh_session
from googledevices.utils.convert import format_json


def device_info(host, loop):
    """Get information about a Google device on your network."""
    from googledevices.api.cast.info import Info

    async def get_device_info():
        """Get device info."""
        async with gdh_session() as session:
            googledevices = Info(host, loop, session)
            await googledevices.get_device_info()
            print(format_json(googledevices.device_info))

    loop.run_until_complete(get_device_info())
