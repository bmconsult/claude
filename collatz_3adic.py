#!/usr/bin/env python3
"""
3-adic analysis: Looking at the problem through powers of 3
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

def collatz_trajectory(n, max_steps=1000):
    """Return full Collatz trajectory"""
    traj = [n]
    while n != 1 and len(traj) < max_steps:
        n = n // 2 if n % 2 == 0 else 3*n + 1
        traj.append(n)
    return traj

def count_operations(n):
    """
    Count number of multiplications by 3 vs divisions by 2
    Returns (num_3x, num_div2, total_div2_power)
    """
    traj = collatz_trajectory(n)

    num_3x = 0
    num_div2 = 0
    total_div2_power = 0

    current = n
    for next_val in traj[1:]:
        if current % 2 == 1:
            # Odd -> 3n+1
            num_3x += 1
            temp = 3*current + 1
            k = v2(temp)
            num_div2 += k
            total_div2_power += k
        else:
            # Even -> n/2
            num_div2 += 1
            total_div2_power += 1

        current = next_val

    return (num_3x, num_div2, total_div2_power)

print("Operation Count Analysis")
print("="*80)
print("Comparing number of ×3 operations vs ÷2 operations")
print()
print("n\t×3\t÷2\ttotal 2^k\tratio (÷2/×3)\t3^(×3) / 2^(÷2)")
print("-"*80)

for n in [3, 7, 15, 27, 31, 47, 63, 71, 91, 103, 127, 255, 447, 703]:
    num_3x, num_div2, total_pow2 = count_operations(n)
    ratio = num_div2 / num_3x if num_3x > 0 else float('inf')

    # After num_3x multiplications by 3 and total_pow2 divisions by powers of 2
    # we have approximately: n * 3^num_3x / 2^total_pow2
    # For convergence, we need 3^num_3x / 2^total_pow2 to shrink to near 0

    magnitude_ratio = (3**num_3x) / (2**total_pow2)

    print(f"{n}\t{num_3x}\t{num_div2}\t{total_pow2}\t\t{ratio:.3f}\t\t{magnitude_ratio:.6e}")

print("\n" + "="*80)
print("\nKEY INSIGHT:")
print("For trajectory to reach 1, we need:")
print("  n * 3^(num_3x) / 2^(total_pow2) = 1")
print("  => 2^(total_pow2) = n * 3^(num_3x)")
print("  => total_pow2 * log(2) = log(n) + num_3x * log(3)")
print("  => total_pow2 = log(n)/log(2) + num_3x * log(3)/log(2)")
print("  => total_pow2 ≈ log₂(n) + 1.585 * num_3x")
print()
print("So we need: (÷2 power) > 1.585 * (×3 count)")
print()

# Empirical check
print("Empirical verification:")
print("n\tnum_3x\ttotal_pow2\ttheoretical\ttheory - actual")
print("-"*80)

for n in [3, 7, 15, 27, 31, 47, 63, 71, 91, 103]:
    num_3x, num_div2, total_pow2 = count_operations(n)
    theoretical = math.log2(n) + 1.585 * num_3x
    diff = theoretical - total_pow2

    print(f"{n}\t{num_3x}\t{total_pow2}\t\t{theoretical:.2f}\t\t{diff:.2f}")

print("\n" + "="*80)
print("\nCRITICAL QUESTION:")
print("Why does total_pow2 EXCEED 1.585 * num_3x + log₂(n)?")
print()
print("This is the HEART of the Collatz conjecture!")
print("We need to prove that v₂(3n+1) is 'large enough' on average.")
print()

# Statistical analysis of v₂(3n+1)
print("Distribution of v₂(3n+1) for odd n:")
print()

v2_samples = []
for n in range(1, 1001, 2):  # Odd numbers
    v2_samples.append(v2(3*n + 1))

from collections import Counter
v2_dist = Counter(v2_samples)

total = len(v2_samples)
print("v₂(3n+1)\tcount\tprobability\tcumulative")
print("-"*60)

cumulative = 0
for k in sorted(v2_dist.keys()):
    count = v2_dist[k]
    prob = count / total
    cumulative += prob
    print(f"{k}\t\t{count}\t{prob:.4f}\t\t{cumulative:.4f}")

# Expected value
expected_v2 = sum(k * count for k, count in v2_dist.items()) / total
print(f"\nExpected value of v₂(3n+1) = {expected_v2:.4f}")
print(f"This is {'>' if expected_v2 > 1.585 else '<='} 1.585")

if expected_v2 > 1.585:
    print("\n*** CRITICAL FINDING ***")
    print(f"E[v₂(3n+1)] = {expected_v2:.4f} > log₂(3) ≈ 1.585")
    print("This means ON AVERAGE, each ×3 step is MORE than compensated by ÷2 steps!")
    print("This is the empirical core of why Collatz works!")
