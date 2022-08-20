class Matrixgrid:
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.matrix = [[1 for col in range(cols)] for row in range(rows)]

    def update_matrix(self, matrix):
        self.matrix = matrix

    def add_obstacle(self, x, y):
        self.x = x
        self.y = y
        self.matrix[x][y] = 0

    def remove_obstacle(self, x, y):
        self.x = x
        self.y = y
        self.matrix[x][y] = 1


"""
x = Matrixgrid(30,42)
x.add_obstacle(x = 1,y = 2)
print (getattr(x, 'matrix'))
"""
