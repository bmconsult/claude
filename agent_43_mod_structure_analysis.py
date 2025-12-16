#!/usr/bin/env python3
"""
Deeper analysis of modular structure to understand eventual monotonicity
"""

def collatz_step(n):
    if n % 2 == 0:
        return n // 2
    else:
        return 3 * n + 1

def S(m):
    """Next odd value in trajectory from m"""
    n = collatz_step(m)
    while n % 2 == 0:
        n = n // 2
    return n

def analyze_S_mod_structure():
    """
    For m ≡ 1 (mod 4), analyze when S(m) ≡ 1 (mod 4) vs S(m) ≡ 3 (mod 4)
    """
    print("=" * 70)
    print("ANALYSIS: When does S(m) ≡ 1 (mod 4)?")
    print("=" * 70)
    print()

    # Check pattern for m ≡ 1 (mod 4)
    results = {}

    for mod in [8, 16, 32, 64]:
        print(f"\n--- Modulo {mod} ---")
        for r in range(1, mod, 4):  # r ≡ 1 (mod 4)
            if r % 4 != 1:
                continue

            # Test with several values
            s_mod4_values = []
            for k in range(10):
                m = r + k * mod
                s = S(m)
                s_mod4_values.append(s % 4)

            # Check if consistent
            if len(set(s_mod4_values)) == 1:
                s_mod4 = s_mod4_values[0]
                results[(mod, r)] = s_mod4
                symbol = "✓" if s_mod4 == 1 else "↑"
                print(f"  m ≡ {r:3d} (mod {mod}): S(m) ≡ {s_mod4} (mod 4) {symbol}")

def analyze_trajectory_to_next_mod4_1():
    """
    Analyze the trajectory from S(m) to next ≡1 (mod 4) value
    When does it increase?
    """
    print("\n" + "=" * 70)
    print("ANALYSIS: Trajectory from S(m) to next ≡1 (mod 4)")
    print("=" * 70)
    print()

    increase_cases = []
    decrease_cases = []

    for m in range(1, 200, 4):  # m ≡ 1 (mod 4)
        s_m = S(m)

        if s_m % 4 == 1:
            # Immediate next ≡1 (mod 4)
            decrease_cases.append((m, s_m, s_m))
        else:
            # Need to continue
            current = s_m
            steps = 0
            while current % 4 != 1 and steps < 1000:
                current = collatz_step(current)
                steps += 1

            next_mod4_1 = current if current % 4 == 1 else None

            if next_mod4_1:
                if next_mod4_1 > m:
                    increase_cases.append((m, s_m, next_mod4_1, next_mod4_1 - m))
                else:
                    decrease_cases.append((m, s_m, next_mod4_1))

    print(f"Total cases analyzed: {len(increase_cases) + len(decrease_cases)}")
    print(f"Decreases: {len(decrease_cases)} ({100*len(decrease_cases)/(len(increase_cases)+len(decrease_cases)):.1f}%)")
    print(f"Increases: {len(increase_cases)} ({100*len(increase_cases)/(len(increase_cases)+len(decrease_cases)):.1f}%)")

    if increase_cases:
        print(f"\nFirst 20 increase cases:")
        for m, s_m, next_v, delta in increase_cases[:20]:
            print(f"  m={m} → S(m)={s_m} → next={next_v} (Δ=+{delta})")

        print(f"\nLargest increases:")
        sorted_increases = sorted(increase_cases, key=lambda x: x[3], reverse=True)
        for m, s_m, next_v, delta in sorted_increases[:10]:
            print(f"  m={m} → S(m)={s_m} → next={next_v} (Δ=+{delta})")

def analyze_small_values_pattern():
    """
    For small values, check if S(m) ≡ 1 (mod 4) eventually always
    """
    print("\n" + "=" * 70)
    print("ANALYSIS: Do small values have S(m) ≡ 1 (mod 4)?")
    print("=" * 70)
    print()

    threshold_values = [10, 20, 50, 100, 200, 500]

    for threshold in threshold_values:
        count_s_is_1_mod4 = 0
        count_s_is_3_mod4 = 0

        for m in range(1, threshold, 4):
            if m % 4 != 1:
                continue
            s_m = S(m)
            if s_m % 4 == 1:
                count_s_is_1_mod4 += 1
            else:
                count_s_is_3_mod4 += 1

        total = count_s_is_1_mod4 + count_s_is_3_mod4
        if total > 0:
            print(f"m < {threshold:4d}: S(m)≡1: {count_s_is_1_mod4:3d} ({100*count_s_is_1_mod4/total:.1f}%), "
                  f"S(m)≡3: {count_s_is_3_mod4:3d} ({100*count_s_is_3_mod4/total:.1f}%)")

def check_eventual_S_is_1_mod4():
    """
    Check if in any trajectory, eventually all S(v_i) ≡ 1 (mod 4)
    """
    print("\n" + "=" * 70)
    print("ANALYSIS: Do trajectories eventually have S(v_i) ≡ 1 (mod 4)?")
    print("=" * 70)
    print()

    def get_mod4_1_sequence_with_S(n, max_steps=10000):
        """Get sequence of ≡1 (mod 4) values with their S values"""
        sequence = []
        current = n
        step = 0

        if current % 4 == 1:
            sequence.append((step, current, S(current) % 4))

        while current != 1 and step < max_steps:
            current = collatz_step(current)
            step += 1
            if current % 4 == 1:
                sequence.append((step, current, S(current) % 4))

        return sequence

    eventually_all_1_count = 0
    never_all_1_count = 0

    for n in range(1, 100, 2):
        seq = get_mod4_1_sequence_with_S(n)
        if len(seq) < 2:
            continue

        # Check if there's a point after which all S values are ≡1 (mod 4)
        found = False
        for start_idx in range(len(seq)):
            all_one_after = all(s_mod4 == 1 for _, _, s_mod4 in seq[start_idx:])
            if all_one_after and len(seq[start_idx:]) >= 2:
                eventually_all_1_count += 1
                found = True
                break

        if not found:
            never_all_1_count += 1
            if never_all_1_count <= 5:
                print(f"  n={n}: S values (mod 4) = {[s_mod4 for _, _, s_mod4 in seq]}")

    total = eventually_all_1_count + never_all_1_count
    print(f"\nTotal trajectories: {total}")
    print(f"Eventually all S(v_i) ≡ 1 (mod 4): {eventually_all_1_count} ({100*eventually_all_1_count/total:.1f}%)")
    print(f"Never all S(v_i) ≡ 1 (mod 4): {never_all_1_count} ({100*never_all_1_count/total:.1f}%)")

if __name__ == "__main__":
    analyze_S_mod_structure()
    analyze_trajectory_to_next_mod4_1()
    analyze_small_values_pattern()
    check_eventual_S_is_1_mod4()
