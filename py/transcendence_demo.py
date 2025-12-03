"""
Transcendence Theory: Computational Demonstrations
Building domain expertise through implementation
"""

import math
from fractions import Fraction

# ============================================
# 1. CONTINUED FRACTIONS OF log(3)/log(2)
# ============================================

def continued_fraction_expansion(x, n_terms=20):
    """Compute continued fraction expansion of x"""
    cf = []
    for _ in range(n_terms):
        a = int(x)
        cf.append(a)
        x = x - a
        if abs(x) < 1e-15:
            break
        x = 1/x
    return cf

def convergents(cf):
    """Compute convergents p_n/q_n from continued fraction"""
    convs = []
    p_prev, p_curr = 1, cf[0]
    q_prev, q_curr = 0, 1
    convs.append((p_curr, q_curr))
    
    for i in range(1, len(cf)):
        p_new = cf[i] * p_curr + p_prev
        q_new = cf[i] * q_curr + q_prev
        convs.append((p_new, q_new))
        p_prev, p_curr = p_curr, p_new
        q_prev, q_curr = q_curr, q_new
    
    return convs

print("=" * 70)
print("TRANSCENDENCE THEORY: KEY CONCEPTS & COLLATZ CONNECTION")
print("=" * 70)

print("\n" + "-" * 70)
print("1. CONTINUED FRACTIONS OF δ = log(3)/log(2)")
print("-" * 70)

delta = math.log(3) / math.log(2)
print(f"\nδ = log(3)/log(2) = {delta:.15f}")

cf = continued_fraction_expansion(delta, 25)
print(f"\nContinued fraction: [{cf[0]}; {', '.join(map(str, cf[1:15]))}...]")

convs = convergents(cf)
print("\nConvergents (BEST rational approximations to δ):")
print("  p/q            value           |δ - p/q|        q·|δ-p/q|")
print("-" * 70)
for p, q in convs[:12]:
    val = p/q
    error = abs(delta - val)
    print(f"  {p}/{q}".ljust(16) + f"{val:.12f}    {error:.2e}      {q*error:.8f}")

print("\n→ Key insight: Convergents give BEST approximations to δ")
print("→ If (K+L)/K for a cycle is NOT a convergent, Baker bounds are needed!")

# ============================================
# 2. THE COLLATZ CONNECTION
# ============================================

print("\n" + "-" * 70)
print("2. CONNECTION TO COLLATZ m-CYCLES")
print("-" * 70)

print("""
For an m-cycle with K odd steps and L even steps:
  - Must have 2^{K+L} = ∏ (3nᵢ + 1) / ∏ nᵢ
  - Taking logarithms: (K+L)·log(2) - K·log(3) = Σ log(1 + 1/(3nᵢ))
  - The RHS is small and positive
  - So (K+L)/K must be VERY CLOSE to δ = log(3)/log(2)

BUT: The ratio (K+L)/K is constrained by cycle structure!
""")

# Which convergents could correspond to cycles?
print("Convergent denominators q (potential K values for cycles):")
print("  K      K+L    (K+L)/K         |deviation from δ|")
print("-" * 70)
for p, q in convs[:15]:
    ratio = p/q
    deviation = ratio - delta
    sign = "+" if deviation > 0 else "-"
    print(f"  {q:<6} {p:<6} {ratio:.12f}   {sign}{abs(deviation):.2e}")

# ============================================
# 3. WHY BAKER BOUNDS ARE ESSENTIAL
# ============================================

print("\n" + "-" * 70)
print("3. WHY BAKER'S THEOREM IS ESSENTIAL")
print("-" * 70)

print("""
The cycle equation gives:
  Λ = K·log(3) - (K+L)·log(2) + Σ log(1 + 1/(3nᵢ))
  
  Where |Λ| is very small but > 0 for nontrivial cycles.

Continued fractions tell us: for q = convergent denominator,
  |δ - p/q| < 1/(q·q_{next})

BUT cycles don't have to use convergent (K, K+L) pairs!

For ARBITRARY integer pairs, we need Baker-type bounds:
  |K·log(3) - N·log(2)| > exp(-C · log(K) · log(max{K,N}))

This is the ONLY way to handle non-convergent cases.
""")

# ============================================
# 4. BAKER-WÜSTHOLZ BOUND STRUCTURE
# ============================================

print("-" * 70)
print("4. BAKER-WÜSTHOLZ BOUND CONSTANTS")
print("-" * 70)

def baker_wustholz_exponent(n, d):
    """
    Exponent structure from Baker-Wüstholz 1993:
    (16nd)^{2(n+2)}
    """
    return (16*n*d)**(2*(n+2))

print("\nBaker-Wüstholz bound structure:")
print("  log|Λ| > -(16nd)^{2(n+2)} · log(A₁)···log(Aₙ) · log(B)")
print()
print("  n   d    (16nd)^{2(n+2)}")
print("-" * 40)
for n in [2, 3, 4]:
    for d in [2, 4]:
        exp = baker_wustholz_exponent(n, d)
        print(f"  {n}   {d}    {exp:.2e}")

print("\nFor Collatz (n=2, d~2): constant ≈ 10^8")
print("This is why computational verification is also essential!")

# ============================================
# 5. HERCHER'S ITERATIVE REFINEMENT
# ============================================

print("\n" + "-" * 70)
print("5. HERCHER'S ITERATIVE REFINEMENT (2023)")
print("-" * 70)

print("""
Starting point: K > 7×10¹¹ (Simons-de Weger 2005)

Each iteration:
  1. Use current K lower bound
  2. Apply Baker-type bounds to constrain (K+L)/K - δ
  3. Use continued fractions of δ to improve K bound
  4. Repeat

Results (conceptual):
  Iteration 0: K > 7.00×10¹¹
  Iteration 1: K > 3.76×10¹²
  Iteration 2: K > 1.82×10¹³
  ...
  Iteration 7: K > 4.79×10¹⁶

Upper bound from cycle structure: K < 1.4784 · m · δᵐ

For m = 91: K_upper ≈ 4.69×10¹⁶ → Still compatible
For m = 92: K_upper ≈ 7.65×10¹⁶ → CONTRADICTION!

Therefore: m ≤ 91.
""")

# ============================================
# 6. THE FUNDAMENTAL EQUATION
# ============================================

print("-" * 70)
print("6. THE FUNDAMENTAL CYCLE EQUATION")
print("-" * 70)

print("""
The m-cycle equation in matrix form (my approach):

  M · (a₁, ..., aₘ)ᵀ = (2^{ℓ₁}, ..., 2^{ℓₘ})ᵀ

where M has structure determined by (k₁,...,kₘ) and (ℓ₁,...,ℓₘ).

Cramer's rule gives: aᵢ = Nᵢ / det(M)

The key constraint: det(M) = 3^K - 2^{K+L}

This connects to Baker's theorem because:
  |3^K - 2^{K+L}| = 3^K · |1 - (2/3)^K · 2^L|
                  = 3^K · |1 - 2^{K+L}/3^K|
                  = 3^K · |1 - 2^{K+L-K·log₂(3)}|

And K+L - K·log₂(3) = K·(L/K + 1 - log₂(3)) = K·((K+L)/K - δ)

So the determinant being small ↔ (K+L)/K close to δ
And Baker bounds control HOW close it can be!
""")

# ============================================
# 7. SUMMARY
# ============================================

print("-" * 70)
print("7. SYNTHESIS: WHAT I'VE LEARNED")
print("-" * 70)

print("""
FROM TRANSCENDENCE THEORY:
  1. Linear forms in logarithms can't be "too small" unless zero
  2. Baker's theorem quantifies this with explicit constants
  3. The proof uses auxiliary functions + extrapolation
  4. Constants are huge but explicit: (16nd)^{2(n+2)}
  5. Specialized results for n=2 have smaller constants (~30)

FOR COLLATZ:
  1. m-cycles require (K+L)/K ≈ δ = log(3)/log(2)
  2. Baker bounds constrain how close this can be
  3. Hercher's iteration refines K bounds
  4. Combined with cycle growth bounds → m ≤ 91
  5. Verification to 2⁷¹ provides the "exterior bound"

META-LESSONS:
  1. Same methodology works: read primary sources, implement, understand
  2. The hard parts are specific (extrapolation, multiplicity estimates)
  3. I understand the structure, not all technical details
  4. Pedagogical clarity ≠ research contribution
  5. Genuine expertise requires knowing what you DON'T know
""")

print("=" * 70)
print("END OF DEMONSTRATION")
print("=" * 70)
