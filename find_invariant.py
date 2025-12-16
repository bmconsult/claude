#!/usr/bin/env python3
"""
Search for a novel Collatz invariant with bounded-step descent.

The idea: Find a potential function Φ(n) and bound K such that
for all n > 1: Φ(T^k(n)) < Φ(n) for some k ≤ K
"""

import math
from collections import defaultdict

def v2(n):
    """2-adic valuation: highest power of 2 dividing n"""
    if n == 0:
        return float('inf')
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k

def collatz_step(n):
    """Single Collatz step"""
    if n % 2 == 0:
        return n // 2
    else:
        return 3 * n + 1

def odd_to_odd(n):
    """Map from odd number to next odd number in Collatz sequence"""
    assert n % 2 == 1
    m = 3 * n + 1
    k = v2(m)
    return m // (2**k), k

def depth(n):
    """Depth function: d(n) = v₂(n+1) - 1 for odd n"""
    assert n % 2 == 1
    return v2(n + 1) - 1

# Test potential function 1: Φ(n) = n / w(n mod 8)
def phi1(n):
    """Weight based on n mod 8"""
    if n % 2 == 0:
        return n

    weights = {
        1: 4.0,   # n ≡ 1 (mod 8): v₂ ≥ 2, good
        3: 2.0,   # n ≡ 3 (mod 8): v₂ = 1, but next is good
        5: 4.0,   # n ≡ 5 (mod 8): v₂ ≥ 2, good
        7: 2.0,   # n ≡ 7 (mod 8): v₂ = 1, next is also problematic
    }
    return n / weights[n % 8]

def test_invariant(phi_func, max_n=1000, max_steps=20):
    """
    Test if invariant has bounded-step descent.
    Returns (success, max_k_needed, counterexamples)
    """
    max_k_needed = 0
    counterexamples = []

    for n in range(2, max_n):
        phi_n = phi_func(n)

        # Check if within max_steps, we find a decrease
        found_decrease = False
        m = n

        for k in range(1, max_steps + 1):
            m = collatz_step(m)
            phi_m = phi_func(m)

            if phi_m < phi_n:
                found_decrease = True
                max_k_needed = max(max_k_needed, k)
                break

        if not found_decrease:
            counterexamples.append(n)

    success = len(counterexamples) == 0
    return success, max_k_needed, counterexamples

# Test potential function 2: Two-step lookahead for odd numbers
def phi2(n):
    """
    For odd n: Φ(n) = min(n/2, g(n)/4) where g is odd-to-odd map
    For even n: Φ(n) = n
    """
    if n % 2 == 0:
        return n

    # Look ahead one step in odd-to-odd map
    g_n, k = odd_to_odd(n)

    # Weight based on expected next v₂
    if g_n % 4 == 1:
        # Next v₂ ≥ 2
        return n / 2.0
    else:
        # Next v₂ = 1, need to look further
        return n / 1.5

# Test potential function 3: Sophisticated multi-scale
def phi3(n):
    """
    Multi-scale potential combining value and modular structure.

    For odd n, we incorporate information about the next few steps.
    """
    if n % 2 == 0:
        return float(n)

    # Analyze n mod 16 to predict next 2-3 steps
    r = n % 16

    # Based on extensive analysis of the modular structure:
    # - n ≡ 1, 5, 9, 13 (mod 16): v₂(3n+1) ≥ 2, immediate decrease
    # - n ≡ 3, 11 (mod 16): v₂(3n+1) = 1, but g(n) ≡ 1 (mod 4), next is good
    # - n ≡ 7, 15 (mod 16): v₂(3n+1) = 1, and g(n) ≡ 3 (mod 4), problematic

    if r in [1, 5, 9, 13]:
        # Good case: next v₂ ≥ 2
        weight = 4.0
    elif r in [3, 11]:
        # Medium case: v₂ = 1 but recovery next step
        weight = 2.5
    else:  # r in [7, 15]
        # Bad case: v₂ = 1 and next also problematic
        weight = 1.8

    return n / weight

# Test potential function 4: Trajectory-based averaging
def phi4(n):
    """
    Φ(n) = weighted average of n and its next few odd values
    """
    if n % 2 == 0:
        return float(n)

    # Compute next few odd numbers in trajectory
    odds = [n]
    m = n
    for _ in range(3):  # Look 3 steps ahead in odd-to-odd
        m, k = odd_to_odd(m)
        odds.append(m)
        if m == 1:
            break

    # Weighted average with exponential decay
    weights = [1.0, 0.75, 0.5, 0.25]
    weighted_sum = sum(w * val for w, val in zip(weights, odds))
    weight_total = sum(weights[:len(odds)])

    return weighted_sum / weight_total


# Test potential function 5: LOG-BASED with modular correction
def phi5(n):
    """
    Φ(n) = log(n) + correction based on modular class

    The log gives rough scale, correction handles local behavior.
    """
    if n == 1:
        return 0.0

    if n % 2 == 0:
        return math.log(n)

    # Correction term based on mod 16
    r = n % 16
    corrections = {
        1: -0.3, 5: -0.3, 9: -0.3, 13: -0.3,  # Good cases
        3: -0.1, 11: -0.1,  # Medium cases
        7: 0.1, 15: 0.1,  # Bad cases
    }

    return math.log(n) + corrections[r]


if __name__ == "__main__":
    print("Testing novel Collatz invariants...")
    print("=" * 60)

    invariants = [
        ("Φ₁: Simple mod-8 weighting", phi1),
        ("Φ₂: Two-step lookahead", phi2),
        ("Φ₃: Multi-scale mod-16", phi3),
        ("Φ₄: Trajectory averaging", phi4),
        ("Φ₅: Log with modular correction", phi5),
    ]

    for name, phi_func in invariants:
        print(f"\n{name}")
        print("-" * 60)
        success, max_k, counterex = test_invariant(phi_func, max_n=10000, max_steps=50)

        if success:
            print(f"✓ SUCCESS! Bounded descent with k ≤ {max_k}")
        else:
            print(f"✗ FAILED. Found {len(counterex)} counterexamples")
            print(f"  First few: {counterex[:10]}")

    # Detailed analysis of why previous invariants failed
    print("\n" + "=" * 60)
    print("ANALYSIS: Why previous invariants failed")
    print("=" * 60)

    print("\nPrevious attempt: Φ(n) = n")
    print("Fails because 3n+1 > n for odd n")

    print("\nPrevious attempt: Φ(n) = log(n)")
    print("Fails because log(3n+1) > log(n) for odd n")

    print("\nPrevious attempt: Φ(n) = n · 4^parity")
    odd_spikes = []
    for n in range(1, 100, 2):
        g_n, k = odd_to_odd(n)
        if g_n > n:
            odd_spikes.append((n, g_n, k))

    print(f"Found {len(odd_spikes)} cases where g(n) > n in first 100 odds")
    print(f"Examples: {odd_spikes[:5]}")
