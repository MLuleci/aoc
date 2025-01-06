import math
import heapq
import itertools

def p(g, v=set()):
    for y, r in enumerate(g):
        for x, c in enumerate(r):
            if (x, y) in v:
                print('O', end='')
            else:
                print(c, end='')
        print()

def find(g, i):
    for y, r in enumerate(g):
        for x, c in enumerate(r):
            if i == c:
                return (x, y)

def n4(g, x, y):
    n = []
    for d, (dx, dy) in enumerate([ (0, -1), (1, 0), (0, 1), (-1, 0) ]):
        xx, yy = x + dx, y + dy
        if 0 <= xx and xx < len(g[0]) and 0 <= yy and yy < len(g) and g[yy][xx] != '#':
            n.append((xx, yy, d))
    return n

class PQ:
    def __init__(self):
        self.heap = []
        self.index = {}
        self.counter = itertools.count()
    
    def add(self, item, priority=0):
        if item in self.index:
            self.remove(item)
        count = next(self.counter)
        entry = [priority, count, item]
        self.index[item] = entry
        heapq.heappush(self.heap, entry)

    def remove(self, item):
        entry = self.index.pop(item)
        entry[-1] = None # Mark as removed
    
    def pop(self):
        while self.heap:
            priority, count, item = heapq.heappop(self.heap)
            if item is not None:
                del self.index[item]
                return item
        raise KeyError('pop from an empty priority queue')

    def __len__(self):
        return len(self.index)
    
    def __bool__(self):
        return len(self.index) > 0

def reconstruct(prev, node):
    path = []
    while node in prev:
        path.append(node)
        node = prev[node]
    return path

def turns(a, b):
    return max(1, min(2, abs(a - b) % 3)) if a != b else 0

def search(g, s, e):
    x, y = s
    pq = PQ()
    pq.add((x, y, 1))
    dist = { (x, y, 1): 0 }
    prev = {}
    seen = set()
    paths = []

    while pq:
        x, y, d = pq.pop()
        u = (x, y, d)
        seen.add(u)

        if (x, y) == e:
            paths.append((reconstruct(prev, u), dist[u]))

        for nx, ny, nd in n4(g, x, y):
            n = (nx, ny, nd)
            if n in seen:
                continue
            alt = dist[u] + 1 + 1000 * turns(d, nd)
            if alt < dist.get(n, math.inf):
                pq.add((nx, ny, nd), alt)
                dist[n] = alt
                prev[n] = u

    return paths[0]

def strip_direction(path):
    return [ (x, y) for x, y, *_ in path ]

def bfs(g):
    x, y = find(g, 'S')
    pq = PQ()
    pq.add((x, y, 1))
    dist = { (x, y, 1): 0 }
    prev = {}
    seen = set()

    while pq:
        x, y, d = pq.pop()
        u = (x, y, d)
        seen.add(u)

        for nx, ny, nd in n4(g, x, y):
            n = (nx, ny, nd)
            if n in seen:
                continue
            alt = dist[u] + 1 + 1000 * turns(d, nd)
            if alt <= dist.get(n, math.inf):
                pq.add((nx, ny, nd), alt)
                dist[n] = alt
                if alt < dist.get(n, math.inf):
                    prev[n] = [u]
                else:
                    prev[n] = prev.get(n, []) + [u]
    
    end = find(g, 'E')
    ends = []
    min_dist = math.inf
    for x, y, d in seen:
        if (x, y) == end:
            min_dist = min(min_dist, dist[(x, y, d)])
            ends.append((x, y, d))
    ends = [ i for i in ends if dist[i] == min_dist ]

    paths = []
    for i in ends:
        q = [[i]]
        while q:
            path = q.pop()
            last = path[-1]
            if last not in prev:
                paths.append(path)
                continue

            parents = prev[last]

            for p in parents:
                q.append(path + [p])
    return paths

with open("16.txt") as f:
    g = [ list(i.strip()) for i in f.readlines() ]
    paths = bfs(g)
    v = set(itertools.chain(*[ strip_direction(i) for i in paths ]))
    print(len(v))
    # p(g, v)