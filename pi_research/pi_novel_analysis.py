"""
NOVEL EXPLORATIONS OF π - Hunting for Undiscovered Patterns
"""
from collections import Counter, defaultdict
import math

# Load pi digits
with open('pi_research/pi_10k_digits.txt', 'r') as f:
    pi_digits = f.read().strip()

print("=" * 70)
print("NOVEL EXPLORATION: HUNTING FOR UNDISCOVERED PATTERNS IN π")
print("=" * 70)

# ===== 1. TRANSITION MATRIX ANALYSIS =====
print("\n" + "=" * 70)
print("1. MARKOV TRANSITION MATRIX - What digit follows what?")
print("=" * 70)

transition = defaultdict(lambda: defaultdict(int))
for i in range(len(pi_digits) - 1):
    transition[pi_digits[i]][pi_digits[i+1]] += 1

print("\nTransition matrix (from row -> to column):")
print("    ", end="")
for d in '0123456789':
    print(f"  {d}  ", end="")
print()

for from_d in '0123456789':
    print(f" {from_d} ", end="")
    row_sum = sum(transition[from_d].values())
    for to_d in '0123456789':
        prob = transition[from_d][to_d] / row_sum * 100 if row_sum > 0 else 0
        # Highlight deviations from expected 10%
        if prob > 12:
            print(f" {prob:4.1f}*", end="")
        elif prob < 8:
            print(f" {prob:4.1f}!", end="")
        else:
            print(f" {prob:4.1f} ", end="")
    print()

print("\n* = higher than expected (>12%), ! = lower than expected (<8%)")

# Find strongest biases
print("\nStrongest transitional biases:")
biases = []
for from_d in '0123456789':
    row_sum = sum(transition[from_d].values())
    for to_d in '0123456789':
        if row_sum > 0:
            prob = transition[from_d][to_d] / row_sum * 100
            biases.append((from_d, to_d, prob, prob - 10))

biases.sort(key=lambda x: abs(x[3]), reverse=True)
print("Top 10 biases (positive and negative):")
for from_d, to_d, prob, bias in biases[:10]:
    sign = "+" if bias > 0 else ""
    print(f"  {from_d}→{to_d}: {prob:.2f}% (expected 10%, bias {sign}{bias:.2f}%)")

# ===== 2. PI AS A 2D RANDOM WALK =====
print("\n" + "=" * 70)
print("2. π AS A 2D RANDOM WALK - Using consecutive digit pairs as vectors")
print("=" * 70)

# Interpret pairs of digits as moves: d1 = direction (0-9 mapped to angle), d2 = distance
import cmath

x, y = 0, 0
positions = [(0, 0)]
for i in range(0, len(pi_digits[:2000]) - 1, 2):
    angle = int(pi_digits[i]) * 36  # 0-9 maps to 0-324 degrees
    dist = int(pi_digits[i+1]) + 1  # 1-10 steps
    angle_rad = math.radians(angle)
    x += dist * math.cos(angle_rad)
    y += dist * math.sin(angle_rad)
    positions.append((x, y))

# Analyze the walk
final_x, final_y = positions[-1]
final_dist = math.sqrt(final_x**2 + final_y**2)
print(f"Walk of 1000 steps ends at: ({final_x:.2f}, {final_y:.2f})")
print(f"Euclidean distance from origin: {final_dist:.2f}")

# Check for returns close to origin
close_returns = [(i, p) for i, p in enumerate(positions) if math.sqrt(p[0]**2 + p[1]**2) < 50 and i > 100]
print(f"Returns close to origin (<50 units) after step 100: {len(close_returns)}")

# ===== 3. SPECTRAL/FOURIER ANALYSIS =====
print("\n" + "=" * 70)
print("3. SPECTRAL ANALYSIS - Periodic patterns in π")
print("=" * 70)

# Simple DFT on first 1000 digits
N = 1000
digits_numeric = [int(d) for d in pi_digits[:N]]

# Compute magnitudes for a few key frequencies
def compute_dft_magnitude(data, freq):
    N = len(data)
    real = sum(data[n] * math.cos(2 * math.pi * freq * n / N) for n in range(N))
    imag = sum(data[n] * math.sin(2 * math.pi * freq * n / N) for n in range(N))
    return math.sqrt(real**2 + imag**2) / N

# DC component (mean)
dc = sum(digits_numeric) / N
print(f"DC component (mean): {dc:.4f} (expected for uniform: 4.5)")

# Check frequencies 1-50
print("\nSignificant frequencies (magnitude > 0.5):")
for freq in range(1, 51):
    mag = compute_dft_magnitude(digits_numeric, freq)
    if mag > 0.5:
        period = N / freq
        print(f"  Frequency {freq}: magnitude {mag:.4f} (period: {period:.1f} digits)")

# ===== 4. PALINDROME ANALYSIS =====
print("\n" + "=" * 70)
print("4. PALINDROMES IN π")
print("=" * 70)

def find_palindromes(s, min_len=5):
    palindromes = []
    for length in range(min_len, min(15, len(s) // 10)):
        for i in range(len(s) - length + 1):
            substr = s[i:i+length]
            if substr == substr[::-1]:
                palindromes.append((substr, i))
    return palindromes

palins = find_palindromes(pi_digits)
print(f"Found {len(palins)} palindromes of length 5+:")
for p, pos in sorted(palins, key=lambda x: len(x[0]), reverse=True)[:15]:
    print(f"  '{p}' at position {pos} (length {len(p)})")

# ===== 5. π XOR'd WITH SHIFTED SELF =====
print("\n" + "=" * 70)
print("5. π XOR'd WITH ITSELF (shifted) - Hidden structure?")
print("=" * 70)

def xor_with_shift(digits, shift):
    result = []
    for i in range(len(digits) - shift):
        xor_val = int(digits[i]) ^ int(digits[i + shift])
        result.append(xor_val)
    return result

print("XOR statistics at various shifts:")
for shift in [1, 2, 3, 7, 11, 13, 37, 100]:
    xored = xor_with_shift(pi_digits[:5000], shift)
    freq = Counter(xored)
    # For random XOR, each value 0-9 should appear, but XOR limits to 0-15
    zeros = freq[0]
    total = len(xored)
    zero_pct = zeros / total * 100
    print(f"  Shift {shift:3}: {zeros}/{total} zeros ({zero_pct:.2f}%)")
    # Expected for random: ~10% zeros (each digit XOR itself gives 0 with prob 1/10)

# ===== 6. PRIME NUMBER SEQUENCES =====
print("\n" + "=" * 70)
print("6. PRIME NUMBER SEQUENCES IN π")
print("=" * 70)

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0: return False
    return True

# Find n-digit primes in pi
print("Multi-digit primes found in π:")
for length in [2, 3, 4, 5, 6]:
    primes_found = []
    for i in range(len(pi_digits) - length + 1):
        num = int(pi_digits[i:i+length])
        if is_prime(num) and pi_digits[i] != '0':  # No leading zeros
            primes_found.append((num, i))
    print(f"  {length}-digit primes: {len(primes_found)} found")
    if length >= 4:
        # Show first few
        for num, pos in primes_found[:3]:
            print(f"    {num} at position {pos}")

# ===== 7. SUM OF DIGITS WINDOWS =====
print("\n" + "=" * 70)
print("7. DIGIT SUM PATTERNS - Rolling window analysis")
print("=" * 70)

window_size = 10
sums = [sum(int(d) for d in pi_digits[i:i+window_size]) for i in range(len(pi_digits) - window_size + 1)]
expected_sum = 4.5 * window_size  # 45 for window of 10

# Find extreme windows
min_sum = min(sums)
max_sum = max(sums)
min_pos = sums.index(min_sum)
max_pos = sums.index(max_sum)

print(f"Window size: {window_size}, Expected sum: {expected_sum:.1f}")
print(f"Minimum sum: {min_sum} at position {min_pos} (digits: {pi_digits[min_pos:min_pos+window_size]})")
print(f"Maximum sum: {max_sum} at position {max_pos} (digits: {pi_digits[max_pos:max_pos+window_size]})")

# ===== 8. CONCATENATED NUMBER SEQUENCES =====
print("\n" + "=" * 70)
print("8. FAMOUS NUMBER SEQUENCES IN π")
print("=" * 70)

sequences = {
    'Primes': '2357111317192329',
    'Squares': '149162536496481',
    'Cubes': '182764125216343',
    'Powers of 2': '248163264128256',
    'Triangular': '136101521283645',
    'e truncated': '27182818284590',
    'sqrt2 truncated': '14142135623730',
    'phi (golden)': '16180339887498',
}

for name, seq in sequences.items():
    for length in range(len(seq), 5, -1):
        subseq = seq[:length]
        pos = pi_digits.find(subseq)
        if pos != -1:
            print(f"  {name}: first {length} chars '{subseq}' found at position {pos}")
            break
    else:
        print(f"  {name}: no match found for lengths 6+")

# ===== 9. DIFFERENCE SEQUENCE =====
print("\n" + "=" * 70)
print("9. FIRST DIFFERENCES OF π (d[i+1] - d[i])")
print("=" * 70)

diffs = [int(pi_digits[i+1]) - int(pi_digits[i]) for i in range(len(pi_digits[:5000]) - 1)]

diff_freq = Counter(diffs)
print("Distribution of first differences (-9 to +9):")
for d in range(-9, 10):
    count = diff_freq[d]
    bar = '*' * (count // 50)
    print(f"  {d:+2}: {count:4} {bar}")

# ===== 10. MODULAR RESIDUE PATTERNS =====
print("\n" + "=" * 70)
print("10. MODULAR RESIDUE PATTERNS")
print("=" * 70)

# Interpret consecutive triplets as numbers, check residues
triplets = [int(pi_digits[i:i+3]) for i in range(0, len(pi_digits[:3000]) - 2, 3)]

for mod in [7, 11, 13, 37]:
    residues = [t % mod for t in triplets]
    residue_freq = Counter(residues)
    # Check for uniformity
    expected = len(triplets) / mod
    max_dev = max(abs(residue_freq[r] - expected) for r in range(mod))
    print(f"  Mod {mod:2}: max deviation from uniform = {max_dev:.1f} (expected count: {expected:.1f})")

# ===== 11. BINARY REPRESENTATION ANALYSIS =====
print("\n" + "=" * 70)
print("11. DIGIT BINARY PATTERNS")
print("=" * 70)

# Convert each digit to 4-bit binary, look for patterns
binary_pi = ''.join(format(int(d), '04b') for d in pi_digits[:2500])
print(f"First 100 bits of π (as digit-binary): {binary_pi[:100]}")

# Count 0s and 1s
ones = binary_pi.count('1')
zeros = binary_pi.count('0')
print(f"Bit balance in first 10000 bits: {ones} ones, {zeros} zeros (ratio: {ones/zeros:.4f})")

# Look for long runs of 0s or 1s
max_run_0 = max(len(match) for match in binary_pi.split('1') if match)
max_run_1 = max(len(match) for match in binary_pi.split('0') if match)
print(f"Longest run of 0s: {max_run_0}, longest run of 1s: {max_run_1}")

print("\n" + "=" * 70)
print("NOVEL EXPLORATION COMPLETE")
print("=" * 70)
