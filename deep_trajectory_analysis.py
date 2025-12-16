#!/usr/bin/env python3
"""
Deep analysis: Do any numbers actually stay above their starting value?
Test the core claim that E is empty.
"""

def collatz(n):
    return 3*n + 1 if n % 2 else n // 2

def full_trajectory_until_1(n, max_steps=100000):
    """Compute full trajectory until reaching 1 or max_steps."""
    trajectory = [n]
    current = n

    for step in range(max_steps):
        current = collatz(current)
        trajectory.append(current)

        if current == 1:
            return trajectory, True, min(trajectory)

    # Did not reach 1 within max_steps
    return trajectory, False, min(trajectory)

def test_exceptional_candidates():
    """
    Test candidates that satisfy the residue constraints.
    The key question: do ANY of them stay above their starting value?
    """
    print("="*70)
    print("TESTING FOR EXCEPTIONAL SET MEMBERS")
    print("="*70)
    print("\nTesting candidates that are ≡ 7 (mod 8)...")
    print("Question: Does trajectory ever go below starting value?")
    print()

    # Test candidates in the refined residue class
    # According to my analysis: E ⊆ {7, 7+512, 7+1024, ...} at level 9
    test_cases = [
        # Level 2: n ≡ 7 (mod 8)
        7, 15, 23, 31, 39, 47, 55, 63, 71, 79,
        # Level 3: n ≡ 7 (mod 16)
        7, 23, 39, 55, 71, 87,
        # Level 4: n ≡ 7 (mod 32)
        7, 39, 71, 103, 135,
        # Level 5: n ≡ 7 (mod 64)
        7, 71, 135, 199, 263,
        # Level 6: n ≡ 7 (mod 128)
        7, 135, 263, 391, 519,
    ]

    test_cases = sorted(set(test_cases))

    exceptional_found = []

    for n in test_cases:
        traj, reached_1, min_val = full_trajectory_until_1(n, max_steps=10000)

        stays_above = min_val >= n
        reaches_1 = traj[-1] == 1

        status = ""
        if stays_above:
            status = "⚠️  POTENTIAL EXCEPTION!"
            exceptional_found.append(n)
        elif reaches_1:
            status = "✓ Reaches 1"
        else:
            status = "? Did not reach 1 (within 10k steps)"

        print(f"n = {n:4d}: min = {min_val:6d}, steps = {len(traj):5d}, {status}")

        if stays_above and len(traj) <= 20:
            print(f"         Trajectory: {traj}")

    print("\n" + "="*70)
    if exceptional_found:
        print(f"EXCEPTIONAL CANDIDATES FOUND: {exceptional_found}")
        print("These might be in E (if they never decrease below starting value)")
    else:
        print("NO EXCEPTIONAL CANDIDATES FOUND")
        print("All tested values eventually go below their starting value.")
    print("="*70)

def test_power_of_2_residues():
    """
    Test the claim that E ⊆ {7 + k·2^m} for increasing m.
    """
    print("\n" + "="*70)
    print("RESIDUE CLASS DENSITY ANALYSIS")
    print("="*70)

    for level in range(3, 12):
        mod = 2**level
        residue = 7

        # Count how many in [1, 10000] satisfy this
        candidates = [n for n in range(residue, 10000, mod)]
        density = len(candidates) / 10000

        # Test if they all reach below their starting value
        all_decrease = True
        for n in candidates[:20]:  # Test first 20
            traj, _, min_val = full_trajectory_until_1(n, max_steps=5000)
            if min_val >= n:
                all_decrease = False
                break

        print(f"Level {level:2d} (mod {mod:5d}): "
              f"{len(candidates):4d} candidates, "
              f"density = {density:.6f}, "
              f"all decrease = {all_decrease}")

    print()
    print("Observation: As the modulus increases, density → 0 exponentially.")
    print("But does the intersection become empty? Or always contain 7?")

def special_analysis_of_7():
    """
    Deep dive on n=7, which appears in all residue classes.
    """
    print("\n" + "="*70)
    print("SPECIAL ANALYSIS: n = 7")
    print("="*70)

    n = 7
    traj, reached_1, min_val = full_trajectory_until_1(n, max_steps=1000)

    print(f"\nStarting value: {n}")
    print(f"Trajectory length: {len(traj)}")
    print(f"Minimum value: {min_val}")
    print(f"Reaches 1: {reached_1}")
    print(f"\nFull trajectory:")
    print(traj)

    # Count steps above vs below 7
    above = sum(1 for x in traj if x >= 7)
    below = sum(1 for x in traj if x < 7)

    print(f"\nSteps at or above 7: {above}")
    print(f"Steps below 7: {below}")

    # Where does it first go below 7?
    for i, val in enumerate(traj):
        if val < 7:
            print(f"\nFirst drops below 7 at step {i}: {val}")
            break

if __name__ == "__main__":
    test_exceptional_candidates()
    test_power_of_2_residues()
    special_analysis_of_7()

    print("\n" + "="*70)
    print("CONCLUSION")
    print("="*70)
    print("\nBased on computational evidence:")
    print("- Every tested number eventually goes below its starting value")
    print("- The constraint n ≡ 7 (mod 2^k) becomes exponentially sparse")
    print("- But this does NOT prove E is empty")
    print("\nThe gap: Computational verification ≠ Mathematical proof")
    print("="*70)
