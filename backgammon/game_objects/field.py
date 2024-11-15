from ..constants import WHITE, BLACK, CHECKERS_COUNT, PIKE_SELECTED_COLOR, PIKE_POSSIBLE_MOVE_COLOR, \
    PIKE_DEFAULT_COLOR, FIELD_POS

from .pike import Pike
from .point import Point
from ..utils import Move

class Field:
    def __init__(self):
        self.points = self._get_start_points()
        self.last_point_index = {WHITE: 23, BLACK: 11}
        self.selected = -1
        self.selected_end = -1
        self.pikes = self._get_pikes()

    @property
    def checkers_count(self) -> int:
        count = 0
        for point in self.points:
            count += point.count
        return count

    @property
    def serialize_data(self):
        checkers = []
        for point in self.points:
            checkers.append(point.checkers)
        return checkers

    @staticmethod
    def _get_start_points():
        points = [Point() for _ in range(24)]
        for i in range(CHECKERS_COUNT):
            points[0].push(WHITE)
            points[12].push(BLACK)
        return points

    @staticmethod
    def _get_pikes_positions():
        first_position = (FIELD_POS[0] + 666, FIELD_POS[1] + 42)
        positions = [first_position]
        for i in range(1, 12):
            if i == 6:
                positions.append((positions[i - 1][0] - 104, first_position[1]))
            else:
                positions.append((positions[i - 1][0] - 50, first_position[1]))

        first_position_down = (FIELD_POS[0] + 62, FIELD_POS[1] + 504)
        positions_down = [first_position_down]
        for i in range(1, 12):
            if i == 6:
                positions_down.append((positions_down[i - 1][0] + 104, first_position_down[1]))
            else:
                positions_down.append((positions_down[i - 1][0] + 50, first_position_down[1]))
        return positions, positions_down

    def _get_pikes(self):
        pikes = []
        positions, positions_down = self._get_pikes_positions()
        for i, pos in enumerate(positions):
            pikes.append(Pike(pos[0], pos[1], self._get_pike_type(i)))
        for i, pos in enumerate(positions_down):
            pikes.append(Pike(pos[0], pos[1], self._get_pike_type(i), True))
        return pikes

    def recolor_pikes(self, dices) -> None:
        """Изменяет цвет пунктов в соответствии с их текущим состоянием"""
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

    def get_pike(self, pos) -> int:
        """Возвращает индекс выбранного пункта по позиции"""
        for i in range(24):
            if self.pikes[i].is_inside(pos[0], pos[1]):
                return i
        return -1

    def make_moves(self, moves) -> None:
        for move in moves:
            self.make_move(move)

    def make_move(self, move) -> None:
        if self.is_move_correct(move):
            self.points[move.end].push(self.points[move.start].pop())

    def is_move_correct(self, move, dice=None) -> bool:
        if move is None or move.start == move.end:
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

        if move.color == BLACK and move.start <= self.last_point_index[BLACK] <= move.end:
            return False
        if move.color == WHITE and move.start > move.end:
            return False

        if end.count == 0:
            return True
        if end.peek() != move.color:
            return False

        return True

    def has_legal_move(self, dices, color) -> bool:
        dices = dices.copy()
        dices.append(sum(dices))
        for dice in dices:
            for i in range(len(self.points)):
                if self.points[i].peek() == color:
                    move = Move(i, i + dice, color)
                    if self.is_move_correct(move):
                        return True
        return False

    def _check_selected(self, dices) -> tuple[set, set]:
        selected_set = set()
        possible_moves = set()
        for i in range(24):
            selected = self.selected
            if selected == i:
                selected_set.add(i)
                for j in dices:
                    if not Move.is_correct(i, (i + j) % 24, self.points[selected].peek()):
                        continue
                    possible_moves.add((i + j) % 24)
                if Move.is_correct(i, (i + sum(dices)) % 24, self.points[selected].peek()):
                    possible_moves.add((i + sum(dices)) % 24)
        return possible_moves, selected_set

    @staticmethod
    def _get_pike_type(pike_index) -> int:
        pike_type = 1
        if pike_index % 6 == 1 or pike_index % 6 == 4:
            pike_type = 2
        elif pike_index % 6 == 2 or pike_index % 6 == 3:
            pike_type = 3
        return pike_type