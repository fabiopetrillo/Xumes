from flask import Flask, request

from framework.game_service_module.i_communication_service_game import ICommunicationServiceGame
from framework.game_service_module.exceptions.key_not_found_exception import KeyNotFoundException


class CommunicationServiceGameRestApi(ICommunicationServiceGame):

    def __init__(self):
        self.app = Flask(__name__)

    def observe(self, client_service) -> None:
        @self.app.route("/", methods=['GET'])
        def get():
            with client_service.game_update_condition:
                client_service.game_update_condition.notify()
            with client_service.get_state_condition:
                client_service.get_state_condition.wait()

            return client_service.observer.get_state()

    def action(self, client_service):
        @self.app.route("/", methods=['POST'])
        def post():
            client_service.update_event(request.json['event'])
            for input_str in request.json['inputs']:
                try:
                    key_input = client_service.event_factory.find_input(input_str)
                except KeyNotFoundException:
                    return f"key {input_str} not found!"
                client_service.inputs.append(key_input)

            with client_service.game_update_condition:
                client_service.game_update_condition.notify()
            return "input send!"

    def run(self, client_service) -> None:
        self.app.run()
