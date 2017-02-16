import asyncio
from multiprocessing import Process
from itertools import starmap
from datetime import datetime

from lxml import html

from modules.dobovo.constants import LINKS_XPATH, CALENDAR_URL, MAIN_PAGE_URL
from tools.basic import BaseScrap, async_request


class DobovoProcessor(BaseScrap):
    def __init__(self, m_dict):
        self.multiprocessing_dict = m_dict
        self.loop = asyncio.new_event_loop()

    @staticmethod
    def _get_url_and_id(tree):
        for tag in tree.xpath(LINKS_XPATH):
            _id = tag.get('data-apt-code')
            link = tag.xpath('div/a')[0].get('href')
            yield _id, link

    @staticmethod
    def _make_state(div):
        return div.get('date'), div.get('class') == "cell clickable"

    @staticmethod
    def _is_correct_day(div):
        return all(cls not in div.get('class') for cls in ('is-other-month', 'is-last-days'))

    @staticmethod
    def _make_state(day, stats):
        """
        :param day: "2017-02-15"
        :param stats: {"price":"1323.00", "state":"0", "minnights":"1", "currency":"UAH"}
        """
        day = datetime.strftime(datetime.strptime(day, '%Y-%m-%d'), '%d.%m.%Y')
        return day, stats['state'] == "1"

    async def _get_calendar(self, item_id, url):
        data = {'id': item_id}
        response = await async_request(CALENDAR_URL, return_type='json', method='post', loop=self.loop, data=data)
        return {url: dict(starmap(self._make_state, response['calendar'].items()))}

    async def _get_link_and_id(self):
        main_page_response = await async_request(MAIN_PAGE_URL, method='get', loop=self.loop)
        tree = html.fromstring(main_page_response)
        return self._get_url_and_id(tree=tree)

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

        tasks = [self._get_calendar(_id, url) for _id, url in await self._get_link_and_id()]
        for task in asyncio.as_completed(tasks, loop=self.loop):
            res = await task
            result_data.update(res)
        self.multiprocessing_dict['dobovo'] = result_data

    def run(self):
        self.loop.run_until_complete(self.proceed())


def run_module(m_dict):
    dobovo_runner = DobovoProcessor(m_dict)
    process = Process(target=dobovo_runner.run)
    return process
