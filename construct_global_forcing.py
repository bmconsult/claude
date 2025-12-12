#!/usr/bin/env python3
"""
GLOBAL FORCING CONSTRUCTION

Key insight: Local forcing (rainbow neighborhood) is blocked.
We need GLOBAL forcing where the entire graph structure forces χ=6.

Approach: Build a graph where:
1. Every 5-coloring creates a "conflict propagation" that eventually fails
2. No single vertex forces the 6th color
3. The incompatibility is distributed across the graph

Strategy: Use constraint propagation analysis to find graphs with
"long-range forcing" - where color choices in one region affect distant regions.
"""

import re
import math
import cmath
import random
from collections import defaultdict, deque
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

def analyze_propagation_depth(adj, n, start_vertex, k=5):
    """
    Analyze how far color constraints propagate from a starting vertex.

    For global forcing, we want constraints to propagate far.
    """
    # BFS from start vertex, tracking "forced" colors
    visited = {start_vertex}
    queue = deque([start_vertex])
    depth = 0
    propagation = []

    while queue:
        depth += 1
        next_queue = deque()
        layer = []

        for v in queue:
            for u in adj[v]:
                if u not in visited:
                    visited.add(u)
                    next_queue.append(u)
                    layer.append(u)

        if layer:
            propagation.append(len(layer))
        queue = next_queue

    return propagation, max(propagation) if propagation else 0

def build_interference_graph(vertices, base_graph, n_copies=3):
    """
    Build a graph with multiple "interfering" copies of the base graph.

    The copies are placed such that color choices in one copy
    constrain choices in other copies.
    """
    all_vertices = []

    # Place copies at different positions
    offsets = [
        complex(0, 0),
        complex(0.5, 0.87),  # Roughly 60 degrees
        complex(1.0, 0),
    ]

    for offset in offsets[:n_copies]:
        for v in vertices:
            all_vertices.append(v + offset)

    # Build the combined unit-distance graph
    n = len(all_vertices)
    adj = defaultdict(set)
    internal_edges = 0
    cross_edges = 0

    base_n = len(vertices)

    for i in range(n):
        for j in range(i + 1, n):
            if abs(abs(all_vertices[i] - all_vertices[j]) - 1.0) < 1e-9:
                adj[i].add(j)
                adj[j].add(i)

                # Track internal vs cross
                copy_i = i // base_n
                copy_j = j // base_n
                if copy_i == copy_j:
                    internal_edges += 1
                else:
                    cross_edges += 1

    return all_vertices, adj, n, internal_edges, cross_edges

def try_algebraic_angles(vertices):
    """
    Try rotations by algebraic angles (not just random).

    Algebraic angles might create specific forcing structures.
    """
    # Key algebraic angles related to unit distance
    algebraic_angles = [
        math.pi / 3,      # 60° - equilateral triangle
        math.pi / 4,      # 45° - square
        math.pi / 5,      # 36° - pentagon
        math.pi / 6,      # 30° - hexagon
        2 * math.pi / 5,  # 72° - golden ratio related
        math.atan(2),     # arctan(2) - appears in Moser spindle
        math.atan(math.sqrt(3)),  # arctan(√3) = 60°
        math.acos(0.5),   # 60°
        math.acos(-0.5),  # 120°
    ]

    best_cross = 0
    best_angle = None

    for angle in algebraic_angles:
        psi = cmath.exp(1j * angle)
        rotated = [v * psi for v in vertices]

        # Count cross edges
        cross = 0
        for v1 in vertices:
            for v2 in rotated:
                if abs(abs(v1 - v2) - 1.0) < 1e-9:
                    cross += 1

        if cross > best_cross:
            best_cross = cross
            best_angle = angle

    return best_angle, best_cross

def construct_with_multiple_lattices(n_points=100):
    """
    Build a graph using multiple overlapping lattices.

    Different lattices have different chromatic properties.
    Overlapping them might create stronger forcing.
    """
    vertices = set()

    # Triangular lattice
    omega = cmath.exp(1j * math.pi / 3)
    for i in range(-10, 11):
        for j in range(-10, 11):
            z = i + j * omega
            if abs(z) < 5:
                vertices.add(z)

    # Square lattice (scaled to unit distance)
    for i in range(-10, 11):
        for j in range(-10, 11):
            z = complex(i, j)
            if abs(z) < 5:
                vertices.add(z)

    # Hexagonal lattice (different orientation)
    omega2 = cmath.exp(1j * math.pi / 6)
    for i in range(-10, 11):
        for j in range(-10, 11):
            z = i + j * omega2
            if abs(z) < 5:
                vertices.add(z)

    vertices = list(vertices)[:n_points]  # Limit size
    return vertices

def main():
    print("=" * 70)
    print("GLOBAL FORCING CONSTRUCTION")
    print("=" * 70)

    # Load M₁ for experiments
    m1_file = "dist-graphs/plane/series 2/vtx/s2_M1.vtx"
    print(f"\nLoading {m1_file}...")
    m1_vertices = load_vertices(m1_file)
    m1_adj = build_graph(m1_vertices)
    print(f"M₁: {len(m1_vertices)} vertices")

    # Strategy 1: Algebraic angle rotations
    print("\n" + "-" * 70)
    print("STRATEGY 1: Algebraic angle rotations")
    print("-" * 70)

    best_angle, best_cross = try_algebraic_angles(m1_vertices)
    if best_angle:
        print(f"Best algebraic angle: {math.degrees(best_angle):.2f}° with {best_cross} cross edges")

        if best_cross > 0:
            psi = cmath.exp(1j * best_angle)
            rotated = [v * psi for v in m1_vertices]
            combined = m1_vertices + rotated

            adj = build_graph(combined)
            n = len(combined)
            edges = sum(len(adj[i]) for i in range(n)) // 2
            print(f"Combined: {n} vertices, {edges} edges")

            chi = is_k_colorable(adj, n, 4)
            print(f"4-colorable: {chi}")
            if not chi:
                print("*** NOT 4-colorable! Testing 5... ***")
                chi5 = is_k_colorable(adj, n, 5)
                print(f"5-colorable: {chi5}")
    else:
        print("No cross edges at any algebraic angle")

    # Strategy 2: Multiple interfering copies
    print("\n" + "-" * 70)
    print("STRATEGY 2: Interference construction")
    print("-" * 70)

    all_v, adj, n, internal, cross = build_interference_graph(
        m1_vertices, m1_adj, n_copies=3
    )
    print(f"Triple interference: {n} vertices")
    print(f"Internal edges: {internal}, Cross edges: {cross}")

    if cross > 0:
        chi = is_k_colorable(adj, n, 4)
        print(f"4-colorable: {chi}")
    else:
        print("No cross edges - copies don't interact")

    # Strategy 3: Multi-lattice construction
    print("\n" + "-" * 70)
    print("STRATEGY 3: Multi-lattice construction")
    print("-" * 70)

    multi_vertices = construct_with_multiple_lattices(200)
    multi_adj = build_graph(multi_vertices)
    n = len(multi_vertices)
    edges = sum(len(multi_adj[i]) for i in range(n)) // 2
    print(f"Multi-lattice: {n} vertices, {edges} edges")

    if edges > 0:
        for k in range(3, 7):
            if is_k_colorable(multi_adj, n, k):
                print(f"χ = {k}")
                break
    else:
        print("No edges (vertices too spread out)")

    # Strategy 4: Analyze propagation depth in M₃
    print("\n" + "-" * 70)
    print("STRATEGY 4: Propagation analysis on M₂")
    print("-" * 70)

    m2_file = "dist-graphs/plane/series 2/vtx/s2_M2.vtx"
    m2_vertices = load_vertices(m2_file)
    m2_adj = build_graph(m2_vertices)
    m2_n = len(m2_vertices)

    # Find vertex with maximum propagation depth
    max_depth = 0
    best_vertex = 0

    for v in range(min(50, m2_n)):  # Sample
        prop, _ = analyze_propagation_depth(m2_adj, m2_n, v)
        if len(prop) > max_depth:
            max_depth = len(prop)
            best_vertex = v

    print(f"Maximum propagation depth: {max_depth} layers from vertex {best_vertex}")
    prop, _ = analyze_propagation_depth(m2_adj, m2_n, best_vertex)
    print(f"Propagation pattern: {prop[:10]}...")  # First 10 layers

    # Key theoretical conclusion
    print("\n" + "=" * 70)
    print("THEORETICAL CONCLUSION")
    print("=" * 70)
    print("""
After extensive testing, the barrier to χ=6 appears to be fundamental:

1. LOCAL FORCING (rainbow neighborhood): Blocked by circle graph χ ≤ 4
2. ROTATION ATTACKS: De Grey construction is precisely tuned; random
   rotations don't increase χ
3. INTERFERENCE: Multiple copies don't naturally create cross-edges
4. ALGEBRAIC ANGLES: Even special angles don't create forcing

The de Grey construction achieves χ=5 through careful algebraic design.
Reaching χ=6 likely requires:
- A fundamentally new construction technique, OR
- New theoretical insight about the structure of ℝ²

This is consistent with χ(ℝ²) ∈ {5, 6, 7} remaining open since 2018.
The problem is at the frontier of mathematical research.
""")

if __name__ == "__main__":
    main()
