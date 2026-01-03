#!/usr/bin/env python3
"""
Case 2b: CRT-based algebraic approach.

Key insight: For coprime tuple (v_1, ..., v_n), can we use CRT to
construct a time t where all distances are >= 1/(n+1)?

At t = k/L where L = lcm(v_1, ..., v_n):
  ||v_i * k/L|| = ||k * v_i/L|| = ||k/m_i|| where m_i = L/v_i

We need: for all i, ||k/m_i|| >= 1/(n+1)
i.e., (k mod m_i)/m_i in [1/(n+1), n/(n+1)]
i.e., k mod m_i in [m_i/(n+1), n*m_i/(n+1)]

The number of valid residues for each i is approx (n-1)*m_i/(n+1).
By CRT, if the constraints are consistent, a solution exists.
"""

from fractions import Fraction
from math import gcd, lcm
from functools import reduce
from itertools import combinations

def multi_lcm(numbers):
    return reduce(lcm, numbers)

def is_coprime_tuple(speeds):
    return reduce(gcd, speeds) == 1

def classify_tuple(speeds):
    n = len(speeds)
    has_mult_n1 = any(v % (n+1) == 0 for v in speeds)
    has_mult_n = any(v % n == 0 for v in speeds)
    if not has_mult_n1:
        return "Case 1"
    elif not has_mult_n:
        return "Case 2a"
    else:
        return "Case 2b"

def valid_residues(m, n):
    """
    Find residues r in {0, ..., m-1} such that ||r/m|| >= 1/(n+1).
    ||r/m|| = min(r/m, 1 - r/m) >= 1/(n+1)
    iff r/m in [1/(n+1), n/(n+1)]
    iff r in [m/(n+1), n*m/(n+1)]
    """
    lower = m / (n + 1)
    upper = n * m / (n + 1)
    return set(range(int(lower) + 1, int(upper) + 1))

def find_crt_solution(moduli, valid_sets):
    """
    Find k such that k mod m_i is in valid_sets[i] for all i.
    Uses brute force for now.
    """
    L = multi_lcm(moduli)

    for k in range(1, L):
        valid = True
        for m, valid_r in zip(moduli, valid_sets):
            if k % m not in valid_r:
                valid = False
                break
        if valid:
            return k, L

    return None, L

def check_time(speeds, t):
    """Check if time t gives all distances >= 1/(n+1)."""
    n = len(speeds)
    threshold = Fraction(1, n + 1)

    for v in speeds:
        vt = Fraction(v) * t
        frac = vt - int(vt)
        dist = min(frac, 1 - frac)
        if dist < threshold:
            return False, v, float(dist)
    return True, None, None

print("=" * 70)
print("CRT-BASED GOOD TIME CONSTRUCTION")
print("=" * 70)

for n in range(3, 6):
    print(f"\n{'='*70}")
    print(f"n = {n}")
    print(f"{'='*70}")

    case2b_tuples = []
    max_speed = 2 * n * (n + 1)

    for speeds in combinations(range(1, max_speed + 1), n):
        if is_coprime_tuple(speeds) and classify_tuple(speeds) == "Case 2b":
            case2b_tuples.append(speeds)
            if len(case2b_tuples) >= 100:
                break

    print(f"Testing {len(case2b_tuples)} Case 2b tuples")

    success = 0
    failures = []

    for speeds in case2b_tuples:
        L = multi_lcm(speeds)
        moduli = [L // v for v in speeds]
        valid_sets = [valid_residues(m, n) for m in moduli]

        k, period = find_crt_solution(moduli, valid_sets)

        if k is not None:
            t = Fraction(k, period)
            ok, bad_v, bad_d = check_time(speeds, t)
            if ok:
                success += 1
            else:
                failures.append((speeds, f"CRT found k={k}/L={period} but failed at v={bad_v}"))
        else:
            # Try finer resolution
            found = False
            for mult in [2, 3, 4, 6]:
                L2 = L * mult
                moduli2 = [L2 // v for v in speeds]
                valid_sets2 = [valid_residues(m, n) for m in moduli2]
                k2, period2 = find_crt_solution(moduli2, valid_sets2)
                if k2 is not None:
                    t = Fraction(k2, period2)
                    ok, _, _ = check_time(speeds, t)
                    if ok:
                        success += 1
                        found = True
                        break
            if not found:
                failures.append((speeds, "No CRT solution at any tested resolution"))

    print(f"Success: {success}/{len(case2b_tuples)}")
    if failures:
        print(f"Failures: {len(failures)}")
        for sp, reason in failures[:5]:
            print(f"  {sp}: {reason}")

print("\n" + "=" * 70)
print("DETAILED ANALYSIS: Why CRT works for coprime tuples")
print("=" * 70)

# For a coprime tuple, analyze the CRT constraints
speeds = (1, 3, 4)  # Simple Case 2b
n = 3
print(f"\nExample: speeds = {speeds}, n = {n}")

L = multi_lcm(speeds)
print(f"L = lcm{speeds} = {L}")

moduli = [L // v for v in speeds]
print(f"Moduli m_i = L/v_i: {moduli}")

valid_sets = [valid_residues(m, n) for m in moduli]
for i, (v, m, vs) in enumerate(zip(speeds, moduli, valid_sets)):
    print(f"  Speed {v}: m={m}, valid residues = {sorted(vs)}")

k, period = find_crt_solution(moduli, valid_sets)
if k:
    print(f"\nCRT solution: k = {k}, t = {k}/{period} = {Fraction(k, period)}")
    t = Fraction(k, period)
    print("Verification:")
    for v in speeds:
        vt = Fraction(v) * t
        frac = vt - int(vt)
        dist = min(frac, 1 - frac)
        print(f"  Speed {v}: ||{v}*{t}|| = ||{vt}|| = {dist} {'✓' if dist >= Fraction(1, n+1) else '✗'}")

print("\n" + "=" * 70)
print("KEY THEOREM: Valid residue count")
print("=" * 70)

print("""
For modulus m and threshold 1/(n+1):
  Valid residues count = |{r : r/m in [1/(n+1), n/(n+1)]}|
                       = floor(n*m/(n+1)) - ceil(m/(n+1)) + 1
                       ≈ (n-1)*m/(n+1)

For m >= 2: valid count >= (n-1)*2/(n+1) = 2(n-1)/(n+1)
For n = 3: 2*2/4 = 1
For n = 4: 2*3/5 = 1.2
For n = 5: 2*4/6 = 1.33

So for m >= 2 and n >= 3, there's at least 1 valid residue per constraint.
""")

for n in range(3, 8):
    print(f"\nn = {n}:")
    for m in range(1, 10):
        valid = valid_residues(m, n)
        count = len(valid)
        theory = (n - 1) * m / (n + 1)
        print(f"  m = {m}: {count} valid residues, theory ≈ {theory:.2f}")

print("\n" + "=" * 70)
print("THE CRITICAL QUESTION: When does CRT have a solution?")
print("=" * 70)

print("""
By CRT, a solution exists iff the constraints are pairwise compatible.

For moduli m_i and valid sets V_i, we need:
  For all pairs (i, j), there exists r such that:
    r ≡ v_i (mod gcd(m_i, m_j)) for some v_i in V_i
    r ≡ v_j (mod gcd(m_i, m_j)) for some v_j in V_j

This is the "pairwise consistency" condition.

For coprime tuples, the moduli m_i = L/v_i have specific structure.
If v_i and v_j are coprime, then gcd(m_i, m_j) = L/(v_i * v_j) * gcd(...).

The coprimality of the tuple (gcd of all speeds = 1) ensures
that the constraints don't "collide" in a way that blocks all solutions.
""")

# Test pairwise compatibility
def check_pairwise_compatibility(moduli, valid_sets):
    n = len(moduli)
    for i in range(n):
        for j in range(i + 1, n):
            g = gcd(moduli[i], moduli[j])
            residues_i = set(r % g for r in valid_sets[i])
            residues_j = set(r % g for r in valid_sets[j])
            common = residues_i & residues_j
            if not common:
                return False, (i, j, g, residues_i, residues_j)
    return True, None

for speeds in [(1, 3, 4), (1, 2, 12), (1, 2, 4, 5)]:
    n = len(speeds)
    L = multi_lcm(speeds)
    moduli = [L // v for v in speeds]
    valid_sets = [valid_residues(m, n) for m in moduli]

    compatible, info = check_pairwise_compatibility(moduli, valid_sets)
    print(f"\nSpeeds {speeds}:")
    print(f"  Moduli: {moduli}")
    if compatible:
        print(f"  Pairwise compatible: YES")
    else:
        i, j, g, ri, rj = info
        print(f"  Pairwise compatible: NO")
        print(f"    Conflict between moduli {moduli[i]} and {moduli[j]}")
        print(f"    gcd = {g}, residues_i mod {g} = {ri}, residues_j mod {g} = {rj}")
