import pygame

from backgammon.bots.smart_bot import SmartBot
from backgammon.bots.stupid_bot import StupidBot
from backgammon.menu_button import MenuButton
from .constants import HOTSEAT_BUTTON_PATH, STUPID_BOT_BUTTON_PATH, SMART_BOT_BUTTON_PATH, SCREEN_SIZE, MENU_BG_PATH
from .utils import get_image


class Menu:
    def __init__(self, event_handler, renderer):
        self.event_handler = event_handler
        self.renderer = renderer
        self.menu_buttons = []
        self.load_buttons()
        self.background_image = get_image(MENU_BG_PATH, SCREEN_SIZE)

    def load_buttons(self):
        button_image_paths = [HOTSEAT_BUTTON_PATH, STUPID_BOT_BUTTON_PATH, SMART_BOT_BUTTON_PATH]
        for i in range(3):
            self.menu_buttons.append(MenuButton(i, button_image_paths[i]))

    def choose_game_mode(self):
        while True:
            self.renderer.draw_menu_background(self.background_image)
            self.renderer.draw_buttons(self.menu_buttons)
            pressed_button_index = self.event_handler.handle_menu_events(self.menu_buttons)
            if pressed_button_index == 0:
                return
            elif pressed_button_index == 1:
                return StupidBot()
            elif pressed_button_index == 2:
                return SmartBot()
            pygame.display.update()