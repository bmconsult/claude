#!/usr/bin/env python3
"""
Heuristic 5-coloring attempt for the icosahedron graph.

If we can find a valid 5-coloring: graph is 5-chromatic (not 6-chromatic)
If all heuristics fail: suggests (but doesn't prove) 6-chromatic
"""

import random
import time
from collections import defaultdict

def parse_dimacs(filename):
    """Parse DIMACS graph file"""
    vertices = set()
    adj = defaultdict(set)

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('p'):
                # p edge n m
                parts = line.split()
                n_vertices = int(parts[2])
                n_edges = int(parts[3])
                print(f"Graph: {n_vertices} vertices, {n_edges} edges")
            elif line.startswith('e'):
                # e u v
                parts = line.split()
                u, v = int(parts[1]), int(parts[2])
                vertices.add(u)
                vertices.add(v)
                adj[u].add(v)
                adj[v].add(u)

    return sorted(vertices), adj

def greedy_coloring(vertices, adj, k):
    """Try greedy k-coloring"""
    color = {}

    # Sort by degree (highest first)
    sorted_verts = sorted(vertices, key=lambda v: -len(adj[v]))

    for v in sorted_verts:
        used = {color[u] for u in adj[v] if u in color}
        for c in range(k):
            if c not in used:
                color[v] = c
                break
        else:
            return None  # Can't color

    return color

def dsatur_coloring(vertices, adj, k):
    """DSatur algorithm - often better than greedy"""
    color = {}
    saturation = {v: 0 for v in vertices}
    uncolored = set(vertices)

    # Start with highest degree vertex
    v = max(uncolored, key=lambda x: len(adj[x]))
    color[v] = 0
    uncolored.remove(v)

    # Update saturation
    for u in adj[v]:
        if u in uncolored:
            saturation[u] += 1

    while uncolored:
        # Pick vertex with highest saturation, break ties by degree
        v = max(uncolored, key=lambda x: (saturation[x], len(adj[x])))

        used = {color[u] for u in adj[v] if u in color}
        for c in range(k):
            if c not in used:
                color[v] = c
                break
        else:
            return None  # Can't color with k colors

        uncolored.remove(v)

        # Update saturation
        for u in adj[v]:
            if u in uncolored:
                neighbor_colors = {color[w] for w in adj[u] if w in color}
                saturation[u] = len(neighbor_colors)

    return color

def local_search_coloring(vertices, adj, k, max_iter=100000):
    """Local search: start random, fix conflicts"""
    # Random initial coloring
    color = {v: random.randint(0, k-1) for v in vertices}

    def conflicts(v):
        return sum(1 for u in adj[v] if color[u] == color[v])

    total_conflicts = sum(conflicts(v) for v in vertices) // 2

    for iteration in range(max_iter):
        if total_conflicts == 0:
            return color

        # Pick a random conflicted vertex
        conflicted = [v for v in vertices if conflicts(v) > 0]
        if not conflicted:
            return color

        v = random.choice(conflicted)
        old_color = color[v]

        # Try each color, pick one that minimizes conflicts
        best_color = old_color
        best_delta = 0

        for c in range(k):
            if c == old_color:
                continue

            # Count conflicts with this color
            new_conflicts = sum(1 for u in adj[v] if color[u] == c)
            old_conflicts = sum(1 for u in adj[v] if color[u] == old_color)
            delta = new_conflicts - old_conflicts

            if delta < best_delta:
                best_delta = delta
                best_color = c

        if best_color != old_color:
            color[v] = best_color
            total_conflicts += best_delta

        if iteration % 10000 == 0:
            print(f"  Iteration {iteration}: {total_conflicts} conflicts")

    return None if total_conflicts > 0 else color

def verify_coloring(vertices, adj, color, k):
    """Verify a coloring is valid"""
    if color is None:
        return False

    for v in vertices:
        if v not in color:
            return False
        if color[v] < 0 or color[v] >= k:
            return False
        for u in adj[v]:
            if color[u] == color[v]:
                return False
    return True

def main():
    print("=" * 70)
    print("HEURISTIC 5-COLORING ATTEMPT")
    print("=" * 70)

    # Look for DIMACS files
    import os
    dimacs_files = []
    for f in os.listdir("dist-graphs/unsolved CNFs"):
        if f.endswith('.dimacs'):
            dimacs_files.append(f"dist-graphs/unsolved CNFs/{f}")

    # If no DIMACS, we need to convert from CNF structure
    # For now, use the plane graphs
    dimacs_path = "dist-graphs/plane/series 2/dimacs/s2_graph1.dimacs"

    if not os.path.exists(dimacs_path):
        print(f"File not found: {dimacs_path}")
        print("Looking for other DIMACS files...")

        for root, dirs, files in os.walk("dist-graphs"):
            for f in files:
                if f.endswith('.dimacs'):
                    print(f"  Found: {os.path.join(root, f)}")
        return

    print(f"\nLoading graph from {dimacs_path}")
    vertices, adj = parse_dimacs(dimacs_path)

    print(f"\nActual: {len(vertices)} vertices, {sum(len(adj[v]) for v in vertices)//2} edges")

    # Try 5-coloring
    k = 5
    print(f"\n--- Attempting {k}-coloring ---")

    # Method 1: Greedy
    print("\n1. Greedy coloring...")
    start = time.time()
    color = greedy_coloring(vertices, adj, k)
    elapsed = time.time() - start
    if verify_coloring(vertices, adj, color, k):
        print(f"  SUCCESS! Greedy found valid {k}-coloring in {elapsed:.2f}s")
        print(f"  => Graph is {k}-colorable (not 6-chromatic)")
        return
    else:
        print(f"  Failed ({elapsed:.2f}s)")

    # Method 2: DSatur
    print("\n2. DSatur coloring...")
    start = time.time()
    color = dsatur_coloring(vertices, adj, k)
    elapsed = time.time() - start
    if verify_coloring(vertices, adj, color, k):
        print(f"  SUCCESS! DSatur found valid {k}-coloring in {elapsed:.2f}s")
        print(f"  => Graph is {k}-colorable (not 6-chromatic)")
        return
    else:
        print(f"  Failed ({elapsed:.2f}s)")

    # Method 3: Local search
    print("\n3. Local search coloring...")
    start = time.time()
    color = local_search_coloring(vertices, adj, k, max_iter=500000)
    elapsed = time.time() - start
    if verify_coloring(vertices, adj, color, k):
        print(f"  SUCCESS! Local search found valid {k}-coloring in {elapsed:.2f}s")
        print(f"  => Graph is {k}-colorable (not 6-chromatic)")
        return
    else:
        print(f"  Failed ({elapsed:.2f}s)")

    print("\n" + "=" * 70)
    print("All heuristics FAILED to find 5-coloring")
    print("This suggests (but does not prove) the graph might be 6-chromatic")
    print("=" * 70)

if __name__ == "__main__":
    main()
