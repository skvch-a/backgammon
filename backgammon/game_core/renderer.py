import pygame

from backgammon.constants import *
from backgammon.utils.help_utils import get_image, get_dices_box_rect


class Renderer:
    def __init__(self):
        pygame.display.set_caption(TITLE)
        self._screen = pygame.display.set_mode(SCREEN_SIZE)
        self._field_image = pygame.image.load(FIELD_PATH)
        self._font = pygame.font.SysFont("Impact", 40)
        self._dice_sprites = self._get_dice_sprites()
        self._game_bg = get_image(GAME_BG_PATH, SCREEN_SIZE)
        self._dices_box_rect = get_dices_box_rect()
        self._throw_dices_button_image = pygame.image.load(THROW_DICES_BUTTON_PATH)
        self._white_checker_image = pygame.image.load(CHECKER_WHITE_PATH)
        self._black_checker_image = pygame.image.load(CHECKER_BLACK_PATH)

    def draw_dices(self, dices, current_color):
        rect = self._dices_box_rect
        rect_color = (255, 255, 255) if current_color == BLACK else (0, 0, 0)
        pygame.draw.rect(self._screen, rect_color, rect)

        indent = 0
        for dice_index in dices:
            self._screen.blit(self._dice_sprites[dice_index - 1], (rect.x + indent * 60 + 10, rect.y + 10))
            indent += 1

    def draw_text(self, text, pos):
        self._screen.blit(self._font.render(text, True, (81, 179, 41)), pos)

    def draw_turn_text(self, current_color):
        colors = ("Black", "White")
        self.draw_text(f"{colors[current_color]} Aliens turn", (320, 30))

    def draw_menu_background(self, background_image):
        self._screen.blit(background_image, (0, 0))

    def draw_buttons(self, *buttons):
        for button in buttons:
            button.draw(self._screen)

    def draw_checker(self, checker_color, checker_number, pike):
        image = self._white_checker_image if checker_color == BLACK else self._black_checker_image
        self._screen.blit(image, pike.get_checker_position(checker_number))

    def draw_checkers(self, points, pikes):
        for point, pike in zip(points, pikes):
            for checker_number in range(point.count):
                self.draw_checker(point.peek(), checker_number, pike)

    def draw_game_bg(self):
        self._screen.blit(self._game_bg, (0, 0))

    def draw_field_bg(self):
        self._screen.blit(self._field_image, FIELD_POS)

    def draw_pike(self, pike):
        pygame.draw.polygon(self._screen, pike.color, pike.vertices)

    def draw_pikes(self, pikes):
        for pike in pikes:
            self.draw_pike(pike)

    def draw_field(self, field, dices, current_color):
        self.draw_game_bg()
        self.draw_field_bg()
        field.recolor_pikes(dices)
        self.draw_pikes(field.pikes)
        self.draw_checkers(field.points, field.pikes)
        self.draw_dices(dices, current_color)

    def render(self, field, dices, current_color):
        self.draw_field(field, dices, current_color)
        self.draw_turn_text(current_color)
        pygame.display.update()

    @staticmethod
    def _get_dice_sprites():
        dice_sprites = []
        for i in range(1, 7):
            dice_sprites.append(get_image(f"assets/images/dice_{i}.png", DICE_SIZE))
        return dice_sprites
