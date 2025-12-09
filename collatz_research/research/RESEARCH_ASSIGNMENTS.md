# Collatz Research Assignments

**Status**: Active research directions
**Last Updated**: December 2024

---

## Current Focus Areas

### 1. Divergence Proof (PRIMARY)

**Goal**: Prove no Collatz trajectory diverges to infinity.

**Status**: The main open problem. No-cycles is solved.

**Key approaches**:
- Block-Escape exclusion (spectral methods)
- Renewal theory (q ≡ 1 mod 8 as renewal state)
- Functional equations (Berg-Meinardus)

---

## Research Task: Contraction Gap Analysis

### The Problem

We have proven:
- No cycles (Dual Constraint Incompatibility)
- T_max(n) ≤ log₂(n) + 5
- Negative expected drift E[Δlog₂] ≈ -0.415

We have NOT proven:
- Deterministic trajectories follow probabilistic predictions

### Key Findings

**Markov chain on q mod 8** at T=1 visits:
- E[log(factor)] = -0.58 < 0 under stationary distribution
- Transition matrix is approximately uniform
- Contraction is 4× stronger than expansion

**The 4:1 Asymmetry**:
- Expansion (q ≡ 5): +0.52 per visit
- Contraction (q ≡ 3): -1.97 per visit
- ONE visit to q ≡ 3 cancels FOUR visits to q ≡ 5

### Research Directions

**Direction A: Algebraic Proof of Mixing**

Prove algebraically that for any starting q, the sequence of qᵢ mod 8 visits all classes.

**Approach**: Use the mod 32/64/128 structure to show no class can be avoided.

**Direction B: Modified Lyapunov Function**

Find L(n) = log(v) + correction(q mod 8) that strictly decreases.

**Challenge**: The correction must handle the fact that q ≡ 5 expands.

**Direction C: Direct Bound on Consecutive q ≡ 5 Visits**

Prove that no trajectory can have more than K consecutive visits to q ≡ 5 for some fixed K.

---

## Research Task: Divergence Analysis

### What We Need

**Task 1: Block-Escape Definition**
- What exactly is the "Block-Escape Property"?
- What is the "unconditional exponential upper bound"?

**Task 2: Net Growth Factor per Block**
- Expected/worst-case NET change per T=1 visit?
- Block residence time analysis?

**Task 3: Lyapunov Function Candidates**
- φ(v) = log(v) - c·T(v)
- φ(v) = v / 2^{T(v)}
- φ(v) = v^α / f(T(v))

**Task 4: Mersenne Stability**
- Prove M_j is stable (T_max = j) for all j ≥ 7 algebraically

**Task 5: Connection Between T_max and Trajectory Max**
- Relationship between T_max and M(n)?
- Maximum ratio M(n)/n as function of T_max(n)?

---

## Completed Research

### No-Cycles (SOLVED)

- Dual Constraint Incompatibility theorem
- D | S ⟺ uniform drops
- Complete algebraic proof

### T-Cascade (SOLVED)

- T(n) ≥ 2 ⟹ T(next) = T(n) - 1
- Gateway structure classified
- Backward tree analysis complete

### TB2 Analysis (RESOLVED)

- TB2 is FALSE (counterexample at j = 485)
- Weaker bound T_max ≤ log₂(n) + 5 is PROVEN
- Gateway mod 3 classification complete

---

## Priority Order

1. **HIGH**: Divergence proof via Block-Escape exclusion
2. **MEDIUM**: Renewal theory formalization
3. **LOW**: Alternative approaches (functional equations, Cuntz algebra)

---

**END OF ASSIGNMENTS**
