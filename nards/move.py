class Move:
    def __init__(self, start, end, color):
        self.start = start % 24
        self.end = end % 24
        self.color = color
