import pytest

from unittest.mock import MagicMock, patch
from backgammon.game_core import EventHandler, Renderer
from backgammon.game_objects import Field
from backgammon.game_core.game import Game
from backgammon.utils import Leaderboard

@pytest.fixture
def game():
    return Game()

def test_game_init(game):
    assert isinstance(game._leaderboard, Leaderboard)
    assert isinstance(game._renderer, Renderer)
    assert isinstance(game._field, Field)
    assert isinstance(game._event_handler, EventHandler)
    assert game._dices == []
    assert game._is_endgame is False
    assert game._current_color == 1
    assert game._selected_pike == 0
    assert game._bot is None

def test_game_render(game):
    with patch.object(game._renderer, 'render') as mock_render:
        game.render()
        mock_render.assert_called_once_with(game._field, game._dices, game._current_color, None)

def test_game_change_color(game):
    game.change_color()
    assert game._current_color == 0
    game.change_color()
    assert game._current_color == 1

def test_game_switch_turn(game):
    with patch.object(game, 'change_color') as mock_change_color, \
         patch.object(game, 'render') as mock_render, \
         patch.object(game, 'throw_dices') as mock_throw_dices:

        game.switch_turn()

        mock_change_color.assert_called_once()
        mock_render.assert_called_once()
        mock_throw_dices.assert_called_once()

def test_game_is_bot_move(game):
    game._bot = MagicMock()
    game._bot.color = 1
    game._current_color = 1
    assert game.is_bot_move() is True

    game._bot.color = 0
    assert game.is_bot_move() is False

    game._bot = None
    assert game.is_bot_move() is False

def test_game_make_player_move(game):
    game._field.selected = 0
    game._field.selected_end = 1
    game._current_color = 1
    game._dices = [1]

    with patch.object(game._field, 'is_move_correct') as mock_is_move_correct, \
         patch.object(game._field, 'make_move') as mock_make_move:

        mock_is_move_correct.return_value = True

        game.make_player_move()

        mock_is_move_correct.assert_called_once()
        mock_make_move.assert_called_once()
        assert game._dices == []
        assert game._field.selected == -1
