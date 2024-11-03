import random

from .bot import Bot
from ..constants import BLACK
from ..utils import Move


class SmartBot(Bot):
    def __init__(self, color=BLACK):
        super().__init__(color)

    @property
    def name(self):
        return 'High IQ Alien'

    def get_moves(self, field, dices):
        points_numbers = list(range(23))
        dices_variations = [0, 1, 2]
        random.shuffle(dices_variations)
        moves = []
        for i in dices_variations:
            random.shuffle(points_numbers)
            for point_num in points_numbers:
                if field.points[point_num].peek() == self._color:
                    move = None
                    if (i == 0 or i == 1) and dices[i] != -1:
                        move = Move(point_num, point_num + dices[i], self._color)
                    elif dices[0] != -1 and dices[1] != -1:
                        move = Move(point_num, point_num + sum(dices), self._color)
                    if field.is_move_correct(move):
                        moves.append(move)
                        field.make_move(move)
                        if i == 0 or i == 1:
                            dices[i] = -1
                            break
                        elif dices[0] != -1 and dices[1] != -1:
                            dices[0] = -1
                            dices[1] = -1
                if sum(dices) == -2:
                    dices.clear()
                    return moves
        dices.clear()

        return moves
