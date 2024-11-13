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
    def get_columns_priority_for_ai(self) -> list[int]:
        pass

    def get_moves(self, field: Field, dices: list) -> list[Move]:
        moves = []
        columns = self.get_columns_priority_for_ai()

        for col in columns:
            if field.points[col].peek() == self._color:
                move = Move(col, col + sum(dices), self._color)
                if field.is_move_correct(move):
                    moves.append(move)
                    dices.clear()

        i = 0
        while i < len(dices):
            dice = dices[i]
            for col in columns:
                if field.points[col].peek() == self._color:
                    move = Move(col, col + dice, self._color)
                    if field.is_move_correct(move):
                        moves.append(move)
                        dices.remove(dice)
                        i = 0
                        break
            i += 1

        return moves