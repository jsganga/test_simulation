
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import random


from functions import low_pass_filter as f
import functions.trig as trig

# from model.robot_body import body
from itertools import cycle
import random
import sys

import pygame
from pygame.locals import *


screen_width  = 288
screen_height = 512
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
im = pygame.image.load('flappy_bird/assets/sprites/0.png').convert_alpha()
# print(im)
screen.blit(im, (0,0))
# pygame.display.set_caption('Flappy Bird Robot')
pygame.display.flip()

now = time.perf_counter()
fps = 30 
clock = pygame.time.Clock()
i = 0
while time.perf_counter() - now < 4:
    i += 1
    # im = pygame.image.load('flappy_bird/assets/sprites/0.png').convert_alpha()
    # pygame.display.set_mode((screen_width, screen_height))
    # screen = pygame.display.get_surface()
    for event in pygame.event.get():
        # I remove the timer just for my testing
        if event.type == pygame.QUIT: sys.exit()
    screen.blit(im, (i,i))
    pygame.display.update()
    clock.tick(fps)  
       # forces the program to run at 30 fps.
# from flappy_bird.flappy import flappy
# # import flappy_bird.flappy_graphics as fg
# import flappy_bird.test_graphics as tg
# # import flappy_bird.flappy_graphics as fg

# test = tg.graphics()
# # test.load_images()
# # test.initialize_display()

# # test = tg.graphics()
# # test.load_images()
# # test.initialize_display()

# now = time.perf_counter()
# y = 0
# while time.perf_counter() - now < 3:
#     # test = tg.graphics()
#     # test.load_images()
#     # test.set_mode()
#     # test.initialize_display()
#     test.update_display(y)
#     y += 10
#     pygame.time.delay(30)