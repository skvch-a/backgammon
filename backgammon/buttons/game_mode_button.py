from pygame import Rect

from .button import Button
from ..constants import MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT


class GameModeButton(Button):
    def __init__(self, button_number: int, image_path: str):
        rect = Rect(button_number * MENU_BUTTON_WIDTH, 175, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
        super().__init__(rect, image_path)
