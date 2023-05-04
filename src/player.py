import pygame

JUMP_SPEEDUP = 300
FALL_SPEEDUP = 10
SIZE = 40

PLAYER_COLOR = "yellow"
LEFT_POSITION = 100


class Player:
    speedup = 0
    points = 0

    def __init__(self, position=None, game=None, screen=None):
        self.position = position
        self.game = game
        self.screen = screen

    def jump(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.speedup = JUMP_SPEEDUP

    def move(self, dt):
        self.position -= self.speedup * dt
        self.speedup -= FALL_SPEEDUP
        self.collision()

    def collision(self):
        if self.position > self.game.height - SIZE:
            self.game.end()

    def draw(self):
        pygame.draw.rect(self.screen, PLAYER_COLOR, (LEFT_POSITION, self.position, SIZE, SIZE))

    def logs(self):
        my_font = pygame.font.SysFont('Arial', 14)
        text_surface = my_font.render(f'points: {self.points } speedup: {self.speedup} position: {int(self.position)}', False, (0, 0, 0))
        self.screen.blit(text_surface, (0, 0))

    def center(self):
        return LEFT_POSITION + SIZE / 2, self.position + SIZE / 2
