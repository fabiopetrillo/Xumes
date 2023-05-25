from abc import ABC

from game_service.state_observer import StateObserver


class SnakeGameObserver(StateObserver, ABC):
    instance = None

    @staticmethod
    def get_instance():
        if SnakeGameObserver.instance is None:
            SnakeGameObserver.instance = StateObserver()
        return SnakeGameObserver.instance
