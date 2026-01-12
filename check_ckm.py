#!/usr/bin/env python3
"""
Quick check: Does 6 = 2×3 structure appear in CKM matrix?
"""
import math

def H(n):
    return 3*n*n - 3*n + 1

def cf_convergents(x, max_terms=10):
    convs = []
    h_prev, h_curr = 0, 1
    k_prev, k_curr = 1, 0
    for _ in range(max_terms):
        a = int(x)
        h_next = a * h_curr + h_prev
        k_next = a * k_curr + k_prev
        convs.append((h_next, k_next))
        h_prev, h_curr = h_curr, h_next
        k_prev, k_curr = k_curr, k_next
        frac = x - a
        if abs(frac) < 1e-12: break
        x = 1 / frac
    return convs

# CKM matrix elements (magnitudes, PDG 2024)
ckm = {
    '|V_ud|': 0.97373,
    '|V_us|': 0.2243,
    '|V_ub|': 0.00382,
    '|V_cd|': 0.221,
    '|V_cs|': 0.975,
    '|V_cb|': 0.0408,
    '|V_td|': 0.0086,
    '|V_ts|': 0.0415,
    '|V_tb|': 1.014,
}

# Cabibbo angle
sin_cabibbo = 0.2243  # ≈ |V_us|
sin2_cabibbo = sin_cabibbo**2

# Wolfenstein parameter λ
lambda_wolf = 0.22650

print("CKM MATRIX QUICK CHECK")
print("=" * 60)

hex_nums = {H(n): n for n in range(1, 15)}

for name, val in ckm.items():
    convs = cf_convergents(val)[:5]
    hex_hits = [(n, d, hex_nums[n]) for n, d in convs if n in hex_nums and n > 1]
    if hex_hits:
        print(f"{name} = {val}")
        for n, d, h_idx in hex_hits:
            print(f"  → {n}/{d}, {n} = H_{h_idx}")

print(f"\nCabibbo angle:")
print(f"  sin θ_C = {sin_cabibbo}")
print(f"  sin²θ_C = {sin2_cabibbo:.6f}")
convs = cf_convergents(sin2_cabibbo)[:6]
print(f"  Convergents: {convs}")

print(f"\nWolfenstein λ:")
print(f"  λ = {lambda_wolf}")
convs = cf_convergents(lambda_wolf)[:6]
print(f"  Convergents: {convs}")

# Check for 2, 3, 6 structure
print(f"\n" + "=" * 60)
print("LOOKING FOR 2×3 STRUCTURE")
print("=" * 60)

# Key ratios in CKM
print(f"\n|V_us|/|V_cd| = {0.2243/0.221:.4f}")  # Should be ~1
print(f"|V_cb|/|V_ts| = {0.0408/0.0415:.4f}")  # Should be ~1
print(f"|V_ub|/|V_td| = {0.00382/0.0086:.4f}")  # 

# Wolfenstein hierarchy: λ ≈ 0.22, λ² ≈ 0.05, λ³ ≈ 0.01
print(f"\nWolfenstein hierarchy:")
print(f"  λ = {lambda_wolf:.4f}")
print(f"  λ² = {lambda_wolf**2:.4f}")
print(f"  λ³ = {lambda_wolf**3:.4f}")

# Is λ related to sin²θ_W?
print(f"\nλ vs sin²θ_W:")
print(f"  λ = {lambda_wolf:.4f}")
print(f"  sin²θ_W = 0.2229")
print(f"  Ratio: {lambda_wolf/0.2229:.4f}")

# Check 37/166 connection
print(f"\n37/166 = {37/166:.4f}")
print(f"λ = {lambda_wolf:.4f}")
print(f"Difference: {abs(lambda_wolf - 37/166):.4f}")

# Interesting: they're very close!
print(f"\nλ ≈ sin²θ_W to {abs(lambda_wolf - 0.2229)/0.2229*100:.1f}%")
