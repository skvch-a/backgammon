from unittest.mock import MagicMock
from backgammon.bots import SimpleBot
from backgammon.constants import BLACK, WHITE


def test_stupid_bot_init():
    bot = SimpleBot(BLACK)
    assert bot._color == BLACK
    assert bot.name == 'Low IQ Alien'

    bot = SimpleBot(WHITE)
    assert bot._color == WHITE
    assert bot.name == 'Low IQ Alien'

def test_stupid_bot_name():
    bot = SimpleBot(BLACK)
    assert bot.name == 'Low IQ Alien'

def test_stupid_bot_get_moves_no_valid_moves():
    field = MagicMock()
    dices = [1, 2]

    field.points = [MagicMock() for _ in range(24)]
    field.is_move_correct = MagicMock(return_value=False)

    for i in range(24):
        field.points[i].peek.return_value = BLACK if i % 2 == 0 else None

    bot = SimpleBot(BLACK)
    moves = bot.get_moves(field, dices)

    assert moves == []

