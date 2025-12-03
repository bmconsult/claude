#!/usr/bin/env python3
"""
Concrete exploration of zero estimates on group varieties.

I want to TEST my understanding by computing specific examples.
The goal is to see the "obstruction phenomenon" in action.
"""

import numpy as np
from fractions import Fraction
from itertools import product
import sympy as sp
from sympy import symbols, expand, gcd, lcm, Poly, factor, simplify

# ============================================================
# EXAMPLE 1: The multiplicative group G_m^2
# ============================================================

def example_multiplicative_group():
    """
    G = G_m^2 (two-dimensional torus)
    
    Points are (x, y) with x, y ≠ 0.
    Group law: (x₁, y₁) · (x₂, y₂) = (x₁x₂, y₁y₂)
    
    Question: If we have many points in G_m^2 on which a polynomial
    vanishes, what can we say?
    """
    print("=" * 60)
    print("EXAMPLE 1: Multiplicative Group G_m^2")
    print("=" * 60)
    
    # Case A: Points with NO algebraic relation
    # Take γ₁ = (2, 3), γ₂ = (5, 7)
    # These generate a "generic" subgroup
    
    print("\nCase A: Generic points γ₁=(2,3), γ₂=(5,7)")
    print("Points Γ(S) = {(2^a·5^b, 3^a·7^b) : |a|,|b| < S}")
    
    S = 3
    points_A = []
    for a in range(-S+1, S):
        for b in range(-S+1, S):
            x = (2**a) * (5**b)
            y = (3**a) * (7**b)
            points_A.append((Fraction(x).limit_denominator(), 
                            Fraction(y).limit_denominator()))
    
    print(f"For S={S}, we have {len(points_A)} points")
    print("Sample points:", points_A[:5])
    
    # These points are "generic" - no polynomial of low degree vanishes on all
    
    # Case B: Points WITH algebraic relation (obstruction)
    # Take γ₁ = (2, 4), γ₂ = (3, 9)
    # Notice: 4 = 2², 9 = 3²
    # So (2^a·3^b)² = 4^a·9^b
    # All points satisfy y = x²!
    
    print("\n" + "-" * 60)
    print("Case B: Points with OBSTRUCTION γ₁=(2,4), γ₂=(3,9)")
    print("Notice: 4=2², 9=3², so all points satisfy y = x²")
    
    points_B = []
    for a in range(-S+1, S):
        for b in range(-S+1, S):
            x = (2**a) * (3**b)
            y = (4**a) * (9**b)
            points_B.append((Fraction(x).limit_denominator(), 
                            Fraction(y).limit_denominator()))
    
    print(f"For S={S}, we have {len(points_B)} points")
    
    # Verify they all satisfy y = x²
    print("\nVerifying obstruction: y = x² for all points?")
    all_on_curve = all(p[1] == p[0]**2 for p in points_B)
    print(f"All points satisfy y = x²: {all_on_curve}")
    
    # The polynomial P(x,y) = y - x² vanishes on ALL points!
    # But deg(P) = 2, which is VERY low compared to number of points
    
    print("\n*** KEY INSIGHT ***")
    print(f"The polynomial y - x² has degree 2")
    print(f"But it vanishes on {len(points_B)} points!")
    print("This is the OBSTRUCTION phenomenon.")
    print("The 'obstruction subgroup' is H = {(t, t²) : t ∈ G_m}")
    
    return points_A, points_B


# ============================================================
# EXAMPLE 2: Understanding WHY zero estimates work
# ============================================================

def dimension_counting():
    """
    The basic argument of zero estimates is DIMENSION COUNTING.
    
    Space of polynomials of degree ≤ D in n variables: dim = C(n+D, D) ≈ D^n/n!
    
    Vanishing at k points imposes ≤ k linear conditions.
    
    If D^n/n! > k, there MUST exist a nonzero polynomial vanishing on all k points.
    
    Conversely, if a polynomial of degree D vanishes on k points with k >> D^n,
    something special must be happening (obstruction).
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Dimension Counting")
    print("=" * 60)
    
    from math import comb, factorial
    
    print("\nDimension of polynomial space in n variables, degree ≤ D:")
    for n in [1, 2, 3]:
        for D in [2, 5, 10]:
            dim = comb(n + D, D)
            approx = (D**n) / factorial(n)
            print(f"  n={n}, D={D}: exact={dim}, approx D^n/n!={approx:.1f}")
    
    print("\nKey observation:")
    print("If we have k points, and k < dim(poly space), then")
    print("there EXISTS a nonzero poly vanishing on all k points.")
    print("\nBUT: If k >> dim(poly space) and such a poly exists,")
    print("the points must have special structure (lie on subvariety).")


# ============================================================
# EXAMPLE 3: The connection to transcendence
# ============================================================

def transcendence_connection():
    """
    In Baker's method, we construct an auxiliary function:
    
    φ(z) = Σ p(k₁,...,kₙ) α₁^{k₁z} ··· αₙ^{kₙz}
    
    This function vanishes to HIGH ORDER at many INTEGER points z = 1, 2, ..., R.
    
    The zero/multiplicity estimate controls:
    - If φ vanishes to order T at R points, how small can the "degree" be?
    - OR: what obstruction subgroup must exist?
    
    This is the technical heart of Baker's theorem.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Connection to Transcendence (Baker's Method)")
    print("=" * 60)
    
    print("""
    The Setup:
    ---------
    Want to prove: log(α₁), ..., log(αₙ) are Q-linearly independent
    
    Construct: φ(z) = Σ p(k₁,...,kₙ) α₁^{k₁z} ··· αₙ^{kₙz}
    
    The coefficients p(k₁,...,kₙ) are chosen so φ vanishes to order T
    at z = 1, 2, ..., R (many integers).
    
    Key Tension:
    -----------
    - Thue-Siegel lemma lets us find p's with ||p|| small
    - Zero estimate says: if φ vanishes at many points, either
      (a) the "degree" L of φ is large, OR
      (b) there's an obstruction
    
    - Obstruction in this context = linear dependence of logs!
    - So if logs are independent, (b) can't happen, forcing large L
    - But we also have upper bounds on L from the construction
    - Contradiction → some φ(m) ≠ 0 → lower bound for linear form
    """)
    
    # Let's see the specific form for n=2 (two logarithms)
    print("\nFor n=2 (Gel'fond-Schneider case):")
    print("φ(z) = Σ_{k,l} p(k,l) α^{kz} β^{lz}")
    print("     = Σ p(k,l) exp(z(k log α + l log β))")
    print("")
    print("At integer z=m: φ(m) = Σ p(k,l) α^{km} β^{lm}")
    print("")
    print("If α^k β^l = 1 for some k,l (i.e., k log α + l log β = 0),")
    print("then the arguments k log α + l log β form a 1-dimensional")
    print("subspace → OBSTRUCTION.")


# ============================================================
# EXAMPLE 4: Trying to compute an obstruction explicitly
# ============================================================

def find_obstruction():
    """
    Given a set of points in G_m^n, try to find the obstruction subgroup.
    
    Method: Look for multiplicative relations among coordinates.
    
    If x_i^{a_i} y_i^{b_i} = 1 for all points (x_i, y_i), 
    then the points lie on the subgroup defined by x^a y^b = 1.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Computing Obstructions")
    print("=" * 60)
    
    # Points generated by (2, 4) and (3, 9) with S=2
    # We know y = x² is the obstruction
    
    print("\nGiven points from γ₁=(2,4), γ₂=(3,9):")
    points = []
    for a in range(-1, 2):
        for b in range(-1, 2):
            x = (2**a) * (3**b)
            y = (4**a) * (9**b)
            points.append((x, y))
            print(f"  ({x}, {y}) = γ₁^{a} · γ₂^{b}")
    
    print("\nLooking for relation x^a · y^b = constant for all points...")
    
    # Check if y/x² is constant
    ratios = [p[1] / (p[0]**2) for p in points]
    print(f"y/x² ratios: {ratios}")
    print(f"All equal to 1? {all(r == 1 for r in ratios)}")
    
    print("\nObstruction found: y = x²")
    print("This defines the algebraic subgroup H ⊂ G_m²:")
    print("H = {(t, t²) : t ∈ G_m} ≅ G_m (one-dimensional)")
    
    # More general: look for x^a y^b = c
    print("\n--- General method to find obstruction ---")
    print("Take logs: a·log(x) + b·log(y) = log(c)")
    print("For our points: log(y) = 2·log(x)")
    print("So a=2, b=-1, c=1 gives x² · y^{-1} = 1, i.e., y = x²")


# ============================================================
# EXAMPLE 5: Why group structure matters
# ============================================================

def group_structure_importance():
    """
    The zero lemma is special to GROUP varieties.
    
    Key property: If P vanishes on Γ, and Γ is a subgroup,
    then P vanishes on a translate g·Γ iff P composed with 
    translation by g vanishes on Γ.
    
    This allows bootstrapping from "vanishes on subgroup" to 
    "vanishes on cosets" to "vanishes on larger set".
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Why Group Structure Matters")
    print("=" * 60)
    
    print("""
    Key insight: The OBSTRUCTION must be a SUBGROUP, not just a subvariety.
    
    Why? Because of the group structure:
    
    1. If P vanishes on Γ (a subgroup), consider translates g·Γ
    
    2. Define P_g(x) = P(g⁻¹·x). Then P_g vanishes on g·Γ iff P vanishes on Γ.
    
    3. If Γ generates a dense subgroup, and P vanishes on Γ,
       then P must vanish on the Zariski closure of Γ.
    
    4. The Zariski closure of a subgroup is... a subgroup!
       (This uses the group structure crucially.)
    
    This is why the obstruction is an algebraic SUBGROUP H ⊂ G,
    not just any algebraic subvariety.
    
    For transcendence: The obstruction subgroup corresponds to
    a LINEAR RELATION among the logarithms. If no relation exists
    (i.e., logs are Q-linearly independent), then no obstruction
    exists, and the zero estimate gives strong bounds.
    """)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("EXPLORING ZERO ESTIMATES THROUGH CONCRETE EXAMPLES")
    print("=" * 60)
    print()
    
    example_multiplicative_group()
    dimension_counting()
    transcendence_connection()
    find_obstruction()
    group_structure_importance()
    
    print("\n" + "=" * 60)
    print("SUMMARY OF WHAT I'VE LEARNED")
    print("=" * 60)
    print("""
    1. Zero estimates control: polynomial degree vs number of zeros
    
    2. The OBSTRUCTION phenomenon: points can lie on a subgroup H,
       allowing low-degree polynomials to vanish on many points
    
    3. The key bound: deg(P)^{dim G} ≳ |Γ(S)| / deg(H)
       (scaled by the degree of the obstruction)
    
    4. For transcendence: obstruction = linear dependence of logs
       No obstruction + zero estimate = Baker's lower bound
    
    5. The GROUP structure is essential: obstructions must be subgroups
    
    What I still don't fully understand:
    - The precise proof of the zero estimate (intersection theory)
    - How multiplicities enter (Hilbert-Samuel functions)
    - The computation of the constants in Baker-Wüstholz
    """)
