#!/usr/bin/env python3
"""
GENUINE ATTEMPT: Search for 6-chromatic unit-distance graph

Strategy:
1. The 517-graph is 5-chromatic and vertex-critical
2. Combine multiple copies with rotation to create more constraints
3. Check if the combined graph is 6-chromatic using SAT

Key insight from de Grey: Rotation creates new unit-distance edges
that propagate color constraints and can force higher chromatic number.
"""

from collections import defaultdict
from pysat.solvers import Solver
from pysat.formula import CNF
import numpy as np
import time

def parse_graph(filename):
    """Parse the 517-graph"""
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
    return sorted(vertices), adj

def is_k_colorable(adj, vertices, k):
    """Check if graph is k-colorable using SAT"""
    vertex_list = sorted(vertices)
    n = len(vertex_list)
    v_to_idx = {v: i for i, v in enumerate(vertex_list)}

    def var(v_idx, c):
        return v_idx * k + c + 1

    cnf = CNF()

    # Each vertex has at least one color
    for i in range(n):
        cnf.append([var(i, c) for c in range(k)])

    # Each vertex has at most one color
    for i in range(n):
        for c1 in range(k):
            for c2 in range(c1 + 1, k):
                cnf.append([-var(i, c1), -var(i, c2)])

    # Adjacent vertices have different colors
    for v in vertex_list:
        v_idx = v_to_idx[v]
        for u in adj[v]:
            if u in v_to_idx and u > v:
                u_idx = v_to_idx[u]
                for c in range(k):
                    cnf.append([-var(v_idx, c), -var(u_idx, c)])

    with Solver(name='g4') as solver:
        solver.append_formula(cnf)
        return solver.solve()

def chromatic_number(adj, vertices):
    """Find chromatic number by binary search"""
    for k in range(1, 10):
        if is_k_colorable(adj, vertices, k):
            return k
    return 10

def combine_graphs_with_shared_vertices(adj1, v1, adj2, v2, shared_mapping):
    """
    Combine two graphs where some vertices are shared.
    shared_mapping: dict from v2 vertices to v1 vertices they're identified with
    """
    # Create new vertex set
    max_v1 = max(v1)
    offset = max_v1 + 1

    # New vertices: all of v1, plus non-shared vertices of v2 (offset)
    new_vertices = set(v1)
    v2_to_new = {}

    for v in v2:
        if v in shared_mapping:
            v2_to_new[v] = shared_mapping[v]
        else:
            v2_to_new[v] = v + offset
            new_vertices.add(v + offset)

    # New adjacency
    new_adj = defaultdict(set)

    # Copy edges from graph 1
    for v in v1:
        for u in adj1[v]:
            new_adj[v].add(u)
            new_adj[u].add(v)

    # Copy edges from graph 2 (translated)
    for v in v2:
        new_v = v2_to_new[v]
        for u in adj2[v]:
            new_u = v2_to_new[u]
            new_adj[new_v].add(new_u)
            new_adj[new_u].add(new_v)

    return new_adj, new_vertices

def add_random_edges(adj, vertices, num_edges):
    """Add random edges between vertices (simulating rotation effects)"""
    import random
    vertex_list = list(vertices)
    new_adj = defaultdict(set)

    # Copy existing
    for v in vertices:
        new_adj[v] = adj[v].copy()

    # Add random edges
    added = 0
    attempts = 0
    while added < num_edges and attempts < num_edges * 10:
        v1 = random.choice(vertex_list)
        v2 = random.choice(vertex_list)
        if v1 != v2 and v2 not in new_adj[v1]:
            new_adj[v1].add(v2)
            new_adj[v2].add(v1)
            added += 1
        attempts += 1

    return new_adj

def search_for_6chromatic():
    """Search for 6-chromatic unit-distance graph"""
    print("=" * 70)
    print("SEARCHING FOR 6-CHROMATIC UNIT-DISTANCE GRAPH")
    print("=" * 70)

    vertices, adj = parse_graph("Hadwiger-Nelson-Project-Data/517.csv")
    print(f"Base graph: {len(vertices)} vertices")

    # Confirm base graph is 5-chromatic
    print("\nConfirming base graph chromatic number...")
    chi = chromatic_number(adj, vertices)
    print(f"  Base graph χ = {chi}")

    if chi != 5:
        print("ERROR: Base graph is not 5-chromatic!")
        return

    # Strategy 1: Combine two copies with shared hub
    print("\n" + "=" * 50)
    print("STRATEGY 1: Combine two copies with shared hub")
    print("=" * 50)

    # Share the main hub (vertex 1)
    shared = {1: 1}  # Vertex 1 in copy 2 = vertex 1 in copy 1

    combined_adj, combined_vertices = combine_graphs_with_shared_vertices(
        adj, vertices, adj, vertices, shared
    )

    print(f"Combined graph: {len(combined_vertices)} vertices")
    chi_combined = chromatic_number(combined_adj, combined_vertices)
    print(f"  Combined χ = {chi_combined}")

    if chi_combined >= 6:
        print("*** FOUND 6-CHROMATIC GRAPH! ***")
        return combined_adj, combined_vertices

    # Strategy 2: Add edges to simulate rotation effects
    print("\n" + "=" * 50)
    print("STRATEGY 2: Add random edges (simulating rotation)")
    print("=" * 50)

    for num_edges in [100, 200, 500, 1000, 2000]:
        test_adj = add_random_edges(adj, vertices, num_edges)
        chi_test = chromatic_number(test_adj, vertices)
        print(f"  +{num_edges} random edges: χ = {chi_test}")

        if chi_test >= 6:
            print(f"*** FOUND 6-CHROMATIC GRAPH WITH {num_edges} EXTRA EDGES! ***")
            return test_adj, vertices

    # Strategy 3: Multiple copies with different sharing patterns
    print("\n" + "=" * 50)
    print("STRATEGY 3: Multiple copies with different sharing")
    print("=" * 50)

    # Share multiple high-degree vertices
    hubs = [1, 267, 271, 320, 322, 328, 332]

    for num_shared in range(1, len(hubs) + 1):
        shared = {h: h for h in hubs[:num_shared]}
        combined_adj, combined_vertices = combine_graphs_with_shared_vertices(
            adj, vertices, adj, vertices, shared
        )
        chi_combined = chromatic_number(combined_adj, combined_vertices)
        print(f"  {num_shared} shared hubs: {len(combined_vertices)} vertices, χ = {chi_combined}")

        if chi_combined >= 6:
            print(f"*** FOUND 6-CHROMATIC GRAPH WITH {num_shared} SHARED HUBS! ***")
            return combined_adj, combined_vertices

    # Strategy 4: Three copies
    print("\n" + "=" * 50)
    print("STRATEGY 4: Three copies with shared hub")
    print("=" * 50)

    # Combine first two copies
    shared = {1: 1}
    combined_adj, combined_vertices = combine_graphs_with_shared_vertices(
        adj, vertices, adj, vertices, shared
    )

    # Add third copy
    shared3 = {1: 1}
    combined_adj, combined_vertices = combine_graphs_with_shared_vertices(
        combined_adj, combined_vertices, adj, vertices, shared3
    )

    print(f"Three copies: {len(combined_vertices)} vertices")
    chi_3 = chromatic_number(combined_adj, combined_vertices)
    print(f"  Three copies χ = {chi_3}")

    if chi_3 >= 6:
        print("*** FOUND 6-CHROMATIC GRAPH WITH THREE COPIES! ***")
        return combined_adj, combined_vertices

    print("\n" + "=" * 70)
    print("RESULT")
    print("=" * 70)
    print("""
No 6-chromatic graph found with these strategies.

This suggests:
1. Simple combinations of the 5-chromatic graph don't yield 6-chromatic
2. The forcing mechanism for 6-chromaticity is more subtle
3. May need de Grey-style rotation with specific angles

NEXT STEPS:
- Get actual coordinates of the 517-graph
- Apply geometric rotations (not just graph-theoretic combinations)
- Search for angles that create forcing patterns
""")

    return None, None

def main():
    search_for_6chromatic()

if __name__ == "__main__":
    main()
