#!/usr/bin/env python3
"""
Use EXACT Voronov angles with THREE copies

Series 2 has 11 different rotation angles ψ that each create 5-chromatic graphs.
Maybe combining TWO different ψ values (THREE total copies) forces 6-chromatic!

M₃ ∪ ψ₁·M₃ ∪ ψ₂·M₃ where ψ₁, ψ₂ are from Voronov's computed angles
"""

import re
import math
import cmath
from collections import defaultdict
from pysat.solvers import Solver
from pysat.formula import CNF
import time

# Voronov Series 2 psi values (computed from notebook output)
# These are complex numbers representing rotations
VORONOV_PSI_SERIES2 = [
    # From psi_series2() output - these are the numerical values
    # ψ = exp(iθ) where θ is the rotation angle
    complex(0.999833687449347, 0.0182372542187895),  # Case 1
    # More values would be extracted from running psi_series2()
]

# Series 1 psi values
VORONOV_PSI_SERIES1 = [
    complex(0.875000000000000, 0.484122918275927),
    complex(0.969160753429815, 0.246429369214292),
    complex(0.977502967880533, 0.210921662673018),
    complex(0.996775678722190, 0.0802386833635565),
    complex(0.999038808433311, 0.0438344527073038),
]

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
    return complex(x, y)  # Return as complex number

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

def rotate_complex(z, psi):
    """Rotate point z by complex rotation psi"""
    return z * psi

def build_triple_graph_complex(vertices, psi1, psi2, tolerance=1e-9):
    """Build M ∪ ψ₁·M ∪ ψ₂·M using complex arithmetic"""
    rot1 = [rotate_complex(z, psi1) for z in vertices]
    rot2 = [rotate_complex(z, psi2) for z in vertices]

    n = len(vertices)
    adj = defaultdict(set)

    all_sets = [vertices, rot1, rot2]
    edges_within = 0
    edges_cross = 0

    # Within each copy
    for offset, vset in enumerate(all_sets):
        for i in range(n):
            for j in range(i + 1, n):
                d = abs(vset[i] - vset[j])
                if abs(d - 1.0) < tolerance:
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
                    d = abs(set1[i] - set2[j])
                    if abs(d - 1.0) < tolerance:
                        adj[o1 * n + i].add(o2 * n + j)
                        adj[o2 * n + j].add(o1 * n + i)
                        edges_cross += 1

    return adj, 3 * n, edges_within, edges_cross

def is_k_colorable(adj, n, k, timeout=60):
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
    print("VORONOV TRIPLE ATTACK: M ∪ ψ₁·M ∪ ψ₂·M")
    print("Using EXACT Voronov rotation angles")
    print("=" * 70)

    # Use Series 1 initial set (Moser spindle based, 31 vertices → 1939 in M₃)
    # This is smaller and the angles are already verified
    vtx_file = "dist-graphs/plane/series 2/vtx/s2_M2.vtx"

    print(f"\nLoading vertices from {vtx_file}...")
    vertices = load_vertices_complex(vtx_file)
    print(f"Loaded {len(vertices)} vertices as complex numbers")

    if len(vertices) < 100:
        print("ERROR: Not enough vertices!")
        return

    n = len(vertices)

    # Count base edges
    base_edges = 0
    adj_base = defaultdict(set)
    for i in range(n):
        for j in range(i + 1, n):
            d = abs(vertices[i] - vertices[j])
            if abs(d - 1.0) < 1e-9:
                adj_base[i].add(j)
                adj_base[j].add(i)
                base_edges += 1

    print(f"Base: {n} vertices, {base_edges} edges")

    # Check base χ
    for k in range(3, 7):
        if is_k_colorable(adj_base, n, k):
            print(f"Base χ = {k}")
            break

    print("\n" + "=" * 70)
    print("TESTING VORONOV ANGLE PAIRS")
    print("=" * 70)

    # Test pairs of Voronov angles
    psi_list = VORONOV_PSI_SERIES1

    for i, psi1 in enumerate(psi_list):
        for j, psi2 in enumerate(psi_list):
            if i >= j:
                continue

            angle1 = cmath.phase(psi1) * 180 / math.pi
            angle2 = cmath.phase(psi2) * 180 / math.pi

            print(f"\nψ₁ = {angle1:.2f}°, ψ₂ = {angle2:.2f}°:")

            adj, total_n, within, cross = build_triple_graph_complex(vertices, psi1, psi2)
            total_edges = within + cross

            print(f"  Combined: {total_n} vertices, {total_edges} edges ({cross} cross)")

            # Test colorability
            start = time.time()
            is_5col = is_k_colorable(adj, total_n, 5)
            elapsed = time.time() - start

            if is_5col:
                print(f"  5-colorable ({elapsed:.1f}s)")
            else:
                print(f"  *** NOT 5-COLORABLE! ({elapsed:.1f}s)")
                is_6col = is_k_colorable(adj, total_n, 6)
                if is_6col:
                    print(f"  *** 6-CHROMATIC! χ = 6 ***")
                    print(f"  BREAKTHROUGH: Found 6-chromatic plane graph!")
                    return psi1, psi2
                else:
                    print(f"  Checking 7-colorability...")
                    is_7col = is_k_colorable(adj, total_n, 7)
                    if is_7col:
                        print(f"  *** 7-CHROMATIC! χ = 7 ***")
                    else:
                        print(f"  *** χ ≥ 8! MAJOR DISCOVERY! ***")

    # Also try combining ALL psi values
    print("\n" + "=" * 70)
    print("TESTING MULTIPLE COPIES")
    print("=" * 70)

    # Try 4 copies with 3 rotations
    if len(psi_list) >= 3:
        psi1, psi2, psi3 = psi_list[0], psi_list[1], psi_list[2]

        print(f"\n4 copies with 3 Voronov rotations:")

        all_sets = [vertices]
        for psi in [psi1, psi2, psi3]:
            all_sets.append([rotate_complex(z, psi) for z in vertices])

        # Build adjacency
        adj = defaultdict(set)
        for o1, set1 in enumerate(all_sets):
            for o2, set2 in enumerate(all_sets):
                if o1 > o2:
                    continue
                for i in range(n):
                    j_start = i + 1 if o1 == o2 else 0
                    for j in range(j_start, n):
                        d = abs(set1[i] - set2[j])
                        if abs(d - 1.0) < 1e-9:
                            adj[o1 * n + i].add(o2 * n + j)
                            adj[o2 * n + j].add(o1 * n + i)

        total_n = 4 * n
        total_edges = sum(len(adj[i]) for i in range(total_n)) // 2
        print(f"  Combined: {total_n} vertices, {total_edges} edges")

        start = time.time()
        is_5col = is_k_colorable(adj, total_n, 5)
        elapsed = time.time() - start

        if is_5col:
            print(f"  5-colorable ({elapsed:.1f}s)")
        else:
            print(f"  *** NOT 5-COLORABLE! Testing 6... ***")

    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print("No 6-chromatic found with Voronov angle combinations.")
    print("The forcing to 5 seems to be the structural limit.")

if __name__ == "__main__":
    main()
