from abc import abstractmethod


class AssertionBucket(set):

    def __init__(self):
        super().__init__()
        self._assertion = None

    @abstractmethod
    def assertion(self):
        raise NotImplementedError
