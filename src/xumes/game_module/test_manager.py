import importlib.util
import json
import logging
import multiprocessing
import os
from abc import abstractmethod

from xumes.core.errors.running_ends_error import RunningEndsError
from xumes.core.registry import create_registry_content, create_registry
from xumes.game_module import TestRunner, GameService, PygameEventFactory, CommunicationServiceGameMq
from xumes.game_module.assertion import AssertionEqual
from xumes.game_module.assertion_bucket import AssertionBucket
from xumes.game_module.i_communication_service_test_manager import ICommunicationServiceTestManager

TEST_MODE = 'test'
RENDER_MODE = 'render'
TRAIN_MODE = 'train'


class TestManager:
    """
    A class that manages the execution of tests in a game environment.

    The TestManager class is responsible for loading and running tests in a game environment. It provides functionality
    for creating game services, running tests, and managing communication with the training manager.

    Attributes:
        given (registry): A registry for storing the given steps of a test scenario.
        when (registry): A registry for storing the when steps of a test scenario.
        loop (registry): A registry for storing the loop steps of a test scenario.
        then (registry): A registry for storing the then steps of a test scenario.
        render (registry): A registry for storing the render steps of a test scenario.
        delete_screen (registry): A registry for storing the delete_screen steps of a test scenario.
        log (registry): A registry for storing the log steps of a test scenario.

    Args:
        communication_service (ICommunicationServiceTestManager): An implementation of the
            ICommunicationServiceTestManager interface for communication with the training manager.
        mode (str, optional): The mode of the test execution. Can be 'test', 'render', or 'train'.
            Defaults to 'test'.
        timesteps (int, optional): The maximum number of steps to run in a test. Defaults to None.
        iterations (int, optional): The maximum number of iterations to run a test. Defaults to None.

    Methods:
        get_port(feature: str, scenario: str) -> int:
            Retrieves the port number for a given feature and scenario.
        add_game_service_data(steps: str, ip: str, port: int) -> None:
            Adds game service data to the list of game services data.
        create_game_service(steps: str, ip: str, port: int) -> GameService:
            Creates a game service instance with the specified steps, IP, and port.
        _build_game_service(test_runner, ip, port) -> GameService:
            Abstract method to build a game service instance. Must be implemented by subclasses.
        test_all() -> None:
            Runs all the tests in the game environment.
        delete_game_services() -> None:
            Deletes all game service instances.
        run_test(steps: str, active_processes) -> None:
            Runs a test with the given steps.
        run_test_render(steps: str, active_processes) -> None:
            Runs a test in render mode with the given steps.
    """
    given = create_registry_content()
    when = create_registry_content()
    loop = create_registry()
    then = create_registry_content()
    render = create_registry()
    delete_screen = create_registry()
    log = create_registry()

    def __init__(self, communication_service: ICommunicationServiceTestManager,
                 mode: str = TEST_MODE, timesteps=None, iterations=None):
        # Load all tests
        for file in os.listdir("./tests"):
            if file.endswith(".py"):
                module_name = file[:-3]
                module_path = os.path.join("./tests", file)
                module = compile(open(module_path).read(), module_path, 'exec')
                exec(module, globals(), locals())
                module_path = os.path.abspath(module_path)
                module_name = os.path.basename(module_path)[:-3]

                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module_dep = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module_dep)

        self._communication_service = communication_service
        self._game_service_processes = {}
        self._game_services_data = {}
        self._game_services = {}
        self._mode = mode
        self._ports = {}
        self._timesteps = timesteps
        self._iterations = iterations

    def get_port(self, feature: str, scenario: str) -> int:
        # Get the port for a given feature and scenario
        if feature + scenario not in self._ports:
            self._ports[feature + scenario] = 5001 + len(self._ports)
        return self._ports[feature + scenario]

    def add_game_service_data(self, steps: str, ip: str, port: int):
        # Add a game service data to the list of game services data
        self._game_services_data[steps] = (ip, port)

    def create_game_service(self, steps: str, ip: str, port: int) -> GameService:

        class ConcreteTestRunner(TestRunner):
            def __init__(self, number_max_of_steps: int = None, number_max_of_tests: int = None,
                         mode: str = TEST_MODE, feature: str = None, scenario: str = None):
                super().__init__()
                self._feature = feature
                self._scenario = scenario
                self._mode = mode
                self._number_of_steps = 0
                self._number_max_of_steps = number_max_of_steps
                self._number_of_tests = 0
                self._number_max_of_tests = number_max_of_tests

                self._assertion_bucket = AssertionBucket()
                given.all[steps][0](self)
                when.all[steps][0](self)

                self._asserting = False
                self._logs = {}

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
                if not self._asserting:
                    self._assertion_bucket.add_assertion(condition)
                else:
                    r, actual = self._assertion_bucket.do_assert(AssertionEqual(True))
                    if not r:
                        logging.error("Assertion failed: Expected: " + "True" + ", Actual: " + str(actual))
                    else:
                        logging.info("Assertion passed: " + str(actual))

            def assert_false(self, condition: bool) -> None:
                pass

            def assert_equal(self, actual, expected) -> None:
                if not self._asserting:
                    self._assertion_bucket.add_assertion(actual)
                else:
                    r, actual = self._assertion_bucket.do_assert(AssertionEqual(expected))
                    if not r:
                        logging.error("Assertion failed: Expected: " + str(expected) + ", Actual: " + str(actual))
                    else:
                        logging.info("Assertion passed: " + str(actual))

            def assert_not_equal(self, actual, expected) -> None:
                pass

            def assert_greater(self, actual, expected) -> None:
                pass

            def assert_greater_equal(self, actual, expected) -> None:
                pass

            def assert_less(self, actual, expected) -> None:
                pass

            def assert_less_equal(self, actual, expected) -> None:
                pass

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
                    self._asserting = True
                    then.all[steps][0](self)
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

        return self._build_game_service(
            ConcreteTestRunner(mode=self._mode, number_max_of_steps=self._timesteps,
                               number_max_of_tests=self._iterations, feature='feature1', scenario=steps), ip, port, )

    @abstractmethod
    def _build_game_service(self, test_runner, ip, port) -> GameService:
        raise NotImplementedError

    def test_all(self) -> None:
        # Check if all tests are finished
        active_processes = multiprocessing.Value('i', 0)

        # For all scenarios, we run the test
        for steps in self.given.all:
            self._communication_service.connect_trainer(self, 'feature1', steps)

            if self._mode == TEST_MODE or self._mode == TRAIN_MODE:  # no render
                process = multiprocessing.Process(target=self.run_test, args=(steps, active_processes,))
            else:  # render
                process = multiprocessing.Process(target=self.run_test_render, args=(steps, active_processes,))
            process.start()
            active_processes.value += 1
            self._game_service_processes[steps] = process

        # Send to the training manager that the training is started
        self._communication_service.start_training(self)

        # Wait for all tests to be finished
        while active_processes.value > 0:
            pass

        # Close all processes and delete all game services
        for steps, process in self._game_service_processes.items():
            process.kill()
            self._communication_service.disconnect_trainer(self, 'feature1', steps)
        self.delete_game_services()

    def delete_game_services(self) -> None:
        self._game_services_data.clear()
        self._game_service_processes.clear()

    def run_test(self, steps: str, active_processes) -> None:
        game_service = self.create_game_service(steps, *self._game_services_data[steps])
        game_service.run()

        with active_processes.get_lock():
            active_processes.value -= 1

        game_service.stop()

    def run_test_render(self, steps: str, active_processes) -> None:
        game_service = self.create_game_service(steps, *self._game_services_data[steps])
        game_service.run_render()

        with active_processes.get_lock():
            active_processes.value -= 1

        game_service.stop()


# Decorators
given = TestManager.given
when = TestManager.when
loop = TestManager.loop
then = TestManager.then
render = TestManager.render
delete_screen = TestManager.delete_screen
log = TestManager.log


class PygameTestManager(TestManager):

    def _build_game_service(self, test_runner, ip, port) -> GameService:
        game_service = GameService(test_runner=test_runner,
                                   event_factory=PygameEventFactory(),
                                   communication_service=CommunicationServiceGameMq(ip=ip, port=port))
        return game_service

# Maybe in the future
# def assert_in(self, a, b) -> None:
#     pass
#
# def assert_not_in(self, a, b) -> None:
#     pass
#
# def assert_is(self, a, b) -> None:
#     pass
#
# def assert_is_not(self, a, b) -> None:
#     pass
#
# def assert_is_none(self, a) -> None:
#     pass
#
# def assert_is_not_none(self, a) -> None:
#     pass
#
# def assert_is_instance(self, a, b) -> None:
#     pass
#
# def assert_is_not_instance(self, a, b) -> None:
#     pass
#
# def assert_raises(self, a, b) -> None:
#     pass
