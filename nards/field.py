from column import *
from constants import *
from move import *


class Field:
    def __init__(self):
        self.checkers_count = 12
        self.columns = [Column() for _ in range(24)]
        for i in range(self.checkers_count):
            self.columns[0].push(WHITE)
            self.columns[12].push(BLACK)
        self.last_column_index = {WHITE: 23, BLACK: 11}
        self.first_column_index = {WHITE: 0, BLACK: 12}
        self.last_column = {WHITE: self.columns[23], BLACK: self.columns[11]}
        self.first_column = {WHITE: self.columns[0], BLACK: self.columns[12]}

        self.houses = {WHITE: Column(), BLACK: Column()}
        self.winner = NONE
        self.moves = (0, 0)

        self.selected = -1
        self.selected_end = -1

        self.warned_column = -1

    def make_move(self, move):
        if not self.is_correct(move):
            return

        a = self.columns[move.start].pop()
        if move.start == self.last_column_index[move.color]:
            self.houses[move.color].push(a)
        else:
            self.columns[move.end].push(a)

    def log(self):
        for i in self.columns:
            print(i.checkers)
        print(self.houses[WHITE].count, self.houses[BLACK].count)

    def is_correct(self, move, dice=None):

        if move is None:
            return False
        if dice is not None:
            if (move.end - move.start) % 24 != dice:
                return False
        start = self.columns[move.start]
        end = self.columns[move.end]

        if start.count == 0:
            return False
        if start.peek() != move.color:
            return False

        if move.color == BLACK:
            if move.start < self.last_column_index[BLACK] < move.end:
                return False
        if move.color == WHITE:
            if move.start > move.end and move.start != 23:
                return False

        if (
            self.last_column_index[move.color] == move.start
            and (self.last_column[move.color].count + self.houses[move.color].count)
            != self.checkers_count
        ):
            return False
        if end.count == 0:
            return True
        if end.peek() != move.color:
            return False

        return True

    def is_there_legal_move(self, dices, color):
        dices = dices.copy()
        dices.append(sum(dices))
        for dice in dices:
            for i in range(len(self.columns)):
                if self.columns[i].peek() == color:
                    move = Move(i, i + dice, color)
                    if self.is_correct(move):
                        return True
        return False

    def can_endgame(self, color):
        return self.last_column[color].count + self.houses[color].count == 12
