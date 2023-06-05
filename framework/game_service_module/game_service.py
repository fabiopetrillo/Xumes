from threading import Thread, Condition

from framework.game_service_module.i_communication_service_game import ICommunicationServiceGame
from framework.game_service_module.event_factory import IEventFactory
from framework.game_service_module.i_game_state_observer import IGameStateObserver
from framework.game_service_module.test_runner import _TestRunner


class GameService:

    def __init__(self,
                 observer: IGameStateObserver,
                 test_runner: _TestRunner,
                 event_factory: IEventFactory,
                 communication_service: ICommunicationServiceGame):

        self.nb_frame = 0
        self.app_thread = None
        self.game_thread = None
        self.game_update_condition = Condition()
        self.get_state_condition = Condition()
        self.observer = observer
        self.test_runner = test_runner
        self.test_runner.set_client(self)
        self.test_runner.update_state("playing")

        self.event_factory = event_factory
        self.inputs = []
        self.communication_service = communication_service

        self.communication_service.observe(self)
        self.communication_service.action(self)

    def run(self):
        self.app_thread = Thread(target=self.communication_service.run, args=[self])
        self.game_thread = Thread(target=self.test_runner.run_test)
        self.app_thread.start()
        self.game_thread.start()

        self.test_runner.delete_screen()

    def run_render(self):
        self.app_thread = Thread(target=self.communication_service.run, args=[self])
        self.game_thread = Thread(target=self.test_runner.run_test_render)

        self.app_thread.start()
        self.game_thread.start()

    def stop(self):
        self.game_thread.join()
        self.app_thread.join()

    def wait(self):

        with self.get_state_condition:
            self.get_state_condition.notify()

        self.nb_frame += 1
        # Clear every previous events
        self.event_factory.clear()

        # Stop every previous events
        for key_input in self.inputs:
            key_input.release()
        self.inputs.clear()

        # Wait event
        with self.game_update_condition:
            self.game_update_condition.wait()

        # Start new events
        for key_input in self.inputs:
            key_input.press()

    def update_event(self, event: str):
        if event == "reset":
            self.test_runner.reset()
        if event == "random_reset":
            self.test_runner.random_reset()
        self.test_runner.update_state("playing")
