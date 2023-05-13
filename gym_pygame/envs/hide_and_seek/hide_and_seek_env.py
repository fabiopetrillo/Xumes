from __future__ import annotations

import gymnasium as gym
import numpy as np
import pygame
from gymnasium import spaces

from envs.hide_and_seek.params import BOARD_SIZE, TILE_SIZE, BACKGROUND_COLOR, VIEW_GRID_SIZE
from envs.hide_and_seek.src.board import Board
from envs.hide_and_seek.src.entity import CONTROL_TOP, CONTROL_RIGHT, CONTROL_DOWN, CONTROL_LEFT, get_tile_from_position
from envs.hide_and_seek.src.ground import Ground


class HideAndSeekEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}
    terminated = False
    previous_points = 0

    def __init__(self, render_mode=None):
        self.board = Board()
        self.board_size_x, self.board_size_y = self.board.size_x, self.board.size_y
        board_total_size_x, board_total_size_y = BOARD_SIZE
        self.width = board_total_size_x * TILE_SIZE
        self.height = board_total_size_y * TILE_SIZE
        self.dt = 0.1

        self.observation_space = spaces.Dict(
            {
                "type": spaces.Box(0, 1, shape=(VIEW_GRID_SIZE, VIEW_GRID_SIZE), dtype=float),
                "coin": spaces.Box(0, 1, shape=(VIEW_GRID_SIZE, VIEW_GRID_SIZE), dtype=float),
                "enemies": spaces.Box(0, 1, shape=(VIEW_GRID_SIZE, VIEW_GRID_SIZE), dtype=float),
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
        player_center_x, player_center_y = self.board.player.center()
        center_tile_x, center_tile_y = get_tile_from_position(player_center_x, player_center_y)
        tile_enemy_map = {}
        for enemy in self.board.enemies:
            enemy_center_x, enemy_center_y = enemy.center()
            enemy_center_tile_x, enemy_center_tile_y = get_tile_from_position(enemy_center_x, enemy_center_y)
            if self.board.board[enemy_center_tile_x][enemy_center_tile_y] in tile_enemy_map.keys():
                tile_enemy_map[self.board.board[enemy_center_tile_x][enemy_center_tile_y]].append(enemy)
            else:
                tile_enemy_map[self.board.board[enemy_center_tile_x][enemy_center_tile_y]] = [enemy]

        type_obs = np.zeros((VIEW_GRID_SIZE, VIEW_GRID_SIZE))
        coin_obs = np.zeros((VIEW_GRID_SIZE, VIEW_GRID_SIZE))
        enemies_obs = np.zeros((VIEW_GRID_SIZE, VIEW_GRID_SIZE))

        for i in range(center_tile_x - (VIEW_GRID_SIZE - 1) // 2, center_tile_x + (VIEW_GRID_SIZE - 1) // 2 + 1):
            for j in range(center_tile_y - (VIEW_GRID_SIZE - 1) // 2, center_tile_y + (VIEW_GRID_SIZE - 1) // 2 + 1):
                if 0 <= i < self.board_size_x-1 and 0 <= j < self.board_size_y-1:
                    tile = self.board.board[i][j]
                    array_x, array_y = i - center_tile_x + (VIEW_GRID_SIZE - 1) // 2,j - center_tile_y + (VIEW_GRID_SIZE - 1) // 2
                    if isinstance(tile, Ground):
                        type_obs[array_x][array_y] = 1
                        if tile.has_coin:
                            coin_obs[array_x][array_y] = 1
                        if tile in tile_enemy_map.keys():  # Not a lot of information for the enemies
                            enemy_ratio = len(tile_enemy_map[tile]) * 1.0 / len(self.board.enemies)
                            enemies_obs[array_x][array_y] = enemy_ratio

        return {"type": type_obs, "coin": coin_obs, "enemies": enemies_obs}

    def _get_info(self):
        return {
            "points": self.board.player.points
        }

    def reset(self, seed=None, option=None, **kwargs):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        self.board.reset()
        self.board_size_x, self.board_size_y = self.board.size_x, self.board.size_y

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    def step(self, action):
        choice = np.argmax(action)
        if choice == 0:
            self.board.player.move(CONTROL_TOP, self.dt)
        elif choice == 1:
            self.board.player.move(CONTROL_RIGHT, self.dt)
        elif choice == 2:
            self.board.player.move(CONTROL_DOWN, self.dt)
        else:
            self.board.player.move(CONTROL_LEFT, self.dt)

        reward = 0.1
        terminated = False
        if self.board.player.check_if_coin():
            reward = 0.5
        if self.board.check_no_more_coins():
            reward = 1
            terminated = True
        if self.board.is_caught_by_enemy(self.dt):
            reward = -1
            terminated = True

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
