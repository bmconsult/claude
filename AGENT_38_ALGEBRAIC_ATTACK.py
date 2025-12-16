#!/usr/bin/env python3
"""
Agent 38: Proof Breaker - Algebraic Attack
Verify the key reduction formula by direct computation
"""

def S(n):
    """Syracuse map: next odd number in Collatz sequence"""
    val = 3*n + 1
    # Divide out all factors of 2
    while val % 2 == 0:
        val //= 2
    return val

def verify_reduction_formula(k):
    """
    Verify: If n ≡ 2^(k+1)-1 (mod 2^(k+2)), then S(n) ≡ 2^k-1 (mod 2^(k+1))
    """
    print(f"\n{'='*60}")
    print(f"TESTING k={k}")
    print(f"{'='*60}")

    target_residue = 2**(k+1) - 1
    target_modulus = 2**(k+2)
    expected_S_residue = 2**k - 1
    expected_S_modulus = 2**(k+1)

    print(f"Formula claim: n ≡ {target_residue} (mod {target_modulus}) => S(n) ≡ {expected_S_residue} (mod {expected_S_modulus})")

    # Test first 10 values in this residue class
    failures = []
    successes = []

    for m in range(10):
        n = m * target_modulus + target_residue
        if n % 2 == 0:  # Skip even (we need odd)
            continue

        S_n = S(n)
        actual_residue = S_n % expected_S_modulus

        if actual_residue == expected_S_residue:
            successes.append((n, S_n, actual_residue))
        else:
            failures.append((n, S_n, actual_residue))

    print(f"\nSuccesses: {len(successes)}")
    for n, S_n, res in successes[:5]:  # Show first 5
        print(f"  n={n}: S({n})={S_n}, S(n) mod {expected_S_modulus} = {res} ✓")

    if failures:
        print(f"\nFAILURES: {len(failures)}")
        for n, S_n, res in failures:
            print(f"  n={n}: S({n})={S_n}, S(n) mod {expected_S_modulus} = {res} ✗ (expected {expected_S_residue})")
        return False
    else:
        print(f"\n✓ ALL TESTS PASSED for k={k}")
        return True

# Test k=3,4,5 as requested
print("ALGEBRAIC ATTACK: Verifying key reduction formula")
print("="*60)

results = {}
for k in [3, 4, 5]:
    results[k] = verify_reduction_formula(k)

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
for k, passed in results.items():
    status = "✓ PASSED" if passed else "✗ FAILED"
    print(f"k={k}: {status}")

if all(results.values()):
    print("\n✓ ALGEBRAIC ATTACK FAILED - Formula is correct!")
else:
    print("\n✗ PROOF BROKEN - Formula has errors!")
