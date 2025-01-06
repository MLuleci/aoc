def in_bounds(x, y, rows, cols):
    return 0 <= x and x < cols and 0 <= y and y < rows

def solve(grid, antennae, gold=False):
    rows = len(grid)
    cols = len(grid[0])
    antinodes = set()

    for positions in antennae.values():
        for i in range(len(positions)):
            x1, y1 = positions[i]
            if gold:
                antinodes.add((x1, y1))
            for j in range(i + 1, len(positions)):
                x2, y2 = positions[j]
                dx = x1 - x2
                dy = y1 - y2

                a1 = x1 + dx
                b1 = y1 + dy
                while in_bounds(a1, b1, rows, cols):
                    antinodes.add((a1, b1))
                    if gold:
                        a1 += dx
                        b1 += dy
                    else:
                        break
                
                a2 = x2 - dx
                b2 = y2 - dy
                while in_bounds(a2, b2, rows, cols):
                    antinodes.add((a2, b2))
                    if gold:
                        a2 -= dx
                        b2 -= dy
                    else:
                        break
    return len(antinodes)

with open("8.txt") as f:
    grid = [ list(row.strip()) for row in f.readlines() ]

    antennae = {}
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == ".":
                continue
            if cell not in antennae:
                antennae[cell] = []
            antennae[cell].append((x, y))
    print(solve(grid, antennae, False))
    print(solve(grid, antennae, True))