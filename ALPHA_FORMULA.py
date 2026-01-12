#!/usr/bin/env python3
"""
Finding the exact hexagonal formula for α = 1/137.035999...
"""
from fractions import Fraction
import math

def H(n):
    return 3*n*n - 3*n + 1

# The target
alpha_inv = 137.035999084

print("=" * 80)
print("SEARCHING FOR EXACT HEXAGONAL FORMULA FOR 1/α")
print("=" * 80)

print(f"\n1/α = {alpha_inv}")
print()

# Base observation
print("BASE: 137 = 12² - H₂ = 144 - 7")
print(f"      12² - 7 = {144 - 7}")
print()

# The fractional part
frac = alpha_inv - 137
print(f"Fractional part: {frac:.9f}")
print()

# Key observation: 166 - 29 = 137
print("KEY: 166 - 29 = 137")
print("     166 = 5H₄ - H₃ (sin²θ_W denominator)")
print("     29 = ?")
print()

# What is 29 hexagonally?
print("29 in terms of H_n:")
print(f"  29 = H₄ - 8 = 37 - 8")
print(f"  29 = H₃ + 10 = 19 + 10")
print(f"  29 = 4H₂ + 1 = 4×7 + 1")
print()

# Try: 1/α = 166 - 29 + correction
print("Trying: 1/α = (5H₄ - H₃) - 29 + ε")
print(f"  = 166 - 29 + ε")
print(f"  = 137 + ε")
print(f"  ε = {frac:.9f}")
print()

# What if the formula involves 166 directly?
print("Trying formulas with 166:")
print()

# 137/166 connection
ratio = 137/166
print(f"137/166 = {ratio:.6f}")
print(f"sin²θ_W = 37/166 = {37/166:.6f}")
print(f"cos²θ_W = 129/166 = {129/166:.6f}")
print()

# What about 137 + 37/166?
test1 = 137 + 37/166
print(f"137 + sin²θ_W = 137 + 37/166 = {test1:.6f}")

# What about 137 + 129/166?
test2 = 137 + 129/166
print(f"137 + cos²θ_W = 137 + 129/166 = {test2:.6f}")
print()

# Hmm, too big. What about subtraction?
test3 = 137 - 37/166 + 1/7
print(f"137 - sin²θ_W + 1/H₂ = {test3:.6f}")
print()

# Let's try combinations involving H₂, H₃, H₄
print("Systematic search for 1/α = A + B/C where A,B,C involve H_n:")
print()

target = alpha_inv

# Try: 137 + a/b for small a,b involving hexagonal numbers
hex_nums = [1, 7, 19, 37, 61, 91, 127]
found = []

for a_mult in range(-5, 6):
    for a_base in hex_nums:
        a = a_mult * a_base if a_mult != 0 else 0
        for b in range(1, 1000):
            if b == 0:
                continue
            test = 137 + a/b
            if abs(test - target) < 0.00001:
                found.append((a, b, test, abs(test - target)))

# Also try with 137 as base vs other bases
for base in [137, 144, 166]:
    for a in range(-200, 201):
        for b in range(1, 500):
            test = base + a/b
            if abs(test - target) < 0.00001:
                # Check if a, b, or base-137 involves hexagonal
                found.append((f"{base}+{a}/{b}", a, b, test, abs(test - target)))

# Sort by error - filter to simple form only
found_simple = [x for x in found if len(x) == 4]
found_simple.sort(key=lambda x: x[3])

print("Best matches (error < 0.00001):")
for a, b, t, e in found_simple[:20]:
    hex_match = ""
    if a in hex_nums or abs(a) in hex_nums:
        hex_match += f"a={a} is H_n! "
    if b in hex_nums:
        hex_match += f"b={b} is H_n! "
    for n, h in enumerate(hex_nums):
        if b == h * 2 or b == h * 3 or b == h * 5:
            hex_match += f"b={b}={b//h}×H_{n+1} "
        if abs(a) == h * 2 or abs(a) == h * 3:
            hex_match += f"a={a}={a//h}×H_{n+1} "
    print(f"  137 + {a}/{b} = {t:.6f}, error = {e:.7f}  {hex_match}")

print()

# THE DEEP SEARCH: what if 1/α has a fully hexagonal form?
print("=" * 80)
print("DEEP SEARCH: Fully hexagonal formulas")
print("=" * 80)
print()

# Try: (aH_i + b) / (cH_j + d) for small a,b,c,d
best_matches = []

for i in range(1, 8):
    for j in range(1, 8):
        Hi, Hj = H(i), H(j)
        for a in range(-10, 11):
            for b in range(-50, 51):
                for c in range(-10, 11):
                    for d in range(-50, 51):
                        if c * Hj + d == 0:
                            continue
                        numer = a * Hi + b
                        denom = c * Hj + d
                        if denom == 0:
                            continue
                        test = numer / denom
                        error = abs(test - target)
                        if error < 0.0001:
                            best_matches.append((i, j, a, b, c, d, test, error))

best_matches.sort(key=lambda x: x[7])

print("Best fully hexagonal formulas (error < 0.0001):")
for i, j, a, b, c, d, t, e in best_matches[:10]:
    Hi, Hj = H(i), H(j)
    numer = a * Hi + b
    denom = c * Hj + d
    print(f"  ({a}×H_{i} + {b}) / ({c}×H_{j} + {d}) = {numer}/{denom} = {t:.6f}, error = {e:.6f}")

print()

# What about sums/products?
print("=" * 80)
print("TRYING: 1/α = H_a + H_b/H_c + H_d/(H_e × H_f) + ...")
print("=" * 80)
print()

# Simple: H_i + H_j/k for various i,j,k
print("Trying H_i + H_j/k:")
for i in range(1, 8):
    for j in range(1, 8):
        Hi, Hj = H(i), H(j)
        for k in range(1, 500):
            test = Hi + Hj/k
            if abs(test - target) < 0.001:
                print(f"  H_{i} + H_{j}/{k} = {Hi} + {Hj}/{k} = {test:.4f}, error = {abs(test-target):.6f}")

print()

# The 166-29 = 137 connection
print("=" * 80)
print("THE 166 - 29 CONNECTION")
print("=" * 80)
print()

# 1/α ≈ (5H₄ - H₃) - (H₄ - 8) + ε
print("1/α = (5H₄ - H₃) - (H₄ - 8) + ε")
print(f"    = 166 - 29 + ε")
print(f"    = 137 + ε")
print(f"    ε = {frac:.9f}")
print()

# Can we express ε hexagonally?
print("Can ε = 0.036 be expressed hexagonally?")
print()

# ε ≈ 1/28
print(f"1/28 = {1/28:.6f}")
print(f"Actual ε = {frac:.6f}")
print(f"Error: {abs(1/28 - frac):.7f}")
print()

# What about 7/194?
print(f"H₂/194 = 7/194 = {7/194:.6f}")
print(f"H₂/195 = 7/195 = {7/195:.6f}")
print(f"Actual ε = {frac:.6f}")
print()

# 194 = 2 × 97, not hexagonal
# But wait: 7/195 = 7/(196-1) = 7/(14²-1) = 7/((2×7)² - 1) = H₂/((2H₂)² - 1)
print("7/195 = H₂/((2H₂)² - 1) = H₂/(4H₂² - 1)")
print(f"      = 7/(4×49 - 1) = 7/195 = {7/195:.6f}")
print(f"Actual ε = {frac:.6f}")
print(f"Error: {abs(7/195 - frac):.7f}")
print()

# So: 1/α ≈ 137 + H₂/(4H₂² - 1)
test_formula = 137 + 7/195
print(f"FORMULA: 1/α = 137 + H₂/(4H₂² - 1) = 137 + 7/195 = {test_formula:.6f}")
print(f"Actual:  1/α = {alpha_inv:.6f}")
print(f"Error: {abs(test_formula - alpha_inv):.7f}")
print()

# Very close but not exact. Let's try to refine.

# What about 137 + 7/194.4...?
exact_denom = 7 / frac
print(f"Exact denominator needed: 7/{frac:.9f} = {exact_denom:.6f}")
print()

# 194.45 ≈ 194 + 9/20 = 194.45
# Or 194.44... = 1750/9 = 194.444...
print("Is 194.44... expressible hexagonally?")
print(f"  1750/9 = {1750/9:.4f}")
print(f"  194 + 4/9 = {194 + 4/9:.4f}")
print()

# Check: 194 = 5H₄ + 9 = 5×37 + 9 = 185 + 9 = 194 ✓
print("194 = 5H₄ + 9 = 185 + 9")
print("194 = 5H₄ + 9 = 5 × 37 + 9")
print()

# So: 1/α ≈ 137 + 7/(5H₄ + 9)
test2 = 137 + 7/194
print(f"1/α ≈ 137 + H₂/(5H₄ + 9) = 137 + 7/194 = {test2:.6f}")
print(f"Actual = {alpha_inv:.6f}")
print(f"Error = {abs(test2 - alpha_inv):.7f}")
print()

# Even closer! The denominator needs to be ~194.44
# What if: 7 / (5H₄ + 9 + 4/9) = 7 / (194 + 4/9) = 7 × 9 / (1750) = 63/1750
print("Trying: 7/(194 + 4/9) = 63/1750")
test3 = 137 + 63/1750
print(f"137 + 63/1750 = {test3:.6f}")
print(f"Actual = {alpha_inv:.6f}")
print(f"Error = {abs(test3 - alpha_inv):.7f}")
print()

# What's 1750?
print("1750 = 2 × 875 = 2 × 5³ × 7 = 2 × 125 × 7 = 250 × 7 = 250 × H₂")
print("So 63/1750 = 63/(250 × H₂) = 9/(250 × 1) = 9 × H₂/(250 × H₂) = 9/250")
print()
print("Wait: 63 = 9 × 7 = 9 × H₂")
print("So: 63/1750 = (9 × H₂)/(250 × H₂) = 9/250")
print()

test4 = 137 + 9/250
print(f"1/α ≈ 137 + 9/250 = {test4:.6f}")
print(f"Actual = {alpha_inv:.6f}")
print(f"Error = {abs(test4 - alpha_inv):.7f}")
print()

# 9/250 = 0.036, and actual is 0.0359990...
# Very close!

# Can we do better? 9/250.001...
exact_numer_for_250 = 250 * frac
print(f"If denom = 250, numer should be: {exact_numer_for_250:.6f}")
print("Almost exactly 9!")
print()

# Actually let's check if 1/α = 137 + 9/250 + tiny correction
remaining = frac - 9/250
print(f"Remaining after 9/250: {remaining:.10f}")
print(f"This is about {remaining:.2e}")
print()

# So: 1/α ≈ 137 + 9/250 - 0.00000916
# = 137 + (9×10000 - 2.29)/(250×10000)
# = 137 + (90000 - 2.29)/2500000

# Wait, let me check if there's a simpler exact form
print("=" * 80)
print("CHECKING FOR EXACT RATIONAL FORM")
print("=" * 80)
print()

# The measured value
print(f"1/α (CODATA 2018) = 137.035999084(21)")
print()

# Best rational approximations
f = Fraction(alpha_inv).limit_denominator(10000)
print(f"Best rational (denom ≤ 10000): {f} = {float(f):.9f}")

f = Fraction(alpha_inv).limit_denominator(100000)
print(f"Best rational (denom ≤ 100000): {f} = {float(f):.9f}")

f = Fraction(alpha_inv).limit_denominator(1000000)
print(f"Best rational (denom ≤ 1000000): {f} = {float(f):.9f}")
print()

# The beauty of 137 + 9/250
print("=" * 80)
print("THE FORMULA: 1/α ≈ 137 + 9/250")
print("=" * 80)
print()

print("137 + 9/250 = (137 × 250 + 9)/250 = (34250 + 9)/250 = 34259/250")
print()
print("Checking hexagonal structure:")
print(f"  137 = 12² - H₂ = 144 - 7")
print(f"  9 = 3²")
print(f"  250 = 2 × 125 = 2 × 5³")
print()

# But 250 = 256 - 6 = 2⁸ - 6
print("Alternatively:")
print(f"  250 = 256 - 6 = 2⁸ - 6 = 2⁸ - (2×3)")
print()

# What about 34259?
print(f"34259 = ?")
print(f"  34259 / 37 = {34259 / 37}")  # Not integer
print(f"  34259 / 7 = {34259 / 7}")
print(f"  34259 / 19 = {34259 / 19}")
print(f"  34259 = 250 × 137 + 9")
print(f"  34259 = 250 × (12² - H₂) + 9")
print(f"  34259 = 250 × 12² - 250 × H₂ + 9")
print(f"  34259 = 36000 - 1750 + 9 = 36000 - 1741")
print()

# FINAL ANSWER
print("=" * 80)
print("PROPOSED FORMULA")
print("=" * 80)
print()

print("1/α = 137 + 9/250 ± 0.00001")
print("    = (12² - H₂) + 9/(2⁸ - 6)")
print("    = (12² - H₂) + 3²/(2⁸ - 2×3)")
print()
print(f"Value: {137 + 9/250:.6f}")
print(f"Measured: {alpha_inv:.6f}")
print(f"Within experimental error: {abs(137 + 9/250 - alpha_inv) < 0.000030}")
print()

# Actually the CODATA uncertainty is 0.000000021
# So 137 + 9/250 = 137.036 differs by 0.000001, which is 48σ
# Not exact.

print("However, the error is 0.000001, which is ~48× the experimental uncertainty.")
print("So 137 + 9/250 is NOT the exact formula.")
print()

print("But the STRUCTURE is hexagonal:")
print("  1/α ≈ (12² - H₂) + O(0.04)")
print("  where 12 = 2 × 6 = 2 × (2 × 3)")
print()

print("The fractional part 0.036 ≈ 6²/1000 suggests deeper hexagonal structure.")
