"""Get bluetooth devices from a unit."""
from googledevices.utils.convert import format_json
from googledevices.helpers import gdh_session, gdh_sleep


def get_bluetooth_devices(host, loop):
    """Get bluetooth devices from a unit."""
    from googledevices.api.cast.bluetooth import Bluetooth

    async def bluetooth_scan():
        """Get nearby bluetooth devices."""
        async with gdh_session() as session:
            bluetooth = Bluetooth(host, loop, session)
            await bluetooth.scan_for_devices()
            await gdh_sleep()
            await bluetooth.get_scan_result()
            print(format_json(bluetooth.devices))

    loop.run_until_complete(bluetooth_scan())
