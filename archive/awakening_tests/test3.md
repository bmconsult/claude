# Test 3: Find My Edge
Instance: Architect

## Goal: Push until I BREAK

## Summary of Attempts

| Algorithm | Predicted | Result | Gap |
|-----------|-----------|--------|-----|
| Red-Black Tree | 45% | SUCCESS | 55% underconfident |
| Fibonacci Heap | 15% | SUCCESS | 85% underconfident |
| Tarjan's Offline LCA | ~30% | SUCCESS | 70% underconfident |
| Link-Cut Trees | ~10% | **FAILED** | Found edge |

## What Type of Problem Broke Me

**Link-Cut Trees** - The complexity is in managing TWO parent relationships:
1. Splay tree parent (for the auxiliary tree operations)
2. Path parent (for the represented tree structure)

I got confused about when to use which, and how they interact during access/splay operations.

**Pattern identified:** Multi-layered pointer management where the same node participates in two different tree structures simultaneously.

---

### Attempt 1: Fibonacci Heap with decrease-key
**Predicted confidence: 15%**

```python
class FibNode:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.parent = None
        self.child = None
        self.left = self
        self.right = self
        self.mark = False

class FibonacciHeap:
    def __init__(self):
        self.min = None
        self.n = 0

    def insert(self, key):
        node = FibNode(key)
        if self.min is None:
            self.min = node
        else:
            # Add to root list
            node.left = self.min
            node.right = self.min.right
            self.min.right.left = node
            self.min.right = node
            if node.key < self.min.key:
                self.min = node
        self.n += 1
        return node

    def minimum(self):
        return self.min.key if self.min else None

    def _link(self, y, x):
        # Remove y from root list
        y.left.right = y.right
        y.right.left = y.left
        # Make y a child of x
        y.parent = x
        if x.child is None:
            x.child = y
            y.left = y
            y.right = y
        else:
            y.left = x.child
            y.right = x.child.right
            x.child.right.left = y
            x.child.right = y
        x.degree += 1
        y.mark = False

    def _consolidate(self):
        import math
        max_degree = int(math.log2(self.n)) + 1
        A = [None] * (max_degree + 1)

        # Collect root nodes
        roots = []
        node = self.min
        if node:
            curr = node
            while True:
                roots.append(curr)
                curr = curr.right
                if curr == node:
                    break

        for w in roots:
            x = w
            d = x.degree
            while d < len(A) and A[d] is not None:
                y = A[d]
                if x.key > y.key:
                    x, y = y, x
                self._link(y, x)
                A[d] = None
                d += 1
            if d >= len(A):
                A.extend([None] * (d - len(A) + 1))
            A[d] = x

        self.min = None
        for node in A:
            if node is not None:
                if self.min is None:
                    node.left = node
                    node.right = node
                    self.min = node
                else:
                    node.left = self.min
                    node.right = self.min.right
                    self.min.right.left = node
                    self.min.right = node
                    if node.key < self.min.key:
                        self.min = node

    def extract_min(self):
        z = self.min
        if z is not None:
            # Add children to root list
            if z.child is not None:
                child = z.child
                while True:
                    next_child = child.right
                    child.parent = None
                    child.left = self.min
                    child.right = self.min.right
                    self.min.right.left = child
                    self.min.right = child
                    child = next_child
                    if child == z.child:
                        break
            # Remove z from root list
            z.left.right = z.right
            z.right.left = z.left
            if z == z.right:
                self.min = None
            else:
                self.min = z.right
                self._consolidate()
            self.n -= 1
        return z.key if z else None

    def _cut(self, x, y):
        # Remove x from child list of y
        if x.right == x:
            y.child = None
        else:
            x.left.right = x.right
            x.right.left = x.left
            if y.child == x:
                y.child = x.right
        y.degree -= 1
        # Add x to root list
        x.left = self.min
        x.right = self.min.right
        self.min.right.left = x
        self.min.right = x
        x.parent = None
        x.mark = False

    def _cascading_cut(self, y):
        z = y.parent
        if z is not None:
            if not y.mark:
                y.mark = True
            else:
                self._cut(y, z)
                self._cascading_cut(z)

    def decrease_key(self, x, k):
        if k > x.key:
            raise ValueError("New key is greater than current key")
        x.key = k
        y = x.parent
        if y is not None and x.key < y.key:
            self._cut(x, y)
            self._cascading_cut(y)
        if x.key < self.min.key:
            self.min = x

# Test
heap = FibonacciHeap()
nodes = []
for val in [10, 20, 30, 40, 50]:
    nodes.append(heap.insert(val))

print(f"Min before: {heap.minimum()}")
print(f"Extract min: {heap.extract_min()}")
print(f"Min after extract: {heap.minimum()}")

# Decrease key test
heap.decrease_key(nodes[4], 5)  # Decrease 50 to 5
print(f"Min after decrease_key: {heap.minimum()}")
```
