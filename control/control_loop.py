'''
beginning control of flappy bird game by calling the flappy module, and initializing the robot state

Jake Sganga 11/20/16
'''
import numpy as np
import time
import pygame
from flappy_bird.flappy import flappy


def control_flappy(game_replay = False,
                   real_time   = True):
    game = flappy()
    control_loop(game, real_time)
    if game_replay:
        game.graphics.game_replay()


def control_loop(game, real_time):
    frame_timer = time.perf_counter()
    clock = pygame.time.Clock()
    while not game.game_over:
        
        game.move_screen()
        game.check_crash()
        game.update_score()

        if real_time:
            game.graphics.check_exit() # necessary or won't update screen!!!
            game.graphics.update_display()
            clock.tick(game.fps)
    pygame.time.delay(2000)


