#!/usr/bin/env python3
"""
Entropy-Based Analysis of Collatz Conjecture
Agent 13: Creative Wanderer (Zephyr)

Idea: View Collatz through thermodynamic lens
"""

def T(n):
    """Collatz map for odd numbers."""
    if n % 2 == 0:
        raise ValueError("n must be odd")
    return (3*n + 1) // (2 ** v2(3*n + 1))

def v2(n):
    """2-adic valuation: highest power of 2 dividing n."""
    if n == 0:
        return float('inf')
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k

def binary_transitions(n):
    """Count number of '10' transitions in binary representation."""
    b = bin(n)[2:]  # Remove '0b' prefix
    transitions = 0
    for i in range(len(b) - 1):
        if b[i] == '1' and b[i+1] == '0':
            transitions += 1
    return transitions

def bit_entropy(n):
    """Simple bit entropy: proportion of 1s."""
    b = bin(n)[2:]
    ones = b.count('1')
    return ones / len(b)

def analyze_entropy_trajectory(n_start, max_steps=100):
    """Analyze entropy evolution along Collatz trajectory."""
    n = n_start
    if n % 2 == 0:
        n = n // 2

    trajectory = []
    for step in range(max_steps):
        trans = binary_transitions(n)
        ent = bit_entropy(n)
        trajectory.append({
            'n': n,
            'step': step,
            'transitions': trans,
            'entropy': ent,
            'mod4': n % 4
        })

        if n == 1:
            break

        n = T(n)

    return trajectory

def find_entropy_invariant():
    """Search for entropy-based invariant."""
    print("=== ENTROPY-BASED COLLATZ ANALYSIS ===\n")

    # Test multiple starting points
    test_values = [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 27, 31, 63, 127, 255]

    for n_start in test_values:
        traj = analyze_entropy_trajectory(n_start)

        print(f"\nn = {n_start} (binary: {bin(n_start)})")
        print(f"{'Step':<6} {'n':<8} {'Binary':<16} {'Trans':<7} {'Entropy':<8} {'Mod4'}")
        print("-" * 60)

        for t in traj[:10]:  # Show first 10 steps
            b = bin(t['n'])[2:]
            print(f"{t['step']:<6} {t['n']:<8} {b:<16} {t['transitions']:<7} {t['entropy']:<8.3f} {t['mod4']}")

        if len(traj) > 10:
            print(f"... ({len(traj)} total steps to reach 1)")

    # Look for patterns
    print("\n\n=== ENTROPY EVOLUTION PATTERNS ===\n")

    # Does entropy decrease on average?
    all_entropy_changes = []

    for n_start in range(3, 100, 2):
        traj = analyze_entropy_trajectory(n_start)
        if len(traj) > 1:
            initial_ent = traj[0]['entropy']
            final_ent = traj[-1]['entropy']
            avg_ent = sum(t['entropy'] for t in traj) / len(traj)
            all_entropy_changes.append({
                'n': n_start,
                'initial': initial_ent,
                'final': final_ent,
                'avg': avg_ent,
                'change': final_ent - initial_ent
            })

    # Statistics
    avg_change = sum(ec['change'] for ec in all_entropy_changes) / len(all_entropy_changes)
    decreasing = sum(1 for ec in all_entropy_changes if ec['change'] < 0)

    print(f"Tested {len(all_entropy_changes)} odd numbers")
    print(f"Average entropy change: {avg_change:.4f}")
    print(f"Trajectories with decreasing entropy: {decreasing}/{len(all_entropy_changes)} ({100*decreasing/len(all_entropy_changes):.1f}%)")

    # Find trajectories with increasing entropy
    print("\n=== TRAJECTORIES WITH INCREASING ENTROPY ===")
    increasing = [ec for ec in all_entropy_changes if ec['change'] > 0]
    for ec in increasing[:10]:
        print(f"n = {ec['n']:3d}: {ec['initial']:.3f} → {ec['final']:.3f} (Δ = {ec['change']:+.3f})")

if __name__ == "__main__":
    find_entropy_invariant()
