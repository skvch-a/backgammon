import pygame
from backgammon.constants import *
from backgammon.move import Move
from backgammon.pike import Pike


class DrawingField:
    def __init__(self, field, screen):
        self.field = field
        self.white_sprite = pygame.image.load("assets/images/checker_white.png")
        self.black_sprite = pygame.image.load("assets/images/checker_black.png")
        self.dice_sprites = [self.white_sprite] * 7
        for i in range(1, 7):
            sprite = pygame.image.load(f"assets/images/dice_{i}.png")
            self.dice_sprites[i] = pygame.transform.scale(sprite, (50, 50))
        self.screen = screen
        self.image = pygame.image.load("assets/images/field.png")
        self.x_coord = 84
        self.y_coord = 120
        self.positions = []
        self.position_down = []
        self.fill_positions()
        self.pikes = []
        self.houses_pikes = [Pike(0, 0, 0, 0)] * 2
        for pos in self.positions:
            self.pikes.append(Pike(pos[0], pos[1], 190, 27))
        for pos_down in self.position_down:
            self.pikes.append(Pike(pos_down[0], pos_down[1], -190, 27))

        black_house_pos = (self.x_coord - 20, self.y_coord)
        white_house_pos = (self.x_coord + self.image.get_width() + 20, self.y_coord)
        self.houses_pikes[WHITE] = Pike(white_house_pos[0], white_house_pos[1], 190, 27)
        self.houses_pikes[WHITE].color = (255, 192, 203)
        self.houses_pikes[BLACK] = Pike(black_house_pos[0], black_house_pos[1], 190, 27)
        self.houses_pikes[BLACK].color = (255, 192, 203)

    def output(self, dices):
        self.screen.blit(self.image, (self.x_coord, self.y_coord))
        possible_moves, selected_set = self.check_selected(dices)

        self.fill_pikes(possible_moves, selected_set)

        self.fill_columns()

        for color in range(2):
            column = self.field.houses[color]
            pike = self.houses_pikes[color]
            sprite = self.white_sprite if color == WHITE else self.black_sprite
            pike.draw_pikes(self.screen, 1)

            for i in range(column.count):
                self.draw_checker(pike.center_x, pike.y + pike.height / 15 * i, sprite)

        self.draw_dices(dices)

    def check_selected(self, dices):
        selected_set = set()
        possible_moves = set()
        for i in range(24):
            selected = self.field.selected
            if selected == i:
                selected_set.add(i)
                a = self.field.columns[selected].peek()
                for j in dices:
                    if not is_move_in_range(
                            i, (i + j) % 24, self.field.columns[selected].peek()
                    ):
                        continue
                    possible_moves.add((i + j) % 24)
                if is_move_in_range(
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
                self.draw_checker(
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

    def draw_dices(self, dices):
        c = 0
        for i in dices:
            self.screen.blit(
                self.dice_sprites[i],
                (self.x_coord + 320 + c * 50, self.y_coord + c + 250),
            )
            c += 1

    def fill_positions(self):
        first_position = (self.x_coord + 666, self.y_coord + 42)
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

        first_position_down = (self.x_coord + 62, self.y_coord + 504)
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

    def draw_checker(self, center_x, center_y, sprite):
        self.screen.blit(sprite, (center_x - 13.5, center_y - 13.5))

    def get_pike_by_coordinates(self, x, y):
        for i in range(24):
            if self.pikes[i].is_inside(x, y):
                return i
        return -1


def is_move_in_range(start, end, color):
    if color == WHITE:
        if start >= end:
            return False
    else:
        if start < 12 <= end:
            return False
    return True
