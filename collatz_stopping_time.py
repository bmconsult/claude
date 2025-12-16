#!/usr/bin/env python3
"""
Stopping time analysis: How many steps to get below starting value?
"""

def collatz_step(n):
    return n // 2 if n % 2 == 0 else 3*n + 1

def steps_to_drop_below(n):
    """
    How many Collatz steps until we get a value < n?
    Returns (steps, minimum_reached)
    """
    original = n
    current = n
    steps = 0
    max_reached = n

    while current >= original:
        current = collatz_step(current)
        steps += 1
        max_reached = max(max_reached, current)

        if steps > 1000:  # Safety
            return (steps, current, max_reached)

    return (steps, current, max_reached)

print("Stopping Time Analysis")
print("="*70)
print("How many steps until trajectory drops below starting value?")
print()
print("n\tsteps\tfirst_below\tmax_reached\tmax/n ratio")
print("-"*70)

for n in range(2, 50):
    steps, first_below, max_reached = steps_to_drop_below(n)
    ratio = max_reached / n
    print(f"{n}\t{steps}\t{first_below}\t\t{max_reached}\t\t{ratio:.3f}")

print("\n" + "="*70)
print("\nStatistics on max_reached/n ratio:")

ratios = []
for n in range(2, 1000):
    steps, first_below, max_reached = steps_to_drop_below(n)
    ratios.append(max_reached / n)

import statistics
print(f"Mean ratio: {statistics.mean(ratios):.4f}")
print(f"Median ratio: {statistics.median(ratios):.4f}")
print(f"Max ratio: {max(ratios):.4f}")
print(f"Min ratio: {min(ratios):.4f}")

# Find worst cases
worst_cases = sorted([(n, ratios[n-2]) for n in range(2, 1000)],
                     key=lambda x: x[1], reverse=True)[:10]
print(f"\nWorst 10 cases (highest max/n):")
for n, ratio in worst_cases:
    steps, first_below, max_reached = steps_to_drop_below(n)
    print(f"  n={n}: max={max_reached}, ratio={ratio:.3f}, steps={steps}")

print("\n" + "="*70)
print("\nKey question: Is max/n bounded by a constant?")
print()

# Check if ratio grows with n
print("Checking if ratio grows with n...")
max_ratio_so_far = 0
growing_cases = []

for n in range(2, 10000):
    steps, first_below, max_reached = steps_to_drop_below(n)
    ratio = max_reached / n

    if ratio > max_ratio_so_far:
        max_ratio_so_far = ratio
        growing_cases.append((n, ratio, max_reached))

print(f"\nFound {len(growing_cases)} cases where ratio is a new maximum:")
for n, ratio, max_r in growing_cases[-20:]:  # Last 20
    print(f"  n={n}: ratio={ratio:.4f}, max={max_r}")

if growing_cases:
    final_max = growing_cases[-1][1]
    print(f"\nLargest ratio found: {final_max:.4f}")
    print(f"This suggests max/n is bounded (empirically < {final_max:.1f})")
