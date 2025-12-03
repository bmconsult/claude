# Grand Conjectures in Transcendence Theory

## From Baker to Periods to Motives

---

## Part I: The Hierarchy of Conjectures

### 1.1 Overview: The Landscape

Transcendence theory contains a hierarchy of conjectures of increasing strength and generality:

```
GROTHENDIECK PERIOD CONJECTURE (motives)
           ↓ implies
SCHANUEL'S CONJECTURE (exponential function)
           ↓ implies
FOUR EXPONENTIALS CONJECTURE
           ↓ implies
SIX EXPONENTIALS THEOREM (proved)
           ↓ consequence
BAKER'S THEOREM (proved)
```

In parallel, for abelian varieties:

```
ANDRÉ PERIOD CONJECTURE (abelian varieties)
           ↓ implies
ABELIAN SCHANUEL CONJECTURE
           ↓ implies
ELLIPTIC FOUR EXPONENTIALS
           ↓ consequence
WÜSTHOLZ ANALYTIC SUBGROUP (proved)
```

### 1.2 The Unifying Theme

All these conjectures concern:
**"Algebraic relations among transcendental values arise only from geometry"**

In other words: If exp(x₁), ..., exp(xₙ) satisfy a polynomial relation, there's an algebraic reason (linear dependence of the xᵢ).

---

## Part II: Schanuel's Conjecture

### 2.1 Statement

**Conjecture (Schanuel, ~1960):** Let z₁, ..., zₙ ∈ ℂ be linearly independent over ℚ. Then:

$$\text{tr.deg}_ℚ\, ℚ(z_1, \ldots, z_n, e^{z_1}, \ldots, e^{z_n}) \geq n$$

**Translation:** Among the 2n numbers z₁, ..., zₙ, e^{z₁}, ..., e^{zₙ}, at least n are algebraically independent over ℚ.

### 2.2 Known Special Cases

| Case | Statement | Status |
|------|-----------|--------|
| n=1, z₁=1 | e is transcendental | Hermite 1873 |
| n=1, z₁=πi | π is transcendental | Lindemann 1882 |
| z₁,...,zₙ algebraic | e^{z₁},...,e^{zₙ} alg. indep. | Lindemann-Weierstrass 1885 |
| β₁log α₁+...+βₙlog αₙ=0 | Linear dependence over ℚ̄ | Baker 1966 |

### 2.3 Unknown Cases

**Still open after 60+ years:**
- Are e and π algebraically independent?
- Is e + π transcendental?
- Is eᵖ transcendental? (Not even e^{π²} is known!)
- Is π^e transcendental?

### 2.4 Consequences

If Schanuel's conjecture is true:
1. e and π are algebraically independent
2. e^e, e^π, π^e, π^π are all transcendental
3. log π and log log 2 are transcendental
4. The constant problem for exp is decidable (Macintyre-Wilkie)

---

## Part III: The Four Exponentials Conjecture

### 3.1 Statement

**Conjecture (Schneider 1957, Lang-Ramachandra 1960s):**

Let x₁, x₂ and y₁, y₂ be two pairs of complex numbers, each pair linearly independent over ℚ. Then at least one of:

$$e^{x_1 y_1}, \quad e^{x_1 y_2}, \quad e^{x_2 y_1}, \quad e^{x_2 y_2}$$

is transcendental.

### 3.2 Matrix Formulation

Equivalently: If the 2×2 matrix of logarithms:

$$\begin{pmatrix} \lambda_{11} & \lambda_{12} \\ \lambda_{21} & \lambda_{22} \end{pmatrix}$$

has algebraic entries e^{λᵢⱼ}, and rows/columns are ℚ-linearly independent, then the matrix has rank ≤ 1 over ℚ̄.

### 3.3 The Six Exponentials Theorem

**Theorem (Siegel-Schneider-Lang-Ramachandra):**

Let x₁, x₂ and y₁, y₂, y₃ be complex numbers with {x₁, x₂} and {y₁, y₂, y₃} each ℚ-linearly independent. Then at least one of:

$$e^{x_1 y_1}, e^{x_1 y_2}, e^{x_1 y_3}, e^{x_2 y_1}, e^{x_2 y_2}, e^{x_2 y_3}$$

is transcendental.

**Why "just misses" four:** The proof uses dimension counting that works for 2×3 but fails for 2×2.

### 3.4 The Strong Versions

**Strong Four Exponentials Conjecture:** Same statement but with "transcendental" replaced by "not in L*" where:

$$L^* = \text{span}_{\bar{ℚ}}\{1, \log α : α \in \bar{ℚ}^×\}$$

This rules out not just algebraic values but all ℚ̄-linear combinations of logarithms.

---

## Part IV: Abelian Analogues

### 4.1 The Abelian Schanuel Conjecture

**Conjecture (Bertolin, André, Philippon et al.):**

Let A be an abelian variety of dimension g over ℚ̄, and let u₁, ..., uₙ ∈ Lie(A) be linearly independent over End(A)⊗ℚ. Let Pᵢ = exp_A(uᵢ).

Then:
$$\text{tr.deg}_ℚ\, ℚ(u_1, \ldots, u_n, P_1, \ldots, P_n) \geq n$$

### 4.2 Connection to 1-Motives

**Key insight (Bertolin 2002):** Schanuel's conjecture is equivalent to André's Generalized Period Conjecture for 1-motives without abelian part.

The abelian Schanuel conjecture is similarly equivalent to the GPC for 1-motives without toric part.

### 4.3 What Is Known

**Wüstholz Analytic Subgroup Theorem:** The qualitative version is proved!

If u ∈ Lie(A) with exp_A(u) algebraic, then u lies in Lie(B) for some abelian subvariety B.

**What's missing:** Algebraic independence (not just linear independence).

### 4.4 The Semi-Abelian Extension

For G = G_m^r × A (extension of abelian variety by torus):

**Semi-Abelian Schanuel Conjecture:** Combines classical Schanuel with abelian Schanuel.

This is the natural setting for periods of mixed motives.

---

## Part V: The André-Oort Conjecture (Now a Theorem)

### 5.1 Statement

**Theorem (Pila-Shankar-Tsimerman 2021):**

Let S be a Shimura variety and let Σ ⊂ S be a set of special points. Then every irreducible component of the Zariski closure of Σ is a special subvariety.

### 5.2 Special Cases

**For A_g (moduli of abelian varieties):**
- Special points = CM abelian varieties
- Special subvarieties = Shimura subvarieties

**For products of modular curves:**
- Special points = pairs of CM elliptic curves
- Proved unconditionally by Pila 2009

### 5.3 The Proof Strategy (Pila-Zannier)

1. **O-minimal geometry:** Count rational points on transcendental varieties
2. **Ax-Lindemann:** Functional transcendence for period maps
3. **Height bounds:** Control heights of special points
4. **Galois bounds:** Lower bounds on Galois orbits (uses isogeny estimates!)

### 5.4 Connection to Our Work

**Key input:** Masser-Wüstholz isogeny estimates!

Tsimerman (2015) used isogeny bounds to prove Galois orbit lower bounds for A_g, completing André-Oort for Siegel modular varieties.

---

## Part VI: Grothendieck's Period Conjecture

### 6.1 The Mumford-Tate Group

For abelian variety A over ℚ̄:
- Hodge structure H¹(A,ℚ)
- Mumford-Tate group MT(A) ⊂ GL(H¹)
- This is the "motivic Galois group" of A

### 6.2 The Conjecture

**Conjecture (Grothendieck ~1966):**

$$\text{tr.deg}_ℚ\, (\text{periods of } A) = \dim MT(A)$$

**What's known:**
- Upper bound: tr.deg ≤ dim MT(A) (Deligne)
- Lower bound: the conjecture!

### 6.3 The Generalized Period Conjecture (André)

For any smooth projective variety X over ℚ̄:

$$\text{tr.deg}_ℚ\, \text{Per}(X) = \dim G_{mot}(X)$$

where G_{mot} is the motivic Galois group.

**This implies everything:**
- Schanuel's conjecture (for G_m)
- Abelian Schanuel (for abelian varieties)
- All period conjectures

---

## Part VII: The Kontsevich-Zagier Program

### 7.1 What is a Period?

**Definition (Kontsevich-Zagier 2001):**

A period is a complex number of the form:
$$\int_\sigma \omega$$

where:
- σ is a semi-algebraic set in ℝⁿ defined over ℚ̄
- ω is an algebraic differential form over ℚ̄

### 7.2 Examples

- π = ∫_{x²+y²≤1} dx dy
- log 2 = ∫_1^2 dx/x
- ζ(3) = ∫∫∫_{0<x<y<z<1} dx dy dz / (xyz)
- Periods of elliptic curves

### 7.3 The Period Conjecture

**Conjecture:** All polynomial relations between periods arise from:
1. Algebraic relations between defining data
2. Stokes' theorem (d(ω) and ∂σ relations)
3. Change of variables

**Status:** Largely open, but motivates much current research.

---

## Part VIII: Connections and Implications

### 8.1 The Full Picture

```
MOTIVIC GALOIS GROUP (Grothendieck-André)
              ↓
    PERIOD CONJECTURE
         /          \
SCHANUEL         ABELIAN SCHANUEL
    |                    |
FOUR EXP             ELLIPTIC ANALOGUE
    |                    |
SIX EXP            WÜSTHOLZ THEOREM
    |                    |
BAKER              PERIOD THEOREM
```

### 8.2 What's Proved vs Conjectured

**PROVED:**
- Six exponentials theorem
- Baker's theorem (linear forms in logs)
- Wüstholz analytic subgroup theorem
- Masser-Wüstholz period theorem
- André-Oort conjecture (2021)
- Lindemann-Weierstrass

**CONJECTURED (widely believed):**
- Four exponentials
- Schanuel
- Grothendieck period conjecture

**CONJECTURED (very hard):**
- Algebraic independence of e and π
- Full motivic conjecture

### 8.3 Why These Conjectures Are Hard

1. **Lack of structure:** No group action to exploit for four exp
2. **No induction:** Can't reduce to lower dimensional cases
3. **No approximation:** Transcendence degree is discrete
4. **Deep geometry:** Requires understanding motivic Galois groups

---

## Part IX: The Role of Our Work

### 9.1 What We've Contributed

This research program has:
1. Proved foundational results (zero estimates, theta theory)
2. Understood proof structure of period theorem
3. Tracked explicit constants (Gaudron-Rémond)
4. Connected archimedean and p-adic theories

### 9.2 Connection to Big Conjectures

Our work on the period theorem is:
- The **proved part** of abelian Schanuel (linear relations)
- A **key input** to André-Oort (isogeny bounds)
- The **prototype** for motivic period bounds

### 9.3 What Would Be Needed

To prove four exponentials:
- New technique beyond current multiplicity estimates
- Possibly: model theory (Zilber's approach)
- Possibly: motivic methods

To prove Schanuel:
- Would require proving tr.deg ≥ n, not just linear independence
- No known approach

---

## Part X: Current Research Frontiers

### 10.1 Zilber's Program

**Pseudo-exponentiation:** Zilber constructed "exponential fields" K_exp satisfying:
- Schanuel's conjecture (by fiat)
- Exponential-algebraic closedness
- Categoricity

**Key question:** Is K_exp ≅ ℂ_exp?

If yes → Schanuel's conjecture is true!

### 10.2 O-Minimality and Counting

**Pila-Wilkie:** Transcendental varieties have few rational points.

Applications:
- André-Oort (completed)
- Manin-Mumford
- Zilber-Pink conjectures

### 10.3 Motivic Periods

**Current work:** Understanding G_{mot} for:
- Mixed Tate motives
- Feynman integrals (physics!)
- Multiple zeta values

### 10.4 Effectivity

**Open problem:** Make André-Oort effective.

Currently: proof is non-effective (uses GRH in some cases, non-constructive bounds in others).

---

## Summary

The grand conjectures of transcendence theory form a coherent program:

1. **Philosophy:** "All relations come from geometry"
2. **Proved cases:** Linear relations (Baker, Wüstholz)
3. **Open cases:** Algebraic independence (Schanuel, four exp)
4. **Ultimate goal:** Grothendieck-André period conjecture

Our work on the period theorem represents the state of the art for what can be proved, while the bigger conjectures remain among the deepest open problems in mathematics.

**Key insight:** The techniques that work (Siegel's lemma, multiplicity estimates, height bounds) all exploit LINEAR structure. Proving algebraic independence requires fundamentally new ideas.
