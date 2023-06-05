from abc import ABC

import pygame

from gym_envs.hide_and_seek.params import TILE_SIZE


class Tile(ABC):

    def __init__(self, x, y, board, color):
        self.x = x
        self.y = y
        self.board = board
        self.rect = pygame.Rect((x * TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
        self.color = color

    def draw(self, canvas):
        pygame.draw.rect(canvas, self.color, self.rect)

    def __lt__(self, other):
        # Use with the A star algorithm
        return self.x + self.y < other.x + other.y
