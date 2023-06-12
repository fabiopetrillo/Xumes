from abc import ABC

from xumes.game_module.game_element_state import GameElementState
from xumes.game_module.test_runner import _TestRunner


class JsonTestRunner(_TestRunner, ABC):

    def state(self):
        return GameElementState({
            "state": self._game_state
        })
