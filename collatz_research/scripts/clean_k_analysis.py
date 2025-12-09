#!/usr/bin/env python3
"""
Clean k Analysis - Investigating algebraic structure of k=10,11,12,20
and the fake cycles that prevent them from being clean.

A value k is "clean" if all odd residue classes mod 2^k eventually
reach class 1 under the Syracuse map S_k(c) = S(c) mod 2^k.
"""

from collections import defaultdict
from functools import lru_cache
import math

def syracuse_mod(n, k):
    """Syracuse map modulo 2^k"""
    if n % 2 == 0:
        raise ValueError("Syracuse is only for odd numbers")

    # Apply 3n+1
    val = 3 * n + 1

    # Count trailing zeros (2-adic valuation)
    v2 = 0
    while val % 2 == 0:
        val //= 2
        v2 += 1

    # Return result mod 2^k
    return val % (2**k)

def find_cycles_mod_k(k, max_iterations=10000):
    """Find all cycles in Syracuse map mod 2^k"""
    mod = 2**k
    cycles = []
    visited_globally = set()

    # Test all odd residue classes
    for start in range(1, mod, 2):
        if start in visited_globally:
            continue

        trajectory = []
        current = start
        visited_local = set()

        for _ in range(max_iterations):
            if current in visited_local:
                # Found a cycle
                cycle_start = trajectory.index(current)
                cycle = trajectory[cycle_start:]

                # Check if cycle contains 1
                if 1 in cycle:
                    # This is the trivial cycle
                    pass
                else:
                    # This is a fake cycle!
                    cycles.append(cycle)

                # Mark all elements in trajectory as visited
                visited_globally.update(trajectory)
                break

            visited_local.add(current)
            trajectory.append(current)
            current = syracuse_mod(current, k)

            if current == 1:
                # Reached the trivial cycle
                visited_globally.update(trajectory)
                break

    return cycles

def analyze_fake_cycles(k):
    """Analyze the fake cycles at a given k"""
    cycles = find_cycles_mod_k(k)

    print(f"\n{'='*60}")
    print(f"k = {k} (mod {2**k})")
    print(f"{'='*60}")

    if not cycles:
        print(f"✓ k = {k} is CLEAN (no fake cycles)")
    else:
        print(f"✗ k = {k} has {len(cycles)} fake cycle(s)")

        for i, cycle in enumerate(cycles, 1):
            print(f"\nFake Cycle {i}: length {len(cycle)}")
            print(f"  Elements: {cycle[:10]}{'...' if len(cycle) > 10 else ''}")

            # Analyze growth factor
            growth_factor = 1
            for c in cycle:
                # Count how many times we multiply by 3
                val = 3 * c + 1
                v2 = 0
                while val % 2 == 0:
                    val //= 2
                    v2 += 1
                growth_factor *= 3 / (2**v2)

            print(f"  Growth factor per cycle: {growth_factor:.6f}")
            print(f"  Log₂(growth): {math.log2(growth_factor):.6f}")

            # Look for patterns in the cycle elements
            print(f"  Min element: {min(cycle)}")
            print(f"  Max element: {max(cycle)}")

            # Check divisibility patterns
            for p in [3, 5, 7, 11, 13]:
                residues = set(c % p for c in cycle)
                if len(residues) < p - 1:  # Skips some residues
                    print(f"  Mod {p} residues: {sorted(residues)}")

def analyze_special_k_values():
    """Analyze what makes k=10,11,12,20 special"""
    special_k = [10, 11, 12, 20]
    clean_k = [13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24]

    print("\n" + "="*60)
    print("SPECIAL K VALUES (with fake cycles)")
    print("="*60)

    for k in special_k:
        analyze_fake_cycles(k)

    print("\n" + "="*60)
    print("CLEAN K VALUES (for comparison)")
    print("="*60)

    for k in clean_k[:4]:  # Just check a few
        analyze_fake_cycles(k)

    # Look for patterns
    print("\n" + "="*60)
    print("PATTERN ANALYSIS")
    print("="*60)

    # Check if k values have special properties
    print("\nSpecial k values:")
    for k in special_k:
        factors = []
        temp = k
        for p in [2, 3, 5, 7, 11]:
            while temp % p == 0:
                factors.append(p)
                temp //= p
        if temp > 1:
            factors.append(temp)

        print(f"  k = {k} = {' × '.join(map(str, factors)) if factors else str(k)}")
        print(f"    2^k mod 3 = {(2**k) % 3}")
        print(f"    2^k mod 9 = {(2**k) % 9}")
        print(f"    3^(k/2) if k even = {3**(k//2) if k % 2 == 0 else 'N/A'}")

        # Check relationship to convergents of log₂(3)
        log2_3 = math.log2(3)
        convergent_quality = abs(k * log2_3 - round(k * log2_3))
        print(f"    Distance to k·log₂(3) integer: {convergent_quality:.6f}")

def search_for_pattern():
    """Search for algebraic pattern in clean vs non-clean k"""
    print("\n" + "="*60)
    print("SEARCHING FOR ALGEBRAIC PATTERN")
    print("="*60)

    # Test k values up to 50 to find more non-clean ones
    non_clean = []
    clean = []

    for k in range(3, 51):
        cycles = find_cycles_mod_k(k)
        if cycles:
            non_clean.append(k)
        else:
            clean.append(k)

    print(f"\nNon-clean k in [3, 50]: {non_clean}")
    print(f"Clean k count: {len(clean)}")

    # Analyze gaps between non-clean k
    if len(non_clean) > 1:
        gaps = [non_clean[i+1] - non_clean[i] for i in range(len(non_clean)-1)]
        print(f"\nGaps between non-clean k: {gaps}")
        print(f"Max gap: {max(gaps) if gaps else 'N/A'}")

    # Check if non-clean k have common properties
    print("\nProperties of non-clean k:")
    for k in non_clean[:10]:  # Limit output
        # Check ord₂(3^q - 1) for various q
        for q in range(1, k+1):
            val = (3**q - 1) % (2**k)
            if val == 0:
                print(f"  k={k}: 3^{q} ≡ 1 (mod 2^{k})")
                break

        # Check if k divides ord₂(3)
        ord_2_3 = 1
        val = 3
        while val % (2**k) != 1:
            val = (val * 3) % (2**k)
            ord_2_3 += 1
            if ord_2_3 > 2**k:  # Prevent infinite loop
                break

        if ord_2_3 <= 2**k:
            print(f"  k={k}: ord_{2**k}(3) = {ord_2_3}")
            if k in [10, 11, 12, 20]:
                print(f"    Special: {ord_2_3} divides 2^k? {(2**k) % ord_2_3 == 0}")

def main():
    print("CLEAN K ALGEBRAIC STRUCTURE ANALYSIS")
    print("="*60)

    # Analyze the known non-clean k values
    analyze_special_k_values()

    # Search for patterns
    search_for_pattern()

    print("\n" + "="*60)
    print("CONCLUSIONS")
    print("="*60)
    print("""
Based on this analysis, we should look for:
1. Relationship to the multiplicative order of 3 mod 2^k
2. Connection to lifting of cycles from smaller k values
3. Special divisibility conditions that enable fake cycles
4. Whether the pattern continues beyond k=100
    """)

if __name__ == "__main__":
    main()