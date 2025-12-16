#!/usr/bin/env python3
"""
CORRECTED Tree Verification
=============================

CRITICAL REALIZATION: The backwards rules must account for PARITY!

Forward Collatz:
  - n even: n → n/2
  - n odd: n → 3n+1

Backwards (what could reach n?):
  - 2n could reach n (via division by 2)
  - If n = 3m+1 and m is ODD, then m could reach n

For m → 3m+1 → n:
  - n = 3m+1
  - m = (n-1)/3
  - m must be ODD for the 3m+1 rule to apply

So (n-1)/3 must be odd:
  - n-1 must be divisible by 3: n ≡ 1 (mod 3)
  - (n-1)/3 must be odd: n-1 ≡ 3 (mod 6), so n ≡ 4 (mod 6)

CORRECTED BACKWARDS RULES:
1. n → 2n (always)
2. n → (n-1)/3 if n ≡ 4 (mod 6)
"""

from collections import deque

def backwards_children_corrected(n):
    """
    CORRECTED: Account for parity constraint.

    From n we can reach:
    1. 2n (reverse of even → even/2)
    2. (n-1)/3 if n ≡ 4 (mod 6) [ensures (n-1)/3 is odd]
    """
    children = [2 * n]

    # Check if n ≡ 4 (mod 6)
    if n % 6 == 4:
        m = (n - 1) // 3
        children.append(m)
        # Verify m is odd
        assert m % 2 == 1, f"Error: (n-1)/3 = {m} should be odd when n={n}"

    return children

def backwards_children_wrong(n):
    """Original (incorrect) version for comparison."""
    children = [2 * n]
    if n > 1 and (n - 1) % 3 == 0:
        children.append((n - 1) // 3)
    return children

def build_tree_and_compare(max_value, correct=True):
    """Build tree with correct or wrong rules."""
    func = backwards_children_corrected if correct else backwards_children_wrong

    reached = {1}
    queue = deque([1])

    while queue:
        if len(reached) >= max_value:
            # Don't generate beyond max_value
            current = queue.popleft()
            for child in func(current):
                if child <= max_value and child not in reached:
                    reached.add(child)
                    queue.append(child)
        else:
            if not queue:
                break
            current = queue.popleft()
            for child in func(current):
                if child <= max_value and child not in reached:
                    reached.add(child)
                    queue.append(child)

    return reached

def comprehensive_analysis():
    """Compare correct vs wrong rules."""
    print("="*70)
    print("BACKWARDS TREE: CORRECTED ANALYSIS")
    print("="*70)

    max_val = 10000

    print("\n1. TESTING CORRECTED RULES (n ≡ 4 (mod 6))...")
    reached_correct = build_tree_and_compare(max_val, correct=True)
    missing_correct = set(range(1, max_val + 1)) - reached_correct

    print(f"   Reached: {len(reached_correct)}/{max_val}")
    print(f"   Coverage: {100*len(reached_correct)/max_val:.2f}%")

    print("\n2. TESTING WRONG RULES (n ≡ 1 (mod 3))...")
    reached_wrong = build_tree_and_compare(max_val, correct=False)
    missing_wrong = set(range(1, max_val + 1)) - reached_wrong

    print(f"   Reached: {len(reached_wrong)}/{max_val}")
    print(f"   Coverage: {100*len(reached_wrong)/max_val:.2f}%")

    print("\n3. COMPARISON:")
    only_in_correct = reached_correct - reached_wrong
    only_in_wrong = reached_wrong - reached_correct

    print(f"   Only in correct: {len(only_in_correct)}")
    print(f"   Only in wrong: {len(only_in_wrong)}")

    if only_in_wrong:
        print(f"\n   Numbers WRONGLY included: {sorted(list(only_in_wrong))[:20]}")

    # Test specific numbers
    print("\n4. TESTING SPECIFIC NUMBERS:")
    test_nums = [27, 31, 41, 47, 71, 97]

    for num in test_nums:
        in_correct = num in reached_correct
        in_wrong = num in reached_wrong
        print(f"   {num:3d}: Correct={in_correct}, Wrong={in_wrong}")

    print("\n5. ANALYZING MISSING NUMBERS (CORRECTED):")
    if missing_correct:
        print(f"   Still missing: {len(missing_correct)}")
        print(f"   First 30: {sorted(list(missing_correct))[:30]}")

        # Analyze pattern of missing numbers
        missing_mod3 = {}
        missing_mod6 = {}
        for m in missing_correct:
            mod3 = m % 3
            mod6 = m % 6
            missing_mod3[mod3] = missing_mod3.get(mod3, 0) + 1
            missing_mod6[mod6] = missing_mod6.get(mod6, 0) + 1

        print(f"\n   Distribution (mod 3): {missing_mod3}")
        print(f"   Distribution (mod 6): {missing_mod6}")

def verify_forward_backward_consistency():
    """
    Verify that backwards rules are truly inverse of forward rules.
    """
    print("\n" + "="*70)
    print("FORWARD-BACKWARD CONSISTENCY CHECK")
    print("="*70)

    def collatz_forward(n):
        """Forward Collatz step."""
        if n % 2 == 0:
            return n // 2
        else:
            return 3 * n + 1

    print("\nTesting: If n is in backwards tree, can it reach 1 forward?")

    # Get some numbers from backwards tree
    reached = build_tree_and_compare(1000, correct=True)

    # Test forward from each
    test_sample = sorted(list(reached))[:50]

    all_reach_one = True
    for n in test_sample:
        current = n
        steps = 0
        max_steps = 10000

        while current != 1 and steps < max_steps:
            current = collatz_forward(current)
            steps += 1

        if current != 1:
            print(f"   {n} did NOT reach 1 in {max_steps} steps!")
            all_reach_one = False

    if all_reach_one:
        print(f"   ✓ All {len(test_sample)} tested numbers reach 1 forward")

    print("\nTesting: Do numbers NOT in tree fail to reach 1?")
    missing = set(range(1, 1001)) - reached

    # Pick some missing numbers and test forward
    test_missing = sorted(list(missing))[:20]

    for n in test_missing:
        current = n
        steps = 0
        max_steps = 10000

        while current != 1 and steps < max_steps:
            current = collatz_forward(current)
            steps += 1

        if current == 1:
            print(f"   {n} IS NOT in backwards tree but DOES reach 1! (steps={steps})")
        else:
            print(f"   {n} NOT in tree, did not reach 1 in {max_steps} steps")

if __name__ == "__main__":
    comprehensive_analysis()
    verify_forward_backward_consistency()
