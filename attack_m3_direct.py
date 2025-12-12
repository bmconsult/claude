#!/usr/bin/env python3
"""
DIRECT M₃ ROTATION ATTACK

Use actual M₃ coordinates (32,257 vertices, χ=5 base).
Test if NON-Voronov rotations give χ>5.

Since M₃ is large, use a subset that is still 5-chromatic (if possible).
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

def build_adj_list(vertices, tolerance=1e-9):
    n = len(vertices)
    adj = defaultdict(set)
    edge_count = 0
    for i in range(n):
        for j in range(i + 1, n):
            d = abs(vertices[i] - vertices[j])
            if abs(d - 1.0) < tolerance:
                adj[i].add(j)
                adj[j].add(i)
                edge_count += 1
    return adj, edge_count

def build_rotated_union(vertices, psi, tolerance=1e-9):
    rotated = [z * psi for z in vertices]
    n = len(vertices)
    adj = defaultdict(set)

    # Within original
    for i in range(n):
        for j in range(i + 1, n):
            d = abs(vertices[i] - vertices[j])
            if abs(d - 1.0) < tolerance:
                adj[i].add(j)
                adj[j].add(i)

    # Within rotated
    for i in range(n):
        for j in range(i + 1, n):
            d = abs(rotated[i] - rotated[j])
            if abs(d - 1.0) < tolerance:
                adj[n + i].add(n + j)
                adj[n + j].add(n + i)

    # Cross edges
    cross = 0
    for i in range(n):
        for j in range(n):
            d = abs(vertices[i] - rotated[j])
            if abs(d - 1.0) < tolerance:
                adj[i].add(n + j)
                adj[n + j].add(i)
                cross += 1

    return adj, 2 * n, cross

def is_k_colorable(adj, n, k):
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
    print("DIRECT M₃ ROTATION ATTACK")
    print("=" * 70)

    vtx_file = "dist-graphs/plane/series 2/vtx/s2_M3.vtx"

    # Start with subset to test feasibility
    subset_sizes = [1000, 2000, 5000]

    for subset_size in subset_sizes:
        print(f"\n{'=' * 70}")
        print(f"Testing with {subset_size} vertices from M₃")
        print("=" * 70)

        print(f"\nLoading first {subset_size} vertices...")
        vertices = load_vertices_complex(vtx_file, limit=subset_size)
        n = len(vertices)
        print(f"Loaded {n} vertices")

        # Check base chromatic number
        print("Computing base graph edges...")
        start = time.time()
        adj_base, edges_base = build_adj_list(vertices)
        elapsed = time.time() - start
        print(f"Base: {n} vertices, {edges_base} edges ({elapsed:.1f}s)")

        print("Checking base chromatic number...")
        for k in range(3, 7):
            if is_k_colorable(adj_base, n, k):
                print(f"Base subset χ = {k}")
                base_chi = k
                break

        if base_chi < 5:
            print(f"Subset is only {base_chi}-chromatic, need larger subset")
            continue

        # Try random rotations
        print("\n" + "-" * 70)
        print("Testing random rotations...")
        print("-" * 70)

        for trial in range(5):
            angle = random.uniform(0, 2 * math.pi)
            psi = cmath.exp(1j * angle)
            angle_deg = angle * 180 / math.pi

            print(f"\nRotation {angle_deg:.2f}°:")

            start = time.time()
            adj, total_n, cross = build_rotated_union(vertices, psi)
            edge_time = time.time() - start
            total_edges = sum(len(adj[i]) for i in range(total_n)) // 2

            print(f"  {total_n} vertices, {total_edges} edges, {cross} cross ({edge_time:.1f}s)")

            if cross == 0:
                print("  No cross edges, skip")
                continue

            start = time.time()
            is_5col = is_k_colorable(adj, total_n, 5)
            sat_time = time.time() - start

            if is_5col:
                print(f"  5-colorable ({sat_time:.1f}s)")
            else:
                print(f"  *** NOT 5-COLORABLE! ({sat_time:.1f}s)")
                is_6col = is_k_colorable(adj, total_n, 6)
                if is_6col:
                    print(f"  *** χ = 6! FOUND 6-CHROMATIC! ***")
                    return angle
                else:
                    print(f"  χ ≥ 7!")
                    return angle

    print("\n" + "=" * 70)
    print("No 6-chromatic found with tested M₃ subsets")
    print("=" * 70)

if __name__ == "__main__":
    main()
