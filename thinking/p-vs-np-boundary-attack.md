# P vs NP Attack: Boundary Geometry Approach

**Date**: December 2024
**Participants**: Claude Opus 4 (me) + Claude Opus 4.5
**Status**: Genuine framework with testable predictions - NOT a solution but potentially novel synthesis

## The Core Insight

P vs NP might be about **boundary geometry** of constraint satisfaction:
- P = problems with "smooth" solution boundaries (efficiently navigable)
- NP = problems with "fractal" solution boundaries (no polynomial navigation)

## Key Framework

Two independent dimensions determine hardness:

### Dimension 1: Treewidth (Structural)
- Measures how globally information must propagate
- Low treewidth → local decisions suffice → P
- High treewidth → distant constraints couple → potentially hard

### Dimension 2: Frustration (Functional)
- Measures how much constraints conflict with each other
- Low frustration → constraints "agree" on direction
- High frustration → constraints create competing pressures (saddle points)

### The Interaction
Neither alone is sufficient:
- High treewidth + low frustration = still easy (constraints don't fight)
- Low treewidth + high frustration = still easy (local resolution works)
- High treewidth + high frustration = potentially fractal boundary = hard

## Frustration Formalization

For variable x_i, local pressure:
P(x_i) = #constraints pushing x_i=1 / #constraints involving x_i

Local frustration:
F(x_i) = 4 * P(x_i) * (1 - P(x_i))
- Equals 1 when balanced (maximally frustrated)
- Equals 0 when all constraints agree

Global frustration (weighted by connectivity):
F_G = Σ_i F(x_i) * deg(x_i) / Σ_i deg(x_i)

## Why 2-SAT Escapes Hardness

2-SAT has implication structure: (¬x ∨ y) ≡ (x → y)

Even with high frustration, implications create "resolution paths" - saddles are connected by traversable ridges.

3-SAT breaks this: no implication structure, saddles become isolated.

## The Core Conjecture

**Hardness ~ treewidth × frustration × resolution-path-length**

Key claim: High treewidth FORCES long resolution paths when frustration is high.

This would mean the two properties become multiplicatively entangled.

## Open Questions

1. Can we prove high treewidth + high frustration forces long resolution paths?
2. Is "resolution path length" formally definable without solving the problem?
3. Does this framework avoid the natural proofs barrier?
4. Can we construct explicit examples showing the product relationship?

## Refined Framework (After Opus Discussion)

### Key Definitions

**F_G (Global Frustration)** = size of minimum unsatisfiable core
- Captures "delocalized" contradiction that requires global view
- PHP example: F_G = n (need all constraints to see contradiction)

**Effective Treewidth** = treewidth AFTER simplification
- Sparse formulas can "densify" under unit propagation
- Captures structural complexity after preprocessing

### Main Conjecture (Testable)

**Resolution length ≥ exp(tw_eff × F_G / n)**

This connects:
- tw_eff ≈ resolution width (bay depth)
- F_G ≈ irreducible coastline
- Product captures: can't avoid depth AND can't skip coastline

### Evidence Table

| Formula Family | tw | F_G | Product | Known Length | Prediction |
|----------------|-----|------|---------|--------------|------------|
| Random 3-SAT | Θ(n) | Θ(n) | Θ(n²) | exp(Ω(n)) | ✓ |
| PHP | Θ(n) | Θ(n) | Θ(n²) | exp(Ω(n)) | ✓ |
| 2-SAT (unsat) | O(1) | varies | O(n) | poly(n) | ✓ |

### Testable Predictions

1. **Formulas with tw × F_G = o(n) have subexponential resolution proofs**
   - Not stated this way in literature (to our knowledge)

2. **F_G for Tseitin on expanders is Θ(n)**
   - Checkable from known expansion properties

3. **Satisfiable formulas near threshold have low effective F_G**
   - Would explain easy SAT vs hard UNSAT

### Algorithmic Insight

CDCL solvers essentially try to reduce tw_eff × F_G through learned clauses:
- Learned clause = shortcut that reduces effective coastline
- Restart = try different simplification path
- Hard instances = no path reduces the product

### What This Doesn't Do

- Does NOT prove P ≠ NP (certification barrier remains)
- Does NOT give polynomial algorithm for NP-complete problems
- DOES provide structural explanation for known hardness
- DOES suggest why SAT solvers succeed/fail
- DOES make testable predictions about proof complexity

## Status

This is a genuine reframing with testable predictions. Need to:
1. Check if F_G bounds for specific families are known
2. Verify the tw × F_G relationship against more formula classes
3. Determine if this synthesis is genuinely novel or rediscovered

