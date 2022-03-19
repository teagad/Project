from field import field
from radar import Radar
from warship import Warship
import os

class Player:

    ships = {tuple(["Ship_len5"]): 5, tuple(["Ship_len4"] * 2): 4, tuple(["Ship_len3"] * 3): 3, tuple(["Ship_len2"] * 4): 2}
    
    def __init__(self):
        self.field = field()
        self.radar = Radar()
        self.fleet = []

    def set_fleet(self):
        input("Pick a coordinate between 1 and 10 for the rows and between 'A'-'Z' for colums on your board(press Enter to continue)")
        input("Boats are placed form right to left(press Enter to continue)")

        alphabet = {"A" : 0, "B" : 1, "C" : 2, "D" : 3, "E" : 4, "F" : 5, "G" : 6, "H" : 7, "I" : 8, "J" : 9}

        for ship_type, size in self.ships.items():
            for ship in ship_type:
                flag = True
                while flag:
                    self.view_console()
                    print("Place your %s" % (ship))
                    row = int(input("Pick a row for head of the ship =)")) - 1
                    col = alphabet[input("Pick a column for head of the ship =)").upper()]
                    orientation = str(input("Vertical or Horizontal v or h"))

                    if orientation.lower() == "v":
                        if self.field.can_use_row(row, col, size):
                            self.field.set_ship_row(row, col, size)
                            boat = Warship(ship, size)
                            boat.plot_vertical(row, col)
                            self.fleet.append(boat)
                            flag = False
                        else:
                            input("Overlapping ships")

                    elif orientation.lower() == "h":
                        if self.field.can_use_col(row, col, size):
                            self.field.set_ship_col(row, col, size)
                            boat = Warship(ship, size)
                            boat.plot_horizontal(row, col)
                            self.fleet.append(boat)
                            flag = False
                        else:
                            input("Overlapping ships")

                    else:
                        continue

                    self.view_console()
                    input("press Enter to clear the consloe")
                    os.system('clear')


    def view_console(self):
        self.radar.view_radar()
        self.field.view_ocean()

    def register_hit(self, row, col):
        for boat in self.fleet:
            if (row, col) in boat.coords:
                boat.coords.remove((row, col))
                if boat.check_status():
                    self.fleet.remove(boat)
                    print("%s has been sunk" % (boat.ship_type))

    def strike(self, target):
        alphabet = {"A" : 0, "B" : 1, "C" : 2, "D" : 3, "E" : 4, "F" : 5, "G" : 6, "H" : 7, "I" : 8, "J" : 9}
        self.view_console()
        row = int(input("Pick a row to make a shot")) - 1
        col = alphabet[input("Pick a colum to make a shot").upper()]

        if self.field.valid_row(row) and self.field.valid_col(col):
            if target.field.field[row][col] == "U":
                print("direct hit")
                target.field.field[row][col] = "X"
                target.register_hit(row, col)
                self.radar.radar[row][col] = "X"

            else:
                if self.radar.radar[row][col] == "O":
                    print("you already hit there")
                    self.strike(target)
                else:
                    print("Missed")
                    self.radar.radar[row][col] = "O"

        else:
            print("Coordinates out of range")
            self.strike(target)
        os.system('clear')