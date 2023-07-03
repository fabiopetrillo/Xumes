import sys

import pygame

from xumes.game_module.implementations.rest_impl.json_test_runner import JsonTestRunner

from games_examples.dont_touch.src.global_state import GlobalState
from games_examples.dont_touch.play import Game
from games_examples.dont_touch.src.services.visualization_service import VisualizationService
from games_examples.dont_touch.src.utils.tools import is_close_app_event, update_background_using_scroll
from games_examples.dont_touch.testing.game_side.dont_touch_observables import HandObservable, PlayerObservable, \
    ScoreBoardObservable
from games_examples.dont_touch.src.components.hand_side import HandSide
from src.xumes.game_module.state_observable import State
from src.xumes.game_module.test_runner import TestRunner


class DontTouchTestRunner(Game, TestRunner, JsonTestRunner):

    def __init__(self, observers):
        super().__init__()
        JsonTestRunner.__init__(self, game_loop_object=self, observers=observers)

        self.game = Game()
        self.game = self.bind(self.game, "game", state=State("terminated", methods_to_observe=["reset"]))
        self.P1 = PlayerObservable(observers=observers, name="player")
        self.H1 = HandObservable(HandSide.RIGHT, observers=observers, name="right_hand")
        self.H2 = HandObservable(HandSide.LEFT, observers=observers, name="left_hand")
        self.scoreboard = ScoreBoardObservable(observers=observers, name="scoreboard")

    def run_test(self) -> None:

        while True:

            self.test_client.wait()
            events = pygame.event.get()

            for event in events:
                if is_close_app_event(event):
                    self.reset()
                    pygame.quit()
                    sys.exit()

            self.P1.update()
            self.H1.move(self.scoreboard, self.P1.player_position)
            self.H2.move(self.scoreboard, self.P1.player_position)

            GlobalState.SCROLL = update_background_using_scroll(GlobalState.SCROLL)
            VisualizationService.draw_background_with_scroll(GlobalState.SCREEN, GlobalState.SCROLL)

            self.game.dt = 0.09

    def run_test_render(self) -> None:

        while True:
            self.test_client.wait()

            events = pygame.event.get()

            for event in events:
                if is_close_app_event(event):
                    self.reset()
                    pygame.quit()
                    sys.exit()

            self.P1.update()
            self.H1.move(self.scoreboard, self.P1.player_position)
            self.H2.move(self.scoreboard, self.P1.player_position)

            GlobalState.SCROLL = update_background_using_scroll(GlobalState.SCROLL)
            VisualizationService.draw_background_with_scroll(GlobalState.SCREEN, GlobalState.SCROLL)

            self.render()

    def reset(self) -> None:
        self.game.reset()

    def random_reset(self) -> None:
        self.reset()

    def delete_screen(self) -> None:
        pass

