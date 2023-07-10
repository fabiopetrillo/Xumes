import json
import multiprocessing
import os
from abc import ABC, abstractmethod
from typing import List

from xumes.core.errors.running_ends_error import RunningEndsError
from xumes.core.modes import TEST_MODE
from xumes.core.registry import create_registry_content, create_registry
from xumes.game_module.assertion_bucket import AssertionBucket
from xumes.game_module.test_runner import TestRunner


class Scenario:

    def __init__(self, name: str = None, steps: str = None, feature=None):
        self.name = name
        self.steps: str = steps
        self.feature: Feature = feature


class Feature:

    def __init__(self, scenarios=None, name: str = None):
        if scenarios is None:
            scenarios = []
        self.scenarios: List[Scenario] = scenarios
        self.name = name


class FeatureStrategy(ABC):
    """
    FeatureStrategy is a class that implements the strategy pattern to define a way to get
    all features.
    """

    given = create_registry_content()
    when = create_registry_content()
    loop = create_registry()
    then = create_registry_content()
    render = create_registry()
    delete_screen = create_registry()
    log = create_registry()

    def __init__(self, alpha: float = 0.001):
        self.features: List[Feature] = []
        self._alpha = alpha

    def build_test_runner(self, timesteps: int = None, iterations: int = None,
                          mode: str = TEST_MODE, scenario: Scenario = None, test_queue: multiprocessing.Queue = None,
                          do_logs: bool = False):
        # Get steps
        steps = scenario.steps
        feature_name = scenario.feature.name
        scenario_name = scenario.name
        do_logs = do_logs
        alpha = self._alpha

        class ConcreteTestRunner(TestRunner):
            def __init__(self, number_max_of_steps: int = None, number_max_of_tests: int = None):
                super().__init__()
                self._feature = feature_name
                self._scenario = scenario_name
                self._mode = mode
                self._number_of_steps = 0
                self._number_max_of_steps = number_max_of_steps
                self._number_of_tests = 0
                self._number_max_of_tests = number_max_of_tests

                self._assertion_bucket = AssertionBucket(test_name=f"{self._feature}/{self._scenario}",
                                                         queue=test_queue,
                                                         alpha=alpha)
                given.all[steps][0](self)

                try:
                    delete_screen.all[steps](self)
                except KeyError:
                    pass

                when.all[steps][0](self)

                self._logs = {}
                self._do_logs = do_logs

            def _write_logs(self):
                # Write logs in file
                os.makedirs('logs', exist_ok=True)
                os.makedirs('logs/' + self._feature, exist_ok=True)
                os.makedirs('logs/' + self._feature + '/' + self._scenario, exist_ok=True)
                with open('logs/' + self._feature + "/" + self._scenario + "/logs.json", 'w') as f:
                    f.write(str(json.dumps(self._logs)))

            def _continue_test(self) -> bool:
                return (self._number_max_of_steps is None or self._number_of_steps < self._number_max_of_steps) and (
                        self._number_max_of_tests is None or self._number_of_tests < self._number_max_of_tests)

            def assert_true(self, condition: bool) -> None:
                self._assertion_bucket.assert_true(data=condition)

            def assert_false(self, condition: bool) -> None:
                self._assertion_bucket.assert_false(data=condition)

            def assert_equal(self, actual, expected) -> None:
                self._assertion_bucket.assert_equal(data=actual, expected=expected)

            def assert_not_equal(self, actual, expected) -> None:
                self._assertion_bucket.assert_not_equal(data=actual, expected=expected)

            def assert_greater(self, actual, expected) -> None:
                self._assertion_bucket.assert_greater_than(data=actual, expected=expected)

            def assert_greater_equal(self, actual, expected) -> None:
                self._assertion_bucket.assert_greater_than_or_equal(data=actual, expected=expected)

            def assert_less(self, actual, expected) -> None:
                self._assertion_bucket.assert_less_than(data=actual, expected=expected)

            def assert_less_equal(self, actual, expected) -> None:
                self._assertion_bucket.assert_less_than_or_equal(data=actual, expected=expected)

            def assert_between(self, actual, expected_min, expected_max) -> None:
                self._assertion_bucket.assert_between(data=actual, expected_min=expected_min, expected_max=expected_max)

            def assert_not_between(self, actual, expected_min, expected_max) -> None:
                self._assertion_bucket.assert_not_between(data=actual, expected_min=expected_min,
                                                          expected_max=expected_max)

            def _make_loop(self) -> bool:
                # Loop content method return False if the test is finished

                # Check if the test is finished
                finished = not self._continue_test()
                self._number_of_steps += 1
                if finished:
                    # If the test is finished, we send to the training manager that the test is finished
                    try:
                        self._test_client.is_finished = True
                        self._test_client.wait()
                    finally:
                        return False
                else:
                    # If the test is not finished, we compute the next step
                    try:
                        reset = self._test_client.wait()
                    except RunningEndsError:  # If the training manager is not running anymore, we stop the test
                        return False

                if not reset:
                    loop.all[steps](self)

                if self._mode == TEST_MODE and self._do_logs:
                    try:
                        # We get the logs of the current step
                        if steps not in self._logs:
                            self._logs[steps] = []

                        if self._number_of_tests == len(self._logs[steps]):
                            self._logs[steps].append([])
                        elif self._number_of_tests > len(self._logs[steps]):
                            raise Exception("The number of tests is greater than the number of logs")

                        self._logs[steps][self._number_of_tests].append(log.all[steps](self))
                    except KeyError:
                        pass
                return True

            def run_test(self) -> None:
                while True:
                    if not self._make_loop():
                        break
                self._do_assert_and_log()

            def run_test_render(self) -> None:
                while True:
                    if not self._make_loop():
                        break
                    render.all[steps](self)
                self._do_assert_and_log()

            def _do_assert_and_log(self) -> None:
                if self._mode == TEST_MODE:
                    # If the test is finished, we assert the test
                    self._assertion_bucket.assertion_mode()
                    then.all[steps][0](self)
                    self._assertion_bucket.send_results()
                    self._assertion_bucket.clear()
                    self._assertion_bucket.collect_mode()

                    if self._do_logs:
                        self._write_logs()

            def random_reset(self) -> None:
                self.reset()

            def reset(self) -> None:
                if self._mode == TEST_MODE:
                    then.all[steps][0](self)
                    self._assertion_bucket.reset_iterator()
                when.all[steps][0](self)
                self._number_of_tests += 1

            def delete_screen(self) -> None:
                if steps in delete_screen.all:
                    delete_screen.all[steps][0](self)

        return ConcreteTestRunner(timesteps, iterations)

    @abstractmethod
    def retrieve_feature(self):
        """
        Get all features.
        """
        raise NotImplementedError


# Decorators
given = FeatureStrategy.given
when = FeatureStrategy.when
loop = FeatureStrategy.loop
then = FeatureStrategy.then
render = FeatureStrategy.render
delete_screen = FeatureStrategy.delete_screen
log = FeatureStrategy.log
