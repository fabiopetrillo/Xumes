import json
from typing import List

import zmq

from framework.training_service_module.i_communication_service_training import ICommunicationServiceTraining


class CommunicationServiceTrainingMq(ICommunicationServiceTraining):
    def __init__(self):
        print("Training server creation...")
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind("tcp://*:5555")

    def push_event(self, event: str) -> None:
        try:
            self.socket.send(json.dumps({
                              'event': event,
                              'inputs': []
                            }).encode("utf-8"))
        except Exception:
            pass

    def push_actions(self, actions: List[str]) -> None:
        self.socket.send(json.dumps({
                          'inputs': actions,
                          'event': ''
                      }).encode("utf-8"))

    def get_states(self) -> List:
        # Use .items to convert dict to list of tuple (KEY, VALUE).
        return json.loads(eval(self.socket.recv().decode("utf-8"))).items()
