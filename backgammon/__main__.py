from backgammon.game_core.game import Game

if __name__ == "__main__":
    game = Game()
    try:
        game.run()
    except KeyboardInterrupt:
        print('Игра закрыта')
