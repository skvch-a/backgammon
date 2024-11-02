import pygame
from random import randint

from ..bots.smart_bot import SmartBot
from ..buttons.button import Button
from ..constants import WHITE, BLACK, CHECKERS_COUNT


class EventHandler:
    def __init__(self, game):
        self._game = game
        self._is_white_endgame = False
        self._is_black_endgame = False
        self._white_off_board_count = 0
        self._black_off_board_count = 0

    @property
    def is_over(self):
        return self._white_off_board_count == CHECKERS_COUNT or self._black_off_board_count == CHECKERS_COUNT

    def handle_menu_events(self, menu_buttons: list[Button]) -> int:
        events = pygame.event.get()
        self.check_for_quit(events)
        return self.get_pressed_button_index(events, menu_buttons)

    def handle_game_events(self):
        print(self._is_white_endgame, self._is_black_endgame)
        if self.is_endgame_for_white() and self._game.current_color == WHITE:
            self._is_white_endgame = True
            for _ in range(2):
                self.pop_random_checker(18, 23, WHITE)
            pygame.time.wait(1000)
            self._game.switch_turn()
            return

        if self.is_endgame_for_black() and self._game.current_color == BLACK:
            self._is_black_endgame = True
            for _ in range(2):
                self.pop_random_checker(6, 11, BLACK)
            pygame.time.wait(1000)
            self._game.switch_turn()
            return


        if (not self._game.field.has_legal_move(self._game.dices, self._game.current_color) or
                (not self._game.is_bot_move() and len(self._game.dices) == 0)):
            self._game.switch_turn()
        elif self._game.is_bot_move():
            moves = self._game.bot.get_moves(self._game.field, self._game.dices)
            self._game.field.make_moves(moves)
            self._game.switch_turn()
        else:
            # self.handle_player_move()
            bob = SmartBot(WHITE)
            moves = bob.get_moves(self._game.field, self._game.dices)
            self._game.field.make_moves(moves)
            self._game.switch_turn()
            pygame.time.wait(200)

    def handle_player_move(self) -> None:
        events = pygame.event.get()
        self.check_for_quit(events)
        self._game.update_current_dice()
        self.select_pike(events)
        self._game.make_player_move()

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


    def pop_random_checker(self, start, end, color):
        rand = randint(start, end)
        check = self._game.field.points[rand].pop()

        if check == WHITE:
            self._white_off_board_count += 1
            print('попнули белизну')
        if check == BLACK:
            self._black_off_board_count += 1
            print('попнули черноту')

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
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and button.is_pressed(event.pos):
                    is_pressed = True
                    break
