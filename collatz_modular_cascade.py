#!/usr/bin/env python3
"""
Analyze the modular cascade: what happens when we apply T repeatedly?
"""

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
    """Map odd numbers to odd numbers"""
    assert n % 2 == 1
    m = 3*n + 1
    return m // (2**v2(m))

def analyze_mod_cascade(n, max_steps=20):
    """Track how n mod various moduli evolves under T"""
    trajectory = [n]
    current = n

    for _ in range(max_steps):
        if current == 1:
            break
        current = T(current)
        trajectory.append(current)

    return trajectory

# Focus on n ≡ 3 (mod 4) since these increase under T
print("Analyzing n ≡ 3 (mod 4):")
print("="*60)

for start_n in [3, 7, 11, 15, 19, 23, 27]:
    traj = analyze_mod_cascade(start_n, max_steps=10)
    print(f"\nn = {start_n}:")
    print(f"  Trajectory: {traj}")

    # Check modulo 8
    mods_8 = [x % 8 for x in traj]
    print(f"  mod 8:      {mods_8}")

    # Check if eventually decreases
    for i in range(len(traj)-1):
        if traj[i+1] < traj[i]:
            print(f"  First decrease at step {i}: {traj[i]} -> {traj[i+1]}")
            break

print("\n" + "="*60)
print("\nPattern investigation:")
print("If n ≡ 3 (mod 4), then T(n) = (3n+1)/2")
print("What is T(n) mod 4?")
print()

for n in range(3, 40, 4):  # n ≡ 3 (mod 4)
    Tn = T(n)
    print(f"n={n:2d}: T(n)={Tn:3d}, T(n) ≡ {Tn % 4} (mod 4), T(n) ≡ {Tn % 8} (mod 8)")

print("\n" + "="*60)
print("\nREVELATION CHECK:")
print("If n ≡ 3 (mod 8), what is (3n+1)/2?")
print()

for n in range(3, 40, 8):  # n ≡ 3 (mod 8)
    result = (3*n + 1) // 2
    print(f"n={n:2d} ≡ 3 (mod 8): (3n+1)/2 = {result:3d} ≡ {result % 8} (mod 8)")

print("\nIf n ≡ 7 (mod 8), what is (3n+1)/2?")
for n in range(7, 40, 8):  # n ≡ 7 (mod 8)
    result = (3*n + 1) // 2
    print(f"n={n:2d} ≡ 7 (mod 8): (3n+1)/2 = {result:3d} ≡ {result % 8} (mod 8)")

print("\n" + "="*60)
print("\nDeriving the pattern algebraically:")
print()
print("If n = 8k + 3:")
print("  3n+1 = 24k + 10 = 2(12k + 5)")
print("  T(n) = 12k + 5 ≡ 5 (mod 8)")
print()
print("If n = 8k + 7:")
print("  3n+1 = 24k + 22 = 2(12k + 11)")
print("  T(n) = 12k + 11 ≡ 3 (mod 8)")
print()

print("So the map on residue classes mod 8 is:")
print("  3 -> 5")
print("  7 -> 3")
print()
print("This forms a cycle: 3 -> 5 -> ? and 7 -> 3 -> 5 -> ?")
print()

# What about 5 mod 8?
print("If n = 8k + 5:")
print("  3n+1 = 24k + 16 = 16(3k/2 + 1)")
print("  v₂(3n+1) = 4")
print("  T(n) = (24k + 16)/16 = (3k + 2)/... wait, need k even/odd")
print()

for n in range(5, 40, 8):  # n ≡ 5 (mod 8)
    Tn = T(n)
    v = v2(3*n+1)
    print(f"n={n:2d} ≡ 5 (mod 8): T(n) = {Tn:3d}, v₂(3n+1) = {v}")

print("\n" + "="*60)
print("\nComplete residue class dynamics for odd numbers mod 8:")
print()

for r in [1, 3, 5, 7]:
    print(f"n ≡ {r} (mod 8):")
    examples = []
    for n in range(r, min(r+64, 100), 8):
        Tn = T(n)
        v = v2(3*n+1)
        examples.append((n, Tn, Tn % 8, v))

    # Show first 3 examples
    for n, Tn, Tn_mod8, v in examples[:3]:
        print(f"  n={n:2d}: T(n)={Tn:3d} ≡ {Tn_mod8} (mod 8), v₂={v}")

    # Check if pattern is consistent
    Tn_mods = [ex[2] for ex in examples]
    if len(set(Tn_mods)) == 1:
        print(f"  -> T(n) ≡ {Tn_mods[0]} (mod 8) ALWAYS")
    else:
        print(f"  -> T(n) mod 8 varies: {set(Tn_mods)}")
    print()
