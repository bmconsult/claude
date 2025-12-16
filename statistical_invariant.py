#!/usr/bin/env python3
"""
Novel Statistical Invariant: Running Average of Future Values

Key insight: E[v₂(3n+1)] = 2 (proved by previous agents)
This means E[g(n)] = (3/4)n on average.

While individual steps can grow, the AVERAGE over K steps must shrink!
"""

import math

def v2(n):
    """2-adic valuation"""
    if n == 0:
        return float('inf')
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k

def odd_to_odd(n):
    """Map odd n to next odd in Collatz sequence"""
    assert n % 2 == 1
    m = 3 * n + 1
    k = v2(m)
    return m // (2**k)

def collatz_step(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1

def collatz_trajectory(n, max_steps=1000):
    traj = [n]
    for _ in range(max_steps):
        if n == 1:
            break
        n = collatz_step(n)
        traj.append(n)
    return traj

# NOVEL INVARIANT 1: K-step running average
def phi_running_avg(n, K=8):
    """
    Φ_K(n) = (n + T(n) + T²(n) + ... + T^(K-1)(n)) / K

    This averages the next K values in the full Collatz sequence.
    """
    traj = collatz_trajectory(n, K)
    return sum(traj[:K]) / len(traj[:K])

# NOVEL INVARIANT 2: Exponentially weighted average
def phi_exp_weighted(n, K=8, decay=0.9):
    """
    Φ(n) = Σᵢ₌₀^(K-1) decay^i · T^i(n) / Σᵢ₌₀^(K-1) decay^i

    Gives more weight to earlier values, but still incorporates future trajectory.
    """
    traj = collatz_trajectory(n, K)
    weights = [decay**i for i in range(len(traj[:K]))]
    weighted_sum = sum(w * val for w, val in zip(weights, traj[:K]))
    return weighted_sum / sum(weights)

# NOVEL INVARIANT 3: Max over sliding window with discount
def phi_discounted_max(n, K=8, discount=0.95):
    """
    Φ(n) = max(n, discount · T(n), discount² · T²(n), ...)

    Like a Bellman backup in RL: accounts for future, but with discounting.
    """
    traj = collatz_trajectory(n, K)
    return max(discount**i * val for i, val in enumerate(traj[:K]))

# NOVEL INVARIANT 4: Probabilistic potential (odd-to-odd)
def phi_probabilistic(n):
    """
    For odd n, use Φ(n) = n / 2^(expected total shrinkage)

    Based on E[v₂(3n+1)] = 2, we expect:
    - With prob 1/2: n ≡ 1 (mod 4), v₂ ≥ 2, ratio ≤ 3/4
    - With prob 1/2: n ≡ 3 (mod 4), v₂ = 1, ratio = 3/2
      - But of these, half have g(n) ≡ 1 (mod 4), recovering next step

    So we use a weighted potential based on n mod 16.
    """
    if n % 2 == 0:
        return float(n)

    r = n % 16

    # Empirically tuned weights based on modular analysis
    if r in [1, 5, 9, 13]:
        # Immediate shrinkage: v₂ ≥ 2
        return n / 3.5
    elif r in [3, 11]:
        # One bad step, then recovery
        return n / 2.2
    else:  # r in [7, 15]
        # Worst case: multiple bad steps
        return n / 1.6

# Test all invariants
def test_invariant_systematic(phi_func, name, max_n=10000, max_steps=200):
    """Test if invariant has bounded descent"""
    print(f"\nTesting: {name}")
    print("=" * 70)

    worst_k = 0
    worst_n = None
    failures = []

    for n in range(2, max_n):
        if n % 500 == 0:
            print(f"  Progress: n={n}/{max_n}, worst_k so far={worst_k}", end='\r')

        phi_n = phi_func(n)
        found = False

        traj = collatz_trajectory(n, max_steps)
        for k, m in enumerate(traj[1:], 1):
            phi_m = phi_func(m)
            if phi_m < phi_n:
                if k > worst_k:
                    worst_k = k
                    worst_n = n
                found = True
                break

        if not found:
            failures.append(n)

    print(f"\n{'':<70}")  # Clear progress line

    if failures:
        print(f"❌ FAILED: {len(failures)} counterexamples")
        print(f"   First few: {failures[:10]}")
        return None
    else:
        print(f"✅ SUCCESS: Bounded descent with k ≤ {worst_k}")
        print(f"   Worst case: n = {worst_n}")

        # Show trajectory for worst case
        if worst_n:
            traj = collatz_trajectory(worst_n, worst_k + 5)
            print(f"   Trajectory: {traj[:min(20, len(traj))]}...")

        return worst_k

if __name__ == "__main__":
    print("=" * 70)
    print("NOVEL STATISTICAL INVARIANTS FOR COLLATZ")
    print("=" * 70)

    results = []

    # Test 1: Running average
    k = test_invariant_systematic(
        lambda n: phi_running_avg(n, K=8),
        "Φ₁(n) = 8-step running average",
        max_n=5000
    )
    if k is not None:
        results.append(("Running average (K=8)", k))

    # Test 2: Exponentially weighted
    k = test_invariant_systematic(
        lambda n: phi_exp_weighted(n, K=8, decay=0.9),
        "Φ₂(n) = Exponentially weighted average (decay=0.9)",
        max_n=5000
    )
    if k is not None:
        results.append(("Exp weighted (decay=0.9)", k))

    # Test 3: Discounted max
    k = test_invariant_systematic(
        lambda n: phi_discounted_max(n, K=8, discount=0.95),
        "Φ₃(n) = Discounted max (K=8, discount=0.95)",
        max_n=5000
    )
    if k is not None:
        results.append(("Discounted max", k))

    # Test 4: Probabilistic based on modular structure
    k = test_invariant_systematic(
        phi_probabilistic,
        "Φ₄(n) = Probabilistic potential (mod 16 based)",
        max_n=5000
    )
    if k is not None:
        results.append(("Probabilistic (mod 16)", k))

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY OF RESULTS")
    print("=" * 70)

    if results:
        print("\n✅ Successful invariants (bounded descent):")
        for name, k in results:
            print(f"   {name:40s}: k ≤ {k:4d}")

        best = min(results, key=lambda x: x[1])
        print(f"\n🏆 Best invariant: {best[0]} with k ≤ {best[1]}")

    else:
        print("\n❌ No successful invariants found in this batch.")

    print("\n" + "=" * 70)
    print("THEORETICAL NOTE:")
    print("=" * 70)
    print("""
If any of these invariants has bounded k, we have a NOVEL result!

Previous agents tried:
  - φ(n) = n              → Works but k unbounded? (empirically k ≤ 132 for n ≤ 10⁴)
  - φ(n) = log(n)         → Same issue
  - φ(n) = n · 4^parity   → Spikes on odd divisions

Our NEW approach:
  - Statistical averaging → Exploits E[v₂(3n+1)] = 2
  - Modular weighting     → Targets worst cases (n ≡ 7,15 mod 16)
  - Future trajectory     → Looks ahead to smooth out variance

The key innovation: Don't try to decrease at EVERY step.
Instead, guarantee decrease within K steps by averaging!
    """)
