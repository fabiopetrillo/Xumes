from abc import ABC

from game_service.state_decoder import StateDecoder
from game_service.state_observable import StateObservable
from game_service.state_observer import ConcreteStateObserver


class Test(StateObservable, ABC):

    def __init__(self, v):
        super().__init__()
        self.__v = v
        self.__list = []

    def set_state_decoder(self):
        return TestState(self)

    def get_v(self):
        return self.__v

    def set_v(self, v):
        self.__v = v
        self.notify()

    def add_element(self, v):
        self.__list.append(v)
        self.notify()

    def set_l(self, new_l):
        self.__list = new_l
        self.notify()

    def get_l(self):
        return self.__list


class TestState(StateDecoder[Test], ABC):

    def state(self):
        return {
            "__v": self._observable.get_v(),
            "__list": self._observable.get_l()
        }


state_observer = ConcreteStateObserver.get_instance()
test = Test(v=0)
test.attach(state_observer)

print(state_observer.state())

test.set_v(5)
test.add_element(1)
test.add_element(2)
print(state_observer.state())

test.add_element(3)

print(state_observer.state())
