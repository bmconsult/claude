#!/usr/bin/env python3
"""
Verify: Do all functions in the same S_n orbit have the same formula complexity?

This should be TRUE: if f has formula of size s, then σ(f) also has formula of size s
(just permute variable names).
"""

import numpy as np
from math import factorial
from itertools import permutations
from collections import defaultdict

def apply_permutation(tt, perm, n):
    """Apply permutation to truth table (permute variable indices)."""
    N = 2**n
    inv_perm = [0] * n
    for i, p in enumerate(perm):
        inv_perm[p] = i

    new_tt = [0] * N
    for x in range(N):
        new_x = sum(((x >> inv_perm[i]) & 1) << i for i in range(n))
        new_tt[x] = tt[new_x]

    return tuple(new_tt)

def compute_full_orbit(tt, n):
    """Compute complete S_n orbit of truth table."""
    orbit = set()
    for perm in permutations(range(n)):
        new_tt = apply_permutation(tt, perm, n)
        orbit.add(new_tt)
    return orbit

def formula_complexity(tt, n, max_size=6):
    """
    Compute minimum formula size for truth table.
    Exhaustive search up to max_size.
    """
    N = 2**n

    # Check constants
    if all(b == 0 for b in tt):
        return 0, "const_0"
    if all(b == 1 for b in tt):
        return 0, "const_1"

    # Check single variables and their negations
    for i in range(n):
        # Variable x_i
        if all(tt[x] == ((x >> i) & 1) for x in range(N)):
            return 0, f"x_{i}"
        # Negation ~x_i
        if all(tt[x] == 1 - ((x >> i) & 1) for x in range(N)):
            return 0, f"~x_{i}"

    # Build formulas iteratively
    # formulas_by_size[s] = list of (truth_table, formula_str)
    formulas_by_size = {0: []}

    # Size 0: variables and constants
    for i in range(n):
        var_tt = tuple((x >> i) & 1 for x in range(N))
        neg_tt = tuple(1 - ((x >> i) & 1) for x in range(N))
        formulas_by_size[0].append((var_tt, f"x_{i}"))
        formulas_by_size[0].append((neg_tt, f"~x_{i}"))
    formulas_by_size[0].append((tuple([0]*N), "0"))
    formulas_by_size[0].append((tuple([1]*N), "1"))

    # Check if target is already found
    if tt in [t for t, _ in formulas_by_size[0]]:
        return 0, [f for t, f in formulas_by_size[0] if t == tt][0]

    # Build larger formulas
    all_tts = {t for t, _ in formulas_by_size[0]}

    for s in range(1, max_size + 1):
        formulas_by_size[s] = []
        new_tts = set()

        # Combine smaller formulas
        for s1 in range(s):
            s2 = s - 1 - s1
            if s2 > s1:
                continue  # Avoid duplicates

            for tt1, f1 in formulas_by_size[s1]:
                for tt2, f2 in formulas_by_size[s2]:
                    # AND
                    new_tt = tuple(a & b for a, b in zip(tt1, tt2))
                    if new_tt not in all_tts and new_tt not in new_tts:
                        new_tts.add(new_tt)
                        formulas_by_size[s].append((new_tt, f"({f1} & {f2})"))
                        if new_tt == tt:
                            return s, f"({f1} & {f2})"

                    # OR
                    new_tt = tuple(a | b for a, b in zip(tt1, tt2))
                    if new_tt not in all_tts and new_tt not in new_tts:
                        new_tts.add(new_tt)
                        formulas_by_size[s].append((new_tt, f"({f1} | {f2})"))
                        if new_tt == tt:
                            return s, f"({f1} | {f2})"

                    # XOR
                    new_tt = tuple(a ^ b for a, b in zip(tt1, tt2))
                    if new_tt not in all_tts and new_tt not in new_tts:
                        new_tts.add(new_tt)
                        formulas_by_size[s].append((new_tt, f"({f1} ^ {f2})"))
                        if new_tt == tt:
                            return s, f"({f1} ^ {f2})"

        all_tts.update(new_tts)

    return max_size + 1, "NOT_FOUND"

def main():
    print("VERIFYING: Orbit members have same formula complexity")
    print("=" * 60)

    for n in [3, 4]:
        print(f"\n{'='*60}")
        print(f"n = {n}")
        print(f"{'='*60}")

        N = 2**n

        # Generate all truth tables
        all_tts = list(range(2**N))

        # Group into orbits
        processed = set()
        orbits = []

        for tt_int in all_tts:
            tt = tuple((tt_int >> x) & 1 for x in range(N))
            if tt in processed:
                continue

            orbit = compute_full_orbit(tt, n)
            processed.update(orbit)
            orbits.append(orbit)

        print(f"Total truth tables: {2**N}")
        print(f"Number of orbits: {len(orbits)}")
        print(f"Orbit sizes: {sorted(set(len(o) for o in orbits))}")

        # Check if all orbit members have same complexity
        inconsistent_orbits = []

        for orbit in orbits:
            complexities = {}
            for tt in orbit:
                size, formula = formula_complexity(tt, n, max_size=5)
                complexities[tt] = size

            unique_sizes = set(complexities.values())
            if len(unique_sizes) > 1:
                inconsistent_orbits.append((orbit, complexities))

        print(f"\nOrbits with inconsistent complexity: {len(inconsistent_orbits)}")

        if inconsistent_orbits:
            print("\n⚠ Found inconsistency! Examples:")
            for orbit, comps in inconsistent_orbits[:3]:
                print(f"  Orbit size {len(orbit)}:")
                for tt in list(orbit)[:4]:
                    print(f"    {tt[:8]}...: complexity {comps[tt]}")
        else:
            print("\n✓ All orbits have consistent complexity across members!")
            print("This confirms: S_n-orbit determines formula complexity.")

        # Show complexity distribution by orbit size
        print("\nComplexity by orbit structure:")
        orbit_data = []
        for orbit in orbits:
            rep = list(orbit)[0]
            size, _ = formula_complexity(rep, n, max_size=5)
            orbit_data.append({
                'orbit_size': len(orbit),
                'formula_size': size,
                'rep': rep
            })

        by_orbit_size = defaultdict(list)
        for d in orbit_data:
            by_orbit_size[d['orbit_size']].append(d['formula_size'])

        for orbit_size in sorted(by_orbit_size.keys()):
            sizes = by_orbit_size[orbit_size]
            print(f"  Orbit size {orbit_size}: {len(sizes)} orbits, formula sizes {sorted(set(sizes))}")

if __name__ == "__main__":
    main()
