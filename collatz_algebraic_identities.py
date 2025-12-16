#!/usr/bin/env python3
"""
Algebraic Identity Approach to Collatz
Agent 13: Creative Wanderer (Zephyr)

Look for unexpected algebraic patterns in Collatz trajectories
"""

def collatz_trajectory(n):
    """Full Collatz trajectory from n to 1."""
    traj = []
    while n != 1:
        traj.append(n)
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3*n + 1
    traj.append(1)
    return traj

def trajectory_sum(n):
    """Sum of all values in trajectory."""
    return sum(collatz_trajectory(n))

def trajectory_product_of_odds(n):
    """Product of all odd values in trajectory (modulo large prime to avoid overflow)."""
    traj = collatz_trajectory(n)
    odds = [x for x in traj if x % 2 == 1]
    # Use modular arithmetic to avoid overflow
    p = 1000000007  # Large prime
    prod = 1
    for x in odds:
        prod = (prod * x) % p
    return prod, len(odds)

def analyze_trajectory_algebraics():
    """Look for algebraic patterns in trajectories."""
    print("=== ALGEBRAIC COLLATZ ANALYSIS ===\n")

    # Compute sums for various n
    print("Trajectory Sums:")
    print(f"{'n':<6} {'Sum':<10} {'Length':<8} {'Sum/n':<10} {'Sum/n²':<10}")
    print("-" * 60)

    for n in range(1, 30):
        s = trajectory_sum(n)
        length = len(collatz_trajectory(n)) - 1  # Don't count n itself
        ratio1 = s / n
        ratio2 = s / (n * n)
        print(f"{n:<6} {s:<10} {length:<8} {ratio1:<10.3f} {ratio2:<10.5f}")

    # Look for patterns in ratios
    print("\n\n=== RATIO ANALYSIS ===\n")

    ratios = []
    for n in range(3, 100, 2):  # Odd numbers
        s = trajectory_sum(n)
        length = len(collatz_trajectory(n)) - 1
        ratios.append({
            'n': n,
            'sum': s,
            'length': length,
            'sum_per_step': s / length if length > 0 else 0,
            'sum_per_n': s / n
        })

    # Find correlations
    avg_sum_per_step = sum(r['sum_per_step'] for r in ratios) / len(ratios)
    avg_sum_per_n = sum(r['sum_per_n'] for r in ratios) / len(ratios)

    print(f"Average sum per step: {avg_sum_per_step:.2f}")
    print(f"Average sum/n ratio: {avg_sum_per_n:.2f}")

    # Most interesting cases
    print("\n=== OUTLIERS ===\n")
    print("Highest sum/n ratios:")
    sorted_ratios = sorted(ratios, key=lambda r: r['sum_per_n'], reverse=True)
    for r in sorted_ratios[:10]:
        print(f"n = {r['n']:3d}: sum = {r['sum']:6d}, length = {r['length']:3d}, sum/n = {r['sum_per_n']:.2f}")

    # Look for patterns in mod 4
    print("\n\n=== MOD 4 PATTERNS ===\n")

    mod1_ratios = [r for r in ratios if r['n'] % 4 == 1]
    mod3_ratios = [r for r in ratios if r['n'] % 4 == 3]

    avg_mod1 = sum(r['sum_per_n'] for r in mod1_ratios) / len(mod1_ratios)
    avg_mod3 = sum(r['sum_per_n'] for r in mod3_ratios) / len(mod3_ratios)

    print(f"n ≡ 1 (mod 4): Average sum/n = {avg_mod1:.2f}")
    print(f"n ≡ 3 (mod 4): Average sum/n = {avg_mod3:.2f}")

    # Look for multiplicative structure
    print("\n\n=== MULTIPLICATIVE PATTERNS ===\n")

    for n in [3, 5, 7, 9, 15, 21, 27]:
        traj = collatz_trajectory(n)
        odds = [x for x in traj if x % 2 == 1]
        print(f"\nn = {n}")
        print(f"Odd values: {odds}")
        print(f"Product (mod 10^9+7): {trajectory_product_of_odds(n)[0]}")
        print(f"Number of odds: {len(odds)}")

    # Try to find a generating function pattern
    print("\n\n=== GENERATING FUNCTION EXPLORATION ===\n")

    # Can we find f(n) such that sum_trajectory relates to f?
    # Try: f(n) = a*n + b*log(n) + c
    # Fit to data

    import math

    data_points = []
    for n in range(3, 100, 2):
        s = trajectory_sum(n)
        data_points.append((n, math.log(n), s))

    # Simple linear regression for s ~ a*n + b*log(n)
    # Using least squares

    n_points = len(data_points)
    sum_n = sum(d[0] for d in data_points)
    sum_logn = sum(d[1] for d in data_points)
    sum_s = sum(d[2] for d in data_points)
    sum_n2 = sum(d[0]**2 for d in data_points)
    sum_logn2 = sum(d[1]**2 for d in data_points)
    sum_n_logn = sum(d[0]*d[1] for d in data_points)
    sum_n_s = sum(d[0]*d[2] for d in data_points)
    sum_logn_s = sum(d[1]*d[2] for d in data_points)

    # Matrix equation: [sum_n2, sum_n_logn] [a]   = [sum_n_s]
    #                  [sum_n_logn, sum_logn2] [b]   [sum_logn_s]

    det = sum_n2 * sum_logn2 - sum_n_logn**2
    if det != 0:
        a = (sum_n_s * sum_logn2 - sum_logn_s * sum_n_logn) / det
        b = (sum_n2 * sum_logn_s - sum_n_logn * sum_n_s) / det
        c = (sum_s - a * sum_n - b * sum_logn) / n_points

        print(f"Best fit: S(n) ≈ {a:.2f}*n + {b:.2f}*log(n) + {c:.2f}")

        # Test fit quality
        residuals = []
        for n, logn, s in data_points:
            predicted = a * n + b * logn + c
            residuals.append(abs(s - predicted))

        avg_residual = sum(residuals) / len(residuals)
        print(f"Average residual: {avg_residual:.2f}")

        print("\nSample predictions vs actual:")
        for n in [5, 15, 27, 49, 81]:
            s_actual = trajectory_sum(n)
            s_pred = a * n + b * math.log(n) + c
            print(f"n = {n:3d}: actual = {s_actual:6.0f}, predicted = {s_pred:6.0f}, error = {abs(s_actual - s_pred):6.0f}")


if __name__ == "__main__":
    analyze_trajectory_algebraics()
