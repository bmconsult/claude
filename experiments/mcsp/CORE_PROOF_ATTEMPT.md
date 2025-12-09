# The Core Proof Attempt

**Goal**: Prove Gap-MCSP ∉ U₂-Formula[N^{3+ε}] using isotypic analysis.

## The Critical Insight

The locality barrier says: "Gap-MCSP can be computed by local verification."

But here's what that DOESN'T mean:
- It doesn't mean every FORMULA computing Gap-MCSP is local
- It means there EXISTS a circuit with local oracles

A formula is not a circuit with oracles. Formulas are trees. The question is: what's the minimum formula size?

## The Argument Structure

### Lemma 1: Isotypic Projection Complexity

**Claim**: Computing π_λ(T) for λ with dim(λ) ≥ D requires formula size ≥ D^{Ω(1)}.

**Proof sketch**:
- π_λ(T) = (dim(λ)/n!) Σ_{σ∈S_n} χ_λ(σ) T^σ
- This is a linear combination of ALL permuted versions of T
- Any formula computing this must "see" how T behaves under all permutations
- A formula of depth d can only aggregate information from 2^d directions
- To aggregate n! directions requires depth Ω(log n!) = Ω(n log n)
- Formula size ≥ 2^{Ω(n log n)} = N^{Ω(log n)}

Wait, this gives a weak bound. Let me think more carefully...

### Key Observation: Formulas vs Circuits

A circuit can reuse intermediate results. A formula cannot - it's a tree.

For isotypic projection:
- Need to compute Σ_{σ∈S_n} χ_λ(σ) T^σ
- Each term T^σ involves N bits permuted
- A circuit can compute T^σ for all σ with shared structure
- A formula must recompute from scratch for each path

For a formula:
- Each leaf is an input variable
- Each internal node combines two children
- To aggregate all n! permutations requires... many leaves!

**Claim**: Any formula computing π_λ(T) exactly has size ≥ n! for dim(λ) > 1.

**Proof**:
- The output depends on T_i for ALL i in a non-trivial way
- Specifically, changing T_i changes the output (for generic T)
- A formula with s leaves mentions at most s distinct variables
- If s < N, there's some i not mentioned, so output is independent of T_i
- But π_λ(T) depends on all T_i, contradiction
- Wait, N = 2^n, not n!. Let me redo this...

Actually, N = 2^n and n! << 2^n for large n. So formula size could be much smaller than N.

Hmm, the issue is: even though π_λ requires averaging over n! permutations, each permutation just reorders the N inputs. A clever formula might exploit structure.

### Different Approach: Distinguishing Power

Instead of computing projections exactly, consider distinguishing based on projections.

**Definition**: Function F has isotypic distinguishing dimension IDD(F) if F can distinguish inputs T, T' that differ only in components with total dimension ≥ IDD(F).

**Claim**: If F has IDD(F) ≥ D, then formula size of F is at least ???

For this to work, I need to show:
1. Gap-MCSP has large IDD
2. Large IDD implies large formula

### Formalizing IDD

Let T, T' ∈ {0,1}^N. Say T ≡_k T' if π_λ(T) = π_λ(T') for all λ with dim(λ) ≤ k.

**Definition**: IDD(F) = min{k : T ≡_k T' ⟹ F(T) = F(T')}

In words: IDD is the smallest k such that F is determined by projections onto components of dimension ≤ k.

### Claim: IDD(Gap-MCSP) is large

**Argument**:
- Consider T = truth table of a simple function (complexity ≤ s)
- Consider T' = truth table of a complex function (complexity ≥ 2s)
- They might agree on low-dimensional projections but differ on high-dimensional ones
- Gap-MCSP must distinguish them

**Question**: Do simple and complex truth tables necessarily differ on high-dimensional projections?

Let's see...
- Simple T: structured, specific isotypic pattern
- Complex T': random-looking, spread across components

If T and T' agree on all low-dimensional projections, what can we say?

Low-dimensional projections capture "symmetric" and "near-symmetric" structure.
High-dimensional projections capture "asymmetric" structure.

A simple function like x_1 has asymmetric structure (only depends on first variable).
A complex function has... also asymmetric structure (random dependence).

So both might have mass in high-dimensional components!

The difference is:
- Simple: mass in FEW high-dimensional components (the orbit of x_1 is small)
- Complex: mass in MANY high-dimensional components (the orbit of random f is large)

So Gap-MCSP distinguishes based on the DISTRIBUTION of mass across high-dimensional components, not just presence/absence.

### Revised Definition

**Definition**: Isotypic spread IS(T) = #{λ : ‖π_λ(T)‖ > ε, dim(λ) > k}

**Claim**: Simple truth tables have IS(T) ≤ poly(n).
**Claim**: Complex truth tables have IS(T') ≥ exp(n).

If both claims hold, Gap-MCSP distinguishes based on IS, which requires seeing many high-dimensional components.

### Proving the Claims

**Claim 1**: Simple T has small IS(T).

Proof:
- Simple T = truth table of function f with circuit complexity ≤ s
- f depends on ≤ s variables "effectively" (the circuit structure)
- The S_n orbit of f has size ≤ (n choose s) × s! ≤ n^s
- Each orbit contributes to ≤ ??? isotypic components
- ...

Actually, this is where I'm stuck. The orbit size doesn't directly bound the isotypic spread.

**Alternative**: The SUPPORT of a simple function.

If f has circuit complexity s, then f can be written as a composition of s gates.
Each gate involves at most 2 inputs.
So f depends on at most 2s input positions "at the leaves."

No wait, that's not right either - a circuit of size s can compute functions of n variables.

Let me think about what makes simple functions "structured" in isotypic terms.

For f(x) = x_1 (projection):
- Truth table: 0 on first half, 1 on second half
- S_n orbit: {x_1, ..., x_n}
- Isotypic decomposition: ???

The key representation is the "permutation representation" on the n coordinate functions.
This decomposes as: trivial + standard = (n) + (n-1, 1).

So x_1 has mass in exactly 2 isotypic components: trivial (constant part) and standard (the varying part).

For f(x) = x_1 ∧ x_2:
- S_n orbit: {x_i ∧ x_j : i ≠ j}
- Isotypic decomposition: related to 2-tensors

The representation on 2-subsets decomposes as: (n) + (n-1, 1) + (n-2, 2) for n ≥ 4.

So x_1 ∧ x_2 has mass in 3 isotypic components.

**Pattern**: Simple functions built from k-ary operations have mass in O(k) isotypic components.

A circuit of depth d with 2-input gates: each level doubles the "arity" roughly, so depth d → arity 2^d → O(2^d) components.

For size s, depth = O(log s), so O(s) components.

**Claim** (refined): A function with circuit size s has isotypic spread IS(T) ≤ poly(s).

**Claim** (random): A random function has IS(T) ≥ p(n) - O(1) ≈ exp(√n) with high probability.

If s = N^{0.01} and p(n) = exp(O(√n)) = exp(O(√log N)):
- Simple: IS ≤ N^{0.01}
- Random: IS ≥ exp(√log N)

For Gap-MCSP to distinguish these:
- It must detect when IS is small vs large
- Detecting small IS requires formula size ≥ ???

### The Final Gap

I still need: "Distinguishing IS ≤ small vs IS ≥ large requires large formula."

This is where the argument should connect to the concentration lemma.

If a formula has size s:
- It can only "see" poly(s) isotypic components
- Distinguishing based on IS requires seeing at least IS components
- So formula size ≥ IS_large / poly(1) = exp(√log N) / poly(1)

This gives formula size ≥ exp(Ω(√log N)), which is superpolynomial but NOT N^{3+ε}!

The gap: N^{3+ε} vs exp(√log N).

N^{3+ε} = exp((3+ε) log N)
exp(√log N) = much smaller

So the isotypic spread argument gives SOME lower bound, but not enough for magnification!

### What's Missing

To get N^{3+ε}:
- Need IS_complex ≥ N^{3+ε}
- But IS ≤ p(n) = exp(√n) = exp(√log N)

The number of isotypic components is bounded by p(n), which is much smaller than N^3.

So isotypic spread can't directly give N^3 bounds!

### Alternative: Weighted Isotypic Measure

Instead of counting components, weight by dimension:

WIS(T) = Σ_λ dim(λ) × 1[‖π_λ(T)‖ > ε]

Now:
- Σ_λ dim(λ)² = n! (by representation theory)
- So WIS(T) ≤ √(p(n) × n!) ≈ n!^{0.5} for average T

For N = 2^n: n! = n^n ≈ (log N)^{log N}

This is larger than exp(√log N) but still not N^3.

Actually, wait. n! = Γ(n+1) ≈ (n/e)^n ≈ e^{n ln n}.

N^3 = 2^{3n} = e^{3n ln 2}.

Comparing exponents: n ln n vs 3n ln 2.

n ln n > 3n ln 2 when ln n > 3 ln 2 ≈ 2, i.e., n > e² ≈ 7.4.

So for n ≥ 8: n! > N^3!

This means the total "budget" of weighted isotypic dimensions is large enough!

### Revised Argument

**Claim**: WIS(complex T) ≈ n!/poly(n) with high probability.

Because random functions spread mass across all components, and total weighted dimension is n!.

**Claim**: WIS(simple T) ≤ poly(n) for circuit complexity ≤ n^c.

Because simple functions have structured isotypic decomposition.

**Claim**: Formula of size s can distinguish based on at most poly(s) weighted isotypic dimension.

If these hold:
- Gap-MCSP distinguishes WIS ≈ n!/poly(n) vs WIS ≤ poly(n)
- Requires formula size ≥ n!/poly(n) / poly(1) ≈ n!/poly(n)
- n! > N^3 for n ≥ 8
- So formula size ≥ N^{3+ε} for appropriate parameters!

THIS MIGHT WORK!

### The Proof (Sketch)

1. **Define** WIS(T) = Σ_λ dim(λ) × 1[‖π_λ(T)‖² > ε‖T‖²]

2. **Prove** WIS(random T) ≈ n!/poly(n) w.h.p.
   - Random T has ‖π_λ(T)‖² ≈ dim(λ)²/N × ‖T‖² for each λ (equidistribution)
   - Sum over λ: Σ dim(λ) × 1[dim(λ)² > εN]
   - For ε = 1/poly(n), most high-dimensional components are included

3. **Prove** WIS(simple T) ≤ poly(n) for circuit size ≤ n^c
   - Induction on circuit structure
   - Base: variables have WIS ≤ 2 (trivial + standard)
   - Step: AND/OR gate multiplies WIS by at most poly(n) (Kronecker bound)
   - Result: size s circuit gives WIS ≤ s^{O(1)} × poly(n)

4. **Prove** Formula size s ⟹ can distinguish based on WIS ≤ poly(s)
   - A formula computes a function of the inputs
   - The function's "sensitivity" to isotypic structure is bounded
   - Specifically: if formula has size s, it can only detect when WIS differs by poly(s)

5. **Conclude**: Gap-MCSP requires formula size ≥ n!/poly(n) ≈ N^{Ω(log N)} >> N^{3+ε}

Actually, n!/poly(n) > N^{3+ε} for n ≥ 8, so we get the needed bound!

### Remaining Gaps

The proof sketch has several gaps:

1. **Step 2**: Need to prove random T has large WIS. This requires understanding the equidistribution of random vectors in isotypic components.

2. **Step 3**: Need to prove the Kronecker coefficient bound - that AND/OR gates multiply WIS by at most poly(n).

3. **Step 4**: Need to prove formulas have bounded isotypic sensitivity.

4. **Non-localization**: Need to verify this argument doesn't apply to circuits with local oracles.

Each gap is technical but potentially closable. The overall structure is sound!
