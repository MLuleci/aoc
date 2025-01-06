import math

def blink_iter(stones):
  result = []
  for stone in stones:
    if stone == 0:
      result.append(1)
    elif math.floor(math.log10(stone)) % 2 == 1:
      digits = str(stone)
      length = len(digits) // 2
      result.extend([ int(digits[:length]), int(digits[length:]) ])
    else:
      result.append(stone * 2024)
  return result

def blink_grouped(stones):
  result = {}
  for number, count in stones.items():
    if number == 0:
      result[1] = result.get(1, 0) + count
    elif math.floor(math.log10(number)) % 2 == 1:
      digits = str(number)
      length = len(digits) // 2
      left = int(digits[:length])
      right = int(digits[length:])
      result[left] = result.get(left, 0) + count
      result[right] = result.get(right, 0) + count
    else:
      index = number * 2024
      result[index] = result.get(index, 0) + count
  return result

with open("11.txt") as f:
  stones = [ int(i) for i in f.readline().split() ]
  stones_iter = stones[:]
  for _ in range(25):
    stones_iter = blink_iter(stones_iter)
  print(len(stones_iter))

  stones_grouped = { i: stones.count(i) for i in set(stones) }
  for _ in range(75):
    stones_grouped = blink_grouped(stones_grouped)
  print(sum(stones_grouped.values()))