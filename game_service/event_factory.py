from typing import final

from game_service.client_event import IClientEvent
from game_service.exceptions.key_not_found_exception import KeyNotFoundException


class IEventFactory:

    def clear(self) -> None:
        pass

    @final
    def find_input(self, input_str: str) -> IClientEvent:
        if input_str == "up":
            return self.up()
        elif input_str == "down":
            return self.down()
        elif input_str == "left":
            return self.left()
        elif input_str == "right":
            return self.right()

        raise KeyNotFoundException()

    def up(self) -> IClientEvent:
        pass

    def down(self) -> IClientEvent:
        pass

    def left(self) -> IClientEvent:
        pass

    def right(self) -> IClientEvent:
        pass

