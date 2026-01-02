# Lonely Runner Conjecture - General Proof Attempts

**Goal:** Rigorous algebraic proof for ALL n (not computational verification)

**Calibration (from CLAUDE.md):**
- P(appears correct) = 5% (1/20)
- P(actually correct | appears correct) = 10% (1/10)
- P(actually correct) = 0.5% (1/200)
- Strategy: 10 rounds of 20 attempts = 200 total

---

## Round 1 (Previous Session)
- Produced a proof that appeared correct
- Adversarial review found fatal gaps
- Status: DISPROVED

---

## Round 2 (Current Session)

### Attempt 1: Measure Theory / Union Bound
**Approach:** View trajectory on n-torus, bound measure of "bad" region.

**Result:** DISPROVED
- μ(bad) ≤ n · (2/(n+1)) = 2n/(n+1) → 2 for large n
- Union bound gives bad region measure > 1
- Cannot guarantee good point exists from measure alone

**Learning:** Pure measure arguments fail. Must use arithmetic structure of speeds.

---

### Attempt 2: Beatty Sequence / Farey Fractions
**Approach:** Analyze valid k values at denominator m as arithmetic progressions (arcs) in Z/mZ.

**Result:** BLOCKED
- Each arc has size ≈ (n-1)m/(n+1)
- Need intersection of n arcs to be nonempty
- Arc positions depend on speed ratios - can't prove intersection guaranteed

**Learning:** Arc intersection is a key sub-problem.

---

### Attempt 3: View Obstruction (Cusick)
**Approach:** Use equidistribution on torus - trajectory is dense, good region has positive measure.

**Result:** BLOCKED
- μ(good) = ((n-1)/(n+1))^n → e^{-2} ≈ 13.5% > 0
- Equidistribution guarantees hitting good region for SOME t
- But need t ∈ (0,1), not t → ∞

**Learning:** Density/equidistribution proves existence but not in bounded time.

---

### Attempt 4: Algebraic Number Theory / Cyclotomic
**Approach:** Use roots of unity, exponential sums, cyclotomic structure.

**Result:** BLOCKED
- Reformulated in terms of e^{2πi·v_i·t} avoiding arc near 1
- No clean algebraic structure emerged
- Exponential sums don't directly give the constraint

**Learning:** Need different algebraic objects.

---

### Attempt 5: Covering Congruences
**Approach:** Failure of LRC = bad sets cover all rationals in (0,1).

**Result:** BLOCKED
- For prime p, constraint is arc intersection in Z/pZ
- Arc sizes are (n-1)/(n+1) of the circle
- Intersection depends on specific speed positions, not just sizes

**Learning:** Arc intersection problem is unavoidable.

---

### Attempt 6: Induction on n
**Approach:** Remove fastest runner, apply induction, perturb to include runner n.

**Result:** DISPROVED
- Inductive hypothesis gives runners 1..n-1 in [1/n, (n-1)/n]
- Slack to expand to [1/(n+1), n/(n+1)] is 1/(n(n+1))
- Perturbation needed for runner n is up to 1/((n+1)v_n)
- Slack insufficient: would need v_n ≥ n·v_{n-1}, not generally true

**Learning:** Naive induction fails due to insufficient slack.

---

### Attempt 7: Strong Induction with Margins
**Approach:** Strengthen inductive hypothesis to guarantee margin ε(n) > 0.

**Result:** DISPROVED
- LRC bound is TIGHT - speeds (1,2,...,n) achieve exactly 1/(n+1)
- Cannot strengthen hypothesis when bound is achieved

**Learning:** No room for stronger induction.

---

### Attempt 8: Probabilistic Method
**Approach:** Show random t ∈ [0,1] satisfies LRC with positive probability.

**Result:** BLOCKED
- P(runner i bad) = 2/(n+1)
- If independent: P(all good) = ((n-1)/(n+1))^n > 0 ✓
- But ALL events depend on same t - complete dependency graph
- Lovász Local Lemma doesn't apply

**Learning:** Complete dependency defeats standard probabilistic tools.

---

### Attempt 9: Discrepancy Theory (Erdős-Turán)
**Approach:** Bound discrepancy of n runners using exponential sums.

**Result:** DISPROVED
- Erdős-Turán gives D = O(√n / log n)
- Need discrepancy D < 1/(n+1) = O(1/n)
- Bounds are O(√n), way too weak

**Learning:** Discrepancy bounds fundamentally insufficient.

---

### Attempt 10: Geometry of Numbers (Minkowski)
**Approach:** Use lattice theory, Minkowski's theorem on torus.

**Result:** BLOCKED
- For coprime speeds, trajectory is dense in T^n
- Density ⟹ ∃t with trajectory in good region
- But density requires t → ∞, not t ∈ (0,1)

**Learning:** Same bounded-time problem as Attempt 3.

---

### Attempt 11: Simultaneous Diophantine Approximation
**Approach:** Use Dirichlet's theorem to find t = p/q with good approximation.

**Result:** BLOCKED
- Dirichlet gives approximation to any target
- But for LRC, need SIMULTANEOUS constraint for all speeds
- Circles back to "does some prime p work for all speeds?"

**Learning:** Same arc intersection problem.

---

### Attempt 12: Polynomial Method
**Approach:** Encode constraints as polynomials over finite fields.

**Result:** BLOCKED
- Indicator of [L,R] has degree O(R-L) = O(p/n)
- Degree too high for polynomial method bounds

**Learning:** Polynomial method structure doesn't fit.

---

### Attempt 13: Pigeonhole / Box Principle
**Approach:** Divide [0,1) into intervals, count by pigeonhole.

**Result:** BLOCKED
- Average # bad runners at any time ≈ 2
- Need variance analysis to find time with 0 bad
- Correlations between runner positions complicate analysis

**Learning:** Correlation structure is the core difficulty.

---

### Attempt 14: Topological / Fixed Point
**Approach:** Use Brouwer fixed point or degree theory.

**Result:** BLOCKED
- Can't find suitable continuous map where fixed points = lonely times
- Problem is fundamentally discrete/arithmetic, not topological

**Learning:** Topology not the right framework.

---

### Attempt 15: Group Action (Wilson's Theorem Style)
**Approach:** Find group action where orbit counting gives lonely times.

**Result:** BLOCKED
- For Wilson's theorem: conjugation on symmetric group
- For LRC: no suitable group action found
- Translation and multiplication don't preserve lonely condition

**Learning:** Need different algebraic structure than symmetric groups.

---

### Attempt 16: Helly's Theorem
**Approach:** Good sets as arcs, use Helly-type intersection theorem.

**Result:** BLOCKED
- Good(v) is union of v intervals, not convex
- Helly requires convexity
- Fractional Helly might apply but needs pairwise intersection guarantee

**Learning:** Convexity assumption fails.

---

### Attempt 17: Sieve Methods
**Approach:** Use Selberg sieve to count lonely times.

**Result:** BLOCKED
- Inclusion-exclusion works if events "independent"
- Correlations create error terms
- Sieve error analysis unclear for this correlation structure

**Learning:** Would need precise correlation bounds.

---

### Attempt 18: Ergodic Theory
**Approach:** Use Birkhoff ergodic theorem, quantitative bounds.

**Result:** BLOCKED
- Birkhoff: fraction of time in good region → μ(good) > 0
- Quantitative: |{t ∈ [0,T] : good}| ≥ T·μ(good) - O(T^{1-δ})
- At T=1, error term dominates

**Learning:** Effective ergodic bounds too weak for T=1.

---

### Attempt 19: First Return Time
**Approach:** Bound first entrance time to good region.

**Result:** BLOCKED
- Kac's lemma: expected return time ≈ 1/μ(good) ≈ e² ≈ 7.4
- Expected time > 1, can't guarantee entrance by t=1
- Specific analysis for t=k/(n+1) circles back to arc intersection

**Learning:** Return time bounds insufficient.

---

### Attempt 20: Direct Construction
**Approach:** Construct explicit lonely time for specific speed families.

**Result:** PARTIAL
- For (1,2,...,n): t = 1/(n+1) works! Positions are 1/(n+1), 2/(n+1), ..., n/(n+1)
- All positions exactly in [1/(n+1), n/(n+1)] ✓
- Cannot generalize construction to arbitrary coprime speeds

**Learning:** Construction works for arithmetic progressions but not generally.

---

## Round 2 Summary

**Attempts:** 20
**Proofs found:** 0
**Approaches disproved:** 5 (measure, induction, strong induction, discrepancy, direct construction partial)
**Approaches blocked:** 15 (need more insight to continue)

### Key Blockers Identified

1. **Arc Intersection Problem:** Most approaches reduce to proving n arcs on Z/pZ have nonempty intersection for some prime p. This is the core combinatorial problem.

2. **Bounded Time Problem:** Equidistribution/density/ergodic arguments prove existence for t → ∞, but LRC needs t ∈ (0,1).

3. **Correlation Structure:** Probabilistic/sieve methods fail because all n runner positions are determined by single parameter t - complete dependency.

### Promising Directions for Round 3

1. **Solve arc intersection directly:** Prove that for any n coprime speeds, ∃ prime p where n arcs of size (n-1)p/(n+1) intersect.

2. **Exploit arithmetic structure:** Speeds being coprime must constrain the arc positions in a useful way.

3. **Hybrid approach:** Combine direct construction (works for special cases) with perturbation/approximation.

4. **Different reformulation:** Find new mathematical objects (not arcs, not torus flow) that capture LRC structure.

---

## Status
- **Round:** 2 of 10
- **Attempts this round:** 20/20
- **Total attempts:** ~40 (Round 1 + Round 2)
- **Proofs found:** 0
- **Next:** Round 3

---

*Last updated: January 2, 2026*
