import sys

import pygame
import requests


pygame.init()
screen = pygame.display.set_mode(
            (100, 100))
while True:
    key = None
    game_event = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                key = 'up'
            if event.key == pygame.K_DOWN:
                key = 'down'
            if event.key == pygame.K_LEFT:
                key = 'left'
            if event.key == pygame.K_RIGHT:
                key = 'right'
            if event.key == pygame.K_SPACE:
                r = requests.get("http://localhost:5000/")
                print(r.json())
            if event.key == pygame.K_r:
                game_event = "reset"
    if key or game_event:
        r = requests.post('http://localhost:5000/',
                          json={
                              'inputs': [key],
                              'event': game_event
                          })


