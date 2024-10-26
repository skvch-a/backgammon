import pygame

from backgammon.constants import *


class Renderer:
    def __init__(self, game):
        self._game = game
        self.dice_sprites = []
        for i in range(1, 7):
            sprite = pygame.image.load(f"assets/images/dice_{i}.png")
            self.dice_sprites.append(pygame.transform.scale(sprite, DICE_SIZE))

    def draw_dices(self, dices):
        rect_width = 130
        rect_height = 70
        rect_x = FIELD_POS[0] + 310
        rect_y = FIELD_POS[1] - 100

        if self._game.current_color == WHITE:
            rect_color = (255, 255, 255)
        else:
            rect_color = (0, 0, 0)
        pygame.draw.rect(self._game.screen, rect_color, (rect_x, rect_y, rect_width, rect_height))

        indent = 0
        for dice_index in dices:
            self._game.screen.blit(self.dice_sprites[dice_index - 1], (rect_x + indent * 60 + 10, rect_y + 10))
            indent += 1