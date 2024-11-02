from backgammon.constants import PIKE_DEFAULT_COLOR, CHECKER_HALF_SIZE, PIKE_WIDTH, PIKE_BASE_HEIGHT


class Pike:
    def __init__(self, center_x, y, pike_type, reverse=False):
        self._color = PIKE_DEFAULT_COLOR
        self._center_x = center_x
        self._x = center_x - PIKE_WIDTH / 2
        self._y = y
        self._signed_height = -1 * PIKE_BASE_HEIGHT if reverse else PIKE_BASE_HEIGHT
        self._render_height = self._signed_height / pike_type

    @property
    def vertices(self):
        return (self._x, self._y), (self._x + PIKE_WIDTH, self._y), (self._center_x, self._y + self._render_height)

    @property
    def color(self):
        return self._color

    def get_checker_position(self, checker_number):
        return self._center_x - CHECKER_HALF_SIZE, self._y + self._signed_height / 15 * checker_number - CHECKER_HALF_SIZE

    def change_color(self, color):
        self._color = color

    def is_inside(self, x, y):
        x1 = self._x
        x2 = self._x + PIKE_WIDTH
        x3 = self._center_x
        y1 = self._y
        y2 = self._y
        y3 = self._y + self._signed_height

        s1 = (x1 - x) * (y2 - y1) - (x2 - x1) * (y1 - y)
        s2 = (x2 - x) * (y3 - y2) - (x3 - x2) * (y2 - y)
        s3 = (x3 - x) * (y1 - y3) - (x1 - x3) * (y3 - y)

        return (s1 >= 0 and s2 >= 0 and s3 >= 0) or (s1 <= 0 and s2 <= 0 and s3 <= 0)
