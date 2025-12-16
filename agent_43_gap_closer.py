#!/usr/bin/env python3
"""
Agent 43: Gap Closer - Computational Framework
Attempting to close the gap in Collatz proof

The gap: Sequence of ≡1 (mod 4) values is not monotone decreasing
Goal: Find additional property that forces descent to 1
"""

from collections import defaultdict
import sys

def collatz_step(n):
    """Single Collatz step"""
    if n % 2 == 0:
        return n // 2
    else:
        return 3 * n + 1

def get_mod4_1_sequence(n, max_steps=10000):
    """
    Get sequence of values ≡ 1 (mod 4) in trajectory from n
    Returns: list of (step_number, value) tuples
    """
    sequence = []
    current = n
    step = 0

    if current % 4 == 1:
        sequence.append((step, current))

    while current != 1 and step < max_steps:
        current = collatz_step(current)
        step += 1
        if current % 4 == 1:
            sequence.append((step, current))

    return sequence

def analyze_mod4_1_sequence(n):
    """
    Analyze the ≡1 (mod 4) sequence for a given starting value
    Returns dict with various statistics
    """
    seq = get_mod4_1_sequence(n)
    if len(seq) < 2:
        return None

    values = [v for _, v in seq]

    # Count increases and decreases
    increases = 0
    decreases = 0
    increase_ratios = []
    max_increase = 0
    max_increase_pair = None

    for i in range(len(values) - 1):
        if values[i+1] > values[i]:
            increases += 1
            ratio = values[i+1] / values[i]
            increase_ratios.append(ratio)
            inc = values[i+1] - values[i]
            if inc > max_increase:
                max_increase = inc
                max_increase_pair = (values[i], values[i+1])
        else:
            decreases += 1

    # Check eventual monotonicity
    eventually_monotone = False
    monotone_from_index = None
    for start_idx in range(len(values)):
        is_monotone = all(values[i+1] < values[i]
                         for i in range(start_idx, len(values)-1))
        if is_monotone:
            eventually_monotone = True
            monotone_from_index = start_idx
            break

    # Compute liminf (minimum of tail values)
    liminf = min(values)

    return {
        'n': n,
        'sequence_length': len(values),
        'values': values,
        'increases': increases,
        'decreases': decreases,
        'max_increase': max_increase,
        'max_increase_pair': max_increase_pair,
        'increase_ratios': increase_ratios,
        'max_ratio': max(increase_ratios) if increase_ratios else 1.0,
        'eventually_monotone': eventually_monotone,
        'monotone_from_index': monotone_from_index,
        'liminf': liminf,
        'reaches_1': values[-1] == 1
    }

# ============================================================================
# APPROACH A: LIMINF = 1
# ============================================================================

def test_liminf_approach(test_range=1000):
    """
    Test if lim inf vᵢ = 1 for all trajectories
    """
    print("=" * 70)
    print("APPROACH A: Testing lim inf vᵢ = 1")
    print("=" * 70)

    counterexamples = []

    for n in range(1, test_range, 2):  # odd numbers only
        stats = analyze_mod4_1_sequence(n)
        if stats is None:
            continue

        if stats['liminf'] != 1:
            counterexamples.append((n, stats['liminf']))

    print(f"\nTested {test_range//2} odd numbers")
    print(f"Counterexamples (liminf ≠ 1): {len(counterexamples)}")

    if counterexamples:
        print("\nFirst 10 counterexamples:")
        for n, liminf in counterexamples[:10]:
            print(f"  n={n}: liminf = {liminf}")
        return False
    else:
        print("✓ All tested trajectories have liminf = 1")
        return True

# ============================================================================
# APPROACH B: BOUNDED GROWTH
# ============================================================================

def test_bounded_growth(test_range=1000):
    """
    Test if increases are bounded: vᵢ₊₁ ≤ C·vᵢ for some constant C
    """
    print("\n" + "=" * 70)
    print("APPROACH B: Testing bounded growth ratios")
    print("=" * 70)

    all_ratios = []

    for n in range(1, test_range, 2):
        stats = analyze_mod4_1_sequence(n)
        if stats is None or not stats['increase_ratios']:
            continue

        all_ratios.extend(stats['increase_ratios'])

    if not all_ratios:
        print("No increases found!")
        return True

    max_ratio = max(all_ratios)
    avg_ratio = sum(all_ratios) / len(all_ratios)

    print(f"\nTotal increases observed: {len(all_ratios)}")
    print(f"Maximum ratio (vᵢ₊₁/vᵢ): {max_ratio:.2f}")
    print(f"Average ratio: {avg_ratio:.2f}")

    # Check distribution
    ratio_bins = defaultdict(int)
    for r in all_ratios:
        if r < 2:
            ratio_bins['1-2x'] += 1
        elif r < 5:
            ratio_bins['2-5x'] += 1
        elif r < 10:
            ratio_bins['5-10x'] += 1
        elif r < 50:
            ratio_bins['10-50x'] += 1
        elif r < 100:
            ratio_bins['50-100x'] += 1
        else:
            ratio_bins['100x+'] += 1

    print("\nRatio distribution:")
    for bin_name in ['1-2x', '2-5x', '5-10x', '10-50x', '50-100x', '100x+']:
        count = ratio_bins[bin_name]
        if count > 0:
            print(f"  {bin_name}: {count} ({100*count/len(all_ratios):.1f}%)")

    # Find worst cases
    print("\nWorst growth cases:")
    for n in range(1, min(200, test_range), 2):
        stats = analyze_mod4_1_sequence(n)
        if stats and stats['max_ratio'] > 10:
            print(f"  n={n}: max ratio {stats['max_ratio']:.2f}, "
                  f"jump {stats['max_increase_pair']}")

    return max_ratio

# ============================================================================
# APPROACH C: EVENTUAL MONOTONICITY
# ============================================================================

def test_eventual_monotonicity(test_range=1000):
    """
    Test if sequence eventually becomes strictly decreasing
    """
    print("\n" + "=" * 70)
    print("APPROACH C: Testing eventual monotonicity")
    print("=" * 70)

    eventually_monotone_count = 0
    never_monotone_count = 0
    always_monotone_count = 0

    for n in range(1, test_range, 2):
        stats = analyze_mod4_1_sequence(n)
        if stats is None:
            continue

        if stats['eventually_monotone']:
            if stats['monotone_from_index'] == 0:
                always_monotone_count += 1
            else:
                eventually_monotone_count += 1
        else:
            never_monotone_count += 1

    total = eventually_monotone_count + never_monotone_count + always_monotone_count

    print(f"\nTested {total} trajectories:")
    print(f"  Always monotone: {always_monotone_count} ({100*always_monotone_count/total:.1f}%)")
    print(f"  Eventually monotone: {eventually_monotone_count} ({100*eventually_monotone_count/total:.1f}%)")
    print(f"  Never monotone: {never_monotone_count} ({100*never_monotone_count/total:.1f}%)")

    if never_monotone_count == 0:
        print("\n✓ All trajectories are eventually monotone!")
        return True
    else:
        print(f"\n✗ {never_monotone_count} trajectories never become monotone")

        # Find examples
        print("\nExamples of never-monotone sequences:")
        count = 0
        for n in range(1, test_range, 2):
            stats = analyze_mod4_1_sequence(n)
            if stats and not stats['eventually_monotone']:
                print(f"  n={n}: sequence = {stats['values']}")
                count += 1
                if count >= 5:
                    break

        return False

# ============================================================================
# APPROACH D: FINER MODULAR CLASS
# ============================================================================

def get_mod_k_sequence(n, k=16, residue=1, max_steps=10000):
    """
    Get sequence of values ≡ residue (mod k) in trajectory from n
    """
    sequence = []
    current = n
    step = 0

    if current % k == residue:
        sequence.append((step, current))

    while current != 1 and step < max_steps:
        current = collatz_step(current)
        step += 1
        if current % k == residue:
            sequence.append((step, current))

    return sequence

def test_finer_modular_class(test_range=200):
    """
    Test if using ≡1 (mod 16) or ≡1 (mod 32) gives monotone descent
    """
    print("\n" + "=" * 70)
    print("APPROACH D: Testing finer modular classes")
    print("=" * 70)

    for modulus in [16, 32, 64]:
        print(f"\n--- Testing ≡1 (mod {modulus}) ---")

        monotone_count = 0
        non_monotone_count = 0
        no_sequence_count = 0

        for n in range(1, test_range, 2):
            seq = get_mod_k_sequence(n, k=modulus, residue=1)

            if len(seq) < 2:
                no_sequence_count += 1
                continue

            values = [v for _, v in seq]

            # Check if monotone decreasing
            is_monotone = all(values[i+1] < values[i] for i in range(len(values)-1))

            if is_monotone:
                monotone_count += 1
            else:
                non_monotone_count += 1
                if non_monotone_count <= 3:  # Show first few
                    print(f"  Non-monotone at n={n}: {values}")

        total = monotone_count + non_monotone_count
        if total > 0:
            print(f"  Trajectories with ≥2 hits: {total}")
            print(f"  Monotone: {monotone_count} ({100*monotone_count/total:.1f}%)")
            print(f"  Non-monotone: {non_monotone_count} ({100*non_monotone_count/total:.1f}%)")

        if non_monotone_count == 0 and total > 0:
            print(f"  ✓ All sequences are monotone!")
            return modulus

    return None

# ============================================================================
# MAIN ANALYSIS
# ============================================================================

def main():
    print("AGENT 43: GAP CLOSER - Computational Exploration")
    print("=" * 70)
    print()

    test_range = 500

    # Test each approach
    liminf_holds = test_liminf_approach(test_range)
    max_ratio = test_bounded_growth(test_range)
    eventually_monotone = test_eventual_monotonicity(test_range)
    finer_modulus = test_finer_modular_class(test_range)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY OF APPROACHES")
    print("=" * 70)
    print()
    print(f"A. Liminf = 1: {'✓ HOLDS' if liminf_holds else '✗ FAILS'}")
    print(f"B. Bounded growth: Max ratio = {max_ratio:.2f}x")
    print(f"C. Eventual monotonicity: {'✓ HOLDS' if eventually_monotone else '✗ FAILS'}")
    print(f"D. Finer modular class: {f'✓ mod {finer_modulus} works' if finer_modulus else '✗ None found'}")
    print()

    # Next steps
    print("=" * 70)
    print("RECOMMENDATIONS FOR RIGOROUS PROOF")
    print("=" * 70)
    print()

    if liminf_holds:
        print("✓ APPROACH A looks PROMISING:")
        print("  - All tested trajectories have liminf = 1")
        print("  - Need to prove: Why must liminf equal 1?")
        print("  - Key insight: S(m) < m for m ≡ 1 (mod 4)")
        print()

    if max_ratio < 100:
        print(f"✓ APPROACH B has potential:")
        print(f"  - Observed max ratio: {max_ratio:.2f}x")
        print(f"  - Could bound be proven theoretically?")
        print()

    if eventually_monotone:
        print("✓ APPROACH C is VERY PROMISING:")
        print("  - All tested sequences eventually monotone")
        print("  - Need to prove: Why does non-monotonicity stop?")
        print()

if __name__ == "__main__":
    main()
