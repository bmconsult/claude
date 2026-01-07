"""
DEEP RELATIONAL ANALYSIS OF π
Can we find hidden structure, self-similarity, or prove patterns exist?
"""
from mpmath import mp
from collections import Counter, defaultdict
import math

mp.dps = 50100

# Get 50,000 digits
pi_str = str(mp.pi)[2:50002]
print(f"Analyzing {len(pi_str)} digits of π")

print("=" * 70)
print("PART 1: PROVING π DOESN'T REPEAT (and why)")
print("=" * 70)

print("""
π is PROVABLY irrational (Lambert, 1761). This means:
- It NEVER repeats
- It CANNOT be expressed as a fraction p/q
- Its decimal expansion goes on forever without cycling

But "doesn't repeat" ≠ "has no pattern"
A number can be non-repeating yet still have structure.

Example: 0.101001000100001... (non-repeating but clearly patterned)
""")

# ===== PART 2: SELF-CORRELATION ANALYSIS =====
print("=" * 70)
print("PART 2: DOES π RELATE TO ITSELF? (Self-correlation)")
print("=" * 70)

def correlation(seq1, seq2):
    """Compute correlation coefficient between two sequences"""
    n = len(seq1)
    mean1 = sum(seq1) / n
    mean2 = sum(seq2) / n
    cov = sum((seq1[i] - mean1) * (seq2[i] - mean2) for i in range(n)) / n
    var1 = sum((x - mean1)**2 for x in seq1) / n
    var2 = sum((x - mean2)**2 for x in seq2) / n
    if var1 * var2 == 0:
        return 0
    return cov / (var1 * var2)**0.5

digits = [int(d) for d in pi_str[:10000]]

print("\nSelf-correlation at various shifts:")
print("(If π has hidden periodicity, we'd see spikes at certain shifts)")
print("Shift  |  Correlation  |  Interpretation")
print("-" * 50)

correlations = []
for shift in [1, 2, 3, 5, 7, 10, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
              50, 100, 137, 314, 500, 761, 1000, 2000, 3141]:
    if shift < len(digits):
        seq1 = digits[:-shift]
        seq2 = digits[shift:]
        corr = correlation(seq1, seq2)
        correlations.append((shift, corr))
        flag = " ⚠️" if abs(corr) > 0.03 else ""
        print(f"{shift:5}  |  {corr:+.6f}    |{flag}")

max_corr = max(correlations, key=lambda x: abs(x[1]))
print(f"\nMax correlation: {max_corr[1]:.6f} at shift {max_corr[0]}")
print("Expected for random: ~0 (with noise ±0.02)")

# ===== PART 3: DOES EARLY π PREDICT LATE π? =====
print("\n" + "=" * 70)
print("PART 3: DO EARLY DIGITS PREDICT LATER ONES?")
print("=" * 70)

# Chi-squared test: does knowing digit d[i] help predict d[i+k]?
print("\nConditional probability analysis:")
print("If π has structure, knowing d[i] should help predict d[i+k]")

for gap in [1, 10, 100, 1000]:
    conditional = defaultdict(lambda: defaultdict(int))
    for i in range(len(pi_str) - gap):
        d1 = pi_str[i]
        d2 = pi_str[i + gap]
        conditional[d1][d2] += 1

    # Compute mutual information
    total = sum(sum(conditional[d1].values()) for d1 in conditional)
    mi = 0
    for d1 in '0123456789':
        p_d1 = sum(conditional[d1].values()) / total if total > 0 else 0
        for d2 in '0123456789':
            p_d2 = sum(conditional[x][d2] for x in '0123456789') / total if total > 0 else 0
            p_joint = conditional[d1][d2] / total if total > 0 else 0
            if p_joint > 0 and p_d1 > 0 and p_d2 > 0:
                mi += p_joint * math.log2(p_joint / (p_d1 * p_d2))

    print(f"Gap {gap:4}: Mutual Information = {mi:.6f} bits")
    print(f"         (0 = no predictive power, higher = more predictable)")

# ===== PART 4: DOES π RELATE TO OTHER CONSTANTS? =====
print("\n" + "=" * 70)
print("PART 4: HOW DOES π RELATE TO OTHER CONSTANTS?")
print("=" * 70)

mp.dps = 100

# Get digit sequences of other constants
e_str = str(mp.e)[2:1002]
phi_str = str((1 + mp.sqrt(5))/2)[2:1002]
sqrt2_str = str(mp.sqrt(2))[2:1002]
ln2_str = str(mp.ln(2))[2:1002]

pi_1k = pi_str[:1000]

def digit_correlation(s1, s2):
    """Correlation between digit sequences"""
    n = min(len(s1), len(s2))
    d1 = [int(c) for c in s1[:n]]
    d2 = [int(c) for c in s2[:n]]
    return correlation(d1, d2)

print("\nCorrelation between π and other constants (first 1000 digits):")
print("-" * 50)
pairs = [
    ("π", "e", pi_1k, e_str),
    ("π", "φ", pi_1k, phi_str),
    ("π", "√2", pi_1k, sqrt2_str),
    ("π", "ln(2)", pi_1k, ln2_str),
]

for name1, name2, s1, s2 in pairs:
    corr = digit_correlation(s1, s2)
    print(f"{name1} vs {name2}: correlation = {corr:+.6f}")

# ===== PART 5: MATHEMATICAL RELATIONSHIPS (The Deep Ones) =====
print("\n" + "=" * 70)
print("PART 5: PROVEN MATHEMATICAL RELATIONSHIPS")
print("=" * 70)

print("""
These are EXACT, PROVEN relationships - not statistical coincidences:

1. EULER'S IDENTITY: e^(iπ) + 1 = 0
   → Connects π, e, i, 1, and 0 in one equation
   → This is NOT a coincidence - it's geometric necessity

2. ZETA FUNCTION: ζ(2) = π²/6
   → The sum 1 + 1/4 + 1/9 + 1/16 + ... = π²/6
   → All even zeta values involve π

3. GAUSSIAN INTEGRAL: ∫e^(-x²)dx from -∞ to ∞ = √π
   → π emerges from seemingly unrelated integrals

4. WALLIS PRODUCT: π/2 = (2/1)(2/3)(4/3)(4/5)(6/5)(6/7)...
   → π from infinite products of rationals

5. CONTINUED FRACTION: π = 3 + 1/(7 + 1/(15 + 1/(1 + 1/(292 + ...))))
   → The coefficients [3; 7, 15, 1, 292, ...] encode π completely
""")

# Verify some of these
print("\nVerifying relationships:")
print(f"  ζ(2) = {float(mp.zeta(2)):.15f}")
print(f"  π²/6 = {float(mp.pi**2/6):.15f}")
print(f"  Match: {abs(float(mp.zeta(2) - mp.pi**2/6)) < 1e-25}")

print(f"\n  ζ(4) = {float(mp.zeta(4)):.15f}")
print(f"  π⁴/90 = {float(mp.pi**4/90):.15f}")
print(f"  Match: {abs(float(mp.zeta(4) - mp.pi**4/90)) < 1e-25}")

# ===== PART 6: INFORMATION-THEORETIC VIEW =====
print("\n" + "=" * 70)
print("PART 6: INFORMATION CONTENT - IS THERE COMPRESSION?")
print("=" * 70)

print("""
If π has hidden structure, it should be COMPRESSIBLE.
Random sequences are incompressible (Kolmogorov complexity).
""")

# Measure compressibility via run-length encoding
def run_length_encode(s):
    """Simple RLE compression"""
    if not s:
        return ""
    result = []
    count = 1
    for i in range(1, len(s)):
        if s[i] == s[i-1]:
            count += 1
        else:
            result.append((s[i-1], count))
            count = 1
    result.append((s[-1], count))
    return result

rle = run_length_encode(pi_str[:10000])
original_len = 10000
rle_len = len(rle) * 2  # Each tuple is (char, count)

print(f"Run-length encoding test (first 10,000 digits):")
print(f"  Original: {original_len} symbols")
print(f"  RLE: {rle_len} symbols")
print(f"  Compression ratio: {rle_len/original_len:.3f}")
print(f"  (Random sequence expected ratio: ~1.0, patterned: <0.5)")

# Digram entropy
digrams = [pi_str[i:i+2] for i in range(len(pi_str[:10000])-1)]
digram_freq = Counter(digrams)
total_digrams = len(digrams)

digram_entropy = -sum((c/total_digrams) * math.log2(c/total_digrams)
                      for c in digram_freq.values())
max_digram_entropy = math.log2(100)  # 100 possible digrams

print(f"\nDigram entropy:")
print(f"  Actual: {digram_entropy:.4f} bits")
print(f"  Maximum: {max_digram_entropy:.4f} bits")
print(f"  Ratio: {digram_entropy/max_digram_entropy:.4f} (1.0 = max randomness)")

# ===== PART 7: THE NORMALITY QUESTION =====
print("\n" + "=" * 70)
print("PART 7: THE BIG OPEN QUESTION - IS π NORMAL?")
print("=" * 70)

print("""
NORMALITY means: Every finite sequence appears with expected frequency.

If π is normal:
- "314159" appears as often as "000000" (in the limit)
- Every book ever written is encoded in π somewhere
- There's no "pattern" in the colloquial sense

WHAT WE KNOW:
- π is BELIEVED to be normal (strong numerical evidence)
- No one has PROVEN π is normal
- No one has proven π is NOT normal
- This is one of the great open problems in mathematics

WHAT OUR DATA SHOWS:
""")

# Test normality at different scales
for n in [1000, 5000, 10000, 50000]:
    segment = pi_str[:n]
    freq = Counter(segment)
    expected = n / 10
    chi_sq = sum((freq.get(str(d), 0) - expected)**2 / expected for d in range(10))

    # Chi-squared critical value for 9 df at p=0.05 is 16.92
    verdict = "PASS" if chi_sq < 16.92 else "FAIL"
    print(f"  {n:5} digits: χ² = {chi_sq:.2f} ({verdict} uniformity test)")

# ===== PART 8: THE DEEPEST QUESTION =====
print("\n" + "=" * 70)
print("PART 8: WHY DOES π EXIST? (The Philosophical Question)")
print("=" * 70)

print("""
π is not arbitrary. It emerges NECESSARILY from:
- The geometry of circles (π = C/d)
- The periodicity of complex exponentials (e^(2πi) = 1)
- The Gaussian distribution (∫e^(-x²) = √π)
- The distribution of primes (prime number theorem)

π appears in physics:
- Heisenberg uncertainty: ΔxΔp ≥ ℏ/2 (where ℏ = h/2π)
- Einstein field equations
- Coulomb's law
- Everywhere circles, waves, or rotations appear

THIS IS THE PATTERN:
π is not a random sequence that happens to encode geometry.
π IS geometry, expressed as a number.
The digits are a CONSEQUENCE, not a coincidence.

The "pattern" in π is not in its digits.
The pattern is in WHY π exists at all.
""")

print("\n" + "=" * 70)
print("CONCLUSIONS")
print("=" * 70)
print("""
1. π provably NEVER repeats (irrational)
2. π's digits show NO predictive structure (empirically)
3. π correlates with NOTHING - not even itself shifted
4. π is as incompressible as random data
5. BUT: π is deeply connected to e, φ, primes via MATHEMATICS
6. The "pattern" is the equations, not the digits
""")
