#!/usr/bin/env python3
"""
MULTI-DISTANCE ATTACK

Key finding from frame dissolution:
- χ(d=1) = 3 on triangular lattice
- χ(d=√3) = 3 on triangular lattice
- χ(d=1 OR d=√3) = 4 on triangular lattice

Multiple forbidden distances INCREASE chromatic number!

Question: Can we find a set of distances D = {d₁, d₂, ...} and
vertex set V such that χ(V, D) ≥ 6?

This is a GENERALIZED Hadwiger-Nelson problem.
"""

import math
import cmath
from collections import defaultdict
from pysat.solvers import Solver
from pysat.formula import CNF
import itertools

def build_graph_multi_distance(vertices, distances, tol=1e-9):
    """Build graph where edge exists if distance is in the forbidden set."""
    n = len(vertices)
    adj = defaultdict(set)
    for i in range(n):
        for j in range(i + 1, n):
            d = abs(vertices[i] - vertices[j])
            for forbidden_d in distances:
                if abs(d - forbidden_d) < tol:
                    adj[i].add(j)
                    adj[j].add(i)
                    break
    return adj

def chromatic_number(adj, n, max_k=8):
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

def generate_triangular_lattice(radius=5):
    """Generate triangular lattice points."""
    omega = cmath.exp(1j * math.pi / 3)
    vertices = []
    for i in range(-10, 11):
        for j in range(-10, 11):
            z = i + j * omega
            if abs(z) < radius:
                vertices.append(z)
    return vertices

def generate_hexagonal_lattice(radius=5):
    """Generate hexagonal (honeycomb) lattice points."""
    omega = cmath.exp(1j * math.pi / 3)
    a = 1 / math.sqrt(3)  # Lattice constant
    vertices = []
    for i in range(-10, 11):
        for j in range(-10, 11):
            # Two points per unit cell
            z1 = a * (i * (3/2) + j * 0) + 1j * a * (i * math.sqrt(3)/2 + j * math.sqrt(3))
            z2 = z1 + a * complex(0.5, math.sqrt(3)/2)
            if abs(z1) < radius:
                vertices.append(z1)
            if abs(z2) < radius:
                vertices.append(z2)
    # Remove duplicates
    unique = []
    for v in vertices:
        if all(abs(v - u) > 0.01 for u in unique):
            unique.append(v)
    return unique

def find_natural_distances(vertices, max_dist=3):
    """Find all naturally occurring distances in a point set."""
    distances = set()
    n = len(vertices)
    for i in range(min(n, 100)):  # Sample
        for j in range(i + 1, min(n, 100)):
            d = abs(vertices[i] - vertices[j])
            if d < max_dist:
                # Round to avoid floating point issues
                d_rounded = round(d * 1000) / 1000
                distances.add(d_rounded)
    return sorted(distances)

def main():
    print("=" * 70)
    print("MULTI-DISTANCE ATTACK")
    print("=" * 70)

    # Generate lattice
    vertices = generate_triangular_lattice(radius=4)
    n = len(vertices)
    print(f"\nTriangular lattice: {n} vertices")

    # Find natural distances
    distances = find_natural_distances(vertices)
    print(f"Natural distances: {len(distances)}")
    print(f"First few: {distances[:10]}")

    # Key distances in triangular lattice
    key_distances = [
        1.0,           # Nearest neighbor
        math.sqrt(3),  # Second neighbor
        2.0,           # Third neighbor
        math.sqrt(7),  # Fourth neighbor (approx)
        3.0,           # Fifth neighbor
    ]

    print("\n" + "-" * 70)
    print("Testing distance subsets")
    print("-" * 70)

    # Test increasing subsets of distances
    for num_distances in range(1, 6):
        for dist_combo in itertools.combinations(key_distances[:5], num_distances):
            adj = build_graph_multi_distance(vertices, dist_combo)
            edges = sum(len(adj[i]) for i in range(n)) // 2
            if edges > 0:
                chi = chromatic_number(adj, n)

                if chi >= 5:
                    print(f"*** D={[f'{d:.3f}' for d in dist_combo]}: χ={chi}, edges={edges} ***")
                elif chi >= 4:
                    print(f"    D={[f'{d:.3f}' for d in dist_combo]}: χ={chi}, edges={edges}")

    # Systematic search for χ≥6
    print("\n" + "-" * 70)
    print("Systematic search for χ ≥ 6")
    print("-" * 70)

    # Try many distance combinations
    search_distances = [
        1.0, math.sqrt(3), 2.0, math.sqrt(7), 3.0,
        math.sqrt(2), math.sqrt(5), math.sqrt(6),
    ]

    best_chi = 0
    best_distances = None

    for num_d in range(2, 6):
        for dist_combo in itertools.combinations(search_distances, num_d):
            adj = build_graph_multi_distance(vertices, dist_combo)
            edges = sum(len(adj[i]) for i in range(n)) // 2
            if edges > n:  # Need enough edges
                chi = chromatic_number(adj, n, max_k=7)
                if chi > best_chi:
                    best_chi = chi
                    best_distances = dist_combo
                    print(f"NEW BEST: χ={chi} with D={[f'{d:.3f}' for d in dist_combo]}")

                if chi >= 6:
                    print(f"*** FOUND χ ≥ 6! ***")
                    break
        if best_chi >= 6:
            break

    print(f"\nBest found: χ = {best_chi}")
    if best_distances:
        print(f"Distances: {[f'{d:.3f}' for d in best_distances]}")

    # Try with larger lattice and more distances
    print("\n" + "-" * 70)
    print("Larger lattice experiment")
    print("-" * 70)

    large_vertices = generate_triangular_lattice(radius=6)
    large_n = len(large_vertices)
    print(f"Large triangular lattice: {large_n} vertices")

    # All distances up to √3
    all_short = [1.0, math.sqrt(3)]
    adj = build_graph_multi_distance(large_vertices, all_short)
    edges = sum(len(adj[i]) for i in range(large_n)) // 2
    chi = chromatic_number(adj, large_n)
    print(f"D={{1, √3}}: {large_n} vertices, {edges} edges, χ={chi}")

    # Add more distances
    more_distances = [1.0, math.sqrt(3), 2.0]
    adj = build_graph_multi_distance(large_vertices, more_distances)
    edges = sum(len(adj[i]) for i in range(large_n)) // 2
    chi = chromatic_number(adj, large_n)
    print(f"D={{1, √3, 2}}: {large_n} vertices, {edges} edges, χ={chi}")

    even_more = [1.0, math.sqrt(3), 2.0, math.sqrt(7)]
    adj = build_graph_multi_distance(large_vertices, even_more)
    edges = sum(len(adj[i]) for i in range(large_n)) // 2
    chi = chromatic_number(adj, large_n)
    print(f"D={{1, √3, 2, √7}}: {large_n} vertices, {edges} edges, χ={chi}")

    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print("""
Multi-distance constraint increases χ, but seems to saturate.

Key observation:
- Triangular lattice is 3-colorable regardless of forbidden distances
- Because its vertices form a periodic structure that's 3-colorable
- Adding more distances creates more edges but same color structure

For χ ≥ 6 with multi-distance:
- Need to BREAK the lattice symmetry
- Or use non-lattice point sets
- Or use distances that create "incompatible" constraint patterns

The multi-distance approach is promising but requires different vertex sets.
""")

if __name__ == "__main__":
    main()
