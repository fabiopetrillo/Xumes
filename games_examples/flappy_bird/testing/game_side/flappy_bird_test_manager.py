import logging

from xumes.game_module.implementations.rest_impl.communication_service_test_manager_rest_api import \
    CommunicationServiceTestManagerRestApi
from xumes.game_module.test_manager import PygameTestManager, TEST_MODE, TRAIN_MODE, RENDER_MODE


test_manager = PygameTestManager(communication_service=CommunicationServiceTestManagerRestApi(ip='localhost', port=5000), mode=RENDER_MODE)
test_manager.test_all()

