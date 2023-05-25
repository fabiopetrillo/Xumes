from abc import ABC


class StateObserver(ABC):

    def __init__(self):
        self._state = {}
        self._state_strategy = None

    def update(self, obs) -> None:
        self._state[(obs.__class__, id(obs))] = obs.state()

    def state(self):
        return self._state


class ConcreteStateObserver(StateObserver, ABC):
    instance = None

    @staticmethod
    def get_instance():
        if ConcreteStateObserver.instance is None:
            ConcreteStateObserver.instance = StateObserver()
        return ConcreteStateObserver.instance
