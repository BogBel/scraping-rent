import abc
import asyncio
import logging

import aiohttp

import settings


class BaseScrap:
    @abc.abstractmethod
    def run(self):
        raise NotImplementedError


async def async_request(url, method, return_type='text', loop=None, **kwargs):
    """
    Async request
    :param url: url for get request
    :param method: 'get' or 'post' supported
    :param return_type: 'text' or 'json'
    :param loop: asyncio.event_loop
    """
    error = None
    logging.debug(url)
    for _ in range(settings.REQUEST_MAX_RETRIES):
        try:
            with aiohttp.Timeout(settings.REQUEST_TIMEOUT, loop=loop):
                async with aiohttp.ClientSession(loop=loop) as session:
                    async with session.request(method=method, url=url, **kwargs) as response:
                        if return_type == 'text':
                            return await response.text()
                        elif return_type == 'json':
                            return await response.json()
                        else:
                            logging.warning('wrong type for request {}'.format(return_type))
                            return None
        except (aiohttp.errors.ClientError,
                asyncio.TimeoutError,
                aiohttp.errors.DisconnectedError,
                aiohttp.errors.HttpProcessingError) as e:
            error = repr(e)
        await asyncio.sleep(settings.REQUEST_COOLDOWN, loop=loop)
    logging.error('Cant get response from {} cause: {}'.format(url, error))
    return None
