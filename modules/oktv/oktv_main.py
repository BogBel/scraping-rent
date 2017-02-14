import asyncio
from multiprocessing import Process

from tools.basic import BaseScrap


class OkTvProcessor(BaseScrap):
    def __init__(self, m_dict):
        self.multiprocessing_dict = m_dict
        self.loop = asyncio.new_event_loop()

    def run(self):
        self.multiprocessing_dict['ok_tv'] = {'data': True}


def run_module(m_dict):
    ok_tv_runner = OkTvProcessor(m_dict)
    process = Process(target=ok_tv_runner.run)
    return process
