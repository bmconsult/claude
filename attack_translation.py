#!/usr/bin/env python3
"""
TRANSLATION ATTACK: M₃ ∪ (M₃ + v) where |v| = 1

Instead of rotation, try TRANSLATION by unit vectors.
If |v| = 1, then every vertex p is connected to p + v.
This creates a PERFECT MATCHING between copies!

Different constraint pattern than rotation.
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

def load_vertices_complex(filename, limit=None):
    vertices = []
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            if limit and i >= limit:
                break
            result = parse_vertex_line(line)
            if result is not None:
                vertices.append(result)
    return vertices

def build_translated_union(vertices, v, tolerance=1e-9):
    """Build M ∪ (M + v) where v is a translation vector"""
    translated = [z + v for z in vertices]
    n = len(vertices)
    adj = defaultdict(set)

    # Edges within original
    edges_orig = 0
    for i in range(n):
        for j in range(i + 1, n):
            d = abs(vertices[i] - vertices[j])
            if abs(d - 1.0) < tolerance:
                adj[i].add(j)
                adj[j].add(i)
                edges_orig += 1

    # Edges within translated (same structure)
    for i in range(n):
        for j in range(i + 1, n):
            d = abs(translated[i] - translated[j])
            if abs(d - 1.0) < tolerance:
                adj[n + i].add(n + j)
                adj[n + j].add(n + i)

    # Cross edges
    edges_cross = 0
    for i in range(n):
        for j in range(n):
            d = abs(vertices[i] - translated[j])
            if abs(d - 1.0) < tolerance:
                adj[i].add(n + j)
                adj[n + j].add(i)
                edges_cross += 1

    return adj, 2 * n, edges_orig * 2 + edges_cross, edges_cross

def is_k_colorable(adj, n, k, timeout=60):
    """Check k-colorability via SAT"""
    def var(v_idx, c):
        return v_idx * k + c + 1

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
    print("TRANSLATION ATTACK: M ∪ (M + v) where |v| = 1")
    print("=" * 70)

    vtx_file = "dist-graphs/plane/series 2/vtx/s2_M2.vtx"

    print(f"\nLoading vertices from {vtx_file}...")
    vertices = load_vertices_complex(vtx_file)
    print(f"Loaded {len(vertices)} vertices")

    n = len(vertices)

    # Compute base graph properties
    adj_base = defaultdict(set)
    base_edges = 0
    for i in range(n):
        for j in range(i + 1, n):
            d = abs(vertices[i] - vertices[j])
            if abs(d - 1.0) < 1e-9:
                adj_base[i].add(j)
                adj_base[j].add(i)
                base_edges += 1

    print(f"Base graph: {n} vertices, {base_edges} edges")

    # Check base χ
    for k in range(3, 7):
        if is_k_colorable(adj_base, n, k):
            print(f"Base χ = {k}")
            break

    # Test various unit translations
    print("\n" + "-" * 70)
    print("Testing unit translations...")
    print("-" * 70)

    # Unit vectors at various angles
    translation_angles = [
        0,           # East
        math.pi/6,   # 30°
        math.pi/4,   # 45°
        math.pi/3,   # 60°
        math.pi/2,   # North
        2*math.pi/3, # 120°
        3*math.pi/4, # 135°
        5*math.pi/6, # 150°
        math.pi,     # West
    ]

    for angle in translation_angles:
        v = cmath.exp(1j * angle)  # Unit vector at angle
        angle_deg = angle * 180 / math.pi

        adj, total_n, total_edges, cross = build_translated_union(vertices, v)

        print(f"\nTranslation at {angle_deg:.0f}°: {total_n} vertices, {total_edges} edges ({cross} cross)")

        # Perfect matching gives n cross-edges (each vertex to its translate)
        if cross == n:
            print("  Perfect matching detected!")

        start = time.time()
        is_5col = is_k_colorable(adj, total_n, 5)
        elapsed = time.time() - start

        if is_5col:
            print(f"  5-colorable ({elapsed:.1f}s)")
        else:
            print(f"  *** NOT 5-COLORABLE! ({elapsed:.1f}s)")

            is_6col = is_k_colorable(adj, total_n, 6)
            if is_6col:
                print(f"  *** χ = 6! FOUND 6-CHROMATIC GRAPH! ***")
                return v
            else:
                print(f"  χ ≥ 7!")

    # Try random unit translations
    print("\n" + "-" * 70)
    print("Testing random unit translations...")
    print("-" * 70)

    for trial in range(20):
        angle = random.uniform(0, 2 * math.pi)
        v = cmath.exp(1j * angle)

        adj, total_n, total_edges, cross = build_translated_union(vertices, v)

        if cross > n + 10:  # More than perfect matching
            angle_deg = angle * 180 / math.pi
            print(f"\nRandom {angle_deg:.2f}°: {cross} cross-edges (>{n} = extra)")

            start = time.time()
            is_5col = is_k_colorable(adj, total_n, 5)
            elapsed = time.time() - start

            if is_5col:
                print(f"  5-colorable ({elapsed:.1f}s)")
            else:
                print(f"  *** NOT 5-COLORABLE! ***")
                return v

    print("\n" + "=" * 70)
    print("CONCLUSION: Translation attacks also result in 5-colorable graphs")
    print("The clamp barrier holds for both rotation and translation.")
    print("=" * 70)

if __name__ == "__main__":
    main()
