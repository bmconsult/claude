#!/usr/bin/env python3
"""
Computational exploration of the modular cascade hypothesis.

Tests whether k consecutive growth steps require increasingly specific
residue classes modulo 2^{k+1}.
"""

def nu_2(n):
    """Compute 2-adic valuation of n."""
    if n == 0:
        return float('inf')
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count

def syracuse(n):
    """Apply Syracuse function S(n) = (3n+1) / 2^{nu_2(3n+1)}."""
    if n % 2 == 0:
        raise ValueError("Syracuse function requires odd input")
    val = nu_2(3*n + 1)
    return (3*n + 1) // (2**val)

def consecutive_growth_length(n, max_steps=50):
    """Count consecutive growth steps starting from n."""
    count = 0
    current = n
    for _ in range(max_steps):
        if nu_2(3*current + 1) == 1:  # Growth step
            count += 1
            current = syracuse(current)
        else:
            break
    return count

def find_residue_class_pattern(k, search_limit=100000):
    """
    Find all n < search_limit with exactly k consecutive growth steps.
    Return the residue classes modulo various powers of 2.
    """
    candidates = []
    for n in range(1, search_limit, 2):  # Only odd numbers
        if consecutive_growth_length(n) >= k:
            candidates.append(n)
        if len(candidates) >= 1000:  # Limit samples
            break

    if not candidates:
        return None

    # Analyze residue classes
    result = {
        'count': len(candidates),
        'first_10': candidates[:10],
    }

    # Check residues modulo 2^j for j = 2 to k+3
    for j in range(2, min(k+4, 12)):
        mod = 2**j
        residues = {}
        for n in candidates:
            r = n % mod
            residues[r] = residues.get(r, 0) + 1

        # Find the dominant residue class(es)
        if residues:
            max_count = max(residues.values())
            dominant = [r for r, count in residues.items() if count >= max_count * 0.5]
            result[f'mod_{mod}'] = {
                'dominant_residues': sorted(dominant),
                'num_classes': len(residues),
                'total_classes_possible': mod // 2,  # Only odd residues
            }

    return result

def test_specific_number(n, steps=20):
    """Trace a specific number through the orbit and check residue classes."""
    print(f"\nTracing n = {n}:")
    print(f"  Initial: n ≡ {n % 4} (mod 4), {n % 8} (mod 8), {n % 16} (mod 16), {n % 32} (mod 32)")

    orbit = [n]
    growth_count = 0
    current = n

    for i in range(steps):
        v = nu_2(3*current + 1)
        next_n = syracuse(current)
        is_growth = (next_n > current)

        if v == 1:
            growth_count += 1
            print(f"  Step {i+1}: {current} -> {next_n} (v={v}, GROWTH)")
        else:
            print(f"  Step {i+1}: {current} -> {next_n} (v={v}, shrink)")
            if growth_count > 0:
                print(f"    → Growth streak ended at {growth_count} steps")
                growth_count = 0

        orbit.append(next_n)
        current = next_n

        if current == 1:
            break

    return orbit

def test_modular_prediction():
    """Test the predicted modular constraints."""
    print("=" * 70)
    print("TEST 1: Modular Cascade Verification")
    print("=" * 70)

    predictions = {
        1: (4, 3, "n ≡ 3 (mod 4) for 1 growth step"),
        2: (8, 7, "n ≡ 7 (mod 8) for 2 consecutive growth steps"),
        3: (16, 15, "n ≡ 15 (mod 16) for 3 consecutive growth steps"),
    }

    for k, (mod, expected_residue, description) in predictions.items():
        print(f"\n{description}")
        result = find_residue_class_pattern(k)

        if result:
            print(f"  Found {result['count']} candidates")
            print(f"  First 10: {result['first_10']}")

            key = f'mod_{mod}'
            if key in result:
                info = result[key]
                print(f"  Dominant residue classes mod {mod}: {info['dominant_residues']}")

                if expected_residue in info['dominant_residues']:
                    print(f"  ✓ CONFIRMED: {expected_residue} is dominant")
                else:
                    print(f"  ✗ UNEXPECTED: {expected_residue} not found!")
                    print(f"     Instead found: {info['dominant_residues']}")
        else:
            print(f"  ✗ No candidates found!")

def test_long_growth_phases():
    """Find the longest consecutive growth phases."""
    print("\n" + "=" * 70)
    print("TEST 2: Longest Consecutive Growth Phases")
    print("=" * 70)

    max_length_found = 0
    max_n = None

    # Distribution of growth lengths
    length_distribution = {}

    test_range = 1000000
    print(f"\nSearching n ∈ [1, {test_range}] (odd only)...")

    for n in range(1, test_range, 2):
        length = consecutive_growth_length(n)

        if length > 0:
            length_distribution[length] = length_distribution.get(length, 0) + 1

        if length > max_length_found:
            max_length_found = length
            max_n = n
            print(f"  New record: {length} consecutive growth steps starting from n = {n}")

    print(f"\nMaximum consecutive growth: {max_length_found} steps (starting from n = {max_n})")
    print("\nDistribution of growth phase lengths:")
    for length in sorted(length_distribution.keys()):
        count = length_distribution[length]
        theoretical = test_range / (2 ** (length + 1))  # Approx expected count
        print(f"  {length} steps: {count} occurrences (expected ~{theoretical:.0f})")

def test_density_decay():
    """Estimate the density of R_k (numbers allowing k consecutive growth)."""
    print("\n" + "=" * 70)
    print("TEST 3: Density Decay of R_k")
    print("=" * 70)

    N = 500000
    print(f"\nSampling N = {N} odd numbers...")

    densities = {}
    for k in range(1, 11):
        count = 0
        for n in range(1, N, 2):
            if consecutive_growth_length(n) >= k:
                count += 1
        density = count / (N // 2)
        densities[k] = density

        theoretical = 1 / (2 ** k)
        ratio = density / theoretical if theoretical > 0 else 0

        print(f"  k={k}: density = {density:.6f}, theoretical = {theoretical:.6f}, ratio = {ratio:.3f}")

    # Fit exponential model
    print("\nFitting exponential model: density(k) ≈ A * λ^k")
    if len(densities) >= 3:
        import math
        # Use ratio of consecutive densities to estimate λ
        ratios = []
        for k in range(2, min(8, len(densities))):
            if densities[k] > 0 and densities[k-1] > 0:
                ratio = densities[k] / densities[k-1]
                ratios.append(ratio)

        if ratios:
            avg_ratio = sum(ratios) / len(ratios)
            print(f"  Average ratio: λ ≈ {avg_ratio:.4f}")
            print(f"  Compare to 1/2 = {0.5:.4f}")
            print(f"  Compare to 2/3 = {2/3:.4f} (critical threshold)")

            if avg_ratio < 2/3:
                print(f"  ✓ λ < 2/3: Growth contribution is bounded!")
            else:
                print(f"  ✗ λ ≥ 2/3: Cannot immediately conclude boundedness")

def test_77671():
    """Test the specific number known to have a long growth phase."""
    print("\n" + "=" * 70)
    print("TEST 4: Analysis of n = 77,671")
    print("=" * 70)

    n = 77671
    print(f"\n77,671 ≡ {n % 4} (mod 4) [expect 3]")
    print(f"77,671 ≡ {n % 8} (mod 8) [expect 7 for 2+ growth]")
    print(f"77,671 ≡ {n % 16} (mod 16) [expect 15 for 3+ growth]")
    print(f"77,671 ≡ {n % 32} (mod 32)")
    print(f"77,671 ≡ {n % 64} (mod 64)")

    length = consecutive_growth_length(n)
    print(f"\nActual consecutive growth length: {length}")

    # Trace first few steps
    orbit = test_specific_number(n, steps=20)

def main():
    """Run all tests."""
    print("MODULAR CASCADE COMPUTATIONAL EXPLORATION")
    print("Testing the hypothesis that k consecutive growth steps")
    print("require n in increasingly restrictive residue classes.")

    test_modular_prediction()
    test_long_growth_phases()
    test_density_decay()
    test_77671()

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
The computational tests aim to verify:
1. Modular cascade: k steps ⟹ n ≡ r_k (mod 2^{k+1})
2. Density decay: |R_k| / N ≈ 1/2^k or faster
3. Bounded growth: No orbit has unbounded consecutive growth

If density decays faster than (2/3)^k, then total growth contribution
is bounded even if infinitely many growth phases occur.
""")

if __name__ == "__main__":
    main()
