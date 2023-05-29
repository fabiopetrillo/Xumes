from flask import Flask, request

from game_service.communication_service import ICommunicationService
from game_service.exceptions.key_not_found_exception import KeyNotFoundException


class CommunicationServiceRestApi(ICommunicationService):

    def __init__(self):
        self.app = Flask(__name__)

    def observe(self, client_service) -> None:
        @self.app.route("/", methods=['GET'])
        def get():
            return client_service.observer.get_state()

    def action(self, client_service):
        @self.app.route("/", methods=['POST'])
        def post():
            print(request.json)
            client_service.update_event(request.json['event'])
            for input_str in request.json['inputs']:
                try:
                    key_input = client_service.event_factory.find_input(input_str)
                except KeyNotFoundException:
                    return f"key {input_str} not found!"
                client_service.inputs.append(key_input)
            with client_service.condition:
                client_service.condition.notify()
            return "input send!"

    def run(self) -> None:
        self.app.run()
