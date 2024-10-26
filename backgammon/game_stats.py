import json

from backgammon.bots.smart_bot import SmartBot
from backgammon.bots.stupid_bot import StupidBot


class GameState:
    def __init__(self):
        self.name_of_bot = None
        self.bot = None
        self.columns = []
        self.dices = []
        self.current_color = 1


    def save(self):
        stat = {
            'bot_name': self.name_of_bot,
            'columns': self.columns,
            'dices': self.dices,
            'current_step': self.current_color
        }

        with open('leaderboard.json', 'w') as file:
            json.dump(stat, file, indent=4)

    def load(self):
        with (open('leaderboard.json', 'r') as file):
            stat = json.load(file)
            self._get_bot(stat['bot_name'])
            self.columns = stat['columns']
            self.dices = stat['dices']
            self.current_color = stat['current_step']

    def _get_bot(self, bot_name):
        if bot_name == "Smart":
            self.bot = SmartBot()
        elif bot_name == "Stupid":
            self.bot = StupidBot()
        else:
            self.bot = None
