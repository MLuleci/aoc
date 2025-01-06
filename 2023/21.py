from Grid import Grid

with open("2023_21.txt") as f:
    grid = Grid(f)
    start = grid.find('S')
    
    q = [start]
    steps = 64
    while steps > 0:
        nq = set()
        for x, y in q:
            n4 = [ 
                (xx, yy) 
                for xx, yy, value in grid.n4(x, y)
                if value != '#' and (xx, yy) not in nq
            ]
            nq.update(n4)
        q = nq
        steps -= 1
    print(len(q))