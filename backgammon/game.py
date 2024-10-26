import random
from os import walk

import pygame

from backgammon.bots.stupid_bot import StupidBot
from backgammon.color_saves import ColorsSaver
from backgammon.column import Column
from backgammon.constants import *
from backgammon.drawing_field import DrawingField
from backgammon.field import Field
from backgammon.game_stats import GameState
from backgammon.event_handler import EventHandler
from backgammon.menu import choose_game_mode
from backgammon.move import Move
from backgammon.utils import update_controls


class Game:
    def __init__(self):
        self.dices = [3, 4]
        self.current_dice = -1
        self.field = Field()
        self.winner = NONE
        self.current_color = 1
        self.last_dice = (-1, WHITE)
        self.selected_pike = 0

        self.is_new_game = True
        self.needed_color = ColorsSaver()
        self.secret_flag = False

        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((900, 600))
        self.drawing_field = DrawingField(self.field)
        pygame.display.set_caption(TITLE)
        self.font = pygame.font.SysFont("Comic Sans", 18)
        self.bot = StupidBot()


        self.field.columns = [Column(i) for i in
                              [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [], [], [], [], [], [], [], [], [], [], [],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [], [], [], [], [], [], [], [], [], [], []]]

        self.event_handler = EventHandler(self)

    def run(self):
        choose_game_mode(self.screen)

        while self.winner == NONE:
            if not self.field.is_there_legal_move(self.dices, self.current_color):

                self.throw_bones()
                self.current_color = (self.current_color + 1) % 2
                update_controls(
                    BG_COLOR, self.screen, self.drawing_field, self.dices, self.secret_flag, self.needed_color
                )
                self.draw_text()
                pygame.time.wait(16)
                pygame.display.update()
                continue

            self.get_winner()

            if self.bot is not None and self.bot.color == self.current_color:
                moves = self.bot.get_moves(self.field, self.dices)
                for move in moves:
                    self.field.make_move(move)
                    if self.field.can_endgame(self.bot.color):
                        break
                pygame.time.wait(1000)
                self.throw_bones()
                self.current_color = (self.current_color + 1) % 2
                continue

            self.event_handler.handle_events()
            self.make_move_by_mouse()

            if len(self.dices) == 0:
                self.throw_bones()
                self.current_color = (self.current_color + 1) % 2

            update_controls(
                BG_COLOR, self.screen, self.drawing_field, self.dices, self.secret_flag, self.needed_color
            )
            self.draw_text()
            pygame.time.wait(16)
            pygame.display.update()

        while True:
            update_controls(BG_COLOR, self.screen, self.drawing_field, self.dices, self.secret_flag, self.current_color)

            winner = ''
            if self.winner == WHITE:
                winner = 'White'
            if self.winner == BLACK:
                winner = 'Black'

            text_surface = self.font.render(f'{winner} won', 0,
                                            (0, 0, 0), (255, 255, 255))
            self.screen.blit(text_surface, (350, 0))
            pygame.display.update()

    def throw_bones(self):
        self.dices = [random.randint(1, 6), random.randint(1, 6)]

    def make_move_by_mouse(self):
        if self.field.selected_end != -1:
            last_column_index = self.field.last_column_index[self.current_color]
            if self.field.selected_end == last_column_index:
                if self.field.can_endgame(self.current_color):
                    move = Move(last_column_index, last_column_index + 1, self.current_color)
                    self.field.make_move(move)
                    self.field.selected = -1
                    self.field.selected_end = -1
                    self.dices = []
                    return

            if (self.field.selected_end - self.field.selected) % 24 in self.dices:
                move = Move(self.field.selected, self.field.selected_end, self.current_color)
                if self.field.is_correct(move):
                    self.field.make_move(move)
                    self.dices.remove((self.field.selected_end - self.field.selected) % 24)
                    self.field.selected = -1

            elif (self.field.selected_end - self.field.selected) % 24 == sum(self.dices):
                move = Move(self.field.selected, self.field.selected_end, self.current_color)
                if self.field.is_correct(move):
                    self.field.make_move(move)
                    self.dices = []
                    self.field.selected = -1
        self.field.selected_end = -1

    def get_winner(self):
        if self.field.houses[BLACK].count == 12:
            self.winner = BLACK
            pygame.time.wait(10)
            pygame.quit()
        elif self.field.houses[WHITE].count == 12:
            self.winner = WHITE
            pygame.time.wait(10)
            pygame.quit()

    def draw_text(self):
        if (self.current_color % 2) == 1:
            text_surface = self.font.render(
                f"White move", 0, (0, 0, 0), (255, 255, 255)
            )
        else:
            text_surface = self.font.render(
                f"Black move", 0, (0, 0, 0), (255, 255, 255)
            )
        self.screen.blit(text_surface, (350, 0))

