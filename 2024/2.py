def is_safe(report, tolerate=False):
  if not tolerate:
    prev = report[0]
    last_diff = report[1] - prev
    for i in range(1, len(report)):
      diff = report[i] - prev
      if sign(diff) != sign(last_diff) or abs(diff) < 1 or abs(diff) > 3:
        return False
      prev = report[i]
      last_diff = diff
    return True
  else:
    return any([ is_safe(report[:i] + report[i + 1:]) for i in range(len(report)) ])

def sign(i):
  if i > 0:
    return 1
  elif i < 0:
    return -1
  else:
    return 0

with open("2.txt") as f:
  num_safe_0 = 0
  num_safe_1 = 0

  for line in f.readlines():
    report = [ int(i) for i in line.strip().split(" ") ]
    if is_safe(report):
      num_safe_0 += 1

    if is_safe(report, True):
      num_safe_1 += 1

  print(num_safe_0)
  print(num_safe_1)
