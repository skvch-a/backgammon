import random

from .bot import Bot
from ..constants import BLACK


class RandomBot(Bot):
    def __init__(self, color=BLACK):
        super().__init__(color)

    @property
    def name(self):
        return 'High IQ Alien'

    def get_columns_priority_for_ai(self):
        columns = list(range(23, -1, -1))
        random.shuffle(columns)
        return columns

