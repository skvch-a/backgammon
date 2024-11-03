import pygame
import logging

from ..bots.smart_bot import SmartBot
from ..bots.stupid_bot import StupidBot
from ..buttons.button import Button
from ..constants import WHITE, BLACK, CHECKERS_COUNT

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EventHandler:
    def __init__(self, game):
        self._game = game
        self._is_white_endgame = False
        self._is_black_endgame = False
        self._white_off_board_count = 0
        self._black_off_board_count = 0

    def get_winner(self):
        if self._white_off_board_count == CHECKERS_COUNT:
            logging.info("WINNER REQUESTED - White wins.")
            return WHITE
        if self._black_off_board_count == CHECKERS_COUNT:
            logging.info("WINNER REQUESTED - Black wins.")
            return BLACK

    def choose_game_mode(self, menu_buttons):
        while True:
            pressed_button_index = self.check_for_menu_buttons_pressed(menu_buttons)
            if pressed_button_index == 0:
                logging.info("HOTSEAT mode selected.")
                return
            elif pressed_button_index == 1:
                logging.info("STUPID-BOT mode selected.")
                return StupidBot()
            elif pressed_button_index == 2:
                logging.info("SMART-BOT mode selected.")
                return SmartBot()

    def check_for_menu_buttons_pressed(self, menu_buttons: list[Button]) -> int:
        events = pygame.event.get()
        self.check_for_quit(events)
        return self.get_pressed_button_index(events, menu_buttons)

    def handle_game_events(self):
        if self._game.current_color == WHITE:
            logging.info('White move.')
        else:
            logging.info('Black move.')

        if self.is_endgame_for_white() and self._game.current_color == WHITE:
            self._is_white_endgame = True
            self.pop_checkers(WHITE)
            self._game.switch_turn()
            return

        if self.is_endgame_for_black() and self._game.current_color == BLACK:
            self._is_black_endgame = True
            self.pop_checkers(BLACK)
            self._game.switch_turn()
            return

        if self._game.is_bot_move():
            moves = self._game.bot.get_moves(self._game.field, self._game.dices)
            logging.info(f"Bot move: {moves}")
            self._game.field.make_moves(moves)
        else:
            self.handle_player_move()
        self._game.switch_turn()

    def handle_player_move(self) -> None:
        while self._game.field.has_legal_move(self._game.dices, self._game.current_color) or len(self._game.dices) != 0:
            events = pygame.event.get()
            self.check_for_quit(events)
            self._game.update_current_dice()
            self.select_pike(events)
            self._game.make_player_move()
            self._game.render()

    def select_pike(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self._game.field.get_pike(event.pos)
                if event.button == 1:
                    target_column_color = self._game.field.points[selected].peek()
                    if target_column_color == self._game.current_color:
                        self._game.field.selected = selected
                elif event.button == 3:
                    self._game.field.selected_end = selected

    def pop_checkers(self, color):
        if color == WHITE:
            last_idx = 24
        else:
            last_idx = 12
        pop_idx_1 = last_idx - self._game.dices[0]
        pop_idx_2 = last_idx - self._game.dices[1]
        for pop_idx in [pop_idx_1, pop_idx_2]:
            check = self._game.field.points[pop_idx].peek()
            logging.info(f"{color} checker removed from position {pop_idx}.")
            if check == color:
                self._game.field.points[pop_idx].pop()
                if color == WHITE:
                    self._white_off_board_count += 1
                elif color == BLACK:
                    self._black_off_board_count += 1
        self._game.dices.clear()

    def is_endgame_for_white(self):
        return self._is_white_endgame or self._is_endgame_for(18, 23, WHITE)

    def is_endgame_for_black(self):
        return self._is_black_endgame or self._is_endgame_for(6, 11, BLACK)

    def _is_endgame_for(self, start_opponent_house_index, end_opponent_house_index, color):
        checkers_count = 0
        for i in range(start_opponent_house_index, end_opponent_house_index + 1):
            point = self._game.field.points[i]
            if point.color == color:
                checkers_count += point.count

        return checkers_count == CHECKERS_COUNT

    @staticmethod
    def check_for_quit(events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                logging.info("Game quit by player.")
                pygame.quit()
                exit()

    @staticmethod
    def get_pressed_button_index(events: list[pygame.event.Event], buttons: list[Button]) -> int:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button_index in range(len(buttons)):
                    if buttons[button_index].is_pressed(event.pos):
                        return button_index

    @staticmethod
    def wait_until_button_pressed(button) -> None:
        is_pressed = False
        while not is_pressed:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    logging.info("Game quit by player.")
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and button.is_pressed(event.pos):
                    is_pressed = True
                    break
