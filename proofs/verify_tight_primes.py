#!/usr/bin/env python3
"""
Computational verification of tight prime existence for Collatz conjecture.

Tests multiple possible definitions to identify the correct one and verify
existence for m up to 10,000 or more.
"""

import math
from typing import List, Tuple, Optional


def is_prime(n: int) -> bool:
    """Check if n is prime using trial division."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def sieve_of_eratosthenes(limit: int) -> List[int]:
    """Generate all primes up to limit using Sieve of Eratosthenes."""
    if limit < 2:
        return []

    is_prime_arr = [True] * (limit + 1)
    is_prime_arr[0] = is_prime_arr[1] = False

    for i in range(2, int(math.sqrt(limit)) + 1):
        if is_prime_arr[i]:
            for j in range(i*i, limit + 1, i):
                is_prime_arr[j] = False

    return [i for i in range(limit + 1) if is_prime_arr[i]]


def multiplicative_order(a: int, p: int) -> int:
    """
    Compute the multiplicative order of a modulo p.
    Returns smallest k > 0 such that a^k ≡ 1 (mod p).
    Assumes gcd(a, p) = 1.
    """
    if math.gcd(a, p) != 1:
        return -1

    k = 1
    current = a % p
    while current != 1:
        current = (current * a) % p
        k += 1
        if k > p:  # Safety check
            return -1
    return k


def find_tight_prime_def1(m: int, primes: List[int]) -> Optional[int]:
    """
    Definition 1: A prime p is m-tight if p > m and there exists k, d with:
    - 1 ≤ d ≤ m
    - d < k ≤ 2m
    - 2^k ≡ 3^d (mod p)
    - p ∤ (3^d - 1)

    Returns the smallest such prime, or None if not found in prime list.
    """
    for p in primes:
        if p <= m:
            continue
        if p > 10 * m:  # Don't search too far
            break

        # Check if there exist k, d with the required properties
        for d in range(1, m + 1):
            # Check p ∤ (3^d - 1)
            if pow(3, d, p) == 1:
                continue

            target = pow(3, d, p)

            for k in range(d + 1, 2 * m + 1):
                if pow(2, k, p) == target:
                    return p

    return None


def find_tight_prime_def2(m: int, primes: List[int]) -> Optional[int]:
    """
    Definition 2: A prime p is m-tight if p is in (m, f(m)) for some function f,
    and ord_p(2) or ord_p(3) has specific properties related to m.

    Here we test: p in (m, 2m) and ord_p(2/3) divides something related to m.
    """
    for p in primes:
        if p <= m or p >= 2 * m:
            continue

        # Check if 2 and 3 have "good" orders modulo p
        ord2 = multiplicative_order(2, p)
        ord3 = multiplicative_order(3, p)

        if ord2 == -1 or ord3 == -1:
            continue

        # Various conditions we might want:
        # 1. ord_p(2) > m and ord_p(3) > m
        if ord2 > m and ord3 > m:
            return p

    return None


def find_tight_prime_def3(m: int, primes: List[int]) -> Optional[int]:
    """
    Definition 3: A prime p is m-tight if:
    - p > m
    - p divides 2^k - 3^d for some specific k, d related to m
    - This creates a cycle-breaking contradiction

    Test: p divides 2^k - 3^d where k ≈ d * log_2(3) (balanced case)
    """
    # For cycle length m, the balanced case is when growth from *3 and shrink from /2 balance
    # log_2(3) ≈ 1.585

    for p in primes:
        if p <= m:
            continue
        if p > 10 * m:
            break

        # Check if p divides 2^k - 3^d for k, d related to m
        for d in range(1, m + 1):
            k = round(d * math.log(3) / math.log(2))
            if k < 1:
                k = 1

            val = (pow(2, k, p) - pow(3, d, p)) % p
            if val == 0:
                # p divides 2^k - 3^d
                return p

    return None


def find_tight_prime_def4(m: int, primes: List[int]) -> Optional[int]:
    """
    Definition 4: Simple version - just any prime in (m, 2m).
    This is to test Bertrand's postulate baseline.
    """
    for p in primes:
        if m < p < 2 * m:
            return p
    return None


def find_tight_prime_def5(m: int, primes: List[int]) -> Optional[int]:
    """
    Definition 5: A prime p is m-tight if:
    - p > 2m (strictly larger than Bertrand range)
    - There exists d ≤ m such that ord_p(3) = d or ord_p(2) divides k for some cycle-relevant k
    """
    for p in primes:
        if p <= 2 * m:
            continue
        if p > 10 * m:
            break

        ord3 = multiplicative_order(3, p)
        if ord3 <= m:
            # Order of 3 is at most m - this might create tight constraints
            return p

    return None


def verify_all_definitions(max_m: int = 10000):
    """
    Verify existence of tight primes for all definitions up to max_m.
    """
    print(f"Generating primes up to {max_m * 20}...")
    primes = sieve_of_eratosthenes(max_m * 20)
    print(f"Generated {len(primes)} primes\n")

    definitions = [
        ("Def1: Modular k,d conditions", find_tight_prime_def1),
        ("Def2: Order conditions", find_tight_prime_def2),
        ("Def3: Balanced 2^k - 3^d", find_tight_prime_def3),
        ("Def4: Bertrand (m, 2m)", find_tight_prime_def4),
        ("Def5: Large p, small ord", find_tight_prime_def5),
    ]

    # Test small values first to see which definition makes sense
    print("Testing small values m = 1 to 20:")
    print("=" * 80)

    for m in range(1, 21):
        print(f"\nm = {m}:")
        for name, func in definitions:
            result = func(m, primes)
            if result:
                print(f"  {name}: p = {result}")
            else:
                print(f"  {name}: NOT FOUND (might need more primes or different range)")

    # Now test larger range and count failures
    print("\n" + "=" * 80)
    print(f"\nTesting m = 1 to {max_m}...")
    print("=" * 80)

    for name, func in definitions:
        failures = []
        for m in range(1, max_m + 1):
            result = func(m, primes)
            if result is None:
                failures.append(m)

            if m % 1000 == 0:
                print(f"{name}: Tested up to m = {m}, failures so far: {len(failures)}")

        print(f"\n{name}:")
        print(f"  Total failures: {len(failures)} / {max_m}")
        if failures and len(failures) <= 20:
            print(f"  Failed for m = {failures}")
        elif failures:
            print(f"  First failures: {failures[:20]}...")
            print(f"  Last failures: {failures[-10:]}")
        print()


def analyze_specific_cases():
    """
    Analyze specific small cases in detail to understand the structure.
    """
    print("Detailed analysis for m = 3, 5, 7:")
    print("=" * 80)

    primes = sieve_of_eratosthenes(10000)

    for m in [3, 5, 7]:
        print(f"\n--- m = {m} ---")
        relevant_primes = [p for p in primes if m < p < 10 * m]

        print(f"Primes in ({m}, {10*m}): {relevant_primes[:20]}...")

        for p in relevant_primes[:10]:
            print(f"\n  p = {p}:")
            print(f"    ord_p(2) = {multiplicative_order(2, p)}")
            print(f"    ord_p(3) = {multiplicative_order(3, p)}")

            # Check for solutions to 2^k ≡ 3^d (mod p)
            solutions = []
            for d in range(1, m + 1):
                target = pow(3, d, p)
                for k in range(d + 1, 2 * m + 1):
                    if pow(2, k, p) == target:
                        solutions.append((k, d))

            if solutions:
                print(f"    Solutions to 2^k ≡ 3^d (mod p): {solutions}")


def main():
    print("=" * 80)
    print("TIGHT PRIME EXISTENCE VERIFICATION")
    print("=" * 80)
    print()

    # First, detailed analysis of small cases
    analyze_specific_cases()

    print("\n" + "=" * 80)
    print()

    # Then verify all definitions
    verify_all_definitions(max_m=1000)  # Start with 1000, can increase

    print("\n" + "=" * 80)
    print("VERIFICATION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
