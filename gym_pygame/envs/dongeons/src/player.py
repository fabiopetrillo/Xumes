from abc import ABC

import pygame

from envs.dongeons.params import PLAYER_SIZE
from envs.dongeons.src.Entity import RIGHT, LEFT, TOP, Entity, CONTROL_TOP, CONTROL_DOWN, CONTROL_LEFT, CONTROL_RIGHT


class Player(Entity, ABC):
    def __init__(self, x, y, board):
        super().__init__(x, y, board)
        self.size_x, self.size_y = PLAYER_SIZE
        self.speed = 150


    def find_control(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            return CONTROL_TOP
        elif keys[pygame.K_s]:
            return CONTROL_DOWN
        elif keys[pygame.K_q]:
            return CONTROL_LEFT
        elif keys[pygame.K_d]:
            return CONTROL_RIGHT

    def center(self):
        return self.x + self.size_x / 2, self.y + self.size_y / 2





    def draw(self, canvas):
        rect_bottom = pygame.Rect(self.x, self.y, self.size_x, self.size_y)
        pygame.draw.rect(canvas, "blue", rect_bottom)
