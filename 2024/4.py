def search(grid, word, i, j, di, dj):
    rows = len(grid)
    cols = len(grid[0])

    index = 0
    while (
        0 <= i and i < rows 
        and 0 <= j and j < cols 
        and index < len(word)
        and grid[i][j] == word[index]
    ):
        i += di
        j += dj
        index += 1
    return index == len(word)

def findLetter(grid, letter):
    rows = len(grid)
    cols = len(grid[0])
    return [ (i, j) for i in range(rows) for j in range(cols) if grid[i][j] == letter ]

def silver(grid):
    word = "XMAS"
    q = findLetter(grid, "X")
    
    count = 0
    for i, j in q:
        count += sum([
            search(grid, word, i, j, di, dj)
            for di, dj in [
                (1, 0), (-1, 0), 
                (0, 1), (0, -1), 
                (1, 1), (-1, -1),
                (1, -1), (-1, 1)
            ]
        ])
    return count

def isLetter(grid, letter, i, j):
    rows = len(grid)
    cols = len(grid[0])
    return (
        0 <= i and i < rows
        and 0 <= j and j < cols
        and grid[i][j] == letter
    )

def leftDiag(grid, i, j):
    return (
        (isLetter(grid, "S", i - 1, j - 1) and isLetter(grid, "M", i + 1, j + 1))
        or 
        (isLetter(grid, "M", i - 1, j - 1) and isLetter(grid, "S", i + 1, j + 1))
    )

def rightDiag(grid, i, j):
    return (
        (isLetter(grid, "S", i - 1, j + 1) and isLetter(grid, "M", i + 1, j - 1))
        or 
        (isLetter(grid, "M", i - 1, j + 1) and isLetter(grid, "S", i + 1, j - 1))
    )

def gold(grid):
    q = findLetter(grid, "A")
    count = 0
    for i, j in q:
        if leftDiag(grid, i, j) and rightDiag(grid, i, j):
            count += 1
    return count

with open("4.txt") as f:
    grid = [ i.strip() for i in f.readlines() ]
    print(silver(grid))
    print(gold(grid))