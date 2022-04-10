from field import field
from radar import Radar
from warship import Warship
from singleton import Singleton
import random
import pygame

class Player:

    ships = {tuple(["Ship_len5"]): 5, tuple(["Ship_len4"] * 2): 4, tuple(["Ship_len3"] * 3): 3, tuple(["Ship_len2"] * 4): 2}
    
    def __init__(self):
        self.field = field()
        self.radar = Radar()
        self.fleet = []

    def set_fleet(self):
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
                            self.field.set_ship_row(row, col, size, 1)
                            boat = Warship(ship, size)
                            boat.plot_vertical(row, col)
                            self.fleet.append(boat)
                            flag = False

                        else:
                            row = row + 2

                    elif orientation == "h":
                        if self.field.can_use_col(row, col, size):
                            self.field.set_ship_col(row, col, size, 1)
                            boat = Warship(ship, size)
                            boat.plot_horizontal(row, col)
                            self.fleet.append(boat)
                            flag = False

                        else:
                            col = col + 2

                    else:
                        continue

    def register_hit(self, row, col):
        for boat in self.fleet:
            if (row, col) in boat.coords:
                boat.coords.remove((row, col))
                if boat.check_status():
                    self.fleet.remove(boat)

    def strike(self, target, col, row):
        screen = Singleton.screen
        BLACK = Singleton.BLACK
        left_margin = Singleton.left_margin
        upper_margin = Singleton.upper_margin
        block_size = Singleton.block_size

        if self.field.valid_row(row) and self.field.valid_col(col):
            if target.field.field[row][col] == "U":
                target.field.field[row][col] = "X"
                target.register_hit(row, col)
                self.radar.radar[row][col] = "X"
                x1 = block_size * (col) + left_margin
                y1 = block_size * (row) + upper_margin
                pygame.draw.line(screen, BLACK, (x1, y1),
                                 (x1 + block_size, y1 + block_size), block_size // 6)
                pygame.draw.line(screen, BLACK, (x1, y1 + block_size),
                                 (x1 + block_size, y1), block_size // 6)
                return False
            else:
                if self.radar.radar[row][col] == "O" or self.radar.radar[row][col] == "X":
                    print("you already hit there")
                    return False
                else:
                    pygame.draw.circle(screen, BLACK, (block_size * (
                            col + 0.5) + left_margin, block_size * (row + 0.5) + upper_margin), block_size // 6)
                    self.radar.radar[row][col] = "O"
                    return True
        else:
            print("Coordinates out of range")
            return False

