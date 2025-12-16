#!/usr/bin/env python3
"""
Collatz Invariant Search
Attempting to find invariants that prove convergence
"""

def v2(n):
    """2-adic valuation: largest k such that 2^k divides n"""
    if n == 0:
        return float('inf')
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k

def T(n):
    """Map odd numbers to odd numbers via (3n+1)/2^v2(3n+1)"""
    assert n % 2 == 1, "T requires odd input"
    m = 3*n + 1
    return m // (2**v2(m))

def collatz_trajectory_odds(n):
    """Return sequence of odd numbers in Collatz trajectory"""
    odds = []
    while n != 1:
        if n % 2 == 1:
            odds.append(n)
        n = 3*n + 1 if n % 2 == 1 else n // 2
        if len(odds) > 10000:  # Prevent infinite loops
            break
    return odds

# Compute T for small odd numbers
print("T mapping for odd numbers:")
print("n\tT(n)\tv₂(3n+1)\tratio T(n)/n")
print("-" * 50)
for n in range(1, 50, 2):
    Tn = T(n)
    ratio = Tn / n
    print(f"{n}\t{Tn}\t{v2(3*n+1)}\t\t{ratio:.4f}")

print("\n" + "="*50)
print("\nSearching for patterns in residue classes...")

# Check: what is n mod 3?
print("\nGrouped by n mod 3:")
for mod_class in [1, 2]:  # odd numbers are 1 or 2 mod 3
    print(f"\nn ≡ {mod_class} (mod 3):")
    for n in range(mod_class, 30, 3):
        if n % 2 == 1:
            Tn = T(n)
            print(f"  n={n}: T(n)={Tn}, T(n) mod 3 = {Tn % 3}")

print("\n" + "="*50)
print("\nChecking if T(n) < n for all odd n > 1...")

counterexamples = []
for n in range(3, 1000, 2):
    Tn = T(n)
    if Tn >= n:
        counterexamples.append((n, Tn))

if counterexamples:
    print(f"Found {len(counterexamples)} counterexamples where T(n) >= n:")
    for n, Tn in counterexamples[:20]:
        print(f"  n={n}, T(n)={Tn}")
else:
    print("NO counterexamples found! T(n) < n for all tested odd n > 1")

print("\n" + "="*50)
print("\nAnalyzing the ratio T(n)/n...")

# What determines when T(n) < n?
# T(n) = (3n+1)/2^k < n
# 3n+1 < n*2^k
# 3n+1 < n*2^k
# (3n+1)/n < 2^k
# 3 + 1/n < 2^k

print("\nFor T(n) < n, we need 2^v₂(3n+1) > 3:")
print("This means v₂(3n+1) ≥ 2")

print("\nChecking v₂(3n+1) distribution:")
v2_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
for n in range(1, 1000, 2):
    k = v2(3*n+1)
    if k in v2_counts:
        v2_counts[k] += 1
    else:
        v2_counts[k] = 1

for k in sorted(v2_counts.keys()):
    print(f"  v₂(3n+1) = {k}: {v2_counts[k]} occurrences")

# What about n where v2(3n+1) = 1?
print("\n" + "="*50)
print("\nOdd n where v₂(3n+1) = 1 (these have T(n) > n):")
problem_cases = []
for n in range(1, 100, 2):
    if v2(3*n+1) == 1:
        problem_cases.append(n)
        if len(problem_cases) <= 10:
            print(f"  n={n}, 3n+1={3*n+1}, T(n)={T(n)}")

print(f"\nTotal in range [1,100]: {len(problem_cases)}")
print(f"These are n ≡ ? (mod 4):")
for mod in range(4):
    count = sum(1 for n in problem_cases if n % 4 == mod)
    print(f"  n ≡ {mod} (mod 4): {count}")
