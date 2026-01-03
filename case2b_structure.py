#!/usr/bin/env python3
"""
Analyze the structure of Case 2b tuples.
Case 2b: Some v ≡ 0 (mod n+1) AND some u ≡ 0 (mod n)

Key question: What structural constraints exist?
"""

from fractions import Fraction
from math import gcd
from functools import reduce
from itertools import combinations

def is_coprime_tuple(speeds):
    """Check if gcd of all speeds is 1."""
    return reduce(gcd, speeds) == 1

def classify_tuple(speeds):
    """Classify tuple into Case 1, 2a, or 2b."""
    n = len(speeds)
    has_mult_n1 = any(v % (n+1) == 0 for v in speeds)
    has_mult_n = any(v % n == 0 for v in speeds)

    if not has_mult_n1:
        return "Case 1"
    elif not has_mult_n:
        return "Case 2a"
    else:
        return "Case 2b"

def get_case2b_structure(speeds):
    """Analyze structure of Case 2b tuple."""
    n = len(speeds)

    mults_n1 = [v for v in speeds if v % (n+1) == 0]
    mults_n = [v for v in speeds if v % n == 0]
    mults_both = [v for v in speeds if v % (n+1) == 0 and v % n == 0]
    neither = [v for v in speeds if v % (n+1) != 0 and v % n != 0]
    only_n1 = [v for v in speeds if v % (n+1) == 0 and v % n != 0]
    only_n = [v for v in speeds if v % (n+1) != 0 and v % n == 0]

    return {
        'mults_n1': mults_n1,
        'mults_n': mults_n,
        'mults_both': mults_both,
        'only_n1': only_n1,
        'only_n': only_n,
        'neither': neither
    }

def compute_ml(speeds, resolution=10000):
    """Compute ML (max loneliness) numerically."""
    n = len(speeds)
    threshold = Fraction(1, n+1)

    best_min_dist = Fraction(0)

    for i in range(resolution + 1):
        t = Fraction(i, resolution)
        min_dist = min(min(Fraction(v * t.numerator, t.denominator) % 1,
                          1 - Fraction(v * t.numerator, t.denominator) % 1)
                      for v in speeds)
        if min_dist > best_min_dist:
            best_min_dist = min_dist

    return float(best_min_dist)

def find_good_time(speeds, resolution=10000):
    """Find a time where all distances >= 1/(n+1)."""
    n = len(speeds)
    threshold = 1.0 / (n + 1)

    for i in range(1, resolution + 1):
        t = i / resolution
        min_dist = min(min(abs((v * t) % 1), 1 - (v * t) % 1) for v in speeds)
        if min_dist >= threshold - 1e-10:
            return t, min_dist

    return None, 0

print("=" * 70)
print("CASE 2B STRUCTURAL ANALYSIS")
print("=" * 70)

# Generate and analyze Case 2b tuples
for n in range(3, 6):
    print(f"\n{'='*70}")
    print(f"n = {n}")
    print(f"{'='*70}")

    case2b_tuples = []
    max_speed = 4 * n * (n + 1)

    # Generate coprime n-tuples
    from itertools import combinations

    for speeds in combinations(range(1, max_speed + 1), n):
        if is_coprime_tuple(speeds) and classify_tuple(speeds) == "Case 2b":
            case2b_tuples.append(speeds)

    print(f"Found {len(case2b_tuples)} Case 2b tuples")

    if len(case2b_tuples) == 0:
        continue

    # Analyze structure patterns
    patterns = {}
    for speeds in case2b_tuples[:100]:  # Sample first 100
        struct = get_case2b_structure(speeds)
        pattern = (len(struct['only_n1']), len(struct['only_n']), len(struct['mults_both']), len(struct['neither']))
        if pattern not in patterns:
            patterns[pattern] = []
        patterns[pattern].append(speeds)

    print(f"\nStructure patterns (only_n+1, only_n, both, neither):")
    for pattern, examples in sorted(patterns.items()):
        print(f"  {pattern}: {len(examples)} tuples")
        if len(examples) <= 3:
            for ex in examples:
                print(f"    Example: {ex}")
        else:
            print(f"    Example: {examples[0]}")

    # Key insight: Can a tuple have v divisible by BOTH n and n+1?
    # That means v divisible by lcm(n, n+1) = n(n+1)
    print(f"\nTuples with speed divisible by n(n+1) = {n*(n+1)}:")
    count_lcm = 0
    for speeds in case2b_tuples[:100]:
        if any(v % (n * (n + 1)) == 0 for v in speeds):
            count_lcm += 1
            if count_lcm <= 3:
                print(f"  {speeds}")
    print(f"  Total: {count_lcm}/100 sampled")

    # Find good times for Case 2b tuples
    print(f"\nGood times analysis:")

    # Try specific candidate times
    candidate_times = [
        Fraction(1, n * (n + 1)),  # t = 1/(n(n+1))
        Fraction(1, 2 * n + 1),     # t = 1/(2n+1)
        Fraction(1, 2 * n),         # t = 1/(2n)
        Fraction(2, 2 * n + 1),     # t = 2/(2n+1)
    ]

    for t in candidate_times:
        works_count = 0
        for speeds in case2b_tuples[:50]:
            threshold = 1.0 / (n + 1)
            t_float = float(t)
            min_dist = min(min(abs((v * t_float) % 1), 1 - (v * t_float) % 1) for v in speeds)
            if min_dist >= threshold - 1e-10:
                works_count += 1
        print(f"  t = {t} works for {works_count}/50 sampled tuples")

print("\n" + "=" * 70)
print("KEY INSIGHT CHECK: The 'other' speed structure")
print("=" * 70)

# For Case 2b, we have:
# - At least one speed v = (n+1)m
# - At least one speed u = nk
# What about the OTHER speeds?

for n in range(3, 5):
    print(f"\nn = {n}:")
    max_speed = 4 * n * (n + 1)

    for speeds in combinations(range(1, max_speed + 1), n):
        if not is_coprime_tuple(speeds) or classify_tuple(speeds) != "Case 2b":
            continue

        struct = get_case2b_structure(speeds)
        other_speeds = struct['neither']

        if len(other_speeds) > 0:
            # These are speeds NOT divisible by n or n+1
            # What are their residues mod n and mod n+1?
            residues_n = [v % n for v in other_speeds]
            residues_n1 = [v % (n+1) for v in other_speeds]

            print(f"  Tuple: {speeds}")
            print(f"    mult(n+1): {struct['only_n1']}, mult(n): {struct['only_n']}, both: {struct['mults_both']}")
            print(f"    Other speeds: {other_speeds}")
            print(f"    Other residues mod {n}: {residues_n}")
            print(f"    Other residues mod {n+1}: {residues_n1}")

            # Find good time
            t, md = find_good_time(speeds)
            print(f"    Good time: t ≈ {t:.6f}, min_dist = {md:.6f}, threshold = {1/(n+1):.6f}")
            print()
            break  # Just show one example per n
