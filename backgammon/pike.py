import pygame


class Pike:
    def __init__(self, center_x, y, height, width):
        self.color = pygame.Color(0, 0, 0)
        self.default_color = pygame.Color(128, 128, 128)
        self.selected_color = pygame.Color(0, 0, 0)
        self.possible_move_color = pygame.Color(0, 255, 0)
        self.center_x = center_x
        self.y = y
        self.height = height
        self.width = width

    def draw_pikes(self, screen, size):
        pygame.draw.polygon(
            screen,
            self.color,
            [
                [self.center_x - self.width / 2, self.y],
                [self.center_x + self.width / 2, self.y],
                [self.center_x, self.y + self.height / size],
            ],
        )

    def is_inside(self, x, y):
        x1 = self.center_x - self.width / 2
        x2 = self.center_x + self.width / 2
        x3 = self.center_x
        y1 = self.y
        y2 = self.y
        y3 = self.y + self.height
        s1 = (x1 - x) * (y2 - y1) - (x2 - x1) * (y1 - y)
        s2 = (x2 - x) * (y3 - y2) - (x3 - x2) * (y2 - y)
        s3 = (x3 - x) * (y1 - y3) - (x1 - x3) * (y3 - y)

        if (s1 >= 0 and s2 >= 0 and s3 >= 0) or (s1 <= 0 and s2 <= 0 and s3 <= 0):
            return True
        return False
