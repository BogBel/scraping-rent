from multiprocessing import Manager
import json
import argparse

from modules.oktv.oktv_main import run_module as ok_tv_module
from modules.dobovo.dobovo_main import run_module as dobovo_module


def get_args():
    arg_parser = argparse.ArgumentParser(description='Scrape', add_help=False)
    arg_parser.add_argument('--help', '-h',
                            action='help',
                            default=argparse.SUPPRESS,
                            help='Search for sources calendars and make output like: '
                                 '\tdate: True(if empty) else False')
    arg_parser.add_argument('--write', '-w', action='store_true', help='Save output to json file', default=True)
    arg_parser.add_argument('--show', '-s', action='store_true', help='Show output to stdout', default=True)
    return arg_parser


def main():
    with Manager() as manager:
        multiprocessing_dict = manager.dict()
        child_processes = list()
        child_processes.append(dobovo_module(multiprocessing_dict))
        child_processes.append(ok_tv_module(multiprocessing_dict))
        arg_parser = get_args().parse_args()

        # try:
        #     for process in child_processes:
        #         process.start()
        # finally:
        #     for process in child_processes:
        #         process.join()
        # args = get_args()
        # if args.help:
        #     print('suka')
        #     raise KeyError
        # print(multiprocessing_dict)
        # with open('data.txt', 'w') as outfile:
        #     json.dump(data, outfile)
        # json.dumps(multiprocessing_dict)

if __name__ == '__main__':
    main()
