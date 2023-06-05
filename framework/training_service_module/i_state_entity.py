from typing import TypeVar

ST = TypeVar("ST")


class IStateEntity:

    def update(self, state: ST) -> None:
        pass

    @staticmethod
    def build(state: ST):
        pass
