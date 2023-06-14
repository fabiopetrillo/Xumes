import sys
import random

import pygame
from xumes.game_module.game_service import GameService
from xumes.game_module.implementations.mq_impl.communication_service_game_mq import CommunicationServiceGameMq
from xumes.game_module.implementations.pygame_impl.pygame_event_factory import PygameEventFactory
from xumes.game_module.implementations.rest_impl.json_game_state_observer import JsonGameStateObserver
from xumes.game_module.implementations.rest_impl.json_test_runner import JsonTestRunner

from games_examples.batkill.play import Game, bat_sprite_path, adventurer_sprites, background
from games_examples.batkill.testing.game_side.batkill_observables import PlayerObservable, BatObservable


# Method random_bat have to be override in order to have BatObservable
def random_bat(sprite_path, current_score, base_prob=20, base_speed=6):
    current_score = 0 if current_score < 0 else current_score
    current_odds = base_prob - current_score / 15
    speed = int(base_speed * (1 + current_score / 20))
    if (random.random() * current_odds) + 1 > current_odds:
        return BatObservable(direction=random.choice([-1, 1]), step=speed, sprite_path=sprite_path)
    else:
        return None


class BatKillerTestRunner(Game, JsonTestRunner):

    def __init__(self, observers):
        Game.__init__(self)
        JsonTestRunner.__init__(self, game_loop_object=self, observers=observers)

        collider_rect = pygame.Rect(335, 673, 30, 54)  # left, top, width, height
        rect = pygame.Rect(300, 653, 100, 74)
        self.player.sp = PlayerObservable.__init__(self, ground_y=653, rect=rect, collider_rect=collider_rect,
                                                   x_step=12, attack_cooldown=self.attack_cooldown)

    #        self.bat = BatObservable(self, observers=observers, name="bat")

    def run_test(self) -> None:
        while True:
            self.test_client.wait()

            attained_score = 0
            action = self.input()  # Command(self.gameInput()).key_pressed

            if action is None:
                action = []
            self.actions = action

            self.player.control(action, self.dt)

            if any([v is None for v in self.sorted_bats.values()]):
                new_bat = random_bat(current_score=self.score, sprite_path=bat_sprite_path, base_speed=self.bat_speed)
                if new_bat:
                    for k, v in self.sorted_bats.items():
                        if v is None:
                            self.sorted_bats[k] = new_bat
                            self.player_list.add(new_bat)
                            self.enemies.add(new_bat)
                            break

            for idx, bat in self.sorted_bats.items():
                if bat is not None:
                    bat.update()
                    if bat.direction == -1:
                        if bat.rect.x < self.player.sp.rect.x:
                            moving_towards = True
                    else:
                        if bat.rect.x > self.player.sp.rect.x:
                            moving_towards = True

                    if self.player.sp.attack.attack_poly is not None and not bat.dying:
                        killed = self.player.sp.attack.attack_poly.rect.colliderect(bat.collider_rect)
                        if killed:
                            bat.die()
                            attained_score += 1
                    if bat.dead or bat.rect.x > self.worldx or bat.rect.x < 0:
                        self.enemies.remove(bat)
                        bat.kill()
                        self.sorted_bats[idx] = None
                        del bat
                    elif bat.collider_rect is not None and self.player.sp.collider_rect.colliderect(bat.collider_rect):
                        bat.die()
                        self.lives -= 1

            self.score += attained_score

    def run_test_render(self) -> None:
        while True:
            self.test_client.wait()

            moving_towards = False
            attained_score = 0
            action = self.input()  # Command(self.gameInput()).key_pressed

            if action is None:
                action = []
            self.actions = action

            self.player.control(action, self.dt)

            if any([v is None for v in self.sorted_bats.values()]):
                new_bat = random_bat(current_score=self.score, sprite_path=bat_sprite_path, base_speed=self.bat_speed)
                if new_bat:
                    for k, v in self.sorted_bats.items():
                        if v is None:
                            self.sorted_bats[k] = new_bat
                            self.player_list.add(new_bat)
                            self.enemies.add(new_bat)
                            break

            for idx, bat in self.sorted_bats.items():
                if bat is not None:
                    bat.update()
                    if bat.direction == -1:
                        if bat.rect.x < self.player.sp.rect.x:
                            moving_towards = True
                    else:
                        if bat.rect.x > self.player.sp.rect.x:
                            moving_towards = True

                    if self.player.sp.attack.attack_poly is not None and not bat.dying:
                        killed = self.player.sp.attack.attack_poly.rect.colliderect(bat.collider_rect)
                        if killed:
                            bat.die()
                            attained_score += 1
                    if bat.dead or bat.rect.x > self.worldx or bat.rect.x < 0:
                        self.enemies.remove(bat)
                        bat.kill()
                        self.sorted_bats[idx] = None
                        del bat
                    elif bat.collider_rect is not None and self.player.sp.collider_rect.colliderect(bat.collider_rect):
                        bat.die()
                        self.lives -= 1

            self.score += attained_score

            self.render(custom_message='Manual Play')

    def reset(self) -> None:
        self.player.detach_all()
        self.bat.detach_all()

        self.initialize_values()

        self.player.notify()
        self.bat.notify()

    def delete_screen(self) -> None:
        pass


if __name__ == "__main__":

    if len(sys.argv) == 2:
        game_service = GameService(observer=JsonGameStateObserver.get_instance(),
                                   test_runner=BatKillerTestRunner(observers=[JsonGameStateObserver.get_instance()]),
                                   event_factory=PygameEventFactory(),
                                   communication_service=CommunicationServiceGameMq(ip="localhost"))
        if sys.argv[1] == "-tests":
            game_service.run()
        if sys.argv[1] == "-render":
            game_service.run_render()

    else:
        game = Game()
        game.run()
