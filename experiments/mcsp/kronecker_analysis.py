#!/usr/bin/env python3
"""
Kronecker Coefficient Analysis for Formula-Isotypic Connection

Key insight: When we compute f ∧ g, the isotypic structure transforms via Kronecker products.
The Kronecker coefficients g^ν_{λμ} control how V_λ ⊗ V_μ decomposes.

Critical formula: d_λ × d_μ = Σ_ν g^ν_{λμ} × d_ν

This means: total weighted dimension is MULTIPLICATIVE under tensor product!
"""

import numpy as np
from math import factorial, comb
from functools import lru_cache
from itertools import permutations

# ============================================================
# Hook Length Formula for Dimensions
# ============================================================

@lru_cache(maxsize=10000)
def hook_length(partition):
    """Dimension of S_n irrep via hook length formula."""
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
    """Generate all partitions of n."""
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
# Kronecker Coefficient Bounds
# ============================================================

def kronecker_support_bound(lambda_part, mu_part):
    """
    Upper bound on number of ν with g^ν_{λμ} > 0.

    Known bounds:
    1. |{ν : g^ν_{λμ} > 0}| ≤ min(d_λ, d_μ, d_ν)
    2. For "rectangular" partitions, sharper bounds exist

    For our purposes, we use the "saturation" bound:
    The support is contained in partitions ν where:
    - |ν| = |λ| = |μ| = n
    - ν is dominated by λ + μ (in the dominance order)
    """
    n = sum(lambda_part)
    d_lambda = hook_length(lambda_part)
    d_mu = hook_length(mu_part)

    # Crude bound: at most min(d_λ, d_μ) nonzero Kronecker coefficients
    # This is because g^ν_{λμ} appears in the decomposition of a d_λ × d_μ matrix
    return min(d_lambda, d_mu)

def weighted_dimension_product(n):
    """
    Analyze how weighted dimension grows under formula operations.

    Key formula: d_λ × d_μ = Σ_ν g^ν_{λμ} × d_ν

    This means if f has weighted isotypic dimension W_f and g has W_g,
    then f ∧ g has weighted dimension at most W_f × W_g.
    """
    parts = list(partitions(n))
    dims = {p: hook_length(p) for p in parts}

    print(f"S_{n} irrep dimensions:")
    for p in sorted(parts, key=lambda x: -dims[x]):
        print(f"  {p}: d = {dims[p]}")

    print(f"\nSum of dimensions: {sum(dims.values())}")
    print(f"Sum of d²: {sum(d**2 for d in dims.values())} = {factorial(n)} (= n!)")

    # For a variable x_i:
    # - Trivial rep (n): d = 1
    # - Standard rep (n-1,1): d = n-1
    # - Total weighted dimension: 1 + (n-1) = n

    print(f"\nVariable x_i weighted dimension: {1 + (n-1)} = {n}")

    # For f ∧ g with weighted dimensions W_f, W_g:
    # W_{f∧g} ≤ W_f × W_g

    # For depth-d formula starting from variables:
    # W ≤ n^{2^d}

    print(f"\nFormula depth analysis:")
    for d in range(1, 8):
        w = n ** (2**d)
        size = 2**d
        print(f"  Depth {d} (size ~{size}): weighted dim ≤ {w:.2e}")
        if w > factorial(n):
            print(f"    (exceeds n! = {factorial(n):.2e}, so this bound is vacuous)")
            break

    return dims

# ============================================================
# The Key Calculation: When Does Weighted Dimension Reach n!?
# ============================================================

def find_critical_depth(n):
    """
    Find depth d where n^{2^d} first exceeds n!.

    This tells us the MAXIMUM depth where the isotypic bound is meaningful.
    """
    nfact = factorial(n)

    print(f"\nFinding critical depth for n={n}:")
    print(f"n! = {nfact:.2e}")

    for d in range(1, 20):
        w = n ** (2**d)
        if w >= nfact:
            print(f"Critical depth: {d} (n^{2^d} = {w:.2e} ≥ n!)")
            print(f"Formula size at this depth: ~2^{d} = {2**d}")
            return d

    return None

def analyze_bound_tightness():
    """
    Analyze whether the weighted dimension bound can give N^{3+ε}.

    We need: formula size s implies weighted dim ≤ something
    And: Gap-MCSP requires weighted dim ≈ n!

    Current bound: depth d → weighted dim ≤ n^{2^d}
    Size s → depth O(log s) → weighted dim ≤ n^{poly(s)}

    For weighted dim = n!:
    n^{poly(s)} ≥ n! = n^{Θ(n)}

    So poly(s) ≥ Θ(n), meaning s ≥ n^{Ω(1)} = (log N)^{Ω(1)}

    This only gives POLYLOGARITHMIC bounds in N!
    """
    print("\n" + "=" * 60)
    print("TIGHTNESS ANALYSIS")
    print("=" * 60)

    for n in [4, 6, 8, 10, 20]:
        N = 2**n
        nfact = factorial(n)

        print(f"\nn = {n}, N = 2^{n} = {N}")
        print(f"n! = {nfact:.2e}")
        print(f"N^3 = {N**3:.2e}")
        print(f"n!/N^3 = {nfact / N**3:.2e}")

        # For weighted dim = n!, need n^{2^d} = n!, so 2^d = log_n(n!) ≈ n
        # So d ≈ log(n), formula size ≈ 2^{log n} = n
        critical_d = find_critical_depth(n)

        # The bound gives: size ≥ 2^d ≈ n
        # But we need: size ≥ N^{3+ε} = 2^{(3+ε)n}

        print(f"Bound gives: size ≥ ~{2**critical_d if critical_d else 'N/A'}")
        print(f"Need: size ≥ N^3 = {N**3:.2e}")
        print(f"GAP: {N**3 / (2**critical_d) if critical_d else 'N/A':.2e}")

# ============================================================
# Alternative: Counting Isotypic Components (Not Weighted)
# ============================================================

def component_count_analysis(n):
    """
    Alternative bound: count isotypic components touched, not weighted dimension.

    A formula of depth d can touch at most 2^{O(d)} components.
    (Each gate at most doubles the component count via Kronecker.)

    For depth O(log s): at most poly(s) components.

    To distinguish Gap-MCSP, need to touch ~p(n) components?
    Where p(n) = number of partitions ≈ exp(√n).

    This gives: poly(s) ≥ exp(√n), so s ≥ exp(√n)^{1/c} = exp(Ω(√n))

    For n = (log N)²: s ≥ exp(Ω(log N)) = N^{Ω(1)}

    Still only polynomial!
    """
    print("\n" + "=" * 60)
    print("COMPONENT COUNT ANALYSIS")
    print("=" * 60)

    for n in [4, 8, 16, 32]:
        num_parts = len(list(partitions(n)))
        N = 2**n

        print(f"\nn = {n}:")
        print(f"  Number of partitions p({n}) = {num_parts}")
        print(f"  N = 2^{n} = {N:.2e}")
        print(f"  N^3 = {N**3:.2e}")

        # If bound gives s ≥ p(n)^{1/c}:
        # For p(n) ≈ exp(π√(2n/3)):
        import math
        p_approx = math.exp(math.pi * math.sqrt(2*n/3))
        print(f"  p(n) ≈ exp(π√(2n/3)) ≈ {p_approx:.2e}")

        # s ≥ p(n)^{1/2} (if c=2)
        bound = p_approx ** 0.5
        print(f"  Component bound gives: size ≥ ~{bound:.2e}")
        print(f"  Need: size ≥ N^3 = {N**3:.2e}")

# ============================================================
# Main Analysis
# ============================================================

def main():
    print("KRONECKER COEFFICIENT ANALYSIS FOR FORMULA BOUNDS")
    print("=" * 60)

    for n in [3, 4, 5, 6]:
        print(f"\n{'='*60}")
        print(f"n = {n}")
        print(f"{'='*60}")
        weighted_dimension_product(n)

    analyze_bound_tightness()
    component_count_analysis(16)

    print("\n" + "=" * 60)
    print("CONCLUSION")
    print("=" * 60)
    print("""
The weighted dimension bound gives:
- Formula size s → weighted isotypic dimension ≤ n^{poly(s)}
- Gap-MCSP requires distinguishing weighted dimension ~n!
- This gives s ≥ n^{Ω(1)} = (log N)^{Ω(1)}

The component count bound gives:
- Formula size s → touches ≤ poly(s) components
- Gap-MCSP involves ~p(n) = exp(O(√n)) components
- This gives s ≥ exp(Ω(√n))

NEITHER bound gives N^{3+ε}!

The gap: These bounds measure the "reach" of formulas, but formulas
might be able to distinguish YES from NO without explicitly "reaching"
all the relevant isotypic structure.

We need a DIFFERENT type of bound - one that captures the inherent
difficulty of the Gap-MCSP decision problem, not just the complexity
of computing isotypic projections.
""")

if __name__ == "__main__":
    main()
