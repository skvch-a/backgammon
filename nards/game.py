from field import *
import pygame
import controls
from drawing_field import DrawingField
import random
from os import walk
from game_stats import GameState
from os import path, makedirs
from color_saves import ColorsSaver
from nards.bots.smart_bot import SmartBot
from nards.bots.stupid_bot import StupidBot


class Game:
    def __init__(self):
        self.dices = [0, 0]
        self.current_dice = -1
        self.field = Field()
        self.winner = NONE
        self.current_color = 1
        self.last_dice = (-1, WHITE)
        self.selected_pike = 0
        self.music = next(walk("assets/music"), (None, None, []))[2]
        self.number_of_music = 0
        self.is_new_game = True
        self.needed_color = ColorsSaver()
        self.secret_flag = False


        pygame.font.init()
        self.screen = pygame.display.set_mode((900, 600))
        self.drawing_field = DrawingField(self.field)
        pygame.display.set_caption("Зелёный слоник")
        self.font = pygame.font.SysFont("Comic Sans", 18)

        self.bot = StupidBot(BLACK)

    def menu(self):

        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("assets/music/" + self.music[self.number_of_music])
        pygame.mixer.music.play(-1)

        button_pvp_rect = pygame.Rect(0, 75, MENU_BUTTON_WIDTH, 300)
        button_pve_stupid_rect = pygame.Rect(MENU_BUTTON_WIDTH, 75, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
        button_pve_smart_rect = pygame.Rect(2 * MENU_BUTTON_WIDTH, 75, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
        button_continue_rect = pygame.Rect(0.75 * MENU_BUTTON_WIDTH, 400, 500, 200)

        button_pvp_image = pygame.image.load("assets/images/Человек.jpg")
        button_pvp_image = pygame.transform.scale(
            button_pvp_image, button_pvp_rect.size
        )

        button_pve_stupid_image = pygame.image.load("assets/images/Тупой.png")
        button_pve_stupid_image = pygame.transform.scale(
            button_pve_stupid_image, button_pve_stupid_rect.size
        )

        button_pve_smart_image = pygame.image.load("assets/images/Умный дом.png")
        button_pve_smart_image = pygame.transform.scale(
            button_pve_smart_image, button_pve_stupid_rect.size
        )

        button_continue_image = pygame.image.load("assets/images/continue.png")
        button_continue_image = pygame.transform.scale(
            button_continue_image, button_continue_rect.size
        )


        while True:
            self.screen.fill((255, 255, 255))
            self.screen.blit(button_pvp_image, button_pvp_rect)
            self.screen.blit(button_pve_stupid_image, button_pve_stupid_rect)
            self.screen.blit(button_pve_smart_image, button_pve_smart_rect)
            self.screen.blit(button_continue_image, button_continue_rect)

            pygame.time.wait(16)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if button_pvp_rect.collidepoint(mouse_pos):
                        self.bot = None
                        return
                    elif button_pve_stupid_rect.collidepoint(mouse_pos):
                        self.bot = StupidBot(BLACK)
                        return
                    elif button_pve_smart_rect.collidepoint(mouse_pos):
                        self.bot = SmartBot(BLACK)
                        return
                    elif button_continue_rect.collidepoint(mouse_pos):
                        self.is_new_game = False
                        return
            pygame.display.update()

    def run(self):
        self.menu()

        if self.is_new_game:
            self.game_state = self.load_fresh_game()
        else:
            self.game_state = self.load_saved_game()

        self.load_info_from_game_stats()
        while self.winner == NONE:
            if not self.field.is_there_legal_move(self.dices, self.current_color):
                pygame.time.wait(300)
                self.throw_bones()
                self.current_color = (self.current_color + 1) % 2
                controls.update(
                    BG_COLOR, self.screen, self.drawing_field, self.dices, self.secret_flag, self.needed_color
                )
                self.draw_text()
                pygame.time.wait(16)
                pygame.display.update()
                continue
            self.get_winner()

            if self.bot is not None:
                if self.bot.color == self.current_color:
                    moves = self.game_state.bot.get_moves(self.field, self.dices)
                    for move in moves:
                        self.field.make_move(move)
                        if self.field.can_endgame(self.bot.color):
                            break
                    pygame.time.wait(1000)
                    self.throw_bones()
                    self.current_color = (self.current_color + 1) % 2
                    continue

            events = pygame.event.get()
            self.check_events(events)
            self.select_column_and_dice(events)
            self.make_move_by_pressing_button(events)
            self.make_move_by_mouse()

            if len(self.dices) == 0:
                self.throw_bones()
                self.current_color = (self.current_color + 1) % 2

            controls.update(
                BG_COLOR, self.screen, self.drawing_field, self.dices, self.secret_flag, self.needed_color
            )
            self.draw_text()
            pygame.time.wait(16)
            pygame.display.update()

        while True:
            controls.update(BG_COLOR, self.screen, self.drawing_field,
                            self.dices, self.secret_flag, self.current_color)

            winner = ''
            if self.winner == WHITE:
                winner = 'White'
            if self.winner == BLACK:
                winner = 'Black'

            text_surface = self.font.render(f'{winner} won', 0,
                                            (0, 0, 0), (255, 255, 255))
            self.screen.blit(text_surface, (350, 0))
            pygame.display.update()

    def check_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.save_info_in_game_stats()
                    self.pause()
            if event.type == pygame.QUIT:
                self.save_info_in_game_stats()
                self.game_state.save()
                pygame.quit()

    def save_info_in_game_stats(self):
        self.game_state.columns = [column.checkers for column in self.field.columns]
        self.game_state.name_of_bot = str(self.bot)
        self.game_state.current_color = self.current_color
        self.game_state.dices = self.dices.copy()
        self.game_state.save()

    def load_info_from_game_stats(self):
        self.field.columns = [Column(i) for i in self.game_state.columns]
        self.current_color = self.game_state.current_color
        self.bot = self.game_state.bot
        self.dices = self.game_state.dices

    def init_window(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Зелёный слоник")
        self.drawing_field = DrawingField(self.field)

    def throw_bones(self):
        self.dices = [random.randint(1, 6), random.randint(1, 6)]

    def select_column_and_dice(self, events):
        self.select_dice(events)
        self.select_pike(events)

    def make_move_by_pressing_button(self, events):
        move = Move(
            self.field.selected,
            self.field.selected + self.dices[self.current_dice % 2],
            self.current_color,
        )
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    if self.field.is_correct(move):
                        self.field.make_move(move)
                        self.dices.pop(self.current_dice)

    def make_move_by_mouse(self):
        if self.field.selected_end != -1:
            last_column_index = self.field.last_column_index[self.current_color]
            if self.field.selected_end == last_column_index:
                if self.field.can_endgame(self.current_color):
                    move = Move(
                        last_column_index, last_column_index + 1, self.current_color
                    )
                    self.field.make_move(move)
                    self.field.selected = -1
                    self.field.selected_end = -1
                    self.dices = []
                    return

            if (self.field.selected_end - self.field.selected) % 24 in self.dices:
                move = Move(
                    self.field.selected, self.field.selected_end, self.current_color
                )
                if self.field.is_correct(move):
                    self.field.make_move(move)
                    self.dices.remove(
                        (self.field.selected_end - self.field.selected) % 24
                    )
                    self.field.selected = -1

            elif (self.field.selected_end - self.field.selected) % 24 == sum(
                    self.dices
            ):
                move = Move(
                    self.field.selected, self.field.selected_end, self.current_color
                )
                if self.field.is_correct(move):
                    self.field.make_move(move)
                    self.dices = []
                    self.field.selected = -1
        self.field.selected_end = -1

    def select_dice(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.current_dice = 0
                if event.key == pygame.K_2:
                    self.current_dice = 1
        self.current_dice %= len(self.dices)

    def select_pike(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    for i in range(self.field.selected - 69, self.field.selected):
                        if self.field.columns[i % 24].peek() == self.current_color:
                            self.field.selected = i % 24
                if event.key == pygame.K_RIGHT:
                    for i in range(self.field.selected + 1, 69 + self.field.selected):
                        if self.field.columns[i % 24].peek() == self.current_color:
                            self.field.selected = i % 24

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                selected = self.drawing_field.get_pike_by_coordinates(x, y)
                target_column_color = self.field.columns[selected].peek()
                if event.button == 1:
                    if target_column_color == self.current_color:
                        self.field.selected = selected
                elif event.button == 3:
                    self.field.selected_end = selected

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

    def pause(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                if event.type == pygame.QUIT:
                    self.save_info_in_game_stats()
                    self.game_state.save()
                    pygame.quit()
            text = self.font.render(
                f"Paused", 0, (0, 0, 0), (255, 255, 255)
            )
            self.screen.fill((255, 255, 255), (0, 0, 999, 30))
            self.screen.blit(text, (350, 0))
            pygame.time.wait(16)
            pygame.display.update()

    def load_fresh_game(self):
        game_state = GameState()
        game_state.current_color = 1
        game_state.name_of_bot = str(self.bot)
        game_state.dices = [3, 4]
        game_state.columns = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [], [], [], [], [], [], [], [], [], [], [],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [], [], [], [], [], [], [], [], [], [], []]
        game_state.save()
        game_state.load()

        return game_state

    def load_saved_game(self):
        game_state = GameState()
        if not path.exists('jsons'):
            makedirs('jsons')
        if not path.isfile('jsons/game_state.json'):
            with open('jsons/game_state.json', 'w'):
                pass
            game_state = self.load_fresh_game()
            game_state.save()
        game_state.load()
        return game_state