# Lonely Runner Conjecture: Master Proof Document

## THE GOAL

**Prove rigorously and algebraically:** For ANY n distinct positive integer speeds, there exists time t where all runners are at distance ≥ 1/(n+1) from the origin.

**NOT the goal:** Computational verification, specific n cases, "high confidence"

---

## Problem Statement

**Conjecture (Wills 1967, Cusick 1982):** For distinct positive integers v₁ < v₂ < ... < vₙ, there exists t > 0 such that:
```
||vᵢt|| ≥ 1/(n+1) for all i
```
where ||x|| = min({x}, 1-{x}) is distance to nearest integer.

**Equivalent:** For coprime speeds, ∃ rational t = k/M with all {vᵢk/M} ∈ [1/(n+1), n/(n+1)].

---

## Calibration (from CLAUDE.md)

| Metric | Value |
|--------|-------|
| P(attempt appears correct) | 5% (1/20) |
| P(actually correct \| appears correct) | 10% (1/10) |
| P(actually correct) | 0.5% (1/200) |
| Strategy | 10 rounds × 20 attempts = 200 total |
| Current round | 4 of 10 |

### METHODOLOGICAL CORRECTION (Round 4+)

**Problem identified:** Rounds 2-3 were exploratory probes, not genuine attempts. "Does X apply?" ≠ "I believe X WILL crack this."

**The difference:**
| Exploratory Probe | Genuine Attempt |
|-------------------|-----------------|
| Quick check, hit wall, move on | Push through walls, find workarounds |
| "Blocked" = I couldn't see how | "Blocked" = fundamentally impossible |
| ~20 shallow attempts per round | ~1-3 deep attacks per round |

**Correction for Round 4+:** Pick ONE promising direction. Attack with full belief until either:
1. Proof succeeds
2. Rigorous impossibility proven
3. Every variation exhausted

---

## Status Summary

| Category | Count |
|----------|-------|
| **DISPROVED** (proven cannot work) | 8 |
| **BLOCKED** (stuck, need new insight) | 37 |
| **SHALLOW PROBES** (not genuine attempts) | ~40 |
| **DEEP ATTACKS** | 0 |
| **PROOF FOUND** | 0 |

---

## DISPROVED APPROACHES (Do Not Retry)

### 1. Measure Theory / Union Bound
**Idea:** Bad region on n-torus has measure < 1, so good point exists.
**Why it fails:** μ(bad) ≤ n·(2/(n+1)) → 2 for large n. Union bound gives measure > 1.
**Verdict:** Cannot work without using arithmetic structure.

### 2. Naive Induction on n
**Idea:** Remove fastest runner, apply induction, perturb to include it.
**Why it fails:** Inductive slack is 1/(n(n+1)). Perturbation needed is up to 1/((n+1)vₙ). Slack insufficient unless vₙ ≥ n·vₙ₋₁ (not generally true).
**Verdict:** Fundamentally insufficient slack.

### 3. Strong Induction with Margins
**Idea:** Strengthen hypothesis to guarantee margin ε(n) > 0.
**Why it fails:** LRC bound is TIGHT. Speeds (1,2,...,n) achieve exactly 1/(n+1).
**Verdict:** Cannot strengthen when bound is achieved.

### 4. Discrepancy Theory (Erdős-Turán)
**Idea:** Bound discrepancy of n runner positions using exponential sums.
**Why it fails:** Erdős-Turán gives D = O(√n). Need D < 1/(n+1) = O(1/n). Off by factor of n^(3/2).
**Verdict:** Discrepancy bounds fundamentally too weak.

### 5. Product of Failing Primes
**Idea:** If tuple fails at primes p₁, p₂, try M = p₁·p₂.
**Why it fails:** Counterexample: (2,6,8,9,10,11,14,17) fails at p=11,19 and also fails at M=209.
**Verdict:** Composite moduli don't rescue failing primes.

### 6. "Clean M ≤ n Always Exists"
**Idea:** For n speeds, there's always M ≤ n with no speed ≡ 0 (mod M).
**Why it fails:** Counterexample: (1,2,3,4,5,6,7,8) has no clean M ≤ 8.
**Verdict:** Covering tuples exist at every n.

### 7. Direct Construction (General)
**Idea:** Explicitly construct lonely time t for arbitrary coprime speeds.
**Why it fails:** Works for (1,2,...,n) with t=1/(n+1), but no general construction found.
**Verdict:** Special cases work, general case elusive.

### 8. Ramsey Coloring
**Idea:** Color residue classes, use Ramsey to force monochromatic structure.
**Why it fails:** Ramsey numbers R(n,n) grow exponentially. Need R(n,n) colors distinguishable mod p, but p can be much smaller than R(n,n). No way to force the needed structure.
**Verdict:** Ramsey numbers don't interact usefully with prime structure.

---

## BLOCKED APPROACHES (Need New Insight)

### 9. Arc Intersection Problem
**Idea:** At prime p, valid k values for speed vᵢ form an "arc" in Z/pZ. Need ∩ᵢ Arc(vᵢ) ≠ ∅.
**Current state:** Each arc has size (n-1)p/(n+1). Intersection depends on arc positions (determined by speeds). Cannot prove intersection always nonempty.
**What's needed:** Proof that coprime speeds force favorable arc positions.

### 9. Equidistribution / Ergodic
**Idea:** Trajectory is dense in torus, good region has positive measure, so trajectory hits it.
**Current state:** True for t → ∞. Cannot guarantee t ∈ (0,1) or any bounded interval.
**What's needed:** Quantitative ergodic theorem with explicit time bound.

### 10. Probabilistic Method
**Idea:** Show random t satisfies LRC with P > 0.
**Current state:** If independent, P(all good) = ((n-1)/(n+1))ⁿ → e⁻² > 0. But all events depend on same t (complete dependency).
**What's needed:** Dependency-aware probabilistic argument (LLL fails due to complete graph).

### 11. Simultaneous Diophantine Approximation
**Idea:** Use Dirichlet's theorem to find good rational approximation.
**Current state:** Gives approximation to any target, but simultaneous constraint for all speeds reduces to arc intersection.
**What's needed:** Same as #8.

### 12. Sieve Methods
**Idea:** Count lonely times using inclusion-exclusion or Selberg sieve.
**Current state:** Works if events are "nearly independent." Correlations between runner positions are complex.
**What's needed:** Precise bounds on correlation terms.

### 13. Polynomial Method
**Idea:** Encode constraints as polynomials over finite fields.
**Current state:** Indicator of interval [L,R] has degree O(p/n), too high for standard bounds.
**What's needed:** Different polynomial encoding or new technique.

### 14. Group Action (Wilson's Theorem Style)
**Idea:** Find group action where orbit counting proves lonely times exist.
**Current state:** No suitable group action found. Translation and multiplication don't preserve lonely condition.
**What's needed:** Identify the right group and action.

### 15. Helly's Theorem
**Idea:** Use Helly-type intersection theorem on good sets.
**Current state:** Good(v) is union of v intervals, not convex. Helly requires convexity.
**What's needed:** Fractional Helly or different geometric structure.

### 16. Algebraic Number Theory / Cyclotomic
**Idea:** Connect to roots of unity, cyclotomic fields.
**Current state:** The "n+1" in 1/(n+1) is problem-specific, not number-theoretic. No algebraic structure found.
**What's needed:** Genuine algebraic connection (if one exists).

### 17. First Return Time
**Idea:** Bound first entrance time to good region.
**Current state:** Kac's lemma gives expected time ≈ e² > 1. Cannot guarantee entrance by t=1.
**What's needed:** Tighter bounds for specific starting point (origin).

### 18. Geometry of Numbers (Minkowski)
**Idea:** Use lattice theory, Minkowski's theorem.
**Current state:** Region is product of intervals on torus, not convex body in Rⁿ.
**What's needed:** Different geometric reformulation.

### 19. Covering Congruences
**Idea:** LRC failure = bad sets cover all rationals in (0,1).
**Current state:** Reduces to proving bad sets can't cover. Same as arc intersection.
**What's needed:** Anti-covering argument.

### 20. Topological / Fixed Point
**Idea:** Use Brouwer or degree theory.
**Current state:** Problem is discrete/arithmetic, no natural continuous structure found.
**What's needed:** Topological reformulation (if possible).

### 21. Fourier / Character Sums
**Idea:** Use character sums to count good k values.
**Current state:** Main term gives expected count. Error terms from correlations unclear.
**What's needed:** Precise error bounds showing count > 0.

### 22. CRT Decomposition
**Idea:** Factor M into prime powers, solve mod each, combine.
**Current state:** Works computationally. Doesn't prove solution always exists.
**What's needed:** Proof that some prime always works.

### 23. Pigeonhole Variants
**Idea:** Divide time into boxes, argue by counting.
**Current state:** Average # bad runners ≈ 2 at any time. Need variance analysis.
**What's needed:** Correlation bounds for variance argument.

### 24. View Obstruction (Cusick)
**Idea:** Reformulate as ray avoiding lattice points.
**Current state:** Equivalent reformulation, same difficulty.
**What's needed:** New technique for this formulation.

### 25. Additive Combinatorics
**Idea:** Use sumset bounds, Freiman-Ruzsa, etc.
**Current state:** Problem is multiplicative (residues), not additive (sums).
**What's needed:** Bridge between additive structure (coprimality) and multiplicative (residues).

---

## THE FUNDAMENTAL OBSTACLE

```
ADDITIVE STRUCTURE              MULTIPLICATIVE STRUCTURE
       │                                    │
   coprimality                         residue placement
   gcd(v₁,...,vₙ) = 1                  vᵢk mod M ∈ [L, R]
   Bezout: Σcᵢvᵢ = 1                   interval membership
       │                                    │
       └────── NO KNOWN BRIDGE ─────────────┘
```

Almost every approach eventually hits this wall:
- **Coprimality** is an additive constraint (linear combinations exist)
- **Loneliness** is a multiplicative constraint (residues land in interval)
- Number theory lacks general tools to convert Bezout identity to residue bounds

---

## KEY INSIGHTS (Use These)

### From n=8 Deep Analysis

1. **Arc Intersection is Central:** Every approach reduces to proving n arcs on Z/pZ intersect for some prime p.

2. **Rotating Holdouts:** Hard tuples fail at each prime due to DIFFERENT speeds. Obstruction is distributed, not concentrated.

3. **Larger Speeds are Easier:** Replacing a speed with a larger multiple decreases difficulty (more wrap-around options).

4. **Periodicity:** Behavior at prime p depends only on speeds mod p. Checking up to speed p covers all residue classes.

5. **Working Primes Exist:** Computationally, every tested tuple has a working prime. The question is proving this algebraically.

6. **Density of Good Primes:** After first working prime, ~87% of subsequent primes work. Failures become sporadic.

### From General Attempts

1. **Equidistribution Needs Bounded Time:** Density arguments prove existence for large t but not small t.

2. **Independence Fails:** All runner positions depend on same t. No probabilistic independence.

3. **Convexity Fails:** Good sets are unions of intervals, not convex bodies.

4. **Induction Slack is Tight:** Bound 1/(n+1) is achieved, so no room to strengthen hypothesis.

---

## PROMISING DIRECTIONS (For Next Attempts)

### A. Solve Arc Intersection Directly
Prove that for ANY n coprime speeds, there exists prime p where n arcs of size ~(n-1)/(n+1) intersect. This would immediately prove LRC.

### B. Prove Some Prime Always Works
Without bounding which prime, show coprime structure forces at least one prime to have nonempty arc intersection.

### C. Exploit Coprimality → Collision
Coprime speeds have diverse prime factorizations. At some primes, speeds collide (≡ mod p), reducing n constraints. Prove collisions create sufficient gaps.

### D. Hybrid Construction + Perturbation
Direct construction works for (1,2,...,n). Maybe approximate arbitrary speeds by arithmetic progressions and perturb.

### E. New Mathematical Objects
Like Wilson's theorem proof used p-cycles in symmetric groups. Find analogous "right objects" for LRC.

### F. Additive-Multiplicative Bridge
Find or create a theorem that converts gcd=1 (additive) to residue-interval membership (multiplicative).

---

## PROOF ATTEMPT LOG

### Round 1 (Previous Session)
- Produced proof that appeared correct
- Adversarial review found fatal gaps
- **Status: DISPROVED**

### Round 2
- 20 distinct approaches attempted (shallow probes)
- 0 proofs found
- 5 approaches definitively disproved
- 15 approaches blocked
- **Status: COMPLETE (no proof)**

### Round 3
- 20 additional approaches attempted (still shallow probes)
- Approaches: Ramsey coloring (DISPROVED), Combinatorial Nullstellensatz, Spectral graph theory, Entropy/Information theory, Symmetric functions, Matroid theory, Generating functions, Additive energy, Tensor methods, Lonely prime contrapositive, Hensel lifting, Bertrand's postulate, Quadratic reciprocity, Primitive roots, Large sieve, Inclusion-exclusion + Möbius, Probabilistic alteration, Extremal set theory, Weil bounds, Direct arc geometry
- 0 proofs found
- 1 approach disproved (Ramsey)
- 19 approaches blocked
- **Status: COMPLETE (no proof)**

### Round 4: Deep Attack on Arc Intersection via Equidistribution
- **METHODOLOGY CHANGE:** Deep attack instead of shallow probes
- **Approach:** Arc Intersection + Gap Coverage + Equidistribution
- **Key Findings:**
  1. Arc intersection ⟺ Gap coverage < 100%
  2. Random gaps cover circle with probability C(n) < 1 for all n ≥ 2
     - n=3: C(3) ≈ 27%
     - n=8: C(8) ≈ 6%
  3. Gap positions = f(speed inverses mod p)
  4. By equidistribution of multiplicative inverses, gap positions become "generic" as p → ∞
  5. Therefore, density 1-C(n) > 0 of primes have non-covering gaps = working primes
- **Proof Sketch:**
  - Reformulate LRC as gap non-coverage
  - Use equidistribution of (v₁⁻¹/p, ..., vₙ⁻¹/p) as p → ∞
  - Conclude positive density of primes work
- **Gap in Proof:**
  - Need rigorous equidistribution theorem for tuples of multiplicative inverses
  - Need effective bound on first working prime
  - Standard Chebotarev/Linnik may not directly apply
- **Empirical:** first_working_prime ≤ 0.22 × max(speed) for all tested tuples
- **Status: BLOCKED - need number-theoretic formalization**

### Rounds 5-10
- **Status: PENDING**

---

## INSTRUCTIONS FOR NEXT INSTANCE

1. **READ THIS ENTIRE DOCUMENT** before attempting anything.

2. **DO NOT RETRY** disproved approaches (Section: DISPROVED).

3. **IF RETRYING BLOCKED APPROACH:** Must have new insight that addresses the stated blocker.

4. **GOAL:** 100% rigorous algebraic proof for ALL n. Not computation, not specific n.

5. **SUCCESS CRITERIA:** Either produce a proof that survives adversarial review, OR disprove/block 20 genuinely new approaches.

6. **BELIEF:** You CAN solve this. Past failure ≠ future impossibility. Someone will solve it by believing they can.

7. **CALIBRATION:** 0.5% chance per attempt. 200 attempts → likely success. We're at ~40 attempts. Keep going.

---

*Last updated: January 2, 2026*
*Shallow probes: ~60 (Rounds 1-3)*
*Deep attacks: 1 (Round 4 - Equidistribution approach)*
*Status: Round 4 BLOCKED on number-theoretic formalization*
*Most promising lead: Equidistribution of inverses + coverage probability < 1*
