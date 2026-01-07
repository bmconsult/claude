"""
Deep Analysis of π - Hunting for Novel Patterns
"""
from collections import Counter, defaultdict
from mpmath import mp
import math

# Load pi digits
with open('pi_research/pi_10k_digits.txt', 'r') as f:
    pi_digits = f.read().strip()

print(f"Analyzing {len(pi_digits)} digits of π\n")

# ===== BASIC FREQUENCY ANALYSIS =====
print("=" * 60)
print("1. DIGIT FREQUENCY ANALYSIS")
print("=" * 60)

freq = Counter(pi_digits)
expected = len(pi_digits) / 10
print(f"Expected count per digit (if normal): {expected:.1f}\n")
print("Digit | Count | Deviation | Chi-sq contribution")
print("-" * 50)

chi_sq = 0
for d in '0123456789':
    count = freq[d]
    dev = count - expected
    chi_contrib = (dev ** 2) / expected
    chi_sq += chi_contrib
    print(f"  {d}   | {count:5} |  {dev:+6.1f}  |  {chi_contrib:.3f}")

print(f"\nChi-squared statistic: {chi_sq:.3f}")
print(f"(p-value threshold at 0.05 for 9 df: 16.92)")
print(f"Result: {'PASSES' if chi_sq < 16.92 else 'FAILS'} uniformity test")

# ===== DIGRAM (PAIR) ANALYSIS =====
print("\n" + "=" * 60)
print("2. CONSECUTIVE PAIR (DIGRAM) ANALYSIS")
print("=" * 60)

digrams = [pi_digits[i:i+2] for i in range(len(pi_digits)-1)]
digram_freq = Counter(digrams)
expected_digram = len(digrams) / 100

# Find most over/under represented pairs
sorted_digrams = sorted(digram_freq.items(), key=lambda x: x[1], reverse=True)
print("\nMost common pairs:")
for pair, count in sorted_digrams[:5]:
    print(f"  '{pair}': {count} (expected: {expected_digram:.1f}, dev: {count - expected_digram:+.1f})")

print("\nLeast common pairs:")
for pair, count in sorted_digrams[-5:]:
    print(f"  '{pair}': {count} (expected: {expected_digram:.1f}, dev: {count - expected_digram:+.1f})")

# ===== RUN LENGTH ANALYSIS =====
print("\n" + "=" * 60)
print("3. RUN LENGTH ANALYSIS (consecutive same digits)")
print("=" * 60)

runs = []
current_run = 1
for i in range(1, len(pi_digits)):
    if pi_digits[i] == pi_digits[i-1]:
        current_run += 1
    else:
        runs.append((pi_digits[i-1], current_run, i - current_run))
        current_run = 1
runs.append((pi_digits[-1], current_run, len(pi_digits) - current_run))

run_lengths = Counter([r[1] for r in runs])
print("\nRun length distribution:")
for length in sorted(run_lengths.keys()):
    print(f"  Length {length}: {run_lengths[length]} occurrences")

# Longest runs
long_runs = sorted([r for r in runs if r[1] >= 3], key=lambda x: x[1], reverse=True)[:10]
print("\nLongest runs (Feynman point territory):")
for digit, length, pos in long_runs:
    print(f"  {digit*length} at position {pos} (length {length})")

# ===== RISING/FALLING PATTERNS =====
print("\n" + "=" * 60)
print("4. MONOTONIC SEQUENCE ANALYSIS")
print("=" * 60)

def find_monotonic_sequences(s, direction='rising'):
    sequences = []
    start = 0
    for i in range(1, len(s)):
        curr, prev = int(s[i]), int(s[i-1])
        if direction == 'rising' and curr <= prev:
            if i - start >= 3:
                sequences.append((s[start:i], start))
            start = i
        elif direction == 'falling' and curr >= prev:
            if i - start >= 3:
                sequences.append((s[start:i], start))
            start = i
    return sequences

rising = find_monotonic_sequences(pi_digits, 'rising')
falling = find_monotonic_sequences(pi_digits, 'falling')

print(f"\nStrictly rising sequences (length >= 3): {len(rising)}")
longest_rising = sorted(rising, key=lambda x: len(x[0]), reverse=True)[:5]
for seq, pos in longest_rising:
    print(f"  '{seq}' at position {pos} (length {len(seq)})")

print(f"\nStrictly falling sequences (length >= 3): {len(falling)}")
longest_falling = sorted(falling, key=lambda x: len(x[0]), reverse=True)[:5]
for seq, pos in longest_falling:
    print(f"  '{seq}' at position {pos} (length {len(seq)})")

# ===== SELF-REFERENTIAL PATTERNS =====
print("\n" + "=" * 60)
print("5. SELF-REFERENTIAL ANALYSIS (π containing its own representation)")
print("=" * 60)

# Search for '314159' etc. within pi
pi_prefixes = ['3141', '31415', '314159', '3141592', '31415926']
for prefix in pi_prefixes:
    pos = pi_digits.find(prefix)
    if pos != -1:
        print(f"  '{prefix}' found at position {pos}")
    else:
        print(f"  '{prefix}' not found in first 10,000 digits")

# ===== PRIME POSITION ANALYSIS =====
print("\n" + "=" * 60)
print("6. DIGITS AT PRIME POSITIONS")
print("=" * 60)

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0: return False
    return True

prime_positions = [i for i in range(1, len(pi_digits)+1) if is_prime(i)]
prime_digits = [pi_digits[p-1] for p in prime_positions[:500]]  # First 500 prime positions

prime_freq = Counter(prime_digits)
print(f"Frequency of digits at first 500 prime positions:")
for d in '0123456789':
    print(f"  {d}: {prime_freq[d]}")

# ===== GAP ANALYSIS =====
print("\n" + "=" * 60)
print("7. GAP ANALYSIS (distance between occurrences of each digit)")
print("=" * 60)

for digit in '0123456789':
    positions = [i for i, d in enumerate(pi_digits) if d == digit]
    gaps = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
    if gaps:
        avg_gap = sum(gaps) / len(gaps)
        max_gap = max(gaps)
        max_gap_after = positions[gaps.index(max_gap)]
        print(f"  Digit {digit}: avg gap = {avg_gap:.2f}, max gap = {max_gap} (after position {max_gap_after})")

# ===== MODULAR PATTERNS =====
print("\n" + "=" * 60)
print("8. MODULAR ARITHMETIC PATTERNS")
print("=" * 60)

# Sum of first n digits mod 9, mod 10, etc.
cumsum = 0
mod9_pattern = []
for i, d in enumerate(pi_digits[:100]):
    cumsum += int(d)
    mod9_pattern.append(cumsum % 9)

print(f"Running sum mod 9 (first 100 digits): {mod9_pattern[:50]}")

# Digital root of consecutive n-digit numbers
print("\nDigital roots of 3-digit chunks:")
chunks = [pi_digits[i:i+3] for i in range(0, 30, 3)]
for chunk in chunks:
    dr = sum(int(d) for d in chunk) % 9
    if dr == 0: dr = 9
    print(f"  {chunk} -> digital root {dr}")

# ===== FIBONACCI IN PI =====
print("\n" + "=" * 60)
print("9. FIBONACCI NUMBERS IN π")
print("=" * 60)

fibs = [str(f) for f in [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]]
for fib in fibs:
    pos = pi_digits.find(fib)
    if pos != -1:
        print(f"  Fibonacci {fib:>5} found at position {pos}")
    else:
        print(f"  Fibonacci {fib:>5} not found in first 10k digits")

# ===== AUTOCORRELATION =====
print("\n" + "=" * 60)
print("10. AUTOCORRELATION ANALYSIS")
print("=" * 60)

def autocorr(seq, lag):
    n = len(seq)
    mean = sum(int(d) for d in seq) / n
    var = sum((int(d) - mean)**2 for d in seq) / n
    if var == 0:
        return 0
    cov = sum((int(seq[i]) - mean) * (int(seq[i+lag]) - mean) for i in range(n - lag)) / (n - lag)
    return cov / var

print("Autocorrelation at different lags:")
for lag in [1, 2, 3, 5, 10, 50, 100]:
    ac = autocorr(pi_digits[:5000], lag)
    print(f"  Lag {lag:3}: {ac:.6f}")

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)
