# Explicit Constants in Transcendence Theory: Modern Improvements

## Gaudron-Rémond and Beyond

---

## Part I: Historical Evolution of Constants

### 1.1 Timeline of Isogeny Bounds

**1993 - Baker-Wüstholz:** First effective isogeny theorem
- deg(φ) ≤ exp(c · g^{10g} · d^{2g+4} · max(1, h_F(A))^{2g+2})
- Constants huge and not computed explicitly

**2006 - Gaudron-Rémond (Théorème des périodes):** Major improvement
- deg(B) ≤ c(g) · d^{κ(g)} · max(1, h_F(A))^{κ(g)}
- κ(g) = 2g² (optimal exponent!)
- First explicit constants

**2014 - Gaudron-Rémond (Polarisations et isogénies):**
- Sharpened all constants
- Extended to polarized case
- Best currently known bounds

### 1.2 The Key Constants

**For elliptic curves (g = 1):**

| Year | Author | Isogeny degree bound |
|------|--------|----------------------|
| 1990 | Masser-Wüstholz | exp(c · d^4 · h²) |
| 2001 | Pellarin | exp(c · d² · h²) |
| 2011 | Gaudron-Rémond | c · d^4 · h² |

**The dramatic improvement:** From exponential to polynomial!

**Explicit Gaudron-Rémond bound (g=1):**
$$\deg(\phi) \leq 10^{6} \cdot d^4 \cdot \max(1, h_F(E))^2$$

### 1.3 Higher Dimensional Cases

**Gaudron-Rémond (2014) for dimension g:**

$$\deg(\phi) \leq c(g) \cdot d^{4g(g+1)} \cdot \max(1, h_F(A))^{2g^2}$$

where:
- c(g) is explicitly computable
- d = [K : ℚ] is the field degree
- h_F(A) is the Faltings height

**Explicit values of c(g):**
- c(1) ≈ 10^6
- c(2) ≈ 10^{20}
- c(3) ≈ 10^{50}

---

## Part II: The Period Theorem Constants

### 2.1 Statement with Explicit Constants

**Theorem (Gaudron-Rémond 2006):** Let A be an abelian variety of dimension g over number field K with [K:ℚ] = d. Let ω be a period of A and B the smallest abelian subvariety with ω ∈ Lie(B).

Then:
$$\deg(B) \leq c_1(g) \cdot c_2(g)^d \cdot \max(1, h_F(A))^{κ(g)}$$

where:
- κ(g) = 2g²
- c₁(g) and c₂(g) are explicit constants

### 2.2 The Explicit Constants

**From Gaudron-Rémond 2014:**

For g = 1:
- c₁(1) = 10^5
- c₂(1) = 1000
- κ(1) = 2

For g = 2:
- c₁(2) = 10^{18}
- c₂(2) = 10^6
- κ(2) = 8

**General formula (approximate):**
- c₁(g) ≈ (10g)^{g²}
- c₂(g) ≈ g^{g}
- κ(g) = 2g²

### 2.3 Comparison with Earlier Work

**Masser-Wüstholz 1993:**
- Existential: deg(B) ≤ f(g,d,h) for some function f
- No explicit form

**Baker-Wüstholz 1993:**
- κ(g) = 2g+2 (not optimal!)
- Constants not explicit

**Why κ(g) = 2g² is optimal:**
- Comes from multiplicity estimate exponent
- Lower bound examples show this is sharp

---

## Part III: The Multiplicity Estimate Constants

### 3.1 The Wüstholz Estimate (1989)

**Original form:** For abelian variety A of dimension g, section F ∈ H⁰(A, L^D) vanishing to order T at origin:

$$T^{\dim B} \leq c(g) \cdot D^{\dim B} \cdot \deg(B)$$

for some abelian subvariety B containing supp(F).

**The constant c(g):** Wüstholz proved c(g) exists but didn't compute it.

### 3.2 Modern Explicit Versions

**Philippon-style bound:**

For G_m^n:
$$c(n) = 2^{n(n+1)/2} \cdot n! \cdot \prod_{j=1}^n j!$$

**Values:**
- c(1) = 2
- c(2) = 16
- c(3) = 384
- c(4) = 24576

**For abelian varieties:**

The constant involves:
- Theta function normalization
- Polarization degree
- Dimension-dependent factors

Explicit: c(g) ≤ (2g)^{g²} · g!

### 3.3 The Zero Estimate Refinement

**Philippon's explicit zero estimate (1986):**

For polynomial P of degree D on G_m^n, vanishing set Z:
$$|Z| \leq D^n$$

unless Z contains a translate of an algebraic subgroup.

**With subgroup obstruction:**
$$|Z \cap (a + H)| \leq \frac{D^n}{\deg(H)}$$

These are the building blocks for all explicit constants.

---

## Part IV: Applications of Explicit Bounds

### 4.1 Rational Points on Modular Curves

**Theorem (Bilu-Parent-Rebolledo 2011, using Gaudron-Rémond):**

For p > 2 · 10^{11} and r > 1:
$$X_0^+(p^r)(ℚ) = \emptyset$$

**Method:** 
1. Relate rational points to isogenies
2. Apply Gaudron-Rémond bounds
3. Get contradiction for large p

### 4.2 Effective Mordell

**Application:** Height bounds for rational points on curves.

If C has genus g ≥ 2, Jacobian J, then for P ∈ C(K):
$$h(P) \leq c(g,K) \cdot \max(1, h_F(J))^{poly(g)}$$

The Gaudron-Rémond constants make this explicit.

### 4.3 S-Unit Equations

**Classical application:** ax + by = 1 with x, y S-units.

**Explicit bound:**
$$\max(|x|, |y|) \leq \exp(c \cdot |S|^{O(1)} \cdot h^{O(1)})$$

where h involves heights of a, b.

---

## Part V: The Real Place Improvement

### 5.1 The Phenomenon

**Gaudron-Rémond observation:** When K has a real embedding, constants improve!

For elliptic curves over K with K ⊂ ℝ:
- Isogeny bound improves by factor ~100
- Period bound improves significantly

### 5.2 Why This Happens

**Technical reason:** The auxiliary construction uses:
1. Real analytic estimates (when K ⊂ ℝ)
2. Complex estimates (general case)

Real estimates are tighter because:
- No phase factors to track
- Simpler error analysis

### 5.3 Explicit Comparison

For E over K with [K:ℚ] = d:

**K has real place:**
$$\deg(\phi) \leq 10^5 \cdot d^3 \cdot h^2$$

**K totally complex:**
$$\deg(\phi) \leq 10^6 \cdot d^4 \cdot h^2$$

---

## Part VI: Current Best Known Constants

### 6.1 Summary Table

| Dimension | κ(g) | c₁(g) | c₂(g) | Source |
|-----------|------|-------|-------|--------|
| 1 | 2 | 10^5 | 10^3 | G-R 2014 |
| 2 | 8 | 10^{18} | 10^6 | G-R 2014 |
| 3 | 18 | 10^{40} | 10^{12} | G-R 2014 |
| g | 2g² | ~(10g)^{g²} | ~g^g | G-R 2014 |

### 6.2 The Baker-Wüstholz Linear Forms Constant

For linear form Λ = b₀ + b₁ log α₁ + ... + bₙ log αₙ:

$$|Λ| > \exp(-c(n) \cdot d^{n+2} \cdot h_1 \cdots h_n \cdot \log B)$$

**Best known c(n):** 
- c(n) = 2^{4n+16} · n^{2n+4} (Matveev 2000)
- For n = 2: c(2) ≈ 10^{12}

### 6.3 Room for Improvement

**Known limitations:**
1. κ(g) = 2g² is optimal (lower bound examples exist)
2. Field degree exponent 4g(g+1) may not be optimal
3. Constant c₁(g) is far from tight

**Conjectured improvements:**
- Field degree exponent: should be ~g²
- Constant: should be ~g^{g}

---

## Part VII: Computational Verification

### 7.1 Testing the Bounds

For elliptic curve E over ℚ with conductor N:
- h_F(E) ≈ (1/12) log N
- Isogeny degree bound: ~10^6 · h_F(E)²

**Example: E = y² = x³ - x (conductor 32):**
- h_F(E) ≈ 0.29
- Bound predicts: deg(φ) ≤ 10^6 · 0.08 ≈ 80,000
- Actual maximum isogeny degree: 2
- Bound is very loose but effective!

### 7.2 The Looseness Issue

**Why bounds are so loose:**
1. Universal constants must work for ALL abelian varieties
2. Worst cases are very special (CM, high degree fields)
3. Generic cases are much better behaved

**For CM elliptic curves:** Bounds are nearly tight
**For non-CM:** Bounds off by factors of 10^3 or more

### 7.3 Probabilistic Improvements

**Heuristic (Masser):** For "random" E over ℚ:
$$\deg(\phi) \leq c \cdot h_F(E)^{1+\epsilon}$$

vs. proven bound with exponent 2.

This suggests room for improvement via understanding "typical" behavior.

---

## Part VIII: Future Directions

### 8.1 Tighter Field Degree Dependence

**Current:** d^{4g(g+1)}
**Conjectured:** d^{2g²}

Reducing this would have major applications to:
- Points on modular curves
- Effective Shafarevich conjecture

### 8.2 Uniform Bounds Across Families

**Question:** Can we get bounds uniform in certain families?

For modular abelian varieties A_f attached to newform f:
- Height varies with conductor
- Can we bound isogenies in terms of conductor alone?

### 8.3 Computational Approaches

**Modern methods:**
1. Interval arithmetic for rigorous numerics
2. Certified computation with error bounds
3. Database of small cases (LMFDB)

These help verify and improve theoretical bounds.

---

## Summary

The development from Baker-Wüstholz (1993) to Gaudron-Rémond (2014) represents:

1. **Optimal exponents:** κ(g) = 2g² achieved
2. **Explicit constants:** All bounds now computable
3. **Polynomial vs exponential:** Dramatic improvement
4. **New applications:** Modular curves, S-unit equations

**Current frontier:**
- Tighter field degree dependence
- Understanding generic vs worst-case
- Connections to p-adic theory

The explicit nature of modern bounds transforms transcendence theory from existence statements to computable mathematics.
