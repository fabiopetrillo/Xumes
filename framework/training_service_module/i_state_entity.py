from typing import TypeVar

ST = TypeVar("ST")


class IStateEntity:

    def update(self, state: ST) -> None:
        """
        Updates his attributes from a state.
        :param state: representation of the updates.
        """
        raise NotImplementedError

    @staticmethod
    def build(state: ST):
        """
        Build a IStateEntity from a state (initiate attributes).
        :param state: representation of the first state of the game object.
        """
        raise NotImplementedError
