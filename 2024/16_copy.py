import math
import sys

sys.setrecursionlimit(int(1e9))

g = list(map(list, open('16.txt').read().split('\n'))); g.pop()
rows, cols = len(g), len(g[0])
cache = [[math.inf] * cols for _ in range(rows)]

m = {}
def dfs(pos, d, cost):
    if pos == (1, cols - 2):
        return cost
    (r, c) = pos
    cache[r][c] = min(cache[r][c], cost)
    dx = ((-1, 0), (0, +1), (+1, 0), (0, -1))
    minimum = math.inf

    # continue
    (dr, dc) = dx[d]
    (rr, cc) = (r + dr, c + dc)
    if g[rr][cc] in '.E' and cache[rr][cc] > cost - 1e3:
        minimum = min(minimum, dfs((rr, cc), d, cost + 1))
    
    # turn left and continue
    (dr, dc) = dx[tmp := d-1 & 3]
    (rr, cc) = (r + dr, c + dc)
    if g[rr][cc] in '.E' and cache[rr][cc] > cost:
        minimum = min(minimum, dfs((rr, cc), tmp, cost + 1001))
    
    # turn right and continue
    (dr, dc) = dx[tmp := d+1 & 3]
    (rr, cc) = (r + dr, c + dc)
    if g[rr][cc] in '.E' and cache[rr][cc] > cost:
        minimum = min(minimum, dfs((rr, cc), tmp, cost + 1001))
        
    if minimum not in m:
        m[minimum] = set()
    m[minimum].add((r, c))
    return minimum

p2 = len(m[p1 := dfs((rows - 2, 1), 1, 0)]) + 1
print(p1, p2)