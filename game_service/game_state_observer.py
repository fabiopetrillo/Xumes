import json
from typing import Dict, Generic, TypeVar

ST = TypeVar("ST")


class IGameStateObserver(Generic[ST]):

    def update_state(self, obs):
        pass

    def remove_state(self, obs):
        pass

    def get_state(self) -> ST:
        # Return only the changes
        pass


class JsonGameStateObserver(Dict, IGameStateObserver):
    instance = None

    def update_state(self, obs) -> None:
        self[id(obs.object)] = obs.state().state
        self[id(obs.object)]['label'] = str(obs.object.__class__)

    def remove_state(self, obs):
        if id(obs.object) in self.keys():
            self.pop(id(obs.object))

    def get_state(self):
        state = json.dumps(self)
        self.clear()
        return state

    def __call__(self, *args, **kwargs):
        return

    @classmethod
    def get_instance(cls):
        if JsonGameStateObserver.instance is None:
            JsonGameStateObserver.instance = JsonGameStateObserver()
        return JsonGameStateObserver.instance
