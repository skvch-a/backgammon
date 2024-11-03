import logging
from backgammon.game_core.game import Game

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    game = Game()
    try:
        game.run()
    except KeyboardInterrupt:
        logging.info('Game closed.')
