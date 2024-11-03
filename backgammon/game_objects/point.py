from ..constants import WHITE, BLACK, NONE


class Point:
    def __init__(self, checkers=()):
        self._checkers = list(checkers)
        self._check_all_checkers_one_color()

    def _check_all_checkers_one_color(self):
        if self._checkers.count(WHITE) != len(self._checkers) and self._checkers.count(BLACK) != len(self._checkers):
            raise ValueError("All checkers in point must have same color")

    @property
    def color(self):
        checker = self.peek()
        if checker is None:
            return NONE
        return checker

    @property
    def count(self):
        return len(self._checkers)

    def push(self, color):
        if self._checkers and self._checkers[0] != color:
            raise ValueError('Cannot push checker with different color')
        self._checkers.append(color)

    def pop(self):
        if len(self._checkers) == 0:
            return
        return self._checkers.pop()

    def peek(self):
        return self._checkers[-1] if self.count > 0 else None
