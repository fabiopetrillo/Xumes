from typing import final

from framework.game_service_module.i_game_event import IGameEvent
from framework.game_service_module.errors.key_not_found_error import KeyNotFoundError


class IEventFactory:

    def clear(self) -> None:
        """
        Remove every event from the event queue.
        """
        raise NotImplementedError

    @final
    def find_input(self, input_str: str) -> IGameEvent:
        """
        Build and return a GameEvent from a input string.
        :param input_str: representation of an action.
        :return: Corresponding GameEvent
        """
        if input_str == "up":
            return self.up()
        elif input_str == "down":
            return self.down()
        elif input_str == "left":
            return self.left()
        elif input_str == "right":
            return self.right()
        elif input_str == "nothing":
            return self.nothing()

        raise KeyNotFoundError()

    # noinspection PyMethodMayBeStatic
    def nothing(self) -> IGameEvent:
        """
        :return: A nothing game event, (not doing anything on the game).
        """
        class Nothing(IGameEvent):
            def press(self) -> None:
                pass

            def release(self) -> None:
                pass

        return Nothing()

    def up(self) -> IGameEvent:
        raise NotImplementedError

    def down(self) -> IGameEvent:
        raise NotImplementedError

    def left(self) -> IGameEvent:
        raise NotImplementedError

    def right(self) -> IGameEvent:
        raise NotImplementedError
