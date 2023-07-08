from unittest import TestCase
from unittest.mock import Mock, MagicMock

from xumes.game_module import State
from xumes.game_module.test_runner import TestRunner


class TestCreatorGameStateObservable(TestCase):

    def setUp(self):
        observer = Mock()

        class ConcreteTestRunner(TestRunner):
            def run_test(self) -> None:
                pass

            def run_test_render(self) -> None:
                pass

            def random_reset(self) -> None:
                pass

            def reset(self) -> None:
                pass

            def delete_screen(self) -> None:
                pass

        self.test_runner = ConcreteTestRunner(observer=observer)

    def tearDown(self):
        del self.test_runner

    def test_create(self):
        class A:

            def __init__(self):
                self.a = 0

            def update_a(self):
                self.update()

            def update(self):
                self.a += 1

        a = self.test_runner.create(A, "a", State("a", methods_to_observe=["update"]))
        a.update_a()
        self.assertEqual(self.test_runner._observer.update_state.call_count, 4)
        self.assertEqual(a.a, 1)

    def test_create_with_args(self):
        class A:

            def __init__(self, a):
                self.a = a

            def update_a(self):
                self.update()

            def update(self):
                self.a += 1

        a = self.test_runner.create(A, "a", State("a"), 0)
        a.update_a()
        self.assertEqual(self.test_runner._observer.update_state.call_count, 3)

    def test_create_with_kwargs(self):
        class A:

            def __init__(self, a=0, b=0):
                self.a = a
                self.b = b

            def update_a(self):
                self.update()

            def update(self):
                self.a += 1

        a = self.test_runner.create(A, "a", State("a"), a=0, b=0)
        a.update_a()
        self.assertEqual(self.test_runner._observer.update_state.call_count, 3)

    def test_create1(self):
        class A:

            def __init__(self):
                self.a = 0

            def update_a(self):
                self.update()

            def update(self):
                self.a += 1

        a = self.test_runner.create(A, "a", State("a", methods_to_observe=["update"]))
        a.update_a()
        self.assertEqual(self.test_runner._observer.update_state.call_count, 4)
        self.assertEqual(a.a, 1)

    def test_create_obj_in_obj(self):
        class A:

            def __init__(self):
                self.a = 0

            def update_a(self):
                self.update()

            def update(self):
                self.a += 1

        class B:

            def __init__(self):
                self.a = A()

            def update_a(self):
                self.a.update_a()

        b = self.test_runner.create(B, "b", State("a", methods_to_observe=["update_a"]))
        b.update_a()
        self.assertEqual(self.test_runner._observer.update_state.call_count, 3)
        self.assertEqual(b.a.a, 1)

    def test_create_list_of_obj_in_obj(self):
        class A:

            def __init__(self):
                self.a = 0

            def update_a(self):
                self.update()

            def update(self):
                self.a += 1

        class B:

            def __init__(self):
                self.a = [A(), A()]

            def update_a(self):
                for a in self.a:
                    a.update_a()

        b = self.test_runner.create(B, "b", State("a", methods_to_observe=["update_a"]))
        b.update_a()
        self.assertEqual(self.test_runner._observer.update_state.call_count, 3)
        self.assertEqual(b.a[0].a, 1)

    def test_create_list_of_obj_in_obj_with_list_of_methods(self):
        class A:

            def __init__(self):
                self.a = 0

            def update_a(self):
                self.update()

            def update(self):
                self.a += 1

        class B:

            def __init__(self):
                self.a = [A(), A()]

            def update(self):
                self.update_a()

            def update_a(self):
                for a in self.a:
                    a.update_a()

        b = self.test_runner.create(B, "b", State("a", State("a", methods_to_observe=["update_a"])))
        b.update()
        self.assertEqual(self.test_runner._observer.update_state.call_count, 3)
        self.assertEqual(b.a[0].a, 1)

    def test_create_two_observable(self):
        class A:

            def __init__(self, value):
                self.value = value

            def update_a(self):
                self.update()

            def update(self):
                self.value += 1

        class B:

            def __init__(self, a):
                self.a = a

            def update_a(self):
                self.a.update()

        a = self.test_runner.create(A, "a", State("value", methods_to_observe=["update"]), value=0)
        b = self.test_runner.create(B, "b", State("a", methods_to_observe=["update_a"]), a=a)

        b.update_a()

        self.assertEqual(self.test_runner._observer.update_state.call_count, 7)

    def test_create_two_observable_no_methods(self):
        class A:

            def __init__(self, value):
                self.value = value

            def update_a(self):
                self.update()

            def update(self):
                self.value += 1

        class B:

            def __init__(self, a):
                self.a = a

            def update_a(self):
                self.a.update()

        a = self.test_runner.create(A, "a", State("value"), value=0)
        b = self.test_runner.create(B, "b", State("a"), a=a)

        b.update_a()

        self.assertEqual(self.test_runner._observer.update_state.call_count, 5)

    def test_create_observable_with_list_of_observable(self):
        class A:

            def __init__(self, value):
                self.value = value

            def update_a(self):
                self.update()

            def update(self):
                self.value += 1

        class B:

            def __init__(self, a_list):
                self.a_list = a_list

            def update_a(self):
                for a in self.a_list:
                    a.update()

        a = self.test_runner.create(A, "a", State("value", methods_to_observe=["update"]), value=0)
        b = self.test_runner.create(B, "b", State("a_list", methods_to_observe=["update_a"]), a_list=[a, a])

        b.update_a()

        self.assertEqual(self.test_runner._observer.update_state.call_count, 9)

    def test_create_two_observable_each_contain_each_other(self):
        class A:

            def __init__(self, b):
                self.b = b

            def update_a(self):
                self.update()

            def update(self):
                pass

        class B:

            def __init__(self, a):
                self.a = a

            def update_a(self):
                self.a.update()

        a = self.test_runner.create(A, "a", State("b", methods_to_observe=["update"]), b=0)
        b = self.test_runner.create(B, "b", State("a", methods_to_observe=["update_a"]), a=a)
        a.b = b

        b.update_a()

        self.assertEqual(self.test_runner._observer.update_state.call_count, 7)

