# Study Notes: Cyclotomic Field Arithmetic for Collatz Proof

## Key Theorems Absorbed

### 1. LTE Lemma (Lifting the Exponent)
For odd prime p with x ≡ y ≢ 0 (mod p):
- v_p(x^m - y^m) = v_p(x - y) + v_p(m)

**My use case**: For a^n - b^n with a = 4, b = 3:
- Primitive divisors of 4^d - 3^d control the structure
- Once p | 4^k - 3^k for minimal k, the valuation at multiples is determined by LTE

### 2. Galois Structure of Cyclotomic Fields
- Gal(Q(μ_n)/Q) ≅ (Z/nZ)^* via σ_a: ζ_n ↦ ζ_n^a
- σ_a(T(ζ_n)) = T(ζ_n^a) when T has rational coefficients
- **Critical**: If T(ζ_n) ≠ 0, then T(ζ_n^a) ≠ 0 for all a coprime to n

### 3. Frobenius at Prime p
For p ∤ n, the Frobenius σ_p ∈ Gal(Q(ζ_n)/Q) satisfies:
- σ_p(ζ_n) = ζ_n^p
- σ_p(x) ≡ x^p (mod P) for any prime P above p

**Key insight**: When p ≡ 1 (mod n), the Frobenius is trivial, so p splits completely.

### 4. Prime Splitting in Cyclotomic Fields
When p ∤ n:
- p splits completely in Q(ζ_n) iff p ≡ 1 (mod n)
- The residue field at any prime P above p is F_p
- Under the isomorphism Z[ζ_n]/P ≅ F_p, ζ_n maps to a primitive n-th root in F_p

### 5. Cyclotomic Polynomial Factorization (Theorem 5.3 from Conrad)
When p ∤ n, the irreducible factors of Φ_n(X) in F_p[X]:
- Are all distinct
- Each has degree = ord_p(X) where X is a root

---

## Application to My Problem

### Setup
- Blocking prime p has ord_p(4/3) = d where d | m
- This means: 4^d ≡ 3^d (mod p), so 4/3 is a d-th root of unity in F_p^*
- Since F_p^* is cyclic of order p-1, we need d | p-1, i.e., p ≡ 1 (mod d)

### The Norm Connection
Let T(X) = Σ c_k X^k where c_k are sums of powers of 2 (rational integers).

**Claim**: If T(ζ_d) ≠ 0 in Q(ζ_d), then the norm N = N_{Q(ζ_d)/Q}(T(ζ_d)) is a nonzero integer.

**Key Formula**: 
N = Π_{j coprime to d} T(ζ_d^j) = ±Res(T, Φ_d)

### The Critical Implication
For blocking prime p with d | m and ord_p(4/3) = d:
- p ≡ 1 (mod d), so p splits completely in Q(ζ_d)
- If p ∤ N = |Res(T, Φ_d)|, then T(ζ_d) ∉ P for any P above p
- Under the isomorphism Z[ζ_d]/P ≅ F_p, T(r) ≢ 0 (mod p)

**CONCLUSION**: 
To show T(r) ≢ 0 (mod p) for at least one blocking prime, I need:
**At least one blocking prime that doesn't divide Res(T, Φ_d)**.

---

## The Remaining Gap

For each failing divisor d of m where T(ζ_d) ≠ 0:
- R_d := |Res(T, Φ_d)| is a nonzero integer
- Blocking primes for d are primitive divisors of 4^d - 3^d
- Need: at least one primitive divisor p of 4^d - 3^d with p ∤ R_d

**Why this is hard**:
1. R_d can be quite large
2. There may be only finitely many primitive divisors
3. Need to show the set of primitive divisors isn't contained in the set of prime factors of R_d

**Possible approaches**:
1. Size argument: Show R_d is smaller than the product of all primitive divisors
2. Structural argument: Show primitive divisors have special arithmetic properties incompatible with dividing R_d
3. Probabilistic/density argument: Primitive divisors are "random" enough to miss the fixed set of primes dividing R_d

---

## What I Still Need to Learn

1. **Baker's method**: Could give bounds on how special values like T(ζ_d) relate to primes
2. **Distribution of primitive divisors**: How are they distributed? Any density results?
3. **Bounds on norms/resultants**: Can I bound |Res(T, Φ_d)| in terms of the structure of T?
4. **Zsigmondy refinements**: Results about the SIZE of primitive divisors, not just existence

The gap is genuine but now I understand it more precisely: it's about the arithmetic relationship between:
- The resultant Res(T, Φ_d) (determined by the bridge path structure)
- The primitive divisors of 4^d - 3^d (determined by cyclotomic arithmetic)

---

## New Insights from Glasby et al. (2017)

### The Φ*_n(q) Quantity
The paper "Primitive prime divisors and the n-th cyclotomic polynomial" defines:

Φ*_n(q) = Φ_n(q) / gcd(Φ_n(q), n)

This removes the "intrinsic divisor" (the prime dividing n itself, if any) and gives the "primitive part" of Φ_n(q).

### Key Property
For q^n - 1, the primitive prime divisors are exactly the prime divisors of Φ*_n(q).

### Bounds
The paper gives an algorithm for finding all (n, q) with Φ*_n(q) ≤ cn^k for any constants c, k.

This is directly relevant! If I can show that:
- |Res(T, Φ_d)| < Φ*_d(4/3) (the primitive part)

Then at least one primitive divisor doesn't divide the resultant.

### The q = 4/3 Case
For my problem, q = 4/3 and I'm looking at 4^d - 3^d = 3^d((4/3)^d - 1).

The primitive divisors of 4^d - 3^d are exactly the primitive divisors of (4/3)^d - 1 in the multiplicative sense, which divide Φ_d(4, 3).

---

## Refined Strategy

### What Would Close the Gap
NEED TO PROVE: For each failing divisor d of m where T(ζ_d) ≠ 0:

**Either**:
(A) |Res(T, Φ_d)| < min{p : p is primitive divisor of 4^d - 3^d}

**Or**:
(B) The product of all primitive divisors exceeds |Res(T, Φ_d)|

**Or**:
(C) Some structural property prevents all primitive divisors from dividing Res(T, Φ_d) simultaneously

### Size Considerations
For the uniform path with m steps:
- D = 4^m - 3^m ≈ 4^m for large m
- Φ_d(4, 3) ≈ (4/3 - 1)^{φ(d)} · 3^{φ(d)} = 3^{-φ(d)} for the lower bound... wait, that's not right

Actually, for a > b > 0:
(a - b)^{φ(n)} < Φ_n(a, b) < (a + b)^{φ(n)}

So for a = 4, b = 3:
1^{φ(d)} < Φ_d(4, 3) < 7^{φ(d)}

This means Φ_d(4, 3) is between 1 and 7^{φ(d)}.

The primitive divisors of 4^d - 3^d divide Φ_d(4, 3), which is bounded.

### The Core Tension
- Resultant Res(T, Φ_d) depends on the PATH structure
- Primitive divisors depend only on d (and the base 4, 3)
- For non-uniform paths, T ≠ uniform, so the resultant is some "random" integer
- Need: this "random" integer misses at least one primitive divisor
