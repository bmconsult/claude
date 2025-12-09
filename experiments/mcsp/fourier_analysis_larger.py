#!/usr/bin/env python3
"""
Fourier Analysis of Gap-MCSP - Larger Scale with Sampling
"""

import numpy as np
from itertools import combinations
from collections import defaultdict
import random

def int_to_truth_table(x, n_vars):
    """Convert integer to truth table for n_vars variables."""
    n = 2 ** n_vars
    return [(x >> i) & 1 for i in range(n)]

def parity_of_subset(tt, subset):
    """Compute χ_S(T) = (-1)^{⊕_{i∈S} T_i}"""
    parity = 0
    for i in subset:
        parity ^= tt[i]
    return 1 if parity == 0 else -1

def compute_circuit_complexity_fast(tt, max_size=10):
    """
    Faster circuit complexity estimation.
    Uses dynamic programming with early termination.
    """
    n = int(np.log2(len(tt)))
    N = len(tt)
    tt_tuple = tuple(tt)

    # Check constants
    if all(b == 0 for b in tt): return 0
    if all(b == 1 for b in tt): return 0

    # Check single variables and negations
    for i in range(n):
        var_tt = tuple((x >> i) & 1 for x in range(N))
        if tt_tuple == var_tt: return 0
        if tt_tuple == tuple(1 - b for b in var_tt): return 1

    # Quick check: Hamming weight gives lower bound on some functions
    hw = sum(tt)

    # Build achievable functions
    base = set()
    for i in range(n):
        var_tt = tuple((x >> i) & 1 for x in range(N))
        base.add(var_tt)
        base.add(tuple(1-b for b in var_tt))
    base.add(tuple(0 for _ in range(N)))
    base.add(tuple(1 for _ in range(N)))

    if tt_tuple in base: return 0

    all_reachable = set(base)
    prev_new = base

    for s in range(1, max_size + 1):
        new_functions = set()
        prev_list = list(prev_new)
        all_list = list(all_reachable)

        # Only combine new functions with all functions
        for f1 in prev_list:
            for f2 in all_list:
                and_tt = tuple(a & b for a, b in zip(f1, f2))
                or_tt = tuple(a | b for a, b in zip(f1, f2))
                if and_tt not in all_reachable:
                    new_functions.add(and_tt)
                if or_tt not in all_reachable:
                    new_functions.add(or_tt)

        if tt_tuple in new_functions:
            return s

        all_reachable.update(new_functions)
        prev_new = new_functions

        if not new_functions:  # No new functions possible
            break

    return max_size

def analyze_symmetry_structure(n_vars=3):
    """
    Investigate why Fourier weight is zero at odd levels.
    """
    N = 2 ** n_vars
    num_tt = 2 ** N

    print(f"Analyzing symmetry structure for n={n_vars}, N={N}")

    # Compute complexities
    complexities = []
    for T_int in range(num_tt):
        tt = int_to_truth_table(T_int, n_vars)
        c = compute_circuit_complexity_fast(tt)
        complexities.append(c)

    # For each complexity level, check symmetry properties
    for threshold in [1, 2, 3]:
        simple = [i for i, c in enumerate(complexities) if c <= threshold]
        print(f"\nThreshold {threshold}: {len(simple)} simple truth tables")

        # Check: are simple truth tables closed under complement?
        complement_closed = True
        for T_int in simple:
            tt = int_to_truth_table(T_int, n_vars)
            comp_tt = tuple(1 - b for b in tt)
            comp_int = sum(b << i for i, b in enumerate(comp_tt))
            if comp_int not in simple:
                complement_closed = False
                break
        print(f"  Complement closed: {complement_closed}")

        # Check: are simple truth tables closed under bit reversal?
        reversal_closed = True
        for T_int in simple:
            tt = int_to_truth_table(T_int, n_vars)
            rev_tt = tuple(reversed(tt))
            rev_int = sum(b << i for i, b in enumerate(rev_tt))
            if rev_int not in simple:
                reversal_closed = False
                break
        print(f"  Reversal closed: {reversal_closed}")

def estimate_fourier_weight_n4(threshold=3, num_samples=1000):
    """
    Estimate Fourier spectrum for n=4 using sampling.
    """
    n_vars = 4
    N = 2 ** n_vars  # N = 16
    num_tt = 2 ** N   # 65536 truth tables

    print(f"\nEstimating Fourier spectrum for n={n_vars}, N={N}")
    print(f"Total truth tables: {num_tt}")
    print(f"Complexity threshold: {threshold}")
    print(f"Sampling {num_samples} random Fourier subsets per level")

    # First, we need to know which truth tables are "simple"
    # This is expensive - let's sample
    print("\nSampling truth tables to estimate simple fraction...")

    sample_size = 2000
    simple_samples = 0
    complexity_counts = defaultdict(int)

    for _ in range(sample_size):
        T_int = random.randint(0, num_tt - 1)
        tt = int_to_truth_table(T_int, n_vars)
        c = compute_circuit_complexity_fast(tt, max_size=threshold + 3)
        complexity_counts[min(c, threshold + 1)] += 1
        if c <= threshold:
            simple_samples += 1

    simple_fraction = simple_samples / sample_size
    print(f"Estimated simple fraction: {simple_fraction:.4f}")
    print(f"Complexity distribution: {dict(complexity_counts)}")

    # For Fourier analysis, we need to sample both truth tables and subsets
    # ĝ(S) = E_T[g(T) × χ_S(T)]
    # We can estimate this by sampling

    print("\nEstimating Fourier weight by level...")

    # For each level, sample random subsets and estimate their coefficient
    for level in [0, 2, 4, 6, 8, 10, 12, 14, 16]:  # Even levels only (odd seem to be 0)
        if level > N:
            continue

        # Sample random subsets at this level
        level_coefs_sq = []

        for _ in range(min(num_samples, int(np.math.comb(N, level)) if level <= N//2 else num_samples)):
            # Random subset of size 'level'
            subset = tuple(sorted(random.sample(range(N), level)))

            # Estimate E_T[g(T) × χ_S(T)] by sampling truth tables
            sum_prod = 0
            for _ in range(500):  # Sample truth tables
                T_int = random.randint(0, num_tt - 1)
                tt = int_to_truth_table(T_int, n_vars)
                c = compute_circuit_complexity_fast(tt, max_size=threshold + 1)
                g_val = 1 if c <= threshold else -1
                chi_val = parity_of_subset(tt, subset)
                sum_prod += g_val * chi_val

            coef_estimate = sum_prod / 500
            level_coefs_sq.append(coef_estimate ** 2)

        avg_coef_sq = np.mean(level_coefs_sq) if level_coefs_sq else 0
        num_subsets = int(np.math.comb(N, level))
        estimated_total_weight = avg_coef_sq * num_subsets

        print(f"Level {level:2d}: avg|coef|² ≈ {avg_coef_sq:.6f}, "
              f"C({N},{level}) = {num_subsets:6d}, "
              f"est total weight ≈ {estimated_total_weight:.4f}")

    # The key question: for N^{3+ε} formula, weight should be ≤ (3+ε)*log(N)
    # For N=16, log(N) = 4, so threshold ≈ 12
    # Weight at levels 13-16 should be negligible for small formula

    print(f"\nFor N^3 formula bound on {N}-bit input:")
    print(f"  Weight should be concentrated at levels ≤ {3 * np.log2(N):.1f}")
    print(f"  If significant weight at levels > 12, this suggests non-small formula")

def main():
    # First analyze symmetry to understand odd-level zeroes
    analyze_symmetry_structure(n_vars=3)

    # Then try n=4
    estimate_fourier_weight_n4(threshold=3, num_samples=500)

if __name__ == "__main__":
    main()
