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

    def draw_text(self, text, pos):
        self._game.screen.blit(self._game.font.render(text, True, (81, 179, 41), BG_COLOR), pos)

    def draw_turn_text(self):
        colors = ("Black", "White")
        self.draw_text(f"{colors[self._game.current_color]} Aliens turn", (320, 30))

    def draw_menu_background(self, background_image):
        self._game.screen.blit(background_image, (0, 0))

    def draw_buttons(self, buttons):
        for button in buttons:
            button.draw(self._game.screen)

    def draw_checker(self, center_x, center_y, sprite):
        self._game.screen.blit(sprite, (center_x - 13.5, center_y - 13.5))