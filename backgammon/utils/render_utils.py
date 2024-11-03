from pygame import transform, image, Rect
from ..constants import FIELD_POS


def get_image(path, size):
    return transform.scale(image.load(path), size)

def get_dices_box_rect():
    return Rect(FIELD_POS[0] + 300, FIELD_POS[1] - 100, 130, 70)