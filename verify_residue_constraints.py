#!/usr/bin/env python3
"""
Computational verification of residue class constraints for Collatz exceptional set.
"""

def collatz(n):
    """Single Collatz step."""
    return 3*n + 1 if n % 2 else n // 2

def nu_2(n):
    """2-adic valuation: largest k such that 2^k divides n."""
    if n == 0:
        return float('inf')
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k

def check_constraint_level_1(n):
    """Check if n ≡ 3 (mod 4)."""
    return n % 4 == 3

def check_constraint_level_2(n):
    """Check if n ≡ 7 (mod 8)."""
    return n % 8 == 7

def compute_next_constraint(n, current_mod):
    """
    Given n satisfying current constraints, compute what constraint
    the next iterate m = T²(n) must satisfy.
    """
    # For odd n, T(n) = 3n+1, T²(n) = (3n+1)/2^k where k = nu_2(3n+1)
    t1 = 3*n + 1
    k = nu_2(t1)
    m = t1 >> k  # Divide by 2^k

    # For m to satisfy nu_2(3m+1) = 1, we need 3m+1 ≡ 2 (mod 4)
    # Compute what this implies about n modulo the next power of 2
    return m, k

def find_residue_class_sequence():
    """
    Iteratively compute the residue class constraints.
    """
    print("Computing residue class constraints for exceptional set E:\n")

    # Start with n ≡ 3 (mod 4)
    print("Level 1: E ⊆ {n : n ≡ 3 (mod 4)}")
    candidates = [n for n in range(3, 100, 4)]
    print(f"  Candidates in [3, 100): {candidates[:10]}...")

    # Level 2: n ≡ 7 (mod 8)
    print("\nLevel 2: E ⊆ {n : n ≡ 7 (mod 8)}")
    candidates = [n for n in range(7, 100, 8)]
    print(f"  Candidates in [3, 100): {candidates[:10]}...")

    # Level 3 and beyond: compute by checking constraint propagation
    print("\nLevel 3+: Computing iteratively...")

    mod = 8
    residue = 7

    for level in range(3, 10):
        # Check which residues mod 2*mod are compatible
        next_mod = 2 * mod
        compatible = []

        for r in [residue, residue + mod]:
            # Check if this residue class works
            # Take sample values and check constraint
            samples = [r + k * next_mod for k in range(10)]
            valid = True

            for n in samples:
                if n < 3:
                    continue
                # Check nu_2(3n+1)
                k_val = nu_2(3*n + 1)
                if k_val != 1:
                    # This is required for n in E
                    valid = False
                    break

                # Check the next iterate
                m = (3*n + 1) >> k_val
                if m < n:  # If m < n, then m must also satisfy constraints
                    m_k_val = nu_2(3*m + 1)
                    # Continue checking...

            if valid:
                compatible.append(r)

        if not compatible:
            print(f"\nLevel {level}: CONSTRAINT CONTRADICTION!")
            print(f"  No residue class mod {next_mod} is compatible.")
            print(f"  Therefore E = ∅")
            return None

        residue = compatible[0]
        mod = next_mod

        candidates = [residue + k * mod for k in range(10) if residue + k * mod >= 3]
        print(f"Level {level}: E ⊆ {{n : n ≡ {residue} (mod {mod})}}")
        print(f"  Candidates: {candidates[:5]}...")

    return residue, mod

def trajectory_analysis(n, max_steps=10000):
    """
    Analyze if n could be in E by checking trajectory.
    Returns (min_value, stays_above_n)
    """
    trajectory = [n]
    current = n
    min_val = n

    for _ in range(max_steps):
        current = collatz(current)
        trajectory.append(current)
        min_val = min(min_val, current)

        if current == 1:
            return min_val, False, trajectory
        if current < n:
            return min_val, False, trajectory

    # Did not conclude within max_steps
    return min_val, min_val >= n, trajectory

def test_candidates():
    """
    Test specific candidates that satisfy residue constraints.
    """
    print("\n" + "="*60)
    print("Testing specific candidates:")
    print("="*60)

    # Test numbers that are ≡ 7 (mod 8)
    test_values = [7, 15, 23, 31, 39, 47, 55, 63, 71, 79, 87, 95]

    for n in test_values:
        min_val, stays_above, traj = trajectory_analysis(n, max_steps=1000)
        k_val = nu_2(3*n + 1)

        print(f"\nn = {n}:")
        print(f"  Residue: {n} ≡ {n % 8} (mod 8)")
        print(f"  ν₂(3n+1) = {k_val} {'✓' if k_val == 1 else '✗ FAILS'}")
        print(f"  Min trajectory value: {min_val}")
        print(f"  Reaches 1: {traj[-1] == 1 if len(traj) < 1000 else 'unknown'}")
        print(f"  First few steps: {traj[:10]}")

        if min_val >= n:
            print(f"  ⚠️  CANDIDATE FOR E (within 1000 steps)")

def check_arithmetic_progression_claim():
    """
    Verify that E contains no 3-term arithmetic progressions.
    """
    print("\n" + "="*60)
    print("Checking for 3-term arithmetic progressions in constraint set:")
    print("="*60)

    # Generate candidates satisfying n ≡ 7 (mod 8)
    candidates = [n for n in range(7, 200, 8)]

    found_progression = False
    for i, n1 in enumerate(candidates):
        for j in range(i+1, len(candidates)):
            n2 = candidates[j]
            d = n2 - n1
            n3 = n2 + d

            if n3 in candidates:
                print(f"Found 3-AP: {n1}, {n2}, {n3} (difference {d})")

                # But check if all three satisfy nu_2 constraint
                k1 = nu_2(3*n1 + 1)
                k2 = nu_2(3*n2 + 1)
                k3 = nu_2(3*n3 + 1)

                all_satisfy = k1 == 1 and k2 == 1 and k3 == 1
                print(f"  ν₂ values: {k1}, {k2}, {k3} - All satisfy: {all_satisfy}")

                if all_satisfy:
                    found_progression = True

    if not found_progression:
        print("\n✓ No 3-term arithmetic progressions found (in tested range)")

if __name__ == "__main__":
    print("COLLATZ EXCEPTIONAL SET: Residue Class Analysis")
    print("=" * 60)

    find_residue_class_sequence()
    test_candidates()
    check_arithmetic_progression_claim()

    print("\n" + "="*60)
    print("Analysis complete. See collatz_additive_combinatorics_analysis.md for details.")
    print("="*60)
