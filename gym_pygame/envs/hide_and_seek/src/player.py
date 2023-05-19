from abc import ABC

import pygame

from envs.hide_and_seek.params import PLAYER_SIZE
from envs.hide_and_seek.src.entity import RIGHT, LEFT, TOP, Entity, CONTROL_TOP, CONTROL_DOWN, CONTROL_LEFT, CONTROL_RIGHT, \
    get_tile_from_position
from envs.hide_and_seek.src.ground import Ground


class Player(Entity, ABC):
    def __init__(self, x, y, board):
        super().__init__(x, y, board)
        self.size_x, self.size_y = PLAYER_SIZE
        self.speed = 150
        self.points = 0

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

    def logs(self, canvas):
        my_font = pygame.font.SysFont('Arial', 14)
        text_surface = my_font.render(f'points: {self.points}',
                                      False, (0, 0, 0))
        canvas.blit(text_surface, (0, 0))

    def check_if_coin(self):
        # Check if there is coin on the tile where the player is
        center_x, center_y = self.center()
        tile_x, tile_y = get_tile_from_position(center_x, center_y)
        tile = self.board.board[tile_x][tile_y]
        if tile and isinstance(tile, Ground):
            if tile.has_coin and tile.in_coin(center_x, center_y):
                self.points += 1
                tile.has_coin = False
                return True
        return False
