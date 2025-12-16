#!/usr/bin/env python3
"""
Detailed analysis of mod 8 dynamics, especially n ≡ 7 (mod 8)
"""

def v2(n):
    """2-adic valuation"""
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k

def T(n):
    """Collatz map for odd numbers"""
    assert n % 2 == 1
    m = 3*n + 1
    return m // (2**v2(m))

print("Mod 8 Transition Analysis")
print("="*80)
print()

# For n ≡ 7 (mod 8), determine when T(n) ≡ 7 vs ≡ 3
print("Case n ≡ 7 (mod 8):")
print("We have n = 8k + 7 for some k ≥ 0")
print("Then 3n + 1 = 24k + 22 = 2(12k + 11)")
print("Since 12k + 11 is odd, v₂(3n+1) = 1")
print("So T(n) = 12k + 11")
print()
print("Now, 12k + 11 mod 8:")
print("  If k is even, k = 2m: T(n) = 24m + 11 ≡ 3 (mod 8)")
print("  If k is odd, k = 2m+1: T(n) = 24m + 23 ≡ 7 (mod 8)")
print()
print("So n ≡ 7 (mod 8) splits into two subclasses based on k mod 2:")
print("  n ≡ 7 (mod 16): T(n) ≡ 3 (mod 8) [ESCAPES!]")
print("  n ≡ 15 (mod 16): T(n) ≡ 7 (mod 8) [STAYS!]")
print()

# Verify empirically
print("Verification:")
print("n mod 16\tn\tT(n)\tT(n) mod 8\tT(n) mod 16")
print("-"*70)

for n in range(7, 100, 8):  # n ≡ 7 (mod 8)
    Tn = T(n)
    print(f"{n % 16:2d}\t\t{n}\t{Tn}\t{Tn % 8}\t\t{Tn % 16}")

print("\n" + "="*80)
print("REFINED ANALYSIS: n ≡ 15 (mod 16)")
print("="*80)
print()
print("For n ≡ 15 (mod 16), we have T(n) ≡ 7 (mod 8)")
print("But which subclass? Let's check n ≡ 15 (mod 32) vs ≡ 47 (mod 32)")
print()

# n ≡ 15 (mod 16) means n = 16j + 15 = 8(2j) + 15 with k = 2j+1 odd
# So n ≡ 15 (mod 16) means k ≡ 1 (mod 2), giving T(n) ≡ 7 (mod 8)
# Now, T(n) = 12k + 11 = 12(2j+1) + 11 = 24j + 23
# For T(n) ≡ ? (mod 16):
#   If j even, j=2m: T(n) = 48m + 23 ≡ 7 (mod 16)
#   If j odd, j=2m+1: T(n) = 48m + 71 ≡ 7 (mod 16) ...wait

print("Let me compute more carefully:")
print()
print("n ≡ 15 (mod 16) hierarchy:")

for n in range(15, 200, 16):
    Tn = T(n)
    T2n = T(Tn) if Tn > 1 else 1

    print(f"n={n:3d} ≡ {n%32:2d} (mod 32): T(n)={Tn:3d} ≡ {Tn%16:2d} (mod 16), ", end="")

    if Tn % 8 == 7:
        print(f"T²(n)={T2n:4d}", end="")
    print()

print("\n" + "="*80)
print("Pattern Discovery:")
print("="*80)
print()

# Let's trace longer chains starting from n ≡ 15 (mod 16)
print("Tracing trajectories from n ≡ 15 (mod 16):")
print()

for start in [15, 31, 47, 63, 79, 95]:
    print(f"n = {start}:")
    current = start
    mods = []

    for step in range(12):
        mod8 = current % 8
        mods.append((current, mod8))

        if current == 1:
            break

        current = T(current)

    print("  Trajectory:", " -> ".join(f"{n}({m})" for n, m in mods[:8]))

    # Count how many are ≡ 3,7 (mod 8) vs ≡ 1,5 (mod 8)
    bad_count = sum(1 for _, m in mods if m in [3, 7])
    good_count = sum(1 for _, m in mods if m in [1, 5])

    print(f"  Bad (3,7 mod 8): {bad_count}, Good (1,5 mod 8): {good_count}")
    print()

print("="*80)
print("KEY QUESTION: Can a trajectory stay in {3, 7} (mod 8) forever?")
print("="*80)
print()

# Let's check: among n ≡ 7 (mod 8), what fraction transition to 3 vs stay at 7?
transitions_to_3 = 0
stays_at_7 = 0

for n in range(7, 1000, 8):
    Tn = T(n)
    if Tn % 8 == 3:
        transitions_to_3 += 1
    elif Tn % 8 == 7:
        stays_at_7 += 1

print(f"From n ≡ 7 (mod 8) in [7, 1000):")
print(f"  Transitions to 3 (mod 8): {transitions_to_3}")
print(f"  Stays at 7 (mod 8): {stays_at_7}")
print(f"  Ratio: {transitions_to_3}/{stays_at_7} = {transitions_to_3/stays_at_7:.3f}")
print()

# And from 3 (mod 8)?
print(f"From n ≡ 3 (mod 8):")
to_1 = 0
to_5 = 0
for n in range(3, 1000, 8):
    Tn = T(n)
    if Tn % 8 == 1:
        to_1 += 1
    elif Tn % 8 == 5:
        to_5 += 1

print(f"  To 1 (mod 8): {to_1}")
print(f"  To 5 (mod 8): {to_5}")
print(f"  Ratio: {to_1}/{to_5} = {to_1/to_5:.3f}")
print()

print("="*80)
print("\nCONCLUSION:")
print("Half of n ≡ 7 (mod 8) escape to 3 (mod 8).")
print("And ALL n ≡ 3 (mod 8) escape to {1, 5} (mod 8), which decrease!")
print()
print("This suggests: trajectories CANNOT stay in {3,7} (mod 8) forever.")
print("They must eventually hit {1,5} (mod 8) and decrease.")
