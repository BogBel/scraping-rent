import abc


class BaseScrap:
    @abc.abstractmethod
    def run(self):
        raise NotImplementedError
