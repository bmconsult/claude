#!/usr/bin/env python3
"""
OMEGA+ Agent 28: Tree Verifier
===============================

Mission: Verify if the backwards Collatz tree from 1 covers ALL positive integers.

Backwards Tree Structure:
- Start from 1
- Each node n has up to 2 children:
  1. 2n (always valid)
  2. (n-1)/3 if n ≡ 1 (mod 3) and n > 1

If this tree covers all ℕ⁺, then Collatz is proven (every number has a path to 1).
"""

from collections import deque
import sys

def backwards_children(n):
    """
    Generate children in the backwards Collatz tree.

    From node n, we can reach:
    1. 2n (reverse of n/2)
    2. (n-1)/3 if n ≡ 1 (mod 3) (reverse of 3n+1)
    """
    children = [2 * n]  # Always can go to 2n

    # Check if we can go to (n-1)/3
    if n > 1 and (n - 1) % 3 == 0:
        children.append((n - 1) // 3)

    return children

def build_backwards_tree_bfs(max_value, max_iterations=1000000):
    """
    Build backwards tree from 1 using BFS.
    Track which numbers we've reached.
    """
    reached = {1}
    queue = deque([1])
    iteration = 0

    while queue and iteration < max_iterations:
        if reached >= set(range(1, max_value + 1)):
            # We've covered all numbers up to max_value
            break

        current = queue.popleft()
        iteration += 1

        for child in backwards_children(current):
            if child <= max_value and child not in reached:
                reached.add(child)
                queue.append(child)

    return reached

def verify_coverage(max_value):
    """
    Verify if backwards tree covers all integers 1 to max_value.
    """
    reached = build_backwards_tree_bfs(max_value)
    all_numbers = set(range(1, max_value + 1))
    missing = all_numbers - reached

    print(f"=== TREE COVERAGE ANALYSIS (n ≤ {max_value}) ===")
    print(f"Total numbers: {len(all_numbers)}")
    print(f"Reached: {len(reached)}")
    print(f"Missing: {len(missing)}")
    print(f"Coverage: {100 * len(reached) / len(all_numbers):.2f}%")

    if missing:
        print(f"\nMISSING NUMBERS: {sorted(missing)[:20]}")
        if len(missing) > 20:
            print(f"... and {len(missing) - 20} more")
        return False
    else:
        print("\n✓ COMPLETE COVERAGE: All numbers reached!")
        return True

def find_path_to_number(target, max_depth=1000):
    """
    Find path from 1 to target in backwards tree (BFS).
    Returns the path if found, None otherwise.
    """
    if target == 1:
        return [1]

    # BFS from 1 to target
    queue = deque([(1, [1])])
    visited = {1}

    while queue:
        current, path = queue.popleft()

        if len(path) > max_depth:
            continue

        for child in backwards_children(current):
            if child == target:
                return path + [child]

            if child not in visited and child <= target * 2:  # Heuristic bound
                visited.add(child)
                queue.append((child, path + [child]))

    return None

def verify_path_properties(path):
    """
    Verify that a backwards path satisfies tree properties.
    """
    print("\n=== PATH VERIFICATION ===")
    print(f"Path: {' → '.join(map(str, path))}")
    print(f"Length: {len(path)}")

    # Verify each step
    for i in range(len(path) - 1):
        current = path[i]
        next_val = path[i + 1]

        valid_children = backwards_children(current)
        if next_val not in valid_children:
            print(f"ERROR: {next_val} is not a valid child of {current}")
            print(f"Valid children: {valid_children}")
            return False

    print("✓ Path valid: each step follows backwards tree rules")
    return True

def theoretical_analysis():
    """
    Theoretical analysis of tree structure.
    """
    print("\n" + "="*60)
    print("THEORETICAL ANALYSIS")
    print("="*60)

    print("\n1. TREE STRUCTURE:")
    print("   - Root: 1")
    print("   - Child rule 1: n → 2n (always)")
    print("   - Child rule 2: n → (n-1)/3 if n ≡ 1 (mod 3)")

    print("\n2. PARITY ANALYSIS:")
    print("   - Starting from 1 (odd):")
    print("     * 2n gives even children")
    print("     * (n-1)/3 gives mixed parity")

    print("\n3. MODULAR STRUCTURE (mod 3):")
    for r in range(3):
        print(f"\n   n ≡ {r} (mod 3):")
        print(f"     2n ≡ {(2*r) % 3} (mod 3)")
        if r == 1:
            print(f"     (n-1)/3: valid, reaches all residues")
        else:
            print(f"     (n-1)/3: NOT VALID")

    print("\n4. KEY INSIGHT:")
    print("   - 2n operation doubles the number (always increases)")
    print("   - (n-1)/3 operation roughly divides by 3")
    print("   - Question: Can we reach ALL numbers this way?")

def check_specific_number(target):
    """
    Check if we can reach a specific number from 1.
    """
    print(f"\n{'='*60}")
    print(f"FINDING PATH TO {target}")
    print("="*60)

    path = find_path_to_number(target, max_depth=500)

    if path:
        print(f"✓ FOUND PATH from 1 to {target}!")
        verify_path_properties(path)
        return True
    else:
        print(f"✗ COULD NOT FIND PATH to {target}")
        print(f"  (within depth limit)")
        return False

def density_analysis(max_val):
    """
    Analyze the density of coverage at different scales.
    """
    print(f"\n{'='*60}")
    print("DENSITY ANALYSIS")
    print("="*60)

    scales = [10, 100, 1000, 10000]
    for scale in scales:
        if scale > max_val:
            break
        reached = build_backwards_tree_bfs(scale)
        coverage = 100 * len(reached) / scale
        print(f"  n ≤ {scale:5d}: {coverage:6.2f}% coverage")

if __name__ == "__main__":
    print("OMEGA+ AGENT 28: BACKWARDS TREE VERIFICATION")
    print("="*60)

    # Theoretical analysis first
    theoretical_analysis()

    # Computational verification for small values
    print("\n" + "="*60)
    print("COMPUTATIONAL VERIFICATION")
    print("="*60)

    # Check coverage for n ≤ 10000
    verify_coverage(10000)

    # Density analysis
    density_analysis(10000)

    # Check specific problematic numbers
    print("\n" + "="*60)
    print("SPECIFIC NUMBER TESTS")
    print("="*60)

    test_numbers = [27, 31, 41, 47, 71, 97, 127]
    print(f"\nTesting numbers known to have long trajectories:")

    for num in test_numbers:
        check_specific_number(num)

    print("\n" + "="*60)
    print("VERIFICATION COMPLETE")
    print("="*60)
