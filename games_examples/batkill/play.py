"""
Objects
"""

import os
import sys

import pygame

from games_examples.batkill.src.backend_player import MOVE_LEFT, MOVE_RIGHT, JUMP, ATTACK
from games_examples.batkill.src.enemy_generation import random_bat
from games_examples.batkill.src.moving_tut import Player

bat_sprite_path = os.path.join('static', 'sprites', 'Bat')
background = os.path.join('static', 'backgrounds', 'forest', 'background.png')
adventurer_sprites = os.path.join('static', 'sprites', 'adventurer')


class Game:
    worldx = 928
    worldy = 793

    metadata = {'render.modes': ['human']}

    def __init__(self, max_bats=2):
        self.max_bats = max_bats
        self.initialize_values()

    def initialize_values(self):
        pygame.init()
        pygame.font.init()

        self.deterministic_bats = False
        self.sorted_bats = {n: None for n in range(self.max_bats)}

        self.lives = 5
        self.score = 0

        self.fps = 30  # frame rate
        self.clock = pygame.time.Clock()

        self.world = pygame.display.set_mode([self.worldx, self.worldy])
        self.backdrop = pygame.image.load(background).convert()
        self.backdropbox = self.world.get_rect()
        self.player = Player(adventurer_sprites)  # spawn player
        self.player_list = pygame.sprite.Group()
        self.player_list.add(self.player)

        self.score_font = pygame.font.SysFont(os.path.join('static', 'fonts', 'SourceCodePro-Medium.ttf'), 30)
        self.score_surface = self.score_font.render(f"SCORE: {round(self.score * 1000)}, LIVES: {self.lives}", True,
                                                    (0, 0, 0, 0))

        self.enemies = pygame.sprite.Group()
        self.running = True

    def get_actions(self):

        player_actions = []
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_actions.append(MOVE_LEFT)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_actions.append(MOVE_RIGHT)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_actions.append(JUMP)
        if keys[pygame.K_SPACE]:
            player_actions.append(ATTACK)
        return player_actions

    def run(self):

        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.running = False
                    sys.exit()

            attained_score = 0
            self.actions = self.get_actions()

            self.player.control(self.actions)

            if any([v is None for v in self.sorted_bats.values()]):
                new_bat = random_bat(current_score=self.score, sprite_path=bat_sprite_path)
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

    def render(self, custom_message=None, **kwargs):
        self.world.blit(self.backdrop, self.backdropbox)
        score_surface = self.score_font.render(f"SCORE: {round(self.score * 1000)}, LIVES: {self.lives}", True,
                                               (0, 0, 0, 0))
        self.world.blit(score_surface, (10, 10))
        if custom_message is not None:
            custom_message_surface = self.score_font.render(str(custom_message), True, (0, 0, 0, 0))
            self.world.blit(custom_message_surface, (10, 30))
        self.player.update()
        self.player_list.draw(self.world)
        self.player_list.draw(self.world)
        pygame.display.flip()
        self.clock.tick(self.fps)

    def reset(self):
        self.initialize_values()


if __name__ == "__main__":
    game = Game(max_bats=5)
    game.run()
