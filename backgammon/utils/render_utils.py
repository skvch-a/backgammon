from pygame import transform, image, Rect, Surface
from ..constants import FIELD_POS


def get_image(path: str, size: tuple[float, float]) -> Surface:
    return transform.scale(image.load(path), size)

def get_dices_box_rect() -> Rect:
    """Возвращает Rect в котором на экране отрисовываются кости"""
    return Rect(FIELD_POS[0] + 300, FIELD_POS[1] - 100, 130, 70)