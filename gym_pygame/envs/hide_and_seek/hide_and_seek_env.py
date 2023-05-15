from __future__ import annotations

import random

import gymnasium as gym
import numpy as np
import pygame
from gymnasium import spaces

from envs.hide_and_seek.params import BOARD_SIZE, TILE_SIZE, BACKGROUND_COLOR
from envs.hide_and_seek.src.board import Board
from envs.hide_and_seek.src.entity import CONTROL_TOP, CONTROL_RIGHT, CONTROL_DOWN, CONTROL_LEFT
from envs.hide_and_seek.src.ground import Ground


class HideAndSeekEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}
    terminated = False
    previous_points = 0

    def __init__(self, render_mode=None):
        self.board = Board(level=0)
        self.board_size_x, self.board_size_y = self.board.size_x, self.board.size_y
        board_total_size_x, board_total_size_y = BOARD_SIZE
        self.width = board_total_size_x * TILE_SIZE
        self.height = board_total_size_y * TILE_SIZE
        self.dt = 0.1
        self.time_since_point = 0
        self.observation_space = spaces.Dict(
            {
                "coin": spaces.Box(0,TILE_SIZE*20, shape=(2,), dtype=float),
                "lidar": spaces.Box(0, 1, shape=(len(self.board.lidar.sight_lines), ), dtype=float),
            }
        )

        # We have two actions jump and not jump
        self.action_space = spaces.Discrete(4)
        self.reset()

        # assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.window = None
        self.clock = None

    def _get_obs(self):
        distance_coin_map = {}
        for ground in self.board.ground_graph.keys():
            if ground.has_coin:
                nd = np.sqrt(np.power(ground.x - self.board.player.x, 2) + np.power(ground.y - self.board.player.y, 2))
                distance_coin_map[nd] = ground

        ground = distance_coin_map[min(distance_coin_map.keys())]
        lidar = [line.distance * 1.0 / 2000 for line in self.board.lidar.sight_lines]
        return {"lidar": np.array(lidar), "coin": np.array([self.board.player.x - ground.x, self.board.player.y - ground.y])}

    def _get_info(self):
        return {
            "points": self.board.player.points
        }

    def reset(self, seed=None, option=None, **kwargs):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)
        # level = random.choice(range(len(self.board.level_names)))
        self.board.reset(level=0)
        self.board_size_x, self.board_size_y = self.board.size_x, self.board.size_y
        self.time_since_point = 0
        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    def step(self, action):
        if action == 0:
            self.board.player.move(CONTROL_TOP, self.dt)
        elif action == 1:
            self.board.player.move(CONTROL_RIGHT, self.dt)
        elif action == 2:
            self.board.player.move(CONTROL_DOWN, self.dt)
        else:
            self.board.player.move(CONTROL_LEFT, self.dt)

        reward = 0
        terminated = False
        if self.board.player.check_if_coin():
            reward = 0.5
        if self.board.check_no_more_coins():
            if self.board.level + 1 < len(self.board.level_names):
                self.__init__(self.board.level + 1)
            else:
                terminated = True
            reward = 1
        if self.board.is_caught_by_enemy(self.dt):
            reward = -1
            terminated = True

        self.board.lidar.vision()
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
