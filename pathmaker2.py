from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

# create path for Enemy


class Pathmaker:
    def __init__(self, matrix):

        # setup
        self.matrix = matrix
        self.grid = Grid(matrix=matrix)
        self.path = []


    def empty_path(self):
        self.path = []

    def create_path(self):
        self.start = self.grid.node(len(self.matrix[0]) // 20, len(self.matrix) // 2)
        #print('start_coord:', len(self.matrix[0]) // 20, len(self.matrix) // 2, 'end_coord:', len(self.matrix[0]) - (len(self.matrix[0]) // 20) - (len(self.matrix[0]) // 10), len(self.matrix) // 2)
        self.end = self.grid.node(len(self.matrix[0]) - (len(self.matrix[0]) // 20) - (len(self.matrix[0]) // 10), len(self.matrix) // 2)
        #print('end_coord:', len(self.matrix[0]) - (len(self.matrix[0]) // 20) - (len(self.matrix[0]) // 10), len(self.matrix) // 2)
        #print('len matrix[0]', len(self.matrix[0]) - (len(self.matrix[0]) // 20),'len matrix', len(self.matrix) // 2)
        self.finder = AStarFinder()
        self.path, _ = self.finder.find_path(self.start, self.end, self.grid)
        self.grid.cleanup()

