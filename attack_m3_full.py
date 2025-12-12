#!/usr/bin/env python3
"""
ATTACK WITH FULL M₃ (32,257 vertices, χ=5)

Key insight: The Voronov rotations are designed for χ=5.
But what about OTHER rotations? Could any give χ=6?

This is computationally expensive but tractable.
M₃ ∪ ψ·M₃ has 64,514 vertices.
SAT for 5-coloring: 322,570 variables.
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
    """Build adjacency list for unit-distance graph"""
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
    """Build M₃ ∪ ψ·M₃"""
    rotated = [z * psi for z in vertices]
    n = len(vertices)
    adj = defaultdict(set)

    # Edges within original (copy 1)
    edges_orig = 0
    for i in range(n):
        for j in range(i + 1, n):
            d = abs(vertices[i] - vertices[j])
            if abs(d - 1.0) < tolerance:
                adj[i].add(j)
                adj[j].add(i)
                edges_orig += 1

    # Edges within rotated (copy 2)
    for i in range(n):
        for j in range(i + 1, n):
            d = abs(rotated[i] - rotated[j])
            if abs(d - 1.0) < tolerance:
                adj[n + i].add(n + j)
                adj[n + j].add(n + i)

    # Cross edges
    edges_cross = 0
    for i in range(n):
        for j in range(n):
            d = abs(vertices[i] - rotated[j])
            if abs(d - 1.0) < tolerance:
                adj[i].add(n + j)
                adj[n + j].add(i)
                edges_cross += 1

    return adj, 2 * n, edges_orig * 2 + edges_cross, edges_cross

def is_k_colorable(adj, n, k, timeout=300):
    """Check k-colorability via SAT"""
    def var(v_idx, c):
        return v_idx * k + c + 1

    cnf = CNF()

    # At least one color per vertex
    for i in range(n):
        cnf.append([var(i, c) for c in range(k)])

    # At most one color per vertex
    for i in range(n):
        for c1 in range(k):
            for c2 in range(c1 + 1, k):
                cnf.append([-var(i, c1), -var(i, c2)])

    # Adjacent vertices different
    for i in range(n):
        for j in adj[i]:
            if j > i:
                for c in range(k):
                    cnf.append([-var(i, c), -var(j, c)])

    with Solver(name='g4') as solver:
        solver.append_formula(cnf)
        return solver.solve()

def random_unit_rotation():
    """Generate random rotation (unit complex number)"""
    angle = random.uniform(0, 2 * math.pi)
    return cmath.exp(1j * angle)

def main():
    print("=" * 70)
    print("M₃ FULL ATTACK: Testing rotations for χ=6")
    print("=" * 70)

    # Load subset of M₃ for faster testing
    # Full M₃ = 32,257 vertices, too slow for multiple tests
    # Use M₂ (865 vertices) but with focus on finding 6-chromatic

    vtx_file = "dist-graphs/plane/series 2/vtx/s2_M2.vtx"

    print(f"\nPhase 1: Testing with M₂ (865 vertices)")
    print("-" * 70)

    vertices = load_vertices_complex(vtx_file)
    print(f"Loaded {len(vertices)} vertices")

    # Verify base chromatic number
    adj_base, edges_base = build_adj_list(vertices)
    print(f"Base graph: {len(vertices)} vertices, {edges_base} edges")

    for k in range(3, 7):
        if is_k_colorable(adj_base, len(vertices), k):
            print(f"Base χ = {k}")
            break

    # Try many random rotations
    print(f"\n" + "-" * 70)
    print("Testing random rotations for χ=6...")
    print("-" * 70)

    n_trials = 50
    best_cross = 0
    high_constraint = []

    for trial in range(n_trials):
        psi = random_unit_rotation()
        angle = cmath.phase(psi) * 180 / math.pi

        # Quick cross-edge count (sample)
        rotated = [z * psi for z in vertices[:100]]
        cross = 0
        for i in range(100):
            for j in range(len(vertices)):
                d = abs(vertices[i] - rotated[j] if j < 100 else vertices[i] - vertices[j] * psi)
                if abs(d - 1.0) < 1e-9:
                    cross += 1

        est_cross = cross * len(vertices) // 100

        if est_cross > best_cross:
            best_cross = est_cross
            print(f"  Trial {trial}: angle={angle:.2f}°, ~{est_cross} cross-edges")

        if est_cross > 100:
            high_constraint.append((psi, angle, est_cross))

    print(f"\nFound {len(high_constraint)} high-constraint rotations")

    # Test highest-constraint rotations
    print(f"\n" + "-" * 70)
    print("Testing high-constraint rotations for 5-colorability...")
    print("-" * 70)

    for psi, angle, est_cross in sorted(high_constraint, key=lambda x: -x[2])[:10]:
        adj, total_n, total_edges, cross = build_rotated_union(vertices, psi)
        print(f"\nAngle {angle:.2f}°: {total_n} vertices, {total_edges} edges ({cross} cross)")

        start = time.time()
        is_5col = is_k_colorable(adj, total_n, 5)
        elapsed = time.time() - start

        if is_5col:
            print(f"  5-colorable ({elapsed:.1f}s)")
        else:
            print(f"  *** NOT 5-COLORABLE! ***")

            is_6col = is_k_colorable(adj, total_n, 6)
            if is_6col:
                print(f"  *** χ = 6! FOUND 6-CHROMATIC GRAPH! ***")
                print(f"  Rotation: ψ = e^(i*{angle*math.pi/180})")
                return psi, angle
            else:
                print(f"  χ ≥ 7! Checking...")

    # Try algebraically special angles
    print(f"\n" + "-" * 70)
    print("Testing algebraically special angles...")
    print("-" * 70)

    special_angles = [
        math.pi / 12,   # 15°
        math.pi / 10,   # 18° (golden ratio related)
        math.pi / 8,    # 22.5°
        math.pi / 6,    # 30°
        math.pi / 5,    # 36° (golden ratio)
        math.pi / 4,    # 45°
        2 * math.pi / 5, # 72° (golden ratio)
        math.atan(math.sqrt(3)),  # arctan(√3) = 60°
        math.atan(math.sqrt(2)),  # arctan(√2) ≈ 54.7°
        math.atan(1 + math.sqrt(2)), # Silver ratio angle
    ]

    for angle in special_angles:
        psi = cmath.exp(1j * angle)
        adj, total_n, total_edges, cross = build_rotated_union(vertices, psi)

        print(f"\nAngle {angle*180/math.pi:.2f}°: {total_n} vertices, {total_edges} edges ({cross} cross)")

        if cross == 0:
            print("  No cross edges - skip")
            continue

        start = time.time()
        is_5col = is_k_colorable(adj, total_n, 5)
        elapsed = time.time() - start

        if is_5col:
            print(f"  5-colorable ({elapsed:.1f}s)")
        else:
            print(f"  *** NOT 5-COLORABLE! ***")
            return psi, angle

    print("\n" + "=" * 70)
    print("CONCLUSION: No 6-chromatic graph found with M₂ rotations")
    print("The clamp barrier appears to hold for this construction.")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Try full M₃ (32,257 vertices) - expensive but might differ")
    print("2. Try different construction (not rotation-based)")
    print("3. Try hypergraph constraints (Fiscus approach)")

if __name__ == "__main__":
    main()
