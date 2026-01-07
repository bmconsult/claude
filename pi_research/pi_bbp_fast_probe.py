"""
FAST BBP PROBE - Hunting anomalies with optimized targets
Focus on positions under 10M for speed
"""
from mpmath import mp
import math

# Use mpmath's built-in high precision for verification
mp.dps = 50

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

def bbp_hex_digit(n):
    """Get hex digits starting at position n using BBP"""
    def series(j, n):
        s = mp.mpf(0)
        for k in range(n + 1):
            ak = 8 * k + j
            if ak == 0:
                continue
            r = modpow(16, n - k, ak)
            s += mp.mpf(r) / ak
            s = s - int(s)

        for k in range(n + 1, n + 100):
            ak = 8 * k + j
            term = mp.power(16, n - k) / ak
            if term < mp.mpf(10)**(-17):
                break
            s += term
            s = s - int(s)
        return s

    s = 4*series(1, n) - 2*series(4, n) - series(5, n) - series(6, n)
    s = s - int(s)
    if s < 0:
        s += 1

    # Extract hex digits
    hex_chars = "0123456789ABCDEF"
    result = ""
    for _ in range(12):
        s *= 16
        digit = int(s)
        digit = max(0, min(15, digit))
        result += hex_chars[digit]
        s = s - digit
    return result

print("=" * 70)
print("FAST BBP PROBE: Targeted Anomaly Hunt")
print("=" * 70)

# Focused targets (all under 10M for speed)
targets = [
    # Self-referential positions
    (314159, "π digits as position"),
    (271828, "e digits"),
    (161803, "φ digits"),

    # Near significant boundaries
    (999999, "Just under 1M"),
    (1000000, "Exactly 1M"),
    (1000001, "Just over 1M"),

    # Powers
    (65536, "2^16"),
    (262144, "2^18"),
    (1048576, "2^20"),
    (2097152, "2^21"),

    # Primes
    (104729, "10,000th prime"),
    (1299709, "100,000th prime"),
    (999983, "Largest prime < 1M"),

    # Fibonacci
    (46368, "F(24)"),
    (75025, "F(25)"),
    (121393, "F(26)"),
    (196418, "F(27)"),
    (317811, "F(28)"),
    (514229, "F(29)"),
    (832040, "F(30)"),

    # Patterns
    (111111, "Six 1s"),
    (222222, "Six 2s"),
    (333333, "Six 3s"),
    (444444, "Six 4s"),
    (555555, "Six 5s"),
    (666666, "Six 6s"),
    (777777, "Six 7s"),
    (888888, "Six 8s"),
    (999999, "Six 9s"),

    # Mystical/interesting
    (142857, "Cyclic number (1/7)"),
    (299792, "Speed of light (km/s)"),
    (602214, "Avogadro-ish"),
    (137036, "Fine structure constant × 1M"),

    # Feynman-related
    (761, "Feynman point position"),
    (7610, "Feynman × 10"),
    (76100, "Feynman × 100"),
    (761000, "Feynman × 1000"),
    (579121, "761²"),

    # Random gut picks - "feels significant"
    (123456, "Ascending"),
    (654321, "Descending"),
    (112358, "Fib digits"),
    (235813, "Fib digits 2"),
    (1618033, "φ × 1M truncated"),
]

print(f"\nProbing {len(targets)} positions...")
print("-" * 70)

results = []
for pos, desc in sorted(targets, key=lambda x: x[0]):
    hex_digits = bbp_hex_digit(pos)
    results.append((pos, desc, hex_digits))
    print(f"Pos {pos:>8} ({desc:22}): {hex_digits}")

# ANOMALY DETECTION
print("\n" + "=" * 70)
print("ANOMALY SCAN")
print("=" * 70)

def find_anomalies(hex_str, pos, desc):
    findings = []

    # Runs of same digit
    max_run = 1
    cur_run = 1
    for i in range(1, len(hex_str)):
        if hex_str[i] == hex_str[i-1]:
            cur_run += 1
            max_run = max(max_run, cur_run)
        else:
            cur_run = 1
    if max_run >= 3:
        findings.append(f"RUN: {max_run} consecutive same digits")

    # Palindromes
    for plen in [8, 6, 4]:
        if hex_str[:plen] == hex_str[:plen][::-1]:
            findings.append(f"PALINDROME: First {plen} chars")
            break

    # Famous hex words
    hex_words = ['DEAD', 'BEEF', 'CAFE', 'BABE', 'FACE', 'F00D', 'C0DE', 'FADE', 'FEED', 'DEED']
    for word in hex_words:
        if word in hex_str:
            findings.append(f"HEX WORD: '{word}' found!")

    # Sequential patterns
    if any(seq in hex_str for seq in ['0123', '3456', '6789', '789A', 'ABCD', 'CDEF']):
        findings.append("SEQUENTIAL: Rising hex sequence")
    if any(seq in hex_str for seq in ['3210', '6543', '9876', 'A987', 'DCBA', 'FEDC']):
        findings.append("SEQUENTIAL: Falling hex sequence")

    # All same digit
    if len(set(hex_str)) == 1:
        findings.append("EXTREME: All identical digits!")

    # Very low diversity
    if len(set(hex_str)) <= 3:
        findings.append(f"LOW DIVERSITY: Only {len(set(hex_str))} unique digits")

    # Repeating pattern
    for plen in [2, 3, 4]:
        pattern = hex_str[:plen]
        if pattern * (len(hex_str) // plen) == hex_str[:plen * (len(hex_str) // plen)]:
            if plen < len(hex_str) // 2:
                findings.append(f"REPEATING: Pattern '{pattern}' repeats")
                break

    return findings

anomaly_count = 0
for pos, desc, hex_str in results:
    findings = find_anomalies(hex_str, pos, desc)
    if findings:
        anomaly_count += 1
        print(f"\n⚡ Position {pos} ({desc})")
        print(f"   Digits: {hex_str}")
        for f in findings:
            print(f"   → {f}")

if anomaly_count == 0:
    print("\nNo major anomalies detected.")
else:
    print(f"\n{anomaly_count} positions with notable features!")

# CROSS-ANALYSIS
print("\n" + "=" * 70)
print("CROSS-POSITION ANALYSIS")
print("=" * 70)

# Frequency across all probes
all_hex = "".join(r[2] for r in results)
from collections import Counter
freq = Counter(all_hex)
total = len(all_hex)
expected = total / 16

print(f"\nDigit frequency across {len(results)} probes ({total} hex digits):")
print("Digit | Count | Expected | Deviation")
print("-" * 40)
deviations = []
for h in "0123456789ABCDEF":
    c = freq[h]
    dev = (c - expected) / expected * 100
    deviations.append((h, dev))
    flag = " ⚠️" if abs(dev) > 25 else ""
    print(f"  {h}   | {c:4}  |  {expected:.1f}   | {dev:+6.1f}%{flag}")

# Any position match another's start?
print("\nShared prefixes between positions:")
for i, (p1, d1, h1) in enumerate(results):
    for p2, d2, h2 in results[i+1:]:
        shared = 0
        for k in range(min(len(h1), len(h2))):
            if h1[k] == h2[k]:
                shared += 1
            else:
                break
        if shared >= 3:
            print(f"  {p1} & {p2}: share '{h1[:shared]}' ({shared} chars)")

# The most "interesting" position
print("\n" + "=" * 70)
print("MOST INTERESTING FINDINGS SUMMARY")
print("=" * 70)

# Calculate interestingness score
def interestingness(hex_str):
    score = 0
    # Runs
    max_run = 1
    cur = 1
    for i in range(1, len(hex_str)):
        if hex_str[i] == hex_str[i-1]:
            cur += 1
            max_run = max(max_run, cur)
        else:
            cur = 1
    score += max_run * 2

    # Low diversity
    unique = len(set(hex_str))
    score += (16 - unique) * 2

    # Hex words
    for word in ['DEAD', 'BEEF', 'CAFE', 'BABE', 'FACE']:
        if word in hex_str:
            score += 10

    return score

scored = [(interestingness(h), p, d, h) for p, d, h in results]
scored.sort(reverse=True)

print("\nTop 10 most 'interesting' positions:")
for score, pos, desc, hex_str in scored[:10]:
    print(f"  Score {score:3}: Position {pos:>8} ({desc})")
    print(f"           {hex_str}")

print("\n" + "=" * 70)
print("PROBE COMPLETE")
print("=" * 70)
