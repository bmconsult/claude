"""
DIRECT PROOF: D | S implies constant path (without tight primes)

The goal is to prove algebraically that for A = 2m:
  D | S  ⟺  δ = (2, 2, ..., 2)
"""

print("="*70)
print("DIRECT ALGEBRAIC PROOF ATTEMPT")
print("="*70)

print("""
SETUP:
  D = 4^m - 3^m
  S = Σ_{j=0}^{m-1} 3^{m-1-j} · 2^{prefix_j}
  
  For constant path (prefix_j = 2j):
    S = Σ 3^{m-1-j} · 4^j = (4^m - 3^m)/(4-3) = 4^m - 3^m = D

CLAIM: S = D only for constant path (when A = 2m).

PROOF ATTEMPT:
""")

print("="*70)
print("STEP 1: The S = D Identity")
print("="*70)

print("""
For S = D, we need:
  Σ_{j=0}^{m-1} 3^{m-1-j} · 2^{prefix_j} = Σ_{j=0}^{m-1} 3^{m-1-j} · 4^j

This is an equality of two sums with the same coefficients 3^{m-1-j}
but potentially different powers of 2.

LHS has powers: 2^{prefix_0}, 2^{prefix_1}, ..., 2^{prefix_{m-1}}
RHS has powers: 2^0, 2^2, 2^4, ..., 2^{2m-2} (i.e., 4^j = 2^{2j})

For the sums to be equal, we DON'T need term-by-term equality.
We need the total sum to match.
""")

print("="*70)
print("STEP 2: Uniqueness of Representation")
print("="*70)

print("""
KEY INSIGHT: D = 4^m - 3^m has a UNIQUE representation as a sum
of the form Σ c_j · 2^{e_j} where:
  - c_j = 3^{m-1-j} (fixed coefficients)
  - e_j is strictly increasing from 0
  - e_j ∈ {0, 1, ..., 2m-1} (for A = 2m)

Why unique? Consider the binary-ternary structure.

D = 4^m - 3^m can be expanded:
  D = Σ_{j=0}^{m-1} 3^{m-1-j} · 4^j  (by geometric series)

This is a weighted sum where:
  - Coefficient of 2^{2j} is 3^{m-1-j}
  - Coefficient of 2^k for odd k is 0
  - Coefficient of 2^{2j} comes ONLY from the j-th term

Now, can ANY other choice of exponents give the same sum?
""")

print("="*70)
print("STEP 3: Why Other Exponent Choices Fail")
print("="*70)

print("""
Suppose we have a different exponent sequence e_0 < e_1 < ... < e_{m-1}
with Σ e_j difference = 2m - (0) = 2m, all e_j ≥ 0.

For S = D, we need:
  Σ 3^{m-1-j} · 2^{e_j} = Σ 3^{m-1-j} · 2^{2j}

Consider this equation modulo various primes p.

For p | D = 4^m - 3^m:
  RHS ≡ 0 (mod p)  [since RHS = D]
  
So we need:
  Σ 3^{m-1-j} · 2^{e_j} ≡ 0 (mod p)

For the CONSTANT path, this holds because S = D.

For NON-CONSTANT paths, the sum is a different linear combination
of powers of 2, and there's no algebraic reason it should equal D.

The "rigidity" comes from the fact that D has a specific closed-form
expression (4^m - 3^m), while S with other exponents doesn't.
""")

print("="*70)
print("STEP 4: The Polynomial Perspective")
print("="*70)

print("""
Define P(x) = Σ_{j=0}^{m-1} 3^{m-1-j} · x^j = (x^m - 3^m)/(x - 3)

Key identity: P(4) = 4^m - 3^m = D

For CONSTANT path with exponents 2j:
  S = Σ 3^{m-1-j} · (2^2)^j = P(4) = D  ✓

For NON-CONSTANT path with exponents e_j:
  S = Σ 3^{m-1-j} · 2^{e_j}
  
  This is NOT P(x) evaluated at any single point!
  It's like P evaluated at m DIFFERENT points and summed.
  
  Specifically: S = Σ_j 3^{m-1-j} · 2^{e_j}
  
  If e_j = 2j: S = Σ_j 3^{m-1-j} · (2^2)^j = P(2^2) = P(4)
  
  If e_j ≠ 2j for some j: S ≠ P(x) for any x.
  
The polynomial identity P(4) = D is BROKEN when we don't use
evenly-spaced exponents.
""")

print("="*70)
print("STEP 5: Making This Rigorous")
print("="*70)

print("""
The challenge: How do we PROVE that Σ 3^{m-1-j} · 2^{e_j} ≠ D
for non-constant exponent sequences?

Approach 1: Show the sums have different 2-adic valuations
  D = 4^m - 3^m has v_2(D) = 0 (D is odd)
  S = Σ 3^{m-1-j} · 2^{e_j} 
  The first term is 3^{m-1} · 2^0 = 3^{m-1} (odd)
  So v_2(S) = 0 as well. This doesn't distinguish them.

Approach 2: Show they differ modulo small primes
  Need to find p where S ≢ D (mod p) for non-constant paths.
  We verified this computationally - the INTERSECTION of all
  prime constraints equals {constant path}.

Approach 3: Use generating functions / polynomial interpolation
  The values S for different exponent sequences span a space.
  D = P(4) is a specific point in this space.
  Show D is "isolated" - only reachable via constant exponents.
""")

# Let's try Approach 2 more carefully
print("="*70)
print("APPROACH 2: Modular Analysis")
print("="*70)

def gen_paths(m, A):
    if m == 1:
        if A >= 1: yield [A]
        return
    for d in range(1, A - m + 2):
        for rest in gen_paths(m - 1, A - d):
            yield [d] + rest

def compute_S(deltas, m):
    S = 0
    prefix = 0
    for j in range(m):
        S += 3**(m-1-j) * 2**prefix
        prefix += deltas[j]
    return S

# For m = 4, verify that S = D only for constant
m = 4
A = 8
D = 4**m - 3**m

print(f"\nm = {m}, D = {D}")
print("\nAll paths with S = D:")

for deltas in gen_paths(m, A):
    S = compute_S(deltas, m)
    if S == D:
        print(f"  δ = {deltas}, S = {S}")

print("\nAll paths with S = 2D:")
for deltas in gen_paths(m, A):
    S = compute_S(deltas, m)
    if S == 2*D:
        print(f"  δ = {deltas}, S = {S}")

print("\nAll paths with D | S:")
for deltas in gen_paths(m, A):
    S = compute_S(deltas, m)
    if S % D == 0:
        k = S // D
        print(f"  δ = {deltas}, S = {S}, k = {k}")

print("\n" + "="*70)
print("KEY FINDING")
print("="*70)

print("""
For m = 4, only the constant path has D | S (with k = 1).

This is NOT because of a tight prime (m = 4 has no tight prime).
It's because the INTERSECTION of constraints from all prime factors
of D = 175 = 5² × 7 forces the constant path.

THE REAL THEOREM:
  For all m, the set of (e_0, ..., e_{m-1}) where
  D | Σ 3^{m-1-j} · 2^{e_j}
  is exactly {(0, 2, 4, ..., 2m-2)} when we require:
  - 0 = e_0 < e_1 < ... < e_{m-1} ≤ 2m-1
  - Σ (e_j - e_{j-1}) = 2m with each gap ≥ 1

This is a number-theoretic fact about the divisibility structure
of weighted sums of powers of 2 by differences of powers.
""")

print("="*70)
print("THE PATH FORWARD")
print("="*70)

print("""
To prove this rigorously for all m, we need to show:

  4^m - 3^m CANNOT divide Σ_{j=0}^{m-1} 3^{m-1-j} · 2^{e_j}
  
  for any (e_0, ..., e_{m-1}) ≠ (0, 2, 4, ..., 2m-2)
  satisfying our constraints.

This is equivalent to:

  4^m - 3^m ∤ (S - D) for all non-constant S.

Where S - D = Σ 3^{m-1-j} · 2^{2j} · (2^{ε_j} - 1)
and ε_j = e_j - 2j is the deviation.

For non-constant paths, some ε_j ≠ 0.

THE KEY QUESTION: Why can't D divide this deviation sum?

This might follow from:
1. The specific factorization of D = 4^m - 3^m
2. The structure of the deviation sum
3. Some number-theoretic incompatibility

THIS IS WHERE THE PROOF CURRENTLY STANDS.
""")
