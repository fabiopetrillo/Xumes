
from xumes.game_module.game_service import GameService
from xumes.game_module.implementations.mq_impl.communication_service_game_mq import CommunicationServiceGameMq
from xumes.game_module.implementations.pygame_impl.pygame_event_factory import PygameEventFactory
from xumes.game_module.implementations.rest_impl.json_game_state_observer import JsonGameStateObserver
from xumes.game_module.implementations.rest_impl.json_test_runner import JsonTestRunner

class DontTouchTestRunner(Game, JsonTestRunner):

    def __init__(self, observers):
        Game.__init__(self, max_bats=nb_bats, bat_speed=6, attack_cooldown=10, jump=True)
        JsonTestRunner.__init__(self, game_loop_object=self, observers=observers)

