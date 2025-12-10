#!/usr/bin/env python3
"""
V=1 ESCAPE GAP ANALYSIS
========================

Goal: Prove that Syracuse orbits cannot stay in the v=1 regime (n ≡ 3 mod 4) forever.

Approach: Exhaustive modular case analysis at increasing powers of 2.

Key facts:
- S(n) > n ⟺ ν₂(3n+1) = 1 ⟺ n ≡ 3 (mod 4)
- For n = 4m+3: S(n) = 6m+5
- S(n) ≡ 1 (mod 4) if m even (n ≡ 3 mod 8) - ESCAPES v=1
- S(n) ≡ 3 (mod 4) if m odd (n ≡ 7 mod 8) - STAYS in v=1
"""

def nu_2(n):
    """Compute 2-adic valuation of n."""
    if n == 0:
        return float('inf')
    v = 0
    while n % 2 == 0:
        v += 1
        n //= 2
    return v

def syracuse(n):
    """Apply Syracuse function S(n) = (3n+1) / 2^{ν₂(3n+1)}."""
    if n % 2 == 0:
        raise ValueError("Syracuse function only defined for odd n")
    m = 3 * n + 1
    v = nu_2(m)
    return m // (2 ** v)

def analyze_residue_class_dynamics(modulus):
    """
    For each residue class n ≡ r (mod modulus) with r odd,
    compute where S(n) lands modulo modulus.

    Returns dict: r -> set of possible S(n) mod modulus
    """
    dynamics = {}

    for r in range(1, modulus, 2):  # Only odd residues
        # Check a few representatives to see where they map
        targets = set()
        for k in range(10):  # Check 10 representatives
            n = r + k * modulus
            try:
                s_n = syracuse(n)
                targets.add(s_n % modulus)
            except:
                pass

        dynamics[r] = targets

    return dynamics

def find_v1_residues(modulus):
    """
    Find all residue classes r (mod modulus) where ν₂(3r+1) = 1.
    These are precisely the classes r ≡ 3 (mod 4).
    """
    v1_residues = []
    for r in range(1, modulus, 2):
        if r % 4 == 3:
            v1_residues.append(r)
    return v1_residues

def check_escape_property(modulus):
    """
    Check if every v=1 residue class eventually escapes to a non-v=1 class.

    Returns:
    - True if all v=1 classes escape
    - False if some v=1 class can map to another v=1 class
    - Dict with detailed info
    """
    v1_residues = find_v1_residues(modulus)
    dynamics = analyze_residue_class_dynamics(modulus)

    results = {
        'modulus': modulus,
        'v1_residues': v1_residues,
        'can_stay_in_v1': [],
        'must_escape_v1': [],
        'analysis': {}
    }

    for r in v1_residues:
        targets = dynamics.get(r, set())

        # Check if any target is also a v=1 residue
        v1_targets = [t for t in targets if t % 4 == 3]

        results['analysis'][r] = {
            'targets': sorted(targets),
            'v1_targets': sorted(v1_targets),
            'escapes': len(v1_targets) == 0
        }

        if v1_targets:
            results['can_stay_in_v1'].append(r)
        else:
            results['must_escape_v1'].append(r)

    return results

def trace_orbit_modular(n, modulus, max_steps=100):
    """
    Trace the orbit of n, tracking residue class mod modulus and whether in v=1.

    Returns list of (n, n mod modulus, v, in_v1_regime)
    """
    orbit = []
    current = n

    for step in range(max_steps):
        v = nu_2(3 * current + 1)
        in_v1 = (current % 4 == 3)

        orbit.append({
            'n': current,
            'residue': current % modulus,
            'v': v,
            'in_v1': in_v1
        })

        if current == 1:
            break

        current = syracuse(current)

    return orbit

def find_longest_v1_streak(start_residue, modulus, max_n=1000000, max_streak=50):
    """
    Among numbers ≡ start_residue (mod modulus), find the longest v=1 streak.
    """
    longest_streak = 0
    longest_n = None

    for k in range(min(100, max_n // modulus)):
        n = start_residue + k * modulus
        if n % 2 == 0:
            continue

        current = n
        streak = 0

        for _ in range(max_streak):
            if current % 4 != 3:
                break
            streak += 1
            current = syracuse(current)
            if current == 1:
                break

        if streak > longest_streak:
            longest_streak = streak
            longest_n = n

    return longest_streak, longest_n

def exhaustive_mod_analysis(max_power=12):
    """
    Exhaustive analysis for moduli 2^k, k = 2, 3, ..., max_power.
    """
    print("="*80)
    print("EXHAUSTIVE MODULAR ANALYSIS OF V=1 ESCAPE")
    print("="*80)
    print()

    for power in range(2, max_power + 1):
        modulus = 2 ** power
        print(f"\n{'='*80}")
        print(f"MODULUS: 2^{power} = {modulus}")
        print(f"{'='*80}\n")

        results = check_escape_property(modulus)

        v1_count = len(results['v1_residues'])
        can_stay_count = len(results['can_stay_in_v1'])
        must_escape_count = len(results['must_escape_v1'])

        print(f"Total v=1 residue classes: {v1_count}")
        print(f"Classes that can stay in v=1: {can_stay_count}")
        print(f"Classes that must escape v=1: {must_escape_count}")
        print()

        if can_stay_count > 0:
            print(f"CRITICAL: Found {can_stay_count} classes that can potentially stay in v=1:")
            print()

            for r in results['can_stay_in_v1'][:10]:  # Show first 10
                info = results['analysis'][r]
                print(f"  r = {r} (mod {modulus}):")
                print(f"    Can map to v=1 classes: {info['v1_targets']}")

                # Find longest streak for this residue class
                streak, example_n = find_longest_v1_streak(r, modulus)
                print(f"    Longest v=1 streak found: {streak} steps (starting from n={example_n})")
                print()
        else:
            print("✓ ALL v=1 classes escape in one step at this modulus!")
            print()

def detailed_case_study(n, max_steps=50):
    """
    Detailed trace of a specific number's orbit.
    """
    print(f"\n{'='*80}")
    print(f"DETAILED CASE STUDY: n = {n}")
    print(f"{'='*80}\n")

    for power in range(3, 11):
        modulus = 2 ** power
        orbit = trace_orbit_modular(n, modulus, max_steps=max_steps)

        v1_streak = 0
        max_v1_streak = 0

        for step in orbit:
            if step['in_v1']:
                v1_streak += 1
                max_v1_streak = max(max_v1_streak, v1_streak)
            else:
                v1_streak = 0

        print(f"mod {modulus:4d}: max v=1 streak = {max_v1_streak:2d}")

    print("\nFull orbit details (first 20 steps):")
    print(f"{'Step':>4} {'n':>10} {'mod 8':>6} {'v':>2} {'in_v1':>6} {'S(n)>n':>7}")
    print("-" * 50)

    current = n
    for step in range(min(20, max_steps)):
        v = nu_2(3 * current + 1)
        in_v1 = (current % 4 == 3)
        next_val = syracuse(current)
        grows = next_val > current

        print(f"{step:4d} {current:10d} {current % 8:6d} {v:2d} {str(in_v1):>6} {str(grows):>7}")

        if current == 1:
            break
        current = next_val

def theoretical_analysis():
    """
    Theoretical analysis of the mod 2^k dynamics.
    """
    print("\n" + "="*80)
    print("THEORETICAL ANALYSIS")
    print("="*80 + "\n")

    print("For n ≡ 3 (mod 4), we have n = 4m + 3, so:")
    print("  S(n) = (3n+1)/2 = (12m+10)/2 = 6m+5")
    print()
    print("The question: what is 6m+5 (mod 4)?")
    print("  - If m ≡ 0 (mod 2): 6m+5 ≡ 5 ≡ 1 (mod 4)  → ESCAPES v=1")
    print("  - If m ≡ 1 (mod 2): 6m+5 ≡ 11 ≡ 3 (mod 4) → STAYS in v=1")
    print()
    print("Now, n = 4m+3:")
    print("  - m even (m=2k) → n = 8k+3 ≡ 3 (mod 8)")
    print("  - m odd (m=2k+1) → n = 8k+7 ≡ 7 (mod 8)")
    print()
    print("Therefore:")
    print("  - n ≡ 3 (mod 8) → S(n) ≡ 1 (mod 4) → ESCAPES")
    print("  - n ≡ 7 (mod 8) → S(n) ≡ 3 (mod 4) → CAN STAY")
    print()
    print("The key question: Can we refine this analysis at higher moduli?")
    print("Does n ≡ 7 (mod 8) always map to something that can continue v=1,")
    print("or do higher-order bits force eventual escape?")
    print()

def search_for_persistent_v1_orbits(max_n=10000000, min_streak=20):
    """
    Search for orbits that stay in v=1 for unusually long.
    """
    print("\n" + "="*80)
    print("SEARCHING FOR PERSISTENT V=1 ORBITS")
    print("="*80 + "\n")
    print(f"Searching n up to {max_n}, looking for v=1 streaks ≥ {min_streak}...")
    print()

    candidates = []

    # Focus on n ≡ 7 (mod 8) since those can potentially stay in v=1
    for n in range(7, min(max_n, 1000000), 8):
        current = n
        streak = 0

        for _ in range(min_streak + 10):
            if current % 4 != 3:
                break
            streak += 1
            current = syracuse(current)
            if current == 1:
                break

        if streak >= min_streak:
            candidates.append((n, streak))

    if candidates:
        print(f"Found {len(candidates)} numbers with v=1 streak ≥ {min_streak}:")
        print()
        for n, streak in sorted(candidates, key=lambda x: -x[1])[:10]:
            print(f"  n = {n:10d}: v=1 streak of {streak} steps")
            # Show the modular pattern
            print(f"    Binary: {bin(n)}")
            for p in range(3, 8):
                print(f"    n ≡ {n % (2**p):3d} (mod {2**p:3d})")
            print()
    else:
        print(f"No orbits found with v=1 streak ≥ {min_streak}")
        print("This suggests v=1 streaks are bounded!")

def algebraic_constraint_analysis():
    """
    Analyze algebraic constraints on staying in v=1 regime.
    """
    print("\n" + "="*80)
    print("ALGEBRAIC CONSTRAINT ANALYSIS")
    print("="*80 + "\n")

    print("To stay in v=1 forever, we need:")
    print("  n₀ ≡ 3 (mod 4)")
    print("  n₁ = S(n₀) ≡ 3 (mod 4)")
    print("  n₂ = S(n₁) ≡ 3 (mod 4)")
    print("  ...")
    print()
    print("Let's trace the constraint propagation:")
    print()

    # Starting from n ≡ 7 (mod 2^k), where does it go?
    for power in range(3, 11):
        modulus = 2 ** power
        # Find the residues ≡ 7 (mod 8) within this modulus

        print(f"mod {modulus}:")

        residues_mod_8_eq_7 = [r for r in range(7, modulus, 8)]

        # For each, see where it maps
        always_v1 = []
        sometimes_v1 = []
        never_v1 = []

        for r in residues_mod_8_eq_7:
            # Check several representatives
            targets_v1 = []
            targets_non_v1 = []

            for k in range(5):
                n = r + k * modulus
                s_n = syracuse(n)
                if s_n % 4 == 3:
                    targets_v1.append(s_n % modulus)
                else:
                    targets_non_v1.append(s_n % modulus)

            if targets_non_v1:
                if targets_v1:
                    sometimes_v1.append(r)
                else:
                    never_v1.append(r)
            else:
                always_v1.append(r)

        print(f"  Total residues ≡ 7 (mod 8): {len(residues_mod_8_eq_7)}")
        print(f"  Always map to v=1: {len(always_v1)}")
        print(f"  Sometimes map to v=1: {len(sometimes_v1)}")
        print(f"  Never map to v=1: {len(never_v1)}")

        if always_v1:
            print(f"  CRITICAL: Residues that always stay in v=1: {always_v1[:5]}")
        print()

if __name__ == "__main__":
    theoretical_analysis()
    exhaustive_mod_analysis(max_power=10)
    search_for_persistent_v1_orbits(max_n=10000000, min_streak=15)
    algebraic_constraint_analysis()

    # Detailed case studies
    interesting_cases = [7, 15, 31, 63, 127, 255, 27]
    for n in interesting_cases:
        detailed_case_study(n, max_steps=30)

    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
