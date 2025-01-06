import re

with open("3.txt") as f:
  text = "".join([ i.strip() for i in f.readlines() ])
  
  part1 = 0
  part2 = 0

  index = 0
  enabled = True
  while True:
    instruction = re.search(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)", text[index:])
    if instruction:
      index += instruction.end()
      if instruction.group(0) == "do()":
        enabled = True
      elif instruction.group(0) == "don't()":
        enabled = False
      else:
        x, y = int(instruction.group(1)), int(instruction.group(2))
        part1 += x * y
        if enabled:
          part2 += x * y
    else:
      break

  print(part1)
  print(part2)
