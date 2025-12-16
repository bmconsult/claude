#!/usr/bin/env python3
"""
Deep analysis of why n=27 is a problematic case for most invariants.
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

def collatz_trajectory(n, steps=50):
    """Generate Collatz trajectory"""
    traj = [n]
    for _ in range(steps):
        if n == 1:
            break
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        traj.append(n)
    return traj

def odd_to_odd_trajectory(n, steps=20):
    """Generate odd-to-odd trajectory with statistics"""
    traj = []
    for _ in range(steps):
        if n == 1:
            traj.append((n, 0, 1))
            break
        m = 3 * n + 1
        k = v2(m)
        next_odd = m // (2**k)
        traj.append((n, k, next_odd))
        n = next_odd
    return traj

print("=" * 70)
print("DETAILED ANALYSIS: Why n=27 breaks simple invariants")
print("=" * 70)

# Full Collatz trajectory
print("\nFull Collatz trajectory for n=27:")
traj = collatz_trajectory(27, 100)
print(f"Length to reach 1: {len(traj)}")
print(f"First 30 steps: {traj[:30]}")
print(f"Max value reached: {max(traj)}")

# Odd-to-odd trajectory
print("\n" + "-" * 70)
print("Odd-to-odd trajectory (showing v₂ values):")
print(f"{'n':>6} → {'v₂(3n+1)':>10} → {'g(n)':>6}  | {'Ratio g(n)/n':>12}")
print("-" * 70)

odd_traj = odd_to_odd_trajectory(27, 15)
for n, k, next_odd in odd_traj:
    ratio = next_odd / n if n > 0 else 0
    print(f"{n:>6} → {k:>10} → {next_odd:>6}  | {ratio:>12.4f}")

# Statistics
print("\n" + "=" * 70)
print("STATISTICS:")
print("=" * 70)

v2_values = [k for _, k, _ in odd_traj if _ != 1]
odds = [n for n, _, _ in odd_traj]

print(f"Average v₂(3n+1): {sum(v2_values) / len(v2_values):.3f}")
print(f"Min v₂: {min(v2_values)}, Max v₂: {max(v2_values)}")
print(f"Number of times v₂ = 1: {v2_values.count(1)}")
print(f"Number of times v₂ ≥ 2: {sum(1 for k in v2_values if k >= 2)}")

# Compute cumulative product to see overall drift
print("\n" + "-" * 70)
print("Cumulative ratio analysis:")
cumulative = 1.0
for i, (n, k, next_odd) in enumerate(odd_traj):
    if n == 1:
        break
    ratio = next_odd / n
    cumulative *= ratio
    expected_avg = (3 / 4) ** (i + 1)  # If average v₂ = 2
    print(f"Step {i+1}: ratio={ratio:.4f}, cumulative={cumulative:.4f}, " f"expected(3/4)^{i+1}={expected_avg:.4f}")

# Now test different potential functions on this trajectory
print("\n" + "=" * 70)
print("TESTING POTENTIAL FUNCTIONS ON n=27 TRAJECTORY:")
print("=" * 70)

def test_phi_on_trajectory(phi_func, name, n=27, full_traj=True):
    """Test if phi decreases within K steps"""
    if full_traj:
        traj = collatz_trajectory(n, 100)
    else:
        # Odd trajectory
        traj = [n for n, _, _ in odd_to_odd_trajectory(n, 20)]

    phi_0 = phi_func(n)
    decreases = []

    for i, m in enumerate(traj[1:], 1):
        phi_m = phi_func(m)
        if phi_m < phi_0:
            decreases.append((i, m, phi_0, phi_m))
            break

    if decreases:
        i, m, phi_0, phi_m = decreases[0]
        print(f"{name:30s}: DECREASE at step {i:3d}, "
              f"φ({n})={phi_0:8.3f} → φ({m})={phi_m:8.3f}")
        return i
    else:
        print(f"{name:30s}: NO DECREASE in {len(traj)} steps!")
        return None

# Test various functions
import math

phi_funcs = [
    ("n", lambda n: float(n)),
    ("log(n)", lambda n: math.log(n) if n > 0 else 0),
    ("n / (n mod 8 weight)", lambda n: n / {0:1, 1:4, 2:1, 3:2, 4:1, 5:4, 6:1, 7:2}[n % 8]),
]

for name, func in phi_funcs:
    test_phi_on_trajectory(func, name, n=27)

# The key question: what's the LONGEST we need to wait for ANY n?
print("\n" + "=" * 70)
print("MAXIMUM STEPS TO DECREASE:")
print("=" * 70)

def find_max_steps_to_decrease(phi_func, max_n=1000, max_steps=100):
    """Find the worst case: maximum steps before decrease"""
    worst_n = None
    worst_k = 0

    for n in range(2, max_n):
        phi_n = phi_func(n)
        traj = collatz_trajectory(n, max_steps)

        found = False
        for k, m in enumerate(traj[1:], 1):
            if phi_func(m) < phi_n:
                if k > worst_k:
                    worst_k = k
                    worst_n = n
                found = True
                break

        if not found and n == traj[-1]:  # Didn't decrease and didn't reach 1
            print(f"  WARNING: n={n} didn't decrease in {max_steps} steps!")

    return worst_n, worst_k

print("\nTesting φ(n) = n:")
worst_n, worst_k = find_max_steps_to_decrease(lambda n: float(n), max_n=1000)
if worst_n:
    print(f"  Worst case: n={worst_n} needs {worst_k} steps to decrease")
    traj = collatz_trajectory(worst_n, worst_k + 5)
    print(f"  Trajectory: {traj[:worst_k+2]}")
