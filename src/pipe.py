import pygame

from src.player import LEFT_POSITION, SIZE

PIPE_SPEED = 300
PIPE_WIDTH = 80


class Pipe:
    player_passed = False

    def __init__(self, player=None, generator=None, space_length=150, height=100, position=0, screen=None):
        self.space_length = space_length
        self.width = PIPE_WIDTH
        self.position = position
        self.height = height
        self.player = player
        self.generator = generator
        self.rect1 = pygame.Rect(self.position, 0, self.width, height)
        self.rect2 = pygame.Rect(self.position, self.space_length + self.height, self.width, generator.game.height - self.height)
        self.screen = screen

    def draw(self):
        pygame.draw.rect(self.screen, "green", self.rect1)
        pygame.draw.rect(self.screen, "green", self.rect2)

    def move(self, dt):
        # Go to left
        self.position -= dt * PIPE_SPEED
        # Move rectangles
        self.rect1 = pygame.Rect(self.position, 0, self.width, self.height)
        self.rect2 = pygame.Rect(self.position, self.space_length + self.height, self.width,
                      self.generator.game.height - self.height - self.space_length)

        # Check if collides with player
        self.collision()

        # Check if player passed the pipe (win one point)
        self.is_player_passed()

    def collision(self):
        # if the pipe collides we stop the game
        if (
                self.position <= SIZE + LEFT_POSITION <= self.position + PIPE_WIDTH or self.position <= LEFT_POSITION <= self.position + PIPE_WIDTH) and (
                self.player.position <= self.height or self.player.position + SIZE >= self.space_length + self.height):
            self.generator.end()

    def is_player_passed(self):
        if self.position <= SIZE + LEFT_POSITION and not self.player_passed:
            self.player_passed = True
            self.player.points += 1
