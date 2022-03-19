from player import Player
from warship import Warship
import random


class Bot(Player):

    def __init__(self):
        super().__init__()

    def set_compu_fleet(self):
        positions = ["v", "h"]

        for ship, size in self.ships.items():

            flag = True
            while flag:
                row = random.randint(0, 9)
                col = random.randint(0, 9)
                orientation = random.choice(positions)

                if orientation == "v":
                    if self.field.can_use_row(row, col, size):
                        self.field.set_ship_row(row, col, size)
                        boat = Warship(ship, size)
                        boat.plot_vertical(row, col)
                        self.fleet.append(boat)
                        flag = False

                    else:
                        row = row + 2

                elif orientation == "h":
                    if self.field.can_use_col(row, col, size):
                        self.field.set_ship_col(row, col, size)
                        boat = Warship(ship, size)
                        boat.plot_horizontal(row, col)
                        self.fleet.append(boat)
                        flag = False

                    else:
                        col = col + 2

                else:
                    continue

    # Automated strike function

    def compu_strike(self, target):
        row = random.randint(0, 9)
        col = random.randint(0, 9)

        if self.radar.radar[row][col] == ".":
            input("...Target acquired....%s, %s" % (row, col))

            if target.field.field[row][col] == "U":
                print("DIRECT HIT!")
                target.field.field[row][col] = "X"
                target.register_hit(row, col)
                self.radar.radar[row][col] = "X"

            else:
                print("Missed....recalibrating")
                self.radar.radar[row][col] = "O"

        else:
            self.compu_strike(target)
