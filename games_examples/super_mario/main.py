import pygame

from games_examples.super_mario.classes.Level import Level
from games_examples.super_mario.classes.Menu import Menu
from games_examples.super_mario.classes.Sound import Sound
from games_examples.super_mario.entities.Mario import Mario
from games_examples.super_mario.classes.Dashboard import Dashboard

windowSize = 640, 480


class Game:
    terminated = False

    def __init__(self):

        pygame.mixer.pre_init(44100, -16, 2, 4096)
        pygame.init()
        self.screen = pygame.display.set_mode(windowSize)
        self.max_frame_rate = 60
        self.dashboard = Dashboard("font.png", 8, self.screen)
        self.sound = Sound()
        self.level = Level(self.screen, self.sound, self.dashboard)
        self.level.loadLevel("Level1-2")
        #self.menu = Menu(self.screen, self.dashboard, self.level, self.sound)
        self.mario = Mario(0, 0, self.level, self.screen, self.dashboard, self.sound)
        self.clock = pygame.time.Clock()
        #self.mario = None
        #self.clock = None

    def run(self):
        #while not self.menu.start:
            #self.menu.update()

        while True:
            pygame.display.set_caption("Super Mario running with {:d} FPS".format(int(self.clock.get_fps())))
            #if self.mario.pause:
            #    self.mario.pauseObj.update()
            #else:
            self.level.drawLevel(self.mario.camera)
            self.dashboard.update()
            self.mario.update()
            self.render()

            if self.mario.restart:
                self.terminated = True
                self.reset()



    def render(self):
        pygame.display.update()
        self.clock.tick(self.max_frame_rate)

    def reset(self):
        self.dashboard = Dashboard("font.png", 8, self.screen)
        self.sound = Sound()
        self.level = Level(self.screen, self.sound, self.dashboard)
        self.level.loadLevel("Level1-2")
        self.mario = Mario(0, 0, self.level, self.screen, self.dashboard, self.sound)
        self.clock = pygame.time.Clock()
        self.terminated = False




if __name__ == "__main__":
    game = Game()
    game.run()
