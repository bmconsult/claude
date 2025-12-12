#!/usr/bin/env python3
"""
Deep test of the 145-vertex core (both triangles + main hub)
with much longer timeout.
"""

from collections import defaultdict
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

def can_4_color_verbose(adj, vertices, timeout_nodes=5000000):
    """4-coloring check with verbose progress"""
    if len(vertices) < 5:
        return True, {}

    # Use more sophisticated ordering: DSATUR-like
    vertex_list = list(vertices)
    n = len(vertex_list)

    # Start with highest degree vertex
    vertex_list.sort(key=lambda v: -len(adj[v] & vertices))

    coloring = [-1] * n
    v_to_idx = {v: i for i, v in enumerate(vertex_list)}
    nodes_checked = [0]
    max_depth = [0]

    def backtrack(idx):
        nodes_checked[0] += 1
        if idx > max_depth[0]:
            max_depth[0] = idx
            if idx % 20 == 0:
                print(f"    Progress: depth {idx}/{n}, nodes checked: {nodes_checked[0]}", flush=True)

        if nodes_checked[0] > timeout_nodes:
            return None
        if idx == n:
            return True
        v = vertex_list[idx]
        neighbor_colors = set()
        for u in adj[v]:
            if u in vertices:
                ui = v_to_idx.get(u)
                if ui is not None and ui < idx:
                    neighbor_colors.add(coloring[ui])

        for c in range(4):
            if c not in neighbor_colors:
                coloring[idx] = c
                result = backtrack(idx + 1)
                if result is True:
                    return True
                if result is None:
                    return None
                coloring[idx] = -1

        return False

    result = backtrack(0)
    print(f"    Final: depth {max_depth[0]}/{n}, nodes checked: {nodes_checked[0]}")

    if result is True:
        return True, {vertex_list[i]: coloring[i] for i in range(n)}
    elif result is None:
        return None, None
    else:
        return False, None

def get_triangle_neighborhood(adj, triangle):
    neighborhood = set(triangle)
    for h in triangle:
        neighborhood.update(adj[h])
    return neighborhood

def main():
    print("=" * 70)
    print("DEEP TEST: 145-VERTEX CORE COLORABILITY")
    print("=" * 70)

    vertices, adj = parse_graph("Hadwiger-Nelson-Project-Data/517.csv")

    main_hub = 1
    triangle1 = [267, 322, 328]
    triangle2 = [271, 320, 332]

    t1_neighborhood = get_triangle_neighborhood(adj, triangle1)
    t2_neighborhood = get_triangle_neighborhood(adj, triangle2)
    main_hub_neighborhood = {main_hub} | adj[main_hub]

    # Core = both triangles + main hub
    vertices_core = t1_neighborhood | t2_neighborhood | main_hub_neighborhood
    adj_core = defaultdict(set)
    for v in vertices_core:
        adj_core[v] = adj[v] & vertices_core

    print(f"\nCore structure: {len(vertices_core)} vertices")

    # Count edges in core
    edge_count = sum(1 for v in vertices_core for u in adj_core[v] if v < u)
    print(f"Core edges: {edge_count}")

    print(f"\nTesting 4-colorability with 5M node timeout...")
    start = time.time()
    result, coloring = can_4_color_verbose(adj_core, vertices_core, timeout_nodes=5000000)
    elapsed = time.time() - start

    if result is True:
        print(f"\n*** CORE IS 4-COLORABLE! ({elapsed:.1f}s) ***")
        # Verify coloring
        colors_used = set(coloring.values())
        print(f"Colors used: {len(colors_used)}")

        # Check for conflicts
        conflicts = 0
        for v in vertices_core:
            for u in adj_core[v]:
                if coloring[v] == coloring[u]:
                    conflicts += 1
        print(f"Conflicts: {conflicts}")

    elif result is False:
        print(f"\n*** CORE IS NOT 4-COLORABLE! ({elapsed:.1f}s) ***")
        print("This is a key finding - the forcing is in the triangle interaction!")

    else:
        print(f"\n*** TIMEOUT ({elapsed:.1f}s) ***")
        print("The search space is too large even for 5M nodes")

    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)

if __name__ == "__main__":
    main()
