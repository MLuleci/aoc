import heapq
import enum

class Direction(enum.IntEnum):
  UP = 0
  RIGHT = 1
  DOWN = 2
  LEFT = 3

def step(x, y, direction):
  if direction == Direction.UP:
    return (x, y - 1)
  if direction == Direction.DOWN:
    return (x, y + 1)
  if direction == Direction.LEFT:
    return (x - 1, y)
  if direction == Direction.RIGHT:
    return (x + 1, y)

def rotate(direction, clockwise):
  if clockwise:
    return Direction((direction + 1) % 4)
  return Direction((direction - 1) % 4)

def solve(grid, min_step=0, max_step=3):
  rows = len(grid)
  cols = len(grid[0])
  q = [(0, 0, 0, Direction.RIGHT, 1), (0, 0, 0, Direction.DOWN, 1)]
  s = set()
  while q:
    cost, x, y, direction, steps = heapq.heappop(q)

    if x == cols - 1 and y == rows - 1 and steps >= min_step:
      return cost

    if (x, y, direction, steps) in s:
      continue

    s.add((x, y, direction, steps))

    if steps >= min_step:
      cw_direction = rotate(direction, True)
      cw_x, cw_y = step(x, y, cw_direction)
      if cw_x >= 0 and cw_x < cols and cw_y >= 0 and cw_y < rows:
        heapq.heappush(q, (cost + grid[cw_y][cw_x], cw_x, cw_y, cw_direction, 1))

      ccw_direction = rotate(direction, False)
      ccw_x, ccw_y = step(x, y, ccw_direction)
      if ccw_x >= 0 and ccw_x < cols and ccw_y >= 0 and ccw_y < rows:
        heapq.heappush(q, (cost + grid[ccw_y][ccw_x], ccw_x, ccw_y, ccw_direction, 1))

    if steps < max_step:
      nx, ny = step(x, y, direction)
      if nx >= 0 and nx < cols and ny >= 0 and ny < rows:
        heapq.heappush(q, (cost + grid[ny][nx], nx, ny, direction, steps + 1))

  return -1

with open("17.txt") as f:
  grid = [ [ int(i) for i in list(s.strip()) ] for s in f.readlines() ]
  print(solve(grid))
  print(solve(grid, 4, 10))
