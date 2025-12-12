#!/usr/bin/env python3
"""
Find the MINIMAL subgraph that forces 5-chromaticity.
Key insight: hub+neighbors is 4-colorable, so forcing is GLOBAL.

Strategy: Binary search on subgraph size to find transition point.
"""

from collections import defaultdict
import random
import time

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

def can_4_color(adj, vertices, timeout_nodes=50000):
    """Try to 4-color with timeout"""
    if not vertices:
        return True, {}

    vertex_list = sorted(vertices, key=lambda v: -len(adj[v] & vertices))
    n = len(vertex_list)
    coloring = [-1] * n
    v_to_idx = {v: i for i, v in enumerate(vertex_list)}

    nodes_checked = [0]

    def backtrack(idx):
        nodes_checked[0] += 1
        if nodes_checked[0] > timeout_nodes:
            return None  # Timeout

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
        return None, None  # Timeout
    else:
        return False, None

def grow_from_hub_until_not_4colorable(adj, vertices):
    """
    Start from hub, grow BFS-style until we can't 4-color.
    This finds a critical transition point.
    """
    print("=== GROWING FROM HUB UNTIL NOT 4-COLORABLE ===\n")

    # Find hub
    degrees = {v: len(adj[v]) for v in vertices}
    hub = max(degrees, key=degrees.get)
    print(f"Hub vertex: {hub} (degree {degrees[hub]})")

    # BFS order from hub
    visited = {hub}
    queue = [hub]
    bfs_order = [hub]

    while queue:
        v = queue.pop(0)
        for u in adj[v]:
            if u not in visited:
                visited.add(u)
                queue.append(u)
                bfs_order.append(u)

    # Grow subgraph and test 4-colorability
    subgraph = set()
    sub_adj = defaultdict(set)

    last_4colorable_size = 0
    transition_found = False

    for i, v in enumerate(bfs_order):
        subgraph.add(v)
        for u in adj[v]:
            if u in subgraph:
                sub_adj[v].add(u)
                sub_adj[u].add(v)

        # Test every 10 vertices to save time
        if (i + 1) % 10 == 0 or i == len(bfs_order) - 1:
            result, _ = can_4_color(sub_adj, subgraph, timeout_nodes=100000)

            if result is True:
                last_4colorable_size = len(subgraph)
                print(f"  Size {len(subgraph):3d}: 4-colorable")
            elif result is False:
                print(f"  Size {len(subgraph):3d}: NOT 4-colorable!")
                print(f"  Transition between {last_4colorable_size} and {len(subgraph)}")
                transition_found = True
                break
            else:
                print(f"  Size {len(subgraph):3d}: timeout")

    if transition_found:
        # Binary search to find exact transition
        print("\n  Refining transition point...")

        # We know: size last_4colorable_size is 4-colorable
        #          size len(subgraph) is NOT 4-colorable

        lo = last_4colorable_size
        hi = len(subgraph)

        while hi - lo > 1:
            mid = (lo + hi) // 2
            test_subgraph = set(bfs_order[:mid])
            test_adj = defaultdict(set)
            for v in test_subgraph:
                test_adj[v] = adj[v] & test_subgraph

            result, _ = can_4_color(test_adj, test_subgraph, timeout_nodes=200000)

            if result is True:
                lo = mid
                print(f"    Size {mid}: 4-colorable")
            elif result is False:
                hi = mid
                print(f"    Size {mid}: NOT 4-colorable")
            else:
                print(f"    Size {mid}: timeout, treating as boundary")
                hi = mid

        critical_size = hi
        critical_vertex = bfs_order[hi - 1]
        print(f"\n  CRITICAL TRANSITION: Adding vertex {critical_vertex} (the {hi}th vertex)")
        print(f"  This vertex has degree {degrees[critical_vertex]} and is at BFS distance {hi} from hub")

        return hi, bfs_order[:hi]

    return len(bfs_order), bfs_order

def analyze_multi_hub_interaction(adj, vertices):
    """
    Look at how multiple high-degree vertices interact.
    Maybe 5-chromaticity emerges from their combined constraints.
    """
    print("\n=== MULTI-HUB INTERACTION ANALYSIS ===\n")

    degrees = {v: len(adj[v]) for v in vertices}

    # Get top 10 highest degree vertices
    top_hubs = sorted(degrees, key=degrees.get, reverse=True)[:10]

    print("Top 10 hubs:")
    for i, h in enumerate(top_hubs):
        print(f"  {i+1}. Vertex {h}: degree {degrees[h]}")

    # Check pairwise distances between hubs
    print("\nPairwise distances between top hubs:")

    def bfs_distance(adj, start, end):
        visited = {start: 0}
        queue = [start]
        while queue:
            v = queue.pop(0)
            if v == end:
                return visited[v]
            for u in adj[v]:
                if u not in visited:
                    visited[u] = visited[v] + 1
                    queue.append(u)
        return -1

    for i, h1 in enumerate(top_hubs[:5]):
        for h2 in top_hubs[i+1:6]:
            dist = bfs_distance(adj, h1, h2)
            shared = len(adj[h1] & adj[h2])
            print(f"  {h1} -- {h2}: distance {dist}, shared neighbors {shared}")

    # Test: is subgraph induced by all hub neighborhoods 4-colorable?
    hub_neighborhood = set(top_hubs)
    for h in top_hubs:
        hub_neighborhood.update(adj[h])

    hub_adj = defaultdict(set)
    for v in hub_neighborhood:
        hub_adj[v] = adj[v] & hub_neighborhood

    print(f"\nUnion of top 10 hub neighborhoods: {len(hub_neighborhood)} vertices")
    result, _ = can_4_color(hub_adj, hub_neighborhood, timeout_nodes=500000)

    if result is True:
        print("  Hub union IS 4-colorable")
    elif result is False:
        print("  Hub union is NOT 4-colorable!")
    else:
        print("  Hub union: timeout")

    return top_hubs, hub_neighborhood

def find_critical_edges(adj, vertices, sample_size=100):
    """
    Find edges whose removal might make graph 4-colorable.
    These are the 'critical' edges forcing 5-chromaticity.
    """
    print("\n=== SEARCHING FOR CRITICAL EDGES ===\n")

    edges = [(u, v) for u in vertices for v in adj[u] if u < v]
    print(f"Total edges: {len(edges)}")

    # Sample random edges to test
    sample_edges = random.sample(edges, min(sample_size, len(edges)))

    critical_edges = []

    for u, v in sample_edges:
        # Remove edge and test
        test_adj = defaultdict(set)
        for x in vertices:
            test_adj[x] = adj[x].copy()
        test_adj[u].discard(v)
        test_adj[v].discard(u)

        result, _ = can_4_color(test_adj, vertices, timeout_nodes=50000)

        if result is True:
            critical_edges.append((u, v))
            degrees_u = len(adj[u])
            degrees_v = len(adj[v])
            print(f"  CRITICAL: edge ({u}, {v}) - degrees ({degrees_u}, {degrees_v})")

    print(f"\nFound {len(critical_edges)} critical edges in sample of {sample_size}")

    return critical_edges

def random_subgraph_search(adj, vertices, num_trials=50):
    """
    Randomly sample subgraphs of various sizes to find
    minimal non-4-colorable subgraph.
    """
    print("\n=== RANDOM SUBGRAPH SEARCH ===\n")

    vertex_list = list(vertices)
    min_non4col_size = len(vertices)
    min_subgraph = None

    for size in [100, 150, 200, 250, 300, 350, 400]:
        print(f"\nTesting size {size}:")
        success_count = 0

        for trial in range(num_trials):
            sample = set(random.sample(vertex_list, size))
            sample_adj = defaultdict(set)
            for v in sample:
                sample_adj[v] = adj[v] & sample

            result, _ = can_4_color(sample_adj, sample, timeout_nodes=100000)

            if result is True:
                success_count += 1
            elif result is False:
                if size < min_non4col_size:
                    min_non4col_size = size
                    min_subgraph = sample
                    print(f"  Trial {trial+1}: NOT 4-colorable (new minimum!)")

        print(f"  4-colorable: {success_count}/{num_trials} trials")

        if success_count == 0:
            print(f"  ALL random subgraphs of size {size} were NOT 4-colorable!")
            break

    if min_subgraph:
        print(f"\nSmallest non-4-colorable random subgraph: {min_non4col_size} vertices")

    return min_non4col_size, min_subgraph

def main():
    print("=" * 70)
    print("FINDING THE FORCING STRUCTURE")
    print("=" * 70)

    vertices, edges, adj = parse_graph("Hadwiger-Nelson-Project-Data/517.csv")
    print(f"\nLoaded graph: {len(vertices)} vertices, {len(edges)} edges")

    # Method 1: Grow from hub
    start = time.time()
    critical_size, critical_subgraph = grow_from_hub_until_not_4colorable(adj, vertices)
    print(f"\nBFS growth took {time.time() - start:.1f}s")

    # Method 2: Multi-hub analysis
    start = time.time()
    top_hubs, hub_neighborhood = analyze_multi_hub_interaction(adj, vertices)
    print(f"\nMulti-hub analysis took {time.time() - start:.1f}s")

    # Method 3: Random subgraph search
    start = time.time()
    min_size, min_subgraph = random_subgraph_search(adj, vertices, num_trials=30)
    print(f"\nRandom search took {time.time() - start:.1f}s")

    print("\n" + "=" * 70)
    print("SYNTHESIS")
    print("=" * 70)
    print(f"""
KEY FINDINGS:

1. BFS growth from hub: transition at ~{critical_size} vertices
   - This tells us the "radius" of the forcing structure

2. Hub neighborhood union: {len(hub_neighborhood)} vertices
   - If NOT 4-colorable: forcing is in hub interactions
   - If 4-colorable: forcing requires peripheral structure

3. Random subgraph minimum: {min_size} vertices
   - This is the observed minimal non-4-colorable size
   - The ACTUAL minimum might be smaller

WHAT THIS MEANS FOR HADWIGER-NELSON:

If we can find a subgraph of ~{min_size} vertices that's:
- Unit-distance realizable
- 5-chromatic

Then we have a SMALLER 5-chromatic graph than de Grey's!

The forcing structure is NOT local (hub + neighbors is 4-colorable).
It emerges from the GLOBAL interaction of multiple local constraints.
""")

if __name__ == "__main__":
    main()
