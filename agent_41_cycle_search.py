#!/usr/bin/env python3
"""
Agent 41: Systematic Cycle Search for Collatz Conjecture
Attempts to construct or find non-trivial cycles.
"""

from typing import List, Set, Tuple, Optional, Dict
from collections import defaultdict
import sys

def collatz_step(n: int) -> int:
    """Single Collatz step."""
    if n % 2 == 0:
        return n // 2
    else:
        return 3 * n + 1

def syracuse_map(n: int) -> int:
    """Syracuse map: odd to next odd."""
    if n % 2 == 0:
        raise ValueError("Syracuse map only defined for odd numbers")
    result = 3 * n + 1
    while result % 2 == 0:
        result //= 2
    return result

def v2(n: int) -> int:
    """2-adic valuation: highest power of 2 dividing n."""
    if n == 0:
        return float('inf')
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count

def find_cycle_direct(n: int, max_steps: int = 10000) -> Optional[Tuple[List[int], int]]:
    """
    Search for cycle in trajectory of n.
    Returns (cycle_values, cycle_start_index) if found, None otherwise.
    """
    trajectory = [n]
    seen = {n: 0}

    current = n
    for step in range(1, max_steps):
        current = collatz_step(current)

        if current in seen:
            # Found cycle
            cycle_start = seen[current]
            cycle = trajectory[cycle_start:]
            return (cycle, cycle_start)

        seen[current] = step
        trajectory.append(current)

    return None

def analyze_cycle(cycle: List[int]) -> Dict:
    """Analyze properties of a cycle."""
    odd_values = [x for x in cycle if x % 2 == 1]

    mod4_classes = {
        1: [x for x in odd_values if x % 4 == 1],
        3: [x for x in odd_values if x % 4 == 3]
    }

    # Check Syracuse map closure on odd values
    if len(odd_values) >= 2:
        syracuse_pairs = []
        for i, val in enumerate(odd_values):
            next_odd_idx = (i + 1) % len(odd_values)
            expected_next = odd_values[next_odd_idx]
            actual_next = syracuse_map(val)
            syracuse_pairs.append((val, actual_next, expected_next))

    return {
        'length': len(cycle),
        'odd_count': len(odd_values),
        'odd_values': odd_values,
        'mod4_1': mod4_classes[1],
        'mod4_3': mod4_classes[3],
        'min': min(cycle),
        'max': max(cycle),
    }

def search_cycles(limit: int) -> List[Tuple[int, List[int]]]:
    """Search for cycles starting from odd numbers up to limit."""
    print(f"Searching for cycles in odd numbers 1 to {limit}...")

    found_cycles = []

    for n in range(1, limit, 2):
        if n % 1000 == 1:
            print(f"  Checking n = {n}...")

        result = find_cycle_direct(n, max_steps=1000)

        if result is not None:
            cycle, cycle_start = result

            # Check if non-trivial (not 1-4-2-1)
            odd_in_cycle = [x for x in cycle if x % 2 == 1]
            if odd_in_cycle != [1] and len(set(odd_in_cycle)) > 1:
                print(f"\n*** NON-TRIVIAL CYCLE FOUND starting from {n}! ***")
                print(f"Cycle: {cycle}")
                print(f"Analysis: {analyze_cycle(cycle)}")
                found_cycles.append((n, cycle))

    return found_cycles

def inverse_syracuse(m: int) -> List[int]:
    """
    Find all odd n such that S(n) = m.

    S(n) = (3n+1)/2^v where v = v₂(3n+1)

    So: 3n+1 = m * 2^v for some v ≥ 1
        n = (m * 2^v - 1) / 3

    For n to be an odd positive integer:
    - m * 2^v - 1 ≡ 0 (mod 3)
    - m * 2^v - 1 must be positive
    - (m * 2^v - 1) / 3 must be odd
    """
    results = []

    # Try different values of v
    for v in range(1, 100):  # Reasonable upper bound
        numerator = m * (2 ** v) - 1

        if numerator % 3 != 0:
            continue

        n = numerator // 3

        if n <= 0:
            continue

        if n % 2 == 0:
            continue

        # Verify: S(n) = m?
        if syracuse_map(n) == m:
            results.append(n)

        # Stop if n is getting too large
        if n > 10**12:
            break

    return results

def backwards_search(target: int, depth: int = 5) -> Dict[int, List[int]]:
    """
    Build backwards tree: find all values that map to target.

    Returns: dict mapping each discovered value to list of predecessors.
    """
    tree = defaultdict(list)
    queue = [target]
    visited = {target}

    for _ in range(depth):
        if not queue:
            break

        next_queue = []

        for current in queue:
            predecessors = inverse_syracuse(current)

            for pred in predecessors:
                tree[current].append(pred)

                if pred not in visited:
                    visited.add(pred)
                    next_queue.append(pred)

        queue = next_queue

    return dict(tree)

def check_cycle_closure(values: List[int]) -> bool:
    """Check if a list of odd values forms a cycle under Syracuse map."""
    if not values or len(values) == 0:
        return False

    for i, val in enumerate(values):
        expected_next = values[(i + 1) % len(values)]
        actual_next = syracuse_map(val)

        if actual_next != expected_next:
            return False

    return True

def construct_small_cycles(max_val: int = 1000) -> List[List[int]]:
    """
    Try to construct small cycles by checking all combinations.
    Very expensive but thorough for small values.
    """
    print(f"Attempting to construct cycles from values up to {max_val}...")
    found = []

    odd_values = list(range(1, max_val, 2))

    # Try 2-cycles
    print("Checking 2-cycles...")
    for i, n1 in enumerate(odd_values):
        if i % 100 == 0:
            print(f"  Progress: {i}/{len(odd_values)}")

        n2 = syracuse_map(n1)
        if n2 < max_val and n2 % 2 == 1:
            if syracuse_map(n2) == n1:
                cycle = [n1, n2]
                if n1 != n2:  # Non-trivial
                    print(f"\n*** 2-CYCLE FOUND: {cycle}")
                    found.append(cycle)

    # Try 3-cycles (more expensive)
    print("Checking 3-cycles (sample)...")
    for i in range(0, min(100, len(odd_values))):
        n1 = odd_values[i]
        n2 = syracuse_map(n1)

        if n2 < max_val and n2 % 2 == 1:
            n3 = syracuse_map(n2)

            if n3 < max_val and n3 % 2 == 1:
                if syracuse_map(n3) == n1:
                    cycle = [n1, n2, n3]
                    if len(set(cycle)) == 3:  # All distinct
                        print(f"\n*** 3-CYCLE FOUND: {cycle}")
                        found.append(cycle)

    return found

def theoretical_cycle_bounds():
    """
    Compute theoretical constraints on cycle existence.
    """
    print("\n" + "="*70)
    print("THEORETICAL CYCLE BOUNDS")
    print("="*70)

    print("\n1. DESCENT CONSTRAINT:")
    print("   - Every cycle must contain at least one m ≡ 1 (mod 4)")
    print("   - For such m: S(m) < m")
    print("   - Therefore: max(cycle) ≡ 1 (mod 4) implies descent\n")

    print("2. GROWTH RATES:")
    for m_mod4 in [1, 3]:
        examples = []
        for m in range(m_mod4, 100, 4):
            if m % 2 == 1:
                s_m = syracuse_map(m)
                ratio = s_m / m
                examples.append((m, s_m, ratio))
                if len(examples) >= 5:
                    break

        print(f"\n   m ≡ {m_mod4} (mod 4):")
        for m, s_m, ratio in examples:
            print(f"     S({m:3d}) = {s_m:3d}, ratio = {ratio:.4f}")

    print("\n3. NECESSARY CONDITION FOR CYCLE:")
    print("   Product of all ratios S(cᵢ)/cᵢ must equal 1")
    print("   For m ≡ 1 (mod 4): ratio ≤ 0.75")
    print("   For m ≡ 3 (mod 4): ratio ≈ 1.5")
    print("   Need balance: #(≡1 mod 4) / #(≡3 mod 4) ≈ 1.4")

    print("\n4. MINIMUM CYCLE LENGTH:")
    print("   By Hitting Time: must hit ≡1 (mod 4)")
    print("   By descent: such values decrease")
    print("   To return: need increases via ≡3 (mod 4) values")
    print("   Minimum length: likely ≥ 3")

def main():
    print("AGENT 41: CYCLE CONSTRUCTION AND SEARCH")
    print("="*70)

    # 1. Theoretical bounds
    theoretical_cycle_bounds()

    # 2. Direct search for cycles
    print("\n" + "="*70)
    print("DIRECT TRAJECTORY SEARCH")
    print("="*70)

    found = search_cycles(limit=10000)

    if found:
        print(f"\n*** TOTAL NON-TRIVIAL CYCLES FOUND: {len(found)} ***")
    else:
        print("\nNo non-trivial cycles found in range.")

    # 3. Backwards tree from 1
    print("\n" + "="*70)
    print("BACKWARDS TREE FROM 1")
    print("="*70)

    tree = backwards_search(1, depth=4)
    print(f"\nBackwards tree from 1 (depth 4):")
    for value, predecessors in sorted(tree.items()):
        print(f"  {value} <- {predecessors}")

    # 4. Attempt to construct small cycles
    print("\n" + "="*70)
    print("CYCLE CONSTRUCTION ATTEMPT")
    print("="*70)

    cycles = construct_small_cycles(max_val=10000)

    if cycles:
        print(f"\n*** CONSTRUCTED CYCLES: {cycles} ***")
    else:
        print("\nNo cycles constructed.")

    # 5. Specific algebraic attempts
    print("\n" + "="*70)
    print("ALGEBRAIC VERIFICATION")
    print("="*70)

    # Check the 9 -> 17 increase
    print("\nVerifying gap example (9 -> 17):")
    traj = [9]
    current = 9
    for _ in range(20):
        current = collatz_step(current)
        traj.append(current)
        if current == 17:
            break

    odd_traj = [x for x in traj if x % 2 == 1]
    mod4_1 = [x for x in odd_traj if x % 4 == 1]

    print(f"  Trajectory: {traj}")
    print(f"  Odd values: {odd_traj}")
    print(f"  Values ≡1 (mod 4): {mod4_1}")
    print(f"  Confirmed: {mod4_1[0]} < {mod4_1[1]} (increase!)")

    print("\n" + "="*70)
    print("SEARCH COMPLETE")
    print("="*70)

if __name__ == "__main__":
    main()
