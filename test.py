import unittest

from backgammon.bots.smart_bot import SmartBot
from backgammon.bots.stupid_bot import StupidBot
from backgammon.game import *


class NerdsTests(unittest.TestCase):
    def setUp(self):
        self.field_only_black = self.create_empty_field()

        self.field_only_black.columns[0].checkers.append(0)
        self.field_only_black.columns[2].checkers.append(0)
        self.field_only_black.columns[3].checkers.append(1)

        self.field_only_black.columns[10].checkers.append(0)
        self.field_only_black.columns[11].checkers.append(0)
        self.field_only_black.columns[22].checkers.append(0)
        self.field_only_black.columns[23].checkers.append(0)

    @staticmethod
    def create_empty_field():
        field = Field()
        for column in field.columns:
            column.checkers = []
        return field

    def _check_move(self, field, move, dice, expected):
        actual = field.is_correct(move, dice)
        self.assertEqual(expected, actual)

    def test_correct_move(self):
        move = Move(0, 2, BLACK)
        self._check_move(self.field_only_black, move, 2, True)

    def test_incorrect_move_wrong_checker_at_end(self):
        move = Move(0, 3, BLACK)
        self._check_move(self.field_only_black, move, 3, False)

    def test_incorrect_move_wrong_checker_at_start(self):
        move = Move(3, 4, BLACK)
        self._check_move(self.field_only_black, move, 1, False)

    def test_incorrect_move_dice_not_match(self):
        move = Move(0, 2, BLACK)
        self._check_move(self.field_only_black, move, 5, False)

    def test_incorrect_move_dice_black_step_out(self):
        move = Move(10, 12, BLACK)
        self._check_move(self.field_only_black, move, 1, False)

    def test_correct_move_dice_black_step_out_first_half(self):
        move = Move(23, 0, BLACK)
        self._check_move(self.field_only_black, move, 1, True)

    def test_is_inside(self):
        x = 111
        y = 124

        field = DrawingField(self.field_only_black, pygame.display.set_mode((900, 800)))
        self.assertTrue(field.pikes[11].is_inside(x, y))

    def test_is_there_legal_move(self):
        field = self.create_empty_field()
        columns = field.columns
        columns[0].push(WHITE)
        columns[1].push(BLACK)
        columns[2].push(BLACK)
        dices = [1, 1]
        self.assertFalse(field.has_legal_move(dices, WHITE))
        self.assertTrue(field.has_legal_move(dices, BLACK))

    def test_is_there_legal_move_sum_of_moves_is_legal(self):
        field = self.create_empty_field()
        columns = field.columns
        columns[0].push(WHITE)
        columns[1].push(BLACK)
        columns[2].push(BLACK)
        dices = [1, 2]
        self.assertTrue(field.has_legal_move(dices, WHITE))

    def test_is_there_legal_move_step_out(self):
        field = self.create_empty_field()
        columns = field.columns
        columns[11].push(BLACK)
        dices = [2, 2]
        self.assertFalse(field.has_legal_move(dices, BLACK))

        field = self.create_empty_field()
        columns = field.columns
        columns[10].push(BLACK)
        dices = [2, 2]
        self.assertFalse(field.has_legal_move(dices, BLACK))

    def test_is_there_legal_can_endgame(self):
        field = self.create_empty_field()
        columns = field.columns
        for i in range(12):
            columns[11].push(BLACK)
        dices = [random.randint(1, 6), random.randint(1, 6)]
        self.assertTrue(field.has_legal_move(dices, BLACK))

    def test_can_endgame_house_is_empty(self):
        field = self.create_empty_field()
        columns = field.columns
        for i in range(12):
            columns[11].push(BLACK)

        self.assertTrue(field.can_endgame(BLACK))

        field = self.create_empty_field()
        columns = field.columns
        for i in range(11):
            columns[11].push(BLACK)

        self.assertFalse(field.can_endgame(BLACK))

    def test_can_endgame_house_is_not_empty(self):
        field = self.create_empty_field()
        columns = field.columns
        for i in range(11):
            columns[11].push(BLACK)
        field.houses[BLACK].push(BLACK)

        self.assertTrue(field.can_endgame(BLACK))

        field = self.create_empty_field()
        columns = field.columns
        for i in range(10):
            columns[11].push(BLACK)
        field.houses[BLACK].push(BLACK)

        self.assertFalse(field.can_endgame(BLACK))

    def test_bot_gives_legal_moves(self):
        field = Field()
        bot_white = StupidBot(WHITE)
        bot_black = SmartBot(BLACK)

        for i in range(10):
            dices = [1, 3]
            moves = bot_white.get_moves(field, dices)
            for move in moves:
                self.assertTrue(field.is_correct(move))
                field.make_move(move)

            dices = [1, 2]
            moves = bot_black.get_moves(field, dices)
            for move in moves:
                self.assertTrue(field.is_correct(move))
                field.make_move(move)

    def test_bot_does_not_give_moves_if_no_legal(self):
        field = self.create_empty_field()
        bot = StupidBot(BLACK)

        columns = field.columns

        columns[0].push(BLACK)
        columns[1].push(WHITE)
        columns[2].push(WHITE)
        columns[3].push(WHITE)
        columns[4].push(WHITE)

        dices = [2, 1]

        moves = bot.get_moves(field, dices)
        self.assertTrue(len(moves) == 0)

    def test_stupid_bot_is_stupid(self):
        field = self.create_empty_field()
        bot = StupidBot(WHITE)

        columns = field.columns

        columns[0].push(WHITE)
        columns[1].push(WHITE)
        dices = [5, 6]

        actual_moves = bot.get_moves(field, dices)
        expected_moves = [Move(1, 1 + 5 + 6, WHITE)]

        for i in range(len(expected_moves)):
            expected_move = expected_moves[i]
            actual_move = actual_moves[i]

            self.assertEqual(expected_move.start, actual_move.start)
            self.assertEqual(expected_move.end, actual_move.end)


def get_random_dices():
    return [random.randint(1, 6) for _ in range(2)]
