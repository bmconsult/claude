"""
APEX Collatz: Computational Falsification Attempts
Testing the claims made by DIVERGE team
"""

def collatz_trajectory(n, max_steps=10000):
    """Full trajectory including evens"""
    traj = [n]
    for _ in range(max_steps):
        if n == 1:
            break
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3*n + 1
        traj.append(n)
    return traj

def t_value(n):
    """Count trailing zeros in binary of 3n+1"""
    if n % 2 == 0:
        return 0
    val = 3*n + 1
    count = 0
    while val % 2 == 0:
        val //= 2
        count += 1
    return count

def odd_only_trajectory(n, max_steps=1000):
    """Trajectory of odd values only, with T-values"""
    if n % 2 == 0:
        n = n // 2
        while n % 2 == 0:
            n = n // 2

    traj = [(n, 0)]
    for _ in range(max_steps):
        if n == 1:
            break
        T = t_value(n)
        n = (3*n + 1) // (2**T)
        traj.append((n, T))
    return traj

def test_t_frequency(n, min_freq=0.50):
    """Test if T>=2 frequency is above threshold"""
    traj = odd_only_trajectory(n, max_steps=1000)
    t_values = [T for (_, T) in traj[1:] if T > 0]  # Skip initial

    if len(t_values) == 0:
        return True, 1.0

    t_geq_2_count = sum(1 for T in t_values if T >= 2)
    freq = t_geq_2_count / len(t_values)

    return freq >= min_freq, freq

def test_gateway_rarity(n):
    """Check maximum T value reached"""
    traj = odd_only_trajectory(n, max_steps=1000)
    max_t = max(T for (_, T) in traj)
    return max_t

def test_potential_sum(n):
    """Track cumulative potential change"""
    def potential(x):
        """v2(x+1)"""
        val = x + 1
        count = 0
        while val % 2 == 0:
            val //= 2
            count += 1
        return count

    traj = collatz_trajectory(n, max_steps=10000)
    potentials = [potential(x) for x in traj]

    # Sum of changes
    delta_sum = sum(potentials[i+1] - potentials[i] for i in range(len(potentials)-1))

    return delta_sum, potentials

# Test Claim 1: T>=2 frequency >= 50%
print("="*60)
print("CLAIM 1: T>=2 frequency >= 50% for all trajectories")
print("="*60)

test_values = [27, 255, 447, 639, 703, 1819, 1823, 2463, 2919, 3711]
failures = []

for n in test_values:
    passes, freq = test_t_frequency(n)
    status = "✓ PASS" if passes else "✗ FAIL"
    print(f"n={n:5d}: freq={freq:.3f} {status}")
    if not passes:
        failures.append((n, freq))

print(f"\nFalsification attempts: {len(failures)}/{len(test_values)} violations found")

# Test Claim 2: Max T values stay bounded logarithmically
print("\n" + "="*60)
print("CLAIM 2: Maximum T-value grows slowly (< log₂(n))")
print("="*60)

import math

for n in [2**10-1, 2**15-1, 2**20-1, 10**6, 10**7, 10**8]:
    max_t = test_gateway_rarity(n)
    log_n = math.log2(n) if n > 0 else 0
    print(f"n={n:12d}: max_T={max_t:3d}, log₂(n)={log_n:6.2f}, ratio={max_t/log_n:.3f}")

# Test Claim 3: Potential sum stays bounded
print("\n" + "="*60)
print("CLAIM 3: Cumulative potential change is bounded")
print("="*60)

for n in [27, 255, 10**4, 10**5]:
    delta_sum, pots = test_potential_sum(n)
    print(f"n={n:6d}: Σ(ΔΦ)={delta_sum:4d}, trajectory_length={len(pots):5d}")

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print("If any claim is violated, we've found a falsification.")
print("If all pass, claims survive (but aren't proven).")
print("="*60)
