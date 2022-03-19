from bot import Bot
from player import Player
import os


class BattleshipsCOMP:

    def __init__(self):
        self.step_bot()

    def fleet_sunk(self, player):
        ship_counters = 0
        for row in range(len(player.field.field)):
            for col in range(len(player.field.field)):
                if player.field.field[row][col] == "U":
                    ship_counters += 1
        if ship_counters == 0:
            return True
        else:
            return False

    def clear_screen(self):
        os.system('clear')

    def victory_message(self):
        print("END OF THE GAME")

    def step_bot(self):
        p = Player()
        p.set_fleet()
        p.view_console()
        self.clear_screen()

        c = Bot()
        c.set_compu_fleet()
        print("bot sets fleet")
        input("\npress Enter to clear the consloe")
        self.clear_screen()

        flag = True
        while flag is True:
            p.strike(c)
            if self.fleet_sunk(c) is True:
                self.victory_message()
                flag = False
            else:
                self.clear_screen()

                c.compu_strike(p)
                if self.fleet_sunk(p) is True:
                    self.victory_message()
                    flag = False
                else:
                    self.clear_screen()
