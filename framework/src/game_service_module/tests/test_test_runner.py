from unittest import TestCase
from unittest.mock import patch, Mock

from framework.src.game_service_module.test_runner import _TestRunner, JsonTestRunner


# noinspection PyPep8Naming
class Test_TestRunner(TestCase):

    @patch.multiple(_TestRunner, __abstractmethods__=set())
    def setUp(self) -> None:
        self.game_service = Mock()
        self.observer1 = Mock()
        self.state = Mock()
        self.game_loop_object = Mock()

        self.test_runner = _TestRunner(game_loop_object=self.game_loop_object, observers=[self.observer1])

    @patch.multiple(_TestRunner, __abstractmethods__=set())
    def test_init(self):
        # Create with one observer
        try:
            _TestRunner(game_loop_object=self.game_loop_object, observers=self.observer1)
        except Exception as e:
            self.fail(f"Can't add one observer on init, {e}.")
        # Create with a list of observers
        try:
            _TestRunner(game_loop_object=self.game_loop_object, observers=[self.observer1])
        except Exception as e:
            self.fail(f"Can't add a list of observers on init, {e}.")

    def test_update_state(self):
        new_state = Mock("new_state")
        self.test_runner.update_state(new_state)
        self.observer1.update_state.assert_called_once()
        self.assertEquals(self.test_runner._game_state, new_state)

    def test_test_client(self):
        client = Mock()
        self.test_runner._test_client = client
        self.assertEqual(self.test_runner.test_client, client)

    def test_set_client(self):
        client = Mock()
        self.test_runner.set_client(client)
        self.assertEqual(self.test_runner._test_client, client)

    def test_run_test(self):
        self.assertRaises(NotImplementedError, self.test_runner.run_test)

    def test_run_test_render(self):
        self.assertRaises(NotImplementedError, self.test_runner.run_test_render)

    def test_random_reset(self):
        self.assertRaises(NotImplementedError, self.test_runner.random_reset)

    def test_reset(self):
        self.assertRaises(NotImplementedError, self.test_runner.reset)

    def test_delete_screen(self):
        self.assertRaises(NotImplementedError, self.test_runner.delete_screen)


class TestJsonTestRunner(TestCase):

    @patch.multiple(JsonTestRunner, __abstractmethods__=set())
    def test_state(self):
        game_service = Mock()
        observer1 = Mock()
        state = Mock()
        game_loop_object = Mock()
        test_runner = JsonTestRunner(game_loop_object=game_loop_object, observers=observer1)
        test_runner.set_client(game_service)
        test_runner.update_state(state)
        self.assertEqual(test_runner.state().state["state"], state)
