from __future__ import annotations

import random

import gymnasium as gym
import numpy as np
import pygame
from gymnasium import spaces

from envs.hide_and_seek.params import BOARD_SIZE, TILE_SIZE, BACKGROUND_COLOR, VIEW_GRID_SIZE, LEVEL_TEST
from envs.hide_and_seek.src.board import Board
from envs.hide_and_seek.src.entity import CONTROL_TOP, CONTROL_RIGHT, CONTROL_DOWN, CONTROL_LEFT, get_tile_from_position
from envs.hide_and_seek.src.ground import Ground
from envs.hide_and_seek.src.wall import Wall


class HideAndSeekEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}
    terminated = False
    previous_points = 0

    def __init__(self, render_mode=None):
        self.board = Board(level=LEVEL_TEST)
        self.board_size_x, self.board_size_y = self.board.size_x, self.board.size_y
        board_total_size_x, board_total_size_y = BOARD_SIZE
        self.width = board_total_size_x * TILE_SIZE
        self.height = board_total_size_y * TILE_SIZE
        self.dt = 0.1
        self.time_since_point = 0
        self.coin_x, self.coin_y = 0, 0

        lidar = [[self.coin_x - line.end_x, self.coin_y - line.end_y, 0 if line.type == Wall else 1] for line in
                 self.board.lidar.sight_lines]
        self.lidars = [lidar for _ in range(5)]
        self.observation_space = spaces.Dict(
            {
                # "position_in_tile": spaces.Box(0, 1, shape=(2,), dtype=float),
                # "position": spaces.Box(0, 1, shape=(4,2), dtype=float),
                "position": spaces.Box(-1, float('inf'), shape=(len(self.board.lidar.sight_lines), 6), dtype=float),
                "coin": spaces.Box(0, float('inf'), shape=(2,), dtype=float),
                "enemy": spaces.Box(0, float('inf'), shape=(2,), dtype=float),

                # "around": spaces.Box(0, 1, shape=(VIEW_GRID_SIZE, VIEW_GRID_SIZE), dtype=float),
            }
        )

        # We have two actions jump and not jump
        self.action_space = spaces.Discrete(4)
        self.reset()

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.window = None
        self.clock = None

    def _get_obs(self):

        self.board.lidar.vision()
        player_center_x, player_center_y = self.board.player.center()

        distance_coin_map = {}
        for ground in self.board.ground_graph.keys():
            if ground.has_coin:
                distance_coin_map[np.abs(ground.x * TILE_SIZE + TILE_SIZE // 2 - player_center_x) + np.abs(
                    ground.y * TILE_SIZE + TILE_SIZE // 2 - player_center_y)] = ground
        try:
            coin = distance_coin_map[min(distance_coin_map.keys())]
            self.coin_x, self.coin_y = coin.x * TILE_SIZE + TILE_SIZE // 2, coin.y * TILE_SIZE + TILE_SIZE // 2
        except:
            self.coin_x, self.coin_y = 0, 0

        distance_enemy_map = {}
        for enemy in self.board.enemies:
            distance_enemy_map[np.abs(enemy.x * TILE_SIZE + TILE_SIZE // 2 - player_center_x) + np.abs(
                enemy.y * TILE_SIZE + TILE_SIZE // 2 - player_center_y)] = enemy
        try:
            enemy = distance_enemy_map[min(distance_enemy_map.keys())]
            self.enemy_x, self.enemy_y = enemy.x, enemy.y
        except:
            self.enemy_x, self.enemy_y = 0, 0

        lidar = [[np.abs(self.coin_x - line.end_x), np.abs(self.coin_y - line.end_y),
                  np.abs(self.enemy_x - line.end_x), np.abs(self.enemy_y - line.end_y),
                  line.distance,
                  0 if line.type == Wall else 1 if line.type == Ground else -1] for line in self.board.lidar.sight_lines]
        # self.lidars.pop(0)
        # self.lidars.append(lidar)
        return {
            # "around": type_obs,
            "enemy": np.array([np.abs(self.enemy_x - player_center_x), np.abs(self.enemy_y - player_center_y)]),
            "coin": np.array([np.abs(self.coin_x - player_center_x), np.abs(self.coin_y - player_center_y)]),
            "position": np.array(lidar)
            # "position": np.array([[top_left_x, top_left_y], [top_right_x, top_right_y], [bottom_left_x, bottom_left_y], [bottom_right_x, bottom_right_y]])
            # "position": np.array([[(top_left_corner_x % TILE_SIZE) * 1.0 / TILE_SIZE, (top_left_corner_y% TILE_SIZE) * 1.0 / TILE_SIZE], [(top_right_corner_x % TILE_SIZE) * 1.0 / TILE_SIZE, (top_right_corner_y % TILE_SIZE) * 1.0 / TILE_SIZE], [(bottom_left_corner_x % TILE_SIZE) * 1.0 / TILE_SIZE, (bottom_left_corner_y % TILE_SIZE) * 1.0 / TILE_SIZE], [(bottom_right_corner_x % TILE_SIZE) * 1.0 / TILE_SIZE, (bottom_right_corner_y % TILE_SIZE) * 1.0 / TILE_SIZE]]),
            # "position_in_tile": np.array([tile_x, tile_y]),
        }
        # "position": np.array([self.board.player.x % TILE_SIZE * 1.0 / TILE_SIZE, self.board.player.y % TILE_SIZE * 1.0 / TILE_SIZE])}

    def _get_info(self):
        return {
            "points": self.board.player.points
        }

    def reset(self, seed=None, **kwargs):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)
        level = random.choice(range(len(self.board.level_names)))
        self.board.reset(level=level)
        self.board_size_x, self.board_size_y = self.board.size_x, self.board.size_y
        self.time_since_point = 0
        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    def step(self, action):
        if action == 0:
            collide = self.board.player.move(CONTROL_TOP, self.dt)
        elif action == 1:
            collide = self.board.player.move(CONTROL_RIGHT, self.dt)
        elif action == 2:
            collide = self.board.player.move(CONTROL_DOWN, self.dt)
        else:
            collide = self.board.player.move(CONTROL_LEFT, self.dt)

        reward = 0
        terminated = False
        if self.board.player.check_if_coin():
            reward = 1
        if self.board.check_no_more_coins():
            terminated = True
            reward = 2
        if self.board.is_caught_by_enemy(self.dt):
            reward = -1
            terminated = True

        if reward == 0 and collide:
            reward = -0.1

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, False, info

    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.font.init()
            pygame.display.init()
            self.window = pygame.display.set_mode(
                (self.width, self.height)
            )
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((self.width, self.height))
        canvas.fill(BACKGROUND_COLOR)

        # Draw
        self.board.draw(canvas)

        my_font = pygame.font.SysFont('Arial', 14)
        text_surface = my_font.render(f'coin: {int(self.coin_y)} {int(self.coin_x)}',
                                      False, (0, 0, 0))
        canvas.blit(text_surface, (0, 15))

        if self.render_mode == "human":
            # The following line copies our drawings from `canvas` to the visible window
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to keep the framerate stable.
            self.dt = self.clock.tick(self.metadata["render_fps"]) / 1000
        else:  # rgb_array
            # self.dt = self.clock.tick() / 1000

            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )

    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
