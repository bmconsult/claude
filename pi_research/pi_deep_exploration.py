"""
DEEP EXPLORATION OF π - Continued Fractions, Hexadecimal, and Mathematical Correlations
"""
from mpmath import mp
from collections import Counter
import math

mp.dps = 1100  # Need extra precision for continued fraction

print("=" * 70)
print("DEEP EXPLORATION: CONTINUED FRACTIONS, HEX, AND CORRELATIONS")
print("=" * 70)

# ===== 1. CONTINUED FRACTION OF π =====
print("\n" + "=" * 70)
print("1. CONTINUED FRACTION COEFFICIENTS OF π")
print("=" * 70)

def continued_fraction(x, n_terms):
    """Extract continued fraction coefficients [a0; a1, a2, ...]"""
    coeffs = []
    for _ in range(n_terms):
        a = int(x)
        coeffs.append(a)
        frac = x - a
        if frac < 1e-50:
            break
        x = 1 / frac
    return coeffs

pi_cf = continued_fraction(mp.pi, 100)
print(f"First 100 continued fraction coefficients of π:")
print(f"{pi_cf}")

# Analyze the coefficients
cf_freq = Counter(pi_cf)
print(f"\nCoefficient frequency distribution:")
for coeff in sorted(cf_freq.keys())[:20]:
    print(f"  {coeff}: {cf_freq[coeff]} occurrences")

# Large coefficients (these determine how "simple" the approximation is)
large_coeffs = [(i, c) for i, c in enumerate(pi_cf) if c > 100]
print(f"\nLarge coefficients (>100) - these create good rational approximations:")
for pos, coeff in large_coeffs[:10]:
    print(f"  Position {pos}: {coeff}")

# Famous rational approximations come from truncating before large coefficients
print("\nRational approximations from continued fraction:")
def convergent(cf):
    """Compute convergent p/q from continued fraction coefficients"""
    if len(cf) == 1:
        return cf[0], 1
    p_prev, p_curr = 1, cf[0]
    q_prev, q_curr = 0, 1
    for a in cf[1:]:
        p_prev, p_curr = p_curr, a * p_curr + p_prev
        q_prev, q_curr = q_curr, a * q_curr + q_prev
    return p_curr, q_curr

for n in [1, 2, 3, 4, 5, 6, 7, 8, 10, 15]:
    p, q = convergent(pi_cf[:n])
    approx = p / q
    error = abs(float(mp.pi) - approx)
    print(f"  [{n} terms] {p}/{q} = {approx:.15f} (error: {error:.2e})")

# ===== 2. HEXADECIMAL π ANALYSIS =====
print("\n" + "=" * 70)
print("2. HEXADECIMAL (BASE 16) π ANALYSIS")
print("=" * 70)

# Convert pi to hex
mp.dps = 5050
pi_str = mp.nstr(mp.pi, 5000, strip_zeros=False)
# Convert decimal digits to hex manually is complex, use mpmath's hex output
def pi_to_hex(precision):
    mp.dps = precision + 50
    # Use BBP-like computation via mpmath
    pi_val = mp.pi
    # Integer part
    hex_digits = "3."
    frac = pi_val - 3
    for _ in range(precision):
        frac *= 16
        digit = int(frac)
        hex_digits += "0123456789ABCDEF"[digit]
        frac -= digit
    return hex_digits

hex_pi = pi_to_hex(2000)
print(f"First 100 hex digits of π: {hex_pi[:102]}")

# Frequency analysis
hex_digits_only = hex_pi[2:]  # Skip "3."
hex_freq = Counter(hex_digits_only)
print(f"\nHex digit frequency (first 2000 digits):")
expected = len(hex_digits_only) / 16
for h in '0123456789ABCDEF':
    count = hex_freq[h]
    dev = count - expected
    print(f"  {h}: {count} ({dev:+.1f})")

# Famous hex sequences
print("\nSearching for famous hex patterns in π:")
patterns = {
    'DEADBEEF': 'DEADBEEF',
    'CAFEBABE': 'CAFEBABE',
    'BABE': 'BABE',
    'DEAD': 'DEAD',
    'FACE': 'FACE',
    'CAFE': 'CAFE',
    'F00D': 'F00D',
    '243F6A88': '243F6A88',  # First few hex digits
}

for name, pattern in patterns.items():
    pos = hex_digits_only.find(pattern)
    if pos != -1:
        print(f"  {name} found at hex position {pos}")
    else:
        print(f"  {name} not found in first 2000 hex digits")

# ===== 3. DIGIT-SUM CONGRUENCES =====
print("\n" + "=" * 70)
print("3. DIGIT-SUM CONGRUENCES - Hidden modular structure?")
print("=" * 70)

with open('pi_research/pi_10k_digits.txt', 'r') as f:
    pi_digits = f.read().strip()

# Running digit sum mod various numbers
for mod in [3, 7, 9, 11]:
    running_sum = 0
    visits = [0] * mod
    for i, d in enumerate(pi_digits[:5000]):
        running_sum += int(d)
        visits[running_sum % mod] += 1

    print(f"\nRunning sum mod {mod}:")
    for r in range(mod):
        expected = 5000 / mod
        pct = visits[r] / 5000 * 100
        print(f"  Residue {r}: {visits[r]} visits ({pct:.2f}%, expected {100/mod:.2f}%)")

# ===== 4. PRIME GAP CORRELATION =====
print("\n" + "=" * 70)
print("4. CORRELATION WITH PRIME GAPS")
print("=" * 70)

def sieve_primes(n):
    """Sieve of Eratosthenes"""
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(n + 1) if is_prime[i]]

primes = sieve_primes(10000)
prime_gaps = [primes[i+1] - primes[i] for i in range(len(primes) - 1)]

# Compare prime gaps to pi digits
print(f"First 30 prime gaps: {prime_gaps[:30]}")
print(f"First 30 pi digits:  {[int(d) for d in pi_digits[:30]]}")

# Correlation coefficient
n = min(500, len(prime_gaps))
gaps = [g % 10 for g in prime_gaps[:n]]  # Reduce to single digit
digits = [int(d) for d in pi_digits[:n]]

mean_g = sum(gaps) / n
mean_d = sum(digits) / n
cov = sum((gaps[i] - mean_g) * (digits[i] - mean_d) for i in range(n)) / n
var_g = sum((g - mean_g)**2 for g in gaps) / n
var_d = sum((d - mean_d)**2 for d in digits) / n

if var_g > 0 and var_d > 0:
    corr = cov / (var_g**0.5 * var_d**0.5)
    print(f"\nCorrelation between prime gaps (mod 10) and π digits: {corr:.6f}")
else:
    print("\nCannot compute correlation (zero variance)")

# ===== 5. SELF-SIMILARITY AT DIFFERENT SCALES =====
print("\n" + "=" * 70)
print("5. SELF-SIMILARITY ANALYSIS")
print("=" * 70)

def digit_signature(s):
    """Create a normalized frequency signature"""
    freq = Counter(s)
    total = len(s)
    return tuple(freq.get(str(d), 0) / total for d in range(10))

# Compare signatures at different scales
scales = [100, 500, 1000, 2000, 5000, 10000]
signatures = {s: digit_signature(pi_digits[:s]) for s in scales}

print("Digit frequency signatures at different scales:")
print("Scale  |  0     1     2     3     4     5     6     7     8     9")
print("-" * 70)
for scale in scales:
    sig = signatures[scale]
    print(f"{scale:5}  | ", end="")
    for freq in sig:
        print(f"{freq:.3f} ", end="")
    print()

# Measure convergence
print("\nDeviation from 10% uniform at each scale:")
for scale in scales:
    sig = signatures[scale]
    max_dev = max(abs(f - 0.1) for f in sig) * 100
    print(f"  {scale:5} digits: max deviation = {max_dev:.2f}%")

# ===== 6. π AND NATURAL LOGARITHMS =====
print("\n" + "=" * 70)
print("6. RELATIONSHIPS: π, e, ln(2), φ")
print("=" * 70)

mp.dps = 100

constants = {
    'π': mp.pi,
    'e': mp.e,
    'ln(2)': mp.ln(2),
    'φ (golden)': (1 + mp.sqrt(5)) / 2,
    'sqrt(2)': mp.sqrt(2),
    'π/e': mp.pi / mp.e,
    'e^π': mp.e ** mp.pi,
    'π^e': mp.pi ** mp.e,
    'π + e': mp.pi + mp.e,
    'π * e': mp.pi * mp.e,
    'π/φ': mp.pi / ((1 + mp.sqrt(5)) / 2),
}

print("Values of interesting expressions:")
for name, val in constants.items():
    print(f"  {name:12} = {mp.nstr(val, 30)}")

# Check for "close to integers" relationships
print("\nNearness to integers (potentially interesting if close):")
for name, val in constants.items():
    frac_part = float(val) - int(float(val))
    if frac_part > 0.5:
        frac_part = 1 - frac_part
    print(f"  {name:12}: distance to nearest int = {frac_part:.10f}")

# ===== 7. ERGODIC PROPERTIES =====
print("\n" + "=" * 70)
print("7. ERGODIC/MIXING PROPERTIES")
print("=" * 70)

# Interpret pi digits as a dynamical system
# x_{n+1} = d_n / 10 (scaled digit)
print("Iterating π digits as a map x → d_n/10:")

# Compute histogram of x-values
x_values = [int(d) / 10 for d in pi_digits[:5000]]
bins = [sum(1 for x in x_values if i/10 <= x < (i+1)/10) for i in range(10)]
print("Distribution of x-values in [0,1):")
for i in range(10):
    bar = '*' * (bins[i] // 25)
    print(f"  [{i/10:.1f}, {(i+1)/10:.1f}): {bins[i]:4} {bar}")

# ===== 8. DIGIT PRODUCTS =====
print("\n" + "=" * 70)
print("8. CONSECUTIVE DIGIT PRODUCTS")
print("=" * 70)

# Product of consecutive n digits
for n in [5, 7, 10]:
    products = []
    for i in range(len(pi_digits[:5000]) - n + 1):
        chunk = pi_digits[i:i+n]
        if '0' not in chunk:  # Skip zeros
            prod = 1
            for d in chunk:
                prod *= int(d)
            products.append((prod, i, chunk))

    products.sort(reverse=True)
    print(f"\nLargest products of {n} consecutive non-zero digits:")
    for prod, pos, chunk in products[:5]:
        print(f"  {chunk} at position {pos}: product = {prod}")

# ===== 9. SEARCH FOR "MESSAGES" =====
print("\n" + "=" * 70)
print("9. SEARCHING FOR 'MESSAGES' - ASCII, Date Codes, etc.")
print("=" * 70)

# Phone number patterns (NNN-NNNN)
print("Searching for phone number patterns (7 consecutive digits):")
phone_patterns = []
for i in range(len(pi_digits) - 7):
    chunk = pi_digits[i:i+7]
    # Check if it looks interesting (not random)
    if chunk == chunk[0] * 7:  # All same digit
        phone_patterns.append((chunk, i, "all same"))
    elif chunk[:3] == chunk[4:7]:  # Mirror
        phone_patterns.append((chunk, i, "partial mirror"))

for chunk, pos, reason in phone_patterns[:10]:
    print(f"  {chunk} at position {pos} ({reason})")

# Date patterns (YYYYMMDD or MMDDYYYY)
print("\nSearching for valid date patterns (YYYYMMDD):")
for i in range(len(pi_digits) - 8):
    chunk = pi_digits[i:i+8]
    year = int(chunk[:4])
    month = int(chunk[4:6])
    day = int(chunk[6:8])
    if 1800 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31:
        # Check if historically significant
        if year in [1776, 1969, 2000, 2001] or (month == day and day in [1, 11, 12]):
            print(f"  {chunk} at position {i} ({year}-{month:02d}-{day:02d})")

# ===== 10. BENFORD'S LAW =====
print("\n" + "=" * 70)
print("10. BENFORD'S LAW ON n-DIGIT CHUNKS")
print("=" * 70)

# For multi-digit numbers carved from pi, check leading digit distribution
for chunk_size in [2, 3, 4]:
    chunks = [pi_digits[i:i+chunk_size] for i in range(0, 5000 - chunk_size + 1, chunk_size)]
    chunks = [c for c in chunks if c[0] != '0']  # Remove leading zeros

    leading_digits = Counter(c[0] for c in chunks)
    total = len(chunks)

    print(f"\n{chunk_size}-digit chunks - leading digit distribution:")
    print("Digit | Count |  %   | Benford |  Diff")
    for d in '123456789':
        count = leading_digits[d]
        pct = count / total * 100
        benford = math.log10(1 + 1/int(d)) * 100  # Expected by Benford's law
        diff = pct - benford
        print(f"  {d}   | {count:4}  | {pct:5.2f} | {benford:5.2f}  | {diff:+5.2f}")

print("\n" + "=" * 70)
print("DEEP EXPLORATION COMPLETE")
print("=" * 70)
