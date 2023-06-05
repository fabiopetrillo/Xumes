from typing import final

from framework.game_service_module.i_game_event import IGameEvent
from framework.game_service_module.exceptions.key_not_found_exception import KeyNotFoundException


class IEventFactory:

    def clear(self) -> None:
        pass

    @final
    def find_input(self, input_str: str) -> IGameEvent:
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

        raise KeyNotFoundException()

    def nothing(self) -> IGameEvent:
        class Nothing(IGameEvent):
            def press(self) -> None:
                pass

            def release(self) -> None:
                pass

        return Nothing()

    def up(self) -> IGameEvent:
        pass

    def down(self) -> IGameEvent:
        pass

    def left(self) -> IGameEvent:
        pass

    def right(self) -> IGameEvent:
        pass
