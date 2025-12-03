"""
KEY HYPOTHESIS: For ANY m (prime or composite), Φ_m(4,3) alone blocks all non-uniform.

If true, this closes the gap completely!
"""

from sympy import factorint, isprime, cyclotomic_poly, totient, symbols
from itertools import product
import sympy

print("=" * 70)
print("HYPOTHESIS: Φ_m(4,3) ALONE BLOCKS ALL NON-UNIFORM")
print("=" * 70)

x = symbols('x')

def phi_m_value(m):
    """Compute Φ_m(4,3)."""
    phi_m = cyclotomic_poly(m, x)
    deg = totient(m)
    val = phi_m.subs(x, sympy.Rational(4, 3))
    return int(3**deg * val)

def compute_N(m, eps):
    """Compute N for a bridge ε."""
    # s_i = 2i + eps_i
    # N = Σ 3^{m-1-i} · 2^{s_i}
    N = 0
    for i in range(m):
        s_i = 2*i + eps[i]
        N += (3**(m-1-i)) * (2**s_i)
    return N

def enumerate_bridges(m, max_height=4):
    """Enumerate valid bridges for m."""
    bridges = []
    
    def backtrack(pos, current):
        if pos == m:
            # Check return constraint: step from ε_{m-1} to ε_m = 0 must be ≥ -1
            # i.e., 0 - current[-1] ≥ -1, so current[-1] ≤ 1
            if current[-1] <= 1:
                bridges.append(tuple(current))
            return
        
        last = current[-1]
        for step in range(-1, max_height + 1):
            next_val = last + step
            if -max_height <= next_val <= max_height:
                # Check if can still return to ≤ 1 at end
                remaining = m - 1 - pos
                if next_val - remaining <= 1:
                    current.append(next_val)
                    backtrack(pos + 1, current)
                    current.pop()
    
    backtrack(1, [0])
    return bridges

def test_phi_m_blocking(m):
    """Test if Φ_m(4,3) alone blocks all non-uniform."""
    
    phi_m = phi_m_value(m)
    print(f"\nm = {m}: Φ_{m}(4,3) = {phi_m} = {factorint(phi_m)}")
    
    bridges = enumerate_bridges(m)
    uniform = tuple([0] * m)
    
    non_uniform_passing = []
    
    for eps in bridges:
        if eps == uniform:
            continue
        
        N = compute_N(m, eps)
        
        # Check if Φ_m(4,3) | N
        # Need to handle fractional 2^{ε_i} carefully
        # Actually N might not be an integer if ε_i < 0
        
        # Scale N to make it an integer
        min_eps = min(eps)
        if min_eps < 0:
            N_scaled = N * (2 ** (-min_eps))
            # Check divisibility: Φ_m | N_scaled means Φ_m | N (since gcd(2, Φ_m) = 1)
        else:
            N_scaled = N
        
        # Convert to integer
        N_int = int(N_scaled)
        
        if N_int % phi_m == 0:
            non_uniform_passing.append(eps)
    
    if non_uniform_passing:
        print(f"  ⚠ {len(non_uniform_passing)} NON-UNIFORM pass Φ_{m} test!")
        for eps in non_uniform_passing[:5]:
            N = compute_N(m, eps)
            print(f"    ε = {eps}, N = {N}")
        return False
    else:
        print(f"  ✓ ALL {len(bridges)-1} non-uniform BLOCKED by Φ_{m}!")
        return True

print("\nTesting for m = 2 to 12:")
results = {}
for m in range(2, 13):
    results[m] = test_phi_m_blocking(m)

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

all_pass = all(results.values())
print(f"\nAll m pass: {all_pass}")

if all_pass:
    print("""
CONCLUSION: Φ_m(4,3) ALONE blocks all non-uniform for m = 2 to 12!

This means we don't need the "covering" argument at all!
The constraint at the Φ_m factor is sufficient.

Why does this work for composite m?

For prime m: deg(Φ_m) = m-1 = deg(P), polynomial argument works.

For composite m: deg(Φ_m) = φ(m) < m-1, BUT:
The constraint P(r) = 0 at r = primitive m-th root still blocks
all non-uniform because the BRIDGE CONSTRAINTS + constraint P(r) = 0
together force P = 0.

The key is: P(x) = Σ (2^{ε_i} - 1) x^i has VERY SPECIAL coefficients!
They're not arbitrary - they come from a bridge structure.

This extra structure makes P(r) = 0 impossible for non-uniform bridges.
""")
else:
    print("\nSome m failed - need to investigate further.")

print("\n" + "=" * 70)
print("ALGEBRAIC PROOF ATTEMPT")
print("=" * 70)

print("""
THEOREM: For any m ≥ 2 and any non-uniform bridge ε, Φ_m(4,3) ∤ N_ε.

PROOF IDEA:

Let r = 4/3 mod p for any prime p | Φ_m(4,3). Then ord_p(r) = m.

The constraint Φ_m(4,3) | N_ε is equivalent to:
    Σ_{i=0}^{m-1} r^i · 2^{ε_i} ≡ 0 (mod p)  for all p | Φ_m(4,3)

For uniform (all ε_i = 0):
    Σ r^i = 0 ✓ (sum of m-th roots of unity)

For non-uniform, write:
    Σ r^i · 2^{ε_i} = Σ r^i + Σ r^i · (2^{ε_i} - 1) = 0 + Σ r^i · c_i

where c_i = 2^{ε_i} - 1 is the perturbation.

KEY STRUCTURAL PROPERTIES:
1. c_0 = 0 (since ε_0 = 0)
2. c_i = 2^{ε_i} - 1 are NOT arbitrary - they're determined by a bridge
3. Bridge: steps ≥ -1, returns to 0

CLAIM: For any non-uniform bridge, Σ r^i c_i ≠ 0 for some primitive m-th root r.

This is equivalent to: Φ_m(x) ∤ C(x) where C(x) = Σ c_i x^i.

Since C(0) = c_0 = 0, we have C(x) = x · C'(x) for some C'.

For Φ_m | C, we'd need Φ_m | C' (since gcd(Φ_m, x) = 1).

But deg(C') = m - 2 and the coefficients of C' = (c_1, c_2, ..., c_{m-1})
have very specific structure from the bridge constraints.

For prime m: deg(Φ_m) = m-1 > deg(C'), so Φ_m ∤ C' unless C' = 0.

For composite m: deg(Φ_m) = φ(m) ≤ m-2, so Φ_m | C' is possible in principle.
But the specific structure of bridge-derived c_i prevents this.

The proof that bridge structure prevents Φ_m | C' is what we're verifying.
""")

# Let's examine the structure more carefully
print("\n" + "=" * 70)
print("EXAMINING THE STRUCTURE OF C' FOR COMPOSITE m")
print("=" * 70)

def analyze_C_prime(m):
    """Analyze when Φ_m could divide C' for bridges."""
    
    if isprime(m):
        print(f"\nm = {m} (prime): deg(Φ_m) = {m-1} > deg(C') = {m-2}, so Φ_m ∤ C' unless C' = 0")
        return
    
    phi_m_deg = totient(m)
    C_prime_deg = m - 2
    
    print(f"\nm = {m} (composite): deg(Φ_m) = {phi_m_deg}, deg(C') = {C_prime_deg}")
    
    if phi_m_deg > C_prime_deg:
        print(f"  deg(Φ_m) > deg(C'), so Φ_m ∤ C' unless C' = 0")
        return
    
    print(f"  deg(Φ_m) ≤ deg(C'), so Φ_m | C' is algebraically possible")
    print(f"  But bridge constraints prevent it!")
    
    # Show the cyclotomic polynomial
    phi_m = cyclotomic_poly(m, x)
    print(f"  Φ_{m}(x) = {phi_m}")
    
    # For Φ_m | C', we need C' = Q · Φ_m for some Q
    # The constant term of C' is c_1 = 2^{ε_1} - 1
    # The constant term of Φ_m is Φ_m(0) = 1
    # So Q(0) = c_1
    
    print(f"  For Φ_m | C', need C' = Q · Φ_m")
    print(f"  Comparing constant terms: c_1 = Q(0) · 1 = Q(0)")
    print(f"  But c_1 = 2^{{ε_1}} - 1 ∈ {{..., -1/2, 0, 1, 3, 7, ...}}")

for m in [4, 6, 8, 9, 10, 12]:
    analyze_C_prime(m)
