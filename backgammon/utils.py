from pygame import transform, image
from constants import WHITE, BLACK
def update_controls(bg_color, screen, field, dices, secret_flag, needed_color):
    if not secret_flag:
        screen.fill(bg_color)
        field.output(dices)
    else:
        current_color = needed_color.get_color()
        screen.fill(current_color)
        field.output(dices)
        needed_color.set_color(10, 5, 3)

def get_image(path, size):
    return transform.scale(image.load(path), size)

def is_move_correct(start, end, color):
    return (color == BLACK or start <= end) and (color == WHITE or start >= 12 or end < 12)