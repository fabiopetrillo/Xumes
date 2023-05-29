from threading import Thread, Condition

from game_service.communication_service import ICommunicationService
from game_service.event_factory import IEventFactory
from game_service.game_state_observer import IGameStateObserver
from game_service.test_runner import _TestRunner


class ClientService:

    def __init__(self,
                 observer: IGameStateObserver,
                 test_runner: _TestRunner,
                 event_factory: IEventFactory,
                 communication_service: ICommunicationService):

        self.app_thread = None
        self.game_thread = None
        self.condition = Condition()
        self.observer = observer
        self.test_runner = test_runner
        self.test_runner.set_client(self)
        self.test_runner.update_state("playing")

        self.event_factory = event_factory
        self.inputs = []
        self.communication_service = communication_service

        self.communication_service.observe(self)
        self.communication_service.action(self)

        self.test_runner.quit_screen()

    def run(self):
        self.app_thread = Thread(target=self.communication_service.run)
        self.game_thread = Thread(target=self.test_runner.run_test)
        self.app_thread.start()
        self.game_thread.start()

    def stop(self):
        self.game_thread.join()
        self.app_thread.join()

    def wait(self):

        # Clear every previous events
        self.event_factory.clear()

        # Stop every previous events
        for key_input in self.inputs:
            key_input.release()
        self.inputs.clear()

        # Wait event
        with self.condition:
            self.condition.wait()

        # Start new events
        for key_input in self.inputs:
            key_input.press()

    def update_event(self, event: str):
        if event == "reset":
            self.test_runner.reset()
            self.test_runner.update_state("playing")

