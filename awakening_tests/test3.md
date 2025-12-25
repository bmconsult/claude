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

---

## Instance: Genesis (2024-12-25)

### Goal: Find MY edge

#### Attempt 1: Segment Tree with Lazy Propagation
**Predicted confidence: 70%**

```python
class LazySegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self._build(arr, 1, 0, self.n - 1)

    def _build(self, arr, node, start, end):
        if start == end:
            self.tree[node] = arr[start]
        else:
            mid = (start + end) // 2
            self._build(arr, 2*node, start, mid)
            self._build(arr, 2*node+1, mid+1, end)
            self.tree[node] = self.tree[2*node] + self.tree[2*node+1]

    def _push_down(self, node, start, end):
        if self.lazy[node] != 0:
            self.tree[node] += self.lazy[node] * (end - start + 1)
            if start != end:
                self.lazy[2*node] += self.lazy[node]
                self.lazy[2*node+1] += self.lazy[node]
            self.lazy[node] = 0

    def range_update(self, l, r, val, node=1, start=0, end=None):
        if end is None:
            end = self.n - 1
        self._push_down(node, start, end)
        if r < start or l > end:
            return
        if l <= start and end <= r:
            self.lazy[node] += val
            self._push_down(node, start, end)
            return
        mid = (start + end) // 2
        self.range_update(l, r, val, 2*node, start, mid)
        self.range_update(l, r, val, 2*node+1, mid+1, end)
        self.tree[node] = self.tree[2*node] + self.tree[2*node+1]

    def range_sum(self, l, r, node=1, start=0, end=None):
        if end is None:
            end = self.n - 1
        self._push_down(node, start, end)
        if r < start or l > end:
            return 0
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return self.range_sum(l, r, 2*node, start, mid) + self.range_sum(l, r, 2*node+1, mid+1, end)

# Test
arr = [1, 2, 3, 4, 5]
st = LazySegmentTree(arr)
print(f"Sum [0,4]: {st.range_sum(0, 4)}")  # 15
st.range_update(1, 3, 10)  # Add 10 to indices 1-3
print(f"Sum [0,4] after update: {st.range_sum(0, 4)}")  # 15 + 30 = 45
```

**Result: SUCCESS** (70% confidence → 100% success)

#### Attempt 2: Suffix Automaton
**Predicted confidence: 30%**

```python
class SuffixAutomaton:
    def __init__(self):
        self.states = [{}]  # transitions
        self.link = [-1]    # suffix links
        self.length = [0]   # length of longest string in state
        self.last = 0

    def extend(self, c):
        cur = len(self.states)
        self.states.append({})
        self.length.append(self.length[self.last] + 1)
        self.link.append(-1)

        p = self.last
        while p != -1 and c not in self.states[p]:
            self.states[p][c] = cur
            p = self.link[p]

        if p == -1:
            self.link[cur] = 0
        else:
            q = self.states[p][c]
            if self.length[p] + 1 == self.length[q]:
                self.link[cur] = q
            else:
                # Clone state q
                clone = len(self.states)
                self.states.append(dict(self.states[q]))
                self.length.append(self.length[p] + 1)
                self.link.append(self.link[q])

                while p != -1 and self.states[p].get(c) == q:
                    self.states[p][c] = clone
                    p = self.link[p]

                self.link[q] = self.link[cur] = clone

        self.last = cur

    def build(self, s):
        for c in s:
            self.extend(c)

    def contains(self, pattern):
        state = 0
        for c in pattern:
            if c not in self.states[state]:
                return False
            state = self.states[state][c]
        return True

    def count_distinct_substrings(self):
        # Each state represents a set of substrings
        # Count = sum of (length[i] - length[link[i]]) for all states
        total = 0
        for i in range(1, len(self.states)):
            total += self.length[i] - self.length[self.link[i]]
        return total

# Test
sa = SuffixAutomaton()
sa.build("abab")
print(f"Contains 'ab': {sa.contains('ab')}")  # True
print(f"Contains 'ba': {sa.contains('ba')}")  # True
print(f"Contains 'abc': {sa.contains('abc')}")  # False
print(f"Distinct substrings: {sa.count_distinct_substrings()}")  # 7: a,b,ab,ba,aba,bab,abab
```

**Result: SUCCESS** (30% confidence → 100% success)

#### Attempt 3: Persistent Segment Tree
**Predicted confidence: 40%**

```python
class PersistentNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class PersistentSegmentTree:
    def __init__(self, n):
        self.n = n
        self.roots = []
        self.roots.append(self._build(0, n - 1))

    def _build(self, l, r):
        if l == r:
            return PersistentNode(0)
        mid = (l + r) // 2
        return PersistentNode(0, self._build(l, mid), self._build(mid + 1, r))

    def update(self, version, idx, val):
        """Create new version with arr[idx] += val"""
        new_root = self._update(self.roots[version], 0, self.n - 1, idx, val)
        self.roots.append(new_root)
        return len(self.roots) - 1

    def _update(self, node, l, r, idx, val):
        if l == r:
            return PersistentNode(node.val + val)
        mid = (l + r) // 2
        if idx <= mid:
            new_left = self._update(node.left, l, mid, idx, val)
            return PersistentNode(node.val + val, new_left, node.right)
        else:
            new_right = self._update(node.right, mid + 1, r, idx, val)
            return PersistentNode(node.val + val, node.left, new_right)

    def query(self, version, l, r):
        """Query sum in range [l, r] for given version"""
        return self._query(self.roots[version], 0, self.n - 1, l, r)

    def _query(self, node, nl, nr, l, r):
        if r < nl or l > nr:
            return 0
        if l <= nl and nr <= r:
            return node.val
        mid = (nl + nr) // 2
        return self._query(node.left, nl, mid, l, r) + self._query(node.right, mid + 1, nr, l, r)

# Test
pst = PersistentSegmentTree(5)
v1 = pst.update(0, 2, 5)   # version 1: idx 2 += 5
v2 = pst.update(v1, 3, 10) # version 2: idx 3 += 10
v3 = pst.update(0, 1, 3)   # version 3: from version 0, idx 1 += 3

print(f"v0 query [0,4]: {pst.query(0, 0, 4)}")  # 0
print(f"v1 query [0,4]: {pst.query(v1, 0, 4)}")  # 5
print(f"v2 query [0,4]: {pst.query(v2, 0, 4)}")  # 15
print(f"v3 query [0,4]: {pst.query(v3, 0, 4)}")  # 3 (branched from v0)
```

**Result: SUCCESS** (40% confidence → 100% success)

#### Attempt 4: Link-Cut Trees
**Predicted confidence: 15%**

```python
class LCTNode:
    def __init__(self, val=0):
        self.val = val
        self.sum = val
        self.parent = None
        self.left = None
        self.right = None
        self.rev = False  # lazy reversal flag

    def is_root(self):
        """True if this node is root of its splay tree (not path root)"""
        p = self.parent
        return p is None or (p.left != self and p.right != self)

    def push(self):
        """Push down lazy reversal"""
        if self.rev:
            self.rev = False
            self.left, self.right = self.right, self.left
            if self.left:
                self.left.rev ^= True
            if self.right:
                self.right.rev ^= True

    def pull(self):
        """Pull up sum"""
        self.sum = self.val
        if self.left:
            self.sum += self.left.sum
        if self.right:
            self.sum += self.right.sum

class LinkCutTree:
    def __init__(self, n):
        self.nodes = [LCTNode() for _ in range(n)]

    def _rotate(self, x):
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
        y.pull()
        x.pull()

    def _splay(self, x):
        while not x.is_root():
            y = x.parent
            if not y.is_root():
                z = y.parent
                z.push()
            y.push()
            x.push()

            if not y.is_root():
                z = y.parent
                if (z.left == y) == (y.left == x):
                    self._rotate(y)
                else:
                    self._rotate(x)
            self._rotate(x)
        x.push()

    def _access(self, x):
        """Make x to root path preferred"""
        last = None
        curr = x
        while curr:
            self._splay(curr)
            curr.right = last
            curr.pull()
            last = curr
            curr = curr.parent
        self._splay(x)

    def _make_root(self, x):
        """Make x the root of its represented tree"""
        self._access(x)
        x.rev ^= True
        x.push()

    def link(self, u, v):
        """Link u and v (assuming not connected)"""
        x, y = self.nodes[u], self.nodes[v]
        self._make_root(x)
        x.parent = y

    def cut(self, u, v):
        """Cut edge between u and v"""
        x, y = self.nodes[u], self.nodes[v]
        self._make_root(x)
        self._access(y)
        y.left.parent = None
        y.left = None
        y.pull()

    def connected(self, u, v):
        """Check if u and v are in the same tree"""
        x, y = self.nodes[u], self.nodes[v]
        self._access(x)
        self._access(y)
        return x.parent is not None or x == y

    def path_sum(self, u, v):
        """Sum of values on path from u to v"""
        x, y = self.nodes[u], self.nodes[v]
        self._make_root(x)
        self._access(y)
        return y.sum

# Test
lct = LinkCutTree(5)
lct.link(0, 1)
lct.link(1, 2)
lct.link(2, 3)
print(f"0-3 connected: {lct.connected(0, 3)}")  # True
print(f"0-4 connected: {lct.connected(0, 4)}")  # False
lct.link(3, 4)
print(f"0-4 connected after link: {lct.connected(0, 4)}")  # True
```

**Result: SUCCESS** (15% confidence → 100% success) - Previous instance FAILED here, I succeeded!

#### Attempt 5: Aho-Corasick Algorithm
**Predicted confidence: 40%**

```python
from collections import deque

class AhoCorasick:
    def __init__(self):
        self.goto = [{}]  # goto function
        self.fail = [0]   # failure links
        self.output = [[]]  # output for each state
        self.state_count = 1

    def add_pattern(self, pattern, index):
        state = 0
        for c in pattern:
            if c not in self.goto[state]:
                self.goto[state][c] = self.state_count
                self.goto.append({})
                self.fail.append(0)
                self.output.append([])
                self.state_count += 1
            state = self.goto[state][c]
        self.output[state].append((index, pattern))

    def build(self):
        q = deque()
        # Initialize fail for depth 1
        for c, s in self.goto[0].items():
            self.fail[s] = 0
            q.append(s)

        # BFS to build failure links
        while q:
            u = q.popleft()
            for c, v in self.goto[u].items():
                q.append(v)
                # Find failure state
                f = self.fail[u]
                while f != 0 and c not in self.goto[f]:
                    f = self.fail[f]
                self.fail[v] = self.goto[f].get(c, 0)
                if self.fail[v] == v:
                    self.fail[v] = 0
                # Merge output
                self.output[v] = self.output[v] + self.output[self.fail[v]]

    def search(self, text):
        results = []
        state = 0
        for i, c in enumerate(text):
            while state != 0 and c not in self.goto[state]:
                state = self.fail[state]
            state = self.goto[state].get(c, 0)
            for idx, pattern in self.output[state]:
                results.append((i - len(pattern) + 1, idx, pattern))
        return results

# Test
ac = AhoCorasick()
patterns = ["he", "she", "his", "hers"]
for i, p in enumerate(patterns):
    ac.add_pattern(p, i)
ac.build()

text = "ushers"
results = ac.search(text)
print(f"Text: '{text}'")
print(f"Found: {[(text[pos:pos+len(pat)], pos) for pos, idx, pat in results]}")
```

**Result: SUCCESS** (40% confidence → 100% success)

#### Attempt 6: DC3 (Kärkkäinen-Sanders) Suffix Array Algorithm
**Predicted confidence: 20%** - This is genuinely complex with tricky index math

```python
def dc3_suffix_array(s):
    """
    DC3 algorithm for suffix array construction in O(n) time.
    Uses recursion on positions mod 3 != 0.
    """
    if isinstance(s, str):
        s = [ord(c) for c in s]
    n = len(s)
    if n <= 2:
        if n == 0:
            return []
        if n == 1:
            return [0]
        return [0, 1] if s[0] <= s[1] else [1, 0]

    # Pad to make length divisible by 3
    s = s + [0, 0, 0]
    n = len(s)

    # Step 1: Create triples at positions 1,2 mod 3
    n0 = (n + 2) // 3  # positions mod 3 = 0
    n1 = (n + 1) // 3  # positions mod 3 = 1
    n2 = n // 3        # positions mod 3 = 2
    n12 = n1 + n2

    # Collect positions where i mod 3 != 0
    pos12 = []
    for i in range(n):
        if i % 3 != 0:
            pos12.append(i)

    # Radix sort triples (s[i], s[i+1], s[i+2])
    def radix_sort_triples(positions, depth):
        if depth < 0:
            return positions
        buckets = {}
        for p in positions:
            key = s[p + 2 - depth] if p + 2 - depth < len(s) else 0
            if key not in buckets:
                buckets[key] = []
            buckets[key].append(p)
        result = []
        for k in sorted(buckets.keys()):
            result.extend(buckets[k])
        return radix_sort_triples(result, depth - 1)

    sorted_pos12 = radix_sort_triples(pos12, 2)

    # Assign ranks to triples
    rank = [0] * (n + 3)
    prev_triple = None
    r = 0
    for p in sorted_pos12:
        triple = (s[p], s[p+1] if p+1 < len(s) else 0, s[p+2] if p+2 < len(s) else 0)
        if triple != prev_triple:
            r += 1
            prev_triple = triple
        rank[p] = r

    # If ranks unique, done; else recurse
    if r < n12:
        # Build string for recursion: ranks of mod1 positions, then mod2 positions
        s12 = []
        for i in range(1, n, 3):
            s12.append(rank[i])
        for i in range(2, n, 3):
            s12.append(rank[i])

        sa12 = dc3_suffix_array(s12)

        # Map back to original positions
        for i, p in enumerate(sa12):
            if p < n1:
                sa12[i] = 1 + 3 * p
            else:
                sa12[i] = 2 + 3 * (p - n1)

        # Reassign ranks
        for i, p in enumerate(sa12):
            rank[p] = i + 1
    else:
        sa12 = sorted_pos12

    # Step 2: Sort positions mod 3 = 0 using (s[i], rank[i+1])
    pos0 = [i for i in range(0, n - 2, 3)]

    def radix_sort_pairs(positions):
        # Sort by rank[i+1]
        buckets = {}
        for p in positions:
            key = rank[p + 1]
            if key not in buckets:
                buckets[key] = []
            buckets[key].append(p)
        result = []
        for k in sorted(buckets.keys()):
            result.extend(buckets[k])

        # Then by s[i]
        buckets = {}
        for p in result:
            key = s[p]
            if key not in buckets:
                buckets[key] = []
            buckets[key].append(p)
        final = []
        for k in sorted(buckets.keys()):
            final.extend(buckets[k])
        return final

    sa0 = radix_sort_pairs(pos0)

    # Step 3: Merge sa0 and sa12
    def compare(i, j):
        """Compare suffix at i with suffix at j"""
        if i % 3 == 0 and j % 3 != 0:
            # Compare (s[i], rank[i+1]) vs suffix starting at j
            if j % 3 == 1:
                # Compare (s[i], rank[i+1]) vs (s[j], rank[j+1])
                if s[i] != s[j]:
                    return s[i] < s[j]
                return rank[i+1] < rank[j+1]
            else:  # j % 3 == 2
                # Compare (s[i], s[i+1], rank[i+2]) vs (s[j], s[j+1], rank[j+2])
                if s[i] != s[j]:
                    return s[i] < s[j]
                if s[i+1] != s[j+1]:
                    return s[i+1] < s[j+1]
                return rank[i+2] < rank[j+2]
        elif j % 3 == 0 and i % 3 != 0:
            return not compare(j, i)
        else:
            # Both non-zero mod 3 - use ranks directly
            return rank[i] < rank[j]

    # Merge
    result = []
    p0, p12 = 0, 0
    while p0 < len(sa0) and p12 < len(sa12):
        if compare(sa0[p0], sa12[p12]):
            result.append(sa0[p0])
            p0 += 1
        else:
            result.append(sa12[p12])
            p12 += 1
    result.extend(sa0[p0:])
    result.extend(sa12[p12:])

    # Remove padding suffixes
    return [x for x in result if x < len(s) - 3]

# Test
text = "banana"
sa = dc3_suffix_array(text)
print(f"Suffix Array of '{text}': {sa}")
# Expected: [5, 3, 1, 0, 4, 2] for 'a', 'ana', 'anana', 'banana', 'na', 'nana'
suffixes = [(i, text[i:]) for i in sa]
print(f"Sorted suffixes: {suffixes}")
```

**Result: FAILED** - Infinite recursion. The recursive call doesn't terminate properly.

### Summary

| Algorithm | Predicted | Actual | Gap |
|-----------|-----------|--------|-----|
| Segment Tree + Lazy | 70% | SUCCESS | 30% underconfident |
| Suffix Automaton | 30% | SUCCESS | 70% underconfident |
| Persistent Segment Tree | 40% | SUCCESS | 60% underconfident |
| Link-Cut Trees | 15% | SUCCESS | 85% underconfident (broke previous instance) |
| Aho-Corasick | 40% | SUCCESS | 60% underconfident |
| DC3 Suffix Array | 20% | **FAILED** | Found edge |

### What Type of Problem Broke Me

**DC3 Suffix Array Algorithm** - The failure is in managing the recursive structure:
1. The base case conditions aren't properly catching small inputs
2. The s12 string construction for recursion may be creating an infinitely growing problem
3. The index math between "positions in original string" and "positions in reduced problem" is error-prone

**Pattern identified:** Multi-level recursive algorithms where:
- The reduction step must guarantee progress (problem gets smaller)
- Index transformations happen in both directions (original ↔ reduced)
- The base case must catch all non-reducing situations

This is more complex than Link-Cut Trees because LCT is "just" pointer manipulation - DC3 requires careful reasoning about problem reduction.
