def expand(data, x, y):
  plots = set()
  perimeter = 0
  corners = 0
  q = [(x, y)]
  while q:
    nq = []
    for x, y in q:
      if (x, y) in plots:
        continue
      plots.add((x, y))
      neighbours = set()
      for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(data[0]) and 0 <= ny < len(data) and data[ny][nx] == data[y][x]:
          nq.append((nx, ny))
          neighbours.add((dx, dy))
        else:
          perimeter += 1

      neighbours = list(neighbours)
      num_neighbours = len(neighbours)
      if num_neighbours == 0: # No neighbours = all four corners
        corners += 4
      elif num_neighbours == 1: # One neighbour = three corners
        corners += 2
      elif num_neighbours == 2:
        n1, n2 = neighbours[0], neighbours[1]
        if n1[0] == -n2[0] or n1[1] == -n2[1]:
          corners += 0 # ...in a straight line = no corners
        else: # ...at a right angle...
          dx, dy = n1[0] + n2[0], n1[1] + n2[1]
          nx, ny = x + dx, y + dy
          if data[ny][nx] == data[y][x]:
            corners += 1
          else:
            corners += 2
      elif num_neighbours > 2: # 3+ neighbours...
        for i in range(num_neighbours - 1):
          n1 = neighbours[i]
          for j in range(i + 1, num_neighbours):
            n2 = neighbours[j]
            if n1[0] == -n2[0] or n1[1] == -n2[1]:
              corners += 0 # ...in a straight line = no corners
            else: # ...at a right angle...
              dx, dy = n1[0] + n2[0], n1[1] + n2[1]
              nx, ny = x + dx, y + dy
              if data[ny][nx] != data[y][x]:
                corners += 1 # ...with no neighbour on the inside = one corner
    q = nq
  return perimeter, plots, corners


with open("12.txt") as f:
  data = f.read().splitlines()
  seen = set()
  price = 0
  price_bulk = 0
  for y in range(len(data)):
    for x in range(len(data[0])):
      if (x, y) in seen:
        continue
      perimeter, plots, corners = expand(data, x, y)
      seen |= plots
      price += len(plots) * perimeter
      price_bulk += len(plots) * corners
  print(price, price_bulk)