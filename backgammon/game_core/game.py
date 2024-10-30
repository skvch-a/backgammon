import random
import pygame

from ..buttons.button import Button
from ..constants import NONE, WHITE, BLACK, MUSIC_PATH, THROW_DICES_BUTTON_PATH
from ..bots.bot import Bot

from ..game_core.event_handler import EventHandler
from ..game_core.menu import Menu
from ..game_core.renderer import Renderer

from ..game_objects.field import Field
from ..game_objects.point import Point

from ..utils.color_saves import ColorsSaver
from ..utils.help_utils import get_dices_box_rect
from ..utils.move import Move


class Game:
    def __init__(self):
        pygame.init()

        self._renderer = Renderer()
        self._event_handler = EventHandler(self)
        self._field = Field(self._renderer)
        self._menu = Menu(self._event_handler, self._renderer)
        self._current_dice = -1
        self._dices = []
        self._winner = NONE
        self._current_color = 1
        self._last_dice = (-1, WHITE)
        self._selected_pike = 0
        self._needed_color = ColorsSaver()
        self._secret_flag = False
        self._throw_dices_button = Button(get_dices_box_rect(), THROW_DICES_BUTTON_PATH)
        self._bot = None
        self._field.points = [Point(i) for i in
                              [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [], [], [], [], [], [], [], [], [], [], [],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [], [], [], [], [], [], [], [], [], [], []]]

    @property
    def current_dice(self):
        return self._current_dice

    @property
    def dices(self):
        return self._dices

    @property
    def field(self):
        return self._field

    @property
    def current_color(self):
        return self._current_color

    def update_current_dice(self):
        self._current_dice %= len(self.dices)

    def change_color(self):
        self._current_color = (self._current_color + 1) % 2

    def run(self):
        pygame.mixer.music.load(MUSIC_PATH)
        pygame.mixer.music.play(-1)
        self._bot: Bot = self._menu.choose_game_mode()

        self._renderer.update_controls(self._field, self._dices, self._secret_flag, self._needed_color,
                                       self._current_color)
        self.throw_bones()

        while self._winner == NONE:
            if not self._field.has_legal_move(self._dices, self._current_color):
                self.throw_bones()
                self.change_color()
                self._renderer.update_controls(self._field, self._dices, self._secret_flag, self._needed_color,
                                               self._current_color)
                continue

            self.get_winner()

            if self._bot is not None and self._bot.color == self._current_color:
                moves = self._bot.get_moves(self._field, self._dices)
                for move in moves:
                    self._field.make_move(move)
                    if self._field.can_endgame(self._bot.color):
                        break
                pygame.time.wait(1000)
                self._current_color = (self._current_color + 1) % 2
                self.throw_bones()
                continue


            self._event_handler.handle_game_events()
            self.make_move_by_mouse()

            self._renderer.update_controls(self._field, self._dices, self._secret_flag, self._needed_color,
                                           self._current_color)
            if len(self._dices) == 0:
                self._current_color = (self._current_color + 1) % 2
                self.throw_bones()


    def throw_bones(self):
        self.field.recolor_pikes(self.dices)
        for pike in self.field.pikes:
            self._renderer.draw_pike(pike)
        self._renderer.draw_checkers(self.field.points, self.field.pikes)
        if self._bot is None or self._current_color == WHITE:
            self._renderer.draw_buttons(self._throw_dices_button)
            pygame.display.update()
            EventHandler.wait_until_button_pressed(self._throw_dices_button)
        self._dices = [random.randint(1, 6), random.randint(1, 6)]

    def make_move_by_mouse(self):
        if self._field.selected_end != -1:
            last_column_index = self._field.last_point_index[self._current_color]
            if self._field.selected_end == last_column_index:
                if self._field.can_endgame(self._current_color):
                    move = Move(last_column_index, last_column_index + 1, self._current_color)
                    self._field.make_move(move)
                    self._field.selected = -1
                    self._field.selected_end = -1
                    self._dices = []
                    return

            if (self._field.selected_end - self._field.selected) % 24 in self._dices:
                move = Move(self._field.selected, self._field.selected_end, self._current_color)
                if self._field.is_move_correct(move):
                    self._field.make_move(move)
                    self._dices.remove((self._field.selected_end - self._field.selected) % 24)
                    self._field.selected = -1

            elif (self._field.selected_end - self._field.selected) % 24 == sum(self._dices):
                move = Move(self._field.selected, self._field.selected_end, self._current_color)
                if self._field.is_move_correct(move):
                    self._field.make_move(move)
                    self._dices = []
                    self._field.selected = -1
        self._field.selected_end = -1

    def get_winner(self):
        if self._field.houses[BLACK].count == 12:
            self._winner = BLACK
            pygame.time.wait(10)
            pygame.quit()
        elif self._field.houses[WHITE].count == 12:
            self._winner = WHITE
            pygame.time.wait(10)
            pygame.quit()
