def shift_left(arr):
  put = 0
  count = 0
  for i, ch in enumerate(arr):
    if ch == '.':
      continue
    if ch == '#':
      for _ in range(count):
        arr[put] = 'O'
        put += 1
      count = 0
      put = i + 1
    if ch == 'O':
      arr[i] = '.'
      count += 1

  for _ in range(count):
    arr[put] = 'O'
    put += 1

  return arr

def compute_load(grid):
  return sum([ row.count('O') * (len(grid) - i) for i, row in enumerate(grid) ])

def transpose(arr):
  return [ list(i) for i in zip(*arr) ]

def shift_north(grid):
  return transpose([ shift_left(i) for i in transpose(grid) ])

def shift_south(grid):
  return transpose([ shift_left(i[::-1])[::-1] for i in transpose(grid) ])

def shift_east(grid):
  return [ shift_left(i[::-1])[::-1] for i in grid ]

def shift_west(grid):
  return [ shift_left(i) for i in grid ]

def spin(grid):
  n = shift_north(grid)
  w = shift_west(n)
  s = shift_south(w)
  e = shift_east(s)
  return e

def hash_grid(grid):
  return ''.join([ ''.join(i) for i in grid ])

def print_grid(grid):
  for i in grid:
    print(''.join(i))
  print()

with open("14.txt") as f:
  grid = [ list(i.strip()) for i in f.readlines() ]

  # Part 1:
  print(compute_load(shift_north(grid)))

  # Part 2:
  memo = []
  loads = []
  i = 0
  while i < 1000000000:
    grid = spin(grid)
    hash = hash_grid(grid)

    if hash in memo:
      start = memo.index(hash)
      length = i - start
      i = start + (1000000000 - start) % length
      break

    memo.append(hash)
    loads.append(compute_load(grid))
    i += 1

  print(loads[i])
