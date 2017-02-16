from multiprocessing import Manager
import json
import argparse
from copy import deepcopy
import logging

from modules.oktv.oktv_main import run_module as ok_tv_module
from modules.dobovo.dobovo_main import run_module as dobovo_module


def get_args():
    arg_parser = argparse.ArgumentParser(description='Scrape Rent', add_help=True)
    arg_parser.add_argument('--write', '-w', action='store', help='filename result will be stored in')
    arg_parser.add_argument('--show', '-s', action='store_true', help='Show output to stdout')
    return arg_parser


def main():
    """
    Scrape sources in modules, collect rent calendar  and display/store it to json
    :return:
    {
        "ok_tv": {
           "https://oktv.ua/id3093608":{
              "18.02.2017":True,
              "28.03.2017":False,
              "08.03.2017":True
           },
           "https://oktv.ua/id3093617":{
              "18.02.2017":True,
              "28.03.2017":True,
              "08.03.2017":True,

           },
        },
        "dobovo": {
           "http://www.dobovo.com/kiev-apartments/elite-apartment-45244.html":{
              "18.02.2017":True,
              "28.03.2017":False,
              "08.03.2017":True,

           },
           "http://www.dobovo.com/kiev-apartments/city-center-23668.html":{
              "18.02.2017":True,
              "28.03.2017":True,
              "08.03.2017":False,

           }
        }
    }
    """
    logging.getLogger().setLevel(logging.DEBUG)
    with Manager() as manager:
        args = vars(get_args().parse_args())
        if not any(args.values()):
            logging.warning('Please run with at least one argument(--show or --write). -h for help')
            return
        multiprocessing_dict = manager.dict()
        child_processes = list()
        child_processes.append(dobovo_module(multiprocessing_dict))
        child_processes.append(ok_tv_module(multiprocessing_dict))
        try:
            for process in child_processes:
                process.start()
        finally:
            for process in child_processes:
                process.join()
        if args.get('show'):
            print(multiprocessing_dict)
        filename = args.get('write')
        if filename:
            with open('{}.json'.format(filename), 'w') as outfile:
                json.dumps(deepcopy(multiprocessing_dict), outfile)

if __name__ == '__main__':
    main()
