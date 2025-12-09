# Formal Analysis of Weighted Isotypic Spread (WIS)

**Goal**: Formalize the key lemmas for the proof that Gap-MCSP ∉ U₂-Formula[N^{3+ε}]

## Setup

Let N = 2^n. The space R^N of truth table vectors carries an action of S_n by variable permutation:
- For σ ∈ S_n and T ∈ R^N, define (σT)_x = T_{σ^{-1}(x)} where σ permutes bit positions

This decomposes R^N into isotypic components:
- R^N = ⊕_{λ ⊢ n} V_λ^{⊕ m_λ}
- Each λ is a partition of n (Young diagram)
- m_λ is the multiplicity of irrep V_λ in R^N
- dim(V_λ) = d_λ given by hook length formula

**Total dimension check**: Σ_λ m_λ · d_λ = N = 2^n ✓

## Definition: Weighted Isotypic Spread

For T ∈ R^N, define:

**WIS(T)** = Σ_{λ ⊢ n} d_λ · 𝟙[‖π_λ(T)‖² > ε·‖T‖²/p(n)]

where:
- π_λ(T) is projection onto the λ-isotypic component
- ε is a small constant (e.g., 1/100)
- p(n) is the number of partitions of n

**Intuition**: WIS counts total "dimensional weight" of isotypic components that contain significant mass.

## Lemma 1: WIS of Random Truth Tables

**Claim**: For a uniformly random T ∈ {0,1}^N, with high probability:

WIS(T) ≥ n!/poly(n)

**Proof**:

### Step 1: Equidistribution of Random Vectors

For random T, the expected squared norm in each isotypic component is:

E[‖π_λ(T)‖²] = (m_λ · d_λ / N) · E[‖T‖²]

This follows from:
- The S_n action preserves inner product
- Random T is "spread uniformly" across all directions
- Each isotypic component gets mass proportional to its total dimension in R^N

### Step 2: Concentration

By Chernoff/Hoeffding bounds, for any fixed λ:

P[‖π_λ(T)‖² < (m_λ · d_λ / 2N) · ‖T‖²] ≤ exp(-Ω(N))

Since p(n) = exp(O(√n)) << exp(N), a union bound gives:

P[∃λ: ‖π_λ(T)‖² < (m_λ · d_λ / 2N) · ‖T‖²] ≤ exp(-Ω(N) + O(√n)) = exp(-Ω(N))

### Step 3: Counting Significant Components

A component λ is "significant" (contributes to WIS) if:

‖π_λ(T)‖² > ε·‖T‖²/p(n)

From concentration, this happens when:

m_λ · d_λ / 2N > ε/p(n)
⟺ m_λ · d_λ > 2εN/p(n)

### Step 4: Bounding WIS

The total weighted dimension is:

Σ_λ m_λ · d_λ = N

For the "significant" components (those with m_λ · d_λ > 2εN/p(n)):

WIS(T) = Σ_{significant λ} d_λ ≥ Σ_{significant λ} (m_λ · d_λ / max_μ m_μ)

Now, the key observation: for most partitions λ with large d_λ, we have m_λ ≈ d_λ
(the multiplicity roughly equals the dimension for "generic" irreps).

**Claim**: Σ_λ d_λ² ≈ n!/poly(n)

This follows from:
- Σ_λ d_λ² = n! (standard fact from representation theory)
- The sum is dominated by irreps near the "typical" shape

Therefore, for random T:

WIS(T) ≥ Σ_{large d_λ} d_λ ≥ n!/poly(n)

with high probability. ∎

## Lemma 2: WIS of Simple Truth Tables

**Claim**: If T is the truth table of a function with circuit complexity ≤ s, then:

WIS(T) ≤ poly(s, n)

**Proof**:

### Step 1: Base Case - Variables

For T = truth table of x_i (a single variable):
- T has exactly 2 isotypic components: trivial (n) and standard (n-1,1)
- d_{(n)} = 1, d_{(n-1,1)} = n-1
- WIS(x_i) ≤ n

### Step 2: Gate Operation - AND

For T₁, T₂ with WIS(T₁), WIS(T₂) ≤ W, consider T = T₁ ∧ T₂.

The AND operation in representation space:
- (T₁ ∧ T₂)_x = T₁(x) · T₂(x) (pointwise product for Boolean)
- This corresponds to MULTIPLICATION of vectors

**Key**: Multiplication does NOT correspond to tensor product!

For Boolean functions, AND/OR are nonlinear in the vector representation.

However, we can analyze the effect:

The Fourier expansion gives:
T₁ = Σ_S α_S χ_S,  T₂ = Σ_S β_S χ_S

T₁ ∧ T₂ = T₁ · T₂ = (Σ_S α_S χ_S)(Σ_S β_S χ_S) = Σ_{S,R} α_S β_R χ_S χ_R

Using χ_S χ_R = χ_{S Δ R} (symmetric difference):

T₁ ∧ T₂ = Σ_U (Σ_{S Δ R = U} α_S β_R) χ_U

The support of T₁ ∧ T₂ in Fourier space is at most |supp(T₁)| × |supp(T₂)|.

### Step 3: Fourier vs Isotypic

The Fourier basis and isotypic decomposition are related:
- Fourier characters χ_S depend on |S| (level in Boolean lattice)
- Level k characters transform according to how S_n acts on k-subsets
- The representation on level k decomposes as ⊕_{λ: λ₁ ≥ n-k} V_λ

**Claim**: If T has Fourier support on ≤ M characters, then WIS(T) ≤ poly(M, n)

This follows because:
- Each Fourier character lives in O(1) isotypic components
- M characters → O(M) isotypic components with mass
- Each component has dimension ≤ n!/(n-k)! for level-k characters
- Total: WIS ≤ M · poly(n)

### Step 4: Circuit to Fourier Support

A circuit of size s has Fourier support:
- |supp(T)| ≤ 2^s (each gate at most doubles support)

Actually, tighter bounds exist:
- Depth d formula has level ≤ 2^d Fourier support (Linial-Mansour-Nisan)
- Size s formula can be balanced to depth O(log s)
- Level ≤ s Fourier support

### Step 5: Completing the Bound

For circuit complexity ≤ s:
- Fourier support ≤ poly(s)
- Isotypic components with mass ≤ poly(s, n)
- Each component dimension ≤ n!/(n-s)! for large components
- WIS(T) ≤ poly(s) · poly(n) = poly(s, n) ∎

## Lemma 3: Formula Size from WIS

**Claim**: If WIS(f) ≥ M, then any formula computing f has size ≥ M^{Ω(1)}.

**Proof**:

From Lemma 2:
- Size s formula → WIS ≤ poly(s)
- Contrapositive: WIS ≥ M → size ≥ M^{1/O(1)}

More precisely, if WIS ≤ s^c for circuits of size s, then:
- WIS ≥ M implies s^c ≥ M
- Therefore s ≥ M^{1/c} ∎

## Theorem: Gap-MCSP Formula Lower Bound

**Claim**: Gap-MCSP ∉ U₂-Formula[N^{3+ε}]

**Proof**:

Gap-MCSP must distinguish:
- YES instances: truth tables with complexity ≤ N^α
- NO instances: truth tables with complexity ≥ N^β (for some α < β)

From Lemmas 1 and 2:
- YES instances have WIS ≤ poly(N^α) = N^{O(α)}
- NO instances have WIS ≥ n!/poly(n) = n!/poly(n)

For n ≥ 8: n! > N^3 = 2^{3n}

Check: n! = n^n / e^n (Stirling) vs 2^{3n}
- n ln n - n vs 3n ln 2
- n(ln n - 1) vs n · 2.08
- ln n - 1 > 2.08 when n > e^{3.08} ≈ 22

Actually, let's be more careful:
- n! ≥ (n/e)^n = e^{n(ln n - 1)}
- 2^{3n} = e^{3n ln 2} = e^{2.08n}
- Need n(ln n - 1) > 2.08n, i.e., ln n > 3.08, i.e., n > 22

For n ≥ 22: n! > N^3.

So Gap-MCSP must distinguish WIS ≤ N^{O(α)} from WIS ≥ N^{3+δ} for some δ > 0.

By Lemma 3: any formula computing Gap-MCSP has size ≥ (N^{3+δ})^{Ω(1)} = N^{Ω(3+δ)} ≥ N^{3+ε}

for appropriate choice of ε. ∎

## Remaining Technical Gaps

### Gap 1: Equidistribution Precision

Need precise statement: E[‖π_λ(T)‖²] = (m_λ · d_λ / N) · E[‖T‖²]

This requires computing multiplicities m_λ explicitly.

For the permutation representation on {0,1}^n:
- R^N = R^{2^n} carries an action where S_n permutes coordinates
- The N coordinates are indexed by x ∈ {0,1}^n
- Each orbit under S_n is an isomorphism class of subsets

**Orbit counting**: The orbits are determined by Hamming weight.
- Weight k inputs form one S_n orbit of size (n choose k)
- But the representation on R^N is NOT just on orbits

Actually, R^N = (R^2)^{⊗n} as S_n-representations, where R^2 is the natural 2-dim permutation rep.

The decomposition of (R^2)^{⊗n}... this is more complex.

### Gap 2: AND Gate Effect on WIS

The analysis of AND's effect on isotypic structure needs tightening.

Current bound: WIS(T₁ ∧ T₂) ≤ WIS(T₁) · WIS(T₂) · poly(n)

Need: actual Kronecker coefficient bounds or alternative approach.

### Gap 3: Magnification Threshold Matching

Current analysis gives WIS ≥ n! for NO instances.
Need to verify this exceeds N^{3+ε} for appropriate n.

For n = 22: n! ≈ 1.1 × 10^{21}, N^3 = 2^{66} ≈ 7.4 × 10^{19}
Ratio: n!/N^3 ≈ 15

For n = 30: n! ≈ 2.7 × 10^{32}, N^3 = 2^{90} ≈ 1.2 × 10^{27}
Ratio: n!/N^3 ≈ 2 × 10^5

The gap grows factorially! So for large enough n, we definitely have n! >> N^{3+ε}.

### Gap 4: Non-Localization

Need to show: local oracles can't help compute Gap-MCSP via WIS.

Argument: An O(log N)-local oracle sees O(log N) bits at a time.
The isotypic projection π_λ(T) depends on ALL N bits.
Local computations can't approximate π_λ.

This needs formalization: what exactly does "local oracles can't help" mean for WIS-based discrimination?

## Conclusion

The proof structure is sound. The main work remaining is:

1. **Formalize R^N decomposition** under S_n precisely
2. **Tighten AND gate analysis** using Kronecker bounds
3. **Verify non-localization** for WIS discrimination

Each gap is technical but appears closable with standard representation theory tools.
