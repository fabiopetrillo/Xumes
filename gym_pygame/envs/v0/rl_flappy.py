from __future__ import annotations

import gymnasium as gym
import numpy as np
import pygame
from gymnasium import spaces

from envs.params import HEIGHT, LIDAR_MAX_DIST, WIDTH
from envs.v0.src.lidar import Lidar
from envs.v0.src.pipe_generator import PipeGenerator
from envs.v0.src.player import Player

# Screen
BACKGROUND_COLOR = (137, 207, 240)


class FlappyEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}
    terminated = False
    previous_points = 0
    def __init__(self, render_mode=None):
        self.player = Player(position=HEIGHT // 2, game=self)
        self.pipe_generator = PipeGenerator(game=self)
        self.lidar = Lidar(pipe_generator=self.pipe_generator, player=self.player)
        self.dt = 0.09
        self.observation_space = spaces.Dict(
            {
                "speedup": spaces.Box(-float('inf'), 300, shape=(1,), dtype=float),
                "lidar": spaces.Box(0, LIDAR_MAX_DIST, shape=(len(self.lidar.sight_lines),), dtype=float),
            }
        )

        # We have two actions jump and not jump
        self.action_space = spaces.Discrete(1)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.window = None
        self.clock = None

    def _get_obs(self):
        lidar = [line.distance for line in self.lidar.sight_lines]
        return {"speedup": np.array(self.player.speedup), "lidar": np.array(lidar)}

    def _get_info(self):
        return {
            "distance": self.player.distance,
            "points": self.player.points,
            "position": self.player.position,
            "speedup": self.player.speedup,
            "pipes": len(self.pipe_generator.pipes)
        }

    def reset(self, seed=None, option=None, **kwargs):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        observation = self._get_obs()
        info = self._get_info()

        self.pipe_generator.reset()
        self.player.reset()
        self.lidar.reset()
        self.terminated = False
        self.previous_points = 0

        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    def step(self, action):

        if action[0] == 1:
            self.player.jump()

            # if not self.render_mode == "human" or self.human_dt > self.learn_dt:
            #     self.human_dt = 0
            # self.human_dt += self.dt

        self.pipe_generator.generator(self.dt)
        self.player.move(self.dt)
        self.pipe_generator.move(self.dt)
        self.lidar.vision()

        terminated = self.terminated
        # if self.player.reward:
        #     reward = 1
        #     self.player.reward = False
        # else:
        #     reward = 0

        reward = self.player.points - self.previous_points
        self.previous_points = self.player.points

        if terminated:
            reward = -1


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
                (WIDTH, HEIGHT)
            )
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((WIDTH, HEIGHT))
        canvas.fill(BACKGROUND_COLOR)

        # First we draw the pipes
        self.pipe_generator.draw(canvas)
        # Now we draw the agent
        self.player.draw(canvas)
        # And finaly we draw the lidar
        # self.lidar.draw(canvas)

        # self.pipe_generator.logs(canvas)
        # self.player.logs(canvas)
        # self.lidar.logs(canvas)

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
