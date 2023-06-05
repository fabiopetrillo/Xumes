from typing import List

import requests

from framework.training_service_module.i_communication_service import ICommunicationService


class CommunicationServiceRestApi(ICommunicationService):

    def __init__(self, url: str):
        self.url = url

    def push_event(self, event) -> None:
        requests.post(self.url,
                      json={
                          'event': event,
                          'inputs': []
                      })

    def push_actions(self, actions) -> None:
        requests.post(self.url,
                      json={
                          'inputs': actions,
                          'event': ''
                      })

    def get_states(self) -> List:
        return requests.get(self.url).json().items()
