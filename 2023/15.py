def hash(s):
  h = 0
  for c in s:
    h = ((h + ord(c)) * 17) % 256
  return h

class Box:
  def __init__(self, number):
    self.number = number
    self.lenses = {}
    self.labels = []

  def add(self, label, lens):
    if label not in self.lenses:
      self.labels.append(label)
    self.lenses[label] = lens
  
  def remove(self, label):
    if label in self.lenses:
      self.labels.remove(label)
      del self.lenses[label]

  def get_power(self):
    return sum([ (self.number + 1) * (i + 1) * self.lenses[l] for i, l in enumerate(self.lenses) ])

with open('15.txt') as f:
  line = f.readline().strip()
  sequence = line.split(",")

  print(sum(hash(s) for s in sequence))

  boxes = []
  for i in range(256):
    boxes.append(Box(i))
  
  for s in sequence:
    if s[-1] != '-':
      label, lens = s.split('=')
      index = hash(label)
      box = boxes[index]
      box.add(label, int(lens))
    else:
      label = s[:-1]
      index = hash(label)
      box = boxes[index]
      box.remove(label)
  
  print(sum(box.get_power() for box in boxes))