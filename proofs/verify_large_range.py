#!/usr/bin/env python3
"""
Extended verification of Definition 1 for tight primes up to m = 100,000.
Also analyzes patterns to inform the proof strategy.
"""

import math
from typing import List, Optional, Tuple


def sieve_of_eratosthenes(limit: int) -> List[int]:
    """Generate all primes up to limit."""
    if limit < 2:
        return []
    is_prime_arr = [True] * (limit + 1)
    is_prime_arr[0] = is_prime_arr[1] = False
    for i in range(2, int(math.sqrt(limit)) + 1):
        if is_prime_arr[i]:
            for j in range(i*i, limit + 1, i):
                is_prime_arr[j] = False
    return [i for i in range(limit + 1) if is_prime_arr[i]]


def find_tight_prime_def1_with_witness(m: int, primes: List[int]) -> Optional[Tuple[int, int, int]]:
    """
    Definition 1: A prime p is m-tight if p > m and there exists k, d with:
    - 1 ≤ d ≤ m
    - d < k ≤ 2m
    - 2^k ≡ 3^d (mod p)
    - p ∤ (3^d - 1)

    Returns (p, k, d) witness, or None if not found.
    """
    for p in primes:
        if p <= m:
            continue
        if p > 10 * m:  # Search bound
            break

        for d in range(1, m + 1):
            # Check p ∤ (3^d - 1)
            if pow(3, d, p) == 1:
                continue

            target = pow(3, d, p)

            for k in range(d + 1, 2 * m + 1):
                if pow(2, k, p) == target:
                    return (p, k, d)

    return None


def analyze_prime_patterns(max_m: int = 10000):
    """
    Analyze patterns in tight prime values.
    """
    print(f"Generating primes up to {max_m * 20}...")
    primes = sieve_of_eratosthenes(max_m * 20)
    print(f"Generated {len(primes)} primes\n")

    # Track statistics
    prime_values = []
    prime_ratios = []  # ratio p/m

    failures = []

    print(f"Testing m = 1 to {max_m}...")
    for m in range(1, max_m + 1):
        result = find_tight_prime_def1_with_witness(m, primes)

        if result is None:
            failures.append(m)
        else:
            p, k, d = result
            prime_values.append(p)
            prime_ratios.append(p / m)

        if m % 10000 == 0:
            print(f"  Progress: m = {m}, failures = {len(failures)}")

    print(f"\n{'='*80}")
    print("RESULTS:")
    print(f"{'='*80}")
    print(f"Total tested: {max_m}")
    print(f"Failures: {len(failures)}")
    if failures:
        print(f"Failed at: {failures}")
    else:
        print("SUCCESS: Tight primes found for ALL m in range!")

    if prime_values:
        print(f"\nStatistics on p/m ratio:")
        print(f"  Min: {min(prime_ratios):.4f}")
        print(f"  Max: {max(prime_ratios):.4f}")
        print(f"  Mean: {sum(prime_ratios)/len(prime_ratios):.4f}")

        # Check if p/m is bounded
        print(f"\nBounding analysis:")
        print(f"  Max p found: {max(prime_values)}")
        print(f"  For m = {max_m}, max p/m = {max(prime_ratios):.4f}")

    # Sample some cases to show witnesses
    print(f"\n{'='*80}")
    print("Sample witnesses (m, p, k, d):")
    print(f"{'='*80}")

    sample_m_values = [10, 100, 1000, 5000, 10000] if max_m >= 10000 else list(range(10, min(max_m, 100), 10))

    for m in sample_m_values:
        if m > max_m:
            continue
        result = find_tight_prime_def1_with_witness(m, primes)
        if result:
            p, k, d = result
            print(f"m = {m:6d}: p = {p:6d} (ratio {p/m:6.3f}), k = {k:6d}, d = {d:6d}")
            # Verify the condition
            check = (pow(2, k, p) - pow(3, d, p)) % p
            assert check == 0, f"Verification failed for m={m}"


def verify_smallest_tight_primes(max_m: int = 1000):
    """
    Find the smallest tight prime for each m.
    Check if there's a pattern or bound.
    """
    print(f"Finding SMALLEST tight prime for each m up to {max_m}...")

    primes = sieve_of_eratosthenes(max_m * 100)

    results = []

    for m in range(1, max_m + 1):
        # Find smallest p
        smallest_p = None
        for p in primes:
            if p <= m:
                continue

            found = False
            for d in range(1, m + 1):
                if pow(3, d, p) == 1:
                    continue

                target = pow(3, d, p)
                for k in range(d + 1, 2 * m + 1):
                    if pow(2, k, p) == target:
                        smallest_p = p
                        found = True
                        break
                if found:
                    break
            if found:
                break

        if smallest_p:
            results.append((m, smallest_p, smallest_p / m))

        if m % 100 == 0:
            print(f"  Progress: m = {m}")

    print(f"\n{'='*80}")
    print("SMALLEST tight primes:")
    print(f"{'='*80}")

    print(f"\nSample results:")
    for i in [0, 10, 50, 100, 500, min(999, len(results)-1)]:
        if i < len(results):
            m, p, ratio = results[i]
            print(f"  m = {m:5d}: smallest p = {p:5d}, ratio = {ratio:.4f}")

    if results:
        max_ratio = max(r[2] for r in results)
        print(f"\nMax ratio (smallest p)/m = {max_ratio:.4f}")

        # Find the bound
        max_ratio_m = max(results, key=lambda x: x[2])
        print(f"Achieved at m = {max_ratio_m[0]}, p = {max_ratio_m[1]}")


def main():
    print("="*80)
    print("EXTENDED TIGHT PRIME VERIFICATION - DEFINITION 1")
    print("="*80)
    print()

    # First verify up to 10,000
    analyze_prime_patterns(max_m=10000)

    print("\n" + "="*80)
    print()

    # Find smallest tight primes
    verify_smallest_tight_primes(max_m=1000)

    print("\n" + "="*80)
    print("VERIFICATION COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()
