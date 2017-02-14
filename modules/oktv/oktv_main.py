import asyncio
from multiprocessing import Process
from lxml import html

from modules.oktv.constants import REQUEST_HEADERS
from tools.basic import BaseScrap, async_request


class OkTvProcessor(BaseScrap):
    def __init__(self, m_dict):
        self.multiprocessing_dict = m_dict
        self.loop = asyncio.new_event_loop()

    async def _collect_urls(self):
        print(1111111111111111111111)
        response = await async_request('https://oktv.ua/kievskaya-oblast/kiev', headers=REQUEST_HEADERS, loop=self.loop)
        tree = html.fromstring(response)
        hrefs = [link.get('href') for link in tree.xpath('//div[@class="object_v_spiske"]/div/a')]
        from pprint import pprint
        pprint(hrefs)

    async def proceed(self):
        await self._collect_urls()

    def run(self):
        self.loop.run_until_complete(self.proceed())
        self.multiprocessing_dict['ok_tv'] = {'data': True}


def run_module(m_dict):
    ok_tv_runner = OkTvProcessor(m_dict)
    process = Process(target=ok_tv_runner.run)
    return process
