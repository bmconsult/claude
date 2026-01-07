"""
BREAKTHROUGH HUNT - Looking for genuinely novel patterns in π
"""
from mpmath import mp
from collections import Counter, defaultdict
import math

mp.dps = 1100

# Load pi digits
with open('pi_research/pi_10k_digits.txt', 'r') as f:
    pi_digits = f.read().strip()

print("=" * 70)
print("BREAKTHROUGH HUNT: SEARCHING FOR NOVEL DISCOVERIES")
print("=" * 70)

# ===== 1. THE GOLDEN RATIO CONNECTION =====
print("\n" + "=" * 70)
print("1. π AND THE GOLDEN RATIO φ - Deep connections?")
print("=" * 70)

phi = (1 + mp.sqrt(5)) / 2

print(f"φ = {float(phi):.15f}")
print(f"π = {float(mp.pi):.15f}")

# Various relationships
relations = {
    'π/φ': mp.pi / phi,
    'π*φ': mp.pi * phi,
    'π + φ': mp.pi + phi,
    'π - φ': mp.pi - phi,
    'π^φ': mp.pi ** phi,
    'φ^π': phi ** mp.pi,
    'π/φ²': mp.pi / (phi**2),
    'π*φ²': mp.pi * (phi**2),
    'sin(π/φ)': mp.sin(mp.pi / phi),
    'cos(π/φ)': mp.cos(mp.pi / phi),
    'ln(π)/ln(φ)': mp.ln(mp.pi) / mp.ln(phi),
    '(π-3)*10': (mp.pi - 3) * 10,
    '(φ-1)*π': (phi - 1) * mp.pi,
}

print("\nInteresting relationships:")
for name, val in relations.items():
    val_f = float(val)
    # Check nearness to simple fractions
    for denom in range(1, 20):
        for numer in range(1, denom * 10):
            if abs(val_f - numer/denom) < 0.001:
                print(f"  {name} = {val_f:.10f} ≈ {numer}/{denom}")
                break

# ===== 2. INFORMATION ENTROPY ANALYSIS =====
print("\n" + "=" * 70)
print("2. INFORMATION ENTROPY - How random is π?")
print("=" * 70)

def entropy(s):
    """Shannon entropy in bits"""
    freq = Counter(s)
    n = len(s)
    return -sum((count/n) * math.log2(count/n) for count in freq.values())

# Entropy at different scales
print("Shannon entropy (bits) at different scales:")
print("(Maximum for 10 symbols = log2(10) ≈ 3.322 bits)")
for n in [100, 500, 1000, 5000, 10000]:
    h = entropy(pi_digits[:n])
    h_pct = h / math.log2(10) * 100
    print(f"  First {n:5} digits: H = {h:.6f} bits ({h_pct:.2f}% of max)")

# Compare to truly random sequence (shuffled pi)
import random
shuffled = list(pi_digits[:10000])
random.shuffle(shuffled)
h_shuffled = entropy(''.join(shuffled))
print(f"\n  Shuffled π (same freq): H = {h_shuffled:.6f} bits")
print(f"  Difference: {abs(entropy(pi_digits[:10000]) - h_shuffled):.6f} bits")

# ===== 3. DIGIT "GRAVITY" - Does π favor certain transitions? =====
print("\n" + "=" * 70)
print("3. DIGIT GRAVITY - Attraction/repulsion between digits")
print("=" * 70)

# For each pair (a,b), compute if a tends to be followed by b more than expected
observed = defaultdict(int)
total = 0
for i in range(len(pi_digits) - 1):
    observed[(pi_digits[i], pi_digits[i+1])] += 1
    total += 1

expected = total / 100  # 10 * 10 pairs
print(f"Expected per pair (uniform): {expected:.1f}")

# Compute chi-squared for each pair
pairs_chi = []
for a in '0123456789':
    for b in '0123456789':
        obs = observed[(a, b)]
        chi = (obs - expected)**2 / expected
        pairs_chi.append((a, b, obs, chi))

# Sort by chi-squared (most anomalous)
pairs_chi.sort(key=lambda x: x[3], reverse=True)
print("\nMost anomalous pairs (highest chi-squared contribution):")
for a, b, obs, chi in pairs_chi[:15]:
    direction = "ATTRACTS" if obs > expected else "REPELS"
    print(f"  {a}→{b}: observed {obs}, chi² = {chi:.2f} ({direction})")

# ===== 4. LOOKING FOR π IN π =====
print("\n" + "=" * 70)
print("4. SELF-REFERENCE: Finding π representations in π")
print("=" * 70)

# Various ways to represent pi
representations = {
    '3141592653': 'First 10 digits',
    '22/7': '227',  # 22/7
    '355/113': '355113',  # 355/113
    '31416': 'Rounded 5 digits',
    '314159265': 'First 9 digits',
    '31831': '100/π ≈ 31.831',
    '15915': '1/2π ≈ 0.15915',
    '19099': 'π² - 10 ≈ -0.1301... wait, π² ≈ 9.8696',
    '98696': 'π² ≈ 9.8696',
    '628': '2π ≈ 6.28',
    '6283': '2π ≈ 6.283',
}

print("Searching for π-related patterns:")
for pattern, meaning in representations.items():
    pos = pi_digits.find(pattern)
    if pos != -1:
        print(f"  '{pattern}' ({meaning}) found at position {pos}")
    else:
        print(f"  '{pattern}' ({meaning}) not found in first 10k digits")

# ===== 5. RAMANUJAN-TYPE PATTERNS =====
print("\n" + "=" * 70)
print("5. RAMANUJAN-STYLE ANALYSIS - Strange near-integer results")
print("=" * 70)

# Ramanujan found many near-integer expressions involving π
expressions = [
    ('e^(π*√163)', lambda: mp.exp(mp.pi * mp.sqrt(163))),  # Famous: almost integer
    ('e^(π*√67)', lambda: mp.exp(mp.pi * mp.sqrt(67))),
    ('e^(π*√43)', lambda: mp.exp(mp.pi * mp.sqrt(43))),
    ('e^(π*√58)', lambda: mp.exp(mp.pi * mp.sqrt(58))),
    ('π^4 + π^5', lambda: mp.pi**4 + mp.pi**5),  # ≈ 403.4... close to 403?
    ('e^π - π', lambda: mp.e**mp.pi - mp.pi),  # ≈ 19.999...
    ('(π^4 - e^π)/e', lambda: (mp.pi**4 - mp.e**mp.pi) / mp.e),
    ('ln(640320³+744)', lambda: mp.ln(640320**3 + 744)),  # Related to Ramanujan
]

print("Near-integer expressions (Ramanujan-style):")
for name, expr in expressions:
    try:
        val = float(expr())
        frac = abs(val - round(val))
        if frac < 0.01:
            print(f"  {name} = {val:.15f}")
            print(f"    Distance from {round(val)}: {frac:.2e} (!!! VERY CLOSE)")
        elif frac < 0.1:
            print(f"  {name} = {val:.10f}")
            print(f"    Distance from {round(val)}: {frac:.6f}")
    except:
        pass

# ===== 6. DIGIT CLUSTERING / VOID ANALYSIS =====
print("\n" + "=" * 70)
print("6. CLUSTERING AND VOIDS - Where do digits bunch up?")
print("=" * 70)

for digit in '0123456789':
    positions = [i for i, d in enumerate(pi_digits[:10000]) if d == digit]

    # Find largest gap (void)
    gaps = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
    max_gap = max(gaps) if gaps else 0
    max_gap_pos = positions[gaps.index(max_gap)] if gaps else -1

    # Find clusters (3+ within 10 positions)
    clusters = 0
    for i in range(len(positions) - 2):
        if positions[i+2] - positions[i] <= 10:
            clusters += 1

    print(f"  Digit {digit}: max void = {max_gap} positions (after pos {max_gap_pos}), clusters = {clusters}")

# ===== 7. SYMMETRY ANALYSIS =====
print("\n" + "=" * 70)
print("7. SYMMETRY HUNTING - Mirror patterns, rotational symmetry")
print("=" * 70)

# Look for mirror pairs (where reversing gives same or complementary pattern)
def digit_complement(d):
    """9-complement"""
    return str(9 - int(d))

def string_complement(s):
    return ''.join(digit_complement(d) for d in s)

print("Looking for complement pairs (where s and reverse(9-s) appear nearby):")
window = 6
found_complements = []
for i in range(len(pi_digits) - window):
    s = pi_digits[i:i+window]
    comp = string_complement(s)[::-1]
    if comp != s:  # Not self-complementary
        comp_pos = pi_digits.find(comp)
        if comp_pos != -1 and abs(comp_pos - i) < 1000:
            found_complements.append((s, comp, i, comp_pos))

print(f"Found {len(found_complements)} complement pairs within 1000 positions")
for s, comp, pos1, pos2 in found_complements[:5]:
    print(f"  '{s}' at {pos1} ↔ '{comp}' at {pos2} (gap: {abs(pos2-pos1)})")

# ===== 8. ARITHMETIC PROGRESSIONS =====
print("\n" + "=" * 70)
print("8. ARITHMETIC PROGRESSIONS IN DIGIT POSITIONS")
print("=" * 70)

for digit in '0123456789':
    positions = [i for i, d in enumerate(pi_digits[:5000]) if d == digit]

    # Find arithmetic progressions of length 4+
    aps = []
    for i in range(len(positions)):
        for j in range(i+1, len(positions)):
            diff = positions[j] - positions[i]
            # Check if there's a progression
            seq = [positions[i]]
            for k in range(j+1, len(positions)):
                if positions[k] == seq[-1] + diff:
                    seq.append(positions[k])
            if len(seq) >= 4:
                aps.append((seq, diff))

    if aps:
        longest = max(aps, key=lambda x: len(x[0]))
        print(f"  Digit {digit}: longest AP of length {len(longest[0])} with diff {longest[1]}")
        if len(longest[0]) >= 5:
            print(f"    Positions: {longest[0][:8]}...")

# ===== 9. MODULAR MAGIC =====
print("\n" + "=" * 70)
print("9. MODULAR MAGIC - Does position predict digit?")
print("=" * 70)

print("Digit frequency by position mod N:")
for mod in [3, 7, 10, 11]:
    print(f"\nMod {mod}:")
    for residue in range(mod):
        digits_at_residue = [pi_digits[i] for i in range(residue, 5000, mod)]
        freq = Counter(digits_at_residue)
        # Check if any digit is over/under-represented
        most_common = freq.most_common(1)[0]
        least_common = freq.most_common()[-1]
        print(f"  r={residue}: most='{most_common[0]}'({most_common[1]}), least='{least_common[0]}'({least_common[1]})")

# ===== 10. THE ULTIMATE TEST: Novel Pattern Discovery =====
print("\n" + "=" * 70)
print("10. NOVEL PATTERN SEARCH - Unique sequences")
print("=" * 70)

# Find sequences that appear exactly once
print("Finding rare sequences (appear exactly once):")
for length in [6, 7, 8]:
    unique_seqs = []
    seq_counts = Counter(pi_digits[i:i+length] for i in range(len(pi_digits) - length + 1))
    unique = [seq for seq, count in seq_counts.items() if count == 1]
    print(f"  {length}-digit sequences appearing exactly once: {len(unique)}")
    # Show first few
    for seq in sorted(unique)[:3]:
        pos = pi_digits.find(seq)
        print(f"    '{seq}' at position {pos}")

# Look for "interesting" unique sequences
print("\nSearching for 'interesting' unique sequences:")
interesting = []
for length in [6, 7]:
    seq_counts = Counter(pi_digits[i:i+length] for i in range(len(pi_digits) - length + 1))
    for seq, count in seq_counts.items():
        if count == 1:
            # Check if "interesting"
            is_interesting = False
            # All same digit
            if len(set(seq)) == 1:
                is_interesting = "all same"
            # Palindrome
            elif seq == seq[::-1]:
                is_interesting = "palindrome"
            # Consecutive digits
            elif seq in '0123456789' or seq in '9876543210':
                is_interesting = "consecutive"
            # Arithmetic progression
            diffs = [int(seq[i+1]) - int(seq[i]) for i in range(len(seq)-1)]
            if len(set(diffs)) == 1 and diffs[0] != 0:
                is_interesting = f"AP with diff {diffs[0]}"

            if is_interesting:
                pos = pi_digits.find(seq)
                interesting.append((seq, pos, is_interesting))

print(f"Found {len(interesting)} interesting unique sequences:")
for seq, pos, reason in interesting[:15]:
    print(f"  '{seq}' at position {pos} ({reason})")

print("\n" + "=" * 70)
print("BREAKTHROUGH HUNT COMPLETE")
print("=" * 70)
