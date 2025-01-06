def dfs(grid, start_x, start_y):
  seen = set()

  def iter(x, y):
    if grid[y][x] == 9:
      seen.add((x, y))
      return 1
    
    neighbours = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        xx = x + dx
        yy = y + dy
        if xx < 0 or yy < 0 or xx >= len(grid[0]) or yy >= len(grid):
          continue
        if grid[yy][xx] == grid[y][x] + 1:
          neighbours.append((xx, yy))
    
    return sum(iter(xx, yy) for xx, yy in neighbours)

  count = iter(start_x, start_y)
  return len(seen), count

with open("10.txt") as f:
  grid = [ [ int(i) for i in row.strip() ] for row in f.readlines() ]
  starts = []
  for y in range(len(grid)):
    for x in range(len(grid[y])):
      if grid[y][x] == 0:
        starts.append((x, y))
  
  total_score = 0
  total_rating = 0
  for x, y in starts:
    score, rating = dfs(grid, x, y)
    total_score += score
    total_rating += rating
  print(total_score, total_rating)