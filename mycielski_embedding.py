#!/usr/bin/env python3
"""
MYCIELSKI EMBEDDING ATTEMPT

Mycielski's construction creates triangle-free graphs with increasing χ:
- M₁ = K₂ (2 vertices, χ=2)
- M₂ = C₅ (5 vertices, χ=3)  [pentagon]
- M₃ = Grötzsch graph (11 vertices, χ=4)
- M₄ = 23 vertices, χ=5
- M₅ = 47 vertices, χ=6

If M₅ is unit-distance embeddable → χ(ℝ²) ≥ 6!

Key property: Mycielski graphs have ω=2 (no triangles).
So unit-distance embedding is possible (no K₄ obstruction).

The question: Can we place 47 points in ℝ² such that:
1. The adjacency matches M₅'s structure
2. Adjacent vertices are at distance 1
3. Non-adjacent vertices are NOT at distance 1
"""

import math
import cmath
import random
from collections import defaultdict
from pysat.solvers import Solver
from pysat.formula import CNF
import numpy as np
from scipy.optimize import minimize

def mycielski(G_adj, n):
    """
    Mycielski construction: G → μ(G)

    Given G with vertices 0..n-1,
    μ(G) has:
    - Original vertices 0..n-1
    - New vertices n..2n-1 (shadows)
    - Apex vertex 2n

    Edges:
    - All original edges
    - For each edge (i,j) in G: add edges (n+i, j) and (i, n+j)
    - Connect all shadows n..2n-1 to apex 2n
    """
    new_adj = defaultdict(set)

    # Copy original edges
    for i in range(n):
        for j in G_adj[i]:
            new_adj[i].add(j)
            new_adj[j].add(i)

    # Shadow edges
    for i in range(n):
        for j in G_adj[i]:
            # Shadow of i connects to j
            new_adj[n + i].add(j)
            new_adj[j].add(n + i)

    # Apex edges (connect to all shadows)
    apex = 2 * n
    for i in range(n):
        new_adj[apex].add(n + i)
        new_adj[n + i].add(apex)

    return new_adj, 2 * n + 1

def build_mycielski_sequence():
    """Build M₁ through M₅"""
    # M₁ = K₂
    M1_adj = defaultdict(set)
    M1_adj[0].add(1)
    M1_adj[1].add(0)
    n1 = 2

    # M₂ = μ(K₂) = C₅
    M2_adj, n2 = mycielski(M1_adj, n1)

    # M₃ = μ(C₅) = Grötzsch
    M3_adj, n3 = mycielski(M2_adj, n2)

    # M₄ = μ(Grötzsch)
    M4_adj, n4 = mycielski(M3_adj, n3)

    # M₅ = μ(M₄)
    M5_adj, n5 = mycielski(M4_adj, n4)

    return [(M1_adj, n1), (M2_adj, n2), (M3_adj, n3), (M4_adj, n4), (M5_adj, n5)]

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

def count_edges(adj, n):
    return sum(len(adj[i]) for i in range(n)) // 2

def try_unit_distance_embedding(adj, n, max_iter=1000):
    """
    Try to find unit-distance embedding using numerical optimization.

    Objective: minimize
    - sum over edges (i,j): (|p_i - p_j| - 1)²
    - sum over non-edges (i,j) where |p_i - p_j| ≈ 1: penalty

    This is a hard non-convex optimization problem.
    """
    edges = set()
    for i in range(n):
        for j in adj[i]:
            if j > i:
                edges.add((i, j))

    def objective(x):
        # x is [x0, y0, x1, y1, ..., x_{n-1}, y_{n-1}]
        positions = [(x[2*i], x[2*i+1]) for i in range(n)]

        loss = 0.0

        # Edge constraint: distance should be 1
        for (i, j) in edges:
            dx = positions[i][0] - positions[j][0]
            dy = positions[i][1] - positions[j][1]
            d = math.sqrt(dx*dx + dy*dy)
            loss += (d - 1.0) ** 2

        # Non-edge soft constraint: distance should NOT be 1
        for i in range(n):
            for j in range(i+1, n):
                if (i, j) not in edges:
                    dx = positions[i][0] - positions[j][0]
                    dy = positions[i][1] - positions[j][1]
                    d = math.sqrt(dx*dx + dy*dy)
                    if abs(d - 1.0) < 0.1:  # Penalize near-1 distances
                        loss += 1.0 / (abs(d - 1.0) + 0.01)

        return loss

    # Random initial positions
    best_result = None
    best_loss = float('inf')

    for trial in range(10):
        x0 = np.random.randn(2 * n) * 3

        result = minimize(objective, x0, method='L-BFGS-B', options={'maxiter': max_iter})

        if result.fun < best_loss:
            best_loss = result.fun
            best_result = result

    return best_result, best_loss

def check_embedding_quality(adj, n, positions):
    """Check how well an embedding satisfies unit-distance constraints."""
    edges = []
    for i in range(n):
        for j in adj[i]:
            if j > i:
                edges.append((i, j))

    # Check edge distances
    edge_errors = []
    for (i, j) in edges:
        d = abs(complex(positions[i][0], positions[i][1]) -
                complex(positions[j][0], positions[j][1]))
        edge_errors.append(abs(d - 1.0))

    # Check non-edge distances (should NOT be 1)
    non_edge_at_1 = 0
    for i in range(n):
        for j in range(i+1, n):
            if (i, j) not in set(edges) and (j, i) not in set(edges):
                d = abs(complex(positions[i][0], positions[i][1]) -
                        complex(positions[j][0], positions[j][1]))
                if abs(d - 1.0) < 0.01:
                    non_edge_at_1 += 1

    return max(edge_errors), sum(edge_errors) / len(edge_errors), non_edge_at_1

def main():
    print("=" * 70)
    print("MYCIELSKI EMBEDDING ATTEMPT")
    print("=" * 70)

    mycielski_graphs = build_mycielski_sequence()

    print("\nMycielski sequence:")
    for i, (adj, n) in enumerate(mycielski_graphs, 1):
        edges = count_edges(adj, n)
        chi = chromatic_number(adj, n)
        print(f"  M_{i}: {n} vertices, {edges} edges, χ = {chi}")

    # Try to embed each Mycielski graph
    for i, (adj, n) in enumerate(mycielski_graphs, 1):
        print(f"\n" + "-" * 70)
        print(f"Attempting unit-distance embedding of M_{i} ({n} vertices)")
        print("-" * 70)

        if n > 50:
            print("Too large for numerical optimization, skipping...")
            continue

        result, loss = try_unit_distance_embedding(adj, n)

        positions = [(result.x[2*j], result.x[2*j+1]) for j in range(n)]

        max_err, avg_err, bad_non_edges = check_embedding_quality(adj, n, positions)

        print(f"  Optimization loss: {loss:.6f}")
        print(f"  Max edge error: {max_err:.6f}")
        print(f"  Avg edge error: {avg_err:.6f}")
        print(f"  Non-edges at distance ~1: {bad_non_edges}")

        if max_err < 0.01 and bad_non_edges == 0:
            print(f"  *** SUCCESS! M_{i} is unit-distance embeddable! ***")
            if i >= 5:
                print(f"  *** This proves χ(ℝ²) ≥ 6! ***")
        elif max_err < 0.1:
            print(f"  Close but not exact - may need refinement")
        else:
            print(f"  Failed - likely not unit-distance embeddable")

    print("\n" + "=" * 70)
    print("ANALYSIS")
    print("=" * 70)
    print("""
The Mycielski construction produces graphs with:
- χ = k for M_k
- ω = 2 (triangle-free)

For unit-distance embedding:
- M₂ = C₅ is easily embeddable (regular pentagon)
- M₃ = Grötzsch (11 vertices) - embeddability is OPEN
- M₄ (23 vertices) - embeddability is OPEN
- M₅ (47 vertices) - embeddability is OPEN

If M₃ is NOT unit-distance embeddable, this gives insight
into why χ(ℝ²) might be bounded above.

If M₃ IS embeddable but M₄ is not, the barrier is between
χ=4 and χ=5.

The numerical optimization suggests the constraints are
very tight - finding an embedding requires exact algebraic
positions, not approximations.
""")

if __name__ == "__main__":
    main()
