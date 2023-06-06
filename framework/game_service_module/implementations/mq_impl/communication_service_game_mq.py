import json
import time

import zmq

from framework.game_service_module.i_communication_service_game import ICommunicationServiceGame
from framework.game_service_module.exceptions.key_not_found_exception import KeyNotFoundException


class CommunicationServiceGameMq(ICommunicationServiceGame):

    def __init__(self, ip):
        context = zmq.Context()

        print("Connecting to training server...")
        self.socket = context.socket(zmq.REQ)
        self.socket.connect(f"tcp://{ip}:5555")

    def observe(self, client_service) -> None:


        # with client_service.get_state_condition:
        #     client_service.get_state_condition.wait()
        self.socket.send(json.dumps(client_service.observer.get_state()).encode("utf-8"))

    def action(self, client_service) -> None:
        message = eval(self.socket.recv().decode("utf-8"))
        client_service.update_event(message['event'])
        for input_str in message['inputs']:
            try:
                key_input = client_service.event_factory.find_input(input_str)
                client_service.inputs.append(key_input)
            except KeyNotFoundException:
                pass

        with client_service.game_update_condition:
            client_service.game_update_condition.notify()

    def run(self, client_service):
        while True:
            with client_service.get_state_condition:
                client_service.get_state_condition.wait()
            self.observe(client_service)
            self.action(client_service)
