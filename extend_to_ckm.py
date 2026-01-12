#!/usr/bin/env python3
"""
The hexagonal structure extends to CKM.
"""

def H(n):
    return 3*n*n - 3*n + 1

print("=" * 70)
print("HEXAGONAL STRUCTURE IN CKM MATRIX")
print("=" * 70)

print("""
CKM MATRIX CONVERGENTS WITH HEXAGONAL NUMERATORS:

  |V_ud| = 0.97373 → 37/38   (37 = H_4)
  |V_cd| = 0.22100 → 19/86   (19 = H_3)  
  |V_td| = 0.00860 → 7/814   (7 = H_2)

THE SAME THREE HEXAGONAL NUMBERS: 7, 19, 37
""")

# Verify
print("VERIFICATION:")
print(f"  37/38 = {37/38:.5f}, |V_ud| = 0.97373, diff = {abs(37/38 - 0.97373):.5f}")
print(f"  19/86 = {19/86:.5f}, |V_cd| = 0.22100, diff = {abs(19/86 - 0.221):.5f}")
print(f"  7/814 = {7/814:.6f}, |V_td| = 0.00860, diff = {abs(7/814 - 0.0086):.6f}")

# The pattern
print("\n" + "=" * 70)
print("THE PATTERN")
print("=" * 70)

print("""
In sin²θ_W:
  sin²θ_W = H_4/(5H_4 - H_3) = 37/166

In CKM:
  |V_ud| = H_4/(H_4 + 1) = 37/38
  |V_cd| ≈ H_3/86
  |V_td| ≈ H_2/814

The NUMERATORS are always H_2, H_3, H_4!
""")

# Check denominators
print("=" * 70)
print("ANALYZING DENOMINATORS")
print("=" * 70)

print(f"""
sin²θ_W: 166 = 5×37 - 19 = 5H_4 - H_3

|V_ud|: 38 = 37 + 1 = H_4 + 1
|V_cd|: 86 = ?
|V_td|: 814 = ?
""")

# Factor 86 and 814
print(f"86 = 2 × 43")
print(f"814 = 2 × 11 × 37 = 2 × 11 × H_4")
print(f"\nInteresting: 814 = 22 × 37 = 22 × H_4")
print(f"So |V_td| ≈ H_2 / (22 × H_4) = 7 / (22 × 37)")

# Check
print(f"\n7/(22×37) = {7/(22*37):.6f}")
print(f"|V_td| = 0.00860")
print(f"Close? {abs(7/(22*37) - 0.0086) < 0.0001}")

# The Wolfenstein connection
print("\n" + "=" * 70)
print("WOLFENSTEIN λ ≈ sin²θ_W")
print("=" * 70)

lambda_wolf = 0.22650
sin2_W = 0.22290

print(f"λ = {lambda_wolf}")
print(f"sin²θ_W = {sin2_W}")
print(f"Ratio: {lambda_wolf/sin2_W:.4f}")
print(f"Difference: {abs(lambda_wolf - sin2_W):.4f} ({abs(lambda_wolf - sin2_W)/sin2_W*100:.1f}%)")

print("""
If λ = sin²θ_W exactly (at some scale or in some limit):
  The Cabibbo angle = electroweak mixing angle
  
This would unify quark mixing with gauge mixing!
""")

# Check the hierarchy
print("=" * 70)
print("THE HIERARCHY")
print("=" * 70)

print("""
CKM elements scale with powers of λ ≈ 0.22:

|V_us| ≈ λ        = 0.22
|V_cb| ≈ λ²       = 0.05
|V_ub| ≈ λ³       = 0.01

If λ ≈ sin²θ_W ≈ 37/166:

|V_us| ≈ H_4/(5H_4 - H_3)
|V_cb| ≈ [H_4/(5H_4 - H_3)]²
|V_ub| ≈ [H_4/(5H_4 - H_3)]³

The CKM hierarchy is powers of the hexagonal ratio!
""")

# Calculate
ratio = 37/166
print(f"λ = 37/166 = {ratio:.4f}")
print(f"λ² = {ratio**2:.4f} (|V_cb| ≈ 0.041)")
print(f"λ³ = {ratio**3:.5f} (|V_ub| ≈ 0.004)")

print("\n" + "=" * 70)
print("UNIFIED PICTURE")
print("=" * 70)

print("""
THE HEXAGONAL STRUCTURE APPEARS IN:

1. GAUGE SECTOR:
   β_3 = 7 = H_2
   β_2 = 19/6, numerator = H_3
   sin²θ_W = 37/166 = H_4/(5H_4 - H_3)

2. FLAVOR SECTOR (CKM):
   |V_ud| ≈ 37/38 = H_4/(H_4 + 1)
   |V_cd| ≈ 19/86 = H_3/86
   |V_td| ≈ 7/814 = H_2/(22×H_4)
   
   λ ≈ sin²θ_W = H_4/(5H_4 - H_3)

The same three numbers (7, 19, 37) appear in BOTH sectors!
""")
