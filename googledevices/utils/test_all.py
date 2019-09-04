"""Test all connections."""
from ..api.connect import Cast, Wifi
from ..helpers import gdh_session, gdh_loop, gdh_sleep
from .convert import format_json


TEST_HOST_CAST = "192.168.2.241"
TEST_HOST_WIFI = "192.168.2.1"
LOOP = gdh_loop()


async def test_all():  # pylint: disable=R0915
    """Test all."""
    print("Testing Cast.")

    print("Testing Cast - Assistant.")

    async with gdh_session() as session:
        print("Testing Cast - Assistant - get_alarms")
        test_class = await Cast(TEST_HOST_CAST, LOOP, session).assistant()
        test = await test_class.get_alarms()
        print(format_json(test))

        print("Testing Cast - Assistant - set_alarm_volume")
        test_class = await Cast(TEST_HOST_CAST, LOOP, session).assistant()
        test = await test_class.set_alarm_volume(0.6)
        print(format_json(test))

        print("Testing Cast - Assistant - get_alarm_volume")
        test_class = await Cast(TEST_HOST_CAST, LOOP, session).assistant()
        test = await test_class.get_alarm_volume()
        print(format_json(test))

        print("Testing Cast - Assistant - set_night_mode_params")
        test_class = await Cast(TEST_HOST_CAST, LOOP, session).assistant()
        data = {}
        test = await test_class.set_night_mode_params(data)
        print(format_json(test))

        print("Testing Cast - Assistant - notifications_enabled")
        test_class = await Cast(TEST_HOST_CAST, LOOP, session).assistant()
        test = await test_class.notifications_enabled()
        print(format_json(test))

        print("Testing Cast - Assistant - set_accessibility")
        test_class = await Cast(TEST_HOST_CAST, LOOP, session).assistant()
        test = await test_class.set_accessibility()
        print(format_json(test))

        print("Testing Cast - Assistant - delete_alarms")
        test_class = await Cast(TEST_HOST_CAST, LOOP, session).assistant()
        data = []
        test = await test_class.delete_alarms(data)
        print(format_json(test))

        print("Testing Cast - Assistant - set_equalizer")
        test_class = await Cast(TEST_HOST_CAST, LOOP, session).assistant()
        test = await test_class.set_equalizer()
        print(format_json(test))

        print("Testing Cast - Bluetooth.")

        print("Testing Cast - Bluetooth - get_bluetooth_status")
        test_class = await Cast(TEST_HOST_CAST, LOOP, session).bluetooth()
        test = await test_class.get_bluetooth_status()
        print(format_json(test))

        print("Testing Cast - Bluetooth - set_discovery_enabled")
        test_class = await Cast(TEST_HOST_CAST, LOOP, session).bluetooth()
        test = await test_class.set_discovery_enabled()
        print(format_json(test))

        print("Testing Cast - Bluetooth - scan_for_devices")
        test_class = await Cast(TEST_HOST_CAST, LOOP, session).bluetooth()
        test = await test_class.scan_for_devices()
        print(format_json(test))

        await gdh_sleep(2)

        print("Testing Cast - Bluetooth - get_scan_result")
        test_class = await Cast(TEST_HOST_CAST, LOOP, session).bluetooth()
        test = await test_class.get_scan_result()
        print(format_json(test))

        print("Testing Cast - Bluetooth - get_paired_devices")
        test_class = await Cast(TEST_HOST_CAST, LOOP, session).bluetooth()
        test = await test_class.get_paired_devices()
        print(format_json(test))

        print("Testing Cast - Bluetooth - pair_with_mac")
        test_class = await Cast(TEST_HOST_CAST, LOOP, session).bluetooth()
        test = await test_class.pair_with_mac("AA:BB:CC:DD:EE:FF")
        print(format_json(test))

        print("Testing Cast - Bluetooth - forget_paired_device")
        test_class = await Cast(TEST_HOST_CAST, LOOP, session).bluetooth()
        test = await test_class.forget_paired_device("AA:BB:CC:DD:EE:FF")
        print(format_json(test))

        print("Testing Cast - Info.")

        print("Testing Cast - Info - get_device_info")
        test_class = await Cast(TEST_HOST_CAST, LOOP, session).info()
        test = await test_class.get_device_info()
        print(format_json(test))

        print("Testing Cast - Info - get_offer")
        test_class = await Cast(TEST_HOST_CAST, LOOP, session).info()
        test = await test_class.get_offer()
        print(format_json(test))

        print("Testing Cast - Info - get_timezones")
        test_class = await Cast(TEST_HOST_CAST, LOOP, session).info()
        test = await test_class.get_timezones()
        print(format_json(test))

        print("Testing Cast - Info - get_locales")
        test_class = await Cast(TEST_HOST_CAST, LOOP, session).info()
        test = await test_class.get_locales()
        print(format_json(test))

        print("Testing Cast - Info - speedtest")
        test_class = await Cast(TEST_HOST_CAST, LOOP, session).info()
        test = await test_class.speedtest()
        print(format_json(test))

        print("Testing Cast - Info - get_app_device_id")
        test_class = await Cast(TEST_HOST_CAST, LOOP, session).info()
        test = await test_class.get_app_device_id()
        print(format_json(test))

        print("Testing Cast - Wifi.")

        print("Testing Cast - Wifi - get_configured_networks")
        test_class = await Cast(TEST_HOST_CAST, LOOP, session).wifi()
        test = await test_class.get_configured_networks()
        print(format_json(test))

        print("Testing Cast - Wifi - scan_for_wifi")
        test_class = await Cast(TEST_HOST_CAST, LOOP, session).wifi()
        test = await test_class.scan_for_wifi()
        print(format_json(test))

        await gdh_sleep(2)

        print("Testing Cast - Wifi - get_wifi_scan_result")
        test_class = await Cast(TEST_HOST_CAST, LOOP, session).wifi()
        test = await test_class.get_wifi_scan_result()
        print(format_json(test))

        print("Testing Cast - Wifi - forget_network")
        test_class = await Cast(TEST_HOST_CAST, LOOP, session).wifi()
        test = await test_class.forget_network(9)
        print(format_json(test))

        print("Testing Cast - Settings.")

        print("Testing Cast - Settings - control_notifications")
        test_class = await Cast(TEST_HOST_CAST, LOOP, session).settings()
        test = await test_class.control_notifications(True)
        print(format_json(test))

        print("Testing Cast - Settings - set_eureka_info")
        test_class = await Cast(TEST_HOST_CAST, LOOP, session).settings()
        data = {"settings": {"control_notifications": 2}}
        test = await test_class.set_eureka_info(data)
        print(format_json(test))

        print("Testing Cast - Settings - reboot")
        test_class = await Cast(TEST_HOST_CAST, LOOP, session).settings()
        test = await test_class.reboot()
        print(format_json(test))

        print("Testing WiFi.")

        print("Testing WiFi - Info.")

        print("Testing WiFi - Info - get_host")
        test_class = await Wifi(TEST_HOST_WIFI, LOOP, session).info()
        test = await test_class.get_host()
        print(format_json(test))

        print("Testing WiFi - Info - get_host - with host not defined.")
        test_class = await Wifi(loop=LOOP, session=session).info()
        test = await test_class.get_host()
        print(format_json(test))

        print("Testing WiFi - Info - get_wifi_info")
        test_class = await Wifi(TEST_HOST_WIFI, LOOP, session).info()
        test = await test_class.get_wifi_info()
        print(format_json(test))

        print("Testing WiFi - Clients.")

        print("Testing WiFi - Clients - get_clients")
        test_class = await Wifi(TEST_HOST_WIFI, LOOP, session).clients()
        test = await test_class.get_clients()
        print(format_json(test))

        print("TESTS COMPLETE.")


LOOP.run_until_complete(test_all())
