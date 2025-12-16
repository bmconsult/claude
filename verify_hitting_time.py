#!/usr/bin/env python3
"""
Verification script for the Hitting Time Theorem.

Tests that every odd number eventually hits n ≡ 1 (mod 4) under the Collatz map.
"""

def v2(n):
    """Compute 2-adic valuation of n."""
    if n == 0:
        return float('inf')
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count

def collatz_next_odd(n):
    """Apply Collatz map to odd n, return next odd number."""
    assert n % 2 == 1
    val = v2(3*n + 1)
    return (3*n + 1) // (2**val)

def hits_one_mod_four(n, max_steps=1000):
    """Check if trajectory hits n ≡ 1 (mod 4) within max_steps."""
    if n % 4 == 1:
        return True, 0

    for step in range(1, max_steps + 1):
        n = collatz_next_odd(n)
        if n % 4 == 1:
            return True, step

    return False, max_steps

def verify_residue_class_formula(k):
    """
    Verify that n ≡ 2^k - 1 (mod 2^{k+1}) maps to T(n) ≡ 2^{k-1} - 1 (mod 2^{k-1}).
    """
    mod_input = 2**k - 1
    mod_check = 2**(k+1)
    expected_output_mod = 2**(k-1) - 1
    expected_output_check = 2**(k-1)

    # Test several representatives of the residue class
    results = []
    for m in range(10):
        n = mod_input + mod_check * m
        if n % 4 != 3:  # Skip if not ≡ 3 (mod 4)
            continue

        t_n = collatz_next_odd(n)
        actual_residue = t_n % expected_output_check

        results.append({
            'n': n,
            'm': m,
            'T(n)': t_n,
            'T(n) mod 2^{k-1}': actual_residue,
            'expected': expected_output_mod,
            'match': actual_residue == expected_output_mod
        })

    return results

def verify_escape_times():
    """Verify that different residue classes escape in expected number of steps."""
    test_cases = [
        (3, 8, 1, "n ≡ 3 (mod 8)"),
        (7, 16, 2, "n ≡ 7 (mod 16)"),
        (15, 32, 3, "n ≡ 15 (mod 32)"),
        (31, 64, 4, "n ≡ 31 (mod 64)"),
        (63, 128, 5, "n ≡ 63 (mod 128)"),
    ]

    print("=" * 70)
    print("ESCAPE TIME VERIFICATION")
    print("=" * 70)

    for residue, modulus, expected_max_steps, description in test_cases:
        print(f"\n{description}:")
        print(f"  Residue: {residue} (mod {modulus})")

        # Test several representatives
        max_observed = 0
        for m in range(20):
            n = residue + modulus * m
            if n % 4 != 3:
                continue

            hit, steps = hits_one_mod_four(n)
            if not hit:
                print(f"    n={n}: FAILED to hit ≡ 1 (mod 4) in 1000 steps!")
                continue

            max_observed = max(max_observed, steps)

            if steps <= expected_max_steps:
                status = "✓"
            else:
                status = "✗"

            if m < 5:  # Print first few
                print(f"    n={n:6d}: hits in {steps} steps {status}")

        print(f"  Maximum steps observed: {max_observed}")
        print(f"  Expected maximum: ≤ {expected_max_steps}")
        if max_observed <= expected_max_steps:
            print("  PASS ✓")
        else:
            print("  FAIL ✗")

def test_formula_verification():
    """Test Claim 1: the residue class reduction formula."""
    print("\n" + "=" * 70)
    print("CLAIM 1 VERIFICATION: T(n ≡ 2^k-1 (mod 2^{k+1})) ≡ 2^{k-1}-1 (mod 2^{k-1})")
    print("=" * 70)

    for k in range(3, 10):
        print(f"\nk = {k}:")
        results = verify_residue_class_formula(k)

        if not results:
            print("  No valid test cases (all n ≢ 3 (mod 4))")
            continue

        all_match = all(r['match'] for r in results)

        for r in results[:5]:  # Print first few
            status = "✓" if r['match'] else "✗"
            print(f"  n={r['n']:6d}, T(n)={r['T(n)']:6d}, " +
                  f"T(n) mod 2^{k-1} = {r['T(n) mod 2^{k-1}']:4d}, " +
                  f"expected {r['expected']:4d} {status}")

        if len(results) > 5:
            print(f"  ... ({len(results)-5} more cases)")

        if all_match:
            print(f"  PASS ✓ (all {len(results)} cases match)")
        else:
            print(f"  FAIL ✗")

def comprehensive_test(max_n=10000):
    """Test that all odd n < max_n eventually hit ≡ 1 (mod 4)."""
    print("\n" + "=" * 70)
    print(f"COMPREHENSIVE TEST: All odd n < {max_n} hit ≡ 1 (mod 4)")
    print("=" * 70)

    failures = []
    max_steps_seen = 0

    for n in range(3, max_n, 2):  # All odd numbers
        hit, steps = hits_one_mod_four(n, max_steps=10000)
        if not hit:
            failures.append(n)
        else:
            max_steps_seen = max(max_steps_seen, steps)

    print(f"\nTested {(max_n-3)//2 + 1} odd numbers from 3 to {max_n-1}")
    print(f"Maximum steps to hit ≡ 1 (mod 4): {max_steps_seen}")

    if failures:
        print(f"\nFAILURES: {len(failures)} numbers did not hit ≡ 1 (mod 4) in 10000 steps")
        print(f"First few failures: {failures[:10]}")
    else:
        print("\nPASS ✓ - All numbers hit ≡ 1 (mod 4)")

if __name__ == "__main__":
    print("HITTING TIME THEOREM - NUMERICAL VERIFICATION")
    print("=" * 70)

    test_formula_verification()
    verify_escape_times()
    comprehensive_test(max_n=10000)

    print("\n" + "=" * 70)
    print("VERIFICATION COMPLETE")
    print("=" * 70)
