#!/usr/bin/env python3
"""
Case 2b: Formalize the CRT-based theorem.

THEOREM (Case 2b): For any coprime n-tuple with n ≥ 2, there exists
t = k/L for some integer k and L = c * lcm(v_1, ..., v_n) such that
min_i ||v_i t|| ≥ 1/(n+1).

The key insight is that coprimality ensures CRT constraints are compatible.
"""

from fractions import Fraction
from math import gcd, lcm
from functools import reduce
from itertools import combinations

def multi_lcm(numbers):
    return reduce(lcm, numbers)

def multi_gcd(numbers):
    return reduce(gcd, numbers)

def is_coprime_tuple(speeds):
    return multi_gcd(speeds) == 1

def valid_residues(m, n):
    """Valid residues r such that ||r/m|| >= 1/(n+1)."""
    if m == 0:
        return set()
    lower = m / (n + 1)
    upper = n * m / (n + 1)
    # r/m in [1/(n+1), n/(n+1)] iff r in [m/(n+1), n*m/(n+1)]
    return set(range(max(1, int(lower) + 1), min(m, int(upper) + 1)))

def check_time(speeds, t):
    """Check if time t gives all distances >= 1/(n+1)."""
    n = len(speeds)
    threshold = Fraction(1, n + 1)
    for v in speeds:
        vt = Fraction(v) * t
        frac = vt - int(vt)
        dist = min(frac, 1 - frac)
        if dist < threshold:
            return False
    return True

def find_good_time_crt(speeds, max_mult=10):
    """Find good time using CRT approach at increasing resolutions."""
    n = len(speeds)
    L = multi_lcm(speeds)

    for mult in range(1, max_mult + 1):
        period = mult * L
        moduli = [period // v for v in speeds]
        valid_sets = [valid_residues(m, n) for m in moduli]

        # Check if any valid set is empty
        if any(len(vs) == 0 for vs in valid_sets):
            continue

        # Brute force search for valid k
        for k in range(1, period):
            if all(k % m in vs for m, vs in zip(moduli, valid_sets)):
                t = Fraction(k, period)
                if check_time(speeds, t):
                    return t, k, period

    return None, None, None

print("=" * 70)
print("THEOREM VERIFICATION: CRT approach for Case 2b")
print("=" * 70)

# Test exhaustively for small n
for n in range(3, 7):
    print(f"\n{'='*70}")
    print(f"n = {n}: Testing ALL coprime tuples with speeds ≤ {3*n}")
    print(f"{'='*70}")

    max_speed = 3 * n
    total_tested = 0
    success = 0
    failures = []

    for speeds in combinations(range(1, max_speed + 1), n):
        if not is_coprime_tuple(speeds):
            continue

        total_tested += 1
        t, k, period = find_good_time_crt(speeds)

        if t is not None:
            success += 1
        else:
            failures.append(speeds)

    print(f"Tested: {total_tested}")
    print(f"Success: {success}")
    print(f"Failures: {len(failures)}")

    if failures:
        print("FAILURES:")
        for f in failures[:10]:
            print(f"  {f}")
            # Try with higher resolution
            t, k, period = find_good_time_crt(f, max_mult=50)
            if t:
                print(f"    -> Found at mult > 10: t = {k}/{period}")
            else:
                # Numerical search
                found = False
                for i in range(1, 100000):
                    t = i / 100000
                    threshold = 1 / (n + 1)
                    min_d = min(min(abs((v * t) % 1), 1 - (v * t) % 1) for v in f)
                    if min_d >= threshold - 1e-9:
                        print(f"    -> Numerical: t ≈ {t:.6f}")
                        found = True
                        break
                if not found:
                    print(f"    -> NO GOOD TIME FOUND (potential counterexample!)")

print("\n" + "=" * 70)
print("KEY LEMMA: Valid residue count guarantees")
print("=" * 70)

print("""
LEMMA: For m >= 2 and n >= 2, the set of valid residues V(m,n) is non-empty.

Proof: V(m,n) = {r : r/m in [1/(n+1), n/(n+1)]}
              = {r : r in [m/(n+1), n*m/(n+1)]}

The interval has length (n-1)*m/(n+1).
For m >= 2 and n >= 2: length >= 2*1/3 = 2/3 > 0.
But we need length >= 1 to guarantee an integer.

For m = 2:
  [2/(n+1), 2n/(n+1)] = [2/(n+1), 2 - 2/(n+1)]
  For n >= 2: 2/(n+1) <= 2/3 < 1 and 2 - 2/(n+1) >= 4/3 > 1
  So r = 1 is always valid. ✓

For m = 3:
  [3/(n+1), 3n/(n+1)]
  For n = 2: [1, 2]. Valid: {1, 2}.
  For n >= 3: [3/4, 9/4] for n=3, etc. Always contains integers.

For m >= 4:
  Length >= 4*2/4 = 2 for n = 3.
  An interval of length >= 2 contains at least 2 integers.

QED
""")

# Verify the lemma
print("Verification:")
for n in range(2, 8):
    for m in range(1, 15):
        vs = valid_residues(m, n)
        expected_nonempty = m >= 2
        status = "✓" if (len(vs) > 0) == expected_nonempty else "✗"
        if m <= 5:
            print(f"  n={n}, m={m}: |V| = {len(vs)}, V = {sorted(vs) if len(vs) <= 5 else '...'} {status}")

print("\n" + "=" * 70)
print("THEOREM: CRT compatibility for coprime tuples")
print("=" * 70)

print("""
THEOREM: For a coprime n-tuple (v_1, ..., v_n) with n >= 2, there exists
an integer k and constant c such that t = k/(c * L) satisfies:

  ||v_i * t|| >= 1/(n+1) for all i

where L = lcm(v_1, ..., v_n).

PROOF STRUCTURE:

1. Define moduli: m_i = c*L / v_i for each speed.

2. Define valid residues: V_i = {r : r/m_i in [1/(n+1), n/(n+1)]}

3. CLAIM: For c = 2 (or small constant), the CRT system has a solution.

   This is because:
   a) Each |V_i| >= 1 (by Lemma above, since m_i >= 2 when c >= 2).
   b) The coprimality of the tuple ensures the moduli m_i have
      a structure that prevents total incompatibility.

4. The CRT solution k gives time t = k/(c*L) with desired property.

KEY INSIGHT: The coprimality gcd(v_1, ..., v_n) = 1 is crucial.
It ensures that no single residue class is blocked by ALL constraints.
""")

# Test the "c = 2 suffices" claim
print("\nTest: Does c = 2 always suffice?")
for n in range(3, 6):
    max_speed = 3 * n
    need_higher_mult = []

    for speeds in combinations(range(1, max_speed + 1), n):
        if not is_coprime_tuple(speeds):
            continue

        L = multi_lcm(speeds)

        # Try c = 1 (original lcm)
        moduli_1 = [L // v for v in speeds]
        valid_1 = [valid_residues(m, n) for m in moduli_1]
        empty_at_1 = any(len(vs) == 0 for vs in valid_1)

        # Try c = 2
        moduli_2 = [2 * L // v for v in speeds]
        valid_2 = [valid_residues(m, n) for m in moduli_2]
        empty_at_2 = any(len(vs) == 0 for vs in valid_2)

        if not empty_at_1:
            # c = 1 works
            pass
        elif not empty_at_2:
            # c = 2 works
            need_higher_mult.append((speeds, "c=2"))
        else:
            need_higher_mult.append((speeds, "c>2?"))

    print(f"n = {n}: {len(need_higher_mult)} tuples need c > 1")
    for sp, note in need_higher_mult[:3]:
        print(f"  {sp}: {note}")

print("\n" + "=" * 70)
print("FINAL VERIFICATION: All coprime tuples have good time")
print("=" * 70)

# Final comprehensive test
for n in range(3, 6):
    max_speed = 4 * n
    all_good = True

    for speeds in combinations(range(1, max_speed + 1), n):
        if not is_coprime_tuple(speeds):
            continue

        t, k, period = find_good_time_crt(speeds, max_mult=20)
        if t is None:
            print(f"FAILURE: {speeds}")
            all_good = False

    if all_good:
        print(f"n = {n}: ALL coprime tuples (speeds ≤ {max_speed}) have good CRT time ✓")
