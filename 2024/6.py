from enum import Enum

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

def step(x, y, d):
    if d == Direction.UP:
        return x, y - 1
    elif d == Direction.RIGHT:
        return x + 1, y
    elif d == Direction.DOWN:
        return x, y + 1
    else:
        return x - 1, y

def in_bounds(width, height, x, y):
    return 0 <= x and x < width and 0 <= y and y < height

def simulate(grid, rows, cols, x, y):
    d = Direction.UP
    visits = set([(x, y, d)])
    next_x, next_y = step(x, y, d)
    while in_bounds(cols, rows, next_x, next_y):
        ch = grid[next_y][next_x]
        if ch == '#':
            d = Direction((d.value + 1) % 4)
        else:
            x, y = next_x, next_y
        if (x, y, d) in visits:
            return None
        visits.add((x, y, d))
        next_x, next_y = step(x, y, d)
    return visits

with open("6.txt") as f:
    text = f.read()
    index = text.index('^')
    grid = [ list(row) for row in text.split('\n') ]
    rows = len(grid)
    cols = len(grid[0])
    start_x = index % (cols + 1)
    start_y = (index - start_x) // (cols + 1)

    # Silver:
    path = simulate(grid, rows, cols, start_x, start_y)
    visits = set([(x, y) for x, y, _ in path ])
    print(len(visits))

    # Gold:
    tests = 0
    found = set()
    for x, y in visits:
        if (x, y) in found:
            continue
        grid[y][x] = '#'
        if not simulate(grid, rows, cols, start_x, start_y):
            found.add((x, y))
        grid[y][x] = '.'
        tests += 1
        print(f"tested: {tests}, found: {len(found)}", end="\r")
    print()
    print(len(found) - 1) # Can't put obsticle in starting position