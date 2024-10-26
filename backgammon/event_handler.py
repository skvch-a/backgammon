import pygame
from backgammon.move import Move


class EventHandler:
    def __init__(self, game):
        self._game = game

    def handle_game_events(self):
        events = pygame.event.get()
        self.check_for_quit(events)
        self.select_dice(events)
        self.select_pike(events)
        self.make_move_by_pressing_button(events)

    def handle_menu_events(self, menu_buttons):
        events = pygame.event.get()
        self.check_for_quit(events)
        return self.get_pressed_button_index(events, menu_buttons)

    def select_dice(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self._game.current_dice = 0
                if event.key == pygame.K_2:
                    self._game.current_dice = 1
        self._game.current_dice %= len(self._game.dices)

    def select_pike(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    for i in range(self._game.field.selected - 69, self._game.field.selected):
                        if self._game.field.columns[i % 24].peek() == self._game.current_color:
                            self._game.field.selected = i % 24
                if event.key == pygame.K_RIGHT:
                    for i in range(self._game.field.selected + 1, 69 + self._game.field.selected):
                        if self._game.field.columns[i % 24].peek() == self._game.current_color:
                            self._game.field.selected = i % 24

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                selected = self._game.drawing_field.get_pike_by_coordinates(x, y)
                target_column_color = self._game.field.columns[selected].peek()
                if event.button == 1:
                    if target_column_color == self._game.current_color:
                        self._game.field.selected = selected
                elif event.button == 3:
                    self._game.field.selected_end = selected

    def make_move_by_pressing_button(self, events):
        move = Move(
            self._game.field.selected,
            self._game.field.selected + self._game.dices[self._game.current_dice % 2],
            self._game.current_color,
        )
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    if self._game.field.is_correct(move):
                        self._game.field.make_move(move)
                        self._game.dices.pop(self._game.current_dice)

    @staticmethod
    def check_for_quit(events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    @staticmethod
    def get_pressed_button_index(events, buttons):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button_index in range(len(buttons)):
                    if buttons[button_index].is_pressed(mouse_pos):
                        return button_index
