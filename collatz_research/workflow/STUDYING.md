# Collatz Study Notes

> **Role**: 🔬 RESEARCHER
>
> This is your primary workspace. Your job is to expand the toolkit—find theorems, techniques, and connections that might help close the divergence gap.

**Purpose**: Learning and understanding the problem
**Status**: Active

---

## Researcher Protocol

1. **Orient**: Read `CURRENT.md`, then `COLLATZ_UNIFIED_KNOWLEDGE.md` (the master reference)
2. **Review existing work**: Check `archive/` for prior research, `research/` for assignments
3. **Don't duplicate**: If knowledge already exists, EXPAND it, don't rewrite it
4. **Work**: Read papers, synthesize, document NEW insights here
5. **End**: Merge findings INTO `COLLATZ_UNIFIED_KNOWLEDGE.md` (single source of truth)

### Anti-Redundancy Rule
Before writing anything, search for it first. The goal is ONE comprehensive knowledge base, not scattered notes. Your job is to make `COLLATZ_UNIFIED_KNOWLEDGE.md` more complete, not to create parallel documents.

---

## What to Study

### Fundamentals (Mastered)
- [x] The Collatz function and Syracuse map
- [x] 2-adic valuation v₂
- [x] T-function T(n) = v₂(3n+1)
- [x] Cycle equation N × D = S
- [x] LTE Lemma for v₂(3^k - 1)

### Current Focus
- [ ] Transfer operators and spectral theory
- [ ] Renewal theory for Markov chains
- [ ] Functional equations (Berg-Meinardus)
- [ ] (p,q)-adic analysis

### Advanced Topics
- [ ] Cuntz algebra O₂
- [ ] Nevanlinna theory
- [ ] Ergodic theory for number-theoretic dynamical systems

---

## Key Concepts Summary

### The Two-Part Problem

**Part I (SOLVED)**: No non-trivial cycles
- Proof via Dual Constraint Incompatibility
- D | S ⟺ uniform drops ⟹ N = 1

**Part II (OPEN)**: No divergence
- Need: trajectories eventually decrease
- Gap: probabilistic → deterministic

### The Fundamental Gap

All approaches face the same core obstacle:
> Converting "typical/expected" behavior to "all/worst-case" proofs

This is why:
- Tao proves "almost all" but not "all"
- Probabilistic models show contraction but can't guarantee it
- Empirical bounds are never proofs

### Why Divergence is Hard

A trajectory could theoretically diverge if:
1. It sustains >63.1% T = 1 steps forever
2. This requires avoiding q ≡ 3 (mod 8) states
3. But transition matrix pushes toward balanced distribution
4. The gap: proving transitions ARE followed

---

## Reading Notes

### Tao (2019)

**Title**: "Almost all Collatz orbits attain almost bounded values"

**Key insight**: Logarithmic density arguments
- Works for density-1 set of starting values
- "Measure zero" exception is THE gap
- His methods can't close this gap

### Lagarias (1985)

**Title**: "The 3x+1 Problem and Its Generalizations"

**Key points**:
- Comprehensive survey
- Cycle lower bounds
- Why simple approaches fail

### Spectral Calculus Preprint (2025)

**Title**: "The Collatz Conjecture and the Spectral Calculus"

**Key claims**:
- Lasota-Yorke inequality proven
- Spectral gap established
- Remaining gap: Block-Escape exclusion

---

## Questions to Resolve

1. Why does the 4:1 asymmetry (contraction vs expansion) not immediately imply convergence?

2. What exactly prevents a trajectory from "staying lucky" with T = 1 steps?

3. How do spectral methods handle the deterministic nature of Collatz?

4. Is there a Lyapunov function that works? What properties must it have?

---

## Study Log

| Date | Topic | Notes |
|------|-------|-------|
| Dec 2024 | No-cycles proof | Complete, understood |
| Dec 2024 | TB2 analysis | Counterexample found at j=485 |
| Dec 2024 | T-Cascade | Fully understood, elegant proof |
| | | |

---

**END OF STUDY NOTES**
