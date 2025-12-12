#!/usr/bin/env python3
"""
HYBRID ATTACK: M ∪ ψ·M ∪ (M + v)

Combine BOTH rotation and translation to create maximum constraint.
Three copies with different geometric relationships.
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

def load_vertices_complex(filename):
    vertices = []
    with open(filename, 'r') as f:
        for line in f:
            result = parse_vertex_line(line)
            if result is not None:
                vertices.append(result)
    return vertices

def build_hybrid_graph(vertices, psi, v, tolerance=1e-9):
    """Build M ∪ ψ·M ∪ (M + v)"""
    rotated = [z * psi for z in vertices]
    translated = [z + v for z in vertices]

    n = len(vertices)
    adj = defaultdict(set)

    all_sets = [vertices, rotated, translated]
    offsets = [0, n, 2*n]

    total_edges = 0
    cross_edges = 0

    # Within each copy
    for o, vset in enumerate(all_sets):
        for i in range(n):
            for j in range(i + 1, n):
                d = abs(vset[i] - vset[j])
                if abs(d - 1.0) < tolerance:
                    adj[offsets[o] + i].add(offsets[o] + j)
                    adj[offsets[o] + j].add(offsets[o] + i)
                    total_edges += 1

    # Between all pairs of copies
    for o1, set1 in enumerate(all_sets):
        for o2, set2 in enumerate(all_sets):
            if o1 >= o2:
                continue
            for i in range(n):
                for j in range(n):
                    d = abs(set1[i] - set2[j])
                    if abs(d - 1.0) < tolerance:
                        adj[offsets[o1] + i].add(offsets[o2] + j)
                        adj[offsets[o2] + j].add(offsets[o1] + i)
                        total_edges += 1
                        cross_edges += 1

    return adj, 3 * n, total_edges, cross_edges

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
    print("HYBRID ATTACK: M ∪ ψ·M ∪ (M + v)")
    print("=" * 70)

    vtx_file = "dist-graphs/plane/series 2/vtx/s2_M2.vtx"
    print(f"\nLoading vertices from {vtx_file}...")
    vertices = load_vertices_complex(vtx_file)
    n = len(vertices)
    print(f"Loaded {n} vertices")

    # Test combinations of rotation and translation
    rotation_angles = [math.pi/6, math.pi/4, math.pi/3, math.pi/2]
    translation_angles = [0, math.pi/4, math.pi/2, 3*math.pi/4]

    print("\n" + "-" * 70)
    print("Testing hybrid combinations...")
    print("-" * 70)

    for rot_angle in rotation_angles:
        for trans_angle in translation_angles:
            psi = cmath.exp(1j * rot_angle)
            v = cmath.exp(1j * trans_angle)  # Unit translation

            rot_deg = rot_angle * 180 / math.pi
            trans_deg = trans_angle * 180 / math.pi

            adj, total_n, total_edges, cross_edges = build_hybrid_graph(vertices, psi, v)

            print(f"\nRotation {rot_deg:.0f}° + Translation {trans_deg:.0f}°:")
            print(f"  {total_n} vertices, {total_edges} edges ({cross_edges} cross)")

            start = time.time()
            is_5col = is_k_colorable(adj, total_n, 5)
            elapsed = time.time() - start

            if is_5col:
                print(f"  5-colorable ({elapsed:.1f}s)")
            else:
                print(f"  *** NOT 5-COLORABLE! ({elapsed:.1f}s)")

                is_6col = is_k_colorable(adj, total_n, 6)
                if is_6col:
                    print(f"  *** χ = 6! FOUND 6-CHROMATIC! ***")
                    return rot_angle, trans_angle
                else:
                    print(f"  χ ≥ 7!")
                    return rot_angle, trans_angle

    print("\n" + "=" * 70)
    print("CONCLUSION: Hybrid attacks also result in 5-colorable")
    print("=" * 70)

if __name__ == "__main__":
    main()
