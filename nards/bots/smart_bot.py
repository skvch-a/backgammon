from nards.bots.bot import Bot
import random
from nards.move import *
import copy


class SmartBot(Bot):
    def __init__(self, color):
        self.color = color

    def __str__(self):
        return "Smart"

    def get_moves(self, field, dices):
        field = copy.deepcopy(field)

        diapason = list(range(23))
        what_move = [0, 1, 2]
        random.shuffle(what_move)
        moves = []
        for i in what_move:
            random.shuffle(diapason)
            for col in diapason:
                if field.columns[col].peek() == self.color:
                    move = None
                    if (i == 0 or i == 1) and dices[i] != -1:
                        move = Move(col, col + dices[i], self.color)
                    elif dices[0] != -1 and dices[1] != -1:
                        move = Move(col, col + sum(dices), self.color)
                    if field.is_correct(move):
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
