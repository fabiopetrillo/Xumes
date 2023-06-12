from typing import List, TypeVar

SW = TypeVar("SW")


class ICommunicationServiceTraining:

    def push_event(self, event: str) -> None:
        """
        Method used to send an event to the game service.
        :param event: string representing a game service event like reset for reset the game.
        """
        raise NotImplementedError

    def push_actions(self, actions: List[str]) -> None:
        """
        Send actions to game service. Action could be buttons pressed
        or the mouse moving.
        :param actions: list of action to perform.
        """
        raise NotImplementedError

    def get_states(self) -> List[SW]:
        """
        Retrieve the state from the game service side.
        """
        raise NotImplementedError
