"""
Verify: Can any tight coprime instance have a speed ≡ 0 (mod n+1)?

For each n, enumerate candidate tight instances and check.
"""
from math import gcd
from fractions import Fraction
from itertools import combinations

def coprime_tuple(speeds):
    """Check if gcd of all speeds is 1"""
    g = speeds[0]
    for v in speeds[1:]:
        g = gcd(g, v)
    return g == 1

def compute_ML(speeds, num_samples=10000):
    """
    Compute ML = sup_t min_i ||v_i * t|| approximately
    Uses rational times with small denominators for exact computation
    """
    n = len(speeds)
    max_v = max(speeds)
    
    best_min_dist = 0
    best_t = None
    
    # Check rational times a/b for small b
    for b in range(1, min(500, max_v * (n+1) + 1)):
        for a in range(1, b):
            if gcd(a, b) == 1:  # Only reduced fractions
                t = Fraction(a, b)
                min_dist = float('inf')
                for v in speeds:
                    pos = (v * t) % 1
                    dist = min(pos, 1 - pos)
                    min_dist = min(min_dist, float(dist))
                
                if min_dist > best_min_dist:
                    best_min_dist = min_dist
                    best_t = t
    
    return best_min_dist, best_t

def is_tight(speeds, tol=1e-9):
    """Check if tuple is tight (ML = 1/(n+1))"""
    n = len(speeds)
    target = 1 / (n + 1)
    ML, _ = compute_ML(speeds)
    return abs(ML - target) < tol

def has_divisible_speed(speeds):
    """Check if any speed ≡ 0 (mod n+1)"""
    n = len(speeds)
    return any(v % (n + 1) == 0 for v in speeds)

# Known tight instances from literature
known_tight = [
    [1, 2, 3],  # n=3
    [1, 2, 3, 4],  # n=4
    [1, 2, 3, 4, 5],  # n=5
    [1, 3, 4, 7],  # n=4, non-arithmetic (Goddyn-Wong)
    [1, 2, 3, 4, 5, 6],  # n=6
    [1, 3, 4, 5, 9],  # n=5, non-arithmetic
    [1, 2, 3, 4, 5, 6, 7],  # n=7
    [1, 2, 3, 4, 5, 7, 12],  # n=7, non-arithmetic
]

print("Checking known tight instances:")
print("=" * 60)
for speeds in known_tight:
    n = len(speeds)
    is_cop = coprime_tuple(speeds)
    tight = is_tight(speeds)
    has_div = has_divisible_speed(speeds)
    ML, best_t = compute_ML(speeds)
    target = 1/(n+1)
    
    print(f"Speeds: {speeds}")
    print(f"  n={n}, n+1={n+1}")
    print(f"  Coprime: {is_cop}, Tight: {tight} (ML={ML:.6f}, target={target:.6f})")
    print(f"  Has speed ≡ 0 (mod {n+1}): {has_div}")
    print(f"  Speeds mod {n+1}: {[v % (n+1) for v in speeds]}")
    print()

# Now try to CONSTRUCT a tight instance with speed ≡ 0 (mod n+1)
print("\nAttempting to find tight instance with speed ≡ 0 (mod n+1):")
print("=" * 60)

for n in range(3, 8):
    print(f"\nn = {n}, looking for tight tuple with some v ≡ 0 (mod {n+1})...")
    found = False
    
    # Try tuples where one speed is (n+1) and others are from 1..3(n+1)
    base_speed = n + 1  # This is ≡ 0 (mod n+1)
    
    # Try various combinations
    candidates = list(range(1, 3*(n+1)))
    candidates = [c for c in candidates if c != base_speed and c % (n+1) != 0]
    
    count = 0
    for other_speeds in combinations(candidates, n-1):
        speeds = list(other_speeds) + [base_speed]
        if coprime_tuple(speeds):
            count += 1
            if count > 1000:  # Limit search
                break
            if is_tight(speeds):
                print(f"  FOUND: {sorted(speeds)} is tight with {base_speed} ≡ 0 (mod {n+1})!")
                found = True
                break
    
    if not found:
        print(f"  No tight instance found with speed ≡ 0 (mod {n+1}) in {count} candidates checked")
