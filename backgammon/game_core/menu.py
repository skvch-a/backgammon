import pygame

from ..constants import HOTSEAT_BUTTON_PATH, STUPID_BOT_BUTTON_PATH, SMART_BOT_BUTTON_PATH
from ..buttons.menu_button import MenuButton

from ..bots.smart_bot import SmartBot
from ..bots.stupid_bot import StupidBot


class Menu:
    def __init__(self, event_handler, renderer):
        self._event_handler = event_handler
        self._renderer = renderer
        self._menu_buttons = []
        self._load_buttons()

    def _load_buttons(self):
        button_image_paths = [HOTSEAT_BUTTON_PATH, STUPID_BOT_BUTTON_PATH, SMART_BOT_BUTTON_PATH]
        for i in range(3):
            self._menu_buttons.append(MenuButton(i, button_image_paths[i]))

    def choose_game_mode(self):
        self._renderer.draw_menu_background()
        self._renderer.draw_buttons(*self._menu_buttons)
        pygame.display.update()
        return self._event_handler.choose_game_mode()