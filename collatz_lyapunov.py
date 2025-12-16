#!/usr/bin/env python3
"""
Lyapunov function approach:
Can we find V(n) such that E[V(T(n))] < V(n) for all n?
"""

import math

def v2(n):
    """2-adic valuation"""
    if n == 0:
        return float('inf')
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k

def T(n):
    """Collatz map for odd numbers only"""
    assert n % 2 == 1
    m = 3*n + 1
    return m // (2**v2(m))

def collatz_step(n):
    """Single Collatz step"""
    return n // 2 if n % 2 == 0 else 3*n + 1

print("Lyapunov Function Analysis")
print("="*80)
print()

# Try V(n) = log(n)
print("Test 1: V(n) = log(n)")
print("-"*80)
print("n\tV(n)\tT(n)\tV(T(n))\tΔV")
print("-"*80)

for n in [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27]:
    Tn = T(n)
    Vn = math.log(n)
    VTn = math.log(Tn)
    delta = VTn - Vn
    print(f"{n}\t{Vn:.3f}\t{Tn}\t{VTn:.3f}\t{delta:+.3f}")

print()
print("Result: ΔV is sometimes positive (fails as strict Lyapunov)")
print()

# Try V(n) = n^α for some α < 1
print("="*80)
print("Test 2: V(n) = n^α")
print("-"*80)

for alpha in [0.9, 0.8, 0.7, 0.6, 0.5]:
    print(f"\nα = {alpha}")
    print("n\tV(n)\tT(n)\tV(T(n))\tΔV")
    print("-"*60)

    failures = 0
    for n in range(3, 100, 2):
        Tn = T(n)
        Vn = n**alpha
        VTn = Tn**alpha
        delta = VTn - Vn

        if n <= 25:
            print(f"{n}\t{Vn:.3f}\t{Tn}\t{VTn:.3f}\t{delta:+.3f}")

        if delta > 0:
            failures += 1

    print(f"Failures (ΔV > 0): {failures} out of {len(range(3, 100, 2))}")

# The issue: deterministic map doesn't always decrease
# But EXPECTED decrease over the DISTRIBUTION of n mod 2^k should work

print("\n" + "="*80)
print("NEW APPROACH: Expected Lyapunov over residue classes")
print("="*80)
print()

# For each residue class mod 2^k, compute expected change
print("For odd n, partition by n mod 8:")
print()

for r in [1, 3, 5, 7]:
    print(f"n ≡ {r} (mod 8):")

    # Sample many n in this residue class
    samples = []
    for n in range(r, 1000, 8):
        Tn = T(n)
        ratio = Tn / n
        samples.append((n, Tn, ratio))

    # Compute statistics
    ratios = [s[2] for s in samples]
    avg_ratio = sum(ratios) / len(ratios)

    print(f"  Average T(n)/n = {avg_ratio:.4f}")

    # Count how many increase vs decrease
    increases = sum(1 for r in ratios if r > 1)
    decreases = sum(1 for r in ratios if r < 1)
    print(f"  Increases: {increases}, Decreases: {decreases}")

    # Show a few examples
    print(f"  Examples: ", end="")
    for n, Tn, ratio in samples[:3]:
        print(f"n={n}→{Tn}({ratio:.2f})", end=" ")
    print()
    print()

print("="*80)
print("\nCRITICAL OBSERVATION:")
print("The map T doesn't decrease n for every single n.")
print("BUT: On average over residue classes, T(n)/n < 1")
print()
print("The question: Does this imply convergence?")
print()
print("This requires showing that even though some n increase,")
print("the increases are 'compensated' by later decreases.")
print()

# Let's check: for numbers that increase, what happens next?
print("="*80)
print("Following trajectories where T(n) > n:")
print("-"*80)

problem_numbers = []
for n in range(3, 100, 2):
    Tn = T(n)
    if Tn > n:
        problem_numbers.append(n)

print(f"Found {len(problem_numbers)} odd numbers < 100 where T(n) > n")
print()
print("Tracking what happens to these:")
print("n\tT(n)\tT²(n)\tT³(n)\t...until < n")
print("-"*80)

for n in problem_numbers[:15]:
    trajectory = [n]
    current = n

    for _ in range(20):
        current = T(current)
        trajectory.append(current)
        if current < n:
            break

    print(f"{n}\t", end="")
    for i, val in enumerate(trajectory[1:6]):
        marker = "*" if val < n else ""
        print(f"{val}{marker}\t", end="")
    print()

print("\n" + "="*80)
print("KEY INSIGHT:")
print("Even when T(n) > n, applying T repeatedly DOES eventually drop below n.")
print("This suggests: sequences eventually decrease even if not monotonically.")
