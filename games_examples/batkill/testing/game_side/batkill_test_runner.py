import sys
import random

import pygame
from xumes.game_module.game_service import GameService
from xumes.game_module.implementations.mq_impl.communication_service_game_mq import CommunicationServiceGameMq
from xumes.game_module.implementations.pygame_impl.pygame_event_factory import PygameEventFactory
from xumes.game_module.implementations.rest_impl.json_game_state_observer import JsonGameStateObserver
from xumes.game_module.implementations.rest_impl.json_test_runner import JsonTestRunner

from games_examples.batkill.play import Game, worldx, bat_sprite_path, nb_bats
from games_examples.batkill.testing.game_side.batkill_observables import PlayerObservable, BatObservable


# Method random_bat have to be override in order to have BatObservable
def random_bat(observers, name, sprite_path, current_score, base_prob=20, base_speed=6):
    current_score = 0 if current_score < 0 else current_score
    current_odds = base_prob - current_score / 15
    speed = int(base_speed * (1 + current_score / 20))
    if (random.random() * current_odds) + 1 > current_odds:
        return BatObservable(direction=random.choice([-1, 1]), step=speed, sprite_path=sprite_path, observers=observers, name=name)
    else:
        return None


class BatKillerTestRunner(Game, JsonTestRunner):

    def __init__(self, observers):
        Game.__init__(self, max_bats=nb_bats, bat_speed=6, attack_cooldown=10, jump=False)
        JsonTestRunner.__init__(self, game_loop_object=self, observers=observers)

        self.collider_rect = pygame.Rect(335, 673, 30, 54)  # left, top, width, height
        self.rect = pygame.Rect(300, 653, 100, 74)
        self.player.sp = PlayerObservable(ground_y=653, rect=self.rect, collider_rect=self.collider_rect,
                                          x_step=12, attack_cooldown=self.attack_cooldown,
                                          observers=observers, name="player")

    def game_over(self):
        if self.player.sp.lives < 1:
            self.update_state("lose")

    def run_test(self) -> None:
        while True:
            self.test_client.wait()

            attained_score = 0
            action = self.input()

            if action is None:
                action = []
            self.actions = action

            self.player.control(action, self.dt)

            if any([v is None for v in self.sorted_bats.values()]):

                for k, v in self.sorted_bats.items():
                    if v is None:
                        new_bat = random_bat(current_score=self.player.sp.score, sprite_path=bat_sprite_path,
                                             base_speed=self.bat_speed, observers=self.observers, name="bat_"+str(k))
                        if new_bat:
                            self.sorted_bats[k] = new_bat
                            self.player_list.add(new_bat)
                            self.enemies.add(new_bat)
                            break

            for idx, bat in self.sorted_bats.items():
                if bat is not None:
                    bat.update()
                    if bat.collider_rect is not None:
                        bat.bool_collider_rect = True
                    if self.player.sp.attack.attack_poly is not None and not bat.dying:
                        killed = self.player.sp.attack.attack_poly.rect.colliderect(bat.collider_rect)
                        self.player.sp.bool_attack_rect = killed
                        if killed:
                            bat.die()
                            attained_score += 1
                    if bat.dead or bat.rect.x > worldx or bat.rect.x < 0:
                        self.enemies.remove(bat)
                        bat.kill()
                        bat.detach_all()
                        bat.notify()
                        self.sorted_bats[idx] = None
                    elif bat.collider_rect is not None and self.player.sp.collider_rect.colliderect(
                            bat.collider_rect):
                        bat.die()
                        self.player.sp.lives -= 1

            self.player.sp.score += attained_score

    def run_test_render(self) -> None:
        while True:
            self.test_client.wait()

            attained_score = 0
            action = self.input()

            if action is None:
                action = []
            self.actions = action

            self.player.control(action, self.dt)

            if any([v is None for v in self.sorted_bats.values()]):

                for k, v in self.sorted_bats.items():
                    if v is None:
                        new_bat = random_bat(current_score=self.player.sp.score, sprite_path=bat_sprite_path,
                                             base_speed=self.bat_speed, observers=self.observers, name="bat_"+str(k))
                        if new_bat:
                            # self.player.sp.bat_collider_rect = new_bat.collider_rect
                            self.sorted_bats[k] = new_bat
                            self.player_list.add(new_bat)
                            self.enemies.add(new_bat)
                            break

            for idx, bat in self.sorted_bats.items():
                if bat is not None:
                    bat.update()
                    if bat.collider_rect is not None:
                        self.player.sp.bat_collider_rect = bat.collider_rect
                    if self.player.sp.attack.attack_poly is not None and not bat.dying:
                        killed = self.player.sp.attack.attack_poly.rect.colliderect(bat.collider_rect)
                        if killed:
                            bat.die()
                            attained_score += 1
                    if bat.dead or bat.rect.x > worldx or bat.rect.x < 0:
                        self.enemies.remove(bat)
                        bat.kill()
                        self.sorted_bats[idx] = None
                        bat.detach_all()
                        bat.notify()
                        del bat
                    elif bat.collider_rect is not None and self.player.sp.collider_rect.colliderect(
                            bat.collider_rect):
                        bat.die()
                        self.player.sp.lives -= 1

            self.player.sp.score += attained_score

            self.render()

    def reset(self) -> None:
        self.player.sp.detach_all()
        for idx, bat in self.sorted_bats.items():
            if bat is not None:
                bat.detach_all()

        self.initialize_values()
        self.player.sp = PlayerObservable(ground_y=653, rect=self.rect, collider_rect=self.collider_rect,
                                          x_step=12, attack_cooldown=self.attack_cooldown,
                                          observers=self.observers, name="player")

        self.player.sp.notify()
        for idx, bat in self.sorted_bats.items():
            if bat is not None:
                bat.notify()

    def random_reset(self) -> None:
        self.reset()

    def delete_screen(self) -> None:
        pass


if __name__ == "__main__":

    if len(sys.argv) == 2:
        game_service = GameService(observer=JsonGameStateObserver.get_instance(),
                                   test_runner=BatKillerTestRunner(observers=[JsonGameStateObserver.get_instance()]),
                                   event_factory=PygameEventFactory(),
                                   communication_service=CommunicationServiceGameMq(ip="localhost"))
        if sys.argv[1] == "-test":
            game_service.run()
        if sys.argv[1] == "-render":
            game_service.run_render()

    else:
        game = Game(max_bats=nb_bats, bat_speed=6, attack_cooldown=10, jump=False)
        game.run()
