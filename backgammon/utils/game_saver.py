import os
import json

from ..bots import SimpleBot, RandomBot

class GameSaver:
    def __init__(self, game):
        self._path = os.path.join(os.path.dirname(__file__), 'game_saving.json')
        self._game = game

    def save(self):
        game_state = {
            'game_mode': 'Hotseat' if self._game.bot is None else self._game.bot.name,
            'dices': self._game.dices,
            'turn_color': self._game.current_color,
            'points': self._game.field.serialize_data,
        }

        with open(self._path, 'w') as f:
            json.dump(game_state, f, indent=2)

    def load(self):
        game_modes = {
            'Hotseat' : None,
            'High IQ Alien' : RandomBot(),
            'Low IQ Alien' : SimpleBot()
        }

        with (open(self._path, 'r') as f):
            game_saving = json.load(f)
            try:
                self._game._bot = game_modes[game_saving['game_mode']]
                for i in range(24):
                    self._game.field.points[i]._checkers = game_saving['points'][i]
                self._game._dices = game_saving['dices']
                self._game._current_color = game_saving['turn_color']
                return 0
            except KeyError:
                return -1