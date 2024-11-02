from ..constants import BLACK, WHITE, NONE, CHECKERS_COUNT, PIKE_SELECTED_COLOR, PIKE_POSSIBLE_MOVE_COLOR, \
    PIKE_DEFAULT_COLOR, FIELD_POS, THROW_DICES_BUTTON_PATH
from ..game_core.renderer import Renderer
from ..game_objects.pike import Pike
from ..game_objects.point import Point
from ..utils.help_utils import get_dices_box_rect
from ..utils.help_utils import is_move_correct
from ..utils.move import Move
from ..buttons.button import Button

class Field:
    def __init__(self, renderer: Renderer):
        self.renderer = renderer
        self.points = [Point() for _ in range(24)]
        for i in range(CHECKERS_COUNT):
            self.points[0].push(BLACK)
            self.points[12].push(WHITE)

        self.last_point_index = {BLACK: 23, WHITE: 11}
        self.selected = -1
        self.selected_end = -1
        self.positions = []
        self.position_down = []
        self._fill_positions()
        self.pikes = []

        for i, pos in enumerate(self.positions):
            self.pikes.append(Pike(pos[0], pos[1], self._get_pike_type(i)))
        for i, pos in enumerate(self.position_down):
            self.pikes.append(Pike(pos[0], pos[1], self._get_pike_type(i), True))

    def recolor_pikes(self, dices):
        possible_moves, selected_set = self._check_selected(dices)
        for i in range(24):
            pike = self.pikes[i]
            if i in selected_set:
                pike.change_color(PIKE_SELECTED_COLOR)
            elif i in possible_moves:
                move = Move(self.selected, i, self.points[self.selected].peek())
                if self.is_move_correct(move):
                    pike.change_color(PIKE_POSSIBLE_MOVE_COLOR)
            else:
                pike.change_color(PIKE_DEFAULT_COLOR)

    def get_pike(self, pos):
        for i in range(24):
            if self.pikes[i].is_inside(pos[0], pos[1]):
                return i
        return -1

    def make_moves(self, moves):
        for move in moves:
            self.make_move(move)

    def make_move(self, move):
        if self.is_move_correct(move):
            self.points[move.end].push(self.points[move.start].pop())

    def is_move_correct(self, move, dice=None):
        if move is None:
            return False
        if dice is not None:
            if (move.end - move.start) % 24 != dice:
                return False
        start = self.points[move.start]
        end = self.points[move.end]

        if start.count == 0:
            return False
        if start.peek() != move.color:
            return False

        if move.color == WHITE:
            if move.start < self.last_point_index[WHITE] < move.end:
                return False
        if move.color == BLACK:
            if move.start > move.end and move.start != 23:
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
            for i in range(len(self.points)):
                if self.points[i].peek() == color:
                    move = Move(i, i + dice, color)
                    if self.is_move_correct(move):
                        return True
        return False

    def _check_selected(self, dices):
        selected_set = set()
        possible_moves = set()
        for i in range(24):
            selected = self.selected
            if selected == i:
                selected_set.add(i)
                for j in dices:
                    if not is_move_correct(i, (i + j) % 24, self.points[selected].peek()):
                        continue
                    possible_moves.add((i + j) % 24)
                if is_move_correct(i, (i + sum(dices)) % 24, self.points[selected].peek()):
                    possible_moves.add((i + sum(dices)) % 24)
        return possible_moves, selected_set

    def _fill_positions(self):
        first_position = (FIELD_POS[0] + 666, FIELD_POS[1] + 42)
        self.positions.append(first_position)
        for i in range(1, 12):
            if i == 6:
                self.positions.append((self.positions[i - 1][0] - 104, first_position[1]))
            else:
                self.positions.append((self.positions[i - 1][0] - 50, first_position[1]))

        first_position_down = (FIELD_POS[0] + 62, FIELD_POS[1] + 504)
        self.position_down.append(first_position_down)
        for i in range(1, 12):
            if i == 6:
                self.position_down.append((self.position_down[i - 1][0] + 104, first_position_down[1]))
            else:
                self.position_down.append((self.position_down[i - 1][0] + 50, first_position_down[1]))

    @staticmethod
    def _get_pike_type(pike_index):
        pike_type = 1
        if pike_index % 6 == 1 or pike_index % 6 == 4:
            pike_type = 2
        elif pike_index % 6 == 2 or pike_index % 6 == 3:
            pike_type = 3
        return pike_type