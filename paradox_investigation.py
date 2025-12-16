#!/usr/bin/env python3
"""
PARADOX INVESTIGATION
=====================

CRITICAL PARADOX:
- 27 reaches 1 going FORWARD (verified in 111 steps)
- 27 is NOT in backwards tree from 1
- This should be IMPOSSIBLE if backwards rules are correct!

HYPOTHESIS:
There must be an error in:
1. The backwards tree construction algorithm, OR
2. The backwards rules themselves, OR
3. Our understanding of the tree structure

Let's trace 27's forward path and check if we can reverse it.
"""

from collections import deque

def collatz_forward(n):
    """Standard forward Collatz."""
    if n % 2 == 0:
        return n // 2
    else:
        return 3 * n + 1

def collatz_forward_path(n):
    """Get full path from n to 1."""
    path = [n]
    while n != 1:
        n = collatz_forward(n)
        path.append(n)
    return path

def backwards_children(n):
    """
    What numbers can reach n in one forward step?

    If m → n in forward Collatz:
    - Case 1: m even, m/2 = n, so m = 2n
    - Case 2: m odd, 3m+1 = n, so m = (n-1)/3 (must be odd integer)
    """
    parents = [2 * n]  # Always can come from 2n

    # Check if (n-1)/3 is an odd integer
    if (n - 1) % 3 == 0:
        m = (n - 1) // 3
        if m % 2 == 1:  # m must be odd
            parents.append(m)

    return parents

def build_backwards_tree_unlimited(start, target, max_depth=None):
    """
    Build backwards tree from start, looking for target.
    No value limits - explore freely.
    """
    if start == target:
        return {start: 0}

    reached = {start: 0}
    queue = deque([(start, 0)])
    found_target = False

    while queue:
        current, depth = queue.popleft()

        if max_depth is not None and depth >= max_depth:
            continue

        for child in backwards_children(current):
            if child == target:
                found_target = True
                reached[child] = depth + 1
                print(f"   FOUND {target} at depth {depth + 1} from {start}")

            if child not in reached:
                reached[child] = depth + 1
                queue.append((child, depth + 1))

    return reached

def trace_specific_number(n):
    """
    Trace n's forward path and attempt to reverse it.
    """
    print(f"\n{'='*70}")
    print(f"INVESTIGATING: {n}")
    print("="*70)

    # Get forward path
    forward_path = collatz_forward_path(n)
    print(f"\n1. FORWARD PATH FROM {n} TO 1:")
    print(f"   Length: {len(forward_path) - 1} steps")
    print(f"   Path: {forward_path[:20]}...")

    # Now try to reverse the path
    print(f"\n2. REVERSING THE PATH:")
    print(f"   Starting from 1, checking each step...")

    reversed_path = list(reversed(forward_path))

    for i in range(len(reversed_path) - 1):
        current = reversed_path[i]
        next_val = reversed_path[i + 1]

        parents = backwards_children(next_val)

        if current in parents:
            print(f"   ✓ {current} → {next_val} (valid backwards step)")
        else:
            print(f"   ✗ {current} → {next_val} (INVALID! Parents of {next_val} are {parents})")
            print(f"      This should be impossible!")
            return False

    print(f"\n   ✓ ALL STEPS VALID! Path is reversible.")

    # Now check if we can find n from 1 using BFS
    print(f"\n3. SEARCHING FOR {n} FROM 1 USING BFS:")

    # Do unlimited search
    reached = build_backwards_tree_unlimited(1, n, max_depth=len(forward_path))

    if n in reached:
        print(f"   ✓ FOUND {n} at depth {reached[n]}")
    else:
        print(f"   ✗ NOT FOUND in depth limit {len(forward_path)}")

    return True

def analyze_backwards_reachability():
    """
    Analyze which numbers are reachable backwards from 1.
    """
    print(f"\n{'='*70}")
    print("BACKWARDS REACHABILITY ANALYSIS")
    print("="*70)

    # Build backwards tree with no value limit
    print("\nBuilding backwards tree from 1 (no value limit, depth 30)...")

    reached = build_backwards_tree_unlimited(1, None, max_depth=30)

    print(f"   Reached {len(reached)} distinct numbers")

    # Check coverage for small numbers
    small_nums = set(range(1, 101))
    reached_small = small_nums & reached.keys()
    missing_small = small_nums - reached.keys()

    print(f"\n   Coverage for n ≤ 100:")
    print(f"   Reached: {len(reached_small)}/100")
    print(f"   Missing: {sorted(missing_small)[:30]}")

    # Check if our problematic numbers are there
    test_nums = [27, 31, 41, 47, 71, 97]
    print(f"\n   Checking specific numbers:")
    for num in test_nums:
        if num in reached:
            print(f"   {num:3d}: FOUND at depth {reached[num]}")
        else:
            print(f"   {num:3d}: NOT FOUND")

def investigate_27_specifically():
    """
    Deep dive into why 27 might not be reachable.
    """
    print(f"\n{'='*70}")
    print("DEEP DIVE: NUMBER 27")
    print("="*70)

    # To reach 27, we need to come from either:
    # 1. 54 (via 27 = 54/2)
    # 2. (27-1)/3 = 26/3 (not integer) - NO

    print("\nTo reach 27 backwards: must come from 54")
    print("To reach 54 backwards: must come from 108 or (54-1)/3 = 53/3 (not int)")
    print("To reach 108 backwards: must come from 216 or (108-1)/3 = 107/3 (not int)")
    print("...")
    print("Pattern: 27 = 27×2⁰, 54 = 27×2¹, 108 = 27×2², 216 = 27×2³, ...")

    # This means 27 can only be reached by a long chain of doublings
    # We need to find some k where 27×2ᵏ can be reached another way

    print("\nSearching for 27×2ᵏ that has two parents...")

    for k in range(20):
        val = 27 * (2 ** k)
        parents = backwards_children(val)

        print(f"   27×2^{k:2d} = {val:8d}: parents = {parents}", end="")

        if len(parents) == 2:
            print(f" ← TWO PARENTS")
        else:
            print()

if __name__ == "__main__":
    print("OMEGA+ PARADOX INVESTIGATION")
    print("="*70)

    # Trace specific numbers
    trace_specific_number(27)
    trace_specific_number(31)

    # Broader analysis
    analyze_backwards_reachability()

    # Deep dive
    investigate_27_specifically()
