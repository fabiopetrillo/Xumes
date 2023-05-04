import pygame

from src.pipe_generator import PipeGenerator
from src.lidar import Lidar
from src.player import Player

HEIGHT = 720
WIDTH = 1280
BACKGROUND_COLOR = (137, 207, 240)


class Game:
    height = HEIGHT
    width = WIDTH

    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.running = True

        self.dt = 0

        self.player = Player(position=self.height // 2, game=self, screen=self.screen)
        self.pipe_generator = PipeGenerator(game=self, screen=self.screen)
        self.lidar = Lidar(pipe_generator=self.pipe_generator, player=self.player, screen=self.screen)

    def run(self):
        while self.running:

            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Background
            self.screen.fill(BACKGROUND_COLOR)

            # Make all game state modification
            self.player.jump()
            self.pipe_generator.generator(self.dt)
            self.player.move(self.dt)
            self.pipe_generator.move(self.dt)

            # Use the lidar
            self.lidar.vision()

            # Draw every component
            self.player.draw()
            self.pipe_generator.draw()
            self.lidar.draw()

            # Print logs on screen
            self.player.logs()
            self.lidar.logs()
            self.pipe_generator.logs()

            # flip() the display to put your work on screen
            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            self.dt = self.clock.tick(60) / 1000

    def end(self):
        self.running = False
