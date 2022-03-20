from attr import field
from bot import Bot
from player import Player
import os


class BattleshipsCOMP:

    def __init__(self):
        self.step_bot()

    def fleet_sunk(self, player):
        for row in player.field.field:
            for element in row:
                if  element == "U":
                    return False
        return True
            

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
        print("\n")
        input("\npress Enter to start the game")
        self.clear_screen()

        while  True:
            p.strike(c)
            if self.fleet_sunk(c) is True:
                self.victory_message()
                break
            else:
                c.compu_strike(p)
                if self.fleet_sunk(p) is True:
                    self.victory_message()
                    break
                else:
                    self.clear_screen()
