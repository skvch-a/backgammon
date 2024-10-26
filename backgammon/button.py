from backgammon.utils import get_image

class Button:
    def __init__(self, rect, image_path):
        self._rect = rect
        self._image = get_image(image_path, rect.size)

    def draw(self, screen):
        screen.blit(self._image, self._rect)

    def is_pressed(self, mouse_pos):
        return self._rect.collidepoint(mouse_pos)