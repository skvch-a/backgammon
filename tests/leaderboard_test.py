import pytest

from unittest.mock import MagicMock, patch
from backgammon.utils import Leaderboard

@pytest.fixture
def leaderboard():
    return Leaderboard()

def test_leaderboard_init(leaderboard):
    assert leaderboard._path.endswith('leaderboard.json')
    assert isinstance(leaderboard._records, dict)

def test_leaderboard_records(leaderboard):
    assert isinstance(leaderboard.records, dict)

def test_leaderboard_update(leaderboard):
    bot_name = 'Low IQ Alien'
    points = 10
    with patch.object(leaderboard, '_save_records') as mock_save_records:
        leaderboard.update(bot_name, points)
        mock_save_records.assert_called_once()
        assert leaderboard._records[bot_name] == points

def test_leaderboard_load_records(leaderboard):
    with patch('builtins.open', new_callable=MagicMock) as mock_open, \
         patch('json.load') as mock_load:

        mock_open.return_value.__enter__.return_value = MagicMock()
        mock_load.return_value = {'Bot1': 10}

        records = leaderboard._load_records()

        mock_open.assert_called_once_with(leaderboard._path, 'r')
        mock_load.assert_called_once()
        assert records == {'Bot1': 10}

def test_leaderboard_save_records(leaderboard):
    with patch('builtins.open', new_callable=MagicMock) as mock_open, \
         patch('json.dump') as mock_dump:

        mock_open.return_value.__enter__.return_value = MagicMock()

        leaderboard._save_records()

        mock_open.assert_called_once_with(leaderboard._path, 'w')
        mock_dump.assert_called_once_with(leaderboard._records, mock_open.return_value.__enter__.return_value, indent=4)
