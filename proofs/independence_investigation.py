#!/usr/bin/env python3
"""
Investigation of independence in consecutive Syracuse function applications.
Goal: Understand if consecutive jumps are statistically independent.
"""

from collections import defaultdict, Counter
from fractions import Fraction
import random
import statistics

def nu_2(n):
    """2-adic valuation: highest power of 2 dividing n"""
    if n == 0:
        return float('inf')
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count

def syracuse(n):
    """Syracuse function: S(n) = (3n+1) / 2^{ν₂(3n+1)}"""
    if n % 2 == 0:
        raise ValueError("Syracuse function only defined for odd n")
    val = 3 * n + 1
    power = nu_2(val)
    return val >> power, power

def collatz_step(n):
    """Standard Collatz step"""
    if n % 2 == 0:
        return n // 2
    else:
        return 3 * n + 1

def analyze_consecutive_jumps(max_n=100000, num_samples=10000):
    """
    Analyze whether jump sizes are independent between consecutive Syracuse steps.
    Returns joint distribution data.
    """
    print("=" * 80)
    print("CONSECUTIVE JUMP INDEPENDENCE ANALYSIS")
    print("=" * 80)

    # Sample random odd numbers
    samples = [2 * random.randint(1, max_n // 2) + 1 for _ in range(num_samples)]

    # Track consecutive jump pairs
    jump_pairs = []
    first_jumps = []
    second_jumps = []
    conditional_second_given_first = defaultdict(list)

    for n in samples:
        if n <= 0:
            continue
        try:
            n1, j1 = syracuse(n)
            if n1 % 2 == 0:  # n1 is even, need to make it odd
                n1_odd = n1
                while n1_odd % 2 == 0:
                    n1_odd //= 2
            else:
                n1_odd = n1

            n2, j2 = syracuse(n1_odd)

            jump_pairs.append((j1, j2))
            first_jumps.append(j1)
            second_jumps.append(j2)
            conditional_second_given_first[j1].append(j2)

        except Exception as e:
            continue

    print(f"\nSamples analyzed: {len(jump_pairs)}")
    print(f"\nJump size distributions:")
    print(f"First jump: {Counter(first_jumps).most_common(10)}")
    print(f"Second jump: {Counter(second_jumps).most_common(10)}")

    # Test for independence: P(J2=j2|J1=j1) vs P(J2=j2)
    print("\n" + "=" * 80)
    print("INDEPENDENCE TEST")
    print("=" * 80)

    total_j2_dist = Counter(second_jumps)

    print("\nConditional distributions P(J2 | J1):")
    for j1 in sorted(conditional_second_given_first.keys())[:8]:
        if len(conditional_second_given_first[j1]) < 20:
            continue
        cond_dist = Counter(conditional_second_given_first[j1])
        print(f"\nJ1 = {j1} (n={len(conditional_second_given_first[j1])} samples):")

        # Compare to marginal
        for j2, count in cond_dist.most_common(5):
            cond_prob = count / len(conditional_second_given_first[j1])
            marginal_prob = total_j2_dist[j2] / len(second_jumps)
            ratio = cond_prob / marginal_prob if marginal_prob > 0 else float('inf')
            print(f"  P(J2={j2}|J1={j1}) = {cond_prob:.4f}, P(J2={j2}) = {marginal_prob:.4f}, ratio = {ratio:.3f}")

    return jump_pairs, conditional_second_given_first

def analyze_algebraic_relations():
    """
    Investigate algebraic relationships between S(n) and S(S(n)).
    """
    print("\n" + "=" * 80)
    print("ALGEBRAIC STRUCTURE ANALYSIS")
    print("=" * 80)

    print("\nLet n be odd. Then:")
    print("  S(n) = (3n+1) / 2^{ν₂(3n+1)}")
    print("\nLet m = S(n). We need to determine when m is odd vs even.")
    print("\nKey insight: m = (3n+1) / 2^k where k = ν₂(3n+1)")
    print("  m is odd ⟺ k = ν₂(3n+1)")
    print("  m is even ⟺ this shouldn't happen by definition of Syracuse!")
    print("\nActually, S(n) might be even. Let's trace through carefully...")

    print("\n" + "-" * 80)
    print("Concrete examples:")
    print("-" * 80)

    for n in [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27]:
        m, j1 = syracuse(n)
        print(f"\nn = {n}:")
        print(f"  3n+1 = {3*n+1}, ν₂ = {j1}, S(n) = {m}")

        # To apply S again, need odd number
        if m % 2 == 0:
            m_odd = m
            steps = 0
            while m_odd % 2 == 0:
                m_odd //= 2
                steps += 1
            print(f"  S(n) is even, divide by 2^{steps} to get {m_odd}")
            m2, j2 = syracuse(m_odd)
            print(f"  S({m_odd}) = {m2}, jump = {j2}")
        else:
            m2, j2 = syracuse(m)
            print(f"  S(S(n)) = S({m}) = {m2}, jump = {j2}")

def analyze_growth_phases():
    """
    Track sequences that experience multiple consecutive 'growth' steps.
    A step is 'growth' if S(n) > n.
    """
    print("\n" + "=" * 80)
    print("GROWTH PHASE ANALYSIS")
    print("=" * 80)

    max_consecutive_growth = 0
    worst_sequence = None

    # Check many starting values
    for start in range(1, 100000, 2):
        n = start
        consecutive_growth = 0
        max_local_growth = 0
        trajectory = [n]

        for step in range(100):
            if n % 2 == 1:
                n_next, jump = syracuse(n)
                trajectory.append(n_next)

                # Growth if n_next > n (considering the odd skeleton)
                # Actually need to be careful here - after Syracuse, might be even
                if n_next > n:
                    consecutive_growth += 1
                    max_local_growth = max(max_local_growth, consecutive_growth)
                else:
                    consecutive_growth = 0

                n = n_next
            else:
                # If even, divide until odd
                while n % 2 == 0:
                    n //= 2
                    trajectory.append(n)

            if n == 1:
                break

        if max_local_growth > max_consecutive_growth:
            max_consecutive_growth = max_local_growth
            worst_sequence = (start, trajectory[:20], max_local_growth)

    print(f"\nMaximum consecutive growth steps found: {max_consecutive_growth}")
    if worst_sequence:
        print(f"Starting value: {worst_sequence[0]}")
        print(f"Trajectory (first 20): {worst_sequence[1]}")

    return max_consecutive_growth

def analyze_2adic_patterns():
    """
    Investigate patterns in 2-adic valuations.
    Question: Is ν₂(3n+1) predictable from n's structure?
    """
    print("\n" + "=" * 80)
    print("2-ADIC VALUATION PATTERNS")
    print("=" * 80)

    print("\nFor odd n, we have 3n+1 ≡ 0 (mod 2).")
    print("The question is: what determines ν₂(3n+1)?")

    # Analyze by residue class modulo powers of 2
    print("\n" + "-" * 80)
    print("Pattern by residue class modulo 8:")
    print("-" * 80)

    residue_jumps = defaultdict(list)

    for n in range(1, 10000, 2):
        residue = n % 8
        _, jump = syracuse(n)
        residue_jumps[residue].append(jump)

    for residue in sorted(residue_jumps.keys()):
        jumps = residue_jumps[residue]
        dist = Counter(jumps)
        print(f"\nn ≡ {residue} (mod 8):")
        print(f"  Jump distribution: {dist.most_common(5)}")
        print(f"  Mean jump: {statistics.mean(jumps):.3f}")

    # Check higher moduli
    print("\n" + "-" * 80)
    print("Pattern by residue class modulo 16:")
    print("-" * 80)

    residue_jumps_16 = defaultdict(list)

    for n in range(1, 10000, 2):
        residue = n % 16
        _, jump = syracuse(n)
        residue_jumps_16[residue].append(jump)

    for residue in sorted(residue_jumps_16.keys()):
        jumps = residue_jumps_16[residue]
        dist = Counter(jumps)
        mean_jump = statistics.mean(jumps)
        print(f"n ≡ {residue:2d} (mod 16): mean jump = {mean_jump:.3f}, mode = {dist.most_common(1)[0]}")

def theoretical_analysis():
    """
    Theoretical framework for independence.
    """
    print("\n" + "=" * 80)
    print("THEORETICAL FRAMEWORK")
    print("=" * 80)

    print("""
DEFINITION OF INDEPENDENCE:
---------------------------
Let J₁ = ν₂(3n+1) be the first jump size.
Let J₂ = ν₂(3S(n)+1) be the second jump size (after reducing S(n) to odd form).

Independence would mean: P(J₂ = j₂ | J₁ = j₁) = P(J₂ = j₂) for all j₁, j₂.

Equivalently: The random variables J₁ and J₂ are independent.

ALGEBRAIC APPROACH:
-------------------
Given odd n:
  S(n) = (3n+1) / 2^{ν₂(3n+1)}

Let k₁ = ν₂(3n+1), so S(n) = (3n+1) / 2^{k₁} = m.

Case 1: m is odd.
  Then S(m) = (3m+1) / 2^{k₂} where k₂ = ν₂(3m+1).

  Now, m = (3n+1) / 2^{k₁}, so:
  3m + 1 = 3(3n+1)/2^{k₁} + 1 = (3(3n+1) + 2^{k₁}) / 2^{k₁}

  For this to have a 2-adic valuation, we need:
  ν₂(3(3n+1) + 2^{k₁}) = ν₂(9n + 3 + 2^{k₁})

Case 2: m is even.
  We divide m by 2 until odd, then apply S.

KEY OBSERVATION:
----------------
The 2-adic valuation ν₂(3n+1) depends on n (mod 2^k) for all k.
After applying S, we get a new number whose residue classes are transformed.

The question is: Does this transformation destroy correlations or preserve them?

KNOWN RESULTS:
--------------
1. The 2-adic valuation ν₂(3n+1) is "pseudorandom" in a certain sense.
2. But there ARE patterns by residue class (as shown above).
3. The transformation n → S(n) mixes residue classes in a complex way.

CHALLENGE:
----------
Even if individual jump probabilities are well-understood, proving independence
of consecutive jumps requires showing that the joint distribution factorizes.

This is subtle because:
- The second number S(n) is algebraically related to n
- While the jump size ν₂(3S(n)+1) may "look" independent, there could be
  hidden correlations through the modular structure.
""")

if __name__ == "__main__":
    # Run all analyses
    theoretical_analysis()
    analyze_algebraic_relations()
    analyze_2adic_patterns()
    jump_pairs, conditional_dist = analyze_consecutive_jumps(max_n=100000, num_samples=50000)
    max_growth = analyze_growth_phases()

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"\nMaximum consecutive growth steps observed: {max_growth}")
    print("\nNext steps for rigorous proof:")
    print("  1. Formalize the notion of independence using probability theory")
    print("  2. Use ergodic theory to analyze long-term behavior")
    print("  3. Apply results from analytic number theory on 2-adic valuations")
    print("  4. Search literature for existing work on Collatz correlation structure")
