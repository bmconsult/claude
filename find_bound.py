#!/usr/bin/env python3
"""
Find if there's a bounded k such that φ(T^k(n)) < φ(n) for ALL n.
This would solve the key requirement!
"""

import sys

def collatz_trajectory(n, max_steps=10000):
    """Generate Collatz trajectory"""
    traj = [n]
    for _ in range(max_steps):
        if n == 1:
            break
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        traj.append(n)
        if len(traj) > max_steps:
            break
    return traj

def steps_until_decrease(n, phi_func, max_steps=10000):
    """
    Find minimum k such that φ(T^k(n)) < φ(n).
    Returns k, or None if no decrease within max_steps.
    """
    phi_n = phi_func(n)
    traj = collatz_trajectory(n, max_steps)

    for k, m in enumerate(traj[1:], 1):
        if phi_func(m) < phi_n:
            return k

    return None  # No decrease found

# Test phi(n) = n
print("=" * 70)
print("FINDING UNIVERSAL BOUND for φ(n) = n")
print("=" * 70)
print("\nSearching for worst cases up to n=10,000...")
print(f"{'n':>8} | {'Steps to decrease (k)':>20} | {'Peak value':>12}")
print("-" * 70)

worst_cases = []
for n in range(2, 10001):
    k = steps_until_decrease(n, lambda x: float(x), max_steps=10000)

    if k is None:
        print(f"{n:>8} | {'NO DECREASE!':>20} | {'???':>12}")
        sys.exit(1)

    if k > 50:  # Report cases needing many steps
        traj = collatz_trajectory(n, k + 1)
        peak = max(traj[:k+1])
        print(f"{n:>8} | {k:>20} | {peak:>12}")
        worst_cases.append((n, k, peak))

# Summary
print("\n" + "=" * 70)
print("SUMMARY:")
print("=" * 70)

if worst_cases:
    worst_cases.sort(key=lambda x: x[1], reverse=True)
    print(f"\nTop 10 worst cases (by steps to decrease):")
    for i, (n, k, peak) in enumerate(worst_cases[:10], 1):
        print(f"  {i:2d}. n={n:>6} needs k={k:>4} steps (reaches peak={peak:>8})")

    max_k = worst_cases[0][1]
    print(f"\n**MAXIMUM k found (up to n=10,000): k = {max_k}**")

    # Check if there's a pattern
    print(f"\nPattern analysis of worst cases:")
    for n, k, peak in worst_cases[:10]:
        print(f"  n={n:>6}: n mod 8 = {n % 8}, n mod 16 = {n % 16:2d}")

else:
    print("All numbers decrease quickly (k ≤ 50)")

# Now the key question: does k grow with n, or is it bounded?
print("\n" + "=" * 70)
print("TESTING: Does k grow unboundedly with n?")
print("=" * 70)

# Sample larger values
test_values = [10000, 25000, 50000, 100000, 250000, 500000, 1000000]
print(f"\n{'n':>10} | {'k (steps to decrease)':>25}")
print("-" * 70)

for n in test_values:
    k = steps_until_decrease(n, lambda x: float(x), max_steps=10000)
    if k is None:
        print(f"{n:>10} | {'NO DECREASE in 10000 steps!':>25}")
    else:
        print(f"{n:>10} | {k:>25}")

print("\n" + "=" * 70)
print("CONCLUSION:")
print("=" * 70)
print("""
If k remains bounded even for large n, then we have found the invariant:

    φ(n) = n

with bounded-step descent: φ(T^k(n)) < φ(n) for some k ≤ K.

But this would essentially BE a proof of the Collatz conjecture!

The question is: can we PROVE k is bounded, or does it grow with n?
""")
