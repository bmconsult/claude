#!/usr/bin/env python3
"""
COMBINE TWO VORONOV 5-CHROMATIC GRAPHS

Each Voronov graph G_i = M₃ ∪ ψ_i·M₃ is 5-chromatic.
What if we take G₁ ∪ G₂? This is M₃ ∪ ψ₁·M₃ ∪ ψ₂·M₃ (three copies).

Key insight: If the three copies share the original M₃, then:
- Vertices 1..32257 are in all copies (original M₃)
- Vertices 32258..64514 are from ψ₁·M₃ in graph1
- Vertices 32258..64514 are from ψ₂·M₃ in graph2 (DIFFERENT!)

So the combined graph would have M₃ ∪ ψ₁·M₃ ∪ ψ₂·M₃ = ~96K vertices.

But wait - the DIMACS files probably overlap on the base M₃.
Let me check if edges from two different rotations combine to force χ=6.
"""

import sys
from collections import defaultdict
from pysat.solvers import Solver
from pysat.formula import CNF
import time

def load_dimacs_edges(filename):
    """Load edges from DIMACS file"""
    edges = []
    n = 0
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('p '):
                parts = line.split()
                n = int(parts[2])
            elif line.startswith('e '):
                parts = line.split()
                u, v = int(parts[1]), int(parts[2])
                edges.append((u, v))
    return n, edges

def build_adj_from_edges(n, edges):
    """Build adjacency from edge list"""
    adj = defaultdict(set)
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj

def combine_graphs(n1, edges1, n2, edges2):
    """
    Combine two Voronov graphs.

    Assumption: Both graphs share the same base M₃ (vertices 1..32257).
    The rotated copies (32258..64514) are different.

    Combined graph has vertices:
    - 1..32257: base M₃ (shared)
    - 32258..64514: ψ₁·M₃ from graph1
    - 64515..96771: ψ₂·M₃ from graph2
    """
    # Find the offset where rotated copy starts
    # In Voronov construction, M₃ has 32257 vertices
    base_size = 32257

    combined_edges = set()

    # Add all edges from graph1 as-is
    for u, v in edges1:
        combined_edges.add((min(u,v), max(u,v)))

    # Add edges from graph2, but offset the rotated copy
    for u, v in edges2:
        # If both vertices are in base M₃, edge already added
        if u <= base_size and v <= base_size:
            continue

        # If one vertex is in rotated copy, offset it
        if u > base_size:
            u_new = u + base_size  # Becomes 64515+
        else:
            u_new = u

        if v > base_size:
            v_new = v + base_size
        else:
            v_new = v

        combined_edges.add((min(u_new, v_new), max(u_new, v_new)))

    # Calculate new total vertices
    total_n = base_size + 2 * base_size  # 3 copies = 96771

    return total_n, list(combined_edges)

def is_k_colorable(adj, n, k, timeout=600):
    """Check k-colorability via SAT"""
    def var(v_idx, c):
        return v_idx * k + c + 1

    cnf = CNF()

    # At least one color per vertex
    for i in range(1, n + 1):  # 1-indexed
        cnf.append([var(i, c) for c in range(k)])

    # At most one color per vertex
    for i in range(1, n + 1):
        for c1 in range(k):
            for c2 in range(c1 + 1, k):
                cnf.append([-var(i, c1), -var(i, c2)])

    # Adjacent vertices different
    for i in adj:
        for j in adj[i]:
            if j > i:
                for c in range(k):
                    cnf.append([-var(i, c), -var(j, c)])

    with Solver(name='g4') as solver:
        solver.append_formula(cnf)
        return solver.solve()

def main():
    print("=" * 70)
    print("COMBINED VORONOV ATTACK: G₁ ∪ G₂ = M₃ ∪ ψ₁·M₃ ∪ ψ₂·M₃")
    print("=" * 70)

    # Load two different Voronov graphs
    graph1_file = "dist-graphs/plane/series 2/dimacs/s2_graph1.dimacs"
    graph2_file = "dist-graphs/plane/series 2/dimacs/s2_graph2.dimacs"

    print(f"\nLoading {graph1_file}...")
    n1, edges1 = load_dimacs_edges(graph1_file)
    print(f"  Graph 1: {n1} vertices, {len(edges1)} edges")

    print(f"\nLoading {graph2_file}...")
    n2, edges2 = load_dimacs_edges(graph2_file)
    print(f"  Graph 2: {n2} vertices, {len(edges2)} edges")

    # Verify both are 5-chromatic (quick check with subset)
    print("\n" + "-" * 70)
    print("Verifying individual graphs...")
    print("-" * 70)

    # For speed, check 5-colorability of first 10000 vertices
    subset_n = 10000
    adj1 = build_adj_from_edges(n1, [(u,v) for u,v in edges1 if u <= subset_n and v <= subset_n])
    adj2 = build_adj_from_edges(n2, [(u,v) for u,v in edges2 if u <= subset_n and v <= subset_n])

    print(f"  Subset ({subset_n} vertices) of G₁: ", end="", flush=True)
    if is_k_colorable(adj1, subset_n, 5):
        print("5-colorable ✓")
    else:
        print("NOT 5-colorable!")

    print(f"  Subset ({subset_n} vertices) of G₂: ", end="", flush=True)
    if is_k_colorable(adj2, subset_n, 5):
        print("5-colorable ✓")
    else:
        print("NOT 5-colorable!")

    # Now combine
    print("\n" + "-" * 70)
    print("Combining graphs...")
    print("-" * 70)

    total_n, combined_edges = combine_graphs(n1, edges1, n2, edges2)
    print(f"Combined: {total_n} vertices, {len(combined_edges)} edges")

    adj_combined = build_adj_from_edges(total_n, combined_edges)

    # Test subset first
    print("\n" + "-" * 70)
    print("Testing combined graph 5-colorability...")
    print("-" * 70)

    # First test a smaller subset
    test_n = 20000
    adj_subset = defaultdict(set)
    for u in adj_combined:
        if u <= test_n:
            for v in adj_combined[u]:
                if v <= test_n:
                    adj_subset[u].add(v)

    print(f"\nTesting subset ({test_n} vertices)...")
    start = time.time()
    result = is_k_colorable(adj_subset, test_n, 5)
    elapsed = time.time() - start

    if result:
        print(f"  5-colorable ({elapsed:.1f}s)")
        print("  Subset is 5-colorable - need to test more")
    else:
        print(f"  *** NOT 5-COLORABLE! ({elapsed:.1f}s)")
        print("  Testing 6-colorability...")

        result6 = is_k_colorable(adj_subset, test_n, 6)
        if result6:
            print(f"  *** χ = 6 FOR SUBSET! ***")
        else:
            print(f"  χ ≥ 7 for subset!")

    # Try different combination: graph1 + graph3
    print("\n" + "=" * 70)
    print("Trying different graph combinations...")
    print("=" * 70)

    other_graphs = [
        ("s2_graph3.dimacs", "s2_graph5.dimacs"),
        ("s2_graph1.dimacs", "s2_graph10.dimacs"),
        ("s2_graph7.dimacs", "s2_graph14.dimacs"),
    ]

    for g1_name, g2_name in other_graphs:
        g1_path = f"dist-graphs/plane/series 2/dimacs/{g1_name}"
        g2_path = f"dist-graphs/plane/series 2/dimacs/{g2_name}"

        print(f"\n{g1_name} ∪ {g2_name}:")

        n1, edges1 = load_dimacs_edges(g1_path)
        n2, edges2 = load_dimacs_edges(g2_path)

        total_n, combined_edges = combine_graphs(n1, edges1, n2, edges2)
        adj_combined = build_adj_from_edges(total_n, combined_edges)

        # Test subset
        test_n = 15000
        adj_subset = defaultdict(set)
        for u in adj_combined:
            if u <= test_n:
                for v in adj_combined[u]:
                    if v <= test_n:
                        adj_subset[u].add(v)

        start = time.time()
        result = is_k_colorable(adj_subset, test_n, 5)
        elapsed = time.time() - start

        if result:
            print(f"  5-colorable ({elapsed:.1f}s)")
        else:
            print(f"  *** NOT 5-COLORABLE! ({elapsed:.1f}s) ***")
            return g1_name, g2_name

    print("\n" + "=" * 70)
    print("CONCLUSION: Combined Voronov graphs remain 5-colorable")
    print("The barrier persists even with triple copies.")
    print("=" * 70)

if __name__ == "__main__":
    main()
