#!/usr/bin/env python3
"""
Analyze the hub vertex (degree 36) and its neighborhood
This might reveal the core structure that forces 5-chromaticity
"""

from collections import defaultdict, Counter
from itertools import combinations

def parse_graph(filename):
    vertices = set()
    edges = set()
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
                    edges.add(tuple(sorted([v, u])))
                    adj[v].add(u)
                    adj[u].add(v)

    return vertices, edges, adj

def analyze_hub(adj, vertices):
    # Find the hub (highest degree vertex)
    degrees = {v: len(adj[v]) for v in vertices}
    hub = max(degrees, key=degrees.get)

    print(f"HUB VERTEX: {hub}")
    print(f"  Degree: {degrees[hub]}")
    print(f"  Neighbors: {sorted(adj[hub])}")

    # Analyze the hub's neighborhood
    neighbors = adj[hub]

    # How many edges within the neighborhood?
    internal_edges = sum(1 for u, v in combinations(neighbors, 2) if v in adj[u])
    max_internal = len(neighbors) * (len(neighbors) - 1) // 2

    print(f"\n  Neighborhood internal edges: {internal_edges}/{max_internal}")
    print(f"  Internal density: {internal_edges/max_internal:.4f}")

    # Find triangles involving the hub
    hub_triangles = []
    for u in neighbors:
        for v in neighbors:
            if u < v and v in adj[u]:
                hub_triangles.append((hub, u, v))

    print(f"  Triangles containing hub: {len(hub_triangles)}")

    # Degree distribution of neighbors
    neighbor_degrees = [degrees[n] for n in neighbors]
    print(f"\n  Neighbor degree stats:")
    print(f"    Min: {min(neighbor_degrees)}")
    print(f"    Max: {max(neighbor_degrees)}")
    print(f"    Avg: {sum(neighbor_degrees)/len(neighbor_degrees):.1f}")

    # Find second-order neighbors (2-hop from hub)
    second_order = set()
    for n in neighbors:
        second_order.update(adj[n])
    second_order -= neighbors
    second_order -= {hub}

    print(f"\n  2-hop neighborhood size: {len(second_order)}")
    print(f"  Total vertices within 2 hops: {1 + len(neighbors) + len(second_order)}")

    # This is potentially the "core" that forces 5-chromaticity!
    core_size = 1 + len(neighbors) + len(second_order)
    print(f"\n  If hub + 2-hop neighborhood is the core:")
    print(f"    Core covers {core_size}/{len(vertices)} = {100*core_size/len(vertices):.1f}% of graph")

    return hub, neighbors, second_order

def analyze_other_high_degree(adj, vertices, top_n=10):
    degrees = {v: len(adj[v]) for v in vertices}
    top_vertices = sorted(degrees, key=degrees.get, reverse=True)[:top_n]

    print(f"\nTOP {top_n} HIGHEST DEGREE VERTICES:")
    for i, v in enumerate(top_vertices):
        print(f"  {i+1}. Vertex {v}: degree {degrees[v]}")

    # Are these vertices connected to each other?
    print(f"\nConnections among top {top_n}:")
    for i, v in enumerate(top_vertices):
        connections = sum(1 for u in top_vertices if u in adj[v] and u != v)
        print(f"  Vertex {v}: connected to {connections}/{top_n-1} other top vertices")

    return top_vertices

def can_4_color_subgraph(adj, vertices):
    """Try to 4-color a subgraph"""
    vertex_list = list(vertices)
    n = len(vertex_list)
    coloring = [-1] * n
    v_to_idx = {v: i for i, v in enumerate(vertex_list)}

    def backtrack(idx):
        if idx == n:
            return True
        v = vertex_list[idx]
        neighbor_colors = {coloring[v_to_idx[u]] for u in adj[v] if u in vertices and v_to_idx[u] < idx}
        for c in range(4):
            if c not in neighbor_colors:
                coloring[idx] = c
                if backtrack(idx + 1):
                    return True
                coloring[idx] = -1
        return False

    return backtrack(0)

def find_minimal_non_4_colorable(adj, hub, neighbors, vertices):
    """
    Try to find a minimal subgraph that's not 4-colorable.
    Start from hub + neighbors and try to reduce.
    """
    print("\nSEARCHING FOR MINIMAL NON-4-COLORABLE CORE...")

    # Start with hub + neighbors
    core = {hub} | neighbors
    print(f"  Starting core size: {len(core)}")

    # Check if hub + neighbors is 4-colorable
    sub_adj = defaultdict(set)
    for v in core:
        sub_adj[v] = adj[v] & core

    if can_4_color_subgraph(sub_adj, core):
        print(f"  Hub + neighbors IS 4-colorable")
        print(f"  Need to expand the core...")

        # Add 2-hop neighbors incrementally
        second_order = set()
        for n in neighbors:
            second_order.update(adj[n])
        second_order -= core

        for v in list(second_order)[:50]:  # Try adding up to 50 more
            core.add(v)
            sub_adj = defaultdict(set)
            for u in core:
                sub_adj[u] = adj[u] & core

            if not can_4_color_subgraph(sub_adj, core):
                print(f"  Found non-4-colorable at size {len(core)} (added vertex {v})")
                break
        else:
            print(f"  Still 4-colorable with {len(core)} vertices")

    else:
        print(f"  Hub + neighbors is NOT 4-colorable!")
        print(f"  This is the core forcing structure!")

        # Try to reduce
        reducible = True
        while reducible:
            reducible = False
            for v in list(core):
                if v == hub:
                    continue
                test_core = core - {v}
                sub_adj = defaultdict(set)
                for u in test_core:
                    sub_adj[u] = adj[u] & test_core

                if not can_4_color_subgraph(sub_adj, test_core):
                    core = test_core
                    reducible = True
                    print(f"    Reduced to {len(core)} vertices")
                    break

        print(f"  Minimal non-4-colorable core: {len(core)} vertices")

    return core

def main():
    print("=" * 70)
    print("HUB ANALYSIS: Finding the core forcing structure")
    print("=" * 70)

    vertices, edges, adj = parse_graph("Hadwiger-Nelson-Project-Data/517.csv")

    hub, neighbors, second_order = analyze_hub(adj, vertices)
    top_vertices = analyze_other_high_degree(adj, vertices)

    # Try to find minimal non-4-colorable subgraph
    minimal_core = find_minimal_non_4_colorable(adj, hub, neighbors, vertices)

    print("\n" + "=" * 70)
    print("KEY FINDINGS")
    print("=" * 70)
    print(f"""
The hub vertex {hub} with degree 36 is likely central to the structure.

If we can identify the MINIMAL non-4-colorable subgraph:
- It would reveal what ACTUALLY forces 5-chromaticity
- It might be much smaller than 517 vertices
- Understanding it could guide construction of 6-chromatic graphs

Current minimal core size: {len(minimal_core)} vertices
""")

if __name__ == "__main__":
    main()
