import pytest

from unittest.mock import MagicMock, patch
from backgammon.constants import *
from backgammon.game_core import Renderer

@pytest.fixture
def renderer():
    return Renderer()

def test_renderer_init(renderer):
    assert renderer._screen is not None
    assert renderer._field_image is not None
    assert renderer._font is not None
    assert renderer._dice_sprites is not None
    assert renderer._game_bg is not None
    assert renderer._dices_box_rect is not None
    assert renderer._throw_dices_button_image is not None
    assert renderer._white_checker_image is not None
    assert renderer._black_checker_image is not None
    assert renderer.menu_bg is not None

def test_renderer_render(renderer):
    field = MagicMock()
    dices = [1, 2]
    current_color = WHITE

    with patch.object(renderer, '_draw_field') as mock_draw_field, \
         patch.object(renderer, '_draw_win_text') as mock_draw_win_text, \
         patch.object(renderer, '_draw_turn_text') as mock_draw_turn_text, \
         patch('pygame.display.update') as mock_update:

        renderer.render(field, dices, current_color)

        mock_draw_field.assert_called_once_with(field, dices, current_color)
        mock_draw_turn_text.assert_called_once_with(current_color)
        mock_update.assert_called_once()

def test_renderer_draw_buttons(renderer):
    buttons = [MagicMock(), MagicMock()]
    with patch.object(buttons[0], 'draw') as mock_draw_button_1, \
         patch.object(buttons[1], 'draw') as mock_draw_button_2:

        renderer.draw_buttons(*buttons)

        mock_draw_button_1.assert_called_once_with(renderer._screen)
        mock_draw_button_2.assert_called_once_with(renderer._screen)

def test_renderer_draw_records(renderer):
    records = {'Bot1': 10, 'Bot2': 20}
    with patch.object(renderer, '_draw_text') as mock_draw_text:
        renderer.draw_records(records)
        mock_draw_text.assert_called()

def test_renderer_draw_turn_text(renderer):
    current_color = WHITE
    with patch.object(renderer, '_draw_text') as mock_draw_text:
        renderer._draw_turn_text(current_color)
        mock_draw_text.assert_called_once()

def test_renderer_draw_win_text(renderer):
    current_color = WHITE
    with patch.object(renderer, '_draw_text') as mock_draw_text:
        renderer._draw_win_text(current_color)
        mock_draw_text.assert_called_once()

def test_renderer_draw_checkers(renderer):
    points = [MagicMock(), MagicMock()]
    pikes = [MagicMock(), MagicMock()]
    with patch.object(renderer, '_draw_checker') as mock_draw_checker:
        renderer._draw_checkers(points, pikes)
        mock_draw_checker.assert_called()

def test_renderer_draw_pikes(renderer):
    pikes = [MagicMock(), MagicMock()]
    with patch.object(renderer, '_draw_pike') as mock_draw_pike:
        renderer._draw_pikes(pikes)
        mock_draw_pike.assert_called()

def test_renderer_draw_field(renderer):
    field = MagicMock()
    dices = [1, 2]
    current_color = WHITE
    with patch.object(renderer, '_draw_game_bg') as mock_draw_game_bg, \
         patch.object(renderer, '_draw_field_bg') as mock_draw_field_bg, \
         patch.object(field, 'recolor_pikes') as mock_recolor_pikes, \
         patch.object(renderer, '_draw_pikes') as mock_draw_pikes, \
         patch.object(renderer, '_draw_checkers') as mock_draw_checkers, \
         patch.object(renderer, '_draw_dices') as mock_draw_dices:

        renderer._draw_field(field, dices, current_color)

        mock_draw_game_bg.assert_called_once()
        mock_draw_field_bg.assert_called_once()
        mock_recolor_pikes.assert_called_once_with(dices)
        mock_draw_pikes.assert_called_once_with(field.pikes)
        mock_draw_checkers.assert_called_once_with(field.points, field.pikes)
        mock_draw_dices.assert_called_once_with(dices, current_color)
