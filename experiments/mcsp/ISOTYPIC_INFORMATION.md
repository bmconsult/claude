# Isotypic Information Theory

## The Key Insight

Projections can be computed efficiently in O(N polylog N).
But formulas might have bounded "isotypic information capacity."

## Definitions

### Isotypic State

For a truth table T ∈ {0,1}^N, define its **isotypic state**:

Iso(T) = (‖π_λ(T)‖² : λ ⊢ n)

This is a vector of p(n) non-negative reals giving the mass in each isotypic component.

**Normalization**: Σ_λ ‖π_λ(T)‖² = ‖T‖² = #{x: T(x)=1} (Hamming weight)

### Isotypic Information

The **isotypic information** of T is the number of bits needed to specify Iso(T) up to sufficient precision.

**Crude bound**: p(n) real numbers → O(p(n) × precision) bits

But with structure, might need fewer bits.

### Isotypic Entropy

For a distribution D over truth tables, define:

H_iso(D) = H(Iso(T) : T ~ D)

This measures how much isotypic variation there is in D.

## The Formulas-Information Connection

### Conjecture: Isotypic Information Bound

**Conjecture**: A formula F of size s can only compute functions that depend on O(poly(s)) bits of isotypic information.

More precisely: There exists a function g: R^{poly(s)} → {0,1} such that:

F(T) = g(I₁(T), I₂(T), ..., I_{poly(s)}(T))

where each I_j is a "simple" function of Iso(T).

### Why This Might Be True

A formula is a tree of AND/OR/NOT gates.
Each gate combines two functions.

**At each gate**: The isotypic information accessible "branches" at most by some constant factor.

By induction:
- Depth 0 (input variables): O(n) isotypic bits (which coordinates are involved)
- Depth d: O(n × c^d) isotypic bits for some constant c

For size s formula: depth O(log s), so O(n × c^{log s}) = O(n × s^{log c}) = O(n × poly(s))

**Total**: O(n × poly(s)) = O(poly(s, n)) isotypic bits

### What Gap-MCSP Needs

**Claim**: Gap-MCSP requires Ω(n!) isotypic bits to compute.

**Why**:
- Simple functions have concentrated isotypic mass (few components)
- Complex functions have spread isotypic mass (many components)
- Distinguishing these requires seeing enough of the isotypic state

To distinguish between:
- Iso_simple: mass in ≤ poly(n) components
- Iso_complex: mass spread across ≈ n!/poly(n) components

Needs Ω(log(n!/poly(n))) = Ω(n log n) bits at minimum.

But actually need more: to verify mass is SPREAD, need to check many components.

**Claim**: Verifying spread requires Ω(n!) bits of isotypic information.

### The Lower Bound

If:
1. Formulas of size s access ≤ poly(s, n) isotypic bits
2. Gap-MCSP requires ≥ n! isotypic bits

Then:
poly(s, n) ≥ n!
s ≥ n!^{Ω(1)} / poly(n)

For n ≥ 20: n! > N^3, so s > N^3.

**This would prove Gap-MCSP ∉ Formula[N^{3+ε}]!**

## Formalizing "Isotypic Bits"

### Definition 1: Projection Access

F **accesses** component λ if F's output depends on π_λ(T) for some inputs.

**Isotypic access set**: Acc(F) = {λ : F accesses λ}

**Conjecture**: |Acc(F)| ≤ poly(size(F))

### Definition 2: Isotypic Sensitivity

For each λ, define F's **isotypic sensitivity** at λ:

IS_λ(F) = max_{T,T' : π_λ(T) ≠ π_λ(T'), π_μ(T)=π_μ(T') ∀μ≠λ} |F(T) - F(T')|

**Conjecture**: Σ_λ IS_λ(F) ≤ poly(size(F))

### Definition 3: Isotypic Influence

Analogous to Fourier influence:

Inf_λ(F) = Pr_{T uniform}[F is sensitive to component λ]

**Conjecture**: Σ_λ Inf_λ(F) ≤ poly(size(F))

## Which Definition is Right?

Different definitions might give different bounds:
- Access set: counting components
- Sensitivity: total sensitivity budget
- Influence: probabilistic measure

The "right" definition is the one where:
1. Formulas have bounded quantity
2. Gap-MCSP requires high quantity

## The Research Program

1. **Define** the right notion of isotypic information
2. **Prove** formulas have bounded isotypic information
3. **Prove** Gap-MCSP requires high isotypic information
4. **Conclude** Gap-MCSP ∉ Formula[N^{3+ε}]

## Connection to Communication Complexity

This is like a communication complexity problem:
- Alice has the "simple components" of T
- Bob has the "complex components" of T
- They want to compute Gap-MCSP(T)

If Gap-MCSP has high "isotypic communication complexity," then formulas are hard.

## What the Papers Should Tell Us

1. **Algebraic metacomplexity**: What's the "algebraic isotypic information" of metapolynomials?
2. **Locality barrier**: How does "locality" relate to "isotypic information access"?
3. **Magnification**: Why is N^{3+ε} specifically the threshold?

## Optimistic Outlook

If "isotypic information" can be properly defined and bounded for formulas,
this could be the missing piece that closes the quantitative gap!

The key technical work is:
- Proving the formula bound (like LMN for Fourier, but for isotypic)
- Proving the Gap-MCSP requirement (information-theoretic argument)
