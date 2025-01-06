import re

with open("1.txt") as f:
    l = []
    r = []
    for i in f.readlines():
        n = re.split(r'\s+', i)
        l.append(int(n[0]))
        r.append(int(n[1]))
    l.sort()
    r.sort()
    print(sum([ abs(x - y) for x, y in zip(l, r) ]))

    s = { i: r.count(i) for i in r }
    print(sum([ i * s.get(i, 0) for i in l ]))