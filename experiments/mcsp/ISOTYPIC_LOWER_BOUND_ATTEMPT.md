# Isotypic Lower Bound Attempt

**Goal**: Prove Gap-MCSP requires formula size N^{3+ε} using isotypic spread

## The Core Lemma (To Prove)

### Definition: Isotypic Spread

For f: {0,1}^n → {0,1}, define:

```
IsoSpread(f) = Σ_{λ ⊢ n} dim(λ) × 1[‖π_λ(f)‖² > ε]
```

where π_λ(f) is projection onto λ-isotypic component.

### Key Lemma (Isotypic Concentration)

**Claim**: A formula of depth d has Fourier weight concentrated on at most exp(O(d)) isotypic components with significant mass.

**Proof Sketch**:

1. **Gate-level analysis**: Each AND/OR gate performs a convolution in representation space.

2. **Representation-theoretic convolution**:
   - For S_n, we have: V_λ ⊗ V_μ = ⊕_ν c^ν_{λμ} V_ν
   - c^ν_{λμ} = Littlewood-Richardson coefficients
   - These coefficients are bounded

3. **Component growth**:
   - Starting from variables (live in standard rep + trivial)
   - Each gate at most doubles the number of significant components
   - Depth d → at most 2^d significant components

4. **Size-depth conversion**:
   - Formula of size s can be balanced to depth O(log s)
   - Therefore at most s^{O(1)} = poly(s) significant components

### Theorem (Isotypic Spread Lower Bound)

If IsoSpread(f) ≥ M, then formula size of f is at least M^{Ω(1)}.

**Proof**:
- Size s formula → depth O(log s) when balanced
- Depth d → at most exp(O(d)) significant components
- IsoSpread(f) ≥ M → need exp(O(d)) ≥ M
- Therefore d ≥ Ω(log M)
- Size s = exp(Ω(d)) = M^{Ω(1)} ∎

## Applying to Gap-MCSP

### Claim: Gap-MCSP Has Large Isotypic Spread

**Need to show**: IsoSpread(Gap-MCSP) ≥ 2^{Ω(n)}

**Argument**:

1. Gap-MCSP is S_n-invariant but depends on "global" properties

2. Circuit complexity is a "generic" property - it doesn't align with any particular irrep

3. Intuitively: distinguishing low-complexity from high-complexity requires understanding the full structure

4. **Formal claim**: The indicator function of "low complexity" has significant mass in irreps with dimension ≥ 2^{n/3}

**Why this is plausible**:
- Low complexity truth tables form a small fraction of all truth tables
- They're distributed "randomly" with respect to the S_n action
- A random function on S_n-orbits would have mass in all irreps proportional to dim²
- Low-complexity functions are a random-looking subset → mass spreads

### Why Local Oracles Fail

**Claim**: Functions depending on k positions have IsoSpread ≤ n^{O(k)}

**Proof**:
- A function depending on k positions is determined by values on 2^k inputs
- These inputs form at most (n choose k) ≤ n^k orbits under S_n
- The induced function on orbits decomposes into at most n^k irreps with mass
- Each irrep has dimension at most n!/(n-k)! ≈ n^k
- Total IsoSpread ≤ n^k × n^k = n^{O(k)}

For k = O(log n): IsoSpread ≤ n^{O(log n)} = poly(n)

But Gap-MCSP has IsoSpread ≥ 2^{Ω(n)} → **contradiction** if local oracles suffice!

## The Magnification Connection

If we can prove:
- Gap-MCSP has IsoSpread ≥ 2^{Ω(n)} on N = 2^n bit inputs
- This implies formula size ≥ 2^{Ω(n)} = N^{Ω(1)}

For the magnification threshold N^{3+ε}:
- Need IsoSpread ≥ N^{3+ε}
- This is 2^{(3+ε)n}
- Requires most irreps with dimension > 2^{n/2} to have significant mass

## Technical Gaps

### Gap 1: Formalizing Littlewood-Richardson Bound

Need precise statement: If f₁ has mass in components C₁ and f₂ has mass in components C₂, then f₁ ∧ f₂ has mass in components C₁₂ where |C₁₂| ≤ |C₁| × |C₂| × poly(n).

### Gap 2: Proving Gap-MCSP Has Large IsoSpread

Need to show low-complexity truth tables are "spread" across isotypic components.

This requires understanding:
- How many truth tables have complexity ≤ s?
- How are they distributed across S_n-orbits?
- What's the isotypic decomposition of the indicator function?

### Gap 3: The N^{3+ε} Threshold

Current argument gives formula size ≥ N^{Ω(1)}, but magnification needs N^{3+ε}.

Need to:
1. Quantify IsoSpread of Gap-MCSP precisely
2. Tighten the concentration lemma constants
3. Match the magnification threshold

## Next Steps

1. **Formalize the Littlewood-Richardson bound** for Boolean operations
   - This is representation theory + Boolean function analysis
   - Should be provable with existing theory

2. **Estimate IsoSpread of Gap-MCSP**
   - Count low-complexity functions
   - Analyze their distribution across orbits
   - Compute (or bound) isotypic projections

3. **Tighten constants** to match N^{3+ε}

4. **Verify non-localization**
   - Show the isotypic spread argument doesn't extend to oracle circuits
   - This should follow from the local oracle bound

## The Vision

A complete proof would be:

1. **Lemma (Isotypic Concentration)**: Depth-d formulas touch ≤ exp(O(d)) components.

2. **Lemma (Gap-MCSP IsoSpread)**: Gap-MCSP has IsoSpread ≥ N^{3+ε}.

3. **Theorem**: Gap-MCSP ∉ U₂-Formula[N^{3+ε}].

4. **Corollary (via Magnification)**: P ≠ NP.

Each lemma is technical but potentially provable with existing tools.
