"""Convert/restructure data sets."""


def get_device_type(device_type=0):
    """Return the device type from a device_type list."""
    device_types = {
        0: "Unknown",
        1: "Classic - BR/EDR devices",
        2: "Low Energy - LE-only",
        3: "Dual Mode - BR/EDR/LE",
    }
    if device_type in [1, 2, 3]:
        return_value = device_types[device_type]
    else:
        return_value = device_types[0]
    return return_value


def format_json(source):
    """Structure json."""
    from json import dumps

    return dumps(source, indent=4, sort_keys=True)
