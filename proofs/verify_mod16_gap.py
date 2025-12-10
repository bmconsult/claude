"""
Verification of the critical gap: n ≡ 15 (mod 16) dynamics
Testing whether orbits can stay in the v=1 regime indefinitely
"""

def nu_2(n):
    """Compute the 2-adic valuation of n"""
    if n == 0:
        return float('inf')
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count

def syracuse(n):
    """Syracuse function: S(n) = (3n+1)/2^{nu_2(3n+1)}"""
    if n % 2 == 0:
        raise ValueError("Syracuse function only defined for odd n")
    numerator = 3 * n + 1
    v = nu_2(numerator)
    return numerator // (2 ** v)

def track_residue_class(n0, modulus, max_steps=100):
    """Track how long an orbit stays in the same residue class"""
    n = n0
    initial_residue = n0 % modulus
    steps_in_class = 0
    orbit = [n]
    residues = [n % modulus]
    valuations = []

    for step in range(max_steps):
        v = nu_2(3*n + 1)
        valuations.append(v)
        n_next = syracuse(n)

        if n_next % modulus == initial_residue:
            steps_in_class += 1
        else:
            break

        orbit.append(n_next)
        residues.append(n_next % modulus)
        n = n_next

        if n == 1:
            break

    return {
        'n0': n0,
        'initial_residue': initial_residue,
        'modulus': modulus,
        'steps_in_class': steps_in_class,
        'orbit': orbit[:20],  # First 20 terms
        'residues': residues[:20],
        'valuations': valuations[:20],
        'escaped': steps_in_class < max_steps and n != 1
    }

def test_critical_residues():
    """Test the critical residue classes identified in the proof"""

    print("=" * 80)
    print("VERIFICATION OF MOD 16 GAP")
    print("=" * 80)

    # Test n ≡ 15 (mod 16)
    print("\n1. Testing n ≡ 15 (mod 16):")
    print("-" * 80)
    test_values_15 = [15, 31, 47, 63, 79, 95, 111, 127, 143, 159]

    for n in test_values_15:
        result = track_residue_class(n, 16, max_steps=50)
        print(f"n={n:4d} (≡{n%16:2d} mod 16): stayed in class for {result['steps_in_class']} steps")
        print(f"  Residues: {result['residues'][:10]}")
        print(f"  Valuations: {result['valuations'][:10]}")

    # Test n ≡ 7 (mod 8)
    print("\n2. Testing n ≡ 7 (mod 8):")
    print("-" * 80)
    test_values_7 = [7, 15, 23, 31, 39, 47, 55, 63, 71, 79]

    for n in test_values_7:
        result = track_residue_class(n, 8, max_steps=50)
        print(f"n={n:4d} (≡{n%8:2d} mod 8): stayed in class for {result['steps_in_class']} steps")

    # Test n ≡ 31 (mod 32)
    print("\n3. Testing n ≡ 31 (mod 32):")
    print("-" * 80)
    test_values_31 = [31, 63, 95, 127, 159, 191, 223, 255]

    max_consecutive_v1 = 0
    for n in test_values_31:
        result = track_residue_class(n, 32, max_steps=50)
        consecutive_v1 = 0
        current_v1_run = 0

        for v in result['valuations']:
            if v == 1:
                current_v1_run += 1
                max_consecutive_v1 = max(max_consecutive_v1, current_v1_run)
            else:
                current_v1_run = 0

        print(f"n={n:4d} (≡{n%32:2d} mod 32): stayed in class for {result['steps_in_class']} steps, max v=1 run: {consecutive_v1}")

    print(f"\nOverall max consecutive v=1 steps: {max_consecutive_v1}")

    # Detailed analysis of n=31
    print("\n4. Detailed analysis of n=31:")
    print("-" * 80)
    n = 31
    orbit = [n]
    for _ in range(30):
        n_next = syracuse(n)
        orbit.append(n_next)
        n = n_next
        if n == 1:
            break

    print(f"First 30 terms of orbit starting from 31:")
    for i, val in enumerate(orbit[:30]):
        v = nu_2(3*val + 1) if val != 1 else 0
        print(f"  n_{i:2d} = {val:10d}, ≡ {val%32:2d} (mod 32), ≡ {val%16:2d} (mod 16), ≡ {val%8:2d} (mod 8), ν₂={v}")

    # Check for patterns in higher moduli
    print("\n5. Testing higher moduli (mod 64, 128, 256):")
    print("-" * 80)

    for mod in [64, 128, 256]:
        print(f"\nMod {mod}:")
        # Test numbers ≡ -1 (mod mod), which is mod-1
        test_val = mod - 1
        result = track_residue_class(test_val, mod, max_steps=30)
        print(f"  n={test_val} (≡{test_val%mod} mod {mod}): stayed {result['steps_in_class']} steps")

    # Statistical analysis
    print("\n6. Statistical analysis: longest runs in v=1 regime")
    print("-" * 80)

    max_runs = {}
    for n in range(1, 1000, 2):  # Odd numbers up to 1000
        orbit = [n]
        current = n
        v1_runs = []
        current_run = 0

        for _ in range(100):
            v = nu_2(3*current + 1)
            if v == 1:
                current_run += 1
            else:
                if current_run > 0:
                    v1_runs.append(current_run)
                current_run = 0

            current = syracuse(current)
            orbit.append(current)
            if current == 1:
                break

        if v1_runs:
            max_run = max(v1_runs)
            if max_run not in max_runs:
                max_runs[max_run] = []
            max_runs[max_run].append(n)

    print("Distribution of maximum v=1 run lengths:")
    for run_length in sorted(max_runs.keys(), reverse=True)[:10]:
        examples = max_runs[run_length][:3]
        print(f"  Max run = {run_length}: {len(max_runs[run_length])} numbers (examples: {examples})")

    print("\n" + "=" * 80)
    print("CONCLUSION:")
    print("=" * 80)
    if max_consecutive_v1 < 10:
        print(f"✓ No orbit tested stayed in v=1 regime for more than {max_consecutive_v1} consecutive steps")
        print("✓ This suggests (but does not prove) that orbits eventually escape to v≥2")
    else:
        print(f"! Found orbits with {max_consecutive_v1} consecutive v=1 steps")
        print("! This is concerning and requires further investigation")

if __name__ == "__main__":
    test_critical_residues()
