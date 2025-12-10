"""
Analyze the worst-case orbits with longest v=1 runs
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

def find_longest_v1_runs(max_n=2000):
    """Find numbers with longest consecutive v=1 runs"""
    longest_runs = []

    for n in range(1, max_n, 2):
        orbit = [n]
        current = n
        max_run = 0
        current_run = 0
        run_start = None

        for step in range(200):
            v = nu_2(3*current + 1)

            if v == 1:
                if current_run == 0:
                    run_start = step
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0

            current = syracuse(current)
            orbit.append(current)

            if current == 1:
                break

        if max_run >= 7:
            longest_runs.append((n, max_run, orbit))

    return sorted(longest_runs, key=lambda x: x[1], reverse=True)

def analyze_orbit_detailed(n, max_steps=100):
    """Detailed analysis of a specific orbit"""
    print(f"\n{'='*80}")
    print(f"DETAILED ANALYSIS: n={n}")
    print(f"{'='*80}")

    orbit = [n]
    current = n
    v1_runs = []
    current_run = 0
    run_start = 0

    for step in range(max_steps):
        v = nu_2(3*current + 1)
        ratio = (3*current + 1) / (current * (2**v))

        if step < 50:  # Print first 50 steps
            print(f"Step {step:3d}: n={current:8d}, v={v}, ratio={ratio:.4f}, "
                  f"mod8={current%8}, mod16={current%16}, mod32={current%32}")

        if v == 1:
            if current_run == 0:
                run_start = step
            current_run += 1
        else:
            if current_run > 0:
                v1_runs.append((run_start, current_run))
            current_run = 0

        current = syracuse(current)
        orbit.append(current)

        if current == 1:
            break

    if current_run > 0:
        v1_runs.append((run_start, current_run))

    print(f"\nv=1 runs: {v1_runs}")
    print(f"Longest v=1 run: {max(run[1] for run in v1_runs) if v1_runs else 0} steps")
    print(f"Total orbit length: {len(orbit)}")
    print(f"Reached 1: {orbit[-1] == 1}")

    # Analyze the longest run
    if v1_runs:
        longest_run = max(v1_runs, key=lambda x: x[1])
        start, length = longest_run
        print(f"\nLongest run details: starts at step {start}, length {length}")
        print(f"Orbit during longest run:")
        for i in range(start, min(start+length+2, len(orbit))):
            if i < len(orbit):
                val = orbit[i]
                print(f"  n_{i} = {val}, mod32={val%32}, mod64={val%64}")

def main():
    print("Finding orbits with longest v=1 runs...")
    longest = find_longest_v1_runs(max_n=2000)

    print(f"\nTop 10 numbers with longest v=1 runs:")
    print("-" * 80)
    for n, max_run, orbit in longest[:10]:
        print(f"n={n:5d}: max v=1 run = {max_run} steps, orbit length = {len(orbit)}")

    # Detailed analysis of top cases
    for n, max_run, orbit in longest[:3]:
        analyze_orbit_detailed(n, max_steps=150)

    # Check for patterns in these numbers
    print(f"\n{'='*80}")
    print("PATTERN ANALYSIS")
    print(f"{'='*80}")

    print("\nModular patterns of worst-case starting values:")
    for n, max_run, orbit in longest[:20]:
        print(f"n={n:5d} (run={max_run}): mod8={n%8:2d}, mod16={n%16:2d}, "
              f"mod32={n%32:2d}, mod64={n%64:2d}")

if __name__ == "__main__":
    main()
