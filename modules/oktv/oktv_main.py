import asyncio
from multiprocessing import Process

from lxml import html

from modules.oktv.constants import REQUEST_HEADERS, LINKS_XPATH, CALENDAR_XPATH, MAIN_PAGE_URL
from tools.basic import BaseScrap, async_request


class OkTvProcessor(BaseScrap):
    def __init__(self, m_dict):
        self.multiprocessing_dict = m_dict
        self.loop = asyncio.new_event_loop()

    @staticmethod
    def _get_attr(tree, xpath, attr):
        for tag in tree.xpath(xpath):
            yield tag.get(attr)

    @staticmethod
    def _make_state(div):
        """
        :param div: lxml.html.HtmlElement <div data-time-default='14.02.2017' data-busy='free>
        :return: ('14.02.2017',
                  True) # if 'free'
        """
        return div.get("data-time-default"), div.get('data-busy')

    @staticmethod
    def _is_correct_day(div):
        class_name = div.get('class')
        return class_name != 'clear' and 'old' not in class_name

    async def _get_calendar(self, url):
        """
        :param url: https://oktv.ua/id3093636
        :return: {
            'https://oktv.ua/id3093594': {
                '05.03.2017': False, # is empty or not
                '19.03.2017': True,
                '21.03.2017': True,
                '07.04.2017': True,
                 '10.03.2017': True,
                }}
        """
        response = await async_request(url, method='get', headers=REQUEST_HEADERS, loop=self.loop)
        tree = html.fromstring(response)
        divs = filter(self._is_correct_day, tree.xpath(CALENDAR_XPATH))
        return {url: dict(map(self._make_state, divs))}

    async def _collect_urls(self):
        """
        :return: {
        'https://oktv.ua/id3093591'
        'https://oktv.ua/id3093592'
        'https://oktv.ua/id3093593'
        }
        """
        response = await async_request(MAIN_PAGE_URL, method='get', headers=REQUEST_HEADERS, loop=self.loop)
        tree = html.fromstring(response)
        hrefs = set(map('https://oktv.ua{}'.format,
                        self._get_attr(tree=tree, xpath=LINKS_XPATH, attr='href')))
        return hrefs

    async def proceed(self):
        """
        Save to multiprocessing dict result of module processing
        multiprocessing_dict['ok_tv'] = {
            'https://oktv.ua/id3093594': {
                '05.03.2017': False, # is empty or not
                 '10.03.2017': True,
                },
            'https://oktv.ua/id3093591': {
                '05.03.2017': True,
                '10.03.2017': True},
            }
        """
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
