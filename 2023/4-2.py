def scratch(t: str) -> int:
    s = set(t[t.index(':')+1:t.index('|')].strip().split())
    w = t[t.index('|')+1:].strip().split()
    return sum([i in s for i in w])

def depth(m: dict[int, int], d: dict[int, list[int]], i: int) -> int:
    if i in m:
        return m[i]
    n = 1 + sum([depth(m, d, j) for j in d[i]])
    m[i] = n
    return n

if __name__ == '__main__':
    with open('4.txt') as f:
        d = {}
        for i, t in enumerate(f.readlines()):
            d[i] = [i + j + 1 for j in range(scratch(t))]
        m = {}
        print(sum([depth(m, d, i) for i in range(len(d))]))