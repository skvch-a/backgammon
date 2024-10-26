from pygame import Rect
from backgammon.button import Button
from backgammon.constants import MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT

class MenuButton(Button):
    def __init__(self, button_number, image_path):
        rect = Rect(button_number * MENU_BUTTON_WIDTH, 75, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
        super().__init__(rect, image_path)
