UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

def simulate(grid, entry):
  rows = len(grid)
  cols = len(grid[0])

  visits = set()
  exits = set()
  stack = [entry]
  while stack:
    x, y, d = stack.pop()
    if x < 0 or x >= cols or y < 0 or y >= rows:
      exits.add((x, y, d))
      continue
    if (x,y,d) in visits:
      continue

    cell = grid[y][x]
    visits.add((x,y,d))
    if cell == ".":
      if d == UP:
        stack.append((x, y-1, d))
      elif d == RIGHT:
        stack.append((x+1, y, d))
      elif d == DOWN:
        stack.append((x, y+1, d))
      elif d == LEFT:
        stack.append((x-1, y, d))
    elif cell == "/":
      if d == UP:
        stack.append((x+1, y, RIGHT))
      elif d == RIGHT:
        stack.append((x, y-1, UP))
      elif d == DOWN:
        stack.append((x-1, y, LEFT))
      elif d == LEFT:
        stack.append((x, y+1, DOWN))
    elif cell == "\\":
      if d == UP:
        stack.append((x-1, y, LEFT))
      elif d == RIGHT:
        stack.append((x, y+1, DOWN))
      elif d == DOWN:
        stack.append((x+1, y, RIGHT))
      elif d == LEFT:
        stack.append((x, y-1, UP))
    elif cell == "|":
      if d == LEFT or d == RIGHT:
        stack.append((x, y-1, UP))
        stack.append((x, y+1, DOWN))
      else:
        if d == UP:
          stack.append((x, y-1, UP))
        elif d == DOWN:
          stack.append((x, y+1, DOWN))
    elif cell == "-":
      if d == UP or d == DOWN:
        stack.append((x-1, y, LEFT))
        stack.append((x+1, y, RIGHT))
      else:
        if d == LEFT:
          stack.append((x-1, y, LEFT))
        elif d == RIGHT:
          stack.append((x+1, y, RIGHT))

  energy = len(set([ (x, y) for x, y, _ in visits ]))
  return energy, exits

def main():
  with open("16.txt") as f:
    grid = [ list(i.strip()) for i in f.readlines() ]
    energy, _ = simulate(grid, (0, 0, RIGHT))
    print(energy) # Part 1

    rows = len(grid)
    cols = len(grid[0])
    starts = set()

    for x in range(cols):
      starts.add((x, 0, DOWN))
      starts.add((x, rows-1, UP))
    for y in range(rows):
      starts.add((0, y, RIGHT))
      starts.add((cols-1, y, LEFT))
    
    max_energy = 0
    while starts:
      s = starts.pop()
      energy, exits = simulate(grid, s)
      max_energy = max(max_energy, energy)

      for x, y, d in exits:
        if d == UP:
          e = (x, y-1, DOWN)
          if e in starts:
            starts.remove(e)
        elif d == RIGHT:
          e = (x-1, y, LEFT)
          if e in starts:
            starts.remove(e)
        elif d == DOWN:
          e = (x, y+1, UP)
          if e in starts:
            starts.remove(e)
        elif d == LEFT:
          e = (x+1, y, RIGHT)
          if e in starts:
            starts.remove(e)
    print(max_energy)

if __name__ == "__main__":
  main()
