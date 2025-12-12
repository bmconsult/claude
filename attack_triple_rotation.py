#!/usr/bin/env python3
"""
TRIPLE ROTATION ATTACK: M₃ ∪ ψ₁·M₃ ∪ ψ₂·M₃

The 5-chromatic graphs use TWO copies with one rotation.
Maybe THREE copies can force 6 colors!

This is a genuine attempt at χ(ℝ²) ≥ 6.
"""

import re
import math
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
    return (x, y)

def load_vertices(filename, limit=None):
    vertices = []
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            if limit and i >= limit:
                break
            result = parse_vertex_line(line)
            if result:
                vertices.append(result)
    return vertices

def rotate_point(p, angle):
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return (p[0] * cos_a - p[1] * sin_a, p[0] * sin_a + p[1] * cos_a)

def build_triple_graph(vertices, angle1, angle2, tolerance=1e-9):
    """Build M ∪ ψ₁·M ∪ ψ₂·M"""
    rot1 = [rotate_point(p, angle1) for p in vertices]
    rot2 = [rotate_point(p, angle2) for p in vertices]

    n = len(vertices)
    adj = defaultdict(set)

    all_sets = [vertices, rot1, rot2]

    edges_within = 0
    edges_cross = 0

    # Within each copy
    for offset, vset in enumerate(all_sets):
        for i in range(n):
            for j in range(i + 1, n):
                d2 = (vset[i][0] - vset[j][0])**2 + (vset[i][1] - vset[j][1])**2
                if abs(d2 - 1.0) < tolerance:
                    adj[offset * n + i].add(offset * n + j)
                    adj[offset * n + j].add(offset * n + i)
                    edges_within += 1

    # Between copies
    for o1, set1 in enumerate(all_sets):
        for o2, set2 in enumerate(all_sets):
            if o1 >= o2:
                continue
            for i in range(n):
                for j in range(n):
                    d2 = (set1[i][0] - set2[j][0])**2 + (set1[i][1] - set2[j][1])**2
                    if abs(d2 - 1.0) < tolerance:
                        adj[o1 * n + i].add(o2 * n + j)
                        adj[o2 * n + j].add(o1 * n + i)
                        edges_cross += 1

    return adj, 3 * n, edges_within, edges_cross

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
    print("TRIPLE ROTATION ATTACK: M ∪ ψ₁·M ∪ ψ₂·M")
    print("=" * 70)

    # Use smaller subset of M₃ for testing
    vtx_file = "dist-graphs/plane/series 2/vtx/s2_M3.vtx"

    print(f"\nLoading vertices from {vtx_file} (first 1000)...")
    vertices = load_vertices(vtx_file, limit=1000)
    print(f"Loaded {len(vertices)} vertices")

    if len(vertices) < 100:
        print("ERROR: Not enough vertices!")
        return

    # Check base chromatic number
    n = len(vertices)
    adj_base = defaultdict(set)
    for i in range(n):
        for j in range(i + 1, n):
            d2 = (vertices[i][0] - vertices[j][0])**2 + (vertices[i][1] - vertices[j][1])**2
            if abs(d2 - 1.0) < 1e-9:
                adj_base[i].add(j)
                adj_base[j].add(i)

    print(f"Base: {n} vertices, {sum(len(adj_base[i]) for i in range(n))//2} edges")

    for k in range(3, 7):
        if is_k_colorable(adj_base, n, k):
            print(f"Base χ = {k}")
            base_chi = k
            break

    # The Voronov angles for series 2
    # phi0 = exp(2πi/24) corresponds to 15° = π/12
    phi0_angle = math.pi / 12

    # Key angles that create 5-chromatic with TWO copies
    # Let's try THREE copies with pairs of these

    print("\n" + "=" * 70)
    print("TESTING TRIPLE ROTATIONS")
    print("=" * 70)

    # Test angle pairs
    angle_pairs = [
        (phi0_angle, 2 * phi0_angle),
        (phi0_angle, 5 * phi0_angle),
        (phi0_angle, 7 * phi0_angle),
        (2 * phi0_angle, 5 * phi0_angle),
        (2 * phi0_angle, 7 * phi0_angle),
        (math.pi/6, math.pi/3),
        (math.pi/6, math.pi/4),
        (math.pi/4, math.pi/3),
    ]

    for angle1, angle2 in angle_pairs:
        name = f"({angle1/math.pi:.3f}π, {angle2/math.pi:.3f}π)"
        print(f"\nAngles {name}:")

        adj, total_n, within, cross = build_triple_graph(vertices, angle1, angle2)
        total_edges = within + cross

        print(f"  Combined: {total_n} vertices, {total_edges} edges ({cross} cross)")

        # Test colorability
        start = time.time()

        for k in [4, 5, 6]:
            result = is_k_colorable(adj, total_n, k)
            elapsed = time.time() - start

            if result:
                print(f"  χ ≤ {k} ({elapsed:.1f}s)")
                if k == 4:
                    print("  Only 4-colorable - not interesting")
                elif k == 5:
                    print("  5-colorable - matches existing construction")
                break
            else:
                if k == 5:
                    print(f"  *** NOT 5-colorable! Testing 6...")
                elif k == 6:
                    print(f"  *** NOT 6-colorable! Checking 7...")
        else:
            print(f"  *** χ ≥ 7! MAJOR DISCOVERY!")
            return angle1, angle2

    print("\n" + "=" * 70)
    print("No 6-chromatic found with these triple rotations.")
    print("Need larger vertex set or different angle combinations.")
    print("=" * 70)

if __name__ == "__main__":
    main()
