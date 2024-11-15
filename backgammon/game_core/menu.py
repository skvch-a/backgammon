import pygame

from .renderer import Renderer
from .event_handler import EventHandler
from ..buttons.continue_button import ContinueButton
from ..constants import HOTSEAT_BUTTON_PATH, STUPID_BOT_BUTTON_PATH, SMART_BOT_BUTTON_PATH
from ..buttons import Button, GameModeButton


class Menu:
    def __init__(self, event_handler: EventHandler, renderer: Renderer, records: dict):
        self.bot = None
        self._event_handler = event_handler
        self._renderer = renderer
        self._buttons = []
        self._records = records
        self._load_buttons()

    def _load_buttons(self):
        game_mode_button_image_paths = [HOTSEAT_BUTTON_PATH, STUPID_BOT_BUTTON_PATH, SMART_BOT_BUTTON_PATH]
        for i in range(3):
            self._buttons.append(GameModeButton(i, game_mode_button_image_paths[i]))
        self._buttons.append(ContinueButton())

    def run(self):
        self._renderer.draw_menu_background()
        self._renderer.draw_buttons(*self._buttons)
        self._renderer.draw_records(self._records)
        pygame.display.update()
        self.bot = self._event_handler.choose_game_mode(self._buttons)