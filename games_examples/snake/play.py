from abc import ABC

import pygame
import sys
import random
from pygame.math import Vector2

from game_service.client_service import ClientService
from game_service.game_state_observer import JsonGameStateObserver
from game_service.pygame_helpers.pygame_event_factory import PygameEventFactory
from game_service.rest_helpers.communication_service_rest_api import CommunicationServiceRestApi
from game_service.state_observable import StateObservable
from game_service.test_runner import JsonTestRunner
from games_examples.snake.observables import SnakeObservable, FruitObservable

cell_size = 30
cell_number = 15


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False
        self.observable: StateObservable[Snake] = SnakeObservable(self)  # Need to be added
        self.observable.attach(JsonGameStateObserver.get_instance())  # Need to be added

    def draw_snake(self, screen):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (183, 111, 122), block_rect)

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

        self.observable.notify()  # Need to be added

    def add_block(self):
        self.new_block = True


class Fruit:
    def __init__(self):
        self.pos = None
        self.y = None
        self.x = None
        self.observable: StateObservable[Fruit] = FruitObservable(self)  # Need to be added
        self.observable.attach(JsonGameStateObserver.get_instance())  # Need to be added
        self.randomize()

    def draw_fruit(self, screen):
        fruit_rect = pygame.Rect(
            int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, (200, 100, 50), fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)
        self.observable.notify()  # Need to be added


class MainTestRunner(JsonTestRunner, ABC):

    def run_test(self) -> None:
        while True:
            self.test_client.wait()
            for event in pygame.event.get():
                self.game_loop.check_events(event)
            self.game_loop.update()
            self.game_loop.clock.tick(0)

    def reset(self) -> None:
        self.game_loop.snake.observable.detach_all()
        self.game_loop.fruit.observable.detach_all()

        self.game_loop.snake = Snake()
        self.game_loop.fruit = Fruit()

    def quit_screen(self) -> None:
        pass


class Main:
    def __init__(self):
        super().__init__()
        pygame.init()

        self.screen = pygame.display.set_mode(
            (cell_number * cell_size, cell_number * cell_size))
        self.clock = pygame.time.Clock()

        self.SCREEN_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(self.SCREEN_UPDATE, 150)

        self.snake = Snake()
        self.fruit = Fruit()

        self.test_runner = MainTestRunner(self)
        self.test_runner.attach(JsonGameStateObserver.get_instance())

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.fruit.draw_fruit(self.screen)
        self.snake.draw_snake(self.screen)

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.test_runner.update_state("fruit_ate")

    def game_over(self):
        self.test_runner.reset()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.test_runner.update_state("lose")
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.test_runner.update_state("lose")
                self.game_over()

    def check_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.snake.direction.y != 1:
                    self.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if self.snake.direction.y != -1:
                    self.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if self.snake.direction.x != 1:
                    self.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                if self.snake.direction.x != -1:
                    self.snake.direction = Vector2(1, 0)

    def run(self):
        while True:
            for event in pygame.event.get():
                self.check_events(event)
                if event.type == self.SCREEN_UPDATE:
                    self.update()

            self.screen.fill((175, 215, 70))
            self.draw_elements()
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":

    if len(sys.argv) == 2:
        if sys.argv[1] == "-test":
            main = Main()
            client_service = ClientService(observer=JsonGameStateObserver.get_instance(),
                                           test_runner=main.test_runner,
                                           event_factory=PygameEventFactory(),
                                           communication_service=CommunicationServiceRestApi())
            client_service.run()
    else:
        game = Main()
        game.run()
