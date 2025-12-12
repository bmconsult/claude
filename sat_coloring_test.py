#!/usr/bin/env python3
"""
SAT-based graph coloring test.
This is MUCH more powerful than backtracking.
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

def is_k_colorable_sat(adj, vertices, k):
    """
    Check if graph is k-colorable using SAT.

    Variables: x_{v,c} means vertex v has color c
    Constraints:
    1. Each vertex has at least one color: OR_c(x_{v,c})
    2. Each vertex has at most one color: NOT(x_{v,c} AND x_{v,c'}) for c != c'
    3. Adjacent vertices have different colors: NOT(x_{v,c} AND x_{u,c})
    """
    vertex_list = sorted(vertices)
    n = len(vertex_list)
    v_to_idx = {v: i for i, v in enumerate(vertex_list)}

    # Variable numbering: var(v, c) = v_idx * k + c + 1
    def var(v_idx, c):
        return v_idx * k + c + 1

    cnf = CNF()

    # Constraint 1: Each vertex has at least one color
    for i in range(n):
        clause = [var(i, c) for c in range(k)]
        cnf.append(clause)

    # Constraint 2: Each vertex has at most one color
    for i in range(n):
        for c1 in range(k):
            for c2 in range(c1 + 1, k):
                cnf.append([-var(i, c1), -var(i, c2)])

    # Constraint 3: Adjacent vertices have different colors
    for v in vertex_list:
        v_idx = v_to_idx[v]
        for u in adj[v]:
            if u in vertices and u > v:  # Only add each edge once
                u_idx = v_to_idx[u]
                for c in range(k):
                    cnf.append([-var(v_idx, c), -var(u_idx, c)])

    # Solve
    with Solver(name='g4') as solver:
        solver.append_formula(cnf)
        result = solver.solve()

        if result:
            model = solver.get_model()
            # Extract coloring
            coloring = {}
            for i, v in enumerate(vertex_list):
                for c in range(k):
                    if model[var(i, c) - 1] > 0:
                        coloring[v] = c
                        break
            return True, coloring
        else:
            return False, None

def get_triangle_neighborhood(adj, triangle):
    neighborhood = set(triangle)
    for h in triangle:
        neighborhood.update(adj[h])
    return neighborhood

def main():
    print("=" * 70)
    print("SAT-BASED COLORING TESTS")
    print("=" * 70)

    vertices, adj = parse_graph("Hadwiger-Nelson-Project-Data/517.csv")
    print(f"Full graph: {len(vertices)} vertices")

    main_hub = 1
    triangle1 = [267, 322, 328]
    triangle2 = [271, 320, 332]

    t1_neighborhood = get_triangle_neighborhood(adj, triangle1)
    t2_neighborhood = get_triangle_neighborhood(adj, triangle2)
    main_hub_neighborhood = {main_hub} | adj[main_hub]

    # Test 1: Core (both triangles + main hub)
    print("\n" + "=" * 50)
    print("TEST 1: Core (both triangles + main hub) - 145 vertices")
    vertices_core = t1_neighborhood | t2_neighborhood | main_hub_neighborhood
    adj_core = defaultdict(set)
    for v in vertices_core:
        adj_core[v] = adj[v] & vertices_core

    for k in [3, 4, 5]:
        start = time.time()
        result, coloring = is_k_colorable_sat(adj_core, vertices_core, k)
        elapsed = time.time() - start
        status = f"{k}-colorable: YES" if result else f"{k}-colorable: NO"
        print(f"  {status} ({elapsed:.2f}s)")

    # Test 2: Both triangles without main hub
    print("\n" + "=" * 50)
    print("TEST 2: Both triangles only - 120 vertices")
    vertices_triangles = t1_neighborhood | t2_neighborhood
    adj_triangles = defaultdict(set)
    for v in vertices_triangles:
        adj_triangles[v] = adj[v] & vertices_triangles

    for k in [3, 4, 5]:
        start = time.time()
        result, _ = is_k_colorable_sat(adj_triangles, vertices_triangles, k)
        elapsed = time.time() - start
        status = f"{k}-colorable: YES" if result else f"{k}-colorable: NO"
        print(f"  {status} ({elapsed:.2f}s)")

    # Test 3: Full graph
    print("\n" + "=" * 50)
    print("TEST 3: Full graph - 517 vertices")

    for k in [3, 4, 5]:
        start = time.time()
        result, _ = is_k_colorable_sat(adj, vertices, k)
        elapsed = time.time() - start
        status = f"{k}-colorable: YES" if result else f"{k}-colorable: NO"
        print(f"  {status} ({elapsed:.2f}s)")

    # Test 4: Various subgraph sizes
    print("\n" + "=" * 50)
    print("TEST 4: Random subgraphs at different sizes")

    import random
    vertex_list = list(vertices)

    for size in [200, 250, 300, 350, 400, 450]:
        print(f"\n  Size {size}:")
        colorable_count = 0
        for trial in range(10):
            sample = set(random.sample(vertex_list, size))
            sample_adj = defaultdict(set)
            for v in sample:
                sample_adj[v] = adj[v] & sample

            result, _ = is_k_colorable_sat(sample_adj, sample, 4)
            if result:
                colorable_count += 1

        print(f"    4-colorable: {colorable_count}/10")

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

if __name__ == "__main__":
    main()
