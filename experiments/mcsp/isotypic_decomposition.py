#!/usr/bin/env python3
"""
Exploring the S_n-isotypic decomposition of functions on {0,1}^n
and its connection to circuit complexity.

Key insight: S_n acts on truth tables by permuting variable names.
Circuit complexity is S_n-invariant.
The isotypic decomposition might reveal non-local structure.
"""

import numpy as np
from itertools import permutations, combinations
from collections import defaultdict
from functools import lru_cache

def truth_table_to_function(tt, n):
    """Convert truth table (list) to function dict."""
    return {tuple((x >> i) & 1 for i in range(n)): tt[x] for x in range(2**n)}

def apply_permutation(func, perm, n):
    """
    Apply permutation perm to function func.
    If func: {0,1}^n -> {0,1}, then (perm·func)(x) = func(perm^{-1}(x))
    where perm permutes the coordinates of x.
    """
    inv_perm = [0] * n
    for i, p in enumerate(perm):
        inv_perm[p] = i

    new_func = {}
    for x, v in func.items():
        # Apply inverse permutation to x
        new_x = tuple(x[inv_perm[i]] for i in range(n))
        new_func[new_x] = v
    return new_func

def function_to_vector(func, n):
    """Convert function dict to vector in R^{2^n}."""
    N = 2**n
    vec = np.zeros(N)
    for x, v in func.items():
        idx = sum(x[i] << i for i in range(n))
        vec[idx] = v
    return vec

def get_orbit(func, n):
    """Get the S_n-orbit of a function."""
    orbit = set()
    for perm in permutations(range(n)):
        perm_func = apply_permutation(func, perm, n)
        # Convert to hashable form
        orbit.add(tuple(sorted(perm_func.items())))
    return orbit

def is_symmetric(func, n):
    """Check if function is fully symmetric (S_n-invariant)."""
    for perm in permutations(range(n)):
        if apply_permutation(func, perm, n) != func:
            return False
    return True

def compute_symmetry_type(func, n):
    """
    Compute the "symmetry type" of a function.
    Returns the orbit size under S_n.
    Symmetric functions have orbit size 1.
    """
    return len(get_orbit(func, n))

def compute_circuit_complexity_local(tt, max_size=10):
    """Compute minimum circuit complexity using enumeration."""
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

        if not new_functions:
            break

    return max_size

def analyze_circuit_complexity_by_symmetry(n, max_complexity=5):
    """
    For each circuit complexity level, analyze the symmetry structure.
    """
    N = 2**n
    num_tt = 2**N

    print(f"Analyzing n={n} (N={N}, {num_tt} truth tables)")
    print()

    # Sample truth tables and compute complexity + symmetry
    complexity_by_orbit_size = defaultdict(list)
    symmetric_functions = []

    for tt_int in range(num_tt):
        tt = [(tt_int >> i) & 1 for i in range(N)]
        func = truth_table_to_function(tt, n)

        complexity = compute_circuit_complexity_local(tt, max_complexity)
        orbit_size = compute_symmetry_type(func, n)

        complexity_by_orbit_size[orbit_size].append(complexity)

        if orbit_size == 1:
            symmetric_functions.append((tt, complexity))

    print("=== Results ===")
    print(f"\nSymmetric functions (orbit size 1): {len(symmetric_functions)}")
    for tt, c in symmetric_functions:
        print(f"  TT={tt}, complexity={c}")

    print(f"\nComplexity by orbit size:")
    for orbit_size in sorted(complexity_by_orbit_size.keys()):
        complexities = complexity_by_orbit_size[orbit_size]
        avg = np.mean(complexities)
        print(f"  Orbit size {orbit_size}: {len(complexities)} functions, avg complexity = {avg:.2f}")

    return complexity_by_orbit_size

def compute_isotypic_projection_trivial(func, n):
    """
    Project function onto the trivial (symmetric) isotypic component.
    This is the average over all permutations.
    """
    N = 2**n
    vec = function_to_vector(func, n)
    total = np.zeros(N)
    count = 0

    for perm in permutations(range(n)):
        perm_func = apply_permutation(func, perm, n)
        perm_vec = function_to_vector(perm_func, n)
        total += perm_vec
        count += 1

    return total / count

def compute_isotypic_structure(n):
    """
    Analyze the isotypic structure of the space R^{2^n} under S_n.
    """
    from math import factorial

    N = 2**n
    order = factorial(n)

    print(f"Isotypic structure for n={n}")
    print(f"Space dimension: {N}")
    print(f"|S_n| = {order}")
    print()

    # The dimension of the trivial isotypic component = number of S_n orbits on {0,1}^n
    # This equals the number of distinct Hamming weights, which is n+1
    print(f"Trivial isotypic component dimension: {n+1}")
    print(f"  (Functions depending only on Hamming weight)")

    # For the standard representation (n-1 dimensional):
    # It appears in the decomposition with some multiplicity
    # The total must add up to 2^n

    print()
    print("The decomposition involves Specht modules S^λ for various partitions λ of n.")
    print("Each level k (functions on k-subsets) contributes specific representations.")

def verify_symmetry_invariance_of_complexity():
    """
    Verify that circuit complexity is indeed S_n-invariant.
    """
    n = 3
    N = 2**n
    num_tt = 2**N

    print("Verifying circuit complexity is S_n-invariant...")

    violations = 0
    for tt_int in range(num_tt):
        tt = [(tt_int >> i) & 1 for i in range(N)]
        func = truth_table_to_function(tt, n)
        base_complexity = compute_circuit_complexity_local(tt)

        for perm in permutations(range(n)):
            perm_func = apply_permutation(func, perm, n)
            perm_tt = [perm_func[tuple((x >> i) & 1 for i in range(n))] for x in range(N)]
            perm_complexity = compute_circuit_complexity_local(perm_tt)

            if perm_complexity != base_complexity:
                violations += 1
                print(f"  Violation! TT={tt}, perm={perm}, base_c={base_complexity}, perm_c={perm_complexity}")

    if violations == 0:
        print("  VERIFIED: Circuit complexity is S_n-invariant!")
    else:
        print(f"  Found {violations} violations!")

    return violations == 0

def main():
    print("=" * 60)
    print("S_n-ISOTYPIC STRUCTURE OF BOOLEAN FUNCTIONS")
    print("=" * 60)
    print()

    # First verify invariance
    verify_symmetry_invariance_of_complexity()
    print()

    # Analyze structure
    compute_isotypic_structure(3)
    print()

    # Analyze complexity by symmetry
    print("=" * 60)
    print("CIRCUIT COMPLEXITY BY SYMMETRY TYPE")
    print("=" * 60)
    analyze_circuit_complexity_by_symmetry(n=2, max_complexity=5)

if __name__ == "__main__":
    main()
