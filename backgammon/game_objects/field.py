import pygame
from backgammon.constants import *
from backgammon.utils.move import Move
from backgammon.game_objects.pike import Pike
from backgammon.game_objects.column import Column

from backgammon.utils.help_utils import is_move_correct

class Field:
    def __init__(self, renderer):
        self.renderer = renderer
        self.columns = [Column() for _ in range(24)]
        for i in range(CHECKERS_COUNT):
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
        self.white_sprite = pygame.image.load(CHECKER_WHITE_PATH)
        self.black_sprite = pygame.image.load(CHECKER_BLACK_PATH)
        self.positions = []
        self.position_down = []
        self.fill_positions()
        self.pikes = []
        self.houses_pikes = [Pike(0, 0, 0, 0)] * 2
        for pos in self.positions:
            self.pikes.append(Pike(pos[0], pos[1], 190, 27))
        for pos_down in self.position_down:
            self.pikes.append(Pike(pos_down[0], pos_down[1], -190, 27))


    def output(self, dices, current_color):
        self.renderer.draw_field_bg()
        possible_moves, selected_set = self.check_selected(dices)

        self.fill_pikes(possible_moves, selected_set)
        self.fill_columns()

        for color in range(2):
            column = self.houses[color]
            pike = self.houses_pikes[color]
            sprite = self.white_sprite if color == WHITE else self.black_sprite
            self.renderer.draw_pike(pike, 1)

            for i in range(column.count):
                self.renderer.draw_checker(pike.center_x, pike.y + pike.height / 15 * i, sprite)

        self.renderer.draw_dices(dices, current_color)

    def check_selected(self, dices):
        selected_set = set()
        possible_moves = set()
        for i in range(24):
            selected = self.selected
            if selected == i:
                selected_set.add(i)
                for j in dices:
                    if not is_move_correct(
                            i, (i + j) % 24, self.columns[selected].peek()
                    ):
                        continue
                    possible_moves.add((i + j) % 24)
                if is_move_correct(
                        i, (i + sum(dices)) % 24, self.columns[selected].peek()
                ):
                    possible_moves.add((i + sum(dices)) % 24)

            if i % 6 == 2 or i % 6 == 3:
                self.renderer.draw_pike(self.pikes[i],3)
            elif i % 6 == 1 or i % 6 == 4:
                self.renderer.draw_pike(self.pikes[i],2)
            else:
                self.renderer.draw_pike(self.pikes[i],1)
        return possible_moves, selected_set

    def fill_columns(self):
        for i in range(24):
            pikes_coordinate = (self.pikes[i].center_x, self.pikes[i].y)
            column = self.columns[i]
            for j in range(column.count):
                sprite = self.white_sprite
                if column.peek() == 0:
                    sprite = self.black_sprite
                self.renderer.draw_checker(
                    pikes_coordinate[0],
                    pikes_coordinate[1] + self.pikes[i].height / 15 * j,
                    sprite,
                )

    def fill_pikes(self, possible_moves, selected_set):
        for i in range(24):
            pike = self.pikes[i]
            if i in selected_set:
                pike.color = pike.selected_color
            elif i in possible_moves:
                move = Move(
                    self.selected,
                    i,
                    self.columns[self.selected].peek(),
                )
                if self.is_correct(move):
                    pike.color = pike.possible_move_color
            else:
                pike.color = pike.default_color

    def fill_positions(self):
        first_position = (FIELD_POS[0] + 666, FIELD_POS[1] + 42)
        self.positions.append(first_position)
        for i in range(1, 12):
            if i == 6:
                self.positions.append(
                    (self.positions[i - 1][0] - 104, first_position[1])
                )
            else:
                self.positions.append(
                    (self.positions[i - 1][0] - 50, first_position[1])
                )

        first_position_down = (FIELD_POS[0] + 62, FIELD_POS[1] + 504)
        self.position_down.append(first_position_down)
        for i in range(1, 12):
            if i == 6:
                self.position_down.append(
                    (self.position_down[i - 1][0] + 104, first_position_down[1])
                )
            else:
                self.position_down.append(
                    (self.position_down[i - 1][0] + 50, first_position_down[1])
                )

    def get_pike_by_coordinates(self, x, y):
        for i in range(24):
            if self.pikes[i].is_inside(x, y):
                return i
        return -1

    def make_move(self, move):
        if not self.is_correct(move):
            return

        a = self.columns[move.start].pop()
        if move.start == self.last_column_index[move.color]:
            self.houses[move.color].push(a)
        else:
            self.columns[move.end].push(a)

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

        if (self.last_column_index[move.color] == move.start
                and (self.last_column[move.color].count + self.houses[move.color].count) != CHECKERS_COUNT):
            return False
        if end.count == 0:
            return True
        if end.peek() != move.color:
            return False

        return True

    def has_legal_move(self, dices, color):
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
