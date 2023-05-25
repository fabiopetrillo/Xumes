from abc import ABC


class StateObserver(ABC):

    def __init__(self):
        self._state = {}

    def update(self, obs) -> None:
        self._state[(obs.object.__class__, id(obs.object))] = obs.state()

    def state(self):
        return self._state


class ConcreteStateObserver(StateObserver, ABC):
    instance = None

    @staticmethod
    def get_instance():
        if ConcreteStateObserver.instance is None:
            ConcreteStateObserver.instance = StateObserver()
        return ConcreteStateObserver.instance
