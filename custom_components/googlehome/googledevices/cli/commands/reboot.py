"""Reboot a Google device."""
from googledevices.helpers import gdh_session


def reboot(host, loop):
    """Reboot a Google device."""

    async def reboot_device(host, loop):
        """Reboot a Google Home unit."""
        from googledevices.api.cast.settings import Settings

        async with gdh_session() as session:
            googledevices = Settings(host, loop, session)
            await googledevices.reboot()

    loop.run_until_complete(reboot_device(host, loop))
