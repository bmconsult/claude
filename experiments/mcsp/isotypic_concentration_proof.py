#!/usr/bin/env python3
"""
Attempting to prove or disprove the Isotypic Concentration Lemma:
"Formulas of depth d touch at most exp(O(d)) isotypic components"

This requires understanding how AND/OR gates act on S_n representations.
"""

import numpy as np
from math import factorial
from itertools import permutations, combinations
from collections import defaultdict
from functools import lru_cache

# ============================================================
# Part 1: Representation Theory of S_n
# ============================================================

def partition_to_young_diagram(partition):
    """Convert partition tuple to Young diagram (list of row lengths)."""
    return list(partition)

@lru_cache(maxsize=1000)
def dimension_of_irrep(partition):
    """
    Compute dimension of S_n irrep corresponding to partition.
    Uses hook length formula: d_λ = n! / Π_{cells} hook_length(cell)
    """
    n = sum(partition)
    if n == 0:
        return 1

    # Build Young diagram
    rows = list(partition)
    rows = [r for r in rows if r > 0]

    if not rows:
        return 1

    # Compute hook lengths
    hook_product = 1
    for i, row_len in enumerate(rows):
        for j in range(row_len):
            # Hook length = cells to the right + cells below + 1
            cells_right = row_len - j - 1
            cells_below = sum(1 for k in range(i+1, len(rows)) if rows[k] > j)
            hook = cells_right + cells_below + 1
            hook_product *= hook

    from math import factorial
    return factorial(n) // hook_product

def partitions_of_n(n):
    """Generate all partitions of n."""
    if n == 0:
        yield ()
        return
    if n == 1:
        yield (1,)
        return

    # Standard partition generation
    def _partitions(n, max_val):
        if n == 0:
            yield ()
            return
        for i in range(min(n, max_val), 0, -1):
            for p in _partitions(n - i, i):
                yield (i,) + p

    for p in _partitions(n, n):
        yield p

def print_irrep_dimensions(n):
    """Print dimensions of all S_n irreps."""
    print(f"Irreducible representations of S_{n}:")
    total = 0
    for partition in partitions_of_n(n):
        dim = dimension_of_irrep(partition)
        print(f"  {partition}: dimension {dim}")
        total += dim * dim
    print(f"Total: Σ d_λ² = {total} (should equal {factorial(n)})")

# ============================================================
# Part 2: Littlewood-Richardson Coefficients
# ============================================================

def littlewood_richardson_simple(lambda1, lambda2, n):
    """
    Simplified LR coefficient estimation.
    Returns list of partitions that appear in V_{λ1} ⊗ V_{λ2}
    along with their multiplicities.

    For full accuracy, need proper LR rule implementation.
    Here we use a heuristic for small cases.
    """
    # For small n, enumerate directly
    if n <= 4:
        # The tensor product V_λ ⊗ V_μ decomposes into irreps
        # We'll estimate which ones appear

        # Trivial case: tensor with trivial rep
        if lambda1 == (n,):
            return [(lambda2, 1)]
        if lambda2 == (n,):
            return [(lambda1, 1)]

        # Sign case: tensor with sign rep
        if lambda1 == (1,)*n:
            # Tensor with sign = conjugate partition
            conj = conjugate_partition(lambda2)
            return [(conj, 1)]
        if lambda2 == (1,)*n:
            conj = conjugate_partition(lambda1)
            return [(conj, 1)]

        # Standard × Standard for n=3
        if n == 3 and lambda1 == (2,1) and lambda2 == (2,1):
            # (2,1) ⊗ (2,1) = (3) + (2,1) + (1,1,1) for S_3
            return [((3,), 1), ((2,1), 2), ((1,1,1), 1)]

        # General case: return all partitions (overestimate)
        return [(p, 1) for p in partitions_of_n(n)]

    # For larger n, use heuristic
    return [(p, 1) for p in partitions_of_n(n)]

def conjugate_partition(partition):
    """Compute conjugate (transpose) of a partition."""
    if not partition:
        return ()
    n = sum(partition)
    rows = list(partition)
    max_row = rows[0] if rows else 0

    # Transpose: column j has length = number of rows with length >= j+1
    conj = []
    for j in range(max_row):
        col_len = sum(1 for r in rows if r > j)
        conj.append(col_len)

    return tuple(conj)

# ============================================================
# Part 3: Formula Operations in Representation Space
# ============================================================

def boolean_function_to_representation(f, n):
    """
    Decompose a Boolean function f: {0,1}^n → {0,1} into S_n representations.

    Returns dict: partition -> coefficient (Fourier coefficient in S_n basis)
    """
    N = 2**n

    # Represent f as a vector in R^N
    vec = np.array([f[i] for i in range(N)], dtype=float)

    # For each partition, compute projection onto that isotypic component
    decomposition = {}

    for partition in partitions_of_n(n):
        dim = dimension_of_irrep(partition)

        # The projection formula: π_λ(f) = (d_λ / n!) Σ_σ χ_λ(σ) f^σ
        # For small n, we can compute this directly

        if n <= 4:
            # Compute character inner product
            projection_norm_sq = compute_projection_norm_sq(vec, partition, n)
            decomposition[partition] = projection_norm_sq
        else:
            # Estimate for larger n
            decomposition[partition] = 0.0

    return decomposition

def compute_projection_norm_sq(vec, partition, n):
    """
    Compute ||π_λ(f)||² for function represented by vec.

    ||π_λ(f)||² = (d_λ / n!) Σ_σ χ_λ(σ) <f, f^σ>

    For small n, compute directly.
    """
    N = 2**n

    # For efficiency, use Fourier analysis over (Z/2Z)^n first
    # Then project onto S_n components

    dim = dimension_of_irrep(partition)
    factorial_n = factorial(n)

    # Compute <f, f^σ> for each σ ∈ S_n
    total = 0.0
    for perm in permutations(range(n)):
        # Apply permutation to indices
        perm_vec = permute_function_vector(vec, perm, n)
        inner_product = np.dot(vec, perm_vec)

        # Get character value χ_λ(σ)
        chi = character_value(partition, perm, n)

        total += chi * inner_product

    return (dim / factorial_n) * total

def permute_function_vector(vec, perm, n):
    """
    Apply permutation to function vector.
    (σf)(x) = f(σ^{-1}(x)) where σ permutes bit positions.
    """
    N = 2**n
    inv_perm = [0] * n
    for i, p in enumerate(perm):
        inv_perm[p] = i

    new_vec = np.zeros(N)
    for x in range(N):
        # Apply inverse permutation to x
        new_x = sum((((x >> inv_perm[i]) & 1) << i) for i in range(n))
        new_vec[x] = vec[new_x]

    return new_vec

@lru_cache(maxsize=10000)
def character_value(partition, perm, n):
    """
    Compute character χ_λ(σ) of permutation σ in representation λ.

    For small n, use explicit formulas.
    """
    # Get cycle type of permutation
    cycle_type = get_cycle_type(perm, n)

    # Character depends only on cycle type
    return character_from_cycle_type(partition, cycle_type, n)

def get_cycle_type(perm, n):
    """Get cycle type (partition) of a permutation."""
    visited = [False] * n
    cycles = []

    for i in range(n):
        if not visited[i]:
            cycle_len = 0
            j = i
            while not visited[j]:
                visited[j] = True
                j = perm[j]
                cycle_len += 1
            cycles.append(cycle_len)

    cycles.sort(reverse=True)
    return tuple(cycles)

def character_from_cycle_type(partition, cycle_type, n):
    """
    Compute character from partition (irrep) and cycle type.
    Uses Murnaghan-Nakayama rule for small cases.
    """
    # Special cases
    if partition == (n,):  # Trivial representation
        return 1

    if partition == tuple([1]*n):  # Sign representation
        # Sign character = (-1)^(number of even cycles)
        even_cycles = sum(1 for c in cycle_type if c % 2 == 0)
        return (-1) ** even_cycles

    if n == 2:
        # S_2 has trivial (2) and sign (1,1)
        return 1 if partition == (2,) else (-1 if partition == (1,1) else 0)

    if n == 3:
        # S_3 character table
        # Cycle types: (3), (2,1), (1,1,1)
        # Partitions: (3), (2,1), (1,1,1)
        table = {
            ((3,), (3,)): 1,
            ((3,), (2,1)): 0,
            ((3,), (1,1,1)): 1,
            ((2,1), (3,)): 2,
            ((2,1), (2,1)): 0,
            ((2,1), (1,1,1)): -1,
            ((1,1,1), (3,)): 1,
            ((1,1,1), (2,1)): -1,
            ((1,1,1), (1,1,1)): 1,
        }
        return table.get((partition, cycle_type), 0)

    # For larger n, return estimate (would need Murnaghan-Nakayama)
    return 0

# ============================================================
# Part 4: Testing Isotypic Concentration
# ============================================================

def test_and_gate_concentration(n=3):
    """
    Test how AND gate affects isotypic spread.

    If f has mass in components C_f and g has mass in C_g,
    does f ∧ g have mass in at most |C_f| × |C_g| components?
    """
    N = 2**n

    print(f"Testing isotypic concentration for AND gate (n={n})")
    print()

    # Create random functions
    np.random.seed(42)

    # Function 1: random
    f1 = np.random.randint(0, 2, N)
    # Function 2: another random
    f2 = np.random.randint(0, 2, N)

    # AND of functions
    f_and = f1 & f2

    # Compute isotypic decompositions
    decomp1 = boolean_function_to_representation(f1, n)
    decomp2 = boolean_function_to_representation(f2, n)
    decomp_and = boolean_function_to_representation(f_and, n)

    print("Function 1 decomposition:")
    for p, v in decomp1.items():
        if abs(v) > 0.01:
            print(f"  {p}: {v:.4f}")

    print("\nFunction 2 decomposition:")
    for p, v in decomp2.items():
        if abs(v) > 0.01:
            print(f"  {p}: {v:.4f}")

    print("\nAND decomposition:")
    for p, v in decomp_and.items():
        if abs(v) > 0.01:
            print(f"  {p}: {v:.4f}")

    # Count significant components
    threshold = 0.01
    sig1 = sum(1 for v in decomp1.values() if abs(v) > threshold)
    sig2 = sum(1 for v in decomp2.values() if abs(v) > threshold)
    sig_and = sum(1 for v in decomp_and.values() if abs(v) > threshold)

    print(f"\nSignificant components (threshold={threshold}):")
    print(f"  f1: {sig1}, f2: {sig2}, f1 ∧ f2: {sig_and}")
    print(f"  Product bound: {sig1 * sig2}")

    if sig_and <= sig1 * sig2:
        print("  ✓ Concentration holds!")
    else:
        print("  ✗ Concentration violated!")

def test_depth_vs_isotypic_spread(n=3, max_depth=3):
    """
    Test how depth affects isotypic spread empirically.
    """
    N = 2**n

    print(f"\nTesting depth vs isotypic spread (n={n})")
    print()

    # Generate random formulas of increasing depth
    np.random.seed(42)

    for depth in range(max_depth + 1):
        # Generate a random depth-d formula
        if depth == 0:
            # Just a variable
            var_idx = np.random.randint(0, n)
            f = np.array([(x >> var_idx) & 1 for x in range(N)])
        else:
            # Combine previous depth functions
            f1_idx = np.random.randint(0, n)
            f1 = np.array([(x >> f1_idx) & 1 for x in range(N)])

            f2_idx = np.random.randint(0, n)
            f2 = np.array([(x >> f2_idx) & 1 for x in range(N)])

            # Apply random gates
            for _ in range(2**(depth-1)):
                gate = np.random.choice(['AND', 'OR', 'XOR'])
                if gate == 'AND':
                    f1 = f1 & f2
                elif gate == 'OR':
                    f1 = f1 | f2
                else:
                    f1 = f1 ^ f2

                f2_idx = np.random.randint(0, n)
                f2 = np.array([(x >> f2_idx) & 1 for x in range(N)])

            f = f1

        # Compute isotypic decomposition
        decomp = boolean_function_to_representation(f, n)

        # Count significant components
        threshold = 0.01
        sig = sum(1 for v in decomp.values() if abs(v) > threshold)
        total_mass = sum(abs(v) for v in decomp.values())

        print(f"Depth {depth}: {sig} significant components, total mass = {total_mass:.4f}")

def main():
    print("=" * 60)
    print("TESTING ISOTYPIC CONCENTRATION LEMMA")
    print("=" * 60)
    print()

    # Show S_n irrep dimensions
    for n in [2, 3, 4]:
        print_irrep_dimensions(n)
        print()

    # Test AND gate concentration
    test_and_gate_concentration(n=3)

    # Test depth vs spread
    test_depth_vs_isotypic_spread(n=3, max_depth=3)

if __name__ == "__main__":
    main()
