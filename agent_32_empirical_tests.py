#!/usr/bin/env python3
"""
Agent 32: Empirical Tester
Comprehensive computational verification of Collatz hitting time claims
"""

from collections import defaultdict
import sys

def collatz_step(n):
    """Single Collatz step"""
    return n // 2 if n % 2 == 0 else 3 * n + 1

def collatz_seq(n):
    """Full Collatz sequence until reaching 1"""
    seq = [n]
    while n != 1:
        n = collatz_step(n)
        seq.append(n)
    return seq

def mod4_values(seq):
    """Extract all values ≡1 (mod 4) from sequence"""
    return [x for x in seq if x % 4 == 1]

def hitting_time(n):
    """Number of steps to reach 1"""
    steps = 0
    while n != 1:
        n = collatz_step(n)
        steps += 1
    return steps

def analyze_mod4_descent(n):
    """Analyze the sequence of ≡1 (mod 4) values"""
    seq = collatz_seq(n)
    mod4_seq = mod4_values(seq)

    if len(mod4_seq) <= 1:
        return {
            'length': len(mod4_seq),
            'increases': 0,
            'decreases': 0,
            'max_value': mod4_seq[0] if mod4_seq else None,
            'backtrack_count': 0,
            'max_consecutive_increases': 0
        }

    increases = 0
    decreases = 0
    consecutive_increases = 0
    max_consecutive_increases = 0
    backtrack_count = 0

    for i in range(len(mod4_seq) - 1):
        if mod4_seq[i+1] > mod4_seq[i]:
            increases += 1
            consecutive_increases += 1
            max_consecutive_increases = max(max_consecutive_increases, consecutive_increases)
            # Any increase is a "backtrack" from the descent perspective
            backtrack_count += 1
        elif mod4_seq[i+1] < mod4_seq[i]:
            decreases += 1
            consecutive_increases = 0
        else:
            consecutive_increases = 0

    return {
        'length': len(mod4_seq),
        'increases': increases,
        'decreases': decreases,
        'max_value': max(mod4_seq),
        'backtrack_count': backtrack_count,
        'max_consecutive_increases': max_consecutive_increases,
        'sequence': mod4_seq[:50]  # Store first 50 for inspection
    }

print("=" * 80)
print("AGENT 32: EMPIRICAL TESTER - COLLATZ VERIFICATION")
print("=" * 80)
print()

# TEST 1: Hitting Time Verification
print("TEST 1: HITTING TIME VERIFICATION (n = 1 to 10000)")
print("-" * 80)

max_hitting_time = 0
max_hitting_n = 0
hitting_time_dist = defaultdict(int)

for n in range(1, 10001):
    ht = hitting_time(n)
    hitting_time_dist[ht] += 1
    if ht > max_hitting_time:
        max_hitting_time = ht
        max_hitting_n = n

print(f"✓ All numbers 1-10000 reach 1 (test passed)")
print(f"✓ Maximum hitting time: {max_hitting_time} (achieved at n={max_hitting_n})")
print(f"✓ Average hitting time: {sum(ht * count for ht, count in hitting_time_dist.items()) / 10000:.2f}")
print()

# TEST 2: Non-Monotonic Descent Analysis
print("TEST 2: NON-MONOTONIC DESCENT ANALYSIS")
print("-" * 80)

total_increases = 0
total_decreases = 0
total_mod4_steps = 0
max_backtrack_n = 0
max_backtrack_count = 0
max_consecutive_increases = 0
max_consecutive_n = 0

backtrack_examples = []

for n in range(1, 10001):
    analysis = analyze_mod4_descent(n)
    total_increases += analysis['increases']
    total_decreases += analysis['decreases']
    total_mod4_steps += analysis['length']

    if analysis['backtrack_count'] > max_backtrack_count:
        max_backtrack_count = analysis['backtrack_count']
        max_backtrack_n = n

    if analysis['max_consecutive_increases'] > max_consecutive_increases:
        max_consecutive_increases = analysis['max_consecutive_increases']
        max_consecutive_n = n

    # Collect examples of significant backtracking
    if analysis['backtrack_count'] >= 5:
        backtrack_examples.append((n, analysis['backtrack_count'], analysis['sequence'][:20]))

print(f"Total mod-4-steps tracked: {total_mod4_steps}")
print(f"Total increases: {total_increases} ({100*total_increases/(total_increases+total_decreases):.2f}%)")
print(f"Total decreases: {total_decreases} ({100*total_decreases/(total_increases+total_decreases):.2f}%)")
print(f"Max backtracking count: {max_backtrack_count} (at n={max_backtrack_n})")
print(f"Max consecutive increases: {max_consecutive_increases} (at n={max_consecutive_n})")
print()

print("Examples of significant backtracking (≥5 increases):")
for n, count, seq in backtrack_examples[:10]:
    print(f"  n={n:5d}: {count} increases, sequence starts: {seq[:10]}")
print()

# TEST 3: Specific Test Cases
print("TEST 3: SPECIFIC TEST CASES")
print("-" * 80)

test_cases = [27, 255, 447, 639, 703, 871]

for n in test_cases:
    seq = collatz_seq(n)
    mod4_seq = mod4_values(seq)
    analysis = analyze_mod4_descent(n)

    print(f"\nn = {n}:")
    print(f"  Total steps: {len(seq) - 1}")
    print(f"  Mod-4 sequence length: {len(mod4_seq)}")
    print(f"  Mod-4 values: {mod4_seq}")
    print(f"  Increases: {analysis['increases']}, Decreases: {analysis['decreases']}")
    print(f"  Max value: {analysis['max_value']}")
    print(f"  Max consecutive increases: {analysis['max_consecutive_increases']}")

print()

# TEST 4: Statistical Analysis
print("TEST 4: STATISTICAL ANALYSIS")
print("-" * 80)

# Correlation between n and max(mod4_values)
correlation_data = []
for n in range(1, 10001):
    seq = collatz_seq(n)
    mod4_seq = mod4_values(seq)
    if mod4_seq:
        max_mod4 = max(mod4_seq)
        correlation_data.append((n, max_mod4))

# Find cases where max exceeds n significantly
excessive_growth = [(n, max_val) for n, max_val in correlation_data if max_val > 10 * n]
excessive_growth.sort(key=lambda x: x[1] / x[0], reverse=True)

print(f"Cases where max(mod4_values) > 10*n: {len(excessive_growth)}")
if excessive_growth:
    print("Top 10 excessive growth cases:")
    for n, max_val in excessive_growth[:10]:
        print(f"  n={n:5d}, max={max_val:8d}, ratio={max_val/n:.2f}")
print()

# Analyze consecutive increases bounds
consecutive_increase_dist = defaultdict(int)
for n in range(1, 10001):
    analysis = analyze_mod4_descent(n)
    consecutive_increase_dist[analysis['max_consecutive_increases']] += 1

print("Distribution of max consecutive increases:")
for k in sorted(consecutive_increase_dist.keys()):
    if consecutive_increase_dist[k] > 0:
        print(f"  {k} increases: {consecutive_increase_dist[k]} numbers")
print()

# TEST 5: Search for Anomalies
print("TEST 5: ANOMALY SEARCH")
print("-" * 80)

# Longest mod-4 sequences
mod4_lengths = []
for n in range(1, 10001):
    seq = collatz_seq(n)
    mod4_seq = mod4_values(seq)
    mod4_lengths.append((n, len(mod4_seq)))

mod4_lengths.sort(key=lambda x: x[1], reverse=True)

print("Numbers with longest mod-4 sequences:")
for n, length in mod4_lengths[:20]:
    analysis = analyze_mod4_descent(n)
    print(f"  n={n:5d}: length={length:3d}, increases={analysis['increases']:3d}, max_val={analysis['max_value']:8d}")
print()

# Numbers with most increases before descent
most_increases = []
for n in range(1, 10001):
    analysis = analyze_mod4_descent(n)
    most_increases.append((n, analysis['increases'], analysis['length']))

most_increases.sort(key=lambda x: x[1], reverse=True)

print("Numbers with most increases in mod-4 sequence:")
for n, increases, length in most_increases[:20]:
    analysis = analyze_mod4_descent(n)
    print(f"  n={n:5d}: {increases:3d} increases out of {length:3d} transitions ({100*increases/max(1,length-1):.1f}%)")
print()

# VERIFICATION: Check the claim about mod 4
print("VERIFICATION: Do all starting values satisfy n ≡ 1 (mod 4)?")
print("-" * 80)
non_mod4_starts = [n for n in range(1, 10001) if n % 4 != 1 and n != 1]
# Actually, the claim is about VALUES IN THE SEQUENCE, not starting values
# Let me check if all values that appear in mod-4 subsequences are indeed ≡1 (mod 4)

all_mod4_correct = True
for n in range(1, 1001):
    seq = collatz_seq(n)
    mod4_seq = mod4_values(seq)
    for val in mod4_seq:
        if val % 4 != 1:
            print(f"ERROR: Found value {val} in mod-4 sequence that is not ≡1 (mod 4)!")
            all_mod4_correct = False

if all_mod4_correct:
    print("✓ VERIFIED: All values in mod-4 subsequences satisfy x ≡ 1 (mod 4)")
else:
    print("✗ FAILED: Found values not satisfying x ≡ 1 (mod 4)")
print()

# CRITICAL INSIGHT CHECK
print("CRITICAL INSIGHT: Monotonicity of mod-4 subsequence")
print("-" * 80)

strictly_monotonic_count = 0
non_monotonic_count = 0
examples_non_monotonic = []

for n in range(1, 10001):
    seq = collatz_seq(n)
    mod4_seq = mod4_values(seq)

    if len(mod4_seq) <= 1:
        strictly_monotonic_count += 1
        continue

    is_monotonic = all(mod4_seq[i] > mod4_seq[i+1] for i in range(len(mod4_seq)-1))

    if is_monotonic:
        strictly_monotonic_count += 1
    else:
        non_monotonic_count += 1
        if len(examples_non_monotonic) < 50:
            examples_non_monotonic.append((n, mod4_seq[:20]))

print(f"Strictly monotonically decreasing: {strictly_monotonic_count} ({100*strictly_monotonic_count/10000:.2f}%)")
print(f"Non-monotonic (has increases): {non_monotonic_count} ({100*non_monotonic_count/10000:.2f}%)")
print()

if non_monotonic_count > 0:
    print("⚠ CRITICAL FINDING: The mod-4 subsequence is NOT always monotonically decreasing!")
    print()
    print("First 20 counterexamples:")
    for n, seq in examples_non_monotonic[:20]:
        print(f"  n={n:5d}: {seq}")
    print()
    print("This contradicts any proof assuming strict monotonic descent!")
else:
    print("✓ The mod-4 subsequence is always monotonically decreasing.")
print()

print("=" * 80)
print("EMPIRICAL TESTING COMPLETE")
print("=" * 80)
