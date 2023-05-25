from abc import ABC
from typing import Type

from game_service.state_observable import StateObservable
from game_service.state_observer import ConcreteStateObserver


class Test:

    def __init__(self, v):
        super().__init__()
        self.__v = v
        self.__list = []
        self.observable_state = TestState(self)
        self.observable_state.attach(ConcreteStateObserver.get_instance())

    def get_v(self):
        return self.__v

    def set_v(self, v):
        self.__v = v
        self.observable_state.notify()

    def add_element(self, v):
        self.__list.append(v)
        self.observable_state.notify()

    def set_l(self, new_l):
        self.__list = new_l
        self.observable_state.notify()

    def get_l(self):
        return self.__list


class TestState(StateObservable[Type[Test]], ABC):

    def state(self):
        return {
            "__v": self.object.get_v(),
            "__list": self.object.get_l()
        }


state_observer = ConcreteStateObserver.get_instance()
test = Test(v=0)

print(state_observer.state())

test.set_v(5)
test.add_element(1)
test.add_element(2)
print(state_observer.state())

test.add_element(3)

print(state_observer.state())
