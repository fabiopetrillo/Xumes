import pygame

from envs.hide_and_seek.params import HEIGHT, WIDTH, BACKGROUND_COLOR, TILE_SIZE, BOARD_SIZE
from envs.hide_and_seek.src.board import Board


class Game:

    def __init__(self):
        pygame.init()
        pygame.font.init()

        board_size_x, board_size_y = BOARD_SIZE
        self.width = board_size_x * TILE_SIZE
        self.height = board_size_y * TILE_SIZE
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.running = True

        self.dt = 0
        self.board = Board(level=0)

    def run(self):
        while self.running:
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Background
            self.screen.fill(BACKGROUND_COLOR)
            self.board.draw(self.screen)
            self.board.compute_state(self.dt)

            # flip() the display to put your work on screen
            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            self.dt = self.clock.tick(60) / 1000


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
