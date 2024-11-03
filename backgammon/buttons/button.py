import pygame

from backgammon.utils.render_utils import get_image

class Button:
    def __init__(self, rect: pygame.Rect, image_path: str):
        self._rect = rect
        self._image = get_image(image_path, rect.size)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self._image, self._rect)

    def is_pressed(self, mouse_pos: tuple[int, int]) -> bool:
        return self._rect.collidepoint(mouse_pos)