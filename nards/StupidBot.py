from bot import Bot
from move import *


class StupidBot(Bot):
    def __init__(self, color):
        self.color = color

    def __str__(self):
        return "Stupid"

    def get_moves(self, field, dices):
        moves = []
        for col in range(23, -1, -1):
            if field.columns[col].peek() == self.color:
                move = Move(col, col + sum(dices), self.color)
                if field.is_correct(move):
                    moves.append(move)
                    dices.clear()

        i = 0
        while i < len(dices):
            dice = dices[i]
            for col in range(23, -1, -1):
                if field.columns[col].peek() == self.color:
                    move = Move(col, col + dice, self.color)
                    if field.is_correct(move):
                        moves.append(move)
                        dices.remove(dice)
                        i = 0
                        break
            i += 1

        return moves
