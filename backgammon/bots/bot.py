import abc


class Bot(abc.ABC):
    def __init__(self, color):
        self._color = color

    @property
    def color(self):
        return self._color

    @staticmethod
    @abc.abstractmethod
    def get_name():
        pass

    @abc.abstractmethod
    def get_moves(self, field, dices):
        pass