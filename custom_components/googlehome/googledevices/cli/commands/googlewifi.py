"""Get information from Google WiFi."""
from googledevices.api.connect import Wifi
from googledevices.helpers import gdh_session
from googledevices.utils.convert import format_json


def get_wifi_info(host, loop):
    """Get information from Google WiFi."""

    async def info():
        """Get information from Google WiFi."""
        async with gdh_session() as session:
            googledevices = await Wifi(host=host, loop=loop, session=session).info()
            await googledevices.get_wifi_info()
        print(format_json(googledevices.wifi_info))

    loop.run_until_complete(info())


def get_wifi_clients(host, loop, show):
    """Get clients from Google WiFi."""

    async def clients():
        """Get information from Google WiFi."""
        async with gdh_session() as session:
            googledevices = await Wifi(host=host, loop=loop, session=session).clients()
            print("This command will take some time to finish.")
            await googledevices.get_clients()
        if show == "mac":
            clients = []
            for client in googledevices.clients:
                clients.append(client["mac"])
        elif show == "ip":
            clients = []
            for client in googledevices.clients:
                clients.append(client["ip"])
        else:
            clients = googledevices.clients
        print(format_json(clients))

    loop.run_until_complete(clients())
