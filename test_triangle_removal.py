#!/usr/bin/env python3
"""
Test hypothesis: Does removing one triangle hub group make the graph 4-colorable?

Structure discovered:
- Main hub: vertex 1 (degree 36)
- Triangle 1: 267-322-328
- Triangle 2: 271-320-332

Each triangle + its neighborhoods might force 5-chromaticity together,
but separately be 4-colorable.
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

def can_4_color(adj, vertices, timeout_nodes=500000):
    """4-coloring check"""
    if len(vertices) < 5:
        return True, {}

    vertex_list = sorted(vertices, key=lambda v: -len(adj[v] & vertices))
    n = len(vertex_list)
    coloring = [-1] * n
    v_to_idx = {v: i for i, v in enumerate(vertex_list)}
    nodes_checked = [0]

    def backtrack(idx):
        nodes_checked[0] += 1
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
    if result is True:
        return True, {vertex_list[i]: coloring[i] for i in range(n)}
    elif result is None:
        return None, None
    else:
        return False, None

def get_triangle_neighborhood(adj, triangle):
    """Get all vertices in the neighborhood of a triangle of hubs"""
    neighborhood = set(triangle)
    for h in triangle:
        neighborhood.update(adj[h])
    return neighborhood

def main():
    print("=" * 70)
    print("TESTING TRIANGLE REMOVAL HYPOTHESIS")
    print("=" * 70)

    vertices, adj = parse_graph("Hadwiger-Nelson-Project-Data/517.csv")
    print(f"Full graph: {len(vertices)} vertices")

    # Define the structures
    main_hub = 1
    triangle1 = [267, 322, 328]  # First triangle
    triangle2 = [271, 320, 332]  # Second triangle

    # Get neighborhoods
    t1_neighborhood = get_triangle_neighborhood(adj, triangle1)
    t2_neighborhood = get_triangle_neighborhood(adj, triangle2)
    main_hub_neighborhood = {main_hub} | adj[main_hub]

    print(f"\nTriangle 1 (267-322-328) neighborhood: {len(t1_neighborhood)} vertices")
    print(f"Triangle 2 (271-320-332) neighborhood: {len(t2_neighborhood)} vertices")
    print(f"Main hub (1) neighborhood: {len(main_hub_neighborhood)} vertices")

    # Overlap analysis
    t1_t2_overlap = t1_neighborhood & t2_neighborhood
    t1_main_overlap = t1_neighborhood & main_hub_neighborhood
    t2_main_overlap = t2_neighborhood & main_hub_neighborhood

    print(f"\nOverlaps:")
    print(f"  T1 ∩ T2: {len(t1_t2_overlap)} vertices")
    print(f"  T1 ∩ Main: {len(t1_main_overlap)} vertices")
    print(f"  T2 ∩ Main: {len(t2_main_overlap)} vertices")

    # TEST 1: Graph without triangle 1
    print("\n" + "=" * 50)
    print("TEST 1: Remove Triangle 1 (267-322-328) and its exclusive neighborhood")
    vertices_without_t1 = vertices - (t1_neighborhood - t2_neighborhood - main_hub_neighborhood)
    adj_without_t1 = defaultdict(set)
    for v in vertices_without_t1:
        adj_without_t1[v] = adj[v] & vertices_without_t1

    print(f"  Remaining: {len(vertices_without_t1)} vertices")
    start = time.time()
    result, _ = can_4_color(adj_without_t1, vertices_without_t1)
    elapsed = time.time() - start
    status = "4-colorable" if result is True else "NOT 4-colorable" if result is False else "timeout"
    print(f"  Result: {status} ({elapsed:.1f}s)")

    # TEST 2: Graph without triangle 2
    print("\n" + "=" * 50)
    print("TEST 2: Remove Triangle 2 (271-320-332) and its exclusive neighborhood")
    vertices_without_t2 = vertices - (t2_neighborhood - t1_neighborhood - main_hub_neighborhood)
    adj_without_t2 = defaultdict(set)
    for v in vertices_without_t2:
        adj_without_t2[v] = adj[v] & vertices_without_t2

    print(f"  Remaining: {len(vertices_without_t2)} vertices")
    start = time.time()
    result, _ = can_4_color(adj_without_t2, vertices_without_t2)
    elapsed = time.time() - start
    status = "4-colorable" if result is True else "NOT 4-colorable" if result is False else "timeout"
    print(f"  Result: {status} ({elapsed:.1f}s)")

    # TEST 3: Keep only triangle 1 + main hub + overlap
    print("\n" + "=" * 50)
    print("TEST 3: Keep only Triangle 1 + Main hub + shared regions")
    vertices_t1_main = t1_neighborhood | main_hub_neighborhood
    adj_t1_main = defaultdict(set)
    for v in vertices_t1_main:
        adj_t1_main[v] = adj[v] & vertices_t1_main

    print(f"  Size: {len(vertices_t1_main)} vertices")
    start = time.time()
    result, _ = can_4_color(adj_t1_main, vertices_t1_main)
    elapsed = time.time() - start
    status = "4-colorable" if result is True else "NOT 4-colorable" if result is False else "timeout"
    print(f"  Result: {status} ({elapsed:.1f}s)")

    # TEST 4: Keep only triangle 2 + main hub + overlap
    print("\n" + "=" * 50)
    print("TEST 4: Keep only Triangle 2 + Main hub + shared regions")
    vertices_t2_main = t2_neighborhood | main_hub_neighborhood
    adj_t2_main = defaultdict(set)
    for v in vertices_t2_main:
        adj_t2_main[v] = adj[v] & vertices_t2_main

    print(f"  Size: {len(vertices_t2_main)} vertices")
    start = time.time()
    result, _ = can_4_color(adj_t2_main, vertices_t2_main)
    elapsed = time.time() - start
    status = "4-colorable" if result is True else "NOT 4-colorable" if result is False else "timeout"
    print(f"  Result: {status} ({elapsed:.1f}s)")

    # TEST 5: Keep both triangles + main hub (no peripheral)
    print("\n" + "=" * 50)
    print("TEST 5: Keep both Triangles + Main hub (core structure only)")
    vertices_core = t1_neighborhood | t2_neighborhood | main_hub_neighborhood
    adj_core = defaultdict(set)
    for v in vertices_core:
        adj_core[v] = adj[v] & vertices_core

    print(f"  Size: {len(vertices_core)} vertices")
    start = time.time()
    result, _ = can_4_color(adj_core, vertices_core)
    elapsed = time.time() - start
    status = "4-colorable" if result is True else "NOT 4-colorable" if result is False else "timeout"
    print(f"  Result: {status} ({elapsed:.1f}s)")

    # TEST 6: Just the two triangles and their neighborhoods (no main hub)
    print("\n" + "=" * 50)
    print("TEST 6: Both Triangles without Main hub")
    vertices_just_triangles = t1_neighborhood | t2_neighborhood
    adj_just_triangles = defaultdict(set)
    for v in vertices_just_triangles:
        adj_just_triangles[v] = adj[v] & vertices_just_triangles

    print(f"  Size: {len(vertices_just_triangles)} vertices")
    start = time.time()
    result, _ = can_4_color(adj_just_triangles, vertices_just_triangles)
    elapsed = time.time() - start
    status = "4-colorable" if result is True else "NOT 4-colorable" if result is False else "timeout"
    print(f"  Result: {status} ({elapsed:.1f}s)")

    print("\n" + "=" * 70)
    print("INTERPRETATION")
    print("=" * 70)
    print("""
If a test shows NOT 4-colorable:
  -> That substructure alone forces 5-chromaticity
  -> It's a self-contained 5-chromatic unit

If all tests show 4-colorable:
  -> The forcing requires ALL structures together
  -> 5-chromaticity is truly global

If some are 4-colorable and some aren't:
  -> Identifies which combinations are necessary
  -> Points to minimal forcing structure
""")

if __name__ == "__main__":
    main()
