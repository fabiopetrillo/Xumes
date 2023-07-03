import sys
import time

import pygame

from games_examples.dont_touch.src.components.hand import Hand
from games_examples.dont_touch.src.components.hand_side import HandSide
from games_examples.dont_touch.src.components.player import Player
from games_examples.dont_touch.src.components.scoreboard import Scoreboard
from games_examples.dont_touch.src.config import Config
from games_examples.dont_touch.src.global_state import GlobalState
from games_examples.dont_touch.src.services.music_service import MusicService
from games_examples.dont_touch.src.services.visualization_service import VisualizationService
from games_examples.dont_touch.src.utils.tools import update_background_using_scroll, update_press_key, \
                                                      is_close_app_event

from games_examples.dont_touch.src.components.game_status import GameStatus


class Game:

    def __init__(self):

        pygame.init()

        self.FramePerSec = pygame.time.Clock()

        GlobalState.load_main_screen()
        VisualizationService.load_main_game_displays()

        self.scoreboard = Scoreboard()

        # Sprite Setup
        self.P1 = Player()
        self.H1 = Hand(HandSide.RIGHT)
        self.H2 = Hand(HandSide.LEFT)

        # Sprite Groups
        self.hands = pygame.sprite.Group()
        self.hands.add(self.H1)
        self.hands.add(self.H2)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.P1)
        self.all_sprites.add(self.H1)
        self.all_sprites.add(self.H2)

        GlobalState.SCROLL = update_background_using_scroll(GlobalState.SCROLL)
        VisualizationService.draw_background_with_scroll(GlobalState.SCREEN, GlobalState.SCROLL)
        GlobalState.PRESS_Y = update_press_key(GlobalState.PRESS_Y)
        VisualizationService.draw_main_menu(GlobalState.SCREEN, self.scoreboard.get_max_score(), GlobalState.PRESS_Y)

    def run(self):

        while True:

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

    def render(self):
        self.P1.draw(GlobalState.SCREEN)
        self.H1.draw(GlobalState.SCREEN)
        self.H2.draw(GlobalState.SCREEN)
        self.scoreboard.draw(GlobalState.SCREEN)

        if pygame.sprite.spritecollide(self.P1, self.hands, False, pygame.sprite.collide_mask):
            self.scoreboard.update_max_score()
            MusicService.play_slap_sound()
            time.sleep(0.5)
            self.reset()

        pygame.display.update()
        self.FramePerSec.tick(Config.FPS)

    def reset(self):
        self.P1.reset()
        self.H1.reset()
        self.H2.reset()
        self.scoreboard.reset_current_score()
        time.sleep(0.5)


if __name__ == "__main__":
    game = Game()
    game.run()
