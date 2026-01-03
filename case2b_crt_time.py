#!/usr/bin/env python3
"""
Case 2b: Test if t = k/(n(n+1)) works for some k.

Key idea: Since Case 2b has speeds divisible by n AND speeds divisible by n+1,
maybe the "natural" time is a multiple of 1/(n(n+1)).
"""

from fractions import Fraction
from math import gcd
from functools import reduce
from itertools import combinations

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

def check_time(speeds, t):
    """Check if time t gives all distances >= 1/(n+1)."""
    n = len(speeds)
    threshold = Fraction(1, n+1)

    for v in speeds:
        vt = Fraction(v) * t
        frac = vt - int(vt)  # Fractional part
        dist = min(frac, 1 - frac)
        if dist < threshold:
            return False
    return True

def find_good_k(speeds):
    """Find k such that t = k/(n(n+1)) works."""
    n = len(speeds)
    period = n * (n + 1)

    good_ks = []
    for k in range(1, period):
        t = Fraction(k, period)
        if check_time(speeds, t):
            good_ks.append(k)

    return good_ks

print("=" * 70)
print("CASE 2B: Testing t = k/(n(n+1)) times")
print("=" * 70)

for n in range(3, 7):
    print(f"\n{'='*70}")
    print(f"n = {n}, testing t = k/{n*(n+1)}")
    print(f"{'='*70}")

    case2b_tuples = []
    max_speed = 3 * n * (n + 1)  # Reduced for speed

    for speeds in combinations(range(1, max_speed + 1), n):
        if is_coprime_tuple(speeds) and classify_tuple(speeds) == "Case 2b":
            case2b_tuples.append(speeds)
            if len(case2b_tuples) >= 500:  # Sample size
                break

    print(f"Testing {len(case2b_tuples)} Case 2b tuples")

    all_have_good_k = True
    failures = []

    for speeds in case2b_tuples:
        good_ks = find_good_k(speeds)
        if not good_ks:
            all_have_good_k = False
            failures.append(speeds)
            if len(failures) <= 3:
                print(f"  NO good k for: {speeds}")

    if all_have_good_k:
        print(f"  ✓ ALL {len(case2b_tuples)} tuples have good k!")

        # Analyze which k values are most common
        k_counts = {}
        for speeds in case2b_tuples[:100]:
            for k in find_good_k(speeds):
                k_counts[k] = k_counts.get(k, 0) + 1

        print(f"\n  Most common good k values (out of 100 tuples):")
        sorted_ks = sorted(k_counts.items(), key=lambda x: -x[1])[:10]
        for k, count in sorted_ks:
            print(f"    k = {k} (k/{n*(n+1)} = {Fraction(k, n*(n+1))}): works for {count}/100")

    else:
        print(f"  ✗ {len(failures)} tuples have NO good k among 1..{n*(n+1)-1}")

        # For failures, find what time DOES work
        print(f"\n  Analyzing failures:")
        for speeds in failures[:5]:
            # Try more k values
            period = 2 * n * (n + 1)
            for k in range(1, period):
                t = Fraction(k, period)
                if check_time(speeds, t):
                    print(f"    {speeds}: t = {k}/{period} = {t} works")
                    break
            else:
                # Try even finer resolution
                period = 4 * n * (n + 1)
                for k in range(1, period):
                    t = Fraction(k, period)
                    if check_time(speeds, t):
                        print(f"    {speeds}: t = {k}/{period} = {t} works")
                        break
                else:
                    print(f"    {speeds}: No simple fractional time found!")

print("\n" + "=" * 70)
print("DEEPER ANALYSIS: What determines which k works?")
print("=" * 70)

n = 3
period = n * (n + 1)
print(f"\nFor n = {n}, period = {period}")

# For each k coprime to period, analyze why it works or fails
for k in range(1, period):
    if gcd(k, period) != 1:
        continue  # Skip non-coprime k

    t = Fraction(k, period)
    print(f"\nk = {k}, t = {t}:")

    # What residues does this give?
    for v in range(1, period + 1):
        vt = v * t
        frac = vt - int(vt)
        dist = min(float(frac), 1 - float(frac))
        if v <= 12:
            status = "✓" if dist >= 1/(n+1) else "✗"
            print(f"  v={v}: ||vt|| = {float(dist):.4f} {status}")
