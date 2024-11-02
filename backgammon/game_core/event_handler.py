import pygame

from ..buttons.button import Button


class EventHandler:
    def __init__(self, game):
        self._game = game

    def handle_menu_events(self, menu_buttons: list[Button]) -> int:
        events = pygame.event.get()
        self.check_for_quit(events)
        return self.get_pressed_button_index(events, menu_buttons)

    def handle_game_events(self):
        if (not self._game.field.has_legal_move(self._game.dices, self._game.current_color) or
                (not self._game.is_bot_move() and len(self._game.dices) == 0)):
            self._game.switch_turn()
        elif self._game.is_bot_move():
            moves = self._game.bot.get_moves(self._game.field, self._game.dices)
            self._game.field.make_moves(moves)
            self._game.switch_turn()
        else:
            self.handle_player_move()

    def handle_player_move(self) -> None:
        events = pygame.event.get()
        self.check_for_quit(events)
        self._game.update_current_dice()
        self.select_pike(events)
        self._game.make_player_move()

    def select_pike(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    for i in range(self._game.field.selected - 69, self._game.field.selected):
                        if self._game.field.points[i % 24].peek() == self._game.current_color:
                            self._game.field.selected = i % 24
                if event.key == pygame.K_RIGHT:
                    for i in range(self._game.field.selected + 1, 69 + self._game.field.selected):
                        if self._game.field.points[i % 24].peek() == self._game.current_color:
                            self._game.field.selected = i % 24

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                selected = self._game.field.get_pike_by_coordinates(x, y)
                target_column_color = self._game.field.points[selected].peek()
                if event.button == 1:
                    if target_column_color == self._game.current_color:
                        self._game.field.selected = selected
                elif event.button == 3:
                    self._game.field.selected_end = selected

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
