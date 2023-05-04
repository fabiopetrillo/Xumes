import random

import pygame

from src.pipe import Pipe, PIPE_SPEED, PIPE_WIDTH

SPACE_BETWEEN_PIPES = 300


class PipeGenerator:

    def __init__(self, game=None, screen=None):
        self.pipes = []
        self.game = game
        self.time_between = (SPACE_BETWEEN_PIPES + PIPE_WIDTH) / PIPE_SPEED
        self.time_spent = 0
        self.screen = screen

    def gen_pipe(self):
        # Create a pipe with random height
        # TODO make an easy way to change how we compute the height (random or not)
        return Pipe(self.game.player, self, position=100+self.game.width, height=random.randint(200, self.game.height - 200), screen=self.screen)

    def generator(self, dt):
        self.time_spent += dt
        # We wait enough time and create a new pipe
        if self.time_spent > self.time_between:
            self.time_spent = 0
            self.pipes.append(self.gen_pipe())

    def move(self, dt):
        for pipe in self.pipes:
            pipe.move(dt)
            # if the pipe is out screen we delete him
            if pipe.position < -100:
                self.pipes.remove(pipe)

    def draw(self):
        for pipe in self.pipes:
            pipe.draw()

    def logs(self):
        my_font = pygame.font.SysFont('Arial', 14)
        text_surface = my_font.render(f'pipes: {len(self.pipes)}', False, (0, 0, 0))
        self.screen.blit(text_surface, (0, 20))

    def end(self):
        self.game.end()