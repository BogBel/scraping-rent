import abc
import asyncio
import logging

import aiohttp

import settings


class BaseScrap:
    @abc.abstractmethod
    def run(self):
        raise NotImplementedError

async def async_request(url, headers=None, loop=None):
    """
    Async request
    :param url: url for get request
    :param headers: if required pass dict
    :param loop: asyncio.event_loop
    """
    error = None
    logging.debug(url)
    for _ in range(settings.REQUEST_MAX_RETRIES):
        try:
            with aiohttp.Timeout(settings.REQUEST_TIMEOUT, loop=loop):
                async with aiohttp.ClientSession(loop=loop) as session:
                    async with session.get(url=url, headers=headers) as response:
                        return await response.text()
        except (aiohttp.errors.ClientError,
                asyncio.TimeoutError,
                aiohttp.errors.DisconnectedError,
                aiohttp.errors.HttpProcessingError) as e:
            error = repr(e)
        await asyncio.sleep(settings.REQUEST_COOLDOWN, loop=loop)
    logging.error('Cant get response from {} cause: {}'.format(url, error))
    return None
