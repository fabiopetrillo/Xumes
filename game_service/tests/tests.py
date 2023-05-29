from game_service.client_service import ClientService, TestRunner
from game_service.state_observable import StateObservable
from game_service.tests.observers import ConcreteStateObserver


class Test:

    def __init__(self, v):
        super().__init__()
        self.__v = v
        self.__list = []
        self.observable_state: StateObservable[Test] = TestState(self)
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


class TestState(StateObservable):

    def state(self):
        return {
            "__v": self.object.get_v(),
            "__list": self.object.get_l()
        }


class GameLoopContainer(TestRunner):

    def __init__(self):
        super().__init__()
        self.test = Test(v=0)

    def run(self):
        while True:
            self.test_client()
            self.test.set_v(self.test.get_v() + 1)

    def run_test(self) -> None:
        self.run()


if __name__ == "__main__":
    client_service = ClientService(ConcreteStateObserver.get_instance(), GameLoopContainer, PygameEventFactory)
    client_service.run()
