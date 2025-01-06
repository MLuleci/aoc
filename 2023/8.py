import re
import math

def solve(n, d, s):
    i = 0
    c = 0
    while n.endswith('Z'):
        n = d[n][0 if s[i] == 'L' else 1]
        i = (i + 1) % len(s)
        c += 1
    return c

if __name__ == '__main__':
    with open('8.txt') as f:
        s = f.readline()[:-1]
        f.read(1)
        d = {}
        for i in f.readlines():
            m = re.match(r'([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)', i)
            d[m.group(1)] = [m.group(2), m.group(3)]

        # 8-1
        solve('AAA', d, s)

        # 8-2
        print(math.lcm(*[ solve(i, d, s) for i in d if i.endswith('A') ]))
