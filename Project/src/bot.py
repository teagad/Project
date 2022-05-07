import pygame
import random
from src.player import Player
from src.singleton import Singleton
from src.warship import Warship


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
        if self.radar.radar[row][col] == ".":
            if target.field.field[row][col] == "U":
                target.field.field[row][col] = "X"
                target.register_hit(row, col)
                self.radar.radar[row][col] = "X"
                x1 = Singleton.block_size * (col + 15) + Singleton.left_margin
                y1 = Singleton.block_size * (row) + Singleton.upper_margin
                pygame.draw.line(Singleton.screen, Singleton.black, (x1, y1),
                                 (x1 + Singleton.block_size, y1 + Singleton.block_size), Singleton.block_size // 6)
                pygame.draw.line(Singleton.screen, Singleton.black, (x1, y1 + Singleton.block_size),
                                 (x1 + Singleton.block_size, y1), Singleton.block_size // 6)
                if Singleton.user_points > 0:
                    Singleton.user_points -= 1
                return True

            else:
                target.field.field[row][col] = "O"
                pygame.draw.circle(Singleton.screen, Singleton.black, (Singleton.block_size * (
                        col + 0.5 + 15) + Singleton.left_margin, Singleton.block_size * (
                                                                                   row + 0.5) + Singleton.upper_margin),
                                   Singleton.block_size // 6)
                self.radar.radar[row][col] = "O"
                return False

        else:
            return True
