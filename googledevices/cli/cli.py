"""CLI commands."""
import click
from googledevices.helpers import gdh_loop


@click.group()
async def commands():
    """Click group."""


@commands.command("device-info")
@click.argument("host", required=1)
def device_info(host):
    """Get information about a Google device on your network."""
    import googledevices.cli.commands.device_info as command

    command.device_info(host, LOOP)


@commands.command("get-bluetooth-devices")
@click.argument("host", required=1)
def get_bluetooth_devices(host):
    """Get bluetooth devices from a unit."""
    import googledevices.cli.commands.bluetooth_devices as command

    command.get_bluetooth_devices(host, LOOP)


@commands.command("get-all-devices")
@click.option("--subnet", type=str, default=None, help="Format 0.0.0.0/00")
def get_all_devices(subnet):
    """Get information about all devices on your network."""
    import googledevices.cli.commands.all_devices as command

    command.get_all_devices(LOOP, subnet)


@commands.command("scan-network")
@click.option(
    "--network",
    "-N",
    type=str,
    default=None,
    help="The network you want to scan\
              in this format '192.168.1.0/24'.",
)
@click.option(
    "--feature",
    "-F",
    type=str,
    default=None,
    help="Filter discovery result to\
              units that contain these feature.",
)
def scan_network(network, feature):
    """Scan the entire subnet for Google devices."""
    import googledevices.cli.commands.scan_network as command

    command.scan_network(LOOP, network, feature)


@commands.command("reboot")
@click.argument("host", required=1)
def reboot(host):
    """Reboot a Google device."""
    import googledevices.cli.commands.reboot as command

    command.reboot(host, LOOP)


@commands.command("googlewifi-info")
@click.argument("host", required=0)
def get_wifi_info(host):
    """Get information about google wifi."""
    import googledevices.cli.commands.googlewifi as command

    command.get_wifi_info(host, LOOP)


@commands.command("googlewifi-clients")
@click.argument("host", required=0)
@click.option("--show", "-S", type=str, help="List only 'mac' or 'ip'")
def get_wifi_clients(host, show=None):
    """Get devices from google wifi."""
    import googledevices.cli.commands.googlewifi as command

    command.get_wifi_clients(host, LOOP, show)


@commands.command("info")
@click.option("--system", "-S", is_flag=True, help="Print more output.")
def info(system):
    """Get information about this package."""
    import googledevices.cli.commands.info as command

    command.info(system)


@commands.command("debug")
@click.argument("host", required=1)
@click.option("--test", "-T", type=str, required=1)
@click.option("--timeout", type=int)
def debug(host, test, timeout=30):
    """Get debug information."""
    import googledevices.cli.commands.debug as command

    command.debug(host, LOOP, test, timeout)


@commands.command("alarm-volume")
@click.argument("host", required=1)
@click.option("--mode", "-M", type=str, required=1, help="'get' or 'set'")
@click.option("--volume", "-V", type=float)
def alarm_volume(host, mode, volume=None):
    """Get or set alarm volume."""
    import googledevices.cli.commands.alarm_volume as command

    command.alarm_volume(host, LOOP, mode, volume)


LOOP = gdh_loop()
CLI = click.CommandCollection(sources=[commands])
