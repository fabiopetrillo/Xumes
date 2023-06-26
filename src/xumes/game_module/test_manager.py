import importlib
import inspect
import os
from collections import deque

from xumes.game_module import TestRunner, GameService, PygameEventFactory, CommunicationServiceGameMq


def create_registry():
    registry = {}

    def registrar_factory(content: str):
        def registrar(func):
            file_path = inspect.getsourcefile(func)
            file_name = os.path.basename(file_path[:-3])
            registry[file_name] = (func, content)
            return func

        registrar_factory.all = registry
        return registrar
    return registrar_factory


class TestManager:
    given = create_registry()
    when = create_registry()
    loop = create_registry()
    then = create_registry()
    render = create_registry()
    delete_screen = create_registry()

    def __init__(self):
        for file in os.listdir("./tests"):
            if file.endswith(".py"):
                module_name = file[:-3]
                module_path = os.path.join("./tests", file)
                module = compile(open(module_path).read(), module_path, 'exec')
                exec(module, globals(), locals())
                # module_dep = importlib.import_module(f"tests.{module_name}")

        print(self.given.all)

        self._game_services = {}

    def _create_game_service(self, steps: str, ip: str, port: int) -> GameService:

        class ConcreteTestRunner(TestRunner):

            def __init__(self, number_max_of_steps: int = 3000, number_max_of_tests: int = 1000):
                super().__init__()
                self._number_of_steps = 0
                self._number_max_of_steps = number_max_of_steps
                self._number_of_tests = 0
                self._number_max_of_tests = number_max_of_tests

                self._assertion_bucket = None  # Assertion bucket
                given.all[steps](self)

            def assert_true(self, condition: bool) -> None:
                pass

            def assert_false(self, condition: bool) -> None:
                pass

            def assert_equal(self, a, b) -> None:
                pass

            def assert_not_equal(self, a, b) -> None:
                pass

            def assert_greater(self, a, b) -> None:
                pass

            def assert_greater_equal(self, a, b) -> None:
                pass

            def assert_less(self, a, b) -> None:
                pass

            def assert_less_equal(self, a, b) -> None:
                pass

            def run_test(self) -> None:
                while self._number_of_steps < self._number_max_of_steps and self._number_of_tests < self._number_max_of_tests:
                    self._number_of_steps += 1
                    self._test_client.wait()
                    loop.all[steps](self)
                self._assertion_bucket.assert_all()

            def run_test_render(self) -> None:
                while self._number_of_steps < self._number_max_of_steps and self._number_of_tests < self._number_max_of_tests:
                    self._test_client.wait()
                    loop.all[steps](self)
                    render.all[steps](self)
                self._assertion_bucket.assert_all()

            def random_reset(self) -> None:
                self.reset()

            def reset(self) -> None:
                if self._number_of_tests > 0:
                    then.all[steps](self)
                when.all[steps](self)
                self._number_of_tests += 1

            def delete_screen(self) -> None:
                delete_screen.all[steps](self)

        game_service = GameService(test_runner=ConcreteTestRunner(),
                                   event_factory=PygameEventFactory(),
                                   communication_service=CommunicationServiceGameMq(ip=ip, port=port))
        return game_service


given = TestManager.given
when = TestManager.when
loop = TestManager.loop
then = TestManager.then
render = TestManager.render
delete_screen = TestManager.delete_screen

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
