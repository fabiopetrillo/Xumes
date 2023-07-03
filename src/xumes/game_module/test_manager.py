import importlib.util
import logging
import multiprocessing
import os
from abc import abstractmethod

from xumes.core.errors.running_ends_error import RunningEndsError
from xumes.core.registry import create_registry_content, create_registry
from xumes.game_module import TestRunner, GameService, PygameEventFactory, CommunicationServiceGameMq
from xumes.game_module.i_communication_service_test_manager import ICommunicationServiceTestManager

TEST_MODE = 'test'
RENDER_MODE = 'render'
TRAIN_MODE = 'train'


class TestManager:
    given = create_registry_content()
    when = create_registry_content()
    loop = create_registry()
    then = create_registry_content()
    render = create_registry()
    delete_screen = create_registry()
    clock_reset = create_registry()

    def __init__(self, communication_service: ICommunicationServiceTestManager,
                 mode: str = TEST_MODE, timesteps=None, iterations=None):
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
        if feature + scenario not in self._ports:
            self._ports[feature + scenario] = 5001 + len(self._ports)
        return self._ports[feature + scenario]

    def add_game_service_data(self, steps: str, ip: str, port: int):
        self._game_services_data[steps] = (ip, port)

    def create_game_service(self, steps: str, ip: str, port: int) -> GameService:

        class ConcreteTestRunner(TestRunner):

            def __init__(self, number_max_of_steps: int = None, number_max_of_tests: int = None,
                         mode: str = TEST_MODE):
                super().__init__()
                self._mode = mode
                self._number_of_steps = 0
                self._number_max_of_steps = number_max_of_steps
                self._number_of_tests = 0
                self._number_max_of_tests = number_max_of_tests

                self._assertion_bucket = None  # Assertion bucket
                given.all[steps][0](self)
                when.all[steps][0](self)

            def continue_test(self) -> bool:
                return (self._number_max_of_steps is None or self._number_of_steps < self._number_max_of_steps) and (
                        self._number_max_of_tests is None or self._number_of_tests < self._number_max_of_tests)

            def assert_true(self, condition: bool) -> None:
                pass

            def assert_false(self, condition: bool) -> None:
                pass

            def assert_equal(self, actual, expected) -> None:
                pass

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

            def _make_loop(self):
                finished = not self.continue_test()
                self._number_of_steps += 1
                if finished:
                    try:
                        self._test_client.is_finished = True
                        self._test_client.wait()
                    finally:
                        return False
                else:
                    try:
                        reset = self._test_client.wait()
                    except RunningEndsError:
                        return False

                if not reset:
                    loop.all[steps](self)
                return True

            def run_test(self) -> None:
                while True:
                    if not self._make_loop():
                        break

                # self._assertion_bucket.assert_all()

            def run_test_render(self) -> None:
                while True:
                    if not self._make_loop():
                        break
                    render.all[steps](self)

                # self._assertion_bucket.assert_all()

            def random_reset(self) -> None:
                self.reset()

            def reset(self) -> None:
                if self._number_of_tests > 0:
                    then.all[steps][0](self)
                when.all[steps][0](self)
                self._number_of_tests += 1

            def delete_screen(self) -> None:
                if steps in delete_screen.all:
                    delete_screen.all[steps][0](self)

        return self._build_game_service(
            ConcreteTestRunner(mode=self._mode, number_max_of_steps=self._timesteps,
                               number_max_of_tests=self._iterations), ip, port, )

    @abstractmethod
    def _build_game_service(self, test_runner, ip, port) -> GameService:
        raise NotImplementedError

    def test_all(self) -> None:
        active_processes = multiprocessing.Value('i', 0)

        for steps in self.given.all:
            self._communication_service.connect_trainer(self, 'feature1', steps)

            if self._mode == TEST_MODE or self._mode == TRAIN_MODE:
                process = multiprocessing.Process(target=self.run_test, args=(steps, active_processes,))
            else:
                process = multiprocessing.Process(target=self.run_test_render, args=(steps, active_processes,))
            process.start()
            active_processes.value += 1
            self._game_service_processes[steps] = process

        self._communication_service.start_training(self)

        while active_processes.value > 0:
            pass

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


given = TestManager.given
when = TestManager.when
loop = TestManager.loop
then = TestManager.then
render = TestManager.render
delete_screen = TestManager.delete_screen
clock_reset = TestManager.clock_reset


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
