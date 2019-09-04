"""Example usage of googledevices."""
from googledevices.helpers import gdh_session
from googledevices.api.cast.assistant import Assistant


def alarm_volume(host, loop, mode, volume=None):
    """Handle alarm volume."""

    async def set_alarm_volume():
        """Get alarms and timers from GH."""
        async with gdh_session() as session:
            googledevices = Assistant(host, loop, session)
            await googledevices.set_alarm_volume(volume)

    async def get_alarm_volume():
        """Get alarms and timers from GH."""
        async with gdh_session() as session:
            googledevices = Assistant(host, loop, session)
            await googledevices.get_alarm_volume()
            print("Volume:", googledevices.alarm_volume)

    if mode == "set":
        if volume is None:
            print("You need to supply a volume like '--volume 0.8'")
            return
        loop.run_until_complete(set_alarm_volume())
    else:
        loop.run_until_complete(get_alarm_volume())
