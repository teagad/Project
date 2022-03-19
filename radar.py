class Radar:

    def __init__(self, width=10, height=10):
        self.radar = [["." for i in range(1, width + 1)] for i in range(1, height + 1)]

    def __getitem__(self, point):
        row, col = point
        return self.radar[row][col]

    def __setitem__(self, point, value):
        row, col = point
        self.radar[row][col] = value

    def view_radar(self):
        print("Radar")
        for row in self.radar:
            print(" ".join(row))
