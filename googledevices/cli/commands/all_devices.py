"""Get information about all devices on your network."""
from googledevices.helpers import gdh_session, gdh_sleep
from googledevices.utils.convert import format_json


def get_all_devices(loop, subnet):
    """Get information about all devices on your network."""
    from googledevices.api.cast.bluetooth import Bluetooth
    from googledevices.utils.scan import NetworkScan
    from googledevices.api.cast.info import Info

    devices = {}

    async def get_device_info(host):
        """Grab device information."""
        async with gdh_session() as session:
            googledevices = Info(host.get("host"), loop, session)
            await googledevices.get_device_info()
            ghname = googledevices.device_info.get("name")
        async with gdh_session() as session:
            googledevices = Bluetooth(host.get("host"), loop, session)
            await googledevices.scan_for_devices()
            await gdh_sleep()
            await googledevices.get_scan_result()
            for device in googledevices.devices:
                mac = device["mac_address"]
                if not devices.get(mac, False):
                    # New device
                    devices[mac] = {}
                    devices[mac]["rssi"] = device.get("rssi")
                    devices[mac]["ghunit"] = ghname
                elif devices[mac].get("rssi") < device.get("rssi"):
                    # Better RSSI value on this device
                    devices[mac]["rssi"] = device.get("rssi")
                    devices[mac]["ghunit"] = ghname

    async def bluetooth_scan():
        """Get devices from all GH units on the network."""
        if not subnet:
            import netifaces

            gateway = netifaces.gateways().get("default", {})
            ipscope = gateway.get(netifaces.AF_INET, ())[0][:-1] + "0/24"
        else:
            ipscope = subnet
        async with gdh_session() as session:
            googledevices = NetworkScan(loop, session)
            result = await googledevices.scan_for_units(ipscope)
        for host in result:
            if host["bluetooth"]:
                await get_device_info(host)
        print(format_json(devices))

    loop.run_until_complete(bluetooth_scan())
