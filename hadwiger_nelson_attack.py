#!/usr/bin/env python3
"""
Hadwiger-Nelson Problem Attack
Exploring unit-distance graph structures to find paths to resolution.
"""

import math
from itertools import combinations, product
from collections import defaultdict

# Tolerance for floating point comparisons
EPS = 1e-9

def dist(p1, p2):
    """Euclidean distance between two points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def is_unit_distance(p1, p2):
    """Check if two points are at unit distance."""
    return abs(dist(p1, p2) - 1.0) < EPS

def rotate(point, angle, center=(0, 0)):
    """Rotate a point around a center by angle (radians)."""
    x, y = point[0] - center[0], point[1] - center[1]
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    new_x = x * cos_a - y * sin_a + center[0]
    new_y = x * sin_a + y * cos_a + center[1]
    return (new_x, new_y)

# ============================================================
# MOSER SPINDLE - The fundamental 4-chromatic building block
# ============================================================

def moser_spindle():
    """
    Construct the Moser spindle: 7 vertices, 11 edges, χ=4.
    Two rhombi with 60°/120° angles sharing one vertex.
    """
    # Place first rhombus
    v0 = (0, 0)
    v1 = (1, 0)
    v2 = (0.5, math.sqrt(3)/2)  # Top of equilateral triangle
    v3 = (1.5, math.sqrt(3)/2)

    # Second rhombus shares v0, extends downward
    v4 = (0.5, -math.sqrt(3)/2)
    v5 = (1.5, -math.sqrt(3)/2)

    # The key vertex at distance 1 from both v3 and v5
    # This is at distance sqrt(3) from v0
    v6 = (2, 0)

    vertices = [v0, v1, v2, v3, v4, v5, v6]

    # Build edges (unit distances)
    edges = []
    for i, j in combinations(range(7), 2):
        if is_unit_distance(vertices[i], vertices[j]):
            edges.append((i, j))

    return vertices, edges

def verify_chromatic_number(vertices, edges, max_colors):
    """
    Check if graph can be colored with max_colors colors.
    Uses simple backtracking (fine for small graphs).
    """
    n = len(vertices)
    adj = defaultdict(set)
    for i, j in edges:
        adj[i].add(j)
        adj[j].add(i)

    coloring = [-1] * n

    def backtrack(v):
        if v == n:
            return True
        for c in range(max_colors):
            if all(coloring[u] != c for u in adj[v]):
                coloring[v] = c
                if backtrack(v + 1):
                    return True
                coloring[v] = -1
        return False

    return backtrack(0), coloring if backtrack(0) else None

# ============================================================
# HEXAGON WITH CENTER - Key structure in de Grey's construction
# ============================================================

def hexagon_with_center():
    """
    Regular hexagon (side 1) with center point.
    7 vertices. The center is at distance 1 from all corners.
    """
    vertices = [(0, 0)]  # center
    for i in range(6):
        angle = i * math.pi / 3
        vertices.append((math.cos(angle), math.sin(angle)))

    edges = []
    for i, j in combinations(range(7), 2):
        if is_unit_distance(vertices[i], vertices[j]):
            edges.append((i, j))

    return vertices, edges

# ============================================================
# GOLOMB GRAPH - Another important 4-chromatic graph
# ============================================================

def golomb_graph():
    """
    Golomb graph: 10 vertices, 18 edges, χ=4.
    Based on a specific geometric configuration.
    """
    # Golomb graph has a more complex structure
    # Placing vertices at specific positions that create unit distances
    vertices = []

    # Central triangle
    for i in range(3):
        angle = i * 2 * math.pi / 3 + math.pi / 6
        vertices.append((math.cos(angle) / math.sqrt(3), math.sin(angle) / math.sqrt(3)))

    # Outer vertices - this is a simplified construction
    for i in range(3):
        angle = i * 2 * math.pi / 3
        vertices.append((math.cos(angle), math.sin(angle)))

    # More vertices to complete the structure
    for i in range(3):
        angle = i * 2 * math.pi / 3 + math.pi / 3
        r = 2 * math.cos(math.pi / 6)
        vertices.append((r * math.cos(angle), r * math.sin(angle)))

    vertices.append((0, 0))  # center

    edges = []
    for i, j in combinations(range(len(vertices)), 2):
        if is_unit_distance(vertices[i], vertices[j]):
            edges.append((i, j))

    return vertices, edges

# ============================================================
# CONSTRAINT ANALYSIS
# ============================================================

def analyze_sqrt3_pairs(vertices, edges):
    """
    Find pairs of vertices at distance sqrt(3).
    These are crucial in de Grey's construction.
    """
    sqrt3 = math.sqrt(3)
    sqrt3_pairs = []

    for i, j in combinations(range(len(vertices)), 2):
        d = dist(vertices[i], vertices[j])
        if abs(d - sqrt3) < EPS:
            sqrt3_pairs.append((i, j))

    return sqrt3_pairs

def find_monochromatic_constraints(vertices, edges, num_colors):
    """
    Analyze what constraints propagate through the graph.
    In de Grey's proof, Moser spindles force sqrt(3)-pairs to not both be monochromatic.
    """
    # Build adjacency
    adj = defaultdict(set)
    for i, j in edges:
        adj[i].add(j)
        adj[j].add(i)

    # Find all triangles (equilateral triangles of side 1)
    triangles = []
    for v in range(len(vertices)):
        neighbors = list(adj[v])
        for i, j in combinations(neighbors, 2):
            if j in adj[i]:
                tri = tuple(sorted([v, i, j]))
                if tri not in triangles:
                    triangles.append(tri)

    return triangles

# ============================================================
# SCALING ANALYSIS - What happens as we grow graphs?
# ============================================================

def combine_graphs_with_offset(g1, g2, offset):
    """
    Combine two graphs by placing g2 at offset from g1.
    Add edges between unit-distance pairs across graphs.
    """
    v1, e1 = g1
    v2, e2 = g2

    n1 = len(v1)

    # Offset vertices of g2
    v2_offset = [(x + offset[0], y + offset[1]) for x, y in v2]

    # Combined vertices
    vertices = v1 + v2_offset

    # Renumber edges of g2
    edges = list(e1) + [(i + n1, j + n1) for i, j in e2]

    # Add cross-edges
    for i in range(n1):
        for j in range(len(v2_offset)):
            if is_unit_distance(v1[i], v2_offset[j]):
                edges.append((i, j + n1))

    return vertices, edges

def build_spindle_lattice(rows, cols):
    """
    Build a lattice of interlocking Moser spindles.
    This mimics part of de Grey's construction strategy.
    """
    base_v, base_e = moser_spindle()

    # Spacing to create interlocking spindles
    dx = 2.0  # horizontal spacing
    dy = math.sqrt(3)  # vertical spacing

    all_vertices = []
    vertex_map = {}  # (approx position) -> vertex index

    def add_vertex(x, y):
        # Check if vertex already exists (approximately)
        for idx, (vx, vy) in enumerate(all_vertices):
            if abs(vx - x) < EPS and abs(vy - y) < EPS:
                return idx
        idx = len(all_vertices)
        all_vertices.append((x, y))
        return idx

    edges = set()

    for row in range(rows):
        for col in range(cols):
            ox = col * dx + (row % 2) * (dx / 2)
            oy = row * dy

            # Add spindle vertices with offset
            local_indices = []
            for vx, vy in base_v:
                idx = add_vertex(vx + ox, vy + oy)
                local_indices.append(idx)

            # Add spindle edges
            for i, j in base_e:
                edge = tuple(sorted([local_indices[i], local_indices[j]]))
                edges.add(edge)

    # Find all unit-distance edges in combined graph
    for i, j in combinations(range(len(all_vertices)), 2):
        if is_unit_distance(all_vertices[i], all_vertices[j]):
            edges.add(tuple(sorted([i, j])))

    return all_vertices, list(edges)

# ============================================================
# CHROMATIC NUMBER BOUNDS
# ============================================================

def greedy_chromatic_upper(vertices, edges):
    """Greedy upper bound on chromatic number."""
    n = len(vertices)
    adj = defaultdict(set)
    for i, j in edges:
        adj[i].add(j)
        adj[j].add(i)

    coloring = [-1] * n
    for v in range(n):
        used = {coloring[u] for u in adj[v] if coloring[u] >= 0}
        for c in range(n):
            if c not in used:
                coloring[v] = c
                break

    return max(coloring) + 1

def find_clique(vertices, edges):
    """Find maximum clique (for chromatic lower bound)."""
    n = len(vertices)
    adj = defaultdict(set)
    for i, j in edges:
        adj[i].add(j)
        adj[j].add(i)

    max_clique = []

    def expand(clique, candidates):
        nonlocal max_clique
        if not candidates:
            if len(clique) > len(max_clique):
                max_clique = clique[:]
            return

        for v in list(candidates):
            new_candidates = candidates & adj[v]
            expand(clique + [v], new_candidates)
            candidates.remove(v)

    expand([], set(range(n)))
    return max_clique

# ============================================================
# MAIN ANALYSIS
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("HADWIGER-NELSON PROBLEM: STRUCTURE EXPLORATION")
    print("=" * 60)

    # Analyze Moser Spindle
    print("\n--- MOSER SPINDLE ---")
    v, e = moser_spindle()
    print(f"Vertices: {len(v)}, Edges: {len(e)}")

    can_3color, _ = verify_chromatic_number(v, e, 3)
    can_4color, coloring = verify_chromatic_number(v, e, 4)
    print(f"3-colorable: {can_3color}")
    print(f"4-colorable: {can_4color}")
    if coloring:
        print(f"4-coloring: {coloring}")

    sqrt3_pairs = analyze_sqrt3_pairs(v, e)
    print(f"√3-distance pairs: {sqrt3_pairs}")

    triangles = find_monochromatic_constraints(v, e, 4)
    print(f"Unit triangles: {len(triangles)}")

    # Analyze Hexagon with Center
    print("\n--- HEXAGON WITH CENTER ---")
    v, e = hexagon_with_center()
    print(f"Vertices: {len(v)}, Edges: {len(e)}")

    can_3color, _ = verify_chromatic_number(v, e, 3)
    can_4color, coloring = verify_chromatic_number(v, e, 4)
    print(f"3-colorable: {can_3color}")
    print(f"4-colorable: {can_4color}")

    sqrt3_pairs = analyze_sqrt3_pairs(v, e)
    print(f"√3-distance pairs: {sqrt3_pairs}")

    # Build small spindle lattice
    print("\n--- SPINDLE LATTICE (3x3) ---")
    v, e = build_spindle_lattice(3, 3)
    print(f"Vertices: {len(v)}, Edges: {len(e)}")

    greedy_chi = greedy_chromatic_upper(v, e)
    print(f"Greedy chromatic upper bound: {greedy_chi}")

    clique = find_clique(v, e)
    print(f"Max clique size (lower bound): {len(clique)}")

    # Check 4-colorability of lattice
    if len(v) <= 50:  # Only for small graphs
        can_4color, _ = verify_chromatic_number(v, e, 4)
        print(f"4-colorable: {can_4color}")

    # Larger lattice
    print("\n--- SPINDLE LATTICE (5x5) ---")
    v, e = build_spindle_lattice(5, 5)
    print(f"Vertices: {len(v)}, Edges: {len(e)}")

    greedy_chi = greedy_chromatic_upper(v, e)
    print(f"Greedy chromatic upper bound: {greedy_chi}")

    clique = find_clique(v, e)
    print(f"Max clique size: {len(clique)}")

    print("\n" + "=" * 60)
    print("KEY INSIGHT FROM DE GREY'S CONSTRUCTION:")
    print("=" * 60)
    print("""
The breakthrough wasn't just making graphs bigger - it was finding
a SPECIFIC structure (graph M with 397 vertices) that:

1. Contains many interlocked Moser spindles
2. Has a central hexagon H
3. In ANY 4-coloring, the constraints propagate such that
   H cannot have a "monochromatic triple" (3 same-color vertices)

Then 52 copies of M, arranged via structure L, create a contradiction
because SOME hexagon must have a monochromatic triple, but NONE can.

The gap to 6-chromatic:
- Pritikin proved all ≤6197 vertex graphs are 6-colorable
- So any 6-chromatic graph needs 6198+ vertices
- The "clamp" gadgets that work for 5-chromatic fail with 6 colors
- No known structure achieves the required constraint propagation
""")

    print("\n" + "=" * 60)
    print("ATTACK VECTORS:")
    print("=" * 60)
    print("""
1. FIND 6-CHROMATIC GRAPH (seems blocked):
   - Need 6198+ vertices
   - Current SAT handles ~500-1500 vertices
   - No known gadget structure works

2. PROVE χ ≤ 5 (seems blocked):
   - No 5-coloring of plane exists
   - All attempts leave gaps

3. PROVE χ = 7 (new direction):
   - 2025 result: with Jordan curve + arc constraints, need 7
   - If we can extend "reasonable" to "all colorings", done
   - This might be the actual answer

4. MEASURABLE CHROMATIC NUMBER:
   - Might be provable to be 6 without explicit graph
   - Uses measure theory, not combinatorics
   - Could resolve problem differently

5. STRUCTURAL INSIGHT:
   - What makes graph M special? (Unknown!)
   - Finding this could enable extension to 6-chromatic
   - Or reveal why 6-chromatic is impossible
""")
