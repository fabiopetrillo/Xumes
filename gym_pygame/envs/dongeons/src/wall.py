import pygame

from envs.dongeons.params import TILE_SIZE
from envs.dongeons.src.tile import Tile


class Wall(Tile):

    def __init__(self, x, y, board):
        super().__init__(x, y, board, "gray")

