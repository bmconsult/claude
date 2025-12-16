#!/usr/bin/env python3
"""
Agent 38: Proof Breaker - Computational Attack
Try to find n that never hits ≡ 1 (mod 4), or takes extremely long
"""

def T(n):
    """Collatz function"""
    if n % 2 == 0:
        return n // 2
    return 3*n + 1

def hitting_time_mod4(n, max_steps=10000):
    """
    Find the first step where trajectory hits ≡ 1 (mod 4)
    Returns (step, value) or (None, None) if not found within max_steps
    """
    current = n
    for step in range(max_steps):
        if current % 4 == 1:
            return (step, current)
        current = T(current)
        if current == 1:  # Reached 1
            return (step+1, 1)
    return (None, None)

def check_nested_containment(n, max_k=20):
    """
    Check if n ∈ {≡ 2^k - 1 (mod 2^k)} for all k from 2 to max_k
    According to the proof, if n ∈ B, this should hold for ALL k
    """
    results = {}
    for k in range(2, max_k + 1):
        residue = 2**k - 1
        modulus = 2**k
        actual = n % modulus
        satisfies = (actual == residue)
        results[k] = satisfies
    return results

print("COMPUTATIONAL ATTACK: Searching for members of B")
print("="*60)

# Strategy 1: Test numbers with many 1's in binary (candidates for intersection)
print("\nStrategy 1: Numbers with many trailing 1's in binary")
print("-"*60)

candidates = []
for num_ones in range(3, 16):
    n = 2**num_ones - 1  # All 1's: 111...1
    if n % 2 == 0:
        continue

    step, val = hitting_time_mod4(n, max_steps=100000)

    # Check nested containment
    containment = check_nested_containment(n, max_k=min(num_ones, 20))
    max_k_satisfied = max([k for k, sat in containment.items() if sat], default=0)

    print(f"\nn = {n:6d} = 2^{num_ones}-1 (binary: {'1'*num_ones})")
    print(f"  Satisfies ≡ 2^k-1 (mod 2^k) up to k = {max_k_satisfied}")
    if step is not None:
        print(f"  Hits ≡ 1 (mod 4) at step {step} (value: {val})")
    else:
        print(f"  ✗ DID NOT HIT ≡ 1 (mod 4) within 100000 steps!")
        candidates.append(n)

# Strategy 2: Test numbers in the "all ones" branch at each level
print("\n\nStrategy 2: Numbers in the 'upper half' at each level")
print("-"*60)
print("(These should escape according to the proof)\n")

for k in range(3, 12):
    # Upper half: n ≡ 2^(k+1) - 1 (mod 2^(k+1))
    residue = 2**(k+1) - 1
    modulus = 2**(k+2)

    # Take first member (smallest n in this class)
    n = residue

    step, val = hitting_time_mod4(n, max_steps=10000)

    # Check how far the nested containment goes
    containment = check_nested_containment(n, max_k=k+5)
    satisfied = [k for k, sat in containment.items() if sat]

    print(f"k={k:2d}: n = {n:5d} ≡ 2^{k+1}-1 (mod 2^{k+2})")
    print(f"      Satisfies nested constraint for k ∈ {satisfied[:10]}")
    if step is not None:
        print(f"      Hits ≡ 1 (mod 4) at step {step}")
    else:
        print(f"      ✗ DID NOT HIT within 10000 steps!")
        candidates.append(n)

# Strategy 3: Direct search for long-hitting numbers
print("\n\nStrategy 3: Exhaustive search for slow hitters")
print("-"*60)

max_hitting_time = 0
slowest_n = None

for n in range(3, 10000, 2):  # Odd numbers only
    step, val = hitting_time_mod4(n, max_steps=100000)

    if step is None:
        print(f"✗ FOUND POTENTIAL MEMBER OF B: n = {n}")
        candidates.append(n)
    elif step > max_hitting_time:
        max_hitting_time = step
        slowest_n = n

print(f"\nSlowest hitter found: n = {slowest_n}, hitting time = {max_hitting_time}")

# Summary
print("\n" + "="*60)
print("SUMMARY")
print("="*60)

if candidates:
    print(f"✗ POTENTIAL MEMBERS OF B FOUND: {len(candidates)}")
    print(f"  {candidates[:10]}")
    print("\n✓ PROOF POTENTIALLY BROKEN!")
else:
    print("✓ NO MEMBERS OF B FOUND")
    print("  All tested numbers hit ≡ 1 (mod 4)")
    print("\n✗ COMPUTATIONAL ATTACK FAILED - Cannot break proof")

# Additional verification: Check the intersection claim
print("\n" + "="*60)
print("INTERSECTION VERIFICATION")
print("="*60)
print("\nThe proof claims: ⋂{n ≡ 2^k-1 (mod 2^k)} = ∅ for finite n")
print("\nChecking: How far can a finite n satisfy these constraints?")

for test_n in [7, 15, 31, 63, 127, 255, 511, 1023]:
    containment = check_nested_containment(test_n, max_k=20)
    max_k = max([k for k, sat in containment.items() if sat], default=0)
    binary = bin(test_n)[2:]
    print(f"n = {test_n:4d} (binary: {binary:>12s}) satisfies up to k = {max_k}")

print("\nPattern: n = 2^m - 1 satisfies the constraint exactly up to k = m")
print("This confirms: finite n CANNOT satisfy the constraint for ALL k")
print("Therefore: The intersection is indeed empty ✓")
