import pytest

from backgammon.game_objects import Point
from backgammon.constants import WHITE, BLACK, NONE

def test_point_init_empty():
    point = Point()
    assert point.count == 0
    assert point.color == NONE

def test_point_init_with_checkers():
    point = Point([WHITE, WHITE])
    assert point.count == 2
    assert point.color == WHITE

    point = Point([BLACK, BLACK])
    assert point.count == 2
    assert point.color == BLACK

def test_point_init_with_mixed_checkers():
    with pytest.raises(ValueError):
        Point([WHITE, BLACK])

def test_point_push():
    point = Point()
    point.push(WHITE)
    assert point.count == 1
    assert point.color == WHITE

    point.push(WHITE)
    assert point.count == 2
    assert point.color == WHITE

    with pytest.raises(ValueError):
        point.push(BLACK)

def test_point_pop():
    point = Point([WHITE, WHITE])
    assert point.pop() == WHITE
    assert point.count == 1
    assert point.color == WHITE

    assert point.pop() == WHITE
    assert point.count == 0
    assert point.color == NONE

    point.pop()  # Should not raise an error

def test_point_peek():
    point = Point([WHITE, WHITE])
    assert point.peek() == WHITE

    point.pop()
    assert point.peek() == WHITE

    point.pop()
    assert point.peek() is None

def test_point_color():
    point = Point([WHITE, WHITE])
    assert point.color == WHITE

    point = Point([BLACK, BLACK])
    assert point.color == BLACK

    point = Point()
    assert point.color == NONE

def test_point_count():
    point = Point([WHITE, WHITE])
    assert point.count == 2

    point.pop()
    assert point.count == 1

    point.pop()
    assert point.count == 0
