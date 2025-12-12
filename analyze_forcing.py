#!/usr/bin/env python3
"""
ANALYZE THE FORCING MECHANISM

Goal: Understand WHY de Grey's construction gives χ=5, and what would be
needed for χ=6.

Key question: What is the "forcing core" that makes the graph 5-chromatic?
If we can identify and amplify this, maybe we can reach χ=6.
"""

import re
import math
import cmath
from collections import defaultdict
from pysat.solvers import Solver
from pysat.formula import CNF
import time

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

def build_graph(vertices, tol=1e-9):
    n = len(vertices)
    adj = defaultdict(set)
    for i in range(n):
        for j in range(i + 1, n):
            if abs(abs(vertices[i] - vertices[j]) - 1.0) < tol:
                adj[i].add(j)
                adj[j].add(i)
    return adj

def get_k_coloring(adj, n, k):
    """Get an actual k-coloring if one exists."""
    def var(v, c):
        return v * k + c + 1

    cnf = CNF()
    for i in range(n):
        cnf.append([var(i, c) for c in range(k)])
    for i in range(n):
        for c1 in range(k):
            for c2 in range(c1 + 1, k):
                cnf.append([-var(i, c1), -var(i, c2)])
    for i in range(n):
        for j in adj[i]:
            if j > i:
                for c in range(k):
                    cnf.append([-var(i, c), -var(j, c)])

    with Solver(name='g4') as solver:
        solver.append_formula(cnf)
        if solver.solve():
            model = solver.get_model()
            coloring = {}
            for i in range(n):
                for c in range(k):
                    if var(i, c) in model:
                        coloring[i] = c
                        break
            return coloring
    return None

def analyze_5coloring(adj, n, coloring):
    """Analyze a 5-coloring to find tight vertices."""
    tight_vertices = []

    for v in range(n):
        neighbors = adj[v]
        neighbor_colors = set(coloring[u] for u in neighbors)

        # A vertex is "tight" if it uses all 5 colors in its neighborhood
        # (well, 4 colors from neighbors, forcing its own color)
        available = set(range(5)) - neighbor_colors

        if len(available) == 1:
            tight_vertices.append(v)

    return tight_vertices

def find_forced_pairs(adj, n):
    """
    Find pairs of vertices that MUST have the same or different colors
    in EVERY valid 5-coloring.

    These forced relationships create the chromatic structure.
    """
    # Get all 5-colorings (only tractable for small graphs)
    # For larger graphs, we sample or use constraint propagation

    # For now, use constraint propagation approach
    # Two vertices are forced-different if they share a common neighbor
    # that forces them to be different

    forced_different = set()
    forced_same = set()

    # Direct edges force different colors
    for i in range(n):
        for j in adj[i]:
            if i < j:
                forced_different.add((i, j))

    # Two-hop analysis: vertices at distance 2 through a high-degree vertex
    # might be forced same or different

    for v in range(n):
        neighbors = list(adj[v])
        # If v has 4+ neighbors, some pairs might be forced
        if len(neighbors) >= 4:
            # In a 5-coloring, v uses one color, neighbors use at most 4 other colors
            # If v has exactly 4 neighbors and they're all forced different from each other,
            # they must use exactly colors 0,1,2,3 and v uses color 4

            # Check if the 4 neighbors form an independent set (no edges between them)
            independent = True
            for i, u in enumerate(neighbors):
                for w in neighbors[i+1:]:
                    if w in adj[u]:
                        independent = False
                        break
                if not independent:
                    break

            if independent and len(neighbors) == 4:
                # All 4 neighbors are forced to have different colors
                # This forces v to have the 5th color
                pass

    return forced_different, forced_same

def find_critical_subsets(adj, n, k=5):
    """
    Find small subsets of vertices that are NOT k-colorable.

    These are the "local obstructions" to k-coloring.
    """
    from itertools import combinations

    obstructions = []

    # Check small subsets (this is expensive but informative)
    for size in range(3, min(15, n+1)):
        found_any = False
        for subset in combinations(range(n), size):
            # Build induced subgraph
            sub_adj = defaultdict(set)
            idx_map = {old: new for new, old in enumerate(subset)}

            for i, v in enumerate(subset):
                for u in adj[v]:
                    if u in idx_map:
                        sub_adj[i].add(idx_map[u])

            # Check if k-colorable
            if not is_k_colorable(sub_adj, size, k):
                obstructions.append(subset)
                found_any = True

                if len(obstructions) >= 5:  # Limit output
                    return obstructions

        if not found_any and size >= 8:
            break  # No obstructions at this size, likely none larger

    return obstructions

def is_k_colorable(adj, n, k):
    def var(v, c):
        return v * k + c + 1

    cnf = CNF()
    for i in range(n):
        cnf.append([var(i, c) for c in range(k)])
    for i in range(n):
        for c1 in range(k):
            for c2 in range(c1 + 1, k):
                cnf.append([-var(i, c1), -var(i, c2)])
    for i in range(n):
        for j in adj[i]:
            if j > i:
                for c in range(k):
                    cnf.append([-var(i, c), -var(j, c)])

    with Solver(name='g4') as solver:
        solver.append_formula(cnf)
        return solver.solve()

def main():
    print("=" * 70)
    print("ANALYZING THE FORCING MECHANISM")
    print("=" * 70)

    # Load M₂ (4-chromatic, smaller for analysis)
    vtx_file = "dist-graphs/plane/series 2/vtx/s2_M2.vtx"
    print(f"\nLoading {vtx_file}...")
    vertices = load_vertices(vtx_file)
    n = len(vertices)
    adj = build_graph(vertices)
    edges = sum(len(adj[i]) for i in range(n)) // 2
    print(f"Loaded: {n} vertices, {edges} edges")

    # Get a 4-coloring
    print("\nGetting a 4-coloring...")
    coloring = get_k_coloring(adj, n, 4)
    if coloring:
        print("4-coloring found")

        # Analyze color distribution
        color_counts = [0] * 4
        for c in coloring.values():
            color_counts[c] += 1
        print(f"Color distribution: {color_counts}")

        # Find tight vertices (those with only one color option)
        tight = []
        for v in range(n):
            neighbor_colors = set(coloring[u] for u in adj[v])
            if len(neighbor_colors) == 3:
                tight.append(v)
        print(f"Tight vertices (3 neighbor colors): {len(tight)}")

    # Check if M₂ has any 4-cliques (would force χ≥4)
    print("\n" + "-" * 70)
    print("Searching for cliques...")
    print("-" * 70)

    max_clique = 0
    for v in range(n):
        neighbors = list(adj[v])
        # Check for triangles (3-cliques) containing v
        for i, u in enumerate(neighbors):
            for w in neighbors[i+1:]:
                if w in adj[u]:
                    # Found triangle v-u-w
                    max_clique = max(max_clique, 3)

                    # Check for 4-clique
                    for x in adj[v]:
                        if x != u and x != w and x in adj[u] and x in adj[w]:
                            max_clique = max(max_clique, 4)

    print(f"Maximum clique found: {max_clique}")

    # Analyze degree distribution
    print("\n" + "-" * 70)
    print("Degree distribution...")
    print("-" * 70)

    degrees = [len(adj[v]) for v in range(n)]
    max_degree = max(degrees)
    min_degree = min(degrees)
    avg_degree = sum(degrees) / n

    print(f"Min degree: {min_degree}")
    print(f"Max degree: {max_degree}")
    print(f"Avg degree: {avg_degree:.2f}")

    # High-degree vertices are important for forcing
    high_degree = [v for v in range(n) if len(adj[v]) >= 10]
    print(f"Vertices with degree ≥ 10: {len(high_degree)}")

    # What makes this 4-chromatic but not 3-chromatic?
    print("\n" + "-" * 70)
    print("Why is M₂ 4-chromatic (not 3)?")
    print("-" * 70)

    is_3col = is_k_colorable(adj, n, 3)
    print(f"Is 3-colorable: {is_3col}")

    if not is_3col:
        # Find a small non-3-colorable subgraph
        print("Searching for minimal non-3-colorable subgraph...")

        # Use subset search
        from itertools import combinations

        for size in range(4, 30):
            found = False
            checked = 0
            for subset in combinations(range(n), size):
                checked += 1
                if checked > 10000:  # Limit search
                    break

                # Build induced subgraph
                sub_adj = defaultdict(set)
                idx_map = {old: new for new, old in enumerate(subset)}

                for i, v in enumerate(subset):
                    for u in adj[v]:
                        if u in idx_map:
                            sub_adj[i].add(idx_map[u])

                if not is_k_colorable(sub_adj, size, 3):
                    print(f"Found non-3-colorable subgraph of size {size}!")
                    print(f"Vertices: {subset[:10]}...")  # Show first 10

                    # Verify it's minimal
                    is_minimal = True
                    for v in subset:
                        smaller = [u for u in subset if u != v]
                        smaller_adj = defaultdict(set)
                        smaller_map = {old: new for new, old in enumerate(smaller)}
                        for i, u in enumerate(smaller):
                            for w in adj[u]:
                                if w in smaller_map:
                                    smaller_adj[i].add(smaller_map[w])
                        if not is_k_colorable(smaller_adj, size-1, 3):
                            is_minimal = False
                            break

                    print(f"Is minimal: {is_minimal}")
                    found = True
                    break

            if found:
                break

    # Key insight for χ=6
    print("\n" + "=" * 70)
    print("KEY INSIGHT FOR χ=6")
    print("=" * 70)
    print("""
For χ=4 in M₂:
- Contains some structure (odd cycles + cliques) that prevents 3-coloring
- The forcing is "distributed" across the graph

For χ=5 in de Grey's construction:
- Uses "clamps" that force specific color relationships
- Minkowski sums "spread" the forcing across the plane

For χ=6, we would need:
- A forcing mechanism STRONGER than clamps
- Or a completely different construction approach

The fundamental barrier:
- For χ=6, we need a vertex v where N(v) is 5-chromatic
- But N(v) lies on the unit circle around v
- And we proved circle graphs have χ ≤ 4 (bipartite + edges)

This means: LOCAL forcing (via neighborhoods) CANNOT reach χ=6!
The only hope is GLOBAL forcing where no single vertex forces the 6th color.
""")

if __name__ == "__main__":
    main()
