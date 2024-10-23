import pygame
import sys
from pygame.locals import *

pygame.init()
FPS = 30
fpsClock = pygame.time.Clock()
width = 500
height = 500
mainSurface = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption('Keyb moves')
background = pygame.image.load('assets/images/Field.png')
sprite = pygame.image.load('assets/images/HighPika.png')

image_pos = ((mainSurface.get_width() - sprite.get_width()) / 2, (mainSurface.get_height() - sprite.get_height()) / 2)
doMove = False

while True:
    fpsClock.tick(FPS)
    mainSurface.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                doMove = True
            if event.button == 3:
                image_pos = ((mainSurface.get_width() - sprite.get_width()) / 2,
                             (mainSurface.get_height() - sprite.get_height()) / 2)
                doMove = False

        if event.type == pygame.MOUSEBUTTONUP: doMove = False

        if event.type == MOUSEMOTION and doMove:
            image_pos = event.pos

    mainSurface.blit(sprite, image_pos)
    pygame.display.update()