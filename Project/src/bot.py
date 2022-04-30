from src.player import Player
from src.warship import Warship
from src.singleton import Singleton
import pygame
from time import sleep
import random


class Bot(Player):

    def __init__(self):
        super().__init__()

    def set_compu_fleet(self):
        positions = ["v", "h"]
        for ship_type, size in self.ships.items():
            for ship in ship_type:
                flag = True
                while flag:
                    row = random.randint(0, 9)
                    col = random.randint(0, 9)
                    orientation = random.choice(positions)

                    if orientation == "v":
                        if self.field.can_use_row(row, col, size):
                            self.field.set_ship_row(row, col, size, 0)
                            boat = Warship(ship, size)
                            boat.plot_vertical(row, col)
                            self.fleet.append(boat)
                            flag = False

                        else:
                            row = row + 2

                    elif orientation == "h":
                        if self.field.can_use_col(row, col, size):
                            self.field.set_ship_col(row, col, size, 0)
                            boat = Warship(ship, size)
                            boat.plot_horizontal(row, col)
                            self.fleet.append(boat)
                            flag = False

                        else:
                            col = col + 2

                    else:
                        continue

    def compu_strike(self, target):
        row = random.randint(0, 9)
        col = random.randint(0, 9)
        screen = Singleton.screen
        BLACK = Singleton.BLACK
        left_margin = Singleton.left_margin
        upper_margin = Singleton.upper_margin
        block_size = Singleton.block_size
        if self.radar.radar[row][col] == ".":
            if target.field.field[row][col] == "U":
                target.field.field[row][col] = "X"
                target.register_hit(row, col)
                self.radar.radar[row][col] = "X"
                x1 = block_size * (col + 15) + left_margin
                y1 = block_size * (row) + upper_margin
                pygame.draw.line(screen, BLACK, (x1, y1),
                                 (x1 + block_size, y1 + block_size), block_size // 6)
                pygame.draw.line(screen, BLACK, (x1, y1 + block_size),
                                 (x1 + block_size, y1), block_size // 6)
                return True

            else:
                target.field.field[row][col] = "O"
                pygame.draw.circle(screen, BLACK, (block_size * (
                        col + 0.5 + 15) + left_margin, block_size * (row + 0.5) + upper_margin), block_size // 6)
                self.radar.radar[row][col] = "O"
                return False

        else:
            return True
