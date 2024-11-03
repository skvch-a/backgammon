import abc

from ..game_objects import Field
from ..utils import Move

class Bot(abc.ABC):
    def __init__(self, color):
        self._color = color

    @property
    def color(self):
        return self._color

    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass

    @abc.abstractmethod
    def get_moves(self, field: Field, dices: list) -> list[Move]:
        pass