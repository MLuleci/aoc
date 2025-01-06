delta = {
    '|': [( 0, 1), ( 0, -1)],
    '-': [( 1, 0), (-1,  0)],
    'L': [( 1, 0), ( 0, -1)],
    'J': [(-1, 0), ( 0, -1)],
    '7': [(-1, 0), ( 0,  1)],
    'F': [( 1, 0), ( 0,  1)]
}

def edges(grid, x, y):
    h = len(grid)
    w = len(grid[0])
    ch = grid[y][x]
    if ch not in delta:
        return []
    e = []
    for dx, dy in delta[ch]:
        xx = x + dx
        yy = y + dy
        if xx < 0 or xx >= w or yy < 0 or yy >= h:
            continue
        e.append((xx, yy))
    return e

def inside(group, row, index):
    # - = 0
    # | or L7 or FJ = 1
    # LJ or F7 = 2
    count = 0
    i = 0
    while i < len(group):
        x = group[i]
        if x > index:
            break
        ch = row[x]
        if ch == '|':
            count += 1
        if ch == 'L' or ch == 'F':
            j = i + 1
            while row[group[j]] == '-':
                j += 1
            end = row[group[j]]
            i = j
            if (ch == 'L' and end == '7') or (ch == 'F' and end == 'J'):
                count += 1
            else:
                count += 2
        i += 1
    return count % 2 != 0

if __name__ == '__main__':
    with open('10.txt') as f:
        grid = [ list(i[:-1]) for i in f.readlines() ]
        
        start = None
        for y, row in enumerate(grid):
            if 'S' in row:
                x = row.index('S')
                start = (x, y)
                conn = [
                    start in edges(grid, xx, yy) 
                    for xx, yy in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
                ]
                if conn[0] and conn[1]:
                    ch = '-'
                if conn[0] and conn[2]:
                    ch = 'J'
                if conn[0] and conn[3]:
                    ch = '7'
                if conn[1] and conn[2]:
                    ch = 'L'
                if conn[1] and conn[3]:
                    ch = 'F'
                if conn[2] and conn[3]:
                    ch = '|'
                grid[y][x] = ch
                break

        q = [start]
        s = set([ start ])
        while q:
            x, y = q.pop(0)
            e = edges(grid, x, y)
            q.extend([ i for i in e if i not in s ])
            s.update(e)
        print(len(s) // 2) # 10-1

        groups = {}
        for x, y in s:
            if y in groups:
                groups[y].append(x)
            else:
                groups[y] = [x]
        for i in groups.values():
            i.sort()
        
        count = 0
        for y, row in enumerate(grid):
            if y not in groups:
                continue
            group = groups[y]
            startx = group[0]
            endx = group[-1]
            for x in range(startx + 1, endx):
                if x in group:
                    continue
                if inside(group, row, x):
                    count += 1
        print(count) # 10-2