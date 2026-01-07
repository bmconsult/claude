"""
BBP DEEP PROBE - Hunting anomalies at specific positions in π
Using gut instinct to pick "meaningful" positions
"""
import math

def modpow(base, exp, mod):
    """Fast modular exponentiation"""
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result

def bbp_sum(n, j):
    """Compute the BBP sum for position n, offset j"""
    s = 0.0
    # Sum from k=0 to n
    for k in range(n + 1):
        ak = 8 * k + j
        if ak == 0:
            continue
        r = modpow(16, n - k, ak)
        s += r / ak
        s = s - int(s)  # Keep fractional part

    # Sum from k=n+1 to infinity (converges quickly)
    for k in range(n + 1, n + 100):
        ak = 8 * k + j
        term = pow(16, n - k) / ak
        if term < 1e-17:
            break
        s += term
        s = s - int(s)

    return s

def get_hex_digits(position, num_digits=16):
    """Get hex digits of π starting at position (0-indexed)"""
    n = position

    # BBP formula components
    s1 = bbp_sum(n, 1)  # 4/(8k+1)
    s4 = bbp_sum(n, 4)  # 2/(8k+4)
    s5 = bbp_sum(n, 5)  # 1/(8k+5)
    s6 = bbp_sum(n, 6)  # 1/(8k+6)

    # Combine
    s = 4*s1 - 2*s4 - s5 - s6
    s = s - int(s)
    if s < 0:
        s += 1

    # Extract hex digits
    hex_chars = "0123456789ABCDEF"
    result = ""
    for _ in range(num_digits):
        s *= 16
        digit = int(s)
        if digit >= 16:
            digit = 15
        if digit < 0:
            digit = 0
        result += hex_chars[digit]
        s = s - digit

    return result

print("=" * 70)
print("BBP DEEP PROBE: Hunting Anomalies at Gut-Target Positions")
print("=" * 70)

# Define gut-target positions with reasoning
targets = [
    # Mathematical constants as positions
    (314159, "π itself (314159)"),
    (271828, "e (271828)"),
    (161803, "φ golden ratio (161803)"),
    (141421, "√2 (141421)"),
    (173205, "√3 (173205)"),

    # Powers and special numbers
    (1000000, "One million"),
    (9999999, "Seven 9s"),
    (1234567, "Sequential digits"),
    (7654321, "Reverse sequential"),
    (1111111, "Seven 1s"),

    # Fibonacci positions
    (832040, "Fibonacci F(30)"),
    (1346269, "Fibonacci F(31)"),
    (2178309, "Fibonacci F(32)"),

    # Prime positions
    (999983, "Largest prime < 1M"),
    (1000003, "Smallest prime > 1M"),
    (104729, "10,000th prime"),

    # Powers of 2
    (1048576, "2^20"),
    (2097152, "2^21"),
    (524288, "2^19"),

    # "Mystical" numbers
    (666666, "Six 6s"),
    (777777, "Seven 7s (lucky)"),
    (123456789, "Full sequential"),
    (987654321, "Full reverse"),

    # Perfect numbers and special
    (8128, "4th perfect number"),
    (33550336, "5th perfect number"),

    # Near Feynman point multiples
    (761 * 1000, "Feynman × 1000"),
    (761 * 761, "Feynman squared"),

    # Random gut picks
    (42424242, "Life universe everything ×2"),
    (31415926, "First 8 digits of π"),
    (27182818, "First 8 digits of e"),
    (14142135, "First 8 digits of √2"),
]

print("\nProbing hex digits at targeted positions...")
print("-" * 70)

results = []
for pos, desc in targets:
    try:
        hex_digits = get_hex_digits(pos, 20)
        results.append((pos, desc, hex_digits))
        print(f"Position {pos:>12} ({desc:25}): {hex_digits}")
    except Exception as e:
        print(f"Position {pos:>12} ({desc:25}): ERROR - {e}")

# Analyze for anomalies
print("\n" + "=" * 70)
print("ANOMALY ANALYSIS")
print("=" * 70)

def analyze_hex(hex_str):
    """Look for interesting patterns"""
    anomalies = []

    # Check for runs
    max_run = 1
    current_run = 1
    run_char = hex_str[0]
    for i in range(1, len(hex_str)):
        if hex_str[i] == hex_str[i-1]:
            current_run += 1
            if current_run > max_run:
                max_run = current_run
                run_char = hex_str[i]
        else:
            current_run = 1
    if max_run >= 3:
        anomalies.append(f"Run of {max_run} '{run_char}'s")

    # Check for palindrome
    if hex_str[:8] == hex_str[:8][::-1]:
        anomalies.append("8-char palindrome prefix!")
    if hex_str[:6] == hex_str[:6][::-1]:
        anomalies.append("6-char palindrome prefix")

    # Check for sequential
    if "0123456789" in hex_str or "9876543210" in hex_str:
        anomalies.append("Sequential digits!")
    if "ABCDEF" in hex_str or "FEDCBA" in hex_str:
        anomalies.append("Sequential hex letters!")

    # Check for famous patterns
    famous = ["DEAD", "BEEF", "CAFE", "BABE", "FACE", "F00D", "C0DE"]
    for pattern in famous:
        if pattern in hex_str:
            anomalies.append(f"Contains '{pattern}'!")

    # Check digit frequency
    from collections import Counter
    freq = Counter(hex_str)
    most_common = freq.most_common(1)[0]
    if most_common[1] >= len(hex_str) * 0.4:  # 40% or more of one digit
        anomalies.append(f"Heavy '{most_common[0]}' bias ({most_common[1]}/{len(hex_str)})")

    # Check for all same
    if len(set(hex_str)) == 1:
        anomalies.append("ALL SAME DIGIT!")

    # Check for only 0s and Fs (extreme)
    if all(c in '0F' for c in hex_str):
        anomalies.append("Only 0s and Fs!")

    return anomalies

print("\nScanning for anomalies in results...")
anomaly_count = 0
for pos, desc, hex_str in results:
    anomalies = analyze_hex(hex_str)
    if anomalies:
        anomaly_count += 1
        print(f"\n*** Position {pos} ({desc}):")
        print(f"    Digits: {hex_str}")
        for a in anomalies:
            print(f"    → {a}")

if anomaly_count == 0:
    print("No major anomalies found in this scan.")
else:
    print(f"\n{anomaly_count} positions with anomalies found!")

# Statistical analysis across all results
print("\n" + "=" * 70)
print("CROSS-POSITION STATISTICAL ANALYSIS")
print("=" * 70)

all_digits = "".join([r[2] for r in results])
from collections import Counter
overall_freq = Counter(all_digits)
total = len(all_digits)

print(f"\nOverall hex digit frequency across {len(results)} probes ({total} digits):")
expected = total / 16
print(f"Expected per digit: {expected:.1f}")
print("\nDigit | Count | Deviation")
print("-" * 30)
for h in "0123456789ABCDEF":
    count = overall_freq[h]
    dev = (count - expected) / expected * 100
    flag = " ***" if abs(dev) > 30 else ""
    print(f"  {h}   | {count:4}  | {dev:+6.1f}%{flag}")

# Look for repeated patterns across positions
print("\n" + "=" * 70)
print("SEARCHING FOR CROSS-POSITION PATTERNS")
print("=" * 70)

# Do any two positions share starting digits?
print("\nPositions sharing 4+ starting hex digits:")
for i, (pos1, desc1, hex1) in enumerate(results):
    for pos2, desc2, hex2 in results[i+1:]:
        for length in [6, 5, 4]:
            if hex1[:length] == hex2[:length]:
                print(f"  {pos1} and {pos2} share '{hex1[:length]}' ({length} chars)")
                break

print("\n" + "=" * 70)
print("PROBE COMPLETE")
print("=" * 70)
