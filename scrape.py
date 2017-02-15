from multiprocessing import Manager

from modules.oktv.oktv_main import run_module as ok_tv_module
from modules.dobovo.dobovo_main import run_module as dobovo_module


def main():
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
        print(multiprocessing_dict)

if __name__ == '__main__':
    main()
