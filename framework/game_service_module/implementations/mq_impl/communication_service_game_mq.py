import json

import zmq

from framework.game_service_module.i_communication_service_game import ICommunicationServiceGame
from framework.game_service_module.errors.key_not_found_error import KeyNotFoundError


class CommunicationServiceGameMq(ICommunicationServiceGame):

    def __init__(self, ip):
        context = zmq.Context()

        print("Connecting to training server...")
        self.socket = context.socket(zmq.REQ)
        self.socket.connect(f"tcp://{ip}:5555")

    def observe(self, game_service) -> None:
        self.socket.send(json.dumps(game_service.observer.get_state()).encode("utf-8"))

    def action(self, game_service) -> None:
        # Get message from training service
        message = eval(self.socket.recv().decode("utf-8"))

        game_service.update_event(message['event'])
        # For every input try the build a game event
        # And add it to inputs list.
        for input_str in message['inputs']:
            try:
                key_input = game_service.event_factory.find_input(input_str)
                game_service.inputs.append(key_input)
            except KeyNotFoundError:
                pass

        # Notify that the game is ready to update.
        with game_service.game_update_condition:
            game_service.game_update_condition.notify()

    def run(self, game_service):
        while True:
            # Wait the game loop to finish iteration
            with game_service.get_state_condition:
                game_service.get_state_condition.wait()
            self.observe(game_service)
            self.action(game_service)
