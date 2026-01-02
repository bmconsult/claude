"""
NEW APPROACH: Measure-theoretic proof of Theorem 4.1

IDEA: Show that the "bad set" (times where some speed is too close to 0)
      cannot cover [0,1) for Case 2 tuples.

For speed v, define:
  B_v = {t ∈ [0,1) : ||vt|| ≤ 1/(n+1)}

This is the set of "bad times" for speed v.

LRC holds iff the complement of ⋃B_v is non-empty.
"""

from fractions import Fraction
from math import gcd
from functools import reduce

def bad_set_measure(v, n):
    """
    Compute the measure of B_v = {t : ||vt|| ≤ 1/(n+1)} in [0,1).

    For each integer k, vt = k has a neighborhood of width 2/(v(n+1)).
    There are v such integers k with k/v ∈ [0,1).
    Total measure = v × 2/(v(n+1)) = 2/(n+1).
    """
    return 2 / (n + 1)

def bad_set_intervals(v, n):
    """
    Return the intervals comprising B_v in [0,1).

    B_v = ⋃_{k=0}^{v-1} [k/v - 1/(v(n+1)), k/v + 1/(v(n+1))]
    """
    intervals = []
    half_width = 1 / (v * (n + 1))

    for k in range(v):
        center = k / v
        left = center - half_width
        right = center + half_width

        # Handle wrap-around at 0
        if left < 0:
            intervals.append((0, right))
            intervals.append((1 + left, 1))
        elif right > 1:
            intervals.append((left, 1))
            intervals.append((0, right - 1))
        else:
            intervals.append((left, right))

    return intervals

print("=" * 70)
print("MEASURE-THEORETIC APPROACH TO THEOREM 4.1")
print("=" * 70)

print("""
OBSERVATION 1: Each speed v contributes a bad set of measure 2/(n+1).

For n speeds, naive upper bound on total bad measure: 2n/(n+1).

For n ≥ 2, this is ≥ 1, so bad sets COULD cover [0,1).

But this ignores overlaps!
""")

def compute_union_measure(speeds, n, resolution=10000):
    """
    Numerically compute the measure of ⋃B_v.
    """
    # Discretize [0,1) into resolution points
    bad = [False] * resolution

    for v in speeds:
        half_width = 1 / (v * (n + 1))
        for k in range(v):
            center = k / v
            left = int((center - half_width) * resolution)
            right = int((center + half_width) * resolution) + 1

            for i in range(max(0, left), min(resolution, right)):
                bad[i] = True

            # Handle wrap-around
            if left < 0:
                for i in range(resolution + left, resolution):
                    bad[i] = True
            if right > resolution:
                for i in range(0, right - resolution):
                    bad[i] = True

    return sum(bad) / resolution

print("Testing union measure for various tuples:")
print("-" * 50)

# Case 1 tuples (tight)
case1_examples = [
    [1, 2, 3],        # n=3, standard
    [1, 2, 3, 4],     # n=4, standard
    [1, 2, 3, 4, 5],  # n=5, standard
]

print("\nCase 1 (tight) tuples:")
for speeds in case1_examples:
    n = len(speeds)
    naive_bound = 2 * n / (n + 1)
    actual = compute_union_measure(speeds, n)
    gap = 1 - actual  # Measure of good set

    print(f"  {speeds}: naive={naive_bound:.4f}, actual={actual:.4f}, good_set={gap:.4f}")

# Case 2 tuples
case2_examples = [
    [1, 2, 4],        # n=3, 4≡0 (mod 4)
    [1, 2, 3, 5],     # n=4, 5≡0 (mod 5)
    [1, 2, 3, 4, 6],  # n=5, 6≡0 (mod 6)
    [1, 2, 3, 4, 5, 7],  # n=6, 7≡0 (mod 7)
]

print("\nCase 2 tuples (with v ≡ 0 mod n+1):")
for speeds in case2_examples:
    n = len(speeds)
    naive_bound = 2 * n / (n + 1)
    actual = compute_union_measure(speeds, n)
    gap = 1 - actual  # Measure of good set

    print(f"  {speeds}: naive={naive_bound:.4f}, actual={actual:.4f}, good_set={gap:.4f}")

print("""

KEY OBSERVATION:
  For Case 1 (tight) tuples: good_set measure is SMALL (tuples are "bad")
  For Case 2 tuples: good_set measure is LARGER (tuples have room)

This is because the speed v ≡ 0 (mod n+1) has its bad intervals at
DIFFERENT positions than other speeds, reducing overlap.
""")

print("=" * 70)
print("THE OVERLAP STRUCTURE")
print("=" * 70)

print("""
For speed v, bad intervals are centered at k/v for k = 0, 1, ..., v-1.

For v = (n+1)m, centers are at k/((n+1)m) for k = 0, 1, ..., (n+1)m-1.
These include 0, 1/(n+1), 2/(n+1), ..., n/(n+1) (when k is a multiple of m).

For v ≢ 0 (mod n+1), centers are at k/v, which generally DON'T align
with multiples of 1/(n+1).

The MISALIGNMENT creates gaps that aren't covered by any bad set!
""")

def find_gaps(speeds, n, resolution=10000):
    """Find the good intervals (gaps in the bad set)."""
    bad = [False] * resolution

    for v in speeds:
        half_width = 1 / (v * (n + 1))
        for k in range(v):
            center = k / v
            left = int((center - half_width) * resolution)
            right = int((center + half_width) * resolution) + 1

            for i in range(max(0, left), min(resolution, right)):
                bad[i] = True
            if left < 0:
                for i in range(resolution + left, resolution):
                    bad[i] = True
            if right > resolution:
                for i in range(0, right - resolution):
                    bad[i] = True

    # Find gaps
    gaps = []
    in_gap = False
    gap_start = 0

    for i in range(resolution):
        if not bad[i] and not in_gap:
            in_gap = True
            gap_start = i
        elif bad[i] and in_gap:
            in_gap = False
            gaps.append((gap_start / resolution, i / resolution))

    if in_gap:
        gaps.append((gap_start / resolution, 1.0))

    return gaps

print("\nGap analysis for Case 2 tuples:")
print("-" * 50)

for speeds in case2_examples:
    n = len(speeds)
    gaps = find_gaps(speeds, n)

    print(f"\n{speeds}:")
    print(f"  Number of gaps: {len(gaps)}")
    if gaps:
        largest_gap = max(g[1] - g[0] for g in gaps)
        print(f"  Largest gap: {largest_gap:.6f}")
        print(f"  Sample gap centers: {[(g[0]+g[1])/2 for g in gaps[:5]]}")

print("\n" + "=" * 70)
print("THE PROOF IDEA")
print("=" * 70)

print("""
THEOREM 4.1 (Measure-theoretic proof):

For a Case 2 tuple with v_j = (n+1)m:

1. The bad set for v_j has centers at k/((n+1)m).
   These include the "dangerous" points 0, 1/(n+1), 2/(n+1), ..., n/(n+1).

2. The bad sets for other speeds v_i ≢ 0 (mod n+1) have centers at k/v_i.
   Since gcd(v_i, n+1) < n+1, these centers are NOT at multiples of 1/(n+1).

3. The MISALIGNMENT between v_j's bad set and other bad sets creates gaps.

4. Specifically: between consecutive centers of v_j's bad set, the other
   speeds' bad intervals don't fully cover the space.

5. By coprimality and the "missing residue" phenomenon, there exist times
   t in these gaps where ALL speeds have distance > 1/(n+1).

The key is: the speed v_j "anchors" the bad structure at multiples of 1/(n+1),
while other speeds' bad structure is incommensurate, creating gaps.
""")

# Verify this structure
print("\nVerifying the gap structure:")
print("-" * 50)

def analyze_bad_structure(speeds, n):
    """Analyze why gaps exist."""
    base = n + 1

    # Find the speed ≡ 0 (mod n+1)
    v_zero = None
    for v in speeds:
        if v % base == 0:
            v_zero = v
            break

    if v_zero is None:
        return "Not Case 2"

    m = v_zero // base

    # v_zero's bad centers: k/(base*m) for k = 0, ..., base*m-1
    # Other speeds' centers: k/v_i for k = 0, ..., v_i-1

    # The key: at t = 1/(2*base*m), v_zero is at position 1/2 (far from 0)
    # Can we show other speeds are also far?

    t = 1 / (2 * base * m)
    distances = []
    for v in speeds:
        pos = (v * t) % 1
        dist = min(pos, 1 - pos)
        distances.append((v, dist))

    return t, distances

for speeds in case2_examples:
    n = len(speeds)
    result = analyze_bad_structure(speeds, n)
    if isinstance(result, str):
        print(f"  {speeds}: {result}")
    else:
        t, distances = result
        print(f"  {speeds}:")
        print(f"    t = {t:.6f}")
        print(f"    distances: {[(v, f'{d:.4f}') for v, d in distances]}")
        print(f"    min_dist = {min(d for v, d in distances):.4f}, target = {1/(n+1):.4f}")
