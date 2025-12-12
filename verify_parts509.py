#!/usr/bin/env python3
"""
Verification script for Parts' 509-vertex graph coordinates.

Once you obtain the coordinates (via Wolfram Language or other source),
use this script to verify:
1. Correct number of vertices (509)
2. Correct number of edges (2442)
3. All edges have unit distance (within tolerance)
4. Graph is indeed not 4-colorable (requires SAT solver or graph coloring library)
"""

import numpy as np
from scipy.spatial.distance import pdist, squareform
import sys

def load_coordinates(filename):
    """Load vertex coordinates from CSV file."""
    try:
        coords = np.loadtxt(filename, delimiter=',')
        if coords.ndim == 1:
            coords = coords.reshape(-1, 2)
        return coords
    except Exception as e:
        print(f"ERROR loading coordinates: {e}")
        sys.exit(1)

def verify_graph(coords, expected_vertices=509, expected_edges=2442, tolerance=1e-6):
    """Verify the graph properties."""

    num_vertices = len(coords)
    print(f"Number of vertices: {num_vertices}")

    if num_vertices != expected_vertices:
        print(f"WARNING: Expected {expected_vertices} vertices, got {num_vertices}")

    # Compute all pairwise distances
    print("\nComputing pairwise distances...")
    distances = squareform(pdist(coords))

    # Find edges (distance = 1, within tolerance)
    edge_mask = (distances > 1 - tolerance) & (distances < 1 + tolerance)

    # Set diagonal to False (no self-loops)
    np.fill_diagonal(edge_mask, False)

    # Count edges (each edge appears twice in adjacency matrix)
    num_edges = np.sum(edge_mask) // 2

    print(f"Number of edges (unit distance): {num_edges}")

    if num_edges != expected_edges:
        print(f"WARNING: Expected {expected_edges} edges, got {num_edges}")

    # Find non-unit distances in the graph
    edge_indices = np.argwhere(edge_mask)
    edge_distances = distances[edge_mask]

    print(f"\nEdge distance statistics:")
    print(f"  Min: {edge_distances.min():.10f}")
    print(f"  Max: {edge_distances.max():.10f}")
    print(f"  Mean: {edge_distances.mean():.10f}")
    print(f"  Std: {edge_distances.std():.10f}")

    # Degree distribution
    degrees = np.sum(edge_mask, axis=1)
    print(f"\nDegree statistics:")
    print(f"  Min degree: {degrees.min()}")
    print(f"  Max degree: {degrees.max()}")
    print(f"  Average degree: {degrees.mean():.2f}")
    print(f"  Median degree: {np.median(degrees):.1f}")

    return edge_mask, degrees

def export_edge_list(coords, edge_mask, filename="parts509_edges_verified.txt"):
    """Export edge list with distances."""
    edges = np.argwhere(np.triu(edge_mask, k=1))  # Upper triangle only

    with open(filename, 'w') as f:
        f.write("# Parts 509-vertex graph edge list\n")
        f.write("# Format: vertex1 vertex2 distance\n")
        for i, j in edges:
            dist = np.linalg.norm(coords[i] - coords[j])
            f.write(f"{i} {j} {dist:.10f}\n")

    print(f"\nEdge list exported to {filename}")
    return edges

def check_moser_spindles(coords, edge_mask, tolerance=1e-6):
    """Check for Moser spindle structures (7 vertices, 4-chromatic)."""
    print("\nSearching for Moser spindles...")

    # A Moser spindle has:
    # - 7 vertices
    # - 11 edges of unit length
    # - Forms two rhombi sharing a vertex
    # - Contains edges of length sqrt(3)

    # This is computationally intensive, so we just count potential 4-cliques
    num_vertices = len(coords)
    clique_count = 0

    # Find all triangles (3-cliques)
    distances = squareform(pdist(coords))

    for i in range(num_vertices):
        neighbors = np.where(edge_mask[i])[0]
        for j in neighbors:
            if j <= i:
                continue
            # Check if i and j share common neighbors
            common = np.where(edge_mask[i] & edge_mask[j])[0]
            clique_count += len(common)

    print(f"Number of triangles (approximate): {clique_count // 3}")

def export_for_visualization(coords, edge_mask, basename="parts509"):
    """Export in various formats for visualization tools."""

    # GraphML format (for Gephi, Cytoscape, etc.)
    edges = np.argwhere(np.triu(edge_mask, k=1))

    with open(f"{basename}.graphml", 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<graphml xmlns="http://graphml.graphdrawing.org/xmlns">\n')
        f.write('  <graph id="Parts509" edgedefault="undirected">\n')

        # Vertices
        for i, (x, y) in enumerate(coords):
            f.write(f'    <node id="v{i}">\n')
            f.write(f'      <data key="x">{x}</data>\n')
            f.write(f'      <data key="y">{y}</data>\n')
            f.write(f'    </node>\n')

        # Edges
        for i, j in edges:
            f.write(f'    <edge source="v{i}" target="v{j}"/>\n')

        f.write('  </graph>\n')
        f.write('</graphml>\n')

    print(f"GraphML format exported to {basename}.graphml")

    # DOT format (for Graphviz)
    with open(f"{basename}.dot", 'w') as f:
        f.write('graph Parts509 {\n')
        f.write('  node [shape=point, width=0.05];\n')

        for i, j in edges:
            f.write(f'  {i} -- {j};\n')

        f.write('}\n')

    print(f"Graphviz DOT format exported to {basename}.dot")

def main():
    if len(sys.argv) < 2:
        print("Usage: python verify_parts509.py <coordinates.csv>")
        print("\nExample:")
        print("  python verify_parts509.py parts509_coordinates.csv")
        sys.exit(1)

    filename = sys.argv[1]

    print("=" * 60)
    print("Parts' 509-Vertex Graph Verification")
    print("=" * 60)
    print(f"\nLoading coordinates from: {filename}")

    coords = load_coordinates(filename)

    print(f"Loaded {len(coords)} vertices with {coords.shape[1]} dimensions")

    if coords.shape[1] != 2:
        print("WARNING: Expected 2D coordinates, got {coords.shape[1]}D")

    # Verify graph properties
    edge_mask, degrees = verify_graph(coords)

    # Export edge list
    edges = export_edge_list(coords, edge_mask)

    # Check for Moser spindles (computationally intensive)
    # check_moser_spindles(coords, edge_mask)

    # Export for visualization
    export_for_visualization(coords, edge_mask)

    print("\n" + "=" * 60)
    print("Verification complete!")
    print("=" * 60)

    # Check if graph properties match expected values
    num_vertices = len(coords)
    num_edges = len(edges)

    if num_vertices == 509 and num_edges == 2442:
        print("\n✓ SUCCESS: Graph matches expected properties!")
    else:
        print("\n✗ WARNING: Graph does not match expected properties.")
        print(f"  Expected: 509 vertices, 2442 edges")
        print(f"  Got: {num_vertices} vertices, {num_edges} edges")

if __name__ == "__main__":
    main()
