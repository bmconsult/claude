#!/usr/bin/env python3
"""
Compute spectral bounds for the 517-vertex 5-chromatic graph.

Hoffman bound: χ ≥ 1 + λ_max / |λ_min|
"""

from collections import defaultdict
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh

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
    return sorted(vertices), adj

def build_adjacency_matrix(vertices, adj):
    """Build sparse adjacency matrix"""
    n = len(vertices)
    v_to_idx = {v: i for i, v in enumerate(vertices)}

    row = []
    col = []
    data = []

    for v in vertices:
        vi = v_to_idx[v]
        for u in adj[v]:
            if u in v_to_idx:
                ui = v_to_idx[u]
                row.append(vi)
                col.append(ui)
                data.append(1.0)

    return sparse.csr_matrix((data, (row, col)), shape=(n, n))

def compute_spectral_bounds(A):
    """Compute spectral bounds on chromatic number"""
    n = A.shape[0]

    print("Computing eigenvalues...")

    # Get largest and smallest eigenvalues
    # For largest: use 'LM' (largest magnitude)
    # For smallest: use 'SA' (smallest algebraic)

    try:
        # Largest eigenvalue
        lambda_max_vals, _ = eigsh(A, k=5, which='LA')
        lambda_max = max(lambda_max_vals)

        # Smallest eigenvalue
        lambda_min_vals, _ = eigsh(A, k=5, which='SA')
        lambda_min = min(lambda_min_vals)

        print(f"\nEigenvalue Analysis:")
        print(f"  λ_max = {lambda_max:.4f}")
        print(f"  λ_min = {lambda_min:.4f}")

        # Hoffman bound
        if lambda_min < 0:
            hoffman = 1 + lambda_max / abs(lambda_min)
            print(f"\nHoffman bound: χ ≥ 1 + {lambda_max:.4f}/{abs(lambda_min):.4f} = {hoffman:.4f}")
            print(f"  Rounded: χ ≥ {int(np.ceil(hoffman))}")
        else:
            print("\nλ_min ≥ 0, Hoffman bound not applicable (need negative eigenvalue)")

        return lambda_max, lambda_min

    except Exception as e:
        print(f"Error computing eigenvalues: {e}")
        return None, None

def compute_all_eigenvalues(A):
    """Compute all eigenvalues for detailed analysis (for small matrices)"""
    print("\nComputing all eigenvalues (this may take a moment)...")

    # Convert to dense for full eigenvalue computation
    A_dense = A.toarray()
    eigenvalues = np.linalg.eigvalsh(A_dense)  # eigvalsh for symmetric matrices
    eigenvalues = np.sort(eigenvalues)[::-1]  # Sort descending

    print(f"\nSpectrum summary:")
    print(f"  Total eigenvalues: {len(eigenvalues)}")
    print(f"  Positive: {np.sum(eigenvalues > 0.001)}")
    print(f"  Negative: {np.sum(eigenvalues < -0.001)}")
    print(f"  Near zero: {np.sum(np.abs(eigenvalues) <= 0.001)}")

    print(f"\n  Top 10 eigenvalues: {eigenvalues[:10]}")
    print(f"  Bottom 10 eigenvalues: {eigenvalues[-10:]}")

    # Generalized Hoffman bounds
    lambda_max = eigenvalues[0]
    lambda_min = eigenvalues[-1]

    if lambda_min < 0:
        # Standard Hoffman
        hoffman_1 = 1 + lambda_max / abs(lambda_min)

        # Sum of positives / sum of negatives
        S_plus = np.sum(eigenvalues[eigenvalues > 0])
        S_minus = abs(np.sum(eigenvalues[eigenvalues < 0]))

        if S_minus > 0:
            ratio_bound = S_plus / S_minus

            print(f"\nSpectral bounds:")
            print(f"  Hoffman (m=1): χ ≥ {hoffman_1:.4f}")
            print(f"  S⁺/S⁻ bound: χ ≥ {ratio_bound:.4f}")

            # Generalized bound: sum of top m / |sum of bottom m|
            print(f"\n  Generalized bounds (sum of top m / |sum of bottom m|):")
            for m in [2, 5, 10, 20, 50]:
                if m < len(eigenvalues) // 2:
                    top_m = np.sum(eigenvalues[:m])
                    bottom_m = abs(np.sum(eigenvalues[-m:]))
                    if bottom_m > 0:
                        gen_bound = 1 + top_m / bottom_m
                        print(f"    m={m}: χ ≥ {gen_bound:.4f}")

    return eigenvalues

def main():
    print("=" * 70)
    print("SPECTRAL ANALYSIS OF 517-VERTEX 5-CHROMATIC GRAPH")
    print("=" * 70)

    vertices, adj = parse_graph("Hadwiger-Nelson-Project-Data/517.csv")
    print(f"\nGraph: {len(vertices)} vertices")

    # Count edges
    edge_count = sum(len(adj[v]) for v in vertices) // 2
    print(f"Edges: {edge_count}")

    # Build adjacency matrix
    A = build_adjacency_matrix(vertices, adj)

    # Compute spectral bounds
    compute_spectral_bounds(A)

    # Full eigenvalue analysis
    eigenvalues = compute_all_eigenvalues(A)

    print("\n" + "=" * 70)
    print("INTERPRETATION")
    print("=" * 70)
    print("""
If Hoffman bound ≥ 5: Spectral proof that χ ≥ 5!
If Hoffman bound < 5: Spectral methods insufficient, need SAT

Note: The known chromatic number is 5 (proven by SAT).
This test checks if spectral methods alone could prove it.
""")

if __name__ == "__main__":
    main()
