import pygame

from envs.hide_and_seek.params import TILE_SIZE
from envs.hide_and_seek.src.tile import Tile


class Ground(Tile):

    def __init__(self, x, y, board, has_coin=None):
        super().__init__(x, y, board, "green")
        self.has_coin = has_coin

    def draw(self, canvas):
        super().draw(canvas)
        if self.has_coin:
            gap_length = TILE_SIZE / 4
            coin_size = TILE_SIZE / 2
            rect = pygame.Rect(self.x*TILE_SIZE + gap_length, self.y*TILE_SIZE + gap_length, coin_size, coin_size)
            pygame.draw.rect(canvas, "yellow", rect)

