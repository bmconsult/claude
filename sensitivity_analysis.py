#!/usr/bin/env python3
"""
Critical sensitivity analysis: How robust is sin²θ_W = 37/166?
"""

def continued_fraction(x, max_terms=20):
    cf = []
    for _ in range(max_terms):
        a = int(x)
        cf.append(a)
        frac = x - a
        if abs(frac) < 1e-12:
            break
        x = 1 / frac
    return cf

def convergents(cf):
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

print("=" * 70)
print("CRITICAL SENSITIVITY ANALYSIS")
print("=" * 70)

# Exact experimental values
sin2_onshell = 0.22290  # On-shell definition at M_Z
sin2_onshell_err = 0.00030  # Uncertainty
sin2_msbar = 0.23122  # MS-bar at M_Z

print(f"""
EXPERIMENTAL VALUES:
  sin²θ_W (on-shell) = {sin2_onshell} ± {sin2_onshell_err}
  sin²θ_W (MS-bar)   = {sin2_msbar}

37/166 = {37/166:.6f}
""")

# Check the range where 37/166 is the best rational approximation
print("=" * 70)
print("FINDING THE EXACT RANGE WHERE 37/166 IS OPTIMAL")
print("=" * 70)

# 37/166 is between convergents 35/157 and 72/323
# (these are the neighbors in the Farey sequence/Stern-Brocot tree)
conv_before = (35, 157)  # Previous convergent
conv_after = (72, 323)   # Would be next but CF structure differs

# The mediant gives the boundary
lower = 35/157
upper = 37/166 + (37/166 - 35/157)  # Approximate upper bound

print(f"35/157 = {35/157:.6f}")
print(f"37/166 = {37/166:.6f}")

# Fine scan to find exact range
print("\nFine scan to find where 37 appears as convergent numerator:")
matches = []
for i in range(-100, 100):
    val = 0.22290 + i * 0.00001
    cf = continued_fraction(val)
    convs = convergents(cf)
    for num, den in convs[:8]:
        if num == 37:
            matches.append((val, den))
            break

if matches:
    print(f"37 appears for sin²θ_W in range [{matches[0][0]:.5f}, {matches[-1][0]:.5f}]")
    print(f"Width of range: {matches[-1][0] - matches[0][0]:.5f}")
    print(f"Experimental uncertainty: ±{sin2_onshell_err}")
    
    # Check what denominators appear
    denoms = set(d for v, d in matches)
    print(f"Denominators that appear with 37: {denoms}")

# Check if experimental value is within range
exp_min = sin2_onshell - sin2_onshell_err
exp_max = sin2_onshell + sin2_onshell_err
print(f"\nExperimental range: [{exp_min:.5f}, {exp_max:.5f}]")

in_range = any(exp_min <= v <= exp_max for v, d in matches)
print(f"37/166 range overlaps experimental range: {in_range}")

# What convergent does MS-bar give?
print("\n" + "=" * 70)
print("MS-BAR VALUE ANALYSIS")
print("=" * 70)

cf_msbar = continued_fraction(sin2_msbar)
conv_msbar = convergents(cf_msbar)
print(f"sin²θ_W (MS-bar) = {sin2_msbar}")
print(f"Continued fraction: {cf_msbar[:8]}")
print(f"Convergents: {conv_msbar[:6]}")

# Check for hexagonal numbers
print("\nChecking for hexagonal numbers in MS-bar convergents:")
def H(n):
    return 3*n*n - 3*n + 1

hex_set = {H(n): n for n in range(1, 20)}
for num, den in conv_msbar[:8]:
    if num in hex_set:
        print(f"  {num}/{den}: numerator {num} = H_{hex_set[num]}")
    if den in hex_set:
        print(f"  {num}/{den}: denominator {den} = H_{hex_set[den]}")

# The key question
print("\n" + "=" * 70)
print("THE CRITICAL QUESTION")
print("=" * 70)
print("""
ON-SHELL vs MS-BAR:

The on-shell definition is measured directly from the W and Z masses:
  sin²θ_W = 1 - M_W²/M_Z²

The MS-bar definition includes quantum corrections and is scale-dependent.

Which is more "fundamental"?

Physics perspective: MS-bar is cleaner theoretically (no mass threshold issues)
Our perspective: On-shell gives hexagonal structure, MS-bar doesn't

This is either:
  (A) Evidence that on-shell is the "natural" definition
  (B) A coincidence that happens to work for on-shell
  
The on-shell value 0.22290 is VERY close to 37/166 = 0.22289...
The difference is 0.00001, much smaller than experimental error.

This precision is suspicious - either:
  1. It's exactly 37/166 (prediction)
  2. It's a coincidence within measurement precision
""")

# Final calculation: how precise is the match?
print("=" * 70)
print("PRECISION OF THE MATCH")
print("=" * 70)

exact_37_166 = 37/166
measured = 0.22290
diff = abs(exact_37_166 - measured)
sigma = diff / sin2_onshell_err

print(f"37/166 = {exact_37_166:.8f}")
print(f"Measured = {measured:.8f}")
print(f"Difference = {diff:.8f}")
print(f"In units of σ: {sigma:.2f}σ")
print(f"\nThe measured value is {sigma:.2f}σ away from exactly 37/166.")
print("This is EXTREMELY close - essentially a perfect match within error.")
