from itertools import takewhile

def stoi(s):
  # return sum([ (1 if c == '#' else 0) << i for i, c in enumerate(s[::-1])])
  return int(s.replace('#', '1').replace('.', '0'), 2)

def transpose(a):
  return [ "".join(i) for i in zip(*a) ]

def bit_count(n):
  count = 0
  while n:
    count += n & 1
    n >>= 1
  return count

def find_reflection(pattern, diff):
  # 1. Iterate over each position, taking it as the center
  # 2. Consider a palindrome of width [0, i] on both sides
  # 3. XOR pairs and sum bit counts to test if palindrome is valid
  # 4. Shrink the width past the middle point
  for i in range(1, len(pattern)):
    width = min(i, len(pattern) - i)
    left = pattern[i-width:i]
    right = pattern[i:i+width]
    if sum(bit_count(a ^ b) for a, b in zip(left, right[::-1])) == diff:
      return i
  return 0

with open("13.txt") as f:
  lines = [ i.strip() for i in f.readlines() ]
  diff = 1
  total = 0
  index = 0
  while index < len(lines):
    # 1. Collect non-empty rows
    pattern = list(takewhile(lambda x: x, lines[index:]))

    # 2. Convert each row into a number (# = 1, . = 0)
    rows = list(map(stoi, pattern))
    cols = list(map(stoi, transpose(pattern)))

    # 3. Find the pattern & score
    score = find_reflection(cols, diff) + 100 * find_reflection(rows, diff)

    total += score
    index += len(rows) + 1

  print(total)
