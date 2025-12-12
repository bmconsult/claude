#!/usr/bin/env python3
"""
Build the ACTUAL Moser spindle with correct coordinates.

The Moser spindle is TWO unit rhombi sharing their short diagonal.
A unit rhombus has sides = 1, angles 60° and 120°.
Diagonals: √3 (long) and 1 (short).

Key insight: The two rhombi are on OPPOSITE SIDES of the shared diagonal.
"""

import math
import cmath
from collections import defaultdict
from pysat.solvers import Solver
from pysat.formula import CNF

def unit_distance(z1, z2, tol=1e-9):
    return abs(abs(z1 - z2) - 1.0) < tol

def build_graph(vertices, tol=1e-9):
    n = len(vertices)
    adj = defaultdict(set)
    for i in range(n):
        for j in range(i + 1, n):
            if unit_distance(vertices[i], vertices[j], tol):
                adj[i].add(j)
                adj[j].add(i)
    return adj

def chromatic_number(adj, n, max_k=7):
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

def moser_spindle_v1():
    """
    Construction: two rhombi back-to-back sharing short diagonal.

    Rhombus 1: A-B-C-D with short diagonal A-C
    Rhombus 2: A-C-E-F (sharing A-C) on opposite side
    Plus vertex G connecting the structure.
    """
    # Short diagonal endpoints
    A = complex(0, 0)
    C = complex(1, 0)

    # Rhombus 1: B and D are at distance 1 from both A and C
    # They're on opposite sides of line AC
    B = complex(0.5, math.sqrt(3)/2)
    D = complex(0.5, -math.sqrt(3)/2)

    # Rhombus 2 shares diagonal A-C
    # E and F at distance 1 from A and C, but displaced
    # Actually this gives B and D again!

    # Different approach: the spindle has 7 vertices.
    # Let's try a different configuration.

    return [A, B, C, D], "Wrong - only 4 vertices"

def moser_spindle_v2():
    """
    The Moser spindle from Soifer's book:

    Place two equilateral triangles sharing edge AB.
    Add vertices at specific positions.
    """
    A = complex(0, 0)
    B = complex(1, 0)

    # Upper triangle ABE
    E = complex(0.5, math.sqrt(3)/2)

    # Lower triangle ABF
    F = complex(0.5, -math.sqrt(3)/2)

    # C at distance 1 from both A and E (not = B)
    # Intersection of circles: B or (-0.5, sqrt(3)/2)
    C = complex(-0.5, math.sqrt(3)/2)

    # D at distance 1 from both B and F (not = A)
    # Intersection: A or (1.5, -sqrt(3)/2)
    D = complex(1.5, -math.sqrt(3)/2)

    # G at distance 1 from C and D?
    # |CD| = sqrt(4 + 3) = sqrt(7), so no intersection with unit circles

    # Try: G at distance 1 from C and E
    # C = (-0.5, sqrt(3)/2), E = (0.5, sqrt(3)/2), |CE| = 1
    # Intersection: A or (-0.5 + 0.5, sqrt(3)/2 + sqrt(3)/2) - let me compute
    # Mid(C,E) = (0, sqrt(3)/2)
    # Perp to CE = (0, 1)
    # G = (0, sqrt(3)/2 + sqrt(3)/2) = (0, sqrt(3)) or (0, 0) = A
    G = complex(0, math.sqrt(3))

    vertices = [A, B, C, D, E, F, G]
    return vertices

def moser_spindle_v3():
    """
    Try yet another construction based on the actual graph structure.

    The Moser spindle graph has these edges:
    - Two triangles ABC, ABD sharing AB
    - Vertex E adjacent to B,C and vertex F adjacent to B,D
    - Vertex G adjacent to both E and F
    - Additional edges to make χ=4
    """
    A = complex(0, 0)
    B = complex(1, 0)
    C = complex(0.5, math.sqrt(3)/2)
    D = complex(0.5, -math.sqrt(3)/2)

    # E adjacent to B and C: at intersection of their unit circles
    # B=(1,0), C=(0.5, sqrt(3)/2), |BC|=1
    # Options: A or (1.5, sqrt(3)/2)
    E = complex(1.5, math.sqrt(3)/2)

    # F adjacent to B and D
    # B=(1,0), D=(0.5, -sqrt(3)/2)
    # Options: A or (1.5, -sqrt(3)/2)
    F = complex(1.5, -math.sqrt(3)/2)

    # G adjacent to E and F
    # E=(1.5, sqrt(3)/2), F=(1.5, -sqrt(3)/2), |EF|=sqrt(3)
    # Circle intersection with |EF|=sqrt(3) gives two points
    # Mid = (1.5, 0), offset = sqrt(1 - 3/4) = 0.5
    # G = (1.5 + 0.5, 0) = (2, 0) or (1.5 - 0.5, 0) = (1, 0) = B
    G = complex(2, 0)

    return [A, B, C, D, E, F, G]

def moser_spindle_v4():
    """
    Classic Moser spindle from the original 1961 paper.

    Uses the fact that it's two unit rhombi glued together.
    """
    # First rhombus ABCD: vertices at 0, 1, 1+ω, ω where ω = e^(iπ/3)
    omega = cmath.exp(1j * math.pi / 3)

    A = complex(0, 0)
    B = complex(1, 0)
    C = 1 + omega  # = 1.5 + sqrt(3)/2 * i
    D = omega      # = 0.5 + sqrt(3)/2 * i

    # Second rhombus shares edge BD (which has length 1)
    # Place it on the opposite side of BD

    # BD midpoint: (1 + omega)/2
    # Perpendicular to BD direction
    # New vertices E, F at distance 1 from B and D

    # Actually with this setup:
    # B = (1, 0), D = (0.5, sqrt(3)/2)
    # |BD| = 1
    # Points at dist 1 from both: (0,0)=A and (1.5, sqrt(3)/2)=C

    # So we need to use the LONG diagonal AD (length sqrt(3)) instead
    # and build the second rhombus differently.

    # Alternative: rotate the second rhombus
    # Place E at distance 1 from B and C
    # B = 1, C = 1+omega, |BC| = 1
    # Intersection: D = omega, or 1 + omega + omega = 1 + 2omega
    E = 1 + 2*omega  # = 1 + 2*(0.5 + sqrt(3)/2*i) = 2 + sqrt(3)*i

    # F at distance 1 from A and D
    # A = 0, D = omega, |AD| = 1
    # Intersection: B=1, or -omega
    F = -omega  # = -0.5 - sqrt(3)/2 * i

    # Now we have 6 vertices. Where's the 7th?
    # G at distance 1 from E and F?
    # E = 2 + sqrt(3)i, F = -0.5 - sqrt(3)/2*i
    # |EF| = sqrt((2.5)^2 + (1.5*sqrt(3))^2) = sqrt(6.25 + 6.75) = sqrt(13) >> 1
    # No intersection.

    return [A, B, C, D, E, F], "6 vertices only"

def search_spindle_combinatorially():
    """
    Search for 7-vertex unit-distance graphs with χ=4.

    Generate candidate vertex sets and check properties.
    """
    print("\nSearching for χ=4 unit-distance graphs on 7 vertices...")

    # Start with a triangle at origin
    base = [
        complex(0, 0),
        complex(1, 0),
        complex(0.5, math.sqrt(3)/2)
    ]

    # Add 4 more vertices from a lattice
    # Use the triangular lattice: m + n*omega where omega = e^(iπ/3)
    omega = cmath.exp(1j * math.pi / 3)

    candidates = []
    for m in range(-2, 4):
        for n in range(-2, 4):
            z = m + n * omega
            # Skip if already in base
            if all(abs(z - b) > 1e-9 for b in base):
                candidates.append(z)

    from itertools import combinations

    best_chi = 0
    best_graph = None

    for extra in combinations(candidates, 4):
        vertices = base + list(extra)
        adj = build_graph(vertices)
        edges = sum(len(adj[i]) for i in range(7)) // 2

        if edges >= 9:  # Need enough edges
            chi = chromatic_number(adj, 7)
            if chi > best_chi:
                best_chi = chi
                best_graph = (vertices, adj, edges)
                if chi >= 4:
                    print(f"Found χ={chi}: {edges} edges")
                    return vertices, adj, edges, chi

    if best_graph:
        print(f"Best found: χ={best_chi}, {best_graph[2]} edges")
    return None

def main():
    print("=" * 70)
    print("SEARCHING FOR REAL MOSER SPINDLE")
    print("=" * 70)

    # Test various constructions
    print("\n--- Testing construction v2 ---")
    v2 = moser_spindle_v2()
    adj = build_graph(v2)
    edges = sum(len(adj[i]) for i in range(7)) // 2
    chi = chromatic_number(adj, 7)
    print(f"V2: {len(v2)} vertices, {edges} edges, χ={chi}")

    print("\n--- Testing construction v3 ---")
    v3 = moser_spindle_v3()
    adj = build_graph(v3)
    edges = sum(len(adj[i]) for i in range(7)) // 2
    chi = chromatic_number(adj, 7)
    print(f"V3: {len(v3)} vertices, {edges} edges, χ={chi}")

    # Print edges
    print("Edges:")
    for i in range(7):
        for j in adj[i]:
            if j > i:
                print(f"  {i}-{j}: |{v3[i]} - {v3[j]}| = {abs(v3[i] - v3[j]):.6f}")

    # Search combinatorially
    print("\n--- Combinatorial search ---")
    result = search_spindle_combinatorially()

    if result:
        vertices, adj, edges, chi = result
        print(f"\nFound unit-distance graph with χ={chi}!")
        print(f"Vertices: {len(vertices)}, Edges: {edges}")
        for i, v in enumerate(vertices):
            print(f"  {i}: ({v.real:.6f}, {v.imag:.6f})")

if __name__ == "__main__":
    main()
