from typing import List

from xumes.game_module.assertion import IAssertionStrategy


class AssertionBucket(List[List]):
    """
    A class that holds a list of lists of values to assert.
    Each list of values is a test case.
    We then iterate over each test case and assert the values.
    """
    def __init__(self):
        super().__init__()
        self._iterator = 0

    def add_assertion(self, other):
        # Add a new assertion to the current test case
        if len(self) > self._iterator:
            self[self._iterator].append(other)
        else:
            self.append([other])
        self._iterator += 1

    def reset_iterator(self):
        self._iterator = 0

    def assertion(self, assertion_strategy: IAssertionStrategy):
        # Get the actual value and assert it
        actual = self[self._iterator]
        r = assertion_strategy.test(actual)
        self._iterator += 1
        return r, actual
