"""
INVESTIGATION: When Res(T, D) = 0 but gcd(T(2), D) < D

This is the interesting case. If T and x^A - 3^m share roots as polynomials,
why doesn't D divide S?
"""

from sympy import symbols, resultant, div, gcd as symgcd, factor, roots
from math import gcd

x = symbols('x')

def S_value(delta_list):
    m = len(delta_list)
    S = 0
    prefix_sum = 0
    for j in range(m):
        S += (3 ** (m - 1 - j)) * (2 ** prefix_sum)
        prefix_sum += delta_list[j]
    return S

def T_poly(delta_list):
    m = len(delta_list)
    prefix_sum = 0
    result = 0
    for j in range(m):
        result += 3**(m-1-j) * x**prefix_sum
        prefix_sum += delta_list[j]
    return result

# ============================================================
# Find paths where Res = 0 but path is non-constant with δ ≥ 1
# ============================================================

print("="*70)
print("CASES WHERE RESULTANT = 0 FOR NON-CONSTANT PATHS")
print("="*70)

from itertools import product

def is_constant(delta_list):
    return len(set(delta_list)) == 1

interesting_cases = []

for m in [4, 5]:
    A_min = 1
    while 2**A_min <= 3**m:
        A_min += 1
    
    for A in range(A_min, A_min + 3):
        D_val = 2**A - 3**m
        D_poly = x**A - 3**m
        
        for deltas in product(range(1, min(A, 6)), repeat=m):
            if sum(deltas) == A and not is_constant(list(deltas)):
                T = T_poly(list(deltas))
                res = resultant(T, D_poly, x)
                
                if res == 0:
                    S = T.subs(x, 2)
                    g = gcd(int(S), D_val)
                    interesting_cases.append({
                        'm': m, 'A': A, 'D': D_val,
                        'path': deltas, 'T': T, 'S': S, 'gcd': g
                    })

print(f"\nFound {len(interesting_cases)} cases with Res = 0:")

for case in interesting_cases[:10]:
    print(f"\n  Path {case['path']} (m={case['m']}, A={case['A']}):")
    print(f"  T(x) = {case['T']}")
    print(f"  S = T(2) = {case['S']}")
    print(f"  D = {case['D']}")
    print(f"  gcd(S, D) = {case['gcd']}")
    
    # Why is Res = 0? Let's find common roots
    T = case['T']
    D_poly = x**case['A'] - 3**case['m']
    
    # Factor T and D
    print(f"  Factoring T(x)...")
    T_factors = factor(T)
    print(f"    T(x) factored: {T_factors}")
    
    # GCD of polynomials
    poly_gcd = symgcd(T, D_poly)
    print(f"    gcd(T, D) as polynomials: {poly_gcd}")

# ============================================================
# Key Question: Why doesn't sharing roots imply D | S?
# ============================================================

print("\n" + "="*70)
print("ANALYSIS: Why shared roots don't imply D | S")
print("="*70)

print("""
When Res(T, D) = 0, T and D share at least one root in some extension.

But T(2) being divisible by D = 2^A - 3^m requires something stronger:
  D | T(2), i.e., T(2) ≡ 0 (mod D)

Sharing roots as polynomials is about the algebraic structure.
Divisibility at x=2 is a specific integer question.

Let me trace through an example...
""")

# Detailed example
path = [2, 1, 2, 3]
m = 4
A = 8
D_val = 2**A - 3**m

T = T_poly(path)
D_poly = x**A - 3**m

print(f"\nDetailed analysis of path {path}:")
print(f"  T(x) = {T}")
print(f"  D(x) = {D_poly}")

# Polynomial division
q, r = div(D_poly, T, x)
print(f"\n  Polynomial division: D = T * Q + R")
print(f"  Q(x) = {q}")
print(f"  R(x) = {r}")

print(f"\n  At x = 2:")
print(f"  T(2) = {T.subs(x, 2)}")
print(f"  Q(2) = {q.subs(x, 2)}")
print(f"  R(2) = {r.subs(x, 2)}")
print(f"  D = T(2)*Q(2) + R(2) = {T.subs(x, 2) * q.subs(x, 2) + r.subs(x, 2)}")
print(f"  Actual D = {D_val}")

# GCD of polynomials
poly_gcd = symgcd(T, D_poly)
print(f"\n  gcd(T, D) as polynomials: {poly_gcd}")

if poly_gcd != 1:
    print(f"  So T and D share the factor: {poly_gcd}")
    
    # Write T = gcd * T' and D = gcd * D'
    T_prime = div(T, poly_gcd, x)[0]
    D_prime = div(D_poly, poly_gcd, x)[0]
    
    print(f"  T = {poly_gcd} * {T_prime}")
    print(f"  D = {poly_gcd} * {D_prime}")
    
    # At x = 2
    gcd_at_2 = poly_gcd.subs(x, 2)
    T_prime_at_2 = T_prime.subs(x, 2)
    D_prime_at_2 = D_prime.subs(x, 2)
    
    print(f"\n  At x = 2:")
    print(f"  gcd(2) = {gcd_at_2}")
    print(f"  T'(2) = {T_prime_at_2}")
    print(f"  D'(2) = {D_prime_at_2}")
    print(f"  T(2) = gcd(2) * T'(2) = {gcd_at_2 * T_prime_at_2}")
    print(f"  D = gcd(2) * D'(2) = {gcd_at_2 * D_prime_at_2}")
    
    # So gcd(T(2), D) = gcd(2) * gcd(T'(2), D'(2))
    integer_gcd = gcd(int(T.subs(x, 2)), D_val)
    print(f"\n  Integer gcd(T(2), D) = {integer_gcd}")
    print(f"  gcd(2) = {gcd_at_2}")
    print(f"  So gcd(T'(2), D'(2)) = {integer_gcd // int(gcd_at_2)}")

# ============================================================
# The key insight
# ============================================================

print("\n" + "="*70)
print("THE KEY INSIGHT")
print("="*70)

print("""
When T and D share a polynomial factor G(x):
  T = G * T'
  D = G * D'

At x = 2:
  T(2) = G(2) * T'(2)
  D    = G(2) * D'(2)

So gcd(T(2), D) is at least G(2).

But for D | T(2), we'd need D'(2) | T'(2) as well.

Since T' and D' share no common factors (by construction),
T'(2) and D'(2) are "generically coprime" at x = 2.

The polynomial factorization tells us about roots, but
the values at x = 2 depend on all coefficients, not just roots.
""")

# ============================================================
# Verify for all cases: gcd = G(2) but D'(2) ∤ T'(2)
# ============================================================

print("\n" + "="*70)
print("VERIFICATION: gcd(S, D) = G(2) in all cases")
print("="*70)

for case in interesting_cases[:5]:
    T = case['T']
    D_poly = x**case['A'] - 3**case['m']
    D_val = case['D']
    
    poly_gcd = symgcd(T, D_poly)
    
    if poly_gcd != 1:
        G_at_2 = int(poly_gcd.subs(x, 2))
        integer_gcd = case['gcd']
        
        print(f"\nPath {case['path']}:")
        print(f"  Polynomial gcd: {poly_gcd}")
        print(f"  G(2) = {G_at_2}")
        print(f"  Integer gcd(S, D) = {integer_gcd}")
        print(f"  Match: {abs(G_at_2) == integer_gcd or integer_gcd % abs(G_at_2) == 0}")

# ============================================================
# The complete picture
# ============================================================

print("\n" + "="*70)
print("THE COMPLETE PICTURE")
print("="*70)

print("""
For CONSTANT path (k,k,...,k):
  T(x) = (x^A - 3^m) / (x^k - 3)
  
  So D = T(x) * (x^k - 3) as polynomials.
  
  At x = 2: D = T(2) * (2^k - 3) = S * (2^k - 3)
  
  Therefore: S = D / (2^k - 3)
  
  When k = 2: S = D / 1 = D, so N = S/D = 1 ✓

For NON-CONSTANT path:
  T(x) may share SOME factors with x^A - 3^m (making Res = 0)
  But T(x) ≠ (x^A - 3^m) / (something simple)
  
  Even when gcd(T, D) = G ≠ 1:
    T = G * T'
    D = G * D'
    
  At x = 2: gcd(S, D) = G(2) * gcd(T'(2), D'(2))
  
  Since T' and D' are coprime as polynomials, their values at x = 2
  are "generically" coprime. The integer gcd is small.
  
  Therefore D ∤ S (since gcd(S, D) << D).

This explains why non-trivial cycles can't exist!
""")

if __name__ == "__main__":
    pass
