class field:

    def __init__(self, width=10, height=10):
        self.field = [["." for i in range(1, width + 1)] for i in range(1, height + 1)]

    def __getitem__(self, point):
        row, col = point
        return self.field[row][col]

    def __setitem__(self, point, value):
        row, col = point
        self.field[row][col] = value

    def view_ocean(self):
        for row in self.field:
            print(" ".join(row))

    def valid_col(self, row):
        try:
            self.field[row]
            return True
        except IndexError:
            return False

    def valid_row(self, col):
        try:
            self.field[0][col]
            return True
        except IndexError:
            return False

    def can_use_col(self, row, col, size):

        valid_coords = []

        for i in range(size):

            if self.valid_col(col) and self.valid_row(row):
                if self.field[row][col] == ".":
                    valid_coords.append((row, col))
                    col = col + 1
                else:
                    col = col + 1
            else:
                return False

        if size == len(valid_coords):
            return True
        else:
            return False

    def can_use_row(self, row, col, size):

        valid_coords = []

        for i in range(size):

            if self.valid_row(row) and self.valid_col(col):
                if self.field[row][col] == ".":
                    valid_coords.append((row, col))
                    row = row + 1
                else:
                    row = row + 1
            else:
                return False

        if size == len(valid_coords):
            return True
        else:
            return False

    def set_ship_col(self, row, col, size):
        for i in range(1, size + 1):
            self.field[row][col] = "U"
            col = col + 1

    def set_ship_row(self, row, col, size):
        for i in range(1, size + 1):
            self.field[row][col] = "U"
            row = row + 1
