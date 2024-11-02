from pygame import transform, image, Rect
from backgammon.constants import WHITE, BLACK, FIELD_POS


def get_image(path, size):
    return transform.scale(image.load(path), size)

def is_move_correct(start, end, color):
    return (color == BLACK or start <= end) and (color == WHITE or start >= 12 or end < 12)

def get_dices_box_rect():
    return Rect(FIELD_POS[0] + 300, FIELD_POS[1] - 100, 130, 70)