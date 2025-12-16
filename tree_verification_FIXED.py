#!/usr/bin/env python3
"""
FIXED TREE VERIFICATION
========================

TERMINOLOGY CLARIFICATION:
==========================

FORWARD COLLATZ TREE (rooted at any starting number):
  - Edges go: n → next_value
  - If n even: n → n/2
  - If n odd: n → 3n+1

BACKWARDS TREE (rooted at 1):
  - We ask: starting from 1, what numbers can we reach by REVERSING the Collatz steps?
  - Edges go: n → reverse_step(n)
  - We can reach:
    1. 2n (reverse of division by 2)
    2. (n-1)/3 if n ≡ 1 (mod 3) and (n-1)/3 is odd (reverse of 3m+1)

CORRECTED FUNCTIONS:
  - forward_step(n): apply Collatz rule
  - backward_successors(n): what numbers can we reach FROM n going backwards?
  - forward_predecessors(n): what numbers can reach n going forward? (same as backward_successors)
"""

from collections import deque

def forward_step(n):
    """Standard Collatz forward step."""
    if n % 2 == 0:
        return n // 2
    else:
        return 3 * n + 1

def forward_path_to_one(n, max_steps=100000):
    """Get forward path from n to 1."""
    path = [n]
    current = n
    steps = 0
    while current != 1 and steps < max_steps:
        current = forward_step(current)
        path.append(current)
        steps += 1
    return path if current == 1 else None

def backward_successors(n):
    """
    What numbers can we reach FROM n by reversing Collatz steps?

    From n, we can go backwards to:
    1. 2n (if m was even and m/2 = n, then m = 2n)
    2. (n-1)/3 if:
       - n ≡ 1 (mod 3), AND
       - (n-1)/3 is odd (so that 3×[(n-1)/3]+1 = n was a valid odd step)

    More precise for case 2:
    - We need m odd such that 3m+1 = n
    - So m = (n-1)/3
    - For m to be odd: (n-1)/3 ≡ 1 (mod 2)
    - So n-1 ≡ 3 (mod 6)
    - So n ≡ 4 (mod 6)
    """
    successors = [2 * n]  # Can always go to 2n

    # Check if we can go to (n-1)/3
    # Condition: n ≡ 4 (mod 6) ensures (n-1)/3 is odd
    if n % 6 == 4 and n > 1:
        m = (n - 1) // 3
        # Verify m is odd
        assert m % 2 == 1, f"Logic error: {m} should be odd"
        successors.append(m)

    return successors

def build_backward_tree_bfs(max_depth=50):
    """
    Build backward tree from 1 using BFS.
    Returns set of all numbers reachable.
    """
    reached = {1}
    queue = deque([(1, 0)])  # (number, depth)

    while queue:
        current, depth = queue.popleft()

        if depth >= max_depth:
            continue

        for successor in backward_successors(current):
            if successor not in reached:
                reached.add(successor)
                queue.append((successor, depth + 1))

    return reached

def find_backward_path(target, max_depth=200):
    """
    Find path from 1 to target in backward tree.
    Returns path if found, None otherwise.
    """
    if target == 1:
        return [1]

    # BFS from 1
    queue = deque([(1, [1])])
    visited = {1}

    while queue:
        current, path = queue.popleft()

        if len(path) > max_depth:
            continue

        for successor in backward_successors(current):
            if successor == target:
                return path + [successor]

            if successor not in visited:
                visited.add(successor)
                queue.append((successor, path + [successor]))

    return None

def comprehensive_test():
    """
    Comprehensive test of backward tree coverage.
    """
    print("="*70)
    print("FIXED BACKWARDS TREE VERIFICATION")
    print("="*70)

    print("\n1. BUILDING BACKWARDS TREE FROM 1...")
    print("   Using BFS with max depth 50...")

    reached = build_backward_tree_bfs(max_depth=50)

    print(f"   Total numbers reached: {len(reached)}")

    # Check coverage for small numbers
    for limit in [10, 100, 1000]:
        small = set(range(1, limit + 1))
        reached_small = small & reached
        missing = small - reached

        print(f"\n   Coverage for n ≤ {limit}:")
        print(f"     Reached: {len(reached_small)}/{limit} ({100*len(reached_small)/limit:.1f}%)")

        if missing and limit <= 100:
            print(f"     Missing: {sorted(missing)[:30]}")

    # Test specific problematic numbers
    print("\n2. TESTING SPECIFIC NUMBERS:")
    test_nums = [27, 31, 41, 47, 54, 55, 71, 97]

    for num in test_nums:
        print(f"\n   Testing {num}:")

        # Check if in tree
        if num in reached:
            print(f"     ✓ Found in backward tree")

            # Find path
            path = find_backward_path(num, max_depth=100)
            if path:
                print(f"     Backward path (length {len(path)-1}): {path[:10]}...")
        else:
            print(f"     ✗ NOT in backward tree (depth 50)")

            # But does it reach 1 going forward?
            fwd_path = forward_path_to_one(num)
            if fwd_path:
                print(f"     However, forward path to 1 exists (length {len(fwd_path)-1})")
                print(f"     This proves backward tree is INCOMPLETE!")

def analyze_coverage_pattern():
    """
    Analyze the pattern of coverage.
    """
    print(f"\n{'='*70}")
    print("COVERAGE PATTERN ANALYSIS")
    print("="*70)

    reached = build_backward_tree_bfs(max_depth=60)

    # Analyze missing numbers mod 6
    missing = set(range(1, 1001)) - reached

    print("\nDistribution of MISSING numbers (n ≤ 1000) by residue class:")

    for mod in [3, 6]:
        print(f"\n  Mod {mod}:")
        counts = {}
        for m in missing:
            r = m % mod
            counts[r] = counts.get(r, 0) + 1

        for r in range(mod):
            count = counts.get(r, 0)
            pct = 100 * count / len(missing) if missing else 0
            print(f"    {r} (mod {mod}): {count:4d} numbers ({pct:5.1f}%)")

    # Check which numbers ARE reached
    print("\nDistribution of REACHED numbers (n ≤ 1000) by residue class:")
    reached_small = set(range(1, 1001)) & reached

    for mod in [3, 6]:
        print(f"\n  Mod {mod}:")
        counts = {}
        for m in reached_small:
            r = m % mod
            counts[r] = counts.get(r, 0) + 1

        for r in range(mod):
            count = counts.get(r, 0)
            pct = 100 * count / len(reached_small) if reached_small else 0
            print(f"    {r} (mod {mod}): {count:4d} numbers ({pct:5.1f}%)")

def verify_27_specifically():
    """
    Trace why 27 is problematic.
    """
    print(f"\n{'='*70}")
    print("DEEP INVESTIGATION: NUMBER 27")
    print("="*70)

    print("\nForward path from 27:")
    fwd = forward_path_to_one(27)
    print(f"  Steps: {len(fwd)-1}")
    print(f"  Path: {fwd[:15]}...")

    print("\nAttempting to find 27 in backward tree:")
    path = find_backward_path(27, max_depth=150)

    if path:
        print(f"  ✓ FOUND! Path from 1 to 27:")
        print(f"  Length: {len(path)-1}")
        print(f"  Path: {path}")

        # Verify each step
        print("\n  Verifying each step:")
        for i in range(len(path)-1):
            curr = path[i]
            next_val = path[i+1]
            successors = backward_successors(curr)

            if next_val in successors:
                print(f"    {curr} → {next_val} ✓")
            else:
                print(f"    {curr} → {next_val} ✗ (successors: {successors})")
    else:
        print(f"  ✗ NOT FOUND in backward tree (depth limit 150)")
        print("\n  This means:")
        print("  - 27 reaches 1 going forward (verified)")
        print("  - But 1 cannot reach 27 going backward (within depth 150)")
        print("  - Conclusion: Backward tree is NOT complete!")

if __name__ == "__main__":
    comprehensive_test()
    analyze_coverage_pattern()
    verify_27_specifically()
