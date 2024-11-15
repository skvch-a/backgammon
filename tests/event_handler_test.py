import pytest
import pygame

from unittest.mock import MagicMock, patch
from backgammon.constants import *
from backgammon.game_core import EventHandler
from backgammon.bots import SimpleBot, RandomBot


@pytest.fixture
def event_handler():
    game = MagicMock()
    return EventHandler(game)

def test_event_handler_init(event_handler):
    assert event_handler._is_white_endgame is False
    assert event_handler._is_black_endgame is False
    assert event_handler._white_off_board_count == 0
    assert event_handler._black_off_board_count == 0

def test_event_handler_get_winner(event_handler):
    event_handler._white_off_board_count = CHECKERS_COUNT
    assert event_handler.get_winner() == WHITE

    event_handler._white_off_board_count = 0
    event_handler._black_off_board_count = CHECKERS_COUNT
    assert event_handler.get_winner() == BLACK

    event_handler._black_off_board_count = 0
    assert event_handler.get_winner() is None

def test_event_handler_choose_game_mode(event_handler):
    buttons = [MagicMock(), MagicMock(), MagicMock()]
    with patch.object(event_handler, 'check_for_buttons_pressed') as mock_check_for_buttons_pressed:
        mock_check_for_buttons_pressed.return_value = 0
        assert event_handler.choose_game_mode(buttons) is None

        mock_check_for_buttons_pressed.return_value = 1
        assert isinstance(event_handler.choose_game_mode(buttons), SimpleBot)

        mock_check_for_buttons_pressed.return_value = 2
        assert isinstance(event_handler.choose_game_mode(buttons), RandomBot)

def test_event_handler_check_for_buttons_pressed(event_handler):
    buttons = [MagicMock(), MagicMock(), MagicMock()]
    buttons[0].is_pressed.return_value = True
    buttons[1].is_pressed.return_value = False
    buttons[2].is_pressed.return_value = False

    with patch('pygame.event.get') as mock_event_get:
        mock_event_get.return_value = [MagicMock(type=pygame.MOUSEBUTTONDOWN, pos=(0, 0))]

        assert event_handler.check_for_buttons_pressed(buttons) == 0

def test_event_handler_handle_game_events(event_handler):
    event_handler._game.current_color = WHITE
    event_handler._game.is_bot_move.return_value = False

    with patch.object(event_handler, 'handle_player_move') as mock_handle_player_move, \
         patch.object(event_handler._game, 'switch_turn') as mock_switch_turn:

        event_handler.handle_game_events()

        mock_handle_player_move.assert_called_once()
        mock_switch_turn.assert_called_once()

def test_event_handler_select_pike(event_handler):
    events = [MagicMock(type=pygame.MOUSEBUTTONDOWN, pos=(0, 0), button=1)]
    event_handler._game.field.get_pike.return_value = 0
    event_handler._game.field.points[0].peek.return_value = WHITE
    event_handler._game.current_color = WHITE

    event_handler.select_pike(events)

    assert event_handler._game.field.selected == 0

def test_event_handler_pop_checkers(event_handler):
    event_handler._game.dices = [1, 2]
    event_handler._game.field.points[23].peek.return_value = WHITE
    event_handler._game.field.points[23].pop.return_value = None

    event_handler._pop_checkers(WHITE)

    assert event_handler._white_off_board_count == 2
    assert event_handler._game.dices == []

def test_event_handler_check_for_quit(event_handler):
    events = [MagicMock(type=pygame.QUIT)]
    with patch('pygame.quit') as mock_quit, \
         patch('builtins.exit') as mock_exit:

        event_handler.check_all_for_quit(events)

        mock_quit.assert_called_once()
        mock_exit.assert_called_once()

def test_event_handler_wait_until_button_pressed(event_handler):
    button = MagicMock()
    button.is_pressed.return_value = True

    with patch('pygame.event.get') as mock_event_get:
        mock_event_get.return_value = [MagicMock(type=pygame.MOUSEBUTTONDOWN, pos=(0, 0))]

        event_handler.wait_until_button_pressed(button)
        button.is_pressed.assert_called_once_with((0, 0))
