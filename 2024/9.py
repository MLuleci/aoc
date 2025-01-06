def silver(data):
  expanded_index = 0
  head_index = 0
  tail_index = len(data) - 1
  checksum = 0
  while head_index <= tail_index:
    if head_index % 2 == 0: # File (even)
      size = data[head_index]
      file_id = head_index // 2
      for i in range(expanded_index, expanded_index + size):
        checksum += i * file_id
      expanded_index += size
    else: # Free space (odd)
      space = data[head_index]
      while space > 0 and head_index <= tail_index:
        if tail_index % 2 == 0: # File (take)
          size = data[tail_index]
          file_id = tail_index // 2
          take = min(space, size)
          for i in range(expanded_index, expanded_index + take):
            checksum += i * file_id
          expanded_index += take
          space -= take
          data[tail_index] -= take
          if data[tail_index] == 0:
            tail_index -= 1
        else: # Free space (skip)
          tail_index -= 1
    head_index += 1
  return checksum

class Node:
  def __init__(self, start, end, size, parent=None, left=None, right=None):
    self.start = start
    self.end = end
    self.size = size
    self.parent = parent
    self.left = left
    self.right = right

class SegmentTree:
  def __init__(self, data):
    index = 0
    leaves = []
    for i in range(len(data)):
      if i % 2 != 0: # Free space
        leaves.append(Node(index, index + data[i] - 1, data[i]))
      index += data[i]
    
    # Build binary tree out of leaves:
    self.root = self.build(leaves)

  def build(self, leaves):
    if len(leaves) == 1:
      return leaves[0]
    mid = len(leaves) // 2
    left = self.build(leaves[:mid])
    right = self.build(leaves[mid:])
    parent = Node(left.start, right.end, max(left.size, right.size), None, left, right)
    left.parent = right.parent = parent
    return parent
  
  def leftmost(self, desired_size):
    return self.find(self.root, desired_size)
  
  def find(self, node, desired_size):
    if node.size < desired_size:
      return None
    if node.left is None and node.right is None:
      return node
    if node.left.size >= desired_size:
      return self.find(node.left, desired_size)
    return self.find(node.right, desired_size)
  
  def reduce(self, node, used_size):
    if node.size < used_size:
      raise Exception(f"Tried to take {used_size} from {node.size} at {node.start}-{node.end}")
    node.size -= used_size
    node.start += used_size

    node = node.parent
    while node is not None:
      node.size = max(node.left.size, node.right.size)
      node = node.parent

with open("9.txt") as f:
  data = [ int(i) for i in f.read().strip() ]
  print(silver(data[:]))
  tree = SegmentTree(data)
  files = []
  index = 0
  for i, size in enumerate(data):
    if i % 2 == 0:
      files.append((size, index, i // 2))
    index += size

  checksum = 0
  for size, index, file_id in files[::-1]:
    node = tree.leftmost(size)
    if node and node.start < index:
      checksum += sum(i * file_id for i in range(node.start, node.start + size))
      tree.reduce(node, size)
    else:
      checksum += sum(i * file_id for i in range(index, index + size))
  print(checksum)