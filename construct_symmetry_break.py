#!/usr/bin/env python3
"""
SYMMETRY-BREAKING CONSTRUCTION

Key insight: Previous attempts failed because:
1. Reflection gives 0 cross edges (M₂ is symmetric)
2. Scaling gives 0 cross edges (wrong distance scale)
3. Pure rotation with Voronov angles gives χ=5 (by design)

New approach: BREAK SYMMETRY by combining:
- Rotation by non-Voronov angle
- Translation by non-trivial vector
- Multiple copies at different positions

Goal: Maximize cross-edges between copies to force higher χ.
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

def build_combined_graph(vertices_list, tol=1e-9):
    """Build graph from multiple vertex sets, tracking cross-edges."""
    all_vertices = []
    set_indices = []  # Which set each vertex came from

    for i, verts in enumerate(vertices_list):
        for v in verts:
            all_vertices.append(v)
            set_indices.append(i)

    n = len(all_vertices)
    adj = defaultdict(set)
    internal_edges = 0
    cross_edges = 0

    for i in range(n):
        for j in range(i + 1, n):
            if abs(abs(all_vertices[i] - all_vertices[j]) - 1.0) < tol:
                adj[i].add(j)
                adj[j].add(i)
                if set_indices[i] == set_indices[j]:
                    internal_edges += 1
                else:
                    cross_edges += 1

    return adj, n, internal_edges, cross_edges

def chromatic_number(adj, n, max_k=7, timeout=60):
    for k in range(1, max_k + 1):
        if is_k_colorable(adj, n, k):
            return k
    return max_k + 1

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

def transform_vertices(vertices, rotation_angle, translation):
    """Apply rotation then translation to vertex set."""
    psi = cmath.exp(1j * rotation_angle)
    return [v * psi + translation for v in vertices]

def search_best_transform(vertices, n_trials=50):
    """Search for transformation that maximizes cross-edges."""
    best_cross = 0
    best_params = None
    best_adj = None

    for trial in range(n_trials):
        # Random rotation and translation
        angle = random.uniform(0, 2 * math.pi)
        # Translation should be "small" to create cross-edges
        tx = random.uniform(-0.5, 0.5)
        ty = random.uniform(-0.5, 0.5)
        translation = complex(tx, ty)

        transformed = transform_vertices(vertices, angle, translation)
        adj, n, internal, cross = build_combined_graph([vertices, transformed])

        if cross > best_cross:
            best_cross = cross
            best_params = (angle, translation)
            best_adj = (adj, n)
            print(f"  Trial {trial}: angle={math.degrees(angle):.1f}°, "
                  f"trans=({tx:.3f},{ty:.3f}), cross={cross}")

    return best_params, best_adj, best_cross

def exhaustive_cross_search(vertices, angle_steps=36, trans_steps=10):
    """More systematic search for maximum cross-edges."""
    best_cross = 0
    best_params = None

    # Search over angle grid
    for a_idx in range(angle_steps):
        angle = 2 * math.pi * a_idx / angle_steps

        # Search over translation grid
        for tx_idx in range(trans_steps):
            for ty_idx in range(trans_steps):
                tx = -0.5 + tx_idx / trans_steps
                ty = -0.5 + ty_idx / trans_steps
                translation = complex(tx, ty)

                transformed = transform_vertices(vertices, angle, translation)
                adj, n, internal, cross = build_combined_graph([vertices, transformed])

                if cross > best_cross:
                    best_cross = cross
                    best_params = (angle, translation)
                    print(f"  Found: angle={math.degrees(angle):.1f}°, "
                          f"trans=({tx:.3f},{ty:.3f}), cross={cross}")

    return best_params, best_cross

def main():
    print("=" * 70)
    print("SYMMETRY-BREAKING CONSTRUCTION")
    print("=" * 70)

    # Load M₂
    vtx_file = "dist-graphs/plane/series 2/vtx/s2_M2.vtx"
    print(f"\nLoading {vtx_file}...")
    vertices = load_vertices(vtx_file)
    n = len(vertices)
    print(f"Loaded {n} vertices")

    # Strategy 1: Random search for best transformation
    print("\n" + "-" * 70)
    print("STRATEGY 1: Random transformation search")
    print("-" * 70)

    best_params, best_adj, best_cross = search_best_transform(vertices, n_trials=100)

    if best_cross > 0:
        angle, trans = best_params
        adj, total_n = best_adj
        print(f"\nBest found: {best_cross} cross edges")
        print(f"Parameters: angle={math.degrees(angle):.2f}°, trans=({trans.real:.4f},{trans.imag:.4f})")

        print("Computing chromatic number...")
        start = time.time()
        chi = chromatic_number(adj, total_n)
        elapsed = time.time() - start
        print(f"χ = {chi} ({elapsed:.1f}s)")

        if chi >= 5:
            print(f"*** FOUND χ = {chi}! ***")
    else:
        print("No cross edges found")

    # Strategy 2: Triple combination
    print("\n" + "-" * 70)
    print("STRATEGY 2: Three copies with different transforms")
    print("-" * 70)

    # Three copies at different rotations/translations
    transforms = [
        (0, complex(0, 0)),                    # Original
        (math.pi / 7, complex(0.3, 0.1)),      # Slightly rotated + shifted
        (math.pi / 5, complex(-0.2, 0.4)),     # Another rotation + shift
    ]

    vertex_sets = [vertices]
    for angle, trans in transforms[1:]:
        vertex_sets.append(transform_vertices(vertices, angle, trans))

    adj, total_n, internal, cross = build_combined_graph(vertex_sets)
    total_edges = internal + cross

    print(f"Triple combination: {total_n} vertices")
    print(f"Internal edges: {internal}, Cross edges: {cross}")
    print(f"Total edges: {total_edges}")

    if cross > 0:
        print("Computing chromatic number...")
        start = time.time()
        chi = chromatic_number(adj, total_n)
        elapsed = time.time() - start
        print(f"χ = {chi} ({elapsed:.1f}s)")

    # Strategy 3: Exhausitive grid search on M₁ (smaller, faster)
    print("\n" + "-" * 70)
    print("STRATEGY 3: Exhaustive search on M₁")
    print("-" * 70)

    m1_file = "dist-graphs/plane/series 2/vtx/s2_M1.vtx"
    m1_vertices = load_vertices(m1_file)
    print(f"M₁: {len(m1_vertices)} vertices")

    best_params, best_cross = exhaustive_cross_search(
        m1_vertices, angle_steps=72, trans_steps=20
    )

    if best_params and best_cross > 0:
        angle, trans = best_params
        transformed = transform_vertices(m1_vertices, angle, trans)
        adj, total_n, internal, cross = build_combined_graph([m1_vertices, transformed])

        print(f"\nBest M₁ combination: {total_n} vertices, {cross} cross edges")
        chi = chromatic_number(adj, total_n)
        print(f"χ = {chi}")

    # Strategy 4: Find the MAXIMUM possible cross-edges
    print("\n" + "-" * 70)
    print("STRATEGY 4: Maximize cross-edges for M₁")
    print("-" * 70)

    # For each vertex pair (one from each copy), check unit distance
    # This is O(n²) per configuration

    max_theoretical = 0
    best_angle = 0

    for angle_deg in range(0, 360, 5):
        angle = math.radians(angle_deg)
        psi = cmath.exp(1j * angle)

        # Count how many pairs could be at unit distance
        cross_count = 0
        for v1 in m1_vertices:
            for v2 in m1_vertices:
                # v2 rotated is v2 * psi
                # Distance = |v1 - v2*psi|
                d = abs(v1 - v2 * psi)
                if abs(d - 1.0) < 1e-6:
                    cross_count += 1

        if cross_count > max_theoretical:
            max_theoretical = cross_count
            best_angle = angle_deg

    print(f"Maximum cross edges at pure rotation: {max_theoretical} at {best_angle}°")

    # Now test with translation added
    print("\nAdding optimal translation...")
    best_with_trans = 0
    best_trans = None

    angle = math.radians(best_angle)
    psi = cmath.exp(1j * angle)
    rotated = [v * psi for v in m1_vertices]

    for tx in range(-5, 6):
        for ty in range(-5, 6):
            translation = complex(tx * 0.1, ty * 0.1)
            shifted = [v + translation for v in rotated]

            cross_count = 0
            for v1 in m1_vertices:
                for v2 in shifted:
                    if abs(abs(v1 - v2) - 1.0) < 1e-6:
                        cross_count += 1

            if cross_count > best_with_trans:
                best_with_trans = cross_count
                best_trans = translation

    print(f"Maximum cross edges with translation: {best_with_trans}")
    if best_trans:
        print(f"Translation: ({best_trans.real:.2f}, {best_trans.imag:.2f})")

        # Build and test this graph
        shifted = [v * psi + best_trans for v in m1_vertices]
        adj, total_n, internal, cross = build_combined_graph([m1_vertices, shifted])
        chi = chromatic_number(adj, total_n)
        print(f"χ of best M₁ combination: {chi}")

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

if __name__ == "__main__":
    main()
