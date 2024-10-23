class Column:
    def __init__(self, needed_checkers=None):
        if needed_checkers is None:
            self.checkers = []
        else:
            self.checkers = needed_checkers

    @property
    def count(self):
        return len(self.checkers)

    def push(self, color):
        self.checkers.append(color)

    def pop(self):
        return self.checkers.pop()

    def peek(self):
        if self.count == 0:
            return None
        return self.checkers[-1]
