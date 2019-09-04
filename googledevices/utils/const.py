"""Constants."""
###############################################################################
# General
###############################################################################
API = "{schema}://{host}{port}/{endpoint}"
DEFAULT_DEVICE_NAME = "GoogleDevice"
HEADERS = {"Content-Type": "application/json", "Host": "localhost"}
PLATFORMS = ["cast", "wifi"]

###############################################################################
# Cast API
###############################################################################
CASTPORT = 8008
CASTSECPORT = 8443

###############################################################################
# WiFI API
###############################################################################
WIFIAPIPREFIX = "api/v1/"
WIFIPORT = None
WIFIHOSTS = [
    "192.168.86.1",
    "192.168.11.1",
    "192.168.2.1",
    "192.168.1.1",
    "testwifi.here",
    "onhub.here",
]

###############################################################################
# Setup information
###############################################################################
VERSION = "1.0.3"
NAME = "googledevices"
DESCRIPTION = "Get information from, and control various Google devices."
URLS = {
    "github": "https://github.com/ludeeus/googledevices",
    "pypi": "https://pypi.org/project/googledevices",
}
AUTHOR = {"name": "Joakim Sorensen", "email": "ludeeus@gmail.com"}
MAINTAINERS = [
    {
        "name": "ludeeus",
        "github": "https://github.com/ludeeus",
        "email": AUTHOR.get("email"),
    },
    {
        "name": "eliseomartelli",
        "github": "https://github.com/eliseomartelli",
        "email": "me@eliseomartelli.it",
    },
]
REQUIREMENTS = ["aiohttp", "async_timeout", "click", "netifaces", "requests"]
CLASSIFIERS = (
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
)
ENTRY_POINTS = {"console_scripts": ["googledevices = googledevices.cli.cli:CLI"]}
