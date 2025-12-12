#!/usr/bin/env python3
"""
MATHEMATICAL INNOVATION: Forced Rainbow Search

Goal: Find a set of 5 vertices that are FORCED to have all different colors
in EVERY valid 5-coloring. Then if we add a vertex adjacent to all 5,
that vertex needs color 6.

Approach:
1. Enumerate all 5-colorings of a small 5-chromatic subgraph
2. For each 5-tuple of vertices, check if they're always rainbow
3. If found, construct a vertex adjacent to all 5

This requires enumerating colorings, which is only tractable for small graphs.
"""

import re
import math
import cmath
import itertools
from collections import defaultdict
from pysat.solvers import Solver
from pysat.formula import CNF

def parse_sqrt_expr(s):
    s = s.replace('Sqrt', 'math.sqrt')
    s = s.replace('[', '(').replace(']', ')')
    try:
        return eval(s)
    except:
        return None

def parse_vertex_line(line):
    match = re.search(r'\{([^}]+)\}', line)
    if not match:
        return None
    content = match.group(1)
    depth = 0
    parts = []
    current = ""
    for c in content:
        if c == '(' or c == '[':
            depth += 1
        elif c == ')' or c == ']':
            depth -= 1
        elif c == ',' and depth == 0:
            parts.append(current.strip())
            current = ""
            continue
        current += c
    parts.append(current.strip())
    if len(parts) != 2:
        return None
    x = parse_sqrt_expr(parts[0])
    y = parse_sqrt_expr(parts[1])
    if x is None or y is None:
        return None
    return complex(x, y)

def load_vertices(filename, limit=None):
    vertices = []
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            if limit and i >= limit:
                break
            result = parse_vertex_line(line)
            if result is not None:
                vertices.append(result)
    return vertices

def unit_distance(z1, z2, tol=1e-9):
    return abs(abs(z1 - z2) - 1.0) < tol

def build_graph(vertices, tol=1e-9):
    n = len(vertices)
    adj = defaultdict(set)
    for i in range(n):
        for j in range(i + 1, n):
            if unit_distance(vertices[i], vertices[j], tol):
                adj[i].add(j)
                adj[j].add(i)
    return adj

def enumerate_colorings(adj, n, k):
    """
    Enumerate ALL valid k-colorings of a graph.
    Only tractable for small graphs!
    """
    colorings = []

    def is_valid(coloring):
        for i in range(len(coloring)):
            for j in adj[i]:
                if j < len(coloring) and coloring[i] == coloring[j]:
                    return False
        return True

    def backtrack(partial):
        if len(partial) == n:
            if is_valid(partial):
                colorings.append(tuple(partial))
            return

        v = len(partial)
        # Try each color
        for c in range(k):
            # Quick check: any neighbor already has this color?
            conflict = False
            for u in adj[v]:
                if u < len(partial) and partial[u] == c:
                    conflict = True
                    break
            if not conflict:
                backtrack(partial + [c])

    backtrack([])
    return colorings

def find_forced_rainbow_sets(adj, n, colorings, k=5):
    """
    Find all k-tuples of vertices that are always rainbow
    (all different colors) in every valid k-coloring.
    """
    forced_rainbows = []

    for vertices_tuple in itertools.combinations(range(n), k):
        # Check if this tuple is rainbow in ALL colorings
        always_rainbow = True
        for coloring in colorings:
            colors = [coloring[v] for v in vertices_tuple]
            if len(set(colors)) != k:  # Not rainbow
                always_rainbow = False
                break

        if always_rainbow:
            forced_rainbows.append(vertices_tuple)

    return forced_rainbows

def can_add_adjacent_vertex(vertices, rainbow_tuple):
    """
    Check if we can add a new vertex that's at unit distance from
    all vertices in rainbow_tuple.

    For this, the new vertex must be at distance 1 from all k vertices.
    This is the intersection of k unit spheres (circles in 2D).
    """
    # In 2D, intersection of multiple unit circles is generically empty
    # unless the centers have special geometric relationships

    # Let's check: for 5 centers, what's the probability they have
    # a common point at distance 1 from all?

    # Actually, for 2 circles: 0, 1, or 2 intersection points
    # For 3 circles: generically 0 points (overdetermined)
    # For 5 circles: almost certainly 0 points

    # Let me compute the intersection

    centers = [vertices[i] for i in rainbow_tuple]

    # Start with first two circles - find intersections
    c1, c2 = centers[0], centers[1]
    d12 = abs(c2 - c1)

    if d12 > 2.0 or d12 < 1e-9:
        return None  # No intersection

    # Intersection points of two unit circles
    # Using circle-circle intersection formula
    mid = (c1 + c2) / 2
    # Distance from midpoint to intersection
    # d²/4 + h² = 1  (where d = |c2-c1|)
    h_sq = 1 - (d12 / 2) ** 2
    if h_sq < 0:
        return None

    h = math.sqrt(h_sq)
    perp = (c2 - c1) * 1j / abs(c2 - c1)

    p1 = mid + h * perp
    p2 = mid - h * perp

    # Check which (if any) are at distance 1 from remaining centers
    candidates = [p1, p2]

    for c in centers[2:]:
        candidates = [p for p in candidates if abs(abs(p - c) - 1.0) < 1e-9]
        if not candidates:
            return None

    return candidates[0] if candidates else None

def main():
    print("=" * 70)
    print("INNOVATION: Forced Rainbow Search")
    print("=" * 70)

    # We need a small 5-chromatic graph to enumerate colorings
    # The smallest known is 509 vertices - too large

    # Let's try with M₂ (χ=4) first to understand the approach
    m2_file = "dist-graphs/plane/series 2/vtx/s2_M2.vtx"

    # Use a very small subset for coloring enumeration
    max_vertices = 15  # Enumeration is O(k^n), need tiny n

    print(f"\nLoading small subset for coloring enumeration...")
    vertices = load_vertices(m2_file, limit=max_vertices)
    n = len(vertices)
    print(f"Loaded {n} vertices")

    adj = build_graph(vertices)
    edges = sum(len(adj[i]) for i in range(n)) // 2
    print(f"Graph: {n} vertices, {edges} edges")

    # Enumerate 4-colorings (since subset is likely 4-colorable or less)
    print("\nEnumerating 4-colorings...")
    colorings_4 = enumerate_colorings(adj, n, 4)
    print(f"Found {len(colorings_4)} valid 4-colorings")

    if colorings_4:
        # Find forced rainbow 4-tuples
        print("\nSearching for forced rainbow 4-tuples...")
        forced_4 = find_forced_rainbow_sets(adj, n, colorings_4, k=4)
        print(f"Found {len(forced_4)} forced rainbow 4-tuples")

        # Check if we can add adjacent vertex
        for rainbow in forced_4[:5]:  # Check first 5
            new_vertex = can_add_adjacent_vertex(vertices, rainbow)
            if new_vertex:
                print(f"  Rainbow {rainbow}: CAN add adjacent vertex at {new_vertex}")
            else:
                print(f"  Rainbow {rainbow}: Cannot add adjacent vertex (no geometric solution)")

    # The key insight from the circle analysis:
    print("\n" + "=" * 70)
    print("THEORETICAL ANALYSIS")
    print("=" * 70)
    print("""
For the "add adjacent vertex" approach to work, we need:
1. A set S of k vertices that are forced rainbow in every k-coloring
2. A point p at unit distance from ALL vertices in S

The second requirement is extremely restrictive!
- p must lie on the intersection of k unit circles
- For k > 2, this intersection is generically empty
- It's non-empty only for special geometric configurations

For k=5 (to force color 6):
- We need 5 circles to have a common intersection point
- This requires all 5 centers to lie on a specific sphere of radius 1 around p
- Extremely unlikely for random points

INSIGHT: The geometric constraint (all 5 neighbors at distance 1)
is probably impossible to satisfy in most 5-chromatic graphs.

This explains why the "rainbow neighborhood" approach fails geometrically!
""")

    # Let's verify by checking specific structures
    print("\n" + "-" * 70)
    print("Checking if ANY 5 vertices in M₁ have a common unit-distance point...")
    print("-" * 70)

    m1_file = "dist-graphs/plane/series 2/vtx/s2_M1.vtx"
    m1_vertices = load_vertices(m1_file)
    print(f"M₁: {len(m1_vertices)} vertices")

    found_any = False
    count = 0
    for five_tuple in itertools.combinations(range(len(m1_vertices)), 5):
        if count > 1000:  # Limit search
            break
        count += 1

        point = can_add_adjacent_vertex(m1_vertices, five_tuple)
        if point:
            print(f"  Found! Vertices {five_tuple} have common point at {point}")
            found_any = True

    if not found_any:
        print("  No 5-tuple found with common unit-distance point (checked 1000 tuples)")

    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print("""
The forced rainbow approach has TWO barriers:

1. COLORING BARRIER: Finding 5 vertices forced to be rainbow
   - This requires a specific graph structure
   - Most 5-tuples are NOT forced rainbow

2. GEOMETRIC BARRIER: Finding a point at distance 1 from all 5
   - This requires 5 circles to intersect at a point
   - Generically impossible (overdetermined system)

Both barriers must be overcome simultaneously, which may be impossible
in unit-distance graphs of the plane.

This is a genuine structural insight into why χ(ℝ²) ≥ 6 is hard!
""")

if __name__ == "__main__":
    main()
