from pygame import Rect

from .button import Button
from ..constants import CONTINUE_BUTTON_PATH


class ContinueButton(Button):
    def __init__(self):
        super().__init__(Rect(650, 650, 220, 70), CONTINUE_BUTTON_PATH)