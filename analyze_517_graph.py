#!/usr/bin/env python3
"""
REAL ANALYSIS of the 517-vertex 5-chromatic graph
No more speculation - actual data analysis
"""

import math
from collections import defaultdict, Counter
from itertools import combinations

def parse_graph(filename):
    """Parse the CSV format: vertex,edges (semicolon-separated)"""
    vertices = set()
    edges = set()
    adj = defaultdict(set)

    with open(filename, 'r') as f:
        next(f)  # Skip header
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
                    edge = tuple(sorted([v, u]))
                    edges.add(edge)
                    adj[v].add(u)
                    adj[u].add(v)

    return vertices, edges, adj

def analyze_degree_distribution(adj):
    """Analyze vertex degrees"""
    degrees = [len(adj[v]) for v in adj]
    degree_counts = Counter(degrees)

    print(f"Degree distribution:")
    print(f"  Min degree: {min(degrees)}")
    print(f"  Max degree: {max(degrees)}")
    print(f"  Avg degree: {sum(degrees)/len(degrees):.2f}")
    print(f"  Degree histogram:")
    for d in sorted(degree_counts.keys()):
        print(f"    degree {d}: {degree_counts[d]} vertices")

    return degrees, degree_counts

def find_triangles(adj, vertices):
    """Find all triangles (3-cliques) - these are unit equilateral triangles"""
    triangles = []
    for v in vertices:
        neighbors = list(adj[v])
        for i, u in enumerate(neighbors):
            for w in neighbors[i+1:]:
                if w in adj[u]:
                    tri = tuple(sorted([v, u, w]))
                    if tri not in triangles:
                        triangles.append(tri)
    return triangles

def find_cliques(adj, vertices, size):
    """Find cliques of given size"""
    cliques = []
    vertex_list = list(vertices)

    for combo in combinations(vertex_list, size):
        is_clique = True
        for i, v in enumerate(combo):
            for u in combo[i+1:]:
                if u not in adj[v]:
                    is_clique = False
                    break
            if not is_clique:
                break
        if is_clique:
            cliques.append(combo)

    return cliques

def analyze_local_structure(adj, vertices):
    """Analyze local neighborhood structure"""
    # For each vertex, count triangles it's in
    vertex_triangles = defaultdict(int)
    triangles = find_triangles(adj, vertices)

    for tri in triangles:
        for v in tri:
            vertex_triangles[v] += 1

    tri_counts = Counter(vertex_triangles.values())

    print(f"\nTriangle participation:")
    print(f"  Total triangles: {len(triangles)}")
    print(f"  Triangles per vertex distribution:")
    for t in sorted(tri_counts.keys())[:10]:
        print(f"    {t} triangles: {tri_counts[t]} vertices")

    return triangles, vertex_triangles

def find_high_degree_core(adj, min_degree):
    """Find the subgraph of vertices with degree >= min_degree"""
    core_vertices = {v for v in adj if len(adj[v]) >= min_degree}
    core_edges = {(u, v) for u, v in combinations(core_vertices, 2) if v in adj[u]}
    return core_vertices, core_edges

def analyze_connectivity(adj, vertices):
    """Basic connectivity analysis"""
    # BFS to check connectivity
    start = next(iter(vertices))
    visited = {start}
    queue = [start]

    while queue:
        v = queue.pop(0)
        for u in adj[v]:
            if u not in visited:
                visited.add(u)
                queue.append(u)

    print(f"\nConnectivity:")
    print(f"  Vertices reachable from arbitrary start: {len(visited)}/{len(vertices)}")
    print(f"  Graph is {'connected' if len(visited) == len(vertices) else 'DISCONNECTED'}")

def greedy_coloring(adj, vertices):
    """Greedy coloring to get upper bound"""
    coloring = {}
    vertex_list = sorted(vertices, key=lambda v: -len(adj[v]))  # High degree first

    for v in vertex_list:
        used_colors = {coloring[u] for u in adj[v] if u in coloring}
        for c in range(len(vertices)):
            if c not in used_colors:
                coloring[v] = c
                break

    num_colors = max(coloring.values()) + 1
    return num_colors, coloring

def can_color_with_k(adj, vertices, k, timeout=1000000):
    """Try to k-color the graph using backtracking with pruning"""
    vertex_list = sorted(vertices, key=lambda v: -len(adj[v]))  # High degree first
    n = len(vertex_list)
    coloring = [-1] * n
    v_to_idx = {v: i for i, v in enumerate(vertex_list)}

    count = [0]

    def backtrack(idx):
        count[0] += 1
        if count[0] > timeout:
            return None  # Timeout

        if idx == n:
            return True

        v = vertex_list[idx]
        neighbor_colors = {coloring[v_to_idx[u]] for u in adj[v] if v_to_idx[u] < idx}

        for c in range(k):
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

def find_moser_spindle_like(adj, vertices):
    """
    Look for Moser spindle-like structures.
    A Moser spindle has 7 vertices and a specific edge pattern.
    We look for vertices with degree pattern similar to spindle.
    """
    # In Moser spindle: degrees are [4, 3, 3, 3, 3, 3, 2] (approximately)
    # Look for 7-vertex subgraphs with ~11 edges

    count = 0
    # This is expensive, so just sample
    vertex_list = list(vertices)[:100]  # Sample first 100

    for v in vertex_list:
        # Get 2-hop neighborhood
        n1 = adj[v]
        n2 = set()
        for u in n1:
            n2.update(adj[u])
        n2 -= n1
        n2 -= {v}

        # Count edges in this local region
        local_vertices = {v} | n1
        local_edges = sum(1 for a, b in combinations(local_vertices, 2) if b in adj[a])

        # Moser spindle has 11 edges for 7 vertices
        # Check if local density is similar
        if len(local_vertices) >= 5 and local_edges >= 8:
            count += 1

    print(f"\nMoser spindle-like local structures (sampled): {count}/100 vertices")
    return count

def main():
    print("=" * 70)
    print("REAL ANALYSIS: 517-vertex 5-chromatic unit-distance graph")
    print("=" * 70)

    # Parse the graph
    vertices, edges, adj = parse_graph("Hadwiger-Nelson-Project-Data/517.csv")

    print(f"\nBasic stats:")
    print(f"  Vertices: {len(vertices)}")
    print(f"  Edges: {len(edges)}")
    print(f"  Edge density: {2*len(edges)/(len(vertices)*(len(vertices)-1)):.6f}")

    # Degree analysis
    print("\n" + "=" * 50)
    degrees, degree_counts = analyze_degree_distribution(adj)

    # Connectivity
    analyze_connectivity(adj, vertices)

    # Triangle analysis
    print("\n" + "=" * 50)
    triangles, vertex_triangles = analyze_local_structure(adj, vertices)

    # Look for 4-cliques (would indicate tight local structure)
    print("\n" + "=" * 50)
    print("Searching for 4-cliques...")
    # This is expensive, so limit search
    four_cliques = find_cliques(adj, vertices, 4)
    print(f"  4-cliques found: {len(four_cliques)}")

    # Moser spindle analysis
    print("\n" + "=" * 50)
    find_moser_spindle_like(adj, vertices)

    # High-degree core
    print("\n" + "=" * 50)
    print("High-degree core analysis:")
    for min_deg in [8, 10, 12, 14]:
        core_v, core_e = find_high_degree_core(adj, min_deg)
        print(f"  Degree >= {min_deg}: {len(core_v)} vertices, {len(core_e)} edges")

    # Greedy coloring
    print("\n" + "=" * 50)
    greedy_colors, _ = greedy_coloring(adj, vertices)
    print(f"Greedy coloring uses: {greedy_colors} colors")

    # Try exact coloring (with timeout)
    print("\n" + "=" * 50)
    print("Testing colorability (with timeout)...")

    for k in [3, 4]:
        result, _ = can_color_with_k(adj, vertices, k, timeout=100000)
        if result is True:
            print(f"  {k}-colorable: YES")
        elif result is False:
            print(f"  {k}-colorable: NO")
        else:
            print(f"  {k}-colorable: TIMEOUT (inconclusive)")

    print(f"  5-colorable: YES (known from construction)")

    # Summary insights
    print("\n" + "=" * 70)
    print("KEY STRUCTURAL INSIGHTS")
    print("=" * 70)

    avg_degree = sum(degrees) / len(degrees)
    max_degree = max(degrees)

    print(f"""
1. DENSITY: {len(edges)} edges for {len(vertices)} vertices
   - Edge density: {2*len(edges)/(len(vertices)*(len(vertices)-1)):.4f}
   - Average degree: {avg_degree:.1f}
   - This is SPARSE (density << 1) but LOCALLY DENSE

2. TRIANGLES: {len(triangles)} triangles total
   - These represent unit equilateral triangles in the plane
   - Each vertex participates in multiple triangles
   - This creates the constraint propagation network

3. HIGH-DEGREE VERTICES: Max degree = {max_degree}
   - These are the "hub" vertices
   - Likely correspond to centers of hexagonal structures

4. NO 4-CLIQUES (if true):
   - Unit distance graph can't have K4 (no 4 mutually equidistant points in plane)
   - {len(four_cliques)} 4-cliques found (should be 0 for true unit-distance graph)

5. THE KEY QUESTION:
   - Which substructure FORCES 5-chromaticity?
   - If we could identify the minimal "forcing" subgraph...
   - We might find a smaller 5-chromatic graph!
""")

if __name__ == "__main__":
    main()
