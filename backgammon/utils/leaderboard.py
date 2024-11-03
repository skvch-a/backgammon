import os
import json


class Leaderboard:
    def __init__(self):
        self._path = os.path.join(os.path.dirname(__file__), 'leaderboard.json')
        self._records = self._load_records()

    @property
    def records(self):
        return self._records

    def update(self, bot_name, points):
        if points > self._records[bot_name]:
            self._records[bot_name] = points
            self._save_records()

    def _load_records(self):
        with open(self._path, 'r') as file:
            return json.load(file)

    def _save_records(self):
        with open(self._path, 'w') as file:
            json.dump(self._records, file, indent=4)