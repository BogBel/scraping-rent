from multiprocessing import Manager
import json
import argparse
from copy import deepcopy
import logging

from modules.oktv.oktv_main import run_module as ok_tv_module
from modules.dobovo.dobovo_main import run_module as dobovo_module


def get_arg_parser():
    arg_parser = argparse.ArgumentParser(description='Scrape Rent', add_help=True)
    arg_parser.add_argument('--debug', '-d', action='store_true', help='Do the same, but show url requests')
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
    args = vars(get_arg_parser().parse_args())
    if not any(args.get(required) for required in ('write', 'show')):
        logging.warning('Please run with at least one argument(--show or --write). -h for help')
        return
    if args['debug']:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    with Manager() as manager:
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

        result = deepcopy(multiprocessing_dict)
        if args.get('show'):
            logging.info(result)
        filename = args.get('write')
        if filename:
            with open('{}.json'.format(filename), 'w') as outfile:
                json.dumps(result, outfile)

if __name__ == '__main__':
    main()
