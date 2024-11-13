from .bot import Bot
from ..constants import BLACK


class SimpleBot(Bot):
    def __init__(self, color=BLACK):
        super().__init__(color)

    @property
    def name(self):
        return 'Low IQ Alien'

    def get_columns_priority_for_ai(self):
        return list(range(23, -1, -1))
