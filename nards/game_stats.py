import json
from os import path, makedirs
from SmartBot import SmartBot
from StupidBot import StupidBot
from nards.constants import BLACK


class GameState:
    def __init__(self):
        self.name_of_bot = None
        self.bot = None
        self.columns = []
        self.dices = []
        self.current_color = 1
        self.dictionary_of_bots = {
            "None": None,
            "Stupid": StupidBot(BLACK),
            "Smart": SmartBot(BLACK)
        }

    def save(self):
        game_state = {
            'bot': self.name_of_bot,
            'columns': self.columns,
            'dices': self.dices,
            'current_step': self.current_color
        }

        if not path.exists('jsons'):
            makedirs('jsons')

        with open('jsons/game_state.json', 'w') as f:
            json.dump(game_state, f)

    def load(self):
        with (open('jsons/game_state.json', 'r') as f):
            game_state = json.load(f)
            self.bot = self.dictionary_of_bots[game_state['bot']]
            self.columns = game_state['columns']
            self.dices = game_state['dices']
            self.current_color = game_state['current_step']
