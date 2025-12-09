#!/usr/bin/env python3
"""
Exact analysis of S_n decomposition of R^{2^n}.

The key insight: R^{2^n} decomposes by LEVEL (Hamming weight of Fourier character).
Level k corresponds to functions that depend on exactly k variables symmetrically.

The representation at level k is the action of S_n on k-subsets of [n].
This decomposes into specific irreps determined by the Johnson scheme.
"""

import numpy as np
from math import factorial, comb
from itertools import permutations, combinations
from collections import defaultdict
from functools import lru_cache

# ============================================================
# Part 1: Hook Length Formula for Irrep Dimensions
# ============================================================

@lru_cache(maxsize=10000)
def hook_length(partition):
    """Compute dimension of S_n irrep using hook length formula."""
    n = sum(partition)
    if n == 0:
        return 1

    rows = list(partition)
    rows = [r for r in rows if r > 0]

    if not rows:
        return 1

    hook_product = 1
    for i, row_len in enumerate(rows):
        for j in range(row_len):
            cells_right = row_len - j - 1
            cells_below = sum(1 for k in range(i+1, len(rows)) if rows[k] > j)
            hook = cells_right + cells_below + 1
            hook_product *= hook

    return factorial(n) // hook_product

def partitions(n):
    """Generate all partitions of n in decreasing order."""
    if n == 0:
        yield ()
        return

    def _parts(n, max_val):
        if n == 0:
            yield ()
            return
        for i in range(min(n, max_val), 0, -1):
            for p in _parts(n - i, i):
                yield (i,) + p

    yield from _parts(n, n)

# ============================================================
# Part 2: Decomposition of Permutation Action on k-Subsets
# ============================================================

def subset_rep_decomposition(n, k):
    """
    Decompose the S_n representation on k-subsets of [n].

    By the theory of symmetric functions, the permutation rep on k-subsets
    decomposes as:

    For k ≤ n/2:
    V_{k-subsets} = ⊕_{j=0}^{k} V_{(n-j, 1^j)}  where 1^j means j 1's

    Actually the correct decomposition uses "hooks":
    V_{k-subsets} ≅ S^{(n-k)} ⊗ sign^{⊗k} restricted appropriately

    More precisely: The permutation rep on (n choose k) elements decomposes into
    irreps indexed by partitions with at most 2 rows, where first row ≥ n-k.

    Let me compute this more carefully using characters.
    """
    if k > n - k:
        # Use symmetry: k-subsets ↔ (n-k)-subsets
        k = n - k

    # The permutation module M^{(n-k,k)} decomposes as:
    # M^{(n-k,k)} = ⊕_{j=0}^{k} S^{(n-j, j)} for j from 0 to k
    # where S^λ is the Specht module (irrep) for partition λ

    decomposition = []
    for j in range(k + 1):
        if n - j >= j:  # Valid partition (n-j, j) with n-j ≥ j
            partition = (n - j, j) if j > 0 else (n,)
            dim = hook_length(partition)
            decomposition.append((partition, 1, dim))  # (partition, multiplicity, dimension)

    return decomposition

def verify_subset_decomposition(n, k):
    """Verify that dimensions add up correctly."""
    decomp = subset_rep_decomposition(n, k)
    total_dim = sum(mult * dim for _, mult, dim in decomp)
    expected = comb(n, k)

    print(f"S_{n} on {k}-subsets:")
    for part, mult, dim in decomp:
        print(f"  {part}: multiplicity {mult}, dimension {dim}")
    print(f"Total: {total_dim}, Expected: {expected}")
    print(f"Match: {total_dim == expected}")
    print()

    return total_dim == expected

# ============================================================
# Part 3: Full Decomposition of R^{2^n}
# ============================================================

def full_decomposition(n):
    """
    Decompose R^{2^n} under S_n.

    R^{2^n} has a basis of Fourier characters χ_S for S ⊆ [n].
    Characters at level k (|S| = k) span a subspace of dimension (n choose k).

    S_n acts on level k by permuting the subsets S.
    So level k is exactly the permutation representation on k-subsets.

    Total decomposition: R^{2^n} = ⊕_{k=0}^{n} (permutation rep on k-subsets)
    """
    print(f"Decomposition of R^{2^n} under S_{n}:")
    print("=" * 50)

    # Track total multiplicities of each irrep
    total_multiplicities = defaultdict(int)
    total_weighted_dim = defaultdict(int)  # partition -> multiplicity × dimension

    for k in range(n + 1):
        print(f"\nLevel {k} (Fourier degree k):")
        decomp = subset_rep_decomposition(n, k)

        for part, mult, dim in decomp:
            total_multiplicities[part] += mult
            total_weighted_dim[part] += mult * dim
            print(f"  {part}: +{mult} (dim={dim})")

    print("\n" + "=" * 50)
    print("TOTAL DECOMPOSITION:")
    print("=" * 50)

    grand_total = 0
    weighted_dim_squared = 0

    for part in sorted(total_multiplicities.keys(), key=lambda p: (-sum(p), p)):
        mult = total_multiplicities[part]
        dim = hook_length(part)
        weighted = mult * dim
        grand_total += weighted
        weighted_dim_squared += mult * dim * dim
        print(f"{part}: multiplicity {mult}, dim {dim}, total contribution {weighted}")

    print(f"\nGrand total dimension: {grand_total} (should be {2**n})")
    print(f"Σ m_λ × d_λ² = {weighted_dim_squared}")
    print(f"n! = {factorial(n)}")

    return total_multiplicities, total_weighted_dim

# ============================================================
# Part 4: WIS Bounds
# ============================================================

def compute_wis_bounds(n):
    """
    Compute WIS bounds for random vs simple functions.

    WIS = Σ_λ d_λ × 1[component λ has significant mass]

    For random T: all components have mass proportional to their total dimension
    For simple T: only few components have mass
    """
    print(f"\nWIS Analysis for n={n}:")
    print("=" * 50)

    multiplicities, weighted_dim = full_decomposition(n)

    N = 2**n

    # For random T, a component λ has significant mass if m_λ × d_λ is not negligible
    # Threshold: we count λ as significant if m_λ × d_λ > N / (n! / some factor)

    # Simpler: count weighted dimension of ALL components (upper bound on random WIS)
    total_wis_random = 0
    for part, mult in multiplicities.items():
        dim = hook_length(part)
        total_wis_random += dim  # Each significant component contributes its dimension

    print(f"\nRandom T: WIS upper bound (all components) = {total_wis_random}")

    # For simple T (single variable):
    # Only trivial (n) and standard (n-1, 1) components
    wis_variable = hook_length((n,)) + hook_length((n-1, 1))
    print(f"Variable x_i: WIS = {wis_variable}")

    # Compare to N^3
    n_cubed = N ** 3
    n_factorial = factorial(n)

    print(f"\nComparison:")
    print(f"n! = {n_factorial}")
    print(f"N^3 = 2^{3*n} = {n_cubed}")
    print(f"Ratio n!/N^3 = {n_factorial / n_cubed:.6e}")

    if n_factorial > n_cubed:
        print(f"✓ n! > N^3: WIS budget exceeds magnification threshold!")
    else:
        print(f"✗ n! ≤ N^3: Need larger n")

    return multiplicities

# ============================================================
# Part 5: Key Insight - Dimension Squared Sum
# ============================================================

def dimension_squared_analysis(n):
    """
    Analyze Σ d_λ² = n!

    This is a key fact: the sum of squared dimensions equals n!.
    It means the "weighted dimension budget" is exactly n!.
    """
    print(f"\nDimension squared analysis for S_{n}:")
    print("=" * 50)

    total_sq = 0
    partitions_list = list(partitions(n))

    print(f"Number of partitions: {len(partitions_list)}")
    print()

    for part in sorted(partitions_list, key=lambda p: -hook_length(p)):
        dim = hook_length(part)
        total_sq += dim * dim
        if dim > 1 or len(partitions_list) <= 10:
            print(f"{part}: d_λ = {dim}, d_λ² = {dim*dim}")

    print(f"\nΣ d_λ² = {total_sq}")
    print(f"n! = {factorial(n)}")
    print(f"Match: {total_sq == factorial(n)}")

    # The largest irrep has dimension about n!/sqrt(2πn)
    # For the standard rep (n-1, 1): d = n-1
    # For two-row partitions: d grows combinatorially

    return total_sq

# ============================================================
# Part 6: Critical Threshold Analysis
# ============================================================

def find_critical_n():
    """Find the n where n! first exceeds N^3 = 2^{3n}."""
    print("\nFinding critical n where n! > N^3:")
    print("=" * 50)

    for n in range(1, 50):
        N = 2**n
        nfact = factorial(n)
        ncubed = N**3
        ratio = nfact / ncubed

        if ratio > 1:
            print(f"n={n}: n!={nfact:.2e}, N^3={ncubed:.2e}, ratio={ratio:.2f} ← THRESHOLD")

            # Continue a few more
            for n2 in range(n+1, n+5):
                N2 = 2**n2
                nfact2 = factorial(n2)
                ncubed2 = N2**3
                ratio2 = nfact2 / ncubed2
                print(f"n={n2}: n!={nfact2:.2e}, N^3={ncubed2:.2e}, ratio={ratio2:.2e}")
            break
        else:
            print(f"n={n}: ratio={ratio:.4f}")

    return n

# ============================================================
# Main
# ============================================================

def main():
    print("EXACT S_n DECOMPOSITION OF R^{2^n}")
    print("=" * 60)

    # Verify subset decomposition for small n
    print("\nVerifying subset representation decompositions:")
    for n in [3, 4, 5]:
        for k in range(n + 1):
            verify_subset_decomposition(n, k)

    # Full decomposition for n=4
    print("\n" + "=" * 60)
    full_decomposition(4)

    # Dimension squared analysis
    for n in [3, 4, 5, 6]:
        dimension_squared_analysis(n)

    # Find critical n
    critical_n = find_critical_n()

    # WIS analysis for several n
    print("\n" + "=" * 60)
    print("WIS ANALYSIS")
    print("=" * 60)

    for n in [4, 5, 6, 8, 10]:
        compute_wis_bounds(n)

if __name__ == "__main__":
    main()
