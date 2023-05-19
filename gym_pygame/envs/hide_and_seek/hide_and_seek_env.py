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
        self.observation_space = spaces.Dict(
            {
                # "position_in_tile": spaces.Box(0, 1, shape=(2,), dtype=float),
                # "position": spaces.Box(0, 1, shape=(4,2), dtype=float),
                "position": spaces.Box(0, float('inf'), shape=(len(self.board.lidar.sight_lines),), dtype=float),
                "coin": spaces.Box(0, float('inf'), shape=(2,), dtype=float),
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
        total_x = BOARD_SIZE[0] * TILE_SIZE
        total_y = BOARD_SIZE[1] * TILE_SIZE
        try:
            coin = distance_coin_map[min(distance_coin_map.keys())]
            coin_x, coin_y = coin.x * TILE_SIZE + TILE_SIZE // 2 - player_center_x, coin.y * TILE_SIZE + TILE_SIZE // 2 - player_center_y
            # coin_x, coin_y = ((coin.x * TILE_SIZE + TILE_SIZE // 2 * 1.0) / total_x,
            #                   (coin.y * TILE_SIZE + TILE_SIZE // 2 * 1.0) / total_y)
        except:
            coin_x, coin_y = 0, 0




        lidar = [line.distance for line in self.board.lidar.sight_lines]
        return {
            # "around": type_obs,
            "coin": np.array([coin_x, coin_y]),
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
        # level = random.choice(range(len(self.board.level_names)))
        self.board.reset(level=LEVEL_TEST)
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
            reward = -0.5

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

        if self.render_mode == "human":
            # The following line copies our drawings from `canvas` to the visible window
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to keep the framerate stable.
            self.dt = self.clock.tick(self.metadata["render_fps"]) / 1000
        else:  # rgb_array
            self.dt = self.clock.tick() / 1000

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
