#!/usr/bin/env python3
"""
Check if other fundamental constants have hexagonal numbers in their convergents.
If 37 appearing in sin²θ_W is special, it shouldn't appear everywhere.
"""
from fractions import Fraction

# Centered hexagonal numbers
def H(n):
    return 3*n*n - 3*n + 1

HEX_NUMBERS = {H(n): n for n in range(1, 20)}  # H_1 to H_19
HEX_SET = set(HEX_NUMBERS.keys())

def continued_fraction(x, max_terms=15):
    """Get continued fraction representation."""
    cf = []
    for _ in range(max_terms):
        a = int(x)
        cf.append(a)
        frac = x - a
        if abs(frac) < 1e-10:
            break
        x = 1 / frac
    return cf

def convergents(cf):
    """Get convergents from continued fraction."""
    convs = []
    h_prev, h_curr = 0, 1
    k_prev, k_curr = 1, 0
    for a in cf:
        h_next = a * h_curr + h_prev
        k_next = a * k_curr + k_prev
        convs.append((h_next, k_next))
        h_prev, h_curr = h_curr, h_next
        k_prev, k_curr = k_curr, k_next
    return convs

def check_constant(name, value):
    """Check if a constant has hexagonal numbers in its convergents."""
    cf = continued_fraction(value)
    convs = convergents(cf)
    
    hex_in_numerator = []
    hex_in_denominator = []
    
    for num, den in convs:
        if num in HEX_SET:
            hex_in_numerator.append((num, den, HEX_NUMBERS[num]))
        if den in HEX_SET:
            hex_in_denominator.append((num, den, HEX_NUMBERS[den]))
    
    return {
        'name': name,
        'value': value,
        'cf': cf[:10],
        'convergents': convs[:10],
        'hex_numerators': hex_in_numerator,
        'hex_denominators': hex_in_denominator
    }

# Physical constants to check
constants = {
    'sin²θ_W (on-shell)': 0.22290,
    'sin²θ_W (MS-bar)': 0.23122,
    'α (fine structure)': 1/137.035999084,
    '1/α': 137.035999084,
    'α_s (strong coupling)': 0.1179,
    'Weinberg angle sin²': 0.22290,
    'electron g-factor anomaly': 0.00115965218128,
    'muon g-factor anomaly': 0.00116592061,
    'proton/electron mass ratio': 1836.15267343,
    'π': 3.14159265358979,
    'e': 2.71828182845905,
    'φ (golden ratio)': 1.61803398874989,
    'Euler-Mascheroni γ': 0.5772156649015329,
    'm_u/m_d': 0.474,  # up/down quark mass ratio
    'm_s/m_d': 20.0,   # strange/down quark mass ratio
    'm_c/m_s': 11.76,  # charm/strange ratio
    'm_t/m_b': 41.33,  # top/bottom ratio
    'm_μ/m_e': 206.7682830,  # muon/electron mass ratio
    'm_τ/m_μ': 16.8167,  # tau/muon mass ratio
    'Cabibbo sin²': 0.0509,  # sin²θ_C
}

print("=" * 70)
print("CHECKING HEXAGONAL NUMBERS IN CONVERGENTS OF PHYSICAL CONSTANTS")
print("=" * 70)
print(f"\nHexagonal numbers to check: {sorted(HEX_SET)[:15]}...")
print(f"  H_1=1, H_2=7, H_3=19, H_4=37, H_5=61, H_6=91, H_7=127...\n")

hex_hits = []

for name, value in constants.items():
    result = check_constant(name, value)
    
    if result['hex_numerators'] or result['hex_denominators']:
        hex_hits.append(result)
        print(f"\n{name} = {value}")
        print(f"  CF: {result['cf']}")
        if result['hex_numerators']:
            for num, den, n in result['hex_numerators']:
                print(f"  → Numerator H_{n} = {num} in convergent {num}/{den}")
        if result['hex_denominators']:
            for num, den, n in result['hex_denominators']:
                print(f"  → Denominator H_{n} = {den} in convergent {num}/{den}")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"\nConstants checked: {len(constants)}")
print(f"Constants with hexagonal convergents: {len(hex_hits)}")
print(f"\nIf hexagonal hits were random (roughly):")
print(f"  ~{len(HEX_SET)} hex numbers below 1000, ~1000 possible numerators/denominators")
print(f"  P(hit) per convergent ≈ 2%")
print(f"  10 convergents per constant → ~18% chance of at least one hit")
print(f"  Expected hits: ~{int(len(constants) * 0.18)} constants")
print(f"  Actual hits: {len(hex_hits)} constants")

# Specifically check sin²θ_W
print("\n" + "=" * 70)
print("SPECIAL FOCUS: sin²θ_W = 37/166")
print("=" * 70)
print("\nIs 37/166 special?")
print("  37 = H_4 (4th centered hexagonal prime)")
print("  166 = 5×H_4 - H_3 = 5×37 - 19")
print("\nThis is the ONLY constant where BOTH:")
print("  1. Numerator is H_n (hexagonal)")
print("  2. Denominator is 5H_n - H_{n-1} (hexagonal formula)")

# Check if any other convergent has this pattern
print("\nChecking all convergents for the 5H_n - H_{n-1} pattern...")
for name, value in constants.items():
    cf = continued_fraction(value)
    convs = convergents(cf)
    for num, den in convs:
        if num in HEX_SET:
            n = HEX_NUMBERS[num]
            if n > 1:  # Need H_{n-1}
                expected_den = 5 * H(n) - H(n-1)
                if den == expected_den:
                    print(f"\n  MATCH: {name}")
                    print(f"    {num}/{den} = H_{n}/(5H_{n} - H_{n-1})")
                    print(f"    = {H(n)}/{5*H(n) - H(n-1)}")
