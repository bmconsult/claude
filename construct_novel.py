#!/usr/bin/env python3
"""
NOVEL CONSTRUCTION ATTEMPT

Key insight from analysis:
1. Rainbow neighborhood blocked (circle graphs bipartite)
2. Minkowski iteration saturates at χ=5
3. Standard rotations preserve χ=5

New approach: Use the ACTUAL chromatic forcing structure of de Grey's graph.
The 517-vertex graph is 5-chromatic because of GLOBAL forcing, not local.

Strategy: Find the "core" forcing structure and try to amplify it.
"""

import re
import math
import cmath
import random
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

def chromatic_number(adj, n, max_k=7):
    for k in range(1, max_k + 1):
        if is_k_colorable(adj, n, k):
            return k
    return max_k + 1

def is_k_colorable(adj, n, k, timeout=30):
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

def find_critical_subgraph(adj, n, target_chi=5):
    """
    Find a vertex-critical subgraph: removing ANY vertex decreases χ.
    This is the "core" of the chromatic forcing.
    """
    vertices = list(range(n))

    # Greedy removal: keep removing vertices that don't decrease χ
    while True:
        removed_any = False
        for v in vertices[:]:
            # Try removing v
            remaining = [u for u in vertices if u != v]
            if len(remaining) < 3:
                break

            # Build subgraph
            sub_adj = defaultdict(set)
            idx_map = {old: new for new, old in enumerate(remaining)}
            for u in remaining:
                for w in adj[u]:
                    if w in idx_map:
                        sub_adj[idx_map[u]].add(idx_map[w])

            chi = chromatic_number(sub_adj, len(remaining))
            if chi >= target_chi:
                # Can remove v without decreasing χ
                vertices.remove(v)
                removed_any = True
                break

        if not removed_any:
            break

    return vertices

def triple_product_construction(vertices):
    """
    Try G × G × G type construction.

    For unit-distance, we create vertices (v1, v2, v3) where
    v1, v2, v3 are from the original graph, and edges exist
    when the "distance" in the product is 1.

    This is NOT standard tensor product - we need geometric meaning.
    """
    # For unit-distance, let's try: sum of positions
    # New vertex set: v1 + v2 + v3 for all v1, v2, v3
    # But this explodes in size

    # Smaller variant: v1 + v2 for v1, v2 from DIFFERENT copies
    n = len(vertices)

    # Place first copy at origin, second rotated by some angle
    # This is essentially Minkowski sum - we've shown it saturates

    return None

def spiral_construction(base_vertices, n_layers=3):
    """
    Build a spiral of unit-distance connections.

    Idea: the plane's 7-coloring uses hexagonal tiling.
    A spiral might create interference patterns that force more colors.
    """
    all_vertices = list(base_vertices)

    for layer in range(n_layers):
        # Add vertices in a spiral pattern
        # Each new vertex is at unit distance from some existing vertex

        for v in base_vertices:
            # Add 6 neighbors in hexagonal pattern (if not already present)
            for k in range(6):
                angle = k * math.pi / 3 + layer * math.pi / 18  # Slight twist per layer
                new_v = v + cmath.exp(1j * angle)

                # Check if this vertex is "new enough"
                is_new = all(abs(new_v - existing) > 0.01 for existing in all_vertices)
                if is_new:
                    all_vertices.append(new_v)

    return all_vertices

def pentagonal_construction():
    """
    Try using pentagons instead of hexagons.

    The hexagonal tiling is 3-colorable (hence 7-colorable when
    we account for the different orientations).

    Pentagons don't tile the plane, but pentagonal GRAPHS might
    have different chromatic properties.
    """
    # Regular pentagon with side length 1
    pentagon = [cmath.exp(2j * math.pi * k / 5) for k in range(5)]

    # Scale so that side length = 1
    scale = 1 / abs(pentagon[1] - pentagon[0])
    pentagon = [p * scale for p in pentagon]

    # This pentagon has side ≈ 1.176, not 1
    # Let me compute the correct scaling

    # For regular pentagon with unit side length:
    # Radius R = 1 / (2 * sin(π/5)) ≈ 0.851
    R = 1 / (2 * math.sin(math.pi / 5))
    pentagon = [R * cmath.exp(2j * math.pi * k / 5) for k in range(5)]

    # Verify side length
    side = abs(pentagon[1] - pentagon[0])
    print(f"Pentagon side length: {side:.6f}")

    return pentagon

def main():
    print("=" * 70)
    print("NOVEL CONSTRUCTION ATTEMPTS")
    print("=" * 70)

    # Load M₂ (865 vertices, χ=4)
    vtx_file = "dist-graphs/plane/series 2/vtx/s2_M2.vtx"

    print(f"\nLoading {vtx_file}...")
    vertices = load_vertices(vtx_file)
    n = len(vertices)
    print(f"Loaded {n} vertices")

    adj = build_graph(vertices)
    edges = sum(len(adj[i]) for i in range(n)) // 2
    print(f"Graph: {n} vertices, {edges} edges")

    # Verify χ = 4
    print("\nVerifying χ = 4...")
    chi = chromatic_number(adj, n)
    print(f"χ = {chi}")

    # Strategy 1: Find critical core
    print("\n" + "-" * 70)
    print("STRATEGY 1: Find vertex-critical core")
    print("-" * 70)
    print("(The 517-vertex graph IS already vertex-critical)")

    # Strategy 2: Pentagon-based construction
    print("\n" + "-" * 70)
    print("STRATEGY 2: Pentagon construction")
    print("-" * 70)

    pentagon = pentagonal_construction()
    adj_pent = build_graph(pentagon)
    edges_pent = sum(len(adj_pent[i]) for i in range(5)) // 2
    chi_pent = chromatic_number(adj_pent, 5)
    print(f"Pentagon: 5 vertices, {edges_pent} edges, χ={chi_pent}")

    # Strategy 3: Spiral construction
    print("\n" + "-" * 70)
    print("STRATEGY 3: Spiral construction")
    print("-" * 70)

    # Start with a small seed
    seed = [complex(0, 0), complex(1, 0), complex(0.5, math.sqrt(3)/2)]
    spiral = spiral_construction(seed, n_layers=4)
    print(f"Spiral: {len(spiral)} vertices")

    adj_spiral = build_graph(spiral)
    edges_spiral = sum(len(adj_spiral[i]) for i in range(len(spiral))) // 2
    print(f"Spiral graph: {len(spiral)} vertices, {edges_spiral} edges")

    chi_spiral = chromatic_number(adj_spiral, len(spiral))
    print(f"χ(spiral) = {chi_spiral}")

    # Strategy 4: Combine 517 with its reflection
    print("\n" + "-" * 70)
    print("STRATEGY 4: 517 + reflection")
    print("-" * 70)

    # Reflect across x-axis
    reflected = [complex(v.real, -v.imag) for v in vertices]
    combined = vertices + reflected

    # Remove near-duplicates
    unique = []
    for v in combined:
        if all(abs(v - u) > 1e-6 for u in unique):
            unique.append(v)

    print(f"Combined (unique): {len(unique)} vertices")

    adj_comb = build_graph(unique)
    edges_comb = sum(len(adj_comb[i]) for i in range(len(unique))) // 2
    print(f"Edges: {edges_comb}")

    # Cross edges between original and reflected
    cross = 0
    for i in range(n):
        for j in range(n, len(unique)):
            if j in adj_comb.get(i, set()):
                cross += 1
    print(f"Cross edges: {cross}")

    if cross > 0:
        print("Testing chromatic number...")
        start = time.time()
        chi_comb = chromatic_number(adj_comb, len(unique))
        elapsed = time.time() - start
        print(f"χ(combined) = {chi_comb} ({elapsed:.1f}s)")
    else:
        print("No cross edges - disjoint union has χ=5")

    # Strategy 5: Multiple scaled copies
    print("\n" + "-" * 70)
    print("STRATEGY 5: Multiple scaled copies at golden ratio")
    print("-" * 70)

    phi = (1 + math.sqrt(5)) / 2  # Golden ratio

    scaled = [v * phi for v in vertices]
    combined2 = vertices + scaled

    # Remove near-duplicates
    unique2 = []
    for v in combined2:
        if all(abs(v - u) > 1e-6 for u in unique2):
            unique2.append(v)

    print(f"Combined with φ-scaled: {len(unique2)} vertices")

    adj_comb2 = build_graph(unique2)
    edges_comb2 = sum(len(adj_comb2[i]) for i in range(len(unique2))) // 2

    cross2 = 0
    for i in range(n):
        for j in range(n, len(unique2)):
            if j in adj_comb2.get(i, set()):
                cross2 += 1
    print(f"Edges: {edges_comb2}, Cross: {cross2}")

    if cross2 > 0:
        print("Testing chromatic number...")
        start = time.time()
        chi_comb2 = chromatic_number(adj_comb2, len(unique2))
        elapsed = time.time() - start
        print(f"χ(φ-combined) = {chi_comb2} ({elapsed:.1f}s)")

    print("\n" + "=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)

if __name__ == "__main__":
    main()
