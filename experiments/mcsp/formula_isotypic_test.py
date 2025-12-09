#!/usr/bin/env python3
"""
Direct computational test: How do formulas relate to isotypic structure?

Goal: Empirically test whether formulas of bounded size can distinguish
truth tables with different isotypic distributions.
"""

import numpy as np
from math import factorial, comb
from itertools import permutations, product
from collections import defaultdict

# ============================================================
# Part 1: Generate All Formulas of Given Size
# ============================================================

def generate_formulas(n, max_size):
    """
    Generate all Boolean formulas over n variables with at most max_size gates.

    A formula is represented as a tree:
    - Leaf: variable index 0..n-1 or constant 0/1
    - Internal: (op, left, right) where op in ['AND', 'OR', 'XOR']
    """
    formulas = []

    # Size 0: just leaves
    for i in range(n):
        formulas.append(('VAR', i))
    formulas.append(('CONST', 0))
    formulas.append(('CONST', 1))

    if max_size == 0:
        return formulas

    # Size s: combine formulas of size < s
    for s in range(1, max_size + 1):
        new_formulas = []
        for s1 in range((s+1)//2 + 1):  # s1 <= s2, s1 + s2 + 1 = s
            s2 = s - 1 - s1
            if s2 < s1:
                continue

            formulas_s1 = [f for f in formulas if formula_size(f) == s1]
            formulas_s2 = [f for f in formulas if formula_size(f) == s2]

            for f1 in formulas_s1:
                for f2 in formulas_s2:
                    for op in ['AND', 'OR', 'XOR']:
                        new_formulas.append((op, f1, f2))
                        if s1 != s2:  # Asymmetric case
                            new_formulas.append((op, f2, f1))

        formulas.extend(new_formulas)

    return formulas

def formula_size(f):
    """Count internal nodes in formula tree."""
    if f[0] in ['VAR', 'CONST']:
        return 0
    return 1 + formula_size(f[1]) + formula_size(f[2])

def evaluate_formula(f, x, n):
    """Evaluate formula f on input x (integer)."""
    if f[0] == 'VAR':
        return (x >> f[1]) & 1
    if f[0] == 'CONST':
        return f[1]
    if f[0] == 'AND':
        return evaluate_formula(f[1], x, n) & evaluate_formula(f[2], x, n)
    if f[0] == 'OR':
        return evaluate_formula(f[1], x, n) | evaluate_formula(f[2], x, n)
    if f[0] == 'XOR':
        return evaluate_formula(f[1], x, n) ^ evaluate_formula(f[2], x, n)

def formula_to_truth_table(f, n):
    """Compute full truth table of formula."""
    N = 2**n
    return tuple(evaluate_formula(f, x, n) for x in range(N))

# ============================================================
# Part 2: Isotypic Analysis
# ============================================================

def apply_permutation(tt, perm, n):
    """Apply permutation to truth table (permute variable indices)."""
    N = 2**n
    inv_perm = [0] * n
    for i, p in enumerate(perm):
        inv_perm[p] = i

    new_tt = [0] * N
    for x in range(N):
        # Apply inverse permutation to x
        new_x = sum(((x >> inv_perm[i]) & 1) << i for i in range(n))
        new_tt[x] = tt[new_x]

    return tuple(new_tt)

def compute_orbit(tt, n, max_orbit=1000):
    """Compute S_n orbit of truth table."""
    orbit = {tt}
    to_process = [tt]

    for perm in permutations(range(n)):
        if len(orbit) >= max_orbit:
            break
        new_tt = apply_permutation(tt, perm, n)
        if new_tt not in orbit:
            orbit.add(new_tt)

    return orbit

def hamming_weight_distribution(tt, n):
    """Compute how truth values distribute across Hamming weights."""
    N = 2**n
    dist = defaultdict(int)

    for x in range(N):
        hw = bin(x).count('1')
        dist[hw] += tt[x]

    return dict(dist)

# ============================================================
# Part 3: Simple Isotypic Invariants
# ============================================================

def symmetric_invariant(tt, n):
    """
    Compute a symmetric invariant of the truth table.

    This invariant is S_n-invariant and captures some isotypic structure.
    """
    N = 2**n

    # Count by Hamming weight (most basic symmetric invariant)
    hw_counts = [0] * (n + 1)
    for x in range(N):
        hw = bin(x).count('1')
        hw_counts[hw] += tt[x]

    return tuple(hw_counts)

def level_invariants(tt, n):
    """
    Compute Fourier-level invariants.

    These are S_n-invariant but don't capture full isotypic structure.
    """
    N = 2**n

    # Walsh-Hadamard transform
    f_hat = np.array(tt, dtype=float) * 2 - 1  # Convert to ±1

    # Simple DFT-like computation
    for i in range(n):
        f_hat_new = np.zeros(N)
        for x in range(N):
            x_flip = x ^ (1 << i)
            f_hat_new[x] = f_hat[x] + f_hat[x_flip]
        f_hat = f_hat_new / 2

    # Level k mass = sum of f_hat[S]^2 for |S| = k
    level_mass = [0.0] * (n + 1)
    for x in range(N):
        k = bin(x).count('1')
        level_mass[k] += f_hat[x] ** 2

    return tuple(round(m, 6) for m in level_mass)

# ============================================================
# Part 4: Testing Formula-Isotypic Connection
# ============================================================

def compute_all_invariants(n, max_formula_size):
    """
    For each formula, compute its truth table and invariants.
    """
    print(f"Computing all formulas up to size {max_formula_size} for n={n}...")

    formulas = generate_formulas(n, max_formula_size)
    print(f"Total formulas: {len(formulas)}")

    # Group by truth table
    tt_to_formulas = defaultdict(list)
    for f in formulas:
        tt = formula_to_truth_table(f, n)
        tt_to_formulas[tt].append(f)

    print(f"Distinct truth tables computed: {len(tt_to_formulas)}")

    # Compute invariants
    tt_data = []
    for tt, formulas_list in tt_to_formulas.items():
        min_size = min(formula_size(f) for f in formulas_list)
        orbit_size = len(compute_orbit(tt, n, max_orbit=factorial(n)))
        sym_inv = symmetric_invariant(tt, n)
        level_inv = level_invariants(tt, n)

        tt_data.append({
            'tt': tt,
            'min_size': min_size,
            'orbit_size': orbit_size,
            'sym_inv': sym_inv,
            'level_inv': level_inv,
            'num_ones': sum(tt)
        })

    return tt_data

def analyze_isotypic_patterns(tt_data, n):
    """
    Analyze how isotypic invariants relate to formula complexity.
    """
    print("\n" + "=" * 60)
    print("ISOTYPIC PATTERNS ANALYSIS")
    print("=" * 60)

    # Group by orbit size
    by_orbit = defaultdict(list)
    for d in tt_data:
        by_orbit[d['orbit_size']].append(d)

    print("\nBy orbit size:")
    for orbit_size in sorted(by_orbit.keys()):
        items = by_orbit[orbit_size]
        avg_size = sum(d['min_size'] for d in items) / len(items)
        print(f"  Orbit {orbit_size}: {len(items)} functions, avg formula size {avg_size:.2f}")

    # Group by symmetric invariant
    by_sym = defaultdict(list)
    for d in tt_data:
        by_sym[d['sym_inv']].append(d)

    print(f"\nDistinct symmetric invariants: {len(by_sym)}")

    # Check if symmetric invariant determines complexity
    print("\nSample symmetric invariants:")
    for sym_inv in list(by_sym.keys())[:10]:
        items = by_sym[sym_inv]
        sizes = [d['min_size'] for d in items]
        print(f"  {sym_inv}: {len(items)} functions, sizes {set(sizes)}")

    # Group by level invariant
    by_level = defaultdict(list)
    for d in tt_data:
        by_level[d['level_inv']].append(d)

    print(f"\nDistinct level invariants: {len(by_level)}")

    # Key question: Do S_n-invariant properties determine formula complexity?
    print("\n" + "=" * 60)
    print("KEY QUESTION: Do S_n invariants determine formula complexity?")
    print("=" * 60)

    # For each orbit, check if all functions have the same complexity
    orbit_complexity_varies = 0
    orbit_complexity_same = 0

    for orbit_size, items in by_orbit.items():
        sizes = set(d['min_size'] for d in items)
        if len(sizes) > 1:
            orbit_complexity_varies += 1
        else:
            orbit_complexity_same += 1

    print(f"\nOrbits with same complexity: {orbit_complexity_same}")
    print(f"Orbits with varying complexity: {orbit_complexity_varies}")

    if orbit_complexity_varies > 0:
        print("\n⚠ IMPORTANT: Some orbits have functions with different formula complexities!")
        print("This means S_n-isotypic structure alone doesn't determine formula complexity.")
    else:
        print("\n✓ All orbits have uniform complexity.")
        print("This is consistent with isotypic structure determining complexity.")

def main():
    print("FORMULA-ISOTYPIC CONNECTION TEST")
    print("=" * 60)

    # Small n for exhaustive analysis
    n = 3
    max_size = 4

    tt_data = compute_all_invariants(n, max_size)
    analyze_isotypic_patterns(tt_data, n)

    # Also test n=4 with smaller formula size
    print("\n" + "=" * 60)
    n = 4
    max_size = 2

    tt_data = compute_all_invariants(n, max_size)
    analyze_isotypic_patterns(tt_data, n)

if __name__ == "__main__":
    main()
