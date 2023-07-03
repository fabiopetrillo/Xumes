import logging
import urllib
from time import sleep

import requests

from xumes.game_module.i_communication_service_test_manager import ICommunicationServiceTestManager


class CommunicationServiceTestManagerRestApi(ICommunicationServiceTestManager):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def connect_trainer(self, test_manager, feature, scenario) -> None:
        while True:
            try:
                # noinspection HttpUrlsUsage
                urllib.request.urlopen(f'http://{self.ip}:{self.port}/ping')
                break
            except Exception as e:
                logging.info(f"Waiting for connection with {self.ip}:{self.port}...")
                sleep(1)

        port = test_manager.get_port(feature, scenario)

        # noinspection HttpUrlsUsage
        requests.post(f'http://{self.ip}:{self.port}/connect',
                      json={
                          'feature': feature,
                          'scenario': scenario,
                          'port': port
                      })
        test_manager.add_game_service_data(steps=scenario, ip=self.ip, port=port)

    def disconnect_trainer(self, test_manager, feature, scenario) -> None:
        # noinspection HttpUrlsUsage
        requests.post(f'http://{self.ip}:{self.port}/disconnect',
                      json={
                          'feature': feature,
                          'scenario': scenario
                      })

    def start_training(self, test_manager) -> None:
        # noinspection HttpUrlsUsage
        requests.post(f'http://{self.ip}:{self.port}/start')

    def run(self, test_manager) -> None:
        pass

    def stop(self) -> None:
        pass
