import pygame

from backgammon.constants import *
from backgammon.utils import get_image


class Renderer:
    def __init__(self, screen):
        self._screen = screen
        self.dice_sprites = []
        self.field_image = pygame.image.load(FIELD_PATH)
        self.font = pygame.font.SysFont("Impact", 40)
        for i in range(1, 7):
            self.dice_sprites.append(get_image(f"assets/images/dice_{i}.png", DICE_SIZE))

    def draw_dices(self, dices, current_color):
        rect_width = 130
        rect_height = 70
        rect_x = FIELD_POS[0] + 310
        rect_y = FIELD_POS[1] - 100

        if current_color == WHITE:
            rect_color = (255, 255, 255)
        else:
            rect_color = (0, 0, 0)
        pygame.draw.rect(self._screen, rect_color, (rect_x, rect_y, rect_width, rect_height))

        indent = 0
        for dice_index in dices:
            self._screen.blit(self.dice_sprites[dice_index - 1], (rect_x + indent * 60 + 10, rect_y + 10))
            indent += 1

    def draw_text(self, text, pos):
        self._screen.blit(self.font.render(text, True, (81, 179, 41), BG_COLOR), pos)

    def draw_turn_text(self, current_color):
        colors = ("Black", "White")
        self.draw_text(f"{colors[current_color]} Aliens turn", (320, 30))

    def draw_menu_background(self, background_image):
        self._screen.blit(background_image, (0, 0))

    def draw_buttons(self, buttons):
        for button in buttons:
            button.draw(self._screen)

    def draw_checker(self, x, y, sprite):
        self._screen.blit(sprite, (x - 13.5, y - 13.5))

    def draw_field_bg(self):
        self._screen.blit(self.field_image, FIELD_POS)

    def draw_pike(self, pike, size):
        pike.draw(self._screen, size)