import pytest

from unittest.mock import MagicMock, patch
from backgammon.buttons import MenuButton
from backgammon.game_core import Menu

@pytest.fixture
def menu():
    event_handler = MagicMock()
    renderer = MagicMock()
    records = {}
    return Menu(event_handler, renderer, records)

def test_menu_choose_game_mode(menu):
    with patch.object(menu._renderer, 'draw_menu_background') as mock_draw_menu_background, \
         patch.object(menu._renderer, 'draw_buttons') as mock_draw_buttons, \
         patch.object(menu._renderer, 'draw_records') as mock_draw_records, \
         patch('pygame.display.update') as mock_update, \
         patch.object(menu._event_handler, 'choose_game_mode') as mock_choose_game_mode:

        mock_choose_game_mode.return_value = None

        menu.choose_game_mode()

        mock_draw_menu_background.assert_called_once()
        mock_draw_buttons.assert_called_once_with(*menu._menu_buttons)
        mock_draw_records.assert_called_once_with(menu._records)
        mock_update.assert_called_once()
        mock_choose_game_mode.assert_called_once_with(menu._menu_buttons)
