"""Googledevices helpers.

All methods are prefixed with 'gdh_' for (GoogleDevicesHelpers).
"""


def gdh_loop():
    """Asyncio loop."""
    from asyncio import get_event_loop

    return get_event_loop()


def gdh_session():
    """Aiohttp clientsession."""
    from aiohttp import ClientSession

    return ClientSession()


async def gdh_sleep(seconds=5):
    """Asyncio sleep."""
    from asyncio import sleep

    await sleep(seconds)


async def gdh_request(
    host,
    schema=None,
    port=None,
    token=None,
    endpoint=None,
    json=True,
    session=None,
    loop=None,
    headers=None,
    data=None,
    json_data=None,
    params=None,
    method="get",
):
    """Web request."""
    import asyncio
    import aiohttp
    import async_timeout
    from socket import gaierror
    from .utils.const import API
    from .utils import log

    if schema is None:
        schema = "http"
    if port is not None:
        port = ":{port}".format(port=port)
    else:
        port = ""
    url = API.format(schema=schema, host=host, port=port, endpoint=endpoint)
    result = None
    if token is not None:
        if headers is None:
            headers = {}
        headers["cast-local-authorization-token"] = token

    if session is None:
        session = gdh_session()
    if loop is None:
        loop = gdh_loop()
    try:
        async with async_timeout.timeout(8, loop=loop):
            if method == "post":
                webrequest = await session.post(
                    url, json=json_data, data=data, params=params, headers=headers, ssl=False
                )
            else:
                webrequest = await session.get(
                    url, json=json_data, data=data, params=params, headers=headers, ssl=False
                )
            if json:
                result = await webrequest.json()
            else:
                result = webrequest
    except (TypeError, KeyError, IndexError) as error:
        log.error("Error parsing information - {}".format(error))
    except asyncio.TimeoutError:
        log.error("Timeout contacting {}".format(url))
    except asyncio.CancelledError:
        log.error("Cancellation error contacting {}".format(url))
    except aiohttp.ClientError as error:
        log.error("ClientError contacting {} - {}".format(url, error))
    except gaierror as error:
        log.error("I/O error contacting {} - {}".format(url, error))
    except Exception as error:  # pylint: disable=W0703
        log.error("Unexpected error contacting {} - {}".format(url, error))
    return result
