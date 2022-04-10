class Warship:

    def __init__(self, ship_type, size):
        self.ship_type = ship_type
        self.size = size
        self.coords = []

    def plot_vertical(self, row, col):
        for i in range(1, self.size + 1):
            self.coords.append((row, col))
            row = row + 1

    def plot_horizontal(self, row, col):
        for i in range(1, self.size + 1):
            self.coords.append((row, col))
            col = col + 1

    def check_status(self):
        return self.coords == []
