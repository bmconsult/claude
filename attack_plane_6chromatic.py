#!/usr/bin/env python3
"""
PROPER ATTACK ON χ(ℝ²) ≥ 6

The question is: Is there a rotation ψ such that M₃ ∪ ψ·M₃ is 6-chromatic in the PLANE?

This would prove χ(ℝ²) ≥ 6 (Hadwiger-Nelson lower bound improvement).

Strategy:
1. Load M₃ coordinates (32,257 vertices in Q(√2, √3))
2. Try many rotation angles ψ
3. Count unit-distance edges created between M₃ and ψ·M₃
4. For high-constraint angles, test 5-colorability via SAT
5. If UNSAT → 6-CHROMATIC PLANE GRAPH FOUND!
"""

import re
import math
import numpy as np
from collections import defaultdict
from pysat.solvers import Solver
from pysat.formula import CNF
import time

def parse_sqrt_expr(s):
    """Convert Mathematica Sqrt expressions to numerical values"""
    s = s.replace('Sqrt', 'math.sqrt')
    s = s.replace('[', '(').replace(']', ')')
    try:
        return eval(s)
    except:
        return None

def parse_vertex_line(line):
    """Parse a line like {x_expr, y_expr} into (x, y) floats"""
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

def load_vertices(filename):
    """Load vertices from a .vtx file"""
    vertices = []
    with open(filename, 'r') as f:
        for line in f:
            result = parse_vertex_line(line)
            if result:
                vertices.append(result)
    return vertices

def rotate_point(p, angle):
    """Rotate point by angle (radians)"""
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return (p[0] * cos_a - p[1] * sin_a, p[0] * sin_a + p[1] * cos_a)

def count_unit_edges(vertices1, vertices2, tolerance=1e-9):
    """Count unit-distance edges between two vertex sets"""
    count = 0
    for p1 in vertices1:
        for p2 in vertices2:
            d2 = (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2
            if abs(d2 - 1.0) < tolerance:
                count += 1
    return count

def build_combined_graph(vertices, angle, tolerance=1e-9):
    """Build M₃ ∪ ψ·M₃ and return adjacency + edge count"""
    rotated = [rotate_point(p, angle) for p in vertices]

    n = len(vertices)
    adj = defaultdict(set)

    # Edges within original M₃
    for i in range(n):
        for j in range(i + 1, n):
            d2 = (vertices[i][0] - vertices[j][0])**2 + (vertices[i][1] - vertices[j][1])**2
            if abs(d2 - 1.0) < tolerance:
                adj[i].add(j)
                adj[j].add(i)

    original_edges = sum(len(adj[i]) for i in range(n)) // 2

    # Edges within rotated ψ·M₃
    for i in range(n):
        for j in range(i + 1, n):
            d2 = (rotated[i][0] - rotated[j][0])**2 + (rotated[i][1] - rotated[j][1])**2
            if abs(d2 - 1.0) < tolerance:
                adj[n + i].add(n + j)
                adj[n + j].add(n + i)

    # Cross edges between M₃ and ψ·M₃
    cross_edges = 0
    for i in range(n):
        for j in range(n):
            d2 = (vertices[i][0] - rotated[j][0])**2 + (vertices[i][1] - rotated[j][1])**2
            if abs(d2 - 1.0) < tolerance:
                adj[i].add(n + j)
                adj[n + j].add(i)
                cross_edges += 1

    return adj, 2 * n, original_edges, cross_edges

def is_k_colorable_fast(adj, n, k, timeout=30):
    """Check if graph is k-colorable using SAT with timeout"""
    def var(v_idx, c):
        return v_idx * k + c + 1

    cnf = CNF()

    # Each vertex has at least one color
    for i in range(n):
        cnf.append([var(i, c) for c in range(k)])

    # Each vertex has at most one color
    for i in range(n):
        for c1 in range(k):
            for c2 in range(c1 + 1, k):
                cnf.append([-var(i, c1), -var(i, c2)])

    # Adjacent vertices different colors
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
    print("ATTACK ON χ(ℝ²) ≥ 6: SEARCHING FOR 6-CHROMATIC PLANE GRAPH")
    print("=" * 70)

    # Use M₂ for faster testing (865 vertices)
    # M₃ has 32,257 vertices - too slow for brute force
    vtx_file = "dist-graphs/plane/series 2/vtx/s2_M2.vtx"

    print(f"\nLoading vertices from {vtx_file}...")
    vertices = load_vertices(vtx_file)
    print(f"Loaded {len(vertices)} vertices")

    if len(vertices) == 0:
        print("ERROR: No vertices loaded!")
        return

    # Count edges in base graph
    n = len(vertices)
    base_edges = 0
    for i in range(n):
        for j in range(i + 1, n):
            d2 = (vertices[i][0] - vertices[j][0])**2 + (vertices[i][1] - vertices[j][1])**2
            if abs(d2 - 1.0) < 1e-9:
                base_edges += 1

    print(f"Base graph M₂: {n} vertices, {base_edges} edges")

    # Check base chromatic number
    print("\nChecking base graph chromatic number...")
    adj_base = defaultdict(set)
    for i in range(n):
        for j in range(i + 1, n):
            d2 = (vertices[i][0] - vertices[j][0])**2 + (vertices[i][1] - vertices[j][1])**2
            if abs(d2 - 1.0) < 1e-9:
                adj_base[i].add(j)
                adj_base[j].add(i)

    for k in range(3, 7):
        if is_k_colorable_fast(adj_base, n, k):
            print(f"  Base graph χ = {k}")
            base_chi = k
            break

    # Search rotation angles
    print("\n" + "=" * 70)
    print("SEARCHING ROTATION ANGLES")
    print("=" * 70)

    # Key angles from Voronov's construction involve 15° and 24° symmetries
    # phi0 in series 2 has order 24 (15° = π/12)
    test_angles = []

    # Fine grid search around known interesting angles
    for denom in [12, 24, 36, 48, 60, 72]:
        for numer in range(1, denom):
            if math.gcd(numer, denom) == 1:  # Primitive angles
                angle = math.pi * numer / denom
                test_angles.append((f"{numer}π/{denom}", angle))

    # Also test small perturbations of specific angles
    # The Voronov angles are computed from algebraic relations

    best_cross = 0
    best_angle = None
    high_constraint_angles = []

    print(f"\nTesting {len(test_angles)} angles...")

    for name, angle in test_angles:
        rotated = [rotate_point(p, angle) for p in vertices]

        # Quick count of cross edges
        cross = 0
        for i in range(min(100, n)):  # Sample
            for j in range(n):
                d2 = (vertices[i][0] - rotated[j][0])**2 + (vertices[i][1] - rotated[j][1])**2
                if abs(d2 - 1.0) < 1e-9:
                    cross += 1

        # Extrapolate
        estimated_cross = cross * n // 100 if n > 100 else cross

        if estimated_cross > best_cross:
            best_cross = estimated_cross
            best_angle = name

        if estimated_cross > 50:
            high_constraint_angles.append((name, angle, estimated_cross))

    print(f"\nBest angle: {best_angle} with ~{best_cross} estimated cross-edges")
    print(f"Found {len(high_constraint_angles)} high-constraint angles (>50 cross-edges)")

    # Test high-constraint angles more carefully
    print("\n" + "=" * 70)
    print("TESTING HIGH-CONSTRAINT ANGLES FOR 6-CHROMATICITY")
    print("=" * 70)

    for name, angle, est_cross in sorted(high_constraint_angles, key=lambda x: -x[2])[:10]:
        print(f"\nAngle {name} (est. {est_cross} cross-edges):")

        adj, total_n, orig_edges, actual_cross = build_combined_graph(vertices, angle)
        total_edges = orig_edges * 2 + actual_cross

        print(f"  Combined: {total_n} vertices, {total_edges} edges ({actual_cross} cross)")

        # Test 5-colorability
        start = time.time()
        is_5col = is_k_colorable_fast(adj, total_n, 5, timeout=60)
        elapsed = time.time() - start

        if is_5col:
            print(f"  5-colorable ({elapsed:.1f}s)")
        else:
            print(f"  *** NOT 5-COLORABLE! ({elapsed:.1f}s)")

            # Verify it's 6-colorable
            is_6col = is_k_colorable_fast(adj, total_n, 6, timeout=60)
            if is_6col:
                print(f"  *** 6-CHROMATIC PLANE GRAPH FOUND! ***")
                print(f"  Angle: {name} = {angle}")
                return name, angle
            else:
                print(f"  WARNING: Not 6-colorable either - checking...")

    print("\n" + "=" * 70)
    print("RESULT")
    print("=" * 70)
    print("No 6-chromatic plane graph found with M₂ rotations.")
    print("Next: Try M₃ (32,257 vertices) or different angle families.")

if __name__ == "__main__":
    main()
