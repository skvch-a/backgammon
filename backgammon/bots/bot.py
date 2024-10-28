import abc
from backgammon.game_objects.field import Field
from backgammon.utils.move import Move

class Bot(abc.ABC):
    def __init__(self, color):
        self._color = color

    @property
    def color(self):
        return self._color

    @staticmethod
    @abc.abstractmethod
    def get_name() -> str:
        pass

    @abc.abstractmethod
    def get_moves(self, field: Field, dices: list[int, int]) -> list[Move]:
        pass