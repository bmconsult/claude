#!/usr/bin/env python3
"""
Investigation of emergent structure: Does the backwards tree from 1 cover all of N?

This explores an alternative proof strategy based on the inverse Collatz map.
"""

def collatz_inverse_odd(n):
    """
    Given odd n, find all odd m such that T(m) = n.

    Returns list of odd predecessors.
    """
    predecessors = []

    # Case 1: m was odd and 3m+1 = 2^k * n for some k >= 1
    # So m = (2^k * n - 1) / 3
    # For m to be odd and positive, need:
    #   - 2^k * n ≡ 1 (mod 3)
    #   - m > 0

    for k in range(1, 100):  # Check first 100 powers
        numerator = (2**k) * n - 1
        if numerator % 3 == 0:
            m = numerator // 3
            if m > 0 and m % 2 == 1:
                # Verify this is correct
                # T(m) should equal n
                # T(m) = (3m+1) / 2^v2(3m+1)
                val = 3*m + 1
                # Find 2-adic valuation
                v = 0
                temp = val
                while temp % 2 == 0:
                    temp //= 2
                    v += 1

                result = val // (2**v)
                if result == n:
                    predecessors.append(m)

    return predecessors

def build_backwards_tree(start, levels):
    """
    Build backwards tree from start for given number of levels.
    Returns set of all reachable numbers.
    """
    current_level = {start}
    all_reached = {start}

    for level in range(levels):
        next_level = set()
        for n in current_level:
            if n % 2 == 1:  # Only process odd numbers
                preds = collatz_inverse_odd(n)
                next_level.update(preds)

        all_reached.update(next_level)
        current_level = next_level

        if level < 5 or level % 5 == 0:
            print(f"Level {level}: {len(current_level)} new nodes, {len(all_reached)} total")

    return all_reached

def check_coverage(max_n, levels):
    """
    Check what fraction of odd numbers up to max_n are covered by backwards tree.
    """
    print(f"\n{'='*60}")
    print(f"Checking backwards tree coverage up to n = {max_n}")
    print(f"Building tree to depth {levels}")
    print(f"{'='*60}\n")

    backwards_tree = build_backwards_tree(1, levels)

    # Check coverage of odd numbers
    odd_numbers = set(range(1, max_n + 1, 2))
    covered = odd_numbers & backwards_tree
    uncovered = odd_numbers - backwards_tree

    coverage_fraction = len(covered) / len(odd_numbers)

    print(f"\n{'='*60}")
    print(f"COVERAGE ANALYSIS")
    print(f"{'='*60}")
    print(f"Odd numbers tested: {len(odd_numbers)}")
    print(f"Covered by tree: {len(covered)}")
    print(f"Not yet covered: {len(uncovered)}")
    print(f"Coverage fraction: {coverage_fraction:.4%}")

    if uncovered and len(uncovered) <= 20:
        print(f"\nUncovered numbers: {sorted(uncovered)}")
    elif uncovered:
        uncovered_sorted = sorted(uncovered)
        print(f"\nFirst uncovered: {uncovered_sorted[:20]}")
        print(f"Last uncovered: {uncovered_sorted[-20:]}")

    return covered, uncovered

def analyze_growth_rate(max_levels=20):
    """
    Analyze how fast the backwards tree grows.
    """
    print(f"\n{'='*60}")
    print(f"BACKWARDS TREE GROWTH RATE ANALYSIS")
    print(f"{'='*60}\n")

    current = {1}
    all_reached = {1}

    print(f"{'Level':<6} {'New':<10} {'Total':<10} {'Growth Rate':<12}")
    print(f"{'-'*60}")
    print(f"{0:<6} {1:<10} {1:<10} {'-':<12}")

    for level in range(1, max_levels + 1):
        next_level = set()
        for n in current:
            if n % 2 == 1:
                preds = collatz_inverse_odd(n)
                next_level.update(preds)

        prev_total = len(all_reached)
        all_reached.update(next_level)
        new_total = len(all_reached)

        growth_rate = new_total / prev_total if prev_total > 0 else 0

        print(f"{level:<6} {len(next_level):<10} {new_total:<10} {growth_rate:<12.4f}")

        current = next_level

        if len(current) == 0:
            print("\nTree stopped growing (no new nodes)")
            break

    return all_reached

def analyze_uncovered_pattern(max_n=1000, levels=15):
    """
    Analyze if uncovered numbers have special structure.
    """
    _, uncovered = check_coverage(max_n, levels)

    if not uncovered:
        print("\n✓ Complete coverage achieved!")
        return

    print(f"\n{'='*60}")
    print(f"ANALYZING UNCOVERED NUMBERS")
    print(f"{'='*60}\n")

    uncovered_sorted = sorted(uncovered)

    # Check residue classes
    print("Residue class distribution:")
    for mod in [4, 8, 16]:
        residues = {}
        for n in uncovered_sorted:
            r = n % mod
            residues[r] = residues.get(r, 0) + 1

        print(f"\nmod {mod}:")
        for r in sorted(residues.keys()):
            print(f"  {r:3d} (mod {mod:2d}): {residues[r]:4d} numbers")

    # Check if they're all in high residue classes
    high_residue = [n for n in uncovered_sorted if n % 32 >= 16]
    print(f"\nNumbers with n ≡ [16,31] (mod 32): {len(high_residue)} / {len(uncovered_sorted)}")

def main():
    print("="*60)
    print("EMERGENT STRUCTURE: Backwards Tree Coverage")
    print("="*60)
    print("\nInvestigating whether T^(-1) covers all of N by iteration.\n")

    # Growth rate analysis
    tree = analyze_growth_rate(max_levels=15)

    # Coverage analysis
    check_coverage(max_n=1000, levels=15)

    # Pattern analysis
    analyze_uncovered_pattern(max_n=1000, levels=15)

    print(f"\n{'='*60}")
    print("INTERPRETATION")
    print(f"{'='*60}")
    print("""
If the backwards tree from 1 covers all odd natural numbers, this provides
an ALTERNATIVE proof of Collatz:

    1. Every odd n is in T^(-k)(1) for some k
    2. Therefore T^k(n) = 1
    3. Therefore every trajectory reaches 1

This would be a CONSTRUCTIVE proof (explicit path to 1) rather than
the EXISTENCE proof given by the Hitting Time Theorem.

The two approaches are complementary:
- Hitting Time: Shows structure forces hitting descent zone
- Backwards Tree: Shows inverse map constructs path from 1 to all n
    """)

if __name__ == "__main__":
    main()
