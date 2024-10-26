import pygame
from backgammon.constants import *
from backgammon.move import Move
from backgammon.pike import Pike
from backgammon.game_core.renderer import Renderer
from utils import is_move_correct

class DrawingField:
    def __init__(self, field, screen, game):
        self.field = field
        self.game = game
        self.white_sprite = pygame.image.load(CHECKER_WHITE_PATH)
        self.black_sprite = pygame.image.load(CHECKER_BLACK_PATH)
        self.dice_sprites = []
        for i in range(1, 7):
            sprite = pygame.image.load(f"assets/images/dice_{i}.png")
            self.dice_sprites.append(pygame.transform.scale(sprite, DICE_SIZE))
        self.screen = screen
        self.image = pygame.image.load(FIELD_PATH)
        self.positions = []
        self.position_down = []
        self.fill_positions()
        self.pikes = []
        self.renderer = Renderer(game)
        self.houses_pikes = [Pike(0, 0, 0, 0)] * 2
        for pos in self.positions:
            self.pikes.append(Pike(pos[0], pos[1], 190, 27))
        for pos_down in self.position_down:
            self.pikes.append(Pike(pos_down[0], pos_down[1], -190, 27))


    def output(self, dices):
        self.screen.blit(self.image, FIELD_POS)
        possible_moves, selected_set = self.check_selected(dices)

        self.fill_pikes(possible_moves, selected_set)
        self.fill_columns()

        for color in range(2):
            column = self.field.houses[color]
            pike = self.houses_pikes[color]
            sprite = self.white_sprite if color == WHITE else self.black_sprite
            pike.draw_pikes(self.screen, 1)

            for i in range(column.count):
                self.renderer.draw_checker(pike.center_x, pike.y + pike.height / 15 * i, sprite)

        self.renderer.draw_dices(dices)

    def check_selected(self, dices):
        selected_set = set()
        possible_moves = set()
        for i in range(24):
            selected = self.field.selected
            if selected == i:
                selected_set.add(i)
                for j in dices:
                    if not is_move_correct(
                            i, (i + j) % 24, self.field.columns[selected].peek()
                    ):
                        continue
                    possible_moves.add((i + j) % 24)
                if is_move_correct(
                        i, (i + sum(dices)) % 24, self.field.columns[selected].peek()
                ):
                    possible_moves.add((i + sum(dices)) % 24)

            if i % 6 == 2 or i % 6 == 3:
                self.pikes[i].draw_pikes(self.screen, 3)
            elif i % 6 == 1 or i % 6 == 4:
                self.pikes[i].draw_pikes(self.screen, 2)
            else:
                self.pikes[i].draw_pikes(self.screen, 1)
        return possible_moves, selected_set

    def fill_columns(self):
        for i in range(24):
            pikes_coordinate = (self.pikes[i].center_x, self.pikes[i].y)
            column = self.field.columns[i]
            for j in range(column.count):
                sprite = self.white_sprite
                if column.peek() == 0:
                    sprite = self.black_sprite
                self.renderer.draw_checker(
                    pikes_coordinate[0],
                    pikes_coordinate[1] + self.pikes[i].height / 15 * j,
                    sprite,
                )

    def fill_pikes(self, possible_moves, selected_set):
        for i in range(24):
            pike = self.pikes[i]
            if i in selected_set:
                pike.color = pike.selected_color
            elif i in possible_moves:
                move = Move(
                    self.field.selected,
                    i,
                    self.field.columns[self.field.selected].peek(),
                )
                if self.field.is_correct(move):
                    pike.color = pike.possible_move_color
            else:
                pike.color = pike.default_color

    def fill_positions(self):
        first_position = (FIELD_POS[0] + 666, FIELD_POS[1] + 42)
        self.positions.append(first_position)
        for i in range(1, 12):
            if i == 6:
                self.positions.append(
                    (self.positions[i - 1][0] - 104, first_position[1])
                )
            else:
                self.positions.append(
                    (self.positions[i - 1][0] - 50, first_position[1])
                )

        first_position_down = (FIELD_POS[0] + 62, FIELD_POS[1] + 504)
        self.position_down.append(first_position_down)
        for i in range(1, 12):
            if i == 6:
                self.position_down.append(
                    (self.position_down[i - 1][0] + 104, first_position_down[1])
                )
            else:
                self.position_down.append(
                    (self.position_down[i - 1][0] + 50, first_position_down[1])
                )

    def get_pike_by_coordinates(self, x, y):
        for i in range(24):
            if self.pikes[i].is_inside(x, y):
                return i
        return -1