import asyncio
from multiprocessing import Process
from lxml import html

from modules.oktv.constants import REQUEST_HEADERS, LINKS_XPATH, CALENDAR_XPATH
from tools.basic import BaseScrap, async_request


class OkTvProcessor(BaseScrap):
    def __init__(self, m_dict):
        self.multiprocessing_dict = m_dict
        self.loop = asyncio.new_event_loop()

    @staticmethod
    def _make_state(div):
        return div.get("data-time-default"), div.get('data-busy') == 'free'

    @staticmethod
    def _is_correct_day(div):
        return 'old' not in div.get('class')

    @staticmethod
    def _get_attr(tree, xpath, attr):
        for tag in tree.xpath(xpath):
            yield tag.get(attr)

    async def _get_calendar(self, url):
        response = await async_request(url, headers=REQUEST_HEADERS, loop=self.loop)
        tree = html.fromstring(response)
        divs = filter(self._is_correct_day, tree.xpath(CALENDAR_XPATH))
        return {url: dict(map(self._make_state, divs))}

    async def _collect_urls(self):
        response = await async_request('https://oktv.ua/kievskaya-oblast/kiev', headers=REQUEST_HEADERS, loop=self.loop)
        tree = html.fromstring(response)
        hrefs = set(map('https://oktv.ua{}'.format,
                        self._get_attr(tree=tree, xpath=LINKS_XPATH, attr='href')))
        return hrefs

    async def proceed(self):
        result_data = {}
        tasks = [self._get_calendar(url) for url in await self._collect_urls()]
        for task in asyncio.as_completed(tasks, loop=self.loop):
            res = await task
            result_data.update(res)

        self.multiprocessing_dict['ok_tv'] = result_data

    def run(self):
        self.loop.run_until_complete(self.proceed())


def run_module(m_dict):
    ok_tv_runner = OkTvProcessor(m_dict)
    process = Process(target=ok_tv_runner.run)
    return process
