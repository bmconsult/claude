#!/usr/bin/env python3
"""
Verify the graph is vertex-critical:
Removing ANY vertex should make it 4-colorable.
"""

from collections import defaultdict
from pysat.solvers import Solver
from pysat.formula import CNF
import time

def parse_graph(filename):
    vertices = set()
    adj = defaultdict(set)
    with open(filename, 'r') as f:
        next(f)
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) < 2:
                continue
            v = int(parts[0])
            vertices.add(v)
            edge_str = parts[1]
            if edge_str:
                neighbors = [int(x) for x in edge_str.split(';') if x]
                for u in neighbors:
                    vertices.add(u)
                    adj[v].add(u)
                    adj[u].add(v)
    return vertices, adj

def is_4_colorable_sat(adj, vertices):
    """Check if graph is 4-colorable using SAT."""
    k = 4
    vertex_list = sorted(vertices)
    n = len(vertex_list)
    v_to_idx = {v: i for i, v in enumerate(vertex_list)}

    def var(v_idx, c):
        return v_idx * k + c + 1

    cnf = CNF()

    for i in range(n):
        cnf.append([var(i, c) for c in range(k)])

    for i in range(n):
        for c1 in range(k):
            for c2 in range(c1 + 1, k):
                cnf.append([-var(i, c1), -var(i, c2)])

    for v in vertex_list:
        v_idx = v_to_idx[v]
        for u in adj[v]:
            if u in vertices and u > v:
                u_idx = v_to_idx[u]
                for c in range(k):
                    cnf.append([-var(v_idx, c), -var(u_idx, c)])

    with Solver(name='g4') as solver:
        solver.append_formula(cnf)
        return solver.solve()

def main():
    print("=" * 70)
    print("VERIFYING VERTEX-CRITICALITY")
    print("=" * 70)

    vertices, adj = parse_graph("Hadwiger-Nelson-Project-Data/517.csv")
    print(f"Full graph: {len(vertices)} vertices")

    # First confirm full graph is NOT 4-colorable
    print("\nConfirming full graph is NOT 4-colorable...")
    start = time.time()
    result = is_4_colorable_sat(adj, vertices)
    elapsed = time.time() - start
    print(f"  Full graph 4-colorable: {result} ({elapsed:.1f}s)")

    if result:
        print("ERROR: Full graph IS 4-colorable!")
        return

    # Test removing each vertex
    print(f"\nTesting removal of each vertex...")
    non_critical = []  # Vertices whose removal doesn't help

    start_total = time.time()

    for i, v in enumerate(sorted(vertices)):
        remaining = vertices - {v}
        rem_adj = defaultdict(set)
        for u in remaining:
            rem_adj[u] = adj[u] & remaining

        result = is_4_colorable_sat(rem_adj, remaining)

        if not result:
            non_critical.append(v)
            print(f"  Removing vertex {v}: STILL NOT 4-colorable!")

        if (i + 1) % 50 == 0:
            elapsed = time.time() - start_total
            print(f"  Progress: {i+1}/{len(vertices)} vertices tested ({elapsed:.1f}s)")

    total_time = time.time() - start_total
    print(f"\nTotal time: {total_time:.1f}s")

    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)

    if len(non_critical) == 0:
        print("""
*** THE GRAPH IS VERTEX-CRITICAL! ***

Removing ANY vertex makes the graph 4-colorable.
This is an EXTREMELY tight structure.

IMPLICATIONS:
- Every single vertex is essential for 5-chromaticity
- The graph cannot be reduced without losing the property
- This is optimal in the sense of vertex count
- The forcing mechanism is truly GLOBAL
""")
    else:
        print(f"""
The graph is NOT fully vertex-critical.

Removing these {len(non_critical)} vertices does NOT make it 4-colorable:
{non_critical[:20]}{'...' if len(non_critical) > 20 else ''}

These vertices form a "redundant" set - they can be removed
without affecting 5-chromaticity.
""")

if __name__ == "__main__":
    main()
