#!/usr/bin/env python3
"""
Case 2b: Rigorous overlap analysis.

Key question: Can we prove algebraically that Case 2b tuples always have gaps?

For an n-tuple with bad sets B_1, ..., B_n:
- Each B_i has measure 2/(n+1)
- Total measure if disjoint: 2n/(n+1)
- For tight tuples, overlaps exactly make up the difference: ∪B_i = [0,1)

The overlap inequality shows B_{n+1} ∩ B_1 > B_n ∩ B_1.
This EXCESS overlap might guarantee gaps.
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

def bad_set_measure(v, n):
    """Measure of B_v = {t : ||vt|| ≤ 1/(n+1)}."""
    return Fraction(2, n + 1)

def pairwise_overlap(v1, v2, n, resolution=100000):
    """Numerically compute |B_{v1} ∩ B_{v2}|."""
    threshold = 1.0 / (n + 1)
    count = 0

    for i in range(resolution):
        t = i / resolution
        d1 = min(abs((v1 * t) % 1), 1 - (v1 * t) % 1)
        d2 = min(abs((v2 * t) % 1), 1 - (v2 * t) % 1)
        if d1 <= threshold and d2 <= threshold:
            count += 1

    return count / resolution

def union_measure(speeds, n, resolution=100000):
    """Numerically compute |∪B_v|."""
    threshold = 1.0 / (n + 1)
    count = 0

    for i in range(resolution):
        t = i / resolution
        all_far = True
        for v in speeds:
            dist = min(abs((v * t) % 1), 1 - (v * t) % 1)
            if dist <= threshold:
                all_far = False
                break
        if not all_far:
            count += 1

    return count / resolution

def gap_measure(speeds, n, resolution=100000):
    """Numerically compute measure of good set = 1 - |∪B_v|."""
    return 1 - union_measure(speeds, n, resolution)

print("=" * 70)
print("CASE 2B: RIGOROUS OVERLAP ANALYSIS")
print("=" * 70)

print("\n1. STANDARD TUPLE (tight, Case 1)")
print("-" * 50)

for n in range(3, 6):
    speeds = tuple(range(1, n + 1))
    union_m = union_measure(speeds, n)
    gap_m = gap_measure(speeds, n)
    print(f"n={n}, tuple={speeds}")
    print(f"  Union measure: {union_m:.6f} (theory: 1.000000)")
    print(f"  Gap measure: {gap_m:.6f}")

print("\n2. CASE 2 TUPLES (replace n with n+1)")
print("-" * 50)

for n in range(3, 6):
    # Replace speed n with n+1
    speeds = tuple(list(range(1, n)) + [n + 1])
    union_m = union_measure(speeds, n)
    gap_m = gap_measure(speeds, n)

    # Compute key overlap difference
    overlap_standard = pairwise_overlap(n, 1, n)
    overlap_case2 = pairwise_overlap(n + 1, 1, n)
    excess_overlap = overlap_case2 - overlap_standard

    print(f"n={n}, tuple={speeds}")
    print(f"  Union measure: {union_m:.6f}")
    print(f"  Gap measure: {gap_m:.6f}")
    print(f"  B_n ∩ B_1: {overlap_standard:.6f}")
    print(f"  B_(n+1) ∩ B_1: {overlap_case2:.6f}")
    print(f"  Excess overlap: {excess_overlap:.6f}")

print("\n3. CASE 2B SPECIFIC: Tuples with mult(n) AND mult(n+1)")
print("-" * 50)

for n in range(3, 6):
    print(f"\nn = {n}:")

    # Find some Case 2b tuples
    case2b_examples = []
    max_speed = 3 * n * (n + 1)

    for speeds in combinations(range(1, max_speed + 1), n):
        if is_coprime_tuple(speeds) and classify_tuple(speeds) == "Case 2b":
            case2b_examples.append(speeds)
            if len(case2b_examples) >= 10:
                break

    for speeds in case2b_examples[:5]:
        union_m = union_measure(speeds, n)
        gap_m = gap_measure(speeds, n)

        # Find which speeds are special
        mult_n1 = [v for v in speeds if v % (n + 1) == 0]
        mult_n = [v for v in speeds if v % n == 0]
        mult_both = [v for v in speeds if v % (n * (n + 1)) == 0]

        print(f"  {speeds}")
        print(f"    mult({n+1}): {mult_n1}, mult({n}): {mult_n}, mult(both): {mult_both}")
        print(f"    Union: {union_m:.6f}, Gap: {gap_m:.6f}")

print("\n4. KEY THEORETICAL CALCULATION")
print("-" * 50)

print("""
For n runners with speeds v_1, ..., v_n:
- Each bad set B_i has measure 2/(n+1)
- Total if disjoint: 2n/(n+1)

By inclusion-exclusion:
|∪B_i| = Σ|B_i| - Σ|B_i ∩ B_j| + ...

For standard tuple {1,...,n} (tight, |∪B_i| = 1):
Total overlap = 2n/(n+1) - 1 = (n-1)/(n+1)

For Case 2, we replace some speed with (n+1)m.
Question: Is the total overlap LARGER, creating gaps?
""")

for n in range(3, 6):
    standard = tuple(range(1, n + 1))
    case2 = tuple(list(range(1, n)) + [n + 1])

    # Compute ALL pairwise overlaps
    standard_total_overlap = 0
    case2_total_overlap = 0

    for i in range(n):
        for j in range(i + 1, n):
            standard_total_overlap += pairwise_overlap(standard[i], standard[j], n)
            case2_total_overlap += pairwise_overlap(case2[i], case2[j], n)

    print(f"n = {n}:")
    print(f"  Standard tuple pairwise overlaps sum: {standard_total_overlap:.6f}")
    print(f"  Case 2 tuple pairwise overlaps sum: {case2_total_overlap:.6f}")
    print(f"  Difference: {case2_total_overlap - standard_total_overlap:.6f}")

    # The gap should be related to excess overlap
    gap = gap_measure(case2, n)
    print(f"  Actual gap measure: {gap:.6f}")
    print()

print("\n5. THE ALGEBRAIC OVERLAP FORMULA")
print("-" * 50)

print("""
For speeds a and b, the overlap |B_a ∩ B_b| can be computed exactly.

Let g = gcd(a, b), a = g·a', b = g·b'.
The overlap depends on the structure of {a'·k mod b' : k = 0,...,b'-1}.

For a = 1 and b = n:
  B_1 ∩ B_n = {t : ||t|| ≤ 1/(n+1) AND ||nt|| ≤ 1/(n+1)}

At t near 0: ||t|| ≤ 1/(n+1) means t ∈ [0, 1/(n+1)]
             ||nt|| ≤ 1/(n+1) means nt ∈ [0, 1/(n+1)] → t ∈ [0, 1/(n(n+1))]
So near 0, overlap = 1/(n(n+1)) on each end, total = 2/(n(n+1)).

For a = 1 and b = n+1:
  Near 0: ||t|| ≤ 1/(n+1) means t ∈ [0, 1/(n+1)]
          ||(n+1)t|| ≤ 1/(n+1) means (n+1)t ∈ [0, 1/(n+1)] → t ∈ [0, 1/(n+1)²]

Wait, this is wrong. Let me recalculate...
""")

# Let's compute the EXACT overlap formulas
def exact_overlap_B1_Bn(n):
    """Compute |B_1 ∩ B_n| exactly."""
    # B_1 = {t : ||t|| ≤ 1/(n+1)} = [0, 1/(n+1)] ∪ [n/(n+1), 1]
    # B_n = {t : ||nt|| ≤ 1/(n+1)}
    #     = {t : nt mod 1 ∈ [0, 1/(n+1)] ∪ [n/(n+1), 1]}

    # The overlap consists of t where BOTH conditions hold.
    # This is a finite union of intervals.

    # Numerically compute with high precision
    return pairwise_overlap(1, n, n, resolution=1000000)

def exact_overlap_B1_Bn1(n):
    """Compute |B_1 ∩ B_{n+1}| exactly."""
    return pairwise_overlap(1, n + 1, n, resolution=1000000)

print("High-precision overlap calculations:")
for n in range(3, 8):
    o_n = exact_overlap_B1_Bn(n)
    o_n1 = exact_overlap_B1_Bn1(n)
    ratio = o_n1 / o_n if o_n > 0 else float('inf')

    # Theoretical values
    theory_n = 2 / (n * (n + 1))
    theory_n1 = 4 / (n + 1) ** 2

    print(f"n = {n}:")
    print(f"  |B_1 ∩ B_n|: computed={o_n:.8f}, theory={theory_n:.8f}")
    print(f"  |B_1 ∩ B_(n+1)|: computed={o_n1:.8f}, theory={theory_n1:.8f}")
    print(f"  Ratio: {ratio:.4f}, theory ratio = {(theory_n1/theory_n):.4f} = 2n/(n+1)")
