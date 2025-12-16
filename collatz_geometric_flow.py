#!/usr/bin/env python3
"""
Geometric Flow Approach to Collatz
Agent 13: Creative Wanderer (Zephyr)

Embed Collatz in continuous geometry and analyze as a flow
"""

import math
import statistics

def v2(n):
    """2-adic valuation."""
    if n == 0:
        return float('inf')
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k

def T(n):
    """Collatz map for odd n."""
    return (3*n + 1) // (2 ** v2(3*n + 1))

def potential_function(n, alpha=1.5):
    """
    Φ(n) = log₂(n) - α·v₂(3n+1)

    This should decrease on average if α is chosen correctly.
    """
    if n % 2 == 0:
        raise ValueError("n must be odd")
    return math.log2(n) - alpha * v2(3*n + 1)

def find_optimal_alpha():
    """Find α that maximizes descent in Φ."""
    print("=== FINDING OPTIMAL ALPHA FOR POTENTIAL FUNCTION ===\n")

    alphas = [0.5 + i * 0.1 for i in range(26)]
    results = []

    for alpha in alphas:
        decreases = 0
        total = 0

        for n in range(3, 1000, 2):
            phi_n = potential_function(n, alpha)
            n_next = T(n)
            if n_next > 1:
                phi_next = potential_function(n_next, alpha)
                if phi_next < phi_n:
                    decreases += 1
                total += 1

        decrease_rate = decreases / total if total > 0 else 0
        results.append((alpha, decrease_rate))

        if alpha in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
            print(f"α = {alpha:.2f}: Φ decreases {decrease_rate:.3f} of the time")

    # Find best alpha
    best_alpha, best_rate = max(results, key=lambda x: x[1])
    print(f"\nOptimal α = {best_alpha:.3f} (decreases {best_rate:.3f} of the time)")

    return best_alpha, results

def analyze_geometric_flow(alpha):
    """Analyze Collatz as a flow with potential Φ."""
    print(f"\n\n=== GEOMETRIC FLOW ANALYSIS (α = {alpha:.3f}) ===\n")

    # Analyze specific trajectories
    test_values = [3, 7, 15, 27, 31, 63, 127]

    for n_start in test_values:
        n = n_start
        traj = []

        while n != 1 and len(traj) < 50:
            phi = potential_function(n, alpha)
            traj.append((n, phi))
            n = T(n)

        print(f"\nn = {n_start}")
        print(f"{'Step':<6} {'n':<8} {'Φ(n)':<10} {'ΔΦ':<10} {'Mod 4'}")
        print("-" * 50)

        for i, (n, phi) in enumerate(traj[:15]):
            if i > 0:
                delta_phi = phi - traj[i-1][1]
            else:
                delta_phi = 0

            print(f"{i:<6} {n:<8} {phi:<10.3f} {delta_phi:+10.3f} {n % 4}")

        if len(traj) > 15:
            print(f"... ({len(traj)} steps shown)")

        # Check if Φ is bounded below
        min_phi = min(phi for _, phi in traj)
        max_phi = max(phi for _, phi in traj)
        print(f"Φ range: [{min_phi:.3f}, {max_phi:.3f}]")

    # Statistical analysis
    print("\n\n=== STATISTICAL ANALYSIS ===\n")

    phi_changes = []
    for n in range(3, 1000, 2):
        if n == 1:
            continue
        phi_n = potential_function(n, alpha)
        n_next = T(n)
        if n_next > 1:
            phi_next = potential_function(n_next, alpha)
            phi_changes.append(phi_next - phi_n)

    avg_change = statistics.mean(phi_changes)
    std_change = statistics.stdev(phi_changes)
    min_change = min(phi_changes)
    max_change = max(phi_changes)

    print(f"Average ΔΦ: {avg_change:.4f}")
    print(f"Std dev ΔΦ: {std_change:.4f}")
    print(f"Range: [{min_change:.4f}, {max_change:.4f}]")

    # Count increases
    increases = sum(1 for x in phi_changes if x > 0)
    decreases = sum(1 for x in phi_changes if x < 0)
    print(f"\nIncreases: {increases}/{len(phi_changes)} ({100*increases/len(phi_changes):.1f}%)")
    print(f"Decreases: {decreases}/{len(phi_changes)} ({100*decreases/len(phi_changes):.1f}%)")

    # Histogram data (without plotting)
    print("\n[Histogram of ΔΦ would show distribution around mean]")

    return phi_changes

def curvature_analysis():
    """Analyze 'curvature' of Collatz flow."""
    print("\n\n=== CURVATURE ANALYSIS ===\n")
    print("Measuring 'curvature' as second-order changes in trajectory\n")

    # For each n, compute T(n) and T(T(n)), measure 'curvature'
    # κ(n) = log(T(T(n))) - 2*log(T(n)) + log(n)

    curvatures = []
    for n in range(3, 500, 2):
        if n == 1:
            continue

        n1 = T(n)
        if n1 == 1:
            continue

        n2 = T(n1)
        if n2 == 1:
            continue

        # Logarithmic second derivative
        kappa = math.log(n2) - 2*math.log(n1) + math.log(n)
        curvatures.append((n, kappa, n % 4))

    # Separate by mod 4
    kappa_mod1 = [k for n, k, m in curvatures if m == 1]
    kappa_mod3 = [k for n, k, m in curvatures if m == 3]

    print(f"Mod 1 curvature: mean = {statistics.mean(kappa_mod1):.4f}, std = {statistics.stdev(kappa_mod1):.4f}")
    print(f"Mod 3 curvature: mean = {statistics.mean(kappa_mod3):.4f}, std = {statistics.stdev(kappa_mod3):.4f}")

    print("\n[Curvature scatter plot would show mod 1 vs mod 3 patterns]")

if __name__ == "__main__":
    # Find optimal alpha
    best_alpha, alpha_results = find_optimal_alpha()

    # Analyze with optimal alpha
    phi_changes = analyze_geometric_flow(best_alpha)

    # Curvature analysis
    curvature_analysis()

    print("\n\n=== CONCLUSION ===")
    print("\nIf Φ(n) = log₂(n) - α·v₂(3n+1) with optimal α, we get:")
    print("- Φ decreases on average (drift toward lower potential)")
    print("- But some trajectories have Φ increases (local maxima)")
    print("- This is similar to a diffusion process with drift")
    print("\nQuestion: Can we prove Φ is bounded below for all trajectories?")
    print("If yes, bounded + average decrease → eventual descent")
