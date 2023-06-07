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
        """
        Run two threads:\n
        - The communication service thread, used to send state and get actions.\n
        - The game thread, used to make run the game loop.
        """
        self.app_thread = Thread(target=self.communication_service.run, args=[self])
        self.game_thread = Thread(target=self.test_runner.run_test)
        self.app_thread.start()
        self.game_thread.start()

        self.test_runner.delete_screen()

    def run_render(self):
        """
        Same has run but for the game thread, we run with rendering.
        """
        self.app_thread = Thread(target=self.communication_service.run, args=[self])
        self.game_thread = Thread(target=self.test_runner.run_test_render)

        self.app_thread.start()
        self.game_thread.start()

    def stop(self):
        """
        Stop both threads.
        """
        self.game_thread.join()
        self.app_thread.join()

    def wait(self):
        """
        First executed method in the game loop, used to make the game
        wait for an event send by the training service.
        """

        # Notify the communication service to send the state to
        # the training service.
        with self.get_state_condition:
            self.get_state_condition.notify()

        # Clear every previous events
        self.event_factory.clear()

        # Stop every previous events
        for key_input in self.inputs:
            key_input.release()
        self.inputs.clear()

        # Wait event
        with self.game_update_condition:
            self.game_update_condition.wait()

        # Run new events
        for key_input in self.inputs:
            key_input.press()

    def update_event(self, event: str):
        """
        Method used to accept external modification on the game,
        like reset.
        :param event: representation of an extern event on the game like reset.
        """
        if event == "reset":
            self.test_runner.reset()
        if event == "random_reset":
            self.test_runner.random_reset()
        self.test_runner.update_state("playing")
