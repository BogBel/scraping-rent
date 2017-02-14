import abc
from multiprocessing import Manager, Process


class BaseScrap:
    @abc.abstractmethod
    def run(self):
        pass

def main():
    with Manager() as manager:
        multiprocessing_dict = manager.dict()
        # p = Process(target=f, args=(d, l))
        # p.start()
        # p.join()
        #
        # print(d)
        # print(l)

if __name__ == '__main__':
    main()