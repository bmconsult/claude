#!/usr/bin/env python3
"""
Fourier Analysis of Gap-MCSP
Attempting to understand the Fourier spectrum of the meta-complexity function.

Key question: Does Gap-MCSP have high Fourier weight at level > O(log N)?
If yes, this could give formula lower bounds beyond the locality barrier.
"""

import numpy as np
from itertools import combinations, product
from collections import defaultdict
import json

def truth_table_to_int(tt):
    """Convert truth table (list of 0/1) to integer."""
    return sum(b << i for i, b in enumerate(tt))

def int_to_truth_table(x, n_vars):
    """Convert integer to truth table for n_vars variables."""
    n = 2 ** n_vars
    return [(x >> i) & 1 for i in range(n)]

def parity_of_subset(tt, subset):
    """
    Compute χ_S(T) = (-1)^{⊕_{i∈S} T_i}
    Returns 1 or -1.
    """
    parity = 0
    for i in subset:
        parity ^= tt[i]
    return 1 if parity == 0 else -1

def compute_fourier_coefficient(f_indicator, subset, N):
    """
    Compute Fourier coefficient ĝ(S) = E_T[g(T) × χ_S(T)]
    where g(T) = 1 if f_indicator[T] else -1.

    f_indicator: list of booleans, f_indicator[i] = True if truth table i is "simple"
    """
    total = 0
    for T_int in range(2**N):
        tt = int_to_truth_table(T_int, int(np.log2(N)))
        g_val = 1 if f_indicator[T_int] else -1
        chi_val = parity_of_subset(tt, subset)
        total += g_val * chi_val
    return total / (2**N)

def compute_circuit_complexity(tt, max_size=20):
    """
    Compute minimum circuit complexity of truth table tt.
    Uses brute force enumeration of circuits.
    Returns the minimum size, or max_size if not found.
    """
    n = int(np.log2(len(tt)))
    N = len(tt)

    # Convert to tuple for hashing
    tt_tuple = tuple(tt)

    # Special cases
    if all(b == 0 for b in tt):
        return 0  # constant 0
    if all(b == 1 for b in tt):
        return 0  # constant 1

    # Check if it's a single variable or its negation
    for i in range(n):
        var_tt = tuple((x >> i) & 1 for x in range(N))
        if tt_tuple == var_tt:
            return 0  # single variable
        neg_var_tt = tuple(1 - b for b in var_tt)
        if tt_tuple == neg_var_tt:
            return 1  # negation of single variable

    # Dynamic programming approach
    # achievable[s] = set of truth tables achievable with s gates
    achievable = [set() for _ in range(max_size + 1)]

    # Base case: single variables and their negations
    base_functions = set()
    for i in range(n):
        var_tt = tuple((x >> i) & 1 for x in range(N))
        neg_var_tt = tuple(1 - b for b in var_tt)
        base_functions.add(var_tt)
        base_functions.add(neg_var_tt)

    # Constants
    base_functions.add(tuple(0 for _ in range(N)))
    base_functions.add(tuple(1 for _ in range(N)))

    achievable[0] = base_functions

    if tt_tuple in achievable[0]:
        return 0

    # All functions reachable so far
    all_reachable = set(achievable[0])

    for s in range(1, max_size + 1):
        new_functions = set()

        # Try combining any two previously reachable functions
        reachable_list = list(all_reachable)
        for i, f1 in enumerate(reachable_list):
            for f2 in reachable_list[i:]:
                # AND
                and_tt = tuple(a & b for a, b in zip(f1, f2))
                if and_tt not in all_reachable:
                    new_functions.add(and_tt)

                # OR
                or_tt = tuple(a | b for a, b in zip(f1, f2))
                if or_tt not in all_reachable:
                    new_functions.add(or_tt)

        # Also NOT of anything reachable (but NOT doesn't add to size in some models)
        # For fan-in-2 AND/OR/NOT, NOT is free once computed

        achievable[s] = new_functions
        all_reachable.update(new_functions)

        if tt_tuple in new_functions:
            return s

    return max_size  # didn't find

def analyze_fourier_spectrum_small(n_vars=2, complexity_threshold=2):
    """
    For small n, compute the Fourier spectrum of Gap-MCSP.

    Gap-MCSP(T) = 1 if circuit_complexity(T) <= threshold, else 0.
    We convert to ±1: g(T) = 1 if simple, -1 if complex.
    """
    N = 2 ** n_vars
    num_truth_tables = 2 ** N

    print(f"Analyzing Fourier spectrum for n={n_vars}, N={N}")
    print(f"Number of truth tables: {num_truth_tables}")
    print(f"Complexity threshold: {complexity_threshold}")
    print()

    # Compute complexity of all truth tables
    print("Computing circuit complexities...")
    complexities = []
    for T_int in range(num_truth_tables):
        tt = int_to_truth_table(T_int, n_vars)
        c = compute_circuit_complexity(tt)
        complexities.append(c)

    # Create indicator for "simple" truth tables
    simple_indicator = [c <= complexity_threshold for c in complexities]
    num_simple = sum(simple_indicator)

    print(f"Simple truth tables (complexity <= {complexity_threshold}): {num_simple}")
    print(f"Complex truth tables: {num_truth_tables - num_simple}")
    print()

    # Compute Fourier coefficients for each level
    print("Computing Fourier coefficients by level...")

    fourier_by_level = defaultdict(list)

    for level in range(N + 1):
        subsets_at_level = list(combinations(range(N), level))
        total_weight_sq = 0

        for subset in subsets_at_level:
            coef = compute_fourier_coefficient(simple_indicator, subset, N)
            fourier_by_level[level].append((subset, coef))
            total_weight_sq += coef ** 2

        print(f"Level {level}: {len(subsets_at_level)} subsets, total weight^2 = {total_weight_sq:.6f}")

    # Summary statistics
    print("\n=== Fourier Spectrum Summary ===")
    for level in range(N + 1):
        weights = [c for _, c in fourier_by_level[level]]
        if weights:
            max_coef = max(abs(c) for c in weights)
            total_sq = sum(c**2 for c in weights)
            print(f"Level {level}: max|coef| = {max_coef:.6f}, Σcoef² = {total_sq:.6f}")

    return fourier_by_level, complexities

def find_high_level_weight(n_vars, complexity_threshold):
    """
    Determine if Gap-MCSP has significant Fourier weight at high levels.

    For U₂-Formula of size N^c, weight should be at levels ≤ c log N.
    If weight at level > c log N is significant, we get lower bounds.
    """
    N = 2 ** n_vars

    fourier_by_level, complexities = analyze_fourier_spectrum_small(n_vars, complexity_threshold)

    # For N^3 formula, weight should be at levels ≤ 3 log N
    # For n=2, N=4, log N = 2, so level threshold = 6 (but N=4, so max level is 4)
    # For n=3, N=8, log N = 3, so level threshold = 9 (but N=8)

    log_N = np.log2(N)
    threshold_level = int(3 * log_N)

    print(f"\nFor N^3 formula bound:")
    print(f"  N = {N}, log N = {log_N:.2f}")
    print(f"  Expected weight at levels <= {threshold_level}")
    print(f"  Max level = {N}")

    high_level_weight = 0
    low_level_weight = 0

    for level in range(N + 1):
        level_weight = sum(c**2 for _, c in fourier_by_level[level])
        if level > threshold_level:
            high_level_weight += level_weight
        else:
            low_level_weight += level_weight

    print(f"\nWeight at levels <= {threshold_level}: {low_level_weight:.6f}")
    print(f"Weight at levels > {threshold_level}: {high_level_weight:.6f}")

    if high_level_weight > 0.01:  # Significant threshold
        print("\n*** SIGNIFICANT HIGH-LEVEL FOURIER WEIGHT DETECTED ***")
        print("This suggests Gap-MCSP might not be in small U₂-Formula!")
    else:
        print("\nMost weight at low levels (consistent with small formula)")

    return fourier_by_level, high_level_weight, low_level_weight

if __name__ == "__main__":
    print("=" * 60)
    print("FOURIER ANALYSIS OF GAP-MCSP")
    print("=" * 60)
    print()

    # Start small
    for n_vars in [2, 3]:
        print(f"\n{'='*60}")
        print(f"n = {n_vars} variables")
        print(f"{'='*60}\n")

        # Try different complexity thresholds
        for threshold in [1, 2, 3]:
            print(f"\n--- Threshold = {threshold} ---")
            result = find_high_level_weight(n_vars, threshold)
            print()
