import json
from typing import List

import zmq

from framework.training_service_module.i_communication_service import ICommunicationService


class CommunicationServiceMq(ICommunicationService):
    def __init__(self):
        print("Training server creation...")
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind("tcp://*:5555")

    def push_event(self, event) -> None:
        try:
            self.socket.send(json.dumps({
                              'event': event,
                              'inputs': []
                            }).encode("utf-8"))
        except Exception:
            pass

    def push_actions(self, actions) -> None:
        self.socket.send(json.dumps({
                          'inputs': actions,
                          'event': ''
                      }).encode("utf-8"))

    def get_states(self) -> List:
        return json.loads(eval(self.socket.recv().decode("utf-8"))).items()
