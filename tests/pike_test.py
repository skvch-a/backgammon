import pytest
from backgammon.game_objects import Pike
from backgammon.constants import PIKE_DEFAULT_COLOR, CHECKER_HALF_SIZE, PIKE_WIDTH, PIKE_BASE_HEIGHT

def test_pike_init():
    pike = Pike(100, 200, 1)
    assert pike._color == PIKE_DEFAULT_COLOR
    assert pike._center_x == 100
    assert pike._x == 100 - PIKE_WIDTH / 2
    assert pike._y == 200
    assert pike._signed_height == PIKE_BASE_HEIGHT
    assert pike._render_height == PIKE_BASE_HEIGHT / 1

def test_pike_vertices():
    pike = Pike(100, 200, 1)
    vertices = pike.vertices
    assert vertices[0] == (pike._x, pike._y)
    assert vertices[1] == (pike._x + PIKE_WIDTH, pike._y)
    assert vertices[2] == (pike._center_x, pike._y + pike._render_height)

def test_pike_color():
    pike = Pike(100, 200, 1)
    assert pike.color == PIKE_DEFAULT_COLOR

    pike.change_color((255, 0, 0))
    assert pike.color == (255, 0, 0)

def test_pike_get_checker_position():
    pike = Pike(100, 200, 1)
    checker_position = pike.get_checker_position(0)
    assert checker_position == (pike._center_x - CHECKER_HALF_SIZE, pike._y + pike._signed_height / 15 * 0 - CHECKER_HALF_SIZE)

    checker_position = pike.get_checker_position(1)
    assert checker_position == (pike._center_x - CHECKER_HALF_SIZE, pike._y + pike._signed_height / 15 * 1 - CHECKER_HALF_SIZE)

def test_pike_is_inside():
    pike = Pike(100, 200, 1)
    assert pike.is_inside(100, 200) is True
    assert pike.is_inside(90, 200) is True
    assert pike.is_inside(110, 200) is True
    assert pike.is_inside(100, 210) is True

def test_pike_reverse():
    pike = Pike(100, 200, 1, reverse=True)
    assert pike._signed_height == -PIKE_BASE_HEIGHT
    assert pike._render_height == -PIKE_BASE_HEIGHT / 1

    vertices = pike.vertices
    assert vertices[0] == (pike._x, pike._y)
    assert vertices[1] == (pike._x + PIKE_WIDTH, pike._y)
    assert vertices[2] == (pike._center_x, pike._y + pike._render_height)
