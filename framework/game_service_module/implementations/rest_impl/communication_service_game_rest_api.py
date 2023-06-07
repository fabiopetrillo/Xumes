from flask import Flask, request

from framework.game_service_module.i_communication_service_game import ICommunicationServiceGame
from framework.game_service_module.errors.key_not_found_error import KeyNotFoundError


class CommunicationServiceGameRestApi(ICommunicationServiceGame):

    def __init__(self):
        self.app = Flask(__name__)

    def observe(self, game_service) -> None:
        @self.app.route("/", methods=['GET'])
        def get():
            # Send the game can update if it's not already done.
            with game_service.game_update_condition:
                game_service.game_update_condition.notify()

            # Wait the game to finish iteration.
            with game_service.get_state_condition:
                game_service.get_state_condition.wait()

            return game_service.observer.get_state()

    def action(self, game_service):
        @self.app.route("/", methods=['POST'])
        def post():
            game_service.update_event(request.json['event'])

            # For every input try the build a game event
            # And add it to inputs list.
            for input_str in request.json['inputs']:
                try:
                    key_input = game_service.event_factory.find_input(input_str)
                except KeyNotFoundError:
                    return f"key {input_str} not found!"
                game_service.inputs.append(key_input)

            # Notify that the game is ready to update.
            with game_service.game_update_condition:
                game_service.game_update_condition.notify()
            return "input send!"

    def run(self, game_service) -> None:
        self.app.run()
