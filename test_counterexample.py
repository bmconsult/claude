"""
Test potential counterexample to Key Lemma:
{1,2,3,4,5,7} has n=6, n+1=7, and speed 7 ≡ 0 (mod 7)

Is this tuple tight? What's the optimal time?
"""
from fractions import Fraction
from math import gcd

def distance(v, t):
    """||vt|| = distance to nearest integer"""
    pos = float(v * t) % 1
    return min(pos, 1 - pos)

def compute_ML(speeds, max_denom=500):
    """Find optimal time and ML value"""
    best_min_dist = 0
    best_t = None
    
    for b in range(1, max_denom + 1):
        for a in range(1, b):
            if gcd(a, b) == 1:
                t = Fraction(a, b)
                min_dist = min(distance(v, t) for v in speeds)
                if min_dist > best_min_dist:
                    best_min_dist = min_dist
                    best_t = t
    
    return best_min_dist, best_t

# Test {1,2,3,4,5,7}
print("Testing {1,2,3,4,5,7}:")
print("=" * 60)
speeds = [1, 2, 3, 4, 5, 7]
n = len(speeds)
target = 1 / (n + 1)

ML, best_t = compute_ML(speeds, max_denom=500)
print(f"n = {n}, n+1 = {n+1}")
print(f"Target (1/(n+1)) = {target:.6f}")
print(f"ML = {ML:.6f}")
print(f"Optimal time = {best_t} = {float(best_t):.6f}")
print(f"Denominator = {best_t.denominator}")
print(f"Is tight? {abs(ML - target) < 1e-9}")
print(f"Has speed ≡ 0 (mod {n+1})? {any(v % (n+1) == 0 for v in speeds)}")

print("\nAt optimal time t =", best_t, ":")
for v in speeds:
    d = distance(v, best_t)
    print(f"  Speed {v}: distance = {d:.6f} {'(tight)' if abs(d - target) < 1e-9 else ''}")

# Compare with standard {1,2,3,4,5,6}
print("\n" + "=" * 60)
print("Compare with standard {1,2,3,4,5,6}:")
speeds2 = [1, 2, 3, 4, 5, 6]
ML2, best_t2 = compute_ML(speeds2, max_denom=500)
print(f"ML = {ML2:.6f}, optimal time = {best_t2}")

# Check if {1,2,3,4,5,7} achieves exactly 1/7
print("\n" + "=" * 60)
print("CRITICAL CHECK:")
print(f"Is {1,2,3,4,5,7} a COUNTEREXAMPLE to Key Lemma?")
print(f"  Has speed ≡ 0 (mod 7)? YES (speed 7)")
print(f"  Is tight (ML = 1/7)? {abs(ML - 1/7) < 1e-9}")
print(f"  Optimal time denominator = {best_t.denominator}")
print(f"  Is denominator = n+1 = 7? {best_t.denominator == 7}")
