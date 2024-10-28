import pygame

from backgammon.constants import *
from backgammon.utils.help_utils import get_image


class Renderer:
    def __init__(self):
        pygame.display.set_caption(TITLE)
        self._screen = pygame.display.set_mode(SCREEN_SIZE)
        self.field_image = pygame.image.load(FIELD_PATH)
        self.font = pygame.font.SysFont("Impact", 40)
        self.dice_sprites = self._get_dice_sprites()

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
        self._screen.blit(self.font.render(text, True, (81, 179, 41)), pos)

    def draw_turn_text(self, current_color):
        colors = ("Black", "White")
        self.draw_text(f"{colors[current_color]} Aliens turn", (320, 30))

    def draw_menu_background(self, background_image):
        self._screen.blit(background_image, (0, 0))

    def draw_buttons(self, buttons):
        for button in buttons:
            button.draw(self._screen)

    def draw_checker(self, checker_image, checker_number, pike):
        self._screen.blit(checker_image, pike.get_checker_position(checker_number))

    def draw_game_bg(self):
        self._screen.blit(get_image('assets/images/game_bg.png', SCREEN_SIZE), (0, 0))

    def draw_field_bg(self):
        self._screen.blit(self.field_image, FIELD_POS)

    def draw_pike(self, pike):
        pygame.draw.polygon(self._screen, pike.color, pike.vertices)

    def update_controls(self, bg_color, field, dices, secret_flag, needed_color, current_color):
        if not secret_flag:
            self._screen.fill(bg_color)
            field.output(dices, current_color)
        else:
            current_color = needed_color.get_color()
            self._screen.fill(current_color)
            field.output(dices, current_color)
            needed_color.set_color(10, 5, 3)

    @staticmethod
    def _get_dice_sprites():
        dice_sprites = []
        for i in range(1, 7):
            dice_sprites.append(get_image(f"assets/images/dice_{i}.png", DICE_SIZE))
        return dice_sprites