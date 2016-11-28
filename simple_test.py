import sys, time
import pygame
from pygame.locals import *

pygame.init()
size = width, height = 800,500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("testing")
myfont = pygame.font.SysFont("monospace", 16)
WHITE = (255,255,255)
im = pygame.image.load('flappy_bird/assets/sprites/0.png').convert_alpha()

score = 0
now = time.perf_counter()
while time.perf_counter() - now < 4:
    pygame.display.flip()
    for event in pygame.event.get():
        # I remove the timer just for my testing
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(WHITE)

    disclaimertext = myfont.render("Some disclaimer...", 1, (0,0,0))
    screen.blit(disclaimertext, (5, 480))

    scoretext = myfont.render("Score {0}".format(score), 1, (0,0,0))
    screen.blit(scoretext, (5, 10))
    screen.blit(im, (score, score))
    score += 1