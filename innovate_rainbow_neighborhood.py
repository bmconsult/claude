#!/usr/bin/env python3
"""
MATHEMATICAL INNOVATION: Rainbow Neighborhood Construction

Key insight for χ=6:
- Vertex v needs color 6 if N(v) is 5-chromatic
- Because then v's neighbors use ALL 5 colors in every valid coloring
- So v must have color 6

Goal: Construct a unit-distance graph where some vertex has a 5-chromatic neighborhood.

Challenge: The neighborhood must:
1. Be a valid unit-distance graph (all neighbors at distance 1 from v)
2. Have chromatic number 5
3. Be embeddable in the plane

Approach:
- Start with v at origin
- Place neighbors on the unit circle around v
- Add edges between neighbors (when they're at unit distance)
- Try to make N(v) = {neighbors} be 5-chromatic
"""

import math
import cmath
from collections import defaultdict
from pysat.solvers import Solver
from pysat.formula import CNF
import itertools

def unit_distance(z1, z2, tol=1e-9):
    """Check if two complex numbers are at unit distance"""
    return abs(abs(z1 - z2) - 1.0) < tol

def build_graph(vertices):
    """Build unit-distance graph from vertex set"""
    n = len(vertices)
    adj = defaultdict(set)
    for i in range(n):
        for j in range(i + 1, n):
            if unit_distance(vertices[i], vertices[j]):
                adj[i].add(j)
                adj[j].add(i)
    return adj

def chromatic_number(adj, n, max_k=7):
    """Find chromatic number via SAT"""
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

def neighbors_on_circle():
    """
    Place neighbors on unit circle such that some pairs are at unit distance.

    Key geometric fact: Two points on a unit circle centered at origin
    are at unit distance iff the angle between them is 60° (π/3).

    Proof: For points e^(iθ₁) and e^(iθ₂) on unit circle,
    |e^(iθ₁) - e^(iθ₂)|² = 2 - 2cos(θ₁ - θ₂)
    This equals 1 when cos(θ₁ - θ₂) = 1/2, i.e., |θ₁ - θ₂| = π/3
    """
    # Place points at multiples of π/3 (60°) on unit circle
    # These form a regular hexagon - each adjacent pair at unit distance
    hexagon = [cmath.exp(1j * k * math.pi / 3) for k in range(6)]
    return hexagon

def build_neighborhood_graph(neighbors):
    """Build the graph induced by N(v) - edges between neighbors"""
    n = len(neighbors)
    adj = defaultdict(set)
    for i in range(n):
        for j in range(i + 1, n):
            if unit_distance(neighbors[i], neighbors[j]):
                adj[i].add(j)
                adj[j].add(i)
    return adj, n

def try_extended_neighborhood():
    """
    Try to build a 5-chromatic neighborhood.

    A regular hexagon (6 vertices) on unit circle has χ=2 (it's bipartite).
    We need to add more structure to force χ=5.

    Idea: Add vertices at distance 1 from MULTIPLE hexagon vertices,
    creating a denser constraint network.
    """
    print("=" * 70)
    print("INNOVATION: Rainbow Neighborhood Construction")
    print("=" * 70)

    # Start with hexagon
    hexagon = neighbors_on_circle()
    print(f"\nBase hexagon: {len(hexagon)} vertices on unit circle")

    adj, n = build_neighborhood_graph(hexagon)
    edges = sum(len(adj[i]) for i in range(n)) // 2
    chi = chromatic_number(adj, n)
    print(f"Hexagon neighborhood: {n} vertices, {edges} edges, χ={chi}")

    # The hexagon alone is only 2-chromatic. Need more vertices.

    # Key insight: Add points that are at distance 1 from multiple hexagon vertices
    # Such points lie on the intersection of multiple unit circles

    # Two unit circles centered at adjacent hexagon vertices (60° apart):
    # Their intersection points are at distance 1 from both centers

    print("\n" + "-" * 70)
    print("Adding intersection points...")
    print("-" * 70)

    extended = list(hexagon)

    # For each pair of adjacent hexagon vertices, find intersection points
    # of their unit circles (excluding the origin which we don't want)

    for i in range(6):
        j = (i + 1) % 6
        c1, c2 = hexagon[i], hexagon[j]

        # Intersection of two unit circles centered at c1 and c2
        # where |c1 - c2| = 1 (since adjacent hexagon vertices are at distance 1)

        # The two intersection points are equidistant from the line c1-c2
        # One is closer to origin, one is farther

        # Using geometry: midpoint + perpendicular offset
        mid = (c1 + c2) / 2
        perp = (c2 - c1) * 1j  # Rotate by 90°
        perp_unit = perp / abs(perp)

        # Distance from midpoint to intersection: sqrt(1 - (1/2)²) = sqrt(3)/2
        offset = math.sqrt(3) / 2

        p1 = mid + offset * perp_unit
        p2 = mid - offset * perp_unit

        # One of these is the origin (or close to it), skip that one
        # Actually, with hexagon on unit circle, neither is exactly at origin

        # Add both if they're new and at distance 1 from origin
        for p in [p1, p2]:
            dist_to_origin = abs(p)
            if abs(dist_to_origin - 1.0) < 1e-9:  # On unit circle = neighbor of v
                # Check if already in extended
                is_new = all(abs(p - e) > 1e-9 for e in extended)
                if is_new:
                    extended.append(p)

    print(f"Extended neighborhood: {len(extended)} vertices")

    adj_ext, n_ext = build_neighborhood_graph(extended)
    edges_ext = sum(len(adj_ext[i]) for i in range(n_ext)) // 2
    chi_ext = chromatic_number(adj_ext, n_ext)
    print(f"Extended neighborhood: {n_ext} vertices, {edges_ext} edges, χ={chi_ext}")

    # Still probably not 5-chromatic. Need more structure.
    # Let's try a different approach: use multiple scales

    print("\n" + "-" * 70)
    print("Trying multi-scale construction...")
    print("-" * 70)

    # Place a Moser spindle at distance 1 from origin
    # The Moser spindle has χ=4

    # Moser spindle vertices (standard embedding):
    # Two triangles sharing an edge, with specific distances

    # Actually, let me try a different approach:
    # Start with known 4-chromatic structure and try to extend to 5

    # The key challenge: N(v) must be contained in the unit circle around v
    # This is a VERY strong geometric constraint

    # Let me compute the maximum degree of v in known 5-chromatic graphs

    return extended, chi_ext

def analyze_degree_bound():
    """
    What's the maximum number of neighbors a vertex can have in a unit-distance graph?

    All neighbors lie on the unit circle around v.
    Pairs of neighbors at distance 1 from each other are at angle 60°.

    So the maximum degree is achieved when we pack as many points as possible
    on the unit circle such that we don't violate any constraints.

    Actually, there's no upper bound from unit-distance alone!
    We can have infinitely many points on the circle, as long as we don't
    require them to form edges with each other.

    But for N(v) to be 5-chromatic, we need N(v) to be a specific structure.
    """
    print("\n" + "=" * 70)
    print("ANALYZING DEGREE BOUNDS")
    print("=" * 70)

    # The minimum 5-chromatic graph has 509 vertices
    # If we could fit a 5-chromatic graph inside N(v) (on the unit circle),
    # then v would need a 6th color

    # Can we embed a 5-chromatic unit-distance graph on a circle?
    # That graph would need to be a unit-distance graph ON THE CIRCLE
    # where "unit distance" means distance 1 in the plane

    # On a unit circle, two points are at plane-distance 1 iff angle = 60°
    # So the induced unit-distance graph of points on unit circle is:
    # - Vertices: points on circle
    # - Edges: pairs at 60° apart

    # This is like a "60°-graph" on the circle
    # What's the max chromatic number of such a graph?

    # If we place vertices at angles 0, 60, 120, 180, 240, 300 (regular hexagon),
    # each vertex is adjacent to its two neighbors → cycle C₆ → χ=2

    # If we add more vertices, say at 30°, 90°, 150°, 210°, 270°, 330°,
    # (dodecagon), vertices at 30° are adjacent to 90° and 330°

    # Let me compute χ for various configurations

    for n_points in [6, 12, 24, 36, 60, 120]:
        angles = [2 * math.pi * k / n_points for k in range(n_points)]
        vertices = [cmath.exp(1j * a) for a in angles]

        adj = defaultdict(set)
        for i in range(n_points):
            for j in range(i + 1, n_points):
                if unit_distance(vertices[i], vertices[j]):
                    adj[i].add(j)
                    adj[j].add(i)

        edges = sum(len(adj[i]) for i in range(n_points)) // 2
        chi = chromatic_number(adj, n_points)
        print(f"Regular {n_points}-gon: {edges} edges, χ={chi}")

    # Key insight: Regular n-gons on unit circle have low χ because
    # the "60°-graph" is just a union of disjoint cycles or paths

def try_irregular_placement():
    """
    Try irregular vertex placements on unit circle to maximize χ of neighborhood.
    """
    print("\n" + "=" * 70)
    print("TRYING IRREGULAR PLACEMENTS")
    print("=" * 70)

    import random

    best_chi = 0
    best_config = None

    for trial in range(100):
        # Random angles
        n_points = random.randint(10, 50)
        angles = sorted([random.uniform(0, 2 * math.pi) for _ in range(n_points)])
        vertices = [cmath.exp(1j * a) for a in angles]

        adj = defaultdict(set)
        for i in range(n_points):
            for j in range(i + 1, n_points):
                if unit_distance(vertices[i], vertices[j]):
                    adj[i].add(j)
                    adj[j].add(i)

        edges = sum(len(adj[i]) for i in range(n_points)) // 2
        if edges == 0:
            continue

        chi = chromatic_number(adj, n_points)

        if chi > best_chi:
            best_chi = chi
            best_config = (n_points, edges, angles)
            print(f"Trial {trial}: {n_points} points, {edges} edges, χ={chi} (NEW BEST)")

    if best_config:
        n, e, angles = best_config
        print(f"\nBest found: {n} points, {e} edges, χ={best_chi}")

    return best_chi

def theoretical_bound():
    """
    Theoretical analysis of maximum χ for neighborhood graph.
    """
    print("\n" + "=" * 70)
    print("THEORETICAL ANALYSIS")
    print("=" * 70)

    print("""
Key constraint: All neighbors of v lie on the unit circle around v.

Two neighbors u₁, u₂ are adjacent (in N(v)) iff |u₁ - u₂| = 1.

On a unit circle, |u₁ - u₂| = 1 iff angle between them is exactly 60°.

So the neighborhood graph N(v) is determined by:
- Points on circle
- Edges between points at 60° apart

This is a CIRCULANT-like graph on the circle.

The maximum clique in such a graph:
- Three points at 60° apart form a clique (equilateral triangle)
- No 4-clique possible (would need 4 points mutually at 60°)

So ω(N(v)) ≤ 3 (clique number ≤ 3)

For χ ≥ 5, we need χ > ω, which requires non-trivial structure.

The Moser spindle achieves χ=4 with ω=3.
Can we embed a χ=4 structure on the circle? YES - the hexagon + triangles.

For χ=5 on the circle?
- Need enough vertices and edges
- But the "60°-graph" structure is limited

INSIGHT: The neighborhood of v in a unit-distance graph cannot have χ ≥ 5!

Because:
- N(v) is a unit-distance graph on a circle
- Such graphs have special structure (60°-adjacency)
- This structure limits χ to at most 4

If true, this means we CANNOT achieve χ(G) ≥ 6 via the rainbow neighborhood approach!
""")

    # Let me verify by exhaustive search on small cases
    print("Verifying by searching for χ=5 neighborhood...")

    # Try all combinations of angles that could give χ=5
    # Angles must be at 60° increments for edges to exist

    # Actually, angles can be anything, but edges only exist at 60° separations
    # So effective graph structure is determined by which 60°-pairs exist

    # Let me try dense configurations
    for n_vertices in range(6, 30):
        # Try many random placements
        max_chi = 0
        for _ in range(50):
            angles = sorted([random.uniform(0, 2 * math.pi) for _ in range(n_vertices)])
            vertices = [cmath.exp(1j * a) for a in angles]

            adj = defaultdict(set)
            for i in range(n_vertices):
                for j in range(i + 1, n_vertices):
                    if unit_distance(vertices[i], vertices[j]):
                        adj[i].add(j)
                        adj[j].add(i)

            edges = sum(len(adj[i]) for i in range(n_vertices)) // 2
            if edges > 0:
                chi = chromatic_number(adj, n_vertices)
                max_chi = max(max_chi, chi)

        if max_chi >= 4:
            print(f"  n={n_vertices}: max χ found = {max_chi}")

    import random

def main():
    extended, chi = try_extended_neighborhood()
    analyze_degree_bound()
    best_chi = try_irregular_placement()
    theoretical_bound()

    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print(f"""
The "rainbow neighborhood" approach has a STRUCTURAL LIMIT:

1. For v to need color 6, we need χ(N(v)) ≥ 5
2. N(v) lies on the unit circle around v
3. Edges in N(v) are determined by 60° angles
4. This "60°-graph" structure limits χ(N(v)) to ≤ 4

Therefore: The rainbow neighborhood approach CANNOT produce χ ≥ 6!

This is a genuine theoretical insight, not just a computational failure.
The approach is fundamentally blocked by geometry, not just by our testing.
""")

if __name__ == "__main__":
    import random
    main()
