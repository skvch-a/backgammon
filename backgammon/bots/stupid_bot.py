from backgammon.constants import BLACK
from backgammon.bots.bot import Bot
from backgammon.utils.move import Move


class StupidBot(Bot):
    def __init__(self, color=BLACK):
        super().__init__(color)

    def get_moves(self, field, dices):
        moves = []
        for col in range(23, -1, -1):
            if field.points[col].peek() == self._color:
                move = Move(col, col + sum(dices), self._color)
                if field.is_move_correct(move):
                    moves.append(move)
                    dices.clear()

        i = 0
        while i < len(dices):
            dice = dices[i]
            for col in range(23, -1, -1):
                if field.points[col].peek() == self._color:
                    move = Move(col, col + dice, self._color)
                    if field.is_move_correct(move):
                        moves.append(move)
                        dices.remove(dice)
                        i = 0
                        break
            i += 1

        return moves
