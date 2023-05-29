from abc import ABC

from game_service.state_observer import StateObserver


class ConcreteStateObserver(StateObserver, ABC):
    instance = None

    @staticmethod
    def get_instance():
        if ConcreteStateObserver.instance is None:
            ConcreteStateObserver.instance = StateObserver()
        return ConcreteStateObserver.instance
