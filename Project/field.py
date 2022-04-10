from singleton import Singleton as bc
import pygame


class field:

    def __init__(self, width=10, height=10):
        self.field = [["." for i in range(1, width + 1)] for i in range(1, height + 1)]

    def __getitem__(self, point):
        return self.field[point[0]][point[1]]

    def __setitem__(self, point, value):
        row, col = point
        self.field[row][col] = value

    def view_ocean(self):
        print("Yours desk\n\n")
        row_number = 1
        colum_names = ["A","B","C","D","E","F",'G','H','I','J']
        print("   " + " ".join(colum_names))
        for row in self.field:
            print(str(row_number).ljust(2) + " " + " ".join(row))
            row_number += 1
        print()

    def valid_col(self, row):
        try:
            self.field[row]
            return True
        except IndexError:
            return False

    def valid_row(self, col):
        try:
            #0 is rand number from 0 to 9
            self.field[0][col]
            return True
        except IndexError:
            return False

    def can_use_col(self, row, col, size):
        for i in range(size):
            if self.valid_col(col) and self.valid_row(row) :
                for i in [-1,0,1]:
                    for j in [-1,0,1]:
                        if ( self.valid_row(row+i) and  self.valid_col(col+j)):
                            if  self.field[row+i][col+j] == "U":
                                return False 
            else:
                return False
            col = col + 1
        return True


    def can_use_row(self, row, col, size):
        for i in range(size):
            if self.valid_col(col) and self.valid_row(row):
                for i in [-1,0,1]:
                    for j in [-1,0,1]:
                        if ( self.valid_row(row+i) and  self.valid_col(col+j)):
                            if  self.field[row+i][col+j] == "U":
                                return False     
            else:
                return False
            row = row + 1
        return True

    def set_ship_col(self, row, col, size, pl_or_bot):
        if pl_or_bot:
            ship_width = size * bc.block_size
            ship_height = bc.block_size
            x = bc.block_size * (col + 15) + bc.left_margin
            y = bc.block_size * (row) + bc.upper_margin
            pygame.draw.rect(bc.screen, bc.BLACK, ((x, y), (ship_width, ship_height)), width=bc.block_size//10)
        for i in range(1, size + 1):
            self.field[row][col] = "U"
            col = col + 1

    def set_ship_row(self, row, col, size, pl_or_bot):
        if pl_or_bot:
            ship_width = bc.block_size
            ship_height = size * bc.block_size
            x = bc.block_size * (col + 15) + bc.left_margin
            y = bc.block_size * (row) + bc.upper_margin
            pygame.draw.rect(bc.screen, bc.BLACK, ((x, y), (ship_width, ship_height)), width=bc.block_size // 10)
        for i in range(1, size + 1):
            self.field[row][col] = "U"
            row = row + 1
