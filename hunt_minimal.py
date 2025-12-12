#!/usr/bin/env python3
"""
Hunt for MINIMAL non-4-colorable subgraph.
We know: size 200 can be non-4-colorable (found 1/30)
Goal: Find smaller ones and reduce them.
"""

from collections import defaultdict
import random
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

def can_4_color_fast(adj, vertices, timeout_nodes=30000):
    """Fast 4-coloring check with tight timeout"""
    if len(vertices) < 5:
        return True

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

    return backtrack(0)

def intensive_search_small(adj, vertices):
    """Intensive search at sizes 150-220"""
    print("=== INTENSIVE SEARCH FOR SMALL NON-4-COLORABLE ===\n")

    vertex_list = list(vertices)
    found = []

    for size in range(150, 221, 5):
        print(f"Size {size}:", end=" ", flush=True)
        non4col_count = 0

        for trial in range(200):  # More trials
            sample = set(random.sample(vertex_list, size))
            sample_adj = defaultdict(set)
            for v in sample:
                sample_adj[v] = adj[v] & sample

            result = can_4_color_fast(sample_adj, sample)

            if result is False:
                non4col_count += 1
                if len(found) < 10 or size < min(f[0] for f in found):
                    found.append((size, sample.copy()))
                    print(f"FOUND!", end=" ", flush=True)

        print(f"{non4col_count}/200 not 4-colorable")

        if non4col_count == 0 and size >= 180:
            # All 4-colorable at this size, keep going
            pass

    return found

def reduce_subgraph(adj, subgraph):
    """Try to reduce a non-4-colorable subgraph"""
    current = subgraph.copy()
    reduced = True

    while reduced:
        reduced = False
        # Try removing each vertex
        vertices_to_try = list(current)
        random.shuffle(vertices_to_try)

        for v in vertices_to_try:
            test = current - {v}
            test_adj = defaultdict(set)
            for u in test:
                test_adj[u] = adj[u] & test

            result = can_4_color_fast(test_adj, test, timeout_nodes=50000)

            if result is False:
                # Still not 4-colorable! Keep going
                current = test
                reduced = True
                break
            # If True or timeout, keep the vertex

    return current

def find_high_degree_core(adj, vertices):
    """Find subgraph induced by high-degree vertices"""
    print("\n=== HIGH-DEGREE CORE SEARCH ===\n")

    degrees = {v: len(adj[v]) for v in vertices}
    sorted_by_degree = sorted(vertices, key=lambda v: -degrees[v])

    # Test cores of different sizes
    for core_size in [100, 120, 140, 160, 180, 200, 220, 240]:
        core = set(sorted_by_degree[:core_size])
        core_adj = defaultdict(set)
        for v in core:
            core_adj[v] = adj[v] & core

        result = can_4_color_fast(core_adj, core, timeout_nodes=100000)

        status = "4-colorable" if result is True else "NOT 4-colorable" if result is False else "timeout"
        print(f"  Top {core_size} by degree: {status}")

        if result is False:
            print(f"  -> Found non-4-colorable core of size {core_size}!")
            return core

    return None

def smart_seed_search(adj, vertices):
    """
    Use known structure: start from hub neighborhoods
    and grow intelligently.
    """
    print("\n=== SMART SEED SEARCH ===\n")

    degrees = {v: len(adj[v]) for v in vertices}

    # Get the 6 degree-24 vertices (the secondary hubs)
    hubs = [v for v in vertices if degrees[v] >= 24]
    print(f"High-degree vertices (>=24): {len(hubs)}")
    print(f"  Vertices: {sorted(hubs)}")

    # Try combinations of hub neighborhoods
    best_size = len(vertices)
    best_subgraph = None

    # Start with union of all hub neighborhoods
    hub_union = set(hubs)
    for h in hubs:
        hub_union.update(adj[h])

    print(f"\nUnion of all hub neighborhoods: {len(hub_union)} vertices")

    # Now add vertices until not 4-colorable
    remaining = list(vertices - hub_union)
    random.shuffle(remaining)

    current = hub_union.copy()

    for v in remaining:
        current.add(v)

        if len(current) % 20 == 0:
            current_adj = defaultdict(set)
            for u in current:
                current_adj[u] = adj[u] & current

            result = can_4_color_fast(current_adj, current, timeout_nodes=50000)

            if result is False:
                print(f"  Size {len(current)}: NOT 4-colorable!")
                if len(current) < best_size:
                    best_size = len(current)
                    best_subgraph = current.copy()
                break
            elif result is True:
                print(f"  Size {len(current)}: 4-colorable")

    return best_size, best_subgraph

def main():
    print("=" * 70)
    print("HUNTING FOR MINIMAL NON-4-COLORABLE SUBGRAPH")
    print("=" * 70)

    vertices, adj = parse_graph("Hadwiger-Nelson-Project-Data/517.csv")
    print(f"Loaded: {len(vertices)} vertices")

    # Method 1: Intensive random search at small sizes
    found_subgraphs = intensive_search_small(adj, vertices)

    # Method 2: High-degree core
    hd_core = find_high_degree_core(adj, vertices)

    # Method 3: Smart seed from hubs
    smart_size, smart_subgraph = smart_seed_search(adj, vertices)

    print("\n" + "=" * 70)
    print("REDUCING FOUND SUBGRAPHS")
    print("=" * 70)

    if found_subgraphs:
        # Sort by size
        found_subgraphs.sort(key=lambda x: x[0])
        best_size, best_subgraph = found_subgraphs[0]

        print(f"\nSmallest found: {best_size} vertices")
        print("Attempting to reduce...")

        reduced = reduce_subgraph(adj, best_subgraph)
        print(f"After reduction: {len(reduced)} vertices")

        if len(reduced) < best_size:
            print(f"REDUCED by {best_size - len(reduced)} vertices!")

    if hd_core:
        print(f"\nHigh-degree core: {len(hd_core)} vertices")
        print("Attempting to reduce...")
        reduced = reduce_subgraph(adj, hd_core)
        print(f"After reduction: {len(reduced)} vertices")

    print("\n" + "=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)

    all_found = []
    if found_subgraphs:
        for size, sg in found_subgraphs:
            all_found.append(size)
    if hd_core:
        all_found.append(len(hd_core))
    if smart_subgraph:
        all_found.append(smart_size)

    if all_found:
        print(f"\nSmallest non-4-colorable subgraph found: {min(all_found)} vertices")
        print(f"This is {min(all_found)/517*100:.1f}% of the full graph")
        print(f"\nIf we can find a ~{min(all_found)}-vertex 5-chromatic unit-distance graph,")
        print("that would be smaller than de Grey's 509-vertex graph!")
    else:
        print("\nNo non-4-colorable subgraphs found in this search")

if __name__ == "__main__":
    main()
