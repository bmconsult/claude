#!/usr/bin/env python3
"""
DIRECT CONSTRUCTION: Build toward χ=6 from scratch

Key insight from analysis:
- Local 5-neighbor rainbow is geometrically blocked
- Need GLOBAL forcing that emerges from graph structure

Strategy: Greedy construction maximizing chromatic number
1. Start with Moser spindle (χ=4)
2. Add vertices that increase constraint
3. Track chromatic number at each step
4. Goal: reach χ=6 without requiring 5 neighbors at once
"""

import math
import cmath
import random
from collections import defaultdict
from pysat.solvers import Solver
from pysat.formula import CNF

def unit_dist(z1, z2, tol=1e-9):
    return abs(abs(z1 - z2) - 1.0) < tol

def build_adj(vertices, tol=1e-9):
    n = len(vertices)
    adj = defaultdict(set)
    for i in range(n):
        for j in range(i + 1, n):
            if unit_dist(vertices[i], vertices[j], tol):
                adj[i].add(j)
                adj[j].add(i)
    return adj

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

def moser_spindle():
    """The Moser spindle: 7 vertices, χ=4"""
    # Standard embedding
    v = [
        complex(0, 0),
        complex(1, 0),
        complex(0.5, math.sqrt(3)/2),
        complex(0.5, -math.sqrt(3)/2),
        complex(1.5, math.sqrt(3)/2),
        complex(1.5, -math.sqrt(3)/2),
        complex(2, 0),
    ]
    return v

def find_unit_distance_points(vertices, min_neighbors=2):
    """Find new points at unit distance from multiple existing vertices"""
    candidates = []
    n = len(vertices)

    # For each pair, find intersection of their unit circles
    for i in range(n):
        for j in range(i + 1, n):
            d = abs(vertices[j] - vertices[i])
            if d > 2.0 or d < 1e-9:
                continue

            mid = (vertices[i] + vertices[j]) / 2
            h_sq = 1 - (d/2)**2
            if h_sq < 0:
                continue
            h = math.sqrt(h_sq)
            perp = (vertices[j] - vertices[i]) * 1j / d

            for p in [mid + h*perp, mid - h*perp]:
                # Count how many existing vertices are at unit distance
                neighbors = sum(1 for v in vertices if unit_dist(p, v))
                if neighbors >= min_neighbors:
                    # Check not duplicate
                    if all(abs(p - v) > 0.01 for v in vertices):
                        candidates.append((p, neighbors))

    return candidates

def greedy_expand(vertices, target_chi=6, max_vertices=200):
    """Greedily add vertices to increase chromatic number"""
    current = list(vertices)
    adj = build_adj(current)
    chi = chromatic(adj, len(current))

    print(f"Start: {len(current)} vertices, χ={chi}")

    iterations = 0
    while chi < target_chi and len(current) < max_vertices:
        iterations += 1

        # Find candidate points
        candidates = find_unit_distance_points(current, min_neighbors=2)

        if not candidates:
            # Try with lower neighbor requirement
            candidates = find_unit_distance_points(current, min_neighbors=1)

        if not candidates:
            print(f"  No more candidates at iteration {iterations}")
            break

        # Sort by number of neighbors (more = more constraint)
        candidates.sort(key=lambda x: -x[1])

        # Try adding best candidates
        improved = False
        for p, neighbors in candidates[:20]:  # Try top 20
            test = current + [p]
            test_adj = build_adj(test)
            test_chi = chromatic(test_adj, len(test))

            if test_chi > chi:
                current = test
                adj = test_adj
                chi = test_chi
                print(f"  +vertex (deg={neighbors}): {len(current)} vertices, χ={chi}")
                improved = True
                break
            elif test_chi == chi and len(test) < max_vertices:
                # Accept if maintains chi and adds edges
                current = test
                adj = test_adj
                # Don't break - keep looking for improvement

        if not improved:
            # Add highest-degree candidate anyway
            p, neighbors = candidates[0]
            current.append(p)
            adj = build_adj(current)

            if iterations % 10 == 0:
                chi = chromatic(adj, len(current))
                print(f"  Iteration {iterations}: {len(current)} vertices, χ={chi}")

    return current, chi

def main():
    print("=" * 60)
    print("DIRECT CONSTRUCTION: Building toward χ=6")
    print("=" * 60)

    # Start with Moser spindle
    vertices = moser_spindle()
    adj = build_adj(vertices)
    chi = chromatic(adj, len(vertices))
    print(f"\nMoser spindle: {len(vertices)} vertices, χ={chi}")

    # Greedy expansion
    print("\n" + "-" * 60)
    print("Greedy expansion...")
    print("-" * 60)

    final_vertices, final_chi = greedy_expand(vertices, target_chi=6, max_vertices=150)

    print(f"\nFinal: {len(final_vertices)} vertices, χ={final_chi}")

    if final_chi >= 6:
        print("\n*** SUCCESS: Constructed χ≥6 graph! ***")
    elif final_chi == 5:
        print("\nReached χ=5 - hit the known barrier")
        print("Trying different seed configurations...")

        # Try starting from different base structures
        for trial in range(5):
            # Random perturbation of Moser spindle
            base = moser_spindle()
            # Add some random unit-distance points
            for _ in range(3):
                angle = random.uniform(0, 2*math.pi)
                base.append(cmath.exp(1j * angle))

            vertices, chi = greedy_expand(base, target_chi=6, max_vertices=100)
            print(f"  Trial {trial+1}: {len(vertices)} vertices, χ={chi}")

            if chi >= 6:
                print("*** FOUND χ≥6! ***")
                return vertices, chi

    return final_vertices, final_chi

if __name__ == "__main__":
    result = main()
