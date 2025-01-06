from functools import cmp_to_key

cards = {
    'A': 12,
    'K': 11,
    'Q': 10,
    'J': -1,  # 7-2
    'T': 8,
    '9': 7,
    '8': 6,
    '7': 5,
    '6': 4,
    '5': 3,
    '4': 2,
    '3': 1,
    '2': 0
}

def strength(x):
    return cards[x]
 
def typeof(x):
    def fn(y):
        d = {}
        for i in y:
            d[i] = d.setdefault(i, 0) + 1
        n = len(d)
        m = max(d.values())
        return {
            1: 6,
            2: m + 1,
            3: m,
            4: 1,
            5: 0
        }[n]
    return max([fn(x.replace('J', t)) for t in cards])  # 7-2
 
def compare(a, b):
    a, b = a[0], b[0]
    dt = typeof(a) - typeof(b)
    if dt != 0:
        return dt
    else:
        for x, y in zip(a, b):
            ds = strength(x) - strength(y)
            if ds != 0:
                return ds
    return 0

if __name__ == '__main__':
    with open('7.txt') as f:
        pairs = [i.split() for i in f.readlines()]
        pairs = [(i[0], int(i[1])) for i in pairs]
        print(
            sum([(i + 1) * p[1] for i, p in enumerate(sorted(pairs, key=cmp_to_key(compare)))]))