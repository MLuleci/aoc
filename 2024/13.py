import re

def det(X):
    return X[0][0] * X[1][1] - X[0][1] * X[1][0]

def inv(X):
    d = det(X)
    return [
        [ X[1][1] / d, -X[0][1] / d ],
        [ -X[1][0] / d, X[0][0] / d ]
    ]

def mul(X, v):
    return [
        X[0][0] * v[0] + X[0][1] * v[1],
        X[1][0] * v[0] + X[1][1] * v[1]
    ]

def close(a, b, e=1e-5):
    for x, y in zip(a, b):
        if abs(x - y) > e:
            return False
    return True

with open("13.txt") as f:
    parts = f.read().split("\n\n")
    equations = []
    for c in [0, 10000000000000]:
        total = 0
        for part in parts:
            lines = part.splitlines()
            button_pattern = r"Button .: X\+(\d+), Y\+(\d+)"
            prize_pattern = r"Prize: X=(\d+), Y=(\d+)"
            a = re.match(button_pattern, lines[0])
            b = re.match(button_pattern, lines[1])
            p = re.match(prize_pattern, lines[2])

            ax, bx = int(a.group(1)), int(b.group(1))
            ay, by = int(a.group(2)), int(b.group(2))
            cx, cy = int(p.group(1)) + c, int(p.group(2)) + c
            
            # Remember:
            # Ax=b so x=A^-1b
            # where A = [ [ a b ], [ c d ] ]
            # A-1 = 1/det(A) * adj(A)
            # det(A) = ax * by - ay * bx
            # adj(A) = [ [ d -b ], [ -c a ] ]
            # thus [ t1 t2 ] = A^-1 [ cx cy ]
            t1 = int((cx * by - cy * bx) / (by * ax - bx * ay))
            t2 = int((cx * ay - cy * ax) / (ay * bx - by * ax))
            if ax * t1 + bx * t2 == cx and ay * t1 + by * t2 == cy:
                total += int(t1) * 3 + int(t2)
            
            A = [ [ ax, bx ], [ ay, by ] ]
            b = [ cx, cy ]
            Ai = inv(A)
            a = [ int(round(i)) for i in mul(Ai, b) ]
            bn = mul(A, a)
            if close(b, bn):
                pass # Same as above!
                
        print(total)
