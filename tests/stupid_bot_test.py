
from unittest.mock import MagicMock
from backgammon.bots import StupidBot
from backgammon.constants import BLACK, WHITE
from backgammon.utils import Move


def test_stupid_bot_init():
    bot = StupidBot(BLACK)
    assert bot._color == BLACK
    assert bot.name == 'Low IQ Alien'

    bot = StupidBot(WHITE)
    assert bot._color == WHITE
    assert bot.name == 'Low IQ Alien'

def test_stupid_bot_name():
    bot = StupidBot(BLACK)
    assert bot.name == 'Low IQ Alien'

def test_stupid_bot_get_moves_no_valid_moves():
    field = MagicMock()
    dices = [1, 2]

    # Mock field.points and field.is_move_correct
    field.points = [MagicMock() for _ in range(24)]
    field.is_move_correct = MagicMock(return_value=False)

    # Set up the mock points
    for i in range(24):
        field.points[i].peek.return_value = BLACK if i % 2 == 0 else None

    bot = StupidBot(BLACK)
    moves = bot.get_moves(field, dices)

    assert moves == []

