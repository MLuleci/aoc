from itertools import groupby

def is_valid(update, rules):
  indices = { k: v for v, k in enumerate(update) }
  for first, index in indices.items():
    if first not in rules:
      continue # No rule regarding this page number (or it's the RHS in a rule)
    for second in rules[first]: # The page number(s) that should come after `first`
      if second not in indices:
        continue # Second page number is not in the update, rule doesn't apply
      if indices[second] < index:
        return False
  return True

def fix_update(update, rules):
  # Graph edges from a node to its children
  update = set(update)
  edges = { k: rules.get(k, set()).intersection(update) for k in update }

  # Find the (reverse) topological order of the graph
  order = []
  while edges:
    # Find a node with no incoming edges
    node = next(iter([ k for k, v in edges.items() if not v ]))
    order.append(node)
    del edges[node] # Remove `node`` (and its edges to children) from graph

    # Remove edges from `node` to its parents
    for v in edges.values():
      v.remove(node)
  return order[::-1]

with open("5.txt") as f:
  rules, updates = f.read().split("\n\n")

  # Parse rules:
  # Construct a dictionary that maps a page number to
  # all the page numbers that should come after it (as a set)
  rules = sorted([ rule.split("|") for rule in rules.split("\n") ], key=lambda x: x[0])
  rules = { k: set(map(lambda x: x[1], g)) for k, g in groupby(rules, lambda x: x[0]) }

  # Parse updates:
  updates = [ update.split(",") for update in updates.split("\n") ]

  # Silver:
  valid_updates = [ update for update in updates if is_valid(update, rules) ]
  middle_pages = [ int(i[len(i) // 2]) for i in valid_updates ]
  print(sum(middle_pages))

  # Gold:
  invalid_updates = [ update for update in updates if not is_valid(update, rules) ]
  fixed_updates = [ fix_update(update, rules) for update in invalid_updates ]
  middle_pages = [ int(i[len(i) // 2]) for i in fixed_updates ]
  print(sum(middle_pages))