import pygame
import logging

from ..constants import WHITE, BLACK, CHECKERS_COUNT
from ..bots import Bot, RandomBot, SimpleBot
from ..buttons import Button
from ..utils.game_saver import GameSaver


class EventHandler:
    def __init__(self, game):
        self._game = game
        self._game_saver = GameSaver(game)
        self._is_white_endgame = False
        self._is_black_endgame = False
        self._white_off_board_count = 0
        self._black_off_board_count = 0

    def get_winner(self) -> int | None:
        if self._white_off_board_count == CHECKERS_COUNT:
            logging.info("WINNER REQUESTED - White wins.")
            return WHITE
        if self._black_off_board_count == CHECKERS_COUNT:
            logging.info("WINNER REQUESTED - Black wins.")
            return BLACK

    def choose_game_mode(self, menu_buttons) -> Bot | None:
        """Позволяет игроку выбрать режим игры

        Args:
            menu_buttons: Кнопки меню
        Returns:
            Bot | None: Экземпляр выбранного бота или None (в случае режима HOTSEAT)
        """
        while True:
            pressed_button_index = self.check_for_buttons_pressed(menu_buttons)
            if pressed_button_index == 0:
                logging.info("HOTSEAT mode selected.")
                return
            elif pressed_button_index == 1:
                logging.info("STUPID_BOT mode selected.")
                return SimpleBot()
            elif pressed_button_index == 2:
                logging.info("SMART_BOT mode selected.")
                return RandomBot()
            elif pressed_button_index == 3:
                exit_code = self._game_saver.load()
                if exit_code == 0:
                    logging.info("Load game from saving.")
                    return self._game.bot


    def check_for_buttons_pressed(self, buttons : list[Button]) -> int | None:
        """Проверяет нажаты ли кнопки, и возвращает индекс нажатой"""
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                logging.info("Game quit by player.")
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button_index in range(len(buttons)):
                    if buttons[button_index].is_pressed(event.pos):
                        return button_index

    def handle_game_events(self):
        if self._game.current_color == WHITE:
            logging.info('White move.')
        else:
            logging.info('Black move.')
        logging.info(f'Dices: {self._game.dices}.')

        if self._is_endgame_for_white() and self._game.current_color == WHITE:
            self._is_white_endgame = True
            self._pop_checkers(WHITE)
        elif self._is_endgame_for_black() and self._game.current_color == BLACK:
            self._is_black_endgame = True
            self._pop_checkers(BLACK)
        elif self._game.is_bot_move():
            moves = self._game.bot.get_moves(self._game.field, self._game.dices)
            logging.info(f"Bot move: {moves}")
            self._game.field.make_moves(moves)
        else:
            self.handle_player_move()

        self._game.switch_turn()

    def handle_player_move(self) -> None:
        while self._game.field.has_legal_move(self._game.dices, self._game.current_color) and len(self._game.dices) != 0:
            events = pygame.event.get()
            self.check_all_for_quit(events)
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

    def _pop_checkers(self, color) -> None:
        """Выводит фишки с доски

        Args:
            color: Цвет шашек, которые нужно удалить
        """
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

    def _is_endgame_for_white(self) -> bool:
        """Проверяет, можно ли выводить фишки с доски белым"""
        return self._is_white_endgame or self._is_endgame_for(18, 23, WHITE)

    def _is_endgame_for_black(self):
        """"Проверяет, можно ли выводить фишки с доски черным"""
        return self._is_black_endgame or self._is_endgame_for(6, 11, BLACK)

    def _is_endgame_for(self, start_opponent_house_index, end_opponent_house_index, color):
        checkers_count = 0
        for i in range(start_opponent_house_index, end_opponent_house_index + 1):
            point = self._game.field.points[i]
            if point.color == color:
                checkers_count += point.count

        return checkers_count == CHECKERS_COUNT

    def check_for_quit(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self._game_saver.save()
            logging.info("Game quit by player.")
            pygame.quit()
            exit()

    def check_all_for_quit(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            self.check_for_quit(event)

    def wait_until_button_pressed(self, button) -> None:
        """Ожидает нажатия заданной кнопки"""
        is_pressed = False
        while not is_pressed:
            events = pygame.event.get()
            for event in events:
                self.check_for_quit(event)
                if event.type == pygame.MOUSEBUTTONDOWN and button.is_pressed(event.pos):
                    is_pressed = True
                    break