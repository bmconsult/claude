# P-adic Transcendence Theory: Complete Development

## The P-adic Analogue of Baker's Theorem

---

## Part I: Foundations

### 1.1 The P-adic Numbers

**Definition:** For prime p, the p-adic absolute value on ℚ is:
$$|x|_p = p^{-\text{ord}_p(x)}$$

where ord_p(x) is the exponent of p in the prime factorization of x.

**Completion:** ℚ_p is the completion of ℚ with respect to |·|_p.

**Properties:**
- Strong triangle inequality: |x + y|_p ≤ max(|x|_p, |y|_p)
- Totally disconnected, locally compact
- Contains ℤ_p = {x ∈ ℚ_p : |x|_p ≤ 1}

**Algebraic closure:** ℂ_p is the completion of the algebraic closure of ℚ_p.

### 1.2 The P-adic Logarithm

**Definition:** For x ∈ ℂ_p with |x - 1|_p < 1:
$$\log_p(x) = \sum_{n=1}^{\infty} \frac{(-1)^{n+1}(x-1)^n}{n}$$

**Convergence:** The series converges when |x - 1|_p < 1.

**More generally:** For |x - 1|_p < p^{-1/(p-1)}, we have stronger convergence.

**Extension:** For x ∈ ℂ_p^×, write x = ζ · y · p^k where:
- ζ is a root of unity
- |y - 1|_p < p^{-1/(p-1)}
- k ∈ ℤ

Then log_p(x) = log_p(y) (roots of unity and p^k contribute 0).

### 1.3 The P-adic Exponential

**Definition:** 
$$\exp_p(x) = \sum_{n=0}^{\infty} \frac{x^n}{n!}$$

**Convergence:** Converges when |x|_p < p^{-1/(p-1)}.

**Note:** This radius is SMALLER than the domain of log_p!

**Key difference from complex case:**
- In ℂ: exp is entire, log is multi-valued
- In ℂ_p: exp has limited convergence, log is single-valued

---

## Part II: P-adic Baker's Theorem

### 2.1 The Main Result

**Theorem (Yu 1990, building on Brumer 1967):** Let p be a prime and let α₁, ..., αₙ ∈ ℂ_p be nonzero algebraic numbers such that log_p(α₁), ..., log_p(αₙ) are well-defined and linearly independent over ℚ.

Then log_p(α₁), ..., log_p(αₙ) are linearly independent over the algebraic numbers.

### 2.2 Quantitative Version

**Theorem (Yu 1990):** Let K be a number field of degree d, let 𝔭 be a prime ideal above p with ramification index e_𝔭 and residue degree f_𝔭.

Let α₁, ..., αₙ ∈ K^× with log heights h₁, ..., hₙ where:
$$h_j \geq \max\left(h(\alpha_j), \frac{\log p}{d}\right)$$

Let b₁, ..., bₙ ∈ ℤ with B = max|b_j|.

If Λ = α₁^{b₁} ⋯ αₙ^{bₙ} ≠ 1, then:
$$\text{ord}_𝔭(\Λ - 1) \leq C(n,p) \cdot d^{n+2} \cdot h₁ ⋯ hₙ \cdot \log B$$

where C(n,p) is an explicit constant.

### 2.3 The Explicit Constant

**Best known (Yu 1998-2007):**
$$C(n,p) = c^n \cdot n^{2n} \cdot p^{f_𝔭} \cdot \left(\frac{e_𝔭}{f_𝔭}\right)^n$$

where c is an absolute constant ≈ 20.

**Comparison with archimedean case:**
- Archimedean (Baker-Wüstholz): C(n) ≈ 18^n · n^{2n}
- P-adic (Yu): similar but with p^{f_𝔭} factor

### 2.4 History and Development

1. **Brumer (1967):** Linear independence (qualitative)
   - Connection to Leopoldt's conjecture
   - Used group cohomology

2. **van der Poorten (1977):** First quantitative attempts
   - Had technical issues with p-adic analysis

3. **Yu (1989-2007):** Complete p-adic theory
   - Series of papers resolving all issues
   - Introduced "supernormality" concept
   - Extended to group varieties

---

## Part III: Proof Structure

### 3.1 Key Difficulties in P-adic Setting

**Problem 1: Limited exponential convergence**
- In ℂ: exp is entire, use exp(2πi) = 1
- In ℂ_p: exp_p converges only on small disk

**Solution:** Work directly with logarithms, use p-adic interpolation.

**Problem 2: No periodicity**
- In ℂ: log α defined mod 2πi
- In ℂ_p: log_p is single-valued on its domain

**Solution:** Different auxiliary construction, based on Mahler expansions.

**Problem 3: Kummer theory issues**
- Extracting p-th roots in ℂ_p is subtle
- "Descent" step needs modification

**Solution:** Yu's supernormality concept.

### 3.2 Outline of Yu's Proof

**Step 1: Setup**
- K = ℚ(α₁, ..., αₙ)
- 𝔭 prime above p
- Assume ord_𝔭(Λ - 1) is large (for contradiction)

**Step 2: Auxiliary function**
- Construct polynomial P(X₁, ..., Xₙ) with:
  - Small height
  - Vanishes to high order at (log_p α₁, ..., log_p αₙ)

**Step 3: Interpolation**
- Use Mahler interpolation series in ℂ_p
- Different from Taylor series in complex case

**Step 4: Multiplicity estimate**
- P-adic version of Wüstholz's estimate
- Control vanishing at translated points

**Step 5: Descent**
- Using supernormality
- Reduce to lower dimensional case

**Step 6: Contradiction**
- Compare p-adic and archimedean bounds
- Get contradiction if ord_𝔭(Λ - 1) too large

### 3.3 The Supernormality Condition

**Definition:** An algebraic number α is supernormal for p if:
$$|\sigma(\alpha)|_v \leq 1 \text{ for all } v | p, \sigma \in \text{Gal}(\bar{K}/K)$$

**Why this matters:** In descent, we need all conjugates to have controlled p-adic behavior.

**Lemma (Yu):** Can always reduce to supernormal case by finite extraction.

---

## Part IV: Extension to Group Varieties

### 4.1 P-adic Logarithmic Forms on Abelian Varieties

**Setting:**
- A: abelian variety over number field K
- 𝔭: prime of K above p
- A has good reduction at 𝔭

**P-adic exponential map:**
$$\exp_{A,p}: T_p(A) \to A(ℂ_p)$$

where T_p(A) is the p-adic tangent space.

**P-adic periods:** The kernel of exp_{A,p} gives p-adic periods.

### 4.2 Yu's Extension

**Theorem (Yu 1998, 1999, 2007):** Let A be an abelian variety of dimension g over K. Let u ∈ Lie(A)(ℂ_p) with exp_{A,p}(u) ∈ A(K).

Then there exists an abelian subvariety B ⊂ A with:
1. u ∈ Lie(B)(ℂ_p)
2. deg(B) bounded in terms of h(A), [K:ℚ], p

### 4.3 The Main Estimate

**Theorem:** With notation as above:
$$\text{ord}_𝔭(u) \leq C(g,p) \cdot d^{c(g)} \cdot h(A)^{\kappa(g)} \cdot h(u)$$

where:
- d = [K : ℚ]
- h(A) = Faltings height
- h(u) = height of algebraic point exp_{A,p}(u)
- κ(g) = 2g² (same as archimedean case!)

---

## Part V: Applications

### 5.1 Leopoldt's Conjecture

**Conjecture (Leopoldt 1962):** For number field K and prime p:
$$\text{rank}_{\mathbb{Z}_p}(\overline{E_K}) = r_1 + r_2 - 1$$

where:
- E_K = unit group of K
- $\overline{E_K}$ = closure in ∏_{𝔭|p} K_𝔭^×
- r_1, r_2 = real, complex embeddings

**Connection to p-adic Baker:**

If Leopoldt fails, there exist units ε₁, ..., εᵣ with:
$$\log_p(\sigma(ε_1))^{b_1} + ... = 0$$

for some non-trivial relation. P-adic Baker rules this out for n = 2.

**Status:** 
- True for abelian extensions (Brumer 1967)
- Open in general

### 5.2 P-adic ABC Conjecture

**Application (Stewart-Yu):** The abc conjecture implies:
$$\log \max(|a|, |b|, |c|) \ll_\epsilon \text{rad}(abc)^{1+\epsilon}$$

P-adic logarithmic forms give effective bounds for:
$$\text{ord}_p(a^m - b^n)$$

### 5.3 Catalan's Conjecture (Now Theorem)

**Mihailescu (2004):** The only solution to x^p - y^q = 1 in integers > 1 is 3² - 2³ = 1.

**Key step:** P-adic analysis using Yu's bounds.

### 5.4 Greatest Prime Factor of 2ⁿ - 1

**Theorem (Stewart, using Yu's refinements):**
$$P(2^n - 1) \to \infty \text{ as } n \to \infty$$

where P(m) = greatest prime factor.

In fact: P(2^n - 1) > n · log₂(n) · (log₂ log n)^{1-ε} for large n.

---

## Part VI: Comparison: Archimedean vs P-adic

### 6.1 Parallel Structure

| Aspect | Archimedean | P-adic |
|--------|-------------|--------|
| Base field | ℂ | ℂ_p |
| Logarithm | Multi-valued | Single-valued |
| Exponential | Entire | Limited convergence |
| Key estimate | \|Λ - 1\| > exp(-C·...) | ord_𝔭(Λ - 1) < C·... |
| Multiplicity | Wüstholz 1989 | Yu 1998 |
| Group varieties | Baker-Wüstholz 1993 | Yu 1998-2007 |

### 6.2 The Unified Viewpoint

Both theories fit into:

**General transcendence framework:**
1. Auxiliary construction (Siegel's lemma)
2. Extrapolation (propagate zeros)
3. Multiplicity estimates (bound subgroup degrees)
4. Height comparison (Arakelov/p-adic)
5. Contradiction

**The multiplicity estimate is the same:**
- Same algebraic statement about sections of line bundles
- Different analytic implementation

### 6.3 What's Special About P-adic

1. **No periodicity:** log_p is well-defined, not mod anything

2. **Stronger ultrametric:** |x + y|_p ≤ max(|x|_p, |y|_p) with equality if |x|_p ≠ |y|_p

3. **Newton polygons:** More refined divisibility analysis

4. **Connection to Iwasawa theory:** p-adic L-functions, cyclotomic towers

---

## Part VII: Open Problems

### 7.1 Algebraic Independence

**Open:** Are p-adic logarithms of algebraically independent numbers themselves algebraically independent?

(Analogue of Schanuel's conjecture)

### 7.2 Leopoldt for All Fields

**Open:** Leopoldt's conjecture for non-abelian extensions.

### 7.3 Uniform Bounds

**Question:** Can constants be made uniform in p?

Current bounds have p^{f_𝔭} factor.

### 7.4 Higher Dimensional Extensions

**Open:** Full p-adic period theory for varieties beyond abelian varieties.

---

## Part VIII: Computational Aspects

### 8.1 The P-adic Numbers in Practice

```
For p = 5, computing log_5(2):
2 = 1 + 1 ≡ 2 (mod 5)
log_5(2) = log_5(1 + 1) = 1 - 1/2 + 1/3 - 1/4 + ...

But |1|_5 = 1, so series doesn't converge directly!

Instead: Write 2 = 2·5^0, find y with 2 = y·5^k where |y-1|_5 < 5^{-1/4}
This requires Hensel lifting...
```

### 8.2 Computing P-adic Logarithms

**Algorithm:**
1. Find k = ord_p(α)
2. Let β = α/p^k
3. Find root of unity ζ with ζ^{-1}β close to 1
4. Compute log_p(ζ^{-1}β) by series
5. log_p(α) = log_p(ζ^{-1}β)

### 8.3 Bounds in Practice

**For ord_𝔭(α^b - 1) with α algebraic:**

Typical bound: ord_𝔭(α^b - 1) < C·d²·h(α)·log(b)

where C ≈ 10^6 in current best results.

---

## Summary

The p-adic theory of logarithmic forms, developed primarily by Kunrui Yu building on earlier work of Brumer and van der Poorten, provides:

1. **Qualitative results:** Linear independence of p-adic logarithms
2. **Quantitative bounds:** Explicit lower bounds for linear forms
3. **Group variety extensions:** Period bounds for abelian varieties
4. **Applications:** Leopoldt conjecture (partial), Catalan's conjecture, greatest prime factors

The theory parallels the archimedean (complex) theory but with distinct technical challenges arising from:
- Limited convergence of p-adic exponential
- Different behavior of p-adic absolute value
- Connection to arithmetic of number fields at p

**Current frontier:** Extending to algebraic independence, uniform bounds in p, and connections to p-adic Hodge theory.
