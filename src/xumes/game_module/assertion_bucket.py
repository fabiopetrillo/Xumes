import multiprocessing
from typing import List

from xumes.game_module.assertion import IAssertionStrategy, AssertionEqual
from xumes.game_module.assertion_result import AssertionResult


class AssertionReport:

    def __init__(self, passed: bool, error_logs: str):
        self.passed = passed
        self.error_logs = error_logs

    def __getstate__(self):
        return self.passed, self.error_logs

    def __setstate__(self, state):
        self.passed, self.error_logs = state


class AssertionBucket:
    """
    A class that holds a list of lists of values to assert.
    Each list of values is a test case.
    We then iterate over each test case and assert the values.
    """
    ASSERT_MODE = "assert"
    COLLECT_MODE = "collect"

    def __init__(self, test_name, queue: multiprocessing.Queue):
        super().__init__()
        self._data = []
        self._results: List[AssertionResult] = []
        self._iterator = 0
        self._test_name = test_name
        self._mode = AssertionBucket.COLLECT_MODE
        self._queue = queue
        self._passed = True

    def reset_iterator(self):
        self._iterator = 0

    def collect_mode(self):
        self._mode = AssertionBucket.COLLECT_MODE

    def assertion_mode(self):
        self._mode = AssertionBucket.ASSERT_MODE

    def do_true(self, data):
        if self._mode == AssertionBucket.COLLECT_MODE:
            self._collect(other=data)
        elif self._mode == AssertionBucket.ASSERT_MODE:
            self._assert(expected=True, assertion_strategy=AssertionEqual(True))

    def do_equal(self, data, expected):
        if self._mode == AssertionBucket.COLLECT_MODE:
            self._collect(other=data)
        elif self._mode == AssertionBucket.ASSERT_MODE:
            self._assert(expected=expected, assertion_strategy=AssertionEqual(expected))

    def _collect(self, other):
        if self._iterator < len(self._data):
            self._data[self._iterator].append(other)
        else:
            self._data.append([other])
        self._iterator += 1

    def _assert(self, expected, assertion_strategy: IAssertionStrategy):
        # Get the actual value and assert it
        actual = self._data[self._iterator]
        r = assertion_strategy.test(actual)
        if not r:
            self._passed = False
        self._results.append(AssertionResult(
            fail_message=f"Test {self._test_name} FAILED on {self._iterator + 1}th assertion",
            passed=r,
            actual=actual,
            expected=expected
        ))
        self._iterator += 1

    def send_results(self):
        error_logs = ""
        for assertion_result in self._results:
            if not assertion_result.passed:
                error_logs += f"\n{assertion_result.fail_message:50}\n" \
                              f"{'Actual':10}: {assertion_result.actual} \n" \
                              f"{'Expected':10}: {assertion_result.expected}\n"
        self._queue.put(AssertionReport(passed=self._passed,
                                        error_logs=error_logs
                                        ))

    def clear(self):
        self._data.clear()
        self._results.clear()
        self._iterator = 0
