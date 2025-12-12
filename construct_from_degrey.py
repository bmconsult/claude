#!/usr/bin/env python3
"""
BUILD FROM DE GREY'S TECHNIQUE

De Grey's key insight: The H hexagon with monochromatic triple property.
Let me reconstruct this from first principles.

Key geometric facts:
- Equilateral triangle with side 1: vertices at distance 1
- Two equilateral triangles sharing an edge = rhombus with vertices at distance 1 or √3

The Moser spindle uses two unit rhombi sharing vertices.
"""

import math
import cmath
from collections import defaultdict
from pysat.solvers import Solver
from pysat.formula import CNF

def unit_dist(z1, z2, tol=1e-9):
    return abs(abs(z1 - z2) - 1.0) < tol

def build_adj(vertices, tol=1e-9):
    n = len(vertices)
    adj = defaultdict(set)
    edges = 0
    for i in range(n):
        for j in range(i + 1, n):
            if unit_dist(vertices[i], vertices[j], tol):
                adj[i].add(j)
                adj[j].add(i)
                edges += 1
    return adj, edges

def chromatic(adj, n, max_k=7):
    for k in range(1, max_k + 1):
        if k_colorable(adj, n, k):
            return k
    return max_k + 1

def k_colorable(adj, n, k):
    def var(v, c): return v * k + c + 1
    cnf = CNF()
    for i in range(n):
        cnf.append([var(i, c) for c in range(k)])
        for c1 in range(k):
            for c2 in range(c1 + 1, k):
                cnf.append([-var(i, c1), -var(i, c2)])
    for i in adj:
        for j in adj[i]:
            if j > i:
                for c in range(k):
                    cnf.append([-var(i, c), -var(j, c)])
    with Solver(name='g4') as s:
        s.append_formula(cnf)
        return s.solve()

def correct_moser_spindle():
    """
    Moser spindle: two rhombi with 60° angles sharing two vertices.

    Rhombus 1: A-B-C-D with A,C at distance √3, B,D at distance 1
    Rhombus 2: shares vertices and adds 3 more

    Actually, easier construction:
    - Place two equilateral triangles sharing one edge
    - Then place another pair sharing different edges
    """
    # Unit equilateral triangle at origin
    A = complex(0, 0)
    B = complex(1, 0)
    C = complex(0.5, math.sqrt(3)/2)

    # Second triangle sharing edge AB, pointing down
    D = complex(0.5, -math.sqrt(3)/2)

    # Third triangle sharing edge AC
    # Point at distance 1 from both A and C, not B
    # A is at (0,0), C is at (0.5, √3/2)
    # Midpoint: (0.25, √3/4)
    # Distance A to C = 1
    # Intersection of circles centered at A and C, radius 1
    # Already have this - it's the one on the other side
    E = complex(-0.5, math.sqrt(3)/2)

    # Fourth triangle sharing edge BC
    F = complex(1.5, math.sqrt(3)/2)

    # Now we have 6 vertices: A,B,C,D,E,F
    # Check which pairs are at unit distance

    # For Moser spindle, we need 7 vertices
    # Add point G at distance 1 from both E and F
    # E = (-0.5, √3/2), F = (1.5, √3/2)
    # Distance E to F = 2, so no point at distance 1 from both

    # Different approach: standard Moser spindle from literature
    # Two unit rhombi (60° angle) sharing two opposite vertices

    sqrt3 = math.sqrt(3)

    # Vertices of Moser spindle
    v0 = complex(0, 0)
    v1 = complex(1, 0)
    v2 = complex(0.5, sqrt3/2)
    v3 = complex(1.5, sqrt3/2)
    v4 = complex(0.5, -sqrt3/2)
    v5 = complex(1.5, -sqrt3/2)
    v6 = complex(2, 0)

    vertices = [v0, v1, v2, v3, v4, v5, v6]
    return vertices

def h_hexagon():
    """
    De Grey's H hexagon: 31 vertices with monochromatic triple property.

    The H hexagon is constructed by:
    1. Taking copies of Moser spindles
    2. Arranging them to create a specific forbidden pattern

    For now, let's build iteratively from the spindle.
    """
    # Start with Moser spindle
    spindle = correct_moser_spindle()

    # Rotate by 60° and translate to connect
    angle = math.pi / 3
    rot = cmath.exp(1j * angle)

    # Place rotated spindle adjacent
    spindle2 = [v * rot + complex(1, 0) for v in spindle]

    # Combine (removing duplicates)
    combined = list(spindle)
    for v in spindle2:
        if all(abs(v - u) > 0.01 for u in combined):
            combined.append(v)

    return combined

def build_j_graph():
    """
    De Grey's J graph: Multiple H copies arranged with rotation.
    This is the core of the 5-chromatic construction.
    """
    h = h_hexagon()

    # Multiple rotated copies
    graphs = [h]

    for k in range(1, 6):  # 5 more rotations
        angle = k * math.pi / 3
        rot = cmath.exp(1j * angle)
        rotated = [v * rot for v in h]
        graphs.append(rotated)

    # Combine all
    combined = []
    for g in graphs:
        for v in g:
            if all(abs(v - u) > 0.01 for u in combined):
                combined.append(v)

    return combined

def main():
    print("=" * 60)
    print("BUILDING FROM DE GREY'S TECHNIQUE")
    print("=" * 60)

    # Test Moser spindle
    print("\n1. Moser Spindle")
    spindle = correct_moser_spindle()
    adj, edges = build_adj(spindle)
    chi = chromatic(adj, len(spindle))
    print(f"   Vertices: {len(spindle)}, Edges: {edges}, χ={chi}")

    # Expected: 7 vertices, 11 edges, χ=4
    if chi != 4:
        print("   WARNING: Expected χ=4 for Moser spindle!")
        # Debug: print distances
        print("   Checking distances:")
        for i in range(len(spindle)):
            for j in range(i+1, len(spindle)):
                d = abs(spindle[j] - spindle[i])
                if abs(d - 1.0) < 0.01:
                    print(f"   {i}-{j}: {d:.6f}")

    # H hexagon
    print("\n2. H Hexagon (double spindle)")
    h = h_hexagon()
    adj_h, edges_h = build_adj(h)
    chi_h = chromatic(adj_h, len(h))
    print(f"   Vertices: {len(h)}, Edges: {edges_h}, χ={chi_h}")

    # J graph
    print("\n3. J Graph (rotated H copies)")
    j = build_j_graph()
    adj_j, edges_j = build_adj(j)
    chi_j = chromatic(adj_j, len(j))
    print(f"   Vertices: {len(j)}, Edges: {edges_j}, χ={chi_j}")

    # Try building more
    print("\n4. Extending J with more rotations...")
    extended = list(j)

    for angle_num in range(12):
        angle = angle_num * math.pi / 6  # 30° increments
        rot = cmath.exp(1j * angle)
        for v in j:
            new_v = v * rot
            if all(abs(new_v - u) > 0.01 for u in extended):
                extended.append(new_v)

    adj_ext, edges_ext = build_adj(extended)
    chi_ext = chromatic(adj_ext, len(extended))
    print(f"   Vertices: {len(extended)}, Edges: {edges_ext}, χ={chi_ext}")

    if chi_ext >= 5:
        print(f"\n*** Reached χ={chi_ext}! ***")

        if chi_ext >= 6:
            print("*** BREAKTHROUGH: χ≥6 ACHIEVED! ***")

if __name__ == "__main__":
    main()
