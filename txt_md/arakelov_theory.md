# Arakelov Intersection Theory: From Foundations to Applications

## Part 1: Motivation and Overview

### 1.1 The Compactification Problem

**Classical Setup:** For a smooth projective variety $X$ over $\mathbb{C}$:
- Intersection theory gives intersection numbers of divisors
- These are integers

**Arithmetic Setup:** For a variety $X$ over a number field $K$:
- The scheme $\text{Spec}(\mathcal{O}_K)$ is like a curve
- But it's not "compact" - missing the archimedean places

**Arakelov's Idea:** Complete $\text{Spec}(\mathcal{O}_K)$ by adding "fibers at infinity" (archimedean places), use hermitian metrics to handle these contributions.

### 1.2 Key Players

| Classical (over $\mathbb{C}$) | Arithmetic (over $\mathcal{O}_K$) |
|-------------------------------|-----------------------------------|
| Variety $X$ | Arithmetic variety $\mathcal{X} \to \text{Spec}(\mathcal{O}_K)$ |
| Line bundle $L$ | Hermitian line bundle $\bar{L}$ |
| Divisor $D$ | Arakelov divisor $\hat{D}$ |
| Degree | Arithmetic degree |
| Intersection number | Arithmetic intersection number |

---

## Part 2: Basic Definitions

### 2.1 Arithmetic Varieties

**Definition:** An **arithmetic variety** is a scheme $\mathcal{X} \to \text{Spec}(\mathcal{O}_K)$ where:
- $K$ is a number field with ring of integers $\mathcal{O}_K$
- The generic fiber $X = \mathcal{X}_K$ is a smooth variety over $K$
- $\mathcal{X}$ is proper and flat over $\mathcal{O}_K$

For each embedding $\sigma: K \hookrightarrow \mathbb{C}$, we get a complex variety $X_\sigma = \mathcal{X} \times_\sigma \mathbb{C}$.

### 2.2 Hermitian Line Bundles

**Definition:** A **hermitian line bundle** $\bar{L} = (L, \|\cdot\|)$ on $\mathcal{X}$ consists of:
- A line bundle $L$ on $\mathcal{X}$
- For each $\sigma: K \hookrightarrow \mathbb{C}$, a smooth hermitian metric $\|\cdot\|_\sigma$ on $L_\sigma$
- **Invariance:** $\|\cdot\|_{\bar{\sigma}} = \overline{\|\cdot\|_\sigma}$ (conjugation invariance)

### 2.3 The Chern Form

For a hermitian line bundle $\bar{L}$ and a local section $s$ with $\|s\| = e^{-\phi}$:

$$c_1(\bar{L}) = \frac{\sqrt{-1}}{2\pi} \partial \bar{\partial} \phi = \frac{1}{2\pi} dd^c \phi$$

This is a $(1,1)$-form representing the first Chern class.

**Key Property:** 
$$\int_{X_\sigma} c_1(\bar{L})^{\dim X} = \deg_L(X)$$

---

## Part 3: Green's Functions

### 3.1 Definition and Properties

For a Riemann surface $X$ with volume form $\mu$ (normalized: $\int_X \mu = 1$):

**Arakelov-Green function:** $g: X \times X \to \mathbb{R} \cup \{+\infty\}$ such that:

1. $g(P, Q) = g(Q, P)$ (symmetry)
2. $g(P, Q) + \log|z_P|$ is smooth near $Q$ (where $z_P$ is local coordinate at $P$)
3. $\int_X g(P, Q) \mu(Q) = 0$ (normalization)
4. $\Delta_Q g(P, Q) = \delta_P - \mu$ (Laplacian equation)

### 3.2 Existence and Uniqueness

**Theorem:** For a compact Riemann surface $X$ of genus $g \geq 1$ with canonical metric, the Arakelov-Green function exists and is unique.

**Construction:** Via eigenfunction expansion of Laplacian:
$$g(P, Q) = \sum_{n=1}^{\infty} \frac{\phi_n(P) \overline{\phi_n(Q)}}{\lambda_n}$$
where $\Delta \phi_n = \lambda_n \phi_n$.

### 3.3 Green Functions for Divisors

For a divisor $D = \sum n_i P_i$ on $X$:
$$g_D(Q) = \sum n_i g(P_i, Q)$$

This extends to arithmetic divisors on arithmetic surfaces.

---

## Part 4: Arakelov Divisors and Intersection Theory

### 4.1 Arakelov Divisors

**Definition:** An **Arakelov divisor** on an arithmetic surface $\mathcal{X}$ is a formal sum:
$$\hat{D} = D_{\text{fin}} + \sum_{\sigma} \lambda_\sigma X_\sigma$$

where:
- $D_{\text{fin}}$ is a Weil divisor on $\mathcal{X}$
- $\lambda_\sigma \in \mathbb{R}$ for each archimedean place $\sigma$
- $X_\sigma$ represents the "fiber at infinity"

### 4.2 Principal Arakelov Divisors

For $f \in K(\mathcal{X})^*$, the principal Arakelov divisor is:
$$\widehat{\text{div}}(f) = \text{div}(f) - \sum_\sigma \log|f|_\sigma \cdot X_\sigma$$

where $\log|f|_\sigma$ is the function $\log|f|$ on $X_\sigma(\mathbb{C})$.

### 4.3 The Arakelov Intersection Pairing

**Definition:** For Arakelov divisors $\hat{D}_1, \hat{D}_2$ with disjoint supports:

$$(\hat{D}_1 \cdot \hat{D}_2) = (D_{1,\text{fin}} \cdot D_{2,\text{fin}})_{\text{finite}} + \sum_\sigma (D_1 \cdot D_2)_\sigma$$

where:
- $(D_{1,\text{fin}} \cdot D_{2,\text{fin}})_{\text{finite}} = \sum_\mathfrak{p} i_\mathfrak{p}(D_1, D_2) \log N(\mathfrak{p})$
- $(D_1 \cdot D_2)_\sigma = -\int_{X_\sigma} g_{D_1}(Q) c_1(\mathcal{O}(D_2))$ at archimedean places

**Key Property (Symmetry):**
$$(\hat{D}_1 \cdot \hat{D}_2) = (\hat{D}_2 \cdot \hat{D}_1)$$

---

## Part 5: The Arithmetic Riemann-Roch Theorem

### 5.1 Classical Riemann-Roch (reminder)

For a smooth projective curve $C$ over a field and line bundle $L$:
$$h^0(C, L) - h^1(C, L) = \deg(L) + 1 - g$$

### 5.2 Faltings' Arithmetic Riemann-Roch

For an arithmetic surface $\pi: \mathcal{X} \to \text{Spec}(\mathcal{O}_K)$ and hermitian line bundle $\bar{L}$:

$$\widehat{\deg}(\pi_* \bar{L}) = \frac{1}{2}(\bar{L} \cdot \bar{L}) + \frac{1}{2}(\bar{L} \cdot \bar{\omega}_{\mathcal{X}/\mathcal{O}_K}) + \chi_{\text{top}}$$

where:
- $\widehat{\deg}$ is the arithmetic degree
- $\bar{\omega}$ is the relative dualizing sheaf with Arakelov metric
- $\chi_{\text{top}}$ involves the delta invariant

### 5.3 The Delta Invariant

Faltings' delta invariant $\delta(\mathcal{X}_\sigma)$ captures the arithmetic complexity at archimedean places.

For genus $g$ curves:
$$\delta = -12 \log \|\Delta\|^{1/6}$$
where $\Delta$ is related to the discriminant.

---

## Part 6: Heights and the Faltings Height

### 6.1 Heights of Points

For a point $P \in X(K)$ and hermitian line bundle $\bar{L}$:

$$h_{\bar{L}}(P) = \frac{1}{[K:\mathbb{Q}]} \sum_v n_v \log \|s(P)\|_v^{-1}$$

where $s$ is any section with $s(P) \neq 0$.

This is independent of $s$ (by product formula).

### 6.2 Heights of Subvarieties

**Faltings Height:** For an abelian variety $A$ over $K$:

$$h(A) = \widehat{\deg}(\omega_{\mathcal{A}/\mathcal{O}_K})$$

where $\mathcal{A}$ is the Néron model and $\omega$ is the bundle of invariant differentials.

### 6.3 Key Properties

1. **Northcott Property:** For fixed degree $d$ and height bound $B$, finitely many points/varieties

2. **Functoriality:** For an isogeny $\phi: A \to B$:
   $$h(B) = h(A) + \frac{1}{2}\log|\ker(\phi)|$$

3. **Positivity:** For principally polarized $A$: $h(A) \geq 0$

---

## Part 7: Higher Dimensional Theory (Gillet-Soulé)

### 7.1 Arithmetic Chow Groups

**Definition:** For an arithmetic variety $\mathcal{X}$ of dimension $d$:

$$\widehat{CH}^p(\mathcal{X}) = \frac{Z^p(\mathcal{X}) \oplus \widetilde{D}^{p-1,p-1}(\mathcal{X}_\mathbb{R})}{(\text{principal divisors})}$$

where:
- $Z^p(\mathcal{X})$ = codimension $p$ cycles
- $\widetilde{D}^{p-1,p-1}$ = certain differential forms at infinity

### 7.2 Arithmetic Intersection Product

For $\hat{\alpha} \in \widehat{CH}^p$, $\hat{\beta} \in \widehat{CH}^q$:

$$\hat{\alpha} \cdot \hat{\beta} \in \widehat{CH}^{p+q}(\mathcal{X}) \otimes \mathbb{Q}$$

satisfying:
- Commutativity
- Associativity  
- Projection formula
- Compatibility with classical intersection

### 7.3 Arithmetic Ampleness

**Definition:** A hermitian line bundle $\bar{L}$ is **arithmetically ample** if:
1. $L$ is ample on $\mathcal{X}$
2. $c_1(\bar{L})_\sigma > 0$ for all archimedean $\sigma$

**Key Theorem:** If $\bar{L}$ is arithmetically ample, then:
$$\widehat{\deg}(\bar{L}^{\dim \mathcal{X}}) > 0$$

---

## Part 8: Applications to Transcendence Theory

### 8.1 The Height Bound Strategy

To prove transcendence results:

1. **Construct auxiliary function** using Siegel lemma
2. **Show high vanishing order** at algebraic points
3. **Apply zero estimate** to get lower bound on degree
4. **Use height bound** (Arakelov) to get upper bound
5. **Derive contradiction** if algebraic relations exist

### 8.2 Heights of Periods

**Key Connection:** For abelian variety $A$ with period lattice $\Lambda$:

The Faltings height $h(A)$ bounds:
- The size of periods
- The degree of abelian subvarieties
- The complexity of endomorphisms

### 8.3 The Period Theorem Proof Structure

**Masser-Wüstholz Approach:**

1. Take period $\omega \in \Lambda$
2. Let $B$ = smallest abelian subvariety with $\omega \in T_0(B)$
3. Build auxiliary function vanishing to high order along $\exp(\mathbb{C}\omega)$
4. Apply multiplicity estimate (zero estimate for abelian varieties)
5. Use Faltings height to bound $\deg(B)$

The Arakelov theory provides the precise height estimates needed in step 5.

---

## Part 9: Gaps and Honest Assessment

### What I Can Prove:

1. ✓ The definition and basic properties of arithmetic intersection
2. ✓ How heights relate to intersection numbers
3. ✓ The product formula and its role
4. ✓ Why Arakelov completion is natural

### What I Understand Structurally:

1. ~ The role of Green functions in completing intersection theory
2. ~ How Faltings height controls abelian variety complexity
3. ~ The Gillet-Soulé generalization strategy

### What I Cannot Prove:

1. ✗ The explicit construction of Arakelov-Green functions
2. ✗ The arithmetic Riemann-Roch theorem
3. ✗ The precise bounds in height comparisons
4. ✗ The full Gillet-Soulé higher intersection theory

---

## Part 10: Synthesis with Zero Estimates

### 10.1 The Complete Picture

**For Zero Estimates on Abelian Varieties:**

| Component | Role | Status |
|-----------|------|--------|
| Zero estimates for $\mathbb{G}_m^n$ | Polynomial vanishing bounds | ✓ PROVED |
| Theta functions | Sections of line bundles | Understood |
| Heisenberg group | Structural explanation | Understood |
| Arakelov heights | Degree bounds | Understood |
| Multiplicity estimates | High-order vanishing | Gap remains |

### 10.2 The Path Forward

To fully prove zero estimates for abelian varieties, I would need:

1. **Complete theta function construction** for arbitrary polarizations
2. **Arakelov height bounds** for sections of powers of $L$
3. **Integration of multiplicity estimates** with algebraic group structure
4. **Induction on dimension** via abelian subvarieties

The gap from $\mathbb{G}_m^n$ to abelian varieties is bridged by theta functions (providing the algebraic structure) and Arakelov theory (providing the metric estimates).

---

## References for Further Study

1. Lang, "Introduction to Arakelov Theory" (1988)
2. Soulé et al., "Lectures on Arakelov Geometry" (1991)
3. Bost-Gillet-Soulé, "Heights of Projective Varieties" (1994)
4. Faltings, "Calculus on Arithmetic Surfaces" (1984)
5. Chambert-Loir, "Arakelov Geometry, Heights, Equidistribution" (2017)
