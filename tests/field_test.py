import pytest

from unittest.mock import MagicMock, patch
from backgammon.constants import *
from backgammon.game_objects import Field
from backgammon.utils import Move

@pytest.fixture
def field():
    return Field()

def test_field_init(field):
    assert len(field.points) == 24
    assert field.last_point_index == {WHITE: 23, BLACK: 11}
    assert field.selected == -1
    assert field.selected_end == -1
    assert len(field.positions) == 12
    assert len(field.position_down) == 12
    assert len(field.pikes) == 24

def test_field_checkers_count(field):
    assert field.checkers_count == CHECKERS_COUNT * 2

def test_field_recolor_pikes(field):
    dices = [1, 2]
    with patch.object(field, '_check_selected') as mock_check_selected:
        mock_check_selected.return_value = (set(), set())
        field.recolor_pikes(dices)
        for pike in field.pikes:
            assert pike.color == PIKE_DEFAULT_COLOR

def test_field_get_pike(field):
    pos = (0, 0)
    with patch.object(field.pikes[0], 'is_inside') as mock_is_inside:
        mock_is_inside.return_value = True
        assert field.get_pike(pos) == 0

def test_field_make_moves(field):
    moves = [MagicMock(), MagicMock()]
    with patch.object(field, 'make_move') as mock_make_move:
        field.make_moves(moves)
        mock_make_move.assert_called()

def test_field_make_move(field):
    move = Move(0, 1, WHITE)
    with patch.object(field, 'is_move_correct') as mock_is_move_correct:
        mock_is_move_correct.return_value = True
        field.make_move(move)
        assert field.points[move.end].peek() == WHITE

def test_field_is_move_correct(field):
    move = Move(0, 1, WHITE)
    assert field.is_move_correct(move) is True

    move = Move(0, 0, WHITE)
    assert field.is_move_correct(move) is False

    move = Move(0, 1, BLACK)
    assert field.is_move_correct(move) is False

def test_field_has_legal_move(field):
    dices = [1, 2]
    color = WHITE
    assert field.has_legal_move(dices, color) is True

def test_field_fill_positions(field):
    assert len(field.positions) == 12
    assert len(field.position_down) == 12

def test_field_get_pike_type(field):
    assert field._get_pike_type(0) == 1
    assert field._get_pike_type(1) == 2
    assert field._get_pike_type(2) == 3

