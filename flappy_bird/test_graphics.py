'''
flappy_graphics.py

File will consolidate the graphics calls for the flappy game allowing for 
real time display or after the fact viewing. Receives the flappy game object
for positions of bird and environment 

'''

from itertools import cycle
import time
import pygame
from pygame.locals import *
import random

import os
x, y = 0, 0
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

# amount by which base can maximum shift to left

# image, sound and hitmask  dicts

# list of all possible players (tuple of 3 positions of flap)
image_folder = 'flappy_bird/assets/sprites/'
bird_images = (
    # red bird
    (
        image_folder + 'redbird-upflap.png',
        image_folder + 'redbird-midflap.png',
        image_folder + 'redbird-downflap.png',
    ),
    # blue bird
    (
        # amount by which base can maximum shift to left
        image_folder + 'bluebird-upflap.png',
        image_folder + 'bluebird-midflap.png',
        image_folder + 'bluebird-downflap.png',
    ),
    # yellow bird
    (
        image_folder + 'yellowbird-upflap.png',
        image_folder + 'yellowbird-midflap.png',
        image_folder + 'yellowbird-downflap.png',
    ),
)

# list of backgrounds
backgrounds_list = (
    image_folder + 'background-day.png',
    image_folder + 'background-night.png',
)

# list of pipes
pipes_list = (
    image_folder + 'pipe-green.png',
    image_folder + 'pipe-red.png',
)

playerIndex = 0
playerIndexGen = cycle([0, 1, 2, 1])
basex = 0

screen_width  = 288
screen_height = 512


# pygame.display.set_mode((screen_width, screen_height))


class graphics(object):
    """graphics object to handle displaying the flappy game"""
    def __init__(self):
        super(graphics, self).__init__()
        pygame.init()
        

        # self.set_mode()

    # def set_mode(self):



    # def load_images(self):
        # numbers sprites for score display
        self.images = {}

        self.images['numbers'] = (
            pygame.image.load(image_folder + '0.png').convert_alpha(),
            pygame.image.load(image_folder + '1.png').convert_alpha(),
            pygame.image.load(image_folder + '2.png').convert_alpha(),
            pygame.image.load(image_folder + '3.png').convert_alpha(),
            pygame.image.load(image_folder + '4.png').convert_alpha(),
            pygame.image.load(image_folder + '5.png').convert_alpha(),
            pygame.image.load(image_folder + '6.png').convert_alpha(),
            pygame.image.load(image_folder + '7.png').convert_alpha(),
            pygame.image.load(image_folder + '8.png').convert_alpha(),
            pygame.image.load(image_folder + '9.png').convert_alpha()
        )

        # game over sprite
        self.images['gameover'] = pygame.image.load(image_folder + 'gameover.png').convert_alpha()
        # message sprite for welcome screen
        self.images['message'] = pygame.image.load(image_folder + 'message.png').convert_alpha()
        # base (ground) sprite
        self.images['base'] = pygame.image.load(image_folder + 'base.png').convert_alpha()

        # select random background sprites
        randBg = random.randint(0, len(backgrounds_list) - 1)
        self.images['background'] = pygame.image.load(backgrounds_list[randBg]).convert()

        # select random player sprites
        randPlayer = random.randint(0, len(bird_images) - 1)
        self.images['player'] = (
            pygame.image.load(bird_images[randPlayer][0]).convert_alpha(),
            pygame.image.load(bird_images[randPlayer][1]).convert_alpha(),
            pygame.image.load(bird_images[randPlayer][2]).convert_alpha(),
        )

        # select random pipe sprites
        pipeindex = random.randint(0, len(pipes_list) - 1)
        self.images['pipe'] = (
            pygame.transform.rotate(
                pygame.image.load(pipes_list[pipeindex]).convert_alpha(), 180),
            pygame.image.load(pipes_list[pipeindex]).convert_alpha(),
        )


    # def initialize_display(self):
        self.screen.fill(Color("black"))
        self.screen.blit(self.images['background'], (0,0))
        
        self.screen.blit(self.images['base'], (0, 280))
        self.screen.blit(self.images['player'][0], (10, 10))

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('Flappy Bird Robot')
        pygame.display.update()


    def update_display(self, y):
        # self.screen.fill(Color("black"))
    

        self.screen.blit(self.images['base'], (0, 300))
        self.screen.blit(self.images['player'][0], (10, y))
        
        pygame.display.update()
        print('update', time.perf_counter(), self.screen)


    def show_score(self):
        """displays score in center of screen"""
        scoreDigits = [int(x) for x in list(str(self.game.score))]
        totalWidth = 0 # total width of all numbers to be printed

        for digit in scoreDigits:
            totalWidth += self.images['numbers'][digit].get_width()

        Xoffset = (self.game.screen_width - totalWidth) / 2

        for digit in scoreDigits:
            self.screen.blit(self.images['numbers'][digit], (Xoffset, self.game.screen_height * 0.1))
            Xoffset += self.images['numbers'][digit].get_width()

    def game_replay(self):
        pass
