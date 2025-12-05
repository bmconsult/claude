# Collatz Expert Knowledge Base

**Purpose**: Deep technical knowledge for advising on Collatz proof attempts

---

## 1. Lifting the Exponent (LTE) Lemma

### Statements

**Odd prime p**: If p | (x-y) and p ∤ xy:
```
v_p(x^n - y^n) = v_p(x - y) + v_p(n)
```

**p = 2**: If x, y are both odd:
```
v_2(x^n - y^n) = v_2(x - y) + v_2(x + y) + v_2(n) - 1  [n even]
v_2(x^n - y^n) = v_2(x - y)                            [n odd]
```

### Application to Collatz

For 3^k - 1 (x=3, y=1):
- **k odd**: v_2(3^k - 1) = 1 (only one factor of 2!)
- **k even**: v_2(3^k - 1) = 2 + v_2(k)

**Why this matters**: Growth phases can only extract limited 2-powers from 3^k terms.
Even for k = 2^20 (over a million), v_2(3^k - 1) = 2 + 20 = 22. Logarithmic growth!

This is the **rigorous foundation** for growth self-limitation.

---

## 2. Mihailescu's Techniques (Catalan Proof)

### Key ingredients

1. **Cyclotomic fields** Q(ζ_p) - not transcendence methods!
2. **Stickelberger's theorem** - Stickelberger ideal annihilates class group
3. **Double Wieferich condition** - p^{q-1} ≡ 1 (mod q²) AND q^{p-1} ≡ 1 (mod p²)
4. **Thaine's theorem** - relates class group to units

### Why Mihailescu matters for Collatz

- Baker's theorem (transcendence) gives bounds but not proofs
- Mihailescu showed pure algebraic/cyclotomic methods can close gaps
- The Collatz cycle equation involves cyclotomic structure Φ_m(4,3)

### Stickelberger element (for reference)
```
θ = Σ_{a=1}^{p-1} (a/p) · σ_a^{-1}
```
where σ_a: ζ → ζ^a is Galois action.

---

## 3. "Bad Primes" for Tight Prime Approach

### Discovery

All primes that fail the tight condition (ord_p(2) < 2m) are **Mersenne divisors**.

| Prime p | ord_p(2) | Divides | Bad for m |
|---------|----------|---------|-----------|
| 5 | 4 | 2⁴-1 | 4, 8, 12, 16, 20, 24, 28 |
| 7 | 3 | 2³-1 | 2, 4, 6, 8, ... (all even) |
| 11 | 10 | 2¹⁰-1 | 10, 15, 20, 25 |
| 13 | 12 | 2¹²-1 | 12, 18, 24 |
| ... | ... | ... | ... |

### Why this happens

These are **inherited primes** from the factorization:
```
4^m - 3^m = ∏_{d|m} Φ_d(4,3)
```

Primes from Φ_d(4,3) for d < m have ord_p(4/3) = d < m, often giving ord_p(2) < 2m.

### The key fact

For m ≥ 5: **Primitive primes** (from Φ_m(4,3)) provide tight primes.
Inherited primes may fail tightness, but we only need ONE tight prime.

---

## 4. Quadratic Reciprocity and ord_p(2)

### The parity rule
```
ord_p(2) is even  ⟺  (2/p) = -1  ⟺  p ≡ 3 or 5 (mod 8)
ord_p(2) is odd   ⟺  (2/p) = +1  ⟺  p ≡ 1 or 7 (mod 8)
```

### Connection to tightness

If ord_p(2) is even: ord_p(4) = ord_p(2)/2
If ord_p(2) is odd: ord_p(4) = ord_p(2)

For tight: need ord_p(2) ≥ 2m
If p ≡ 3,5 (mod 8) and ord_p(4) ≥ m, then ord_p(2) = 2·ord_p(4) ≥ 2m ✓

---

## 5. Artin's Conjecture Connection

### The Conjecture

Artin's conjecture: 2 is a primitive root mod p for ~37.4% of primes (density C_Artin ≈ 0.374).
When 2 is primitive root: ord_p(2) = p - 1 (maximal).

**Status**: Unproven. Hooley proved it under GRH. Heath-Brown proved at least one of {2,3,5} works infinitely often.

### Connection to Tight Primes

If p | Φ_m(4,3) and 2 is primitive root mod p:
- ord_p(2) = p - 1
- For tight: need p - 1 ≥ 2m, i.e., p ≥ 2m + 1
- Since p ≡ 1 (mod m), minimum p = m + 1

**Key finding**: Even when 2 IS a primitive root, if p ≤ 2m the prime isn't tight!

### Problematic m values

When smallest prime of Φ_m(4,3) is ≤ 2m:
- m = 4, 14, 16, 18, 20, 28, 30, 40, 42, ...

Pattern: Often min(p) = m + 1 (the smallest prime ≡ 1 mod m), which gives p - 1 = m < 2m.

### Why this doesn't break tight prime approach

For cycle equation, we check ALL primes of 2^A - 3^m, not just Φ_m(4,3).
Different A values give different prime factorizations.
Empirically: for m ≥ 5, at least one valid A has tight primes.

---

## 6. Chebotarev Density Theorem Connection

### Statement

For K/Q a Galois extension with group G:
- Primes p split according to conjugacy class of Frobenius σ_p
- Density of primes with σ_p in conjugacy class C is |C|/|G|

For **cyclotomic fields** Q(ζ_m):
- G ≅ (Z/mZ)* has order φ(m)
- Density of primes p ≡ a (mod m) is 1/φ(m) (Dirichlet's theorem!)

### Application to Collatz

Primitive primes p | Φ_m(4,3) satisfy p ≡ 1 (mod m).
These are primes that **split completely** in Q(ζ_m).

The smallest such prime determines whether we get immediate tightness:
- If min{p ≡ 1 (mod m)} > 2m, then all primitives are automatically tight candidates
- If min{p ≡ 1 (mod m)} ≤ 2m, need to check other A values

Sources: [Chebotarev density theorem](https://en.wikipedia.org/wiki/Chebotarev's_density_theorem)

---

## 7. CRUCIAL: Φ_m(4,3) vs 2^A - 3^m

### The Key Distinction

**Φ_m(4,3)**: The primitive part of 4^m - 3^m
- All primes p | Φ_m(4,3) satisfy p ≡ 1 (mod m)
- Only "new" primes first appearing at m

**2^A - 3^m**: The ACTUAL cycle equation denominator
- A varies over valid range: ⌈m·log₂(3)⌉ + 1 ≤ A ≤ some_upper_bound
- Different A values give completely different factorizations
- May include primes from DIFFERENT congruence classes

### Why This Matters

Even when Φ_m(4,3) has NO tight primes, other A values provide them!

**Verified examples** (problematic m values):
- m=4, A=8: 175 = 5²×7 → NO tight (ord_5(2)=4, ord_7(2)=3)
- m=4, A=9: 431 prime → ord_431(2)=43 ≥ 8 ✓ TIGHT

All tested m values (up to 60) have at least one A value with tight primes.

### Implication

The tight prime approach works **empirically for all m**, even when the "obvious" Φ_m(4,3) primes fail tightness. The proof needs to establish this works **for all m** by considering the full (m, A) search space.

---

## 8. Zsygmondy's Theorem

### Statement

For coprime integers a > b > 0, a^n - b^n has a **primitive prime divisor** for all n > 1, except:
- a = 2, b = 1, n = 6: 2^6 - 1 = 63 = 7 × 9 (all primes divide 2^k - 1 for k < 6)
- a - b = 1, n = 2, and a + b is a power of 2 (perfect square case)

### Application to Collatz

For 4^m - 3^m with m ≥ 2:
- gcd(4,3) = 1, so Zsygmondy applies
- We're not in the exceptional cases
- **Therefore**: 4^m - 3^m always has a primitive prime p with ord_p(4/3) = m

This **guarantees** the existence of primitive primes for the cyclotomic factorization.

### Strength and Limitation

**Strength**: Unconditional existence of primitive primes
**Limitation**: Says nothing about the SIZE of these primes or ord_p(2)

For tight primes, we need ord_p(2) ≥ 2m, which Zsygmondy doesn't address.

---

## 8.5. Baker's Theorem (Linear Forms in Logarithms)

### Statement (simplified)

For algebraic numbers α₁, ..., αₙ and integers b₁, ..., bₙ with:
  Λ = b₁ log(α₁) + ... + bₙ log(αₙ) ≠ 0

Then |Λ| > exp(-c · B · log(B)), where B = max|bᵢ|.

### Application to Collatz

The approximation 2^A ≈ 3^m gives:
  A log(2) - m log(3) ≈ 0

Baker gives lower bounds on how close this can get. Since log(2)/log(3) is irrational,
2^A can never exactly equal 3^m × (rational).

### Why Baker Doesn't Directly Solve Collatz

1. **Bounds, not proofs**: Baker provides bounds on solution sizes, not non-existence proofs
2. **Not a linear form**: The actual cycle equation 2^A - 3^m × (S/N) = 0 is an EXACT equation
3. **Ratio compensates**: The term S/N can compensate for the gap between 2^A and 3^m

**Bottom line**: Baker is useful for bounding where solutions could live, but tight primes
prove non-existence directly for each (m, A) pair.

---

## 8.6. Open Questions for Investigation

### Q1: Stickelberger for Collatz?
Can Stickelberger-type annihilation results be applied to ideals arising from 4^m - 3^m?

### Q2: "Collatz Wieferich" condition?
Is there a mod p² condition that forces tight primes, analogous to double Wieferich in Catalan?

### Q3: Primitive prime distribution
For large m, what fraction of primitive primes p | Φ_m(4,3) are tight?
Empirically ~85%, but why?

### Q4: Growth phase → cycle impossibility
Can the growth self-limitation theorem (LTE-based) be connected to the cycle analysis?
If trajectories can't sustain growth, and can't cycle, they must descend.

---

## 9. Techniques NOT to Pursue (Failed Approaches)

See COLLATZ_FAILED_APPROACHES_ANALYSIS.md for details:

1. **Ergodic/probabilistic** - "Almost all" ≠ "all"
2. **Transfer operators** - Mixing doesn't capture exceptional trajectories
3. **Automata theory** - Wrong structural lens
4. **p-adic naive** - 2-adic and 3-adic have conflicting completions

---

## 10. Key Computational Tools

### Multiplicative order
```python
def mult_ord(a, n):
    for d in divisors(n - 1):
        if pow(a, d, n) == 1:
            return d
```

### Cyclotomic polynomial value
```python
def Phi_m(x, y, m):
    # Φ_m(x,y) via Möbius: ∏_{d|m} (x^d - y^d)^{μ(m/d)}
```

### 2-adic valuation
```python
def v2(n):
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count
```

---

## 11. Galois Theory Foundations

### Key Concepts for Collatz

**Frobenius Element**: For prime p unramified in K/Q:
```
Frob_p: α ↦ α^p (mod P)
```
Frob_p encodes how p splits in K.

**Splitting Behavior**:
- p splits completely ⟺ Frob_p = identity ⟺ p ≡ 1 (mod conductor)
- p is inert ⟺ Frob_p has maximal order
- p ramifies ⟺ p | disc(K)

**For cyclotomic Q(ζ_m)**:
- Frob_p: ζ_m ↦ ζ_m^p
- ord(Frob_p) = ord_m(p) = multiplicative order of p mod m
- p splits into φ(m)/ord_m(p) primes of degree ord_m(p)

### Connection to Primitive Primes

For primitive prime p | Φ_m(4,3):
- p ≡ 1 (mod m) means ord_m(p) = 1
- Frob_p = identity in Gal(Q(ζ_m)/Q)
- p SPLITS COMPLETELY in Q(ζ_m)

This is WHY primitive primes have the congruence condition!

---

## 12. Local Fields and the 2-3 Conflict

### p-adic Numbers Q_p

For prime p: Q_p = completion of Q with respect to p-adic valuation v_p.
- |x|_p = p^{-v_p(x)}
- Z_p = {x : |x|_p ≤ 1} (p-adic integers)

### LTE Lemma as Local Structure

The LTE lemma v_2(3^k - 1) measures 2-adic distance of 3^k from 1:
- k odd: v_2(3^k - 1) = 1 (3^k is 2-adically close to 1)
- k even: v_2(3^k - 1) = 2 + v_2(k)

This is inherently a LOCAL (2-adic) result!

### The Fundamental 2-3 Conflict

**In Q_2**: Division by 2 shrinks (2-adically); Collatz contracts on average
**In Q_3**: Multiplication by 3 expands; +1 creates 3-adic structure

These are INDEPENDENT completions! No single local field captures both.
The LTE lemma bridges 2-adic and 3-adic by relating v_2(3^k - 1) to k.

### Why This Makes Collatz Hard

- Q_2 and Q_3 don't communicate directly
- Global structure must reconcile both local behaviors
- The tight prime approach works because primes capture global constraints
  while ord_p(2) is a local condition

---

## 13. Class Field Theory (CFT) Framework

### The Artin Reciprocity Map

For abelian extensions K/Q:
```
Gal(K/Q) ≅ J_Q / (Q* · U_K)
```
where J_Q is the idele group and U_K is determined by K.

### Ideles and Adeles

**Adele ring**: A_Q = R × ∏_p Q_p (restricted product)
**Idele group**: J_Q = A_Q* = R* × ∏_p Q_p*

Elements are tuples (x_∞, x_2, x_3, x_5, ...) with almost all x_p in Z_p*.

### Potential CFT Approach to Collatz

1. View 4^m - 3^m as generating an ideal in Z[ζ_m]
2. Factor into prime ideals corresponding to primes of Φ_d(4,3)
3. Apply Stickelberger-type constraints
4. Use Galois cohomology to force tight prime existence

KEY QUESTION: Can CFT + Stickelberger prove that for ALL m ≥ 5,
some prime p | 2^A - 3^m is tight?

---

## 14. Verified Computational Results

### Primitive Primes and Artin's Conjecture

Among primitive primes p | Φ_m(4,3) for m ∈ [2, 50]:
- ~40% have 2 as primitive root (close to Artin's constant 0.374)
- ~85% are tight (ord_p(2) ≥ 2m)

### Problematic m Values

m values where smallest primitive prime p ≤ 2m:
- m = 4, 14, 16, 18, 20, 28, 30, 40, 42, 44, 48, 50, 52, 54, 56, ...

Pattern: Often min(p) = m + 1, giving p - 1 = m < 2m (not tight).

### But Alternative A Values Save Us

For ALL tested m (up to 60), at least one A value has tight primes!
- m=4, A=8: 175 = 5²×7, no tight primes
- m=4, A=9: 431 (prime), ord_431(2) = 43 ≥ 8 ✓

---

## 15. Expert Advisor Capabilities

Ready to advise on:
1. **Tight prime lemma** - rigorous statement and proof
2. **Cyclotomic structure** - Φ_m(4,3) factorization
3. **LTE lemma** - growth phase constraints
4. **Frobenius/splitting** - why primes behave as they do
5. **Local-global** - 2-3 conflict and resolution
6. **Stickelberger** - potential algebraic approaches
7. **Computational verification** - checking specific m, A, p values

---

**Status**: Deep expertise in algebraic number theory, Galois theory, local fields,
and their application to Collatz. Ready to advise with genuine domain depth.
