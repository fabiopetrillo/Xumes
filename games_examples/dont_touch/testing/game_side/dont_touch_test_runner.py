import sys
import logging

import pygame

from games_examples.dont_touch.src.components.hand import Hand
from games_examples.dont_touch.src.components.player import Player
from games_examples.dont_touch.src.components.scoreboard import Scoreboard
from games_examples.dont_touch.src.global_state import GlobalState
from games_examples.dont_touch.play import Game
from games_examples.dont_touch.src.services.visualization_service import VisualizationService
from games_examples.dont_touch.src.utils.tools import is_close_app_event, update_background_using_scroll
from games_examples.dont_touch.src.components.hand_side import HandSide

from xumes.game_module import TestRunner, GameService, PygameEventFactory, CommunicationServiceGameMq, State


class DontTouchTestRunner(TestRunner):

    def __init__(self):
        super().__init__()
        self.game = Game()
        self.game = self.bind(self.game, "game", state=State("terminated", methods_to_observe=["reset"]))

        def get_pos(pos):
            return [pos.x, pos.y]

        self.P1 = self.bind(Player(), name="player", state=[
            State("player_position", [State("x", func=get_pos), State("y", func=get_pos)], methods_to_observe="update"),
        ])
        self.H1 = self.bind(Hand(HandSide.RIGHT), name="right_hand", state=[
            State("new_x", methods_to_observe="move"),
            State("new_y", methods_to_observe="move"),
            State("new_spd", methods_to_observe="move")
        ])
        self.H2 = self.bind(Hand(HandSide.LEFT), name="left_hand", state=[
            State("new_x", methods_to_observe="move"),
            State("new_y", methods_to_observe="move"),
            State("new_spd", methods_to_observe="move")
        ])
        self.scoreboard = self.bind(Scoreboard(), name="scoreboard", state=[
            State("_current_score", methods_to_observe="increase_current_score"),
            State("_max_score", methods_to_observe="update_max_score")
        ])

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

if __name__ == "__main__":

    if len(sys.argv) > 1:
        if sys.argv[1] == "-test":
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
        if sys.argv[1] == "-render":
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

        game_service = GameService(test_runner=DontTouchTestRunner(),
                                   event_factory=PygameEventFactory(),
                                   communication_service=CommunicationServiceGameMq(ip="localhost"))
        if sys.argv[1] == "-test":
            game_service.run()
        if sys.argv[1] == "-render":
            game_service.run_render()

    else:
        game = Game()
        game.run()
