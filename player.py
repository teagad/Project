from field import field
from radar import Radar
from warship import Warship
import os

class Player:

    ships = {"Ship_len4": 4, "Ship_len3": 3, "Ship_len2": 2, "Ship_len1": 1}

    def __init__(self):
        self.field = field()
        self.radar = Radar()
        self.fleet = []

    def set_fleet(self):
        input("Pick a coordinate between 1 and 10 for the columns and rows on your board")
        input("Boats are placed form right to left.")
        for ship, size in self.ships.items():

            flag = True
            while flag:
                self.view_console()
                print("Place your %s" % (ship))
                row = int(input("Pick a row for head of the ship =)")) - 1
                col = int(input("Pick a column for head of the ship =)")) - 1
                orientation = str(input("Vertical or Horizontal v or h"))

                if orientation == "v":
                    if self.field.can_use_row(row, col, size):
                        self.field.set_ship_row(row, col, size)
                        boat = Warship(ship, size)
                        boat.plot_vertical(row, col)
                        self.fleet.append(boat)
                        flag = False
                    else:
                        input("Overlapping ships, try again")

                elif orientation == "h":
                    if self.field.can_use_col(row, col, size):
                        self.field.set_ship_col(row, col, size)
                        boat = Warship(ship, size)
                        boat.plot_horizontal(row, col)
                        self.fleet.append(boat)
                        flag = False
                    else:
                        input("Overlapping ships, try agin")

                else:
                    continue

                self.view_console()
                input("press Enter to continue")
                os.system('clear')


    def view_console(self):
        self.radar.view_radar()
        print("Yours desk")
        self.field.view_ocean()

    def register_hit(self, row, col):
        for boat in self.fleet:
            if (row, col) in boat.coords:
                boat.coords.remove((row, col))
                if boat.check_status():
                    self.fleet.remove(boat)
                    print("%s has been sunk!" % (boat.ship_type))

    # Player interface for initiating in-game strikes,
    # updates the state of the boards of both players

    def strike(self, target):
        self.view_console()
        row = int(input("Pick a row ")) - 1
        col = int(input("Pick a column ")) - 1

        if self.field.valid_row(row) and self.field.valid_col(col):
            if target.field.field[row][col] == "U":
                print("DIRECT HIT!!!")
                target.field.field[row][col] = "X"
                target.register_hit(row, col)
                self.radar.radar[row][col] = "X"

            else:
                if self.radar.radar[row][col] == "O":
                    print("Area already hit....Check your radar!")
                    self.strike(target)
                else:
                    print("Missed")
                    self.radar.radar[row][col] = "O"

        else:
            print("Coordinates out of range...")
            self.strike(target)
        input()
        os.system('clear')