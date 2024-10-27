from pygame import transform, image
from constants import WHITE, BLACK


def get_image(path, size):
    return transform.scale(image.load(path), size)

def is_move_correct(start, end, color):
    return (color == BLACK or start <= end) and (color == WHITE or start >= 12 or end < 12)