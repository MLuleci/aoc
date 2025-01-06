from functools import lru_cache

move_to_delta = {
    '^': (0, -1),
    '>': (1, 0),
    'v': (0, 1),
    '<': (-1, 0)
}

def gps(grid, char='O'):
    hash = 0
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == char:
                hash += 100 * i + j
    return hash

def step(grid, robot, move):
    x, y = robot
    dx, dy = move
    while 0 <= x and x < len(grid[0]) and 0 <= y and y < len(grid):
        if grid[y][x] in ('#', '.'):
            break
        x, y = x + dx, y + dy
    
    if grid[y][x] == '#':
        return grid, robot
    
    rx, ry = robot
    tmp = grid[y][x]
    while not (x == rx and y == ry):
        nx, ny = x - dx, y - dy
        grid[y][x] = grid[ny][nx]
        x, y = nx, ny
    grid[y][x] = tmp

    return grid, (x + dx, y + dy)

def expand(grid):
    new_grid = []
    for row in grid:
        new_row = []
        for cell in row:
            if cell == '#':
                new_row.extend([ '#', '#' ])
            elif cell == '.':
                new_row.extend([ '.', '.' ])
            elif cell == 'O':
                new_row.extend([ '[', ']' ])
            else:
                new_row.extend([ '@', '.' ])
        new_grid.append(new_row)
    return new_grid

def print_grid(grid):
    for row in grid:
        for cell in row:
            print(cell, end='')
        print()

def clone(grid):
    new_grid = []
    for row in grid:
        new_grid.append(row[:])
    return new_grid

def find_robot(grid):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == '@':
                return (j, i)

def step_2(grid, robot, move):
    dx, dy = move

    @lru_cache
    def can_move(x, y):
        cell = grid[y][x]
        if cell == '#':
            return False
        if cell == '.':
            return True
        
        nx, ny = x + dx, y + dy
        to_check = [(nx, ny)]
        if grid[ny][nx] == '[':
            if dx == 1: # moving to the right, check right edge only
                to_check = [(nx + 1, ny)]
            else:
                to_check.append((nx + 1, ny))
        elif grid[ny][nx] == ']':
            if dx == -1: # same as above, check left edge only
                to_check = [(nx - 1, ny)]
            else:
                to_check.append((nx - 1, ny))
        
        return all(can_move(i, j) for i, j in to_check)
    
    def move_recursive(x, y):
        cell = grid[y][x]
        if cell == '.':
            return

        nx, ny = x + dx, y + dy
        next_cell = grid[ny][nx]
        if next_cell == '[':
            move_recursive(nx + 1, ny)
        elif next_cell == ']':
            move_recursive(nx - 1, ny)
        move_recursive(nx, ny)
        grid[y][x], grid[ny][nx] = '.', cell

    x, y = robot
    if can_move(x, y):
        move_recursive(x, y)
        x += dx
        y += dy
    return grid, (x, y)

with open("15.txt") as f:
    grid, moves = f.read().split("\n\n")
    grid = [ list(i) for i in grid.splitlines() ]
    moves = [ move_to_delta[i] for i in ''.join(moves.splitlines()) ]

    grid_i = clone(grid)
    robot = find_robot(grid_i)
    for move in moves:
        grid_i, robot = step(grid_i, robot, move)
    print(gps(grid_i))

    grid_i = expand(grid)
    robot = find_robot(grid_i)
    for move in moves:
        grid_i, robot = step_2(grid_i, robot, move)
    print(gps(grid_i, char='['))