class Grid:
    def __init__(self, file):
        self.data = [ list(i.strip()) for i in file.readlines() ]
        self.height = len(self.data)
        self.width = len(self.data[0])
    
    def contains(self, x, y):
        return 0 <= x and x < self.width and 0 <= y and y < self.height

    def at(self, x, y):
        return None if not self.contains(x, y) else self.data[y][x]
    
    def _find(self, value):
        for x in range(self.width):
            for y in range(self.height):
                if self.data[y][x] == value:
                    yield (x, y)
        return None
    
    def find(self, value):
        return next(self._find(value))
    
    def find_all(self, value):
        return [ i for i in self._find(value) ]
    
    def __iter__(self):
        return GridIterator(self)
    
    def _n(self, x, y, d):
        n = []
        for dx, dy in d:
            xx, yy = x + dx, y + dy
            value = self.at(xx, yy)
            if value:
                n.append((xx, yy, value))
        return n

    def n4(self, x, y):
        return self._n(x, y, [(-1, 0), (1, 0), (0, -1), (0, 1)])
    
    def n8(self, x, y):
        return self._n(x, y, [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (1, 1), (-1, 1), (1, -1)
        ])
    
    def by_row(self):
        return GridIterator(self)
    
    def by_column(self):
        return GridIterator(self, row_major=False)

class GridIterator:
    def __init__(self, grid, row_major=True):
        self.grid = grid
        self.x = 0
        self.y = 0
        self.row_major = row_major

    def __next__(self):
        x, y = self.x, self.y
        value = self.grid.at(x, y)
        if value:
            if self.row_major:
                self.x += 1
                if self.x >= self.grid.width:
                    self.x = 0
                    self.y += 1
            else:
                self.y += 1
                if self.y >= self.grid.height:
                    self.y = 0
                    self.x += 1
            return x, y, value

        raise StopIteration()