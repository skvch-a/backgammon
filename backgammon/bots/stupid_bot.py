from backgammon.utils.move import Move
from backgammon.constants import BLACK

class StupidBot:
    def __init__(self, color=BLACK):
        self._color = color

    @property
    def color(self):
        return self._color

    @staticmethod
    def get_name():
        return "stupid"

    def get_moves(self, field, dices):
        moves = []
        for col in range(23, -1, -1):
            if field.columns[col].peek() == self._color:
                move = Move(col, col + sum(dices), self._color)
                if field.is_move_correct(move):
                    moves.append(move)
                    dices.clear()

        i = 0
        while i < len(dices):
            dice = dices[i]
            for col in range(23, -1, -1):
                if field.columns[col].peek() == self._color:
                    move = Move(col, col + dice, self._color)
                    if field.is_move_correct(move):
                        moves.append(move)
                        dices.remove(dice)
                        i = 0
                        break
            i += 1

        return moves
