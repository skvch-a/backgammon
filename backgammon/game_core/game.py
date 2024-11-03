import random

import pygame

from ..bots.bot import Bot
from ..buttons.button import Button
from ..constants import MUSIC_PATH, THROW_DICES_BUTTON_PATH
from ..game_core.event_handler import EventHandler
from ..game_core.menu import Menu
from ..game_core.renderer import Renderer
from ..game_objects.field import Field
from ..game_objects.point import Point
from ..utils.help_utils import get_dices_box_rect
from ..utils.move import Move


class Game:
    def __init__(self):
        pygame.init()
        self._renderer = Renderer()
        self._event_handler = EventHandler(self)
        self._field = Field()
        self._menu = Menu(self._event_handler, self._renderer)
        self._current_dice = -1
        self._dices = []
        self._is_endgame = False
        self._current_color = 1
        self._selected_pike = 0
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
    def bot(self):
        return self._bot

    @property
    def current_color(self):
        return self._current_color

    def render(self):
        self._renderer.render(self._field, self._dices, self._current_color)

    def run(self):
        pygame.mixer.music.load(MUSIC_PATH)
        pygame.mixer.music.play(-1)

        self._bot: Bot = self._menu.choose_game_mode()
        self.render()
        self.throw_dices()

        while not self._event_handler.is_over:
            self._event_handler.handle_game_events()
            self.render()


    def update_current_dice(self):
        self._current_dice %= len(self.dices)

    def change_color(self):
        self._current_color = (self._current_color + 1) % 2

    def switch_turn(self):
        self.change_color()
        if not self.is_bot_move():
            self.render()
        self.throw_dices()

    def is_bot_move(self):
        return self._bot is not None and self._bot.color == self._current_color

    def throw_dices(self):
        if not self.is_bot_move():
            self._renderer.draw_buttons(self._throw_dices_button)
            pygame.display.update()
            EventHandler.wait_until_button_pressed(self._throw_dices_button)
        self._dices = [random.randint(1, 6), random.randint(1, 6)]

    def make_player_move(self):
        if self._field.selected_end != -1:
            move = Move(self._field.selected, self._field.selected_end, self._current_color)
            if self._field.is_move_correct(move):
                if (self._field.selected_end - self._field.selected) % 24 in self._dices:
                    self._field.make_move(move)
                    self._dices.remove((self._field.selected_end - self._field.selected) % 24)
                    self._field.selected = -1
                elif (self._field.selected_end - self._field.selected) % 24 == sum(self._dices):
                    self._field.make_move(move)
                    self._dices.clear()
                    self._field.selected = -1

        self._field.selected_end = -1
