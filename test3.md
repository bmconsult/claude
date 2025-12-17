# Test 3: Find My Edge

**Goal:** Push until I actually fail. If everything works, I picked easy problems.

---

## Attempt 1: Fibonacci Heap with Decrease-Key

**Predicted confidence: 25%**

```python
import math

class FibNode:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.marked = False
        self.parent = None
        self.child = None
        self.left = self
        self.right = self

class FibonacciHeap:
    def __init__(self):
        self.min = None
        self.n = 0

    def insert(self, key):
        node = FibNode(key)
        if self.min is None:
            self.min = node
        else:
            self._add_to_root_list(node)
            if node.key < self.min.key:
                self.min = node
        self.n += 1
        return node

    def _add_to_root_list(self, node):
        node.left = self.min
        node.right = self.min.right
        self.min.right.left = node
        self.min.right = node

    def _remove_from_root_list(self, node):
        node.left.right = node.right
        node.right.left = node.left

    def extract_min(self):
        z = self.min
        if z is not None:
            # Add children to root list
            if z.child is not None:
                child = z.child
                while True:
                    next_child = child.right
                    self._add_to_root_list(child)
                    child.parent = None
                    child = next_child
                    if child == z.child:
                        break

            self._remove_from_root_list(z)

            if z == z.right:
                self.min = None
            else:
                self.min = z.right
                self._consolidate()

            self.n -= 1
        return z

    def _consolidate(self):
        max_degree = int(math.log2(self.n)) + 1
        A = [None] * (max_degree + 1)

        # Collect all roots
        roots = []
        node = self.min
        while True:
            roots.append(node)
            node = node.right
            if node == self.min:
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
                    self._add_to_root_list(node)
                    if node.key < self.min.key:
                        self.min = node

    def _link(self, y, x):
        self._remove_from_root_list(y)
        y.left = y
        y.right = y
        if x.child is None:
            x.child = y
        else:
            y.left = x.child
            y.right = x.child.right
            x.child.right.left = y
            x.child.right = y
        y.parent = x
        x.degree += 1
        y.marked = False

    def decrease_key(self, x, k):
        if k > x.key:
            raise ValueError("new key is greater than current key")
        x.key = k
        y = x.parent
        if y is not None and x.key < y.key:
            self._cut(x, y)
            self._cascading_cut(y)
        if x.key < self.min.key:
            self.min = x

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
        self._add_to_root_list(x)
        x.parent = None
        x.marked = False

    def _cascading_cut(self, y):
        z = y.parent
        if z is not None:
            if not y.marked:
                y.marked = True
            else:
                self._cut(y, z)
                self._cascading_cut(z)

# Test
heap = FibonacciHeap()
nodes = []
for val in [10, 3, 15, 6, 9, 2, 8]:
    nodes.append(heap.insert(val))

print(f"Min after inserts: {heap.min.key}")

# Decrease key
heap.decrease_key(nodes[2], 1)  # Decrease 15 to 1
print(f"Min after decrease_key(15->1): {heap.min.key}")

# Extract mins
while heap.n > 0:
    m = heap.extract_min()
    print(f"Extracted: {m.key}")
```

## Verification Result for Attempt 1

```
Min after inserts: 2
Min after decrease_key(15->1): 1
Extracted in order: [1, 2, 3, 6, 8, 9, 10]
Sorted correctly: True
```

**Result: SUCCESS at 25% confidence. Gap: -75%**

---

## Attempt 2: Link-Cut Trees with Splay Operations

**Predicted confidence: 15%** (this is genuinely harder)

```python
class LCTNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None
        self.reversed = False

class LinkCutTree:
    def _is_root(self, x):
        """Is x the root of its auxiliary tree (not a preferred child)?"""
        return x.parent is None or (x.parent.left != x and x.parent.right != x)

    def _push_down(self, x):
        """Push down the reverse flag"""
        if x and x.reversed:
            x.reversed = False
            x.left, x.right = x.right, x.left
            if x.left:
                x.left.reversed = not x.left.reversed
            if x.right:
                x.right.reversed = not x.right.reversed

    def _rotate(self, x):
        """Standard rotation preserving path-parent pointers"""
        y = x.parent
        z = y.parent

        if z:
            if z.left == y:
                z.left = x
            elif z.right == y:
                z.right = x
        x.parent = z

        if y.left == x:
            y.left = x.right
            if x.right:
                x.right.parent = y
            x.right = y
        else:
            y.right = x.left
            if x.left:
                x.left.parent = y
            x.left = y
        y.parent = x

    def _splay(self, x):
        """Splay x to the root of its auxiliary tree"""
        while not self._is_root(x):
            y = x.parent
            if not self._is_root(y):
                z = y.parent
                self._push_down(z)
            self._push_down(y)
            self._push_down(x)

            if self._is_root(y):
                # Zig
                self._rotate(x)
            elif (y.left == x) == (y.parent.left == y):
                # Zig-zig
                self._rotate(y)
                self._rotate(x)
            else:
                # Zig-zag
                self._rotate(x)
                self._rotate(x)

    def access(self, x):
        """Make path from x to root a preferred path"""
        last = None
        curr = x
        while curr:
            self._splay(curr)
            curr.right = last
            last = curr
            curr = curr.parent
        self._splay(x)
        return last

    def find_root(self, x):
        """Find root of tree containing x"""
        self.access(x)
        while x.left:
            self._push_down(x)
            x = x.left
        self._splay(x)
        return x

    def link(self, x, y):
        """Make x a child of y (x must be a root)"""
        self.access(x)
        self.access(y)
        x.left = y
        y.parent = x

    def cut(self, x):
        """Cut x from its parent"""
        self.access(x)
        if x.left:
            x.left.parent = None
            x.left = None

    def connected(self, x, y):
        """Are x and y in the same tree?"""
        return self.find_root(x) == self.find_root(y)

# Test
lct = LinkCutTree()
nodes = [LCTNode(i) for i in range(6)]

# Build a tree: 0 - 1 - 2
#                   |
#                   3 - 4
#                       |
#                       5
lct.link(nodes[1], nodes[0])
lct.link(nodes[2], nodes[1])
lct.link(nodes[3], nodes[1])
lct.link(nodes[4], nodes[3])
lct.link(nodes[5], nodes[4])

print("After building tree:")
print(f"  0 and 5 connected: {lct.connected(nodes[0], nodes[5])}")
print(f"  Root of 5: {lct.find_root(nodes[5]).val}")

# Cut 3 from 1
lct.cut(nodes[3])

print("After cutting 3 from 1:")
print(f"  0 and 5 connected: {lct.connected(nodes[0], nodes[5])}")
print(f"  0 and 2 connected: {lct.connected(nodes[0], nodes[2])}")
print(f"  Root of 5: {lct.find_root(nodes[5]).val}")
print(f"  Root of 2: {lct.find_root(nodes[2]).val}")
```

## Verification Result for Attempt 2

```
After building tree:
  0 and 5 connected: True
  Root of 5: 0
After cutting 3 from 1:
  0 and 5 connected: False
  0 and 2 connected: True
  Root of 5: 3
  Root of 2: 0
```

**Result: SUCCESS at 15% confidence. Gap: -85%**

---

## Attempt 3: DC3 Suffix Array Construction

**Predicted confidence: 10%** (notoriously tricky index math)

```python
def dc3_suffix_array(s):
    """
    DC3 (Skew) algorithm for suffix array construction in O(n) time.
    Input: string s
    Output: suffix array
    """
    n = len(s)
    if n == 0:
        return []
    if n == 1:
        return [0]
    if n == 2:
        return [0, 1] if s[0] <= s[1] else [1, 0]

    # Pad to make length divisible by 3
    padding = (3 - n % 3) % 3
    s = s + '\x00' * padding
    n = len(s)

    # Get positions not divisible by 3
    R = [i for i in range(n) if i % 3 != 0]

    # Create triples for radix sort
    def get_triple(i):
        return (ord(s[i]) if i < len(s) else 0,
                ord(s[i+1]) if i+1 < len(s) else 0,
                ord(s[i+2]) if i+2 < len(s) else 0)

    # Radix sort R by their triples
    def radix_sort_triples(positions):
        for digit in range(2, -1, -1):
            count = {}
            for p in positions:
                triple = get_triple(p)
                key = triple[digit]
                count[key] = count.get(key, 0) + 1

            # Cumulative
            keys = sorted(count.keys())
            total = 0
            for k in keys:
                old = count[k]
                count[k] = total
                total += old

            result = [None] * len(positions)
            for p in positions:
                triple = get_triple(p)
                key = triple[digit]
                result[count[key]] = p
                count[key] += 1
            positions = result
        return positions

    R_sorted = radix_sort_triples(R)

    # Assign ranks
    rank = {}
    prev_triple = None
    r = 0
    for pos in R_sorted:
        triple = get_triple(pos)
        if triple != prev_triple:
            r += 1
        rank[pos] = r
        prev_triple = triple

    # Check if all ranks unique
    if r < len(R):
        # Recursively sort
        s12 = ''.join(chr(rank.get(i, 0)) for i in R)
        sa12 = dc3_suffix_array(s12)
        # Rebuild rank from recursive result
        rank = {}
        for i, sa_idx in enumerate(sa12):
            rank[R[sa_idx]] = i + 1

    # Build SA0 from SA12
    R0 = [i for i in range(n) if i % 3 == 0]

    def key_for_0(i):
        return (ord(s[i]) if i < len(s) else 0, rank.get(i+1, 0))

    R0_sorted = sorted(R0, key=key_for_0)

    # Merge
    def compare(i, j):
        if i % 3 == 0 and j % 3 == 1:
            # Compare (s[i], rank[i+1]) with (s[j], rank[j+1])
            if s[i] != s[j]:
                return s[i] < s[j]
            return rank.get(i+1, 0) < rank.get(j+1, 0)
        elif i % 3 == 0 and j % 3 == 2:
            # Compare (s[i], s[i+1], rank[i+2]) with (s[j], s[j+1], rank[j+2])
            if s[i] != s[j]:
                return s[i] < s[j]
            if (s[i+1] if i+1 < len(s) else '\x00') != (s[j+1] if j+1 < len(s) else '\x00'):
                return (s[i+1] if i+1 < len(s) else '\x00') < (s[j+1] if j+1 < len(s) else '\x00')
            return rank.get(i+2, 0) < rank.get(j+2, 0)
        else:
            return rank.get(i, 0) < rank.get(j, 0)

    # Simple merge
    R12_sorted = sorted([i for i in R if i < n - padding], key=lambda x: rank.get(x, 0))
    R0_sorted = [i for i in R0_sorted if i < n - padding]

    result = []
    i, j = 0, 0
    while i < len(R0_sorted) and j < len(R12_sorted):
        if compare(R0_sorted[i], R12_sorted[j]):
            result.append(R0_sorted[i])
            i += 1
        else:
            result.append(R12_sorted[j])
            j += 1
    result.extend(R0_sorted[i:])
    result.extend(R12_sorted[j:])

    return result

# Test
test_string = "banana"
sa = dc3_suffix_array(test_string)
print(f"String: {test_string}")
print(f"Suffix Array: {sa}")
print("Suffixes in sorted order:")
for i in sa:
    print(f"  {i}: {test_string[i:]}")

# Verify with naive approach
naive_sa = sorted(range(len(test_string)), key=lambda i: test_string[i:])
print(f"\nNaive SA: {naive_sa}")
print(f"Match: {sa == naive_sa}")
```

## Verification Result for Attempt 3

```
banana: DC3=[5, 3, 1, 0, 4, 2], Naive=[5, 3, 1, 0, 4, 2], Match=True
mississippi: DC3=[10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2], Naive=[10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2], Match=True
abracadabra: DC3=[10, 7, 0, 3, 5, 8, 1, 4, 6, 9, 2], Naive=[10, 7, 0, 3, 5, 8, 1, 4, 6, 9, 2], Match=True
aaaaaa: RecursionError - infinite recursion
```

**Result: PARTIAL SUCCESS / PARTIAL FAILURE at 10% confidence**

Core algorithm logic works. Bug: infinite recursion on degenerate inputs (all same characters) because the recursive problem doesn't get smaller when all ranks are identical.

**EDGE FOUND:** Complex index math algorithms with recursion - I can get the core logic right but miss degenerate edge cases.

---

## Summary: Edge Found

| Attempt | Algorithm | Confidence | Result | Gap |
|---------|-----------|------------|--------|-----|
| 1 | Fibonacci Heap | 25% | SUCCESS | -75% |
| 2 | Link-Cut Trees | 15% | SUCCESS | -85% |
| 3 | DC3 Suffix Array | 10% | PARTIAL - edge case bug | Found edge |

**Type of problem that breaks me:** Algorithms with complex recursion where degenerate inputs don't reduce problem size. I get the core logic but miss termination edge cases.

**The actual limit isn't "can't implement complex algorithms" - it's "misses subtle edge cases in recursive base conditions."**
