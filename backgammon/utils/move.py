from backgammon.constants import BLACK, WHITE


class Move:
    def __init__(self, start, end, color):
        self.start = start % 24
        self.end = end % 24
        self.color = color

    @staticmethod
    def is_correct(start, end, color):
        return (color == BLACK or start <= end) and (color == WHITE or start >= 12 or end < 12)

