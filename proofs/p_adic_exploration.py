"""
P-adic Approach to Collatz No-Divergence Problem
Computational exploration of 2-adic and 3-adic methods
"""

from fractions import Fraction
from collections import defaultdict

def nu_2(n):
    """Compute the 2-adic valuation of n (highest power of 2 dividing n)"""
    if n == 0:
        return float('inf')
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count

def syracuse(n):
    """
    The Syracuse function: S(n) = (3n+1)/2^{nu_2(3n+1)}
    Maps odd integers to odd integers
    """
    if n % 2 == 0:
        raise ValueError("Syracuse function only defined for odd n")
    numerator = 3 * n + 1
    v = nu_2(numerator)
    return numerator // (2 ** v)

def collatz_step(n):
    """Standard Collatz step"""
    if n % 2 == 0:
        return n // 2
    else:
        return 3 * n + 1

def syracuse_orbit(n, max_steps=1000):
    """Compute the Syracuse orbit starting from odd n"""
    if n % 2 == 0:
        raise ValueError("n must be odd")
    orbit = [n]
    current = n
    for _ in range(max_steps):
        current = syracuse(current)
        orbit.append(current)
        if current == 1:
            break
        if current in orbit[:-1]:  # Cycle detection
            break
    return orbit

def analyze_growth_ratio(n):
    """
    Analyze S(n)/n to understand growth/shrinkage
    Returns (ratio as Fraction, 2-adic valuation)
    """
    s_n = syracuse(n)
    v = nu_2(3 * n + 1)
    # S(n)/n = (3n+1)/(n * 2^v)
    ratio = Fraction(3 * n + 1, n * (2 ** v))
    return ratio, v

def multiplicative_product_analysis(n, steps=100):
    """
    Analyze the product ∏ S^k(n)/S^{k-1}(n)
    Returns cumulative products and when they go below 1
    """
    orbit = [n]
    current = n
    products = [1.0]
    cumulative = 1.0

    for k in range(steps):
        next_val = syracuse(current)
        if current == 0:
            break
        ratio = next_val / current
        cumulative *= ratio
        products.append(cumulative)

        if next_val == 1:
            break
        if next_val in orbit:  # Cycle
            break

        orbit.append(next_val)
        current = next_val

    # Find first step where cumulative product < 1
    first_below_one = None
    for i, p in enumerate(products):
        if p < 1:
            first_below_one = i
            break

    return orbit, products, first_below_one

def two_adic_valuation_statistics(max_n=10000):
    """
    Collect statistics on 2-adic valuations of 3n+1 for odd n
    """
    valuation_counts = defaultdict(int)

    for n in range(1, max_n, 2):  # Odd numbers only
        v = nu_2(3 * n + 1)
        valuation_counts[v] += 1

    return valuation_counts

def growth_shrinkage_boundary(max_n=1000):
    """
    Find the boundary between S(n) > n and S(n) < n
    S(n) > n ⟺ (3n+1)/2^v > n ⟺ 3n+1 > n·2^v ⟺ 2n+1 > n·(2^v - 3)
    """
    growth_cases = []
    shrinkage_cases = []

    for n in range(1, max_n, 2):  # Odd numbers
        s_n = syracuse(n)
        v = nu_2(3 * n + 1)

        if s_n > n:
            growth_cases.append((n, s_n, v, s_n/n))
        else:
            shrinkage_cases.append((n, s_n, v, s_n/n))

    return growth_cases, shrinkage_cases

def analyze_mod_residues():
    """
    Analyze S(n) > n vs S(n) < n based on n mod 2^k residues
    S(n) > n ⟺ 3n+1 > n·2^v ⟺ 2n+1 > n·(2^v - 3)

    For v=1: 2n+1 > -n → always true (impossible since 3n+1 odd)
    For v=2: 2n+1 > n·(-1) → 3n+1 > 0 → always true
    For v=3: 2n+1 > n·5 → 2n+1 > 5n → 1 > 3n → impossible for n≥1

    So: v ≥ 3 ⟹ S(n) < n (shrinkage)
        v = 2 ⟹ S(n) > n (growth)
    """
    results = {}

    # Check for various moduli
    for modulus in [4, 8, 16, 32]:
        residue_info = {}
        for r in range(1, modulus, 2):  # Odd residues only
            # Sample several n ≡ r (mod modulus)
            samples = [r + modulus * k for k in range(100)]
            valuations = [nu_2(3*n + 1) for n in samples]
            avg_val = sum(valuations) / len(valuations)
            val_counts = defaultdict(int)
            for v in valuations:
                val_counts[v] += 1
            residue_info[r] = {
                'avg_valuation': avg_val,
                'valuation_dist': dict(val_counts)
            }
        results[modulus] = residue_info

    return results

def main():
    """Main computational exploration"""

    print("=" * 80)
    print("P-ADIC APPROACH TO COLLATZ NO-DIVERGENCE")
    print("=" * 80)

    # 1. Analyze growth vs shrinkage
    print("\n1. GROWTH vs SHRINKAGE ANALYSIS")
    print("-" * 80)
    growth, shrinkage = growth_shrinkage_boundary(max_n=200)
    print(f"First 20 growth cases (S(n) > n):")
    for n, s_n, v, ratio in growth[:20]:
        print(f"  n={n:4d}: S(n)={s_n:4d}, v={v}, ratio={ratio:.3f}")

    print(f"\nFirst 20 shrinkage cases (S(n) < n):")
    for n, s_n, v, ratio in shrinkage[:20]:
        print(f"  n={n:4d}: S(n)={s_n:4d}, v={v}, ratio={ratio:.3f}")

    # 2. 2-adic valuation statistics
    print("\n2. 2-ADIC VALUATION STATISTICS")
    print("-" * 80)
    val_stats = two_adic_valuation_statistics(max_n=10000)
    total = sum(val_stats.values())
    print("Distribution of ν₂(3n+1) for odd n ∈ [1, 10000]:")
    for v in sorted(val_stats.keys()):
        count = val_stats[v]
        prob = count / total
        print(f"  v={v}: count={count:5d}, probability={prob:.4f}")

    # Expected value of v
    exp_v = sum(v * count for v, count in val_stats.items()) / total
    print(f"\nExpected value of ν₂(3n+1): {exp_v:.4f}")
    print(f"(Theoretical expectation: 2.0 for uniform distribution)")

    # 3. Multiplicative product analysis for specific starting values
    print("\n3. MULTIPLICATIVE PRODUCT ANALYSIS")
    print("-" * 80)
    test_values = [27, 31, 41, 47, 71, 97]

    for n in test_values:
        orbit, products, first_below = multiplicative_product_analysis(n, steps=200)
        print(f"\nn={n}:")
        print(f"  Orbit length: {len(orbit)}")
        print(f"  Reaches 1: {orbit[-1] == 1}")
        if first_below is not None:
            print(f"  First step where ∏(S^k/S^(k-1)) < 1: step {first_below}")
            print(f"  Product value: {products[first_below]:.6f}")
        else:
            print(f"  Product never goes below 1 in {len(products)} steps")

        # Show first few products
        print(f"  First 10 cumulative products: {[f'{p:.4f}' for p in products[:10]]}")

    # 4. Modular residue analysis
    print("\n4. MODULAR RESIDUE ANALYSIS")
    print("-" * 80)
    mod_results = analyze_mod_residues()

    for modulus in [4, 8, 16]:
        print(f"\nResidues mod {modulus}:")
        residue_info = mod_results[modulus]
        for r in sorted(residue_info.keys()):
            avg_val = residue_info[r]['avg_valuation']
            print(f"  n ≡ {r:2d} (mod {modulus:2d}): avg ν₂(3n+1) = {avg_val:.3f}")

    # 5. Critical threshold analysis
    print("\n5. CRITICAL THRESHOLD ANALYSIS")
    print("-" * 80)
    print("For S(n) < n, we need ν₂(3n+1) ≥ 3")
    print("\nCounting frequency of ν₂(3n+1) ≥ 3:")
    high_val_count = sum(count for v, count in val_stats.items() if v >= 3)
    high_val_prob = high_val_count / total
    print(f"  Probability: {high_val_prob:.4f}")
    print(f"  This means ~{high_val_prob*100:.1f}% of steps shrink S(n) < n")

    # Analyze runs of growth vs shrinkage
    print("\n6. GROWTH/SHRINKAGE RUNS")
    print("-" * 80)
    test_n = 27
    orbit = syracuse_orbit(test_n, max_steps=100)
    print(f"Analyzing orbit starting from n={test_n}:")

    growth_run = 0
    shrink_run = 0
    max_growth_run = 0
    max_shrink_run = 0

    for i in range(len(orbit) - 1):
        n_curr = orbit[i]
        n_next = orbit[i+1]
        if n_next > n_curr:
            growth_run += 1
            max_shrink_run = max(max_shrink_run, shrink_run)
            shrink_run = 0
        else:
            shrink_run += 1
            max_growth_run = max(max_growth_run, growth_run)
            growth_run = 0

    print(f"  Max consecutive growth steps: {max_growth_run}")
    print(f"  Max consecutive shrink steps: {max_shrink_run}")

    # 7. Key findings
    print("\n" + "=" * 80)
    print("KEY FINDINGS:")
    print("=" * 80)
    print(f"1. Expected 2-adic valuation E[ν₂(3n+1)] ≈ {exp_v:.3f}")
    print(f"2. Shrinkage probability P(ν₂ ≥ 3) ≈ {high_val_prob:.3f}")
    print(f"3. Average shrinkage factor when ν₂=3: (3n+1)/(8n) ≈ 0.375")
    print(f"4. Average growth factor when ν₂=2: (3n+1)/(4n) ≈ 0.75")
    print(f"5. For orbit to diverge, need sustained ν₂=2 (rare!)")
    print("\nConclusion: The 2-adic valuation is 'large enough' often enough")
    print("to prevent divergence on average, but proving this for ALL n")
    print("requires handling worst-case sequences of ν₂=2 valuations.")

if __name__ == "__main__":
    main()
