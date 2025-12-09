# Collatz Research Session Briefing

**Purpose**: Quick onboarding for new Claude sessions
**Last Updated**: December 2024

---

## TL;DR

- **No cycles**: PROVEN ✓
- **No divergence**: OPEN (this is what we're working on)
- **Main reference**: `COLLATZ_UNIFIED_KNOWLEDGE.md`

---

## What's Been Solved

### No Non-Trivial Cycles (COMPLETE)

**Theorem**: The only Collatz cycle is 1 → 4 → 2 → 1.

**Proof method**: Dual Constraint Incompatibility
- For cycle equation N = S/D, D | S ⟺ uniform drops
- Uniform drops give N = 1
- See: `proofs/NO_CYCLES_PROOF.md`

### T-Cascade Theorem (COMPLETE)

**Theorem**: For T(n) ≥ 2, T(next_odd(n)) = T(n) - 1

**Implication**: T can only increase from T = 1 values
- See: `proofs/T_CASCADE_AND_TB2.md`

### TB2 Status (RESOLVED)

**TB2 claimed**: T_max(n) ≤ log₂(n) + 2
**Reality**: FALSE - counterexample at n ≈ 2^{482.5}
**What IS true**: T_max(n) ≤ log₂(n) + 5 (proven)

---

## Current Goal

**Prove no Collatz trajectory diverges to infinity.**

### Why It's Hard

The gap is probabilistic → deterministic:
- Probabilistic model shows E[Δlog₂] = -0.415 (contraction)
- But Collatz trajectories are deterministic
- Need to prove deterministic sequences can't "stay lucky"

### Current Approaches

1. **Block-Escape Exclusion** (spectral methods)
2. **Renewal Theory** (q ≡ 1 mod 8 as reset point)
3. **Functional Equations** (Berg-Meinardus)

---

## Key Concepts

### The T-Function

T(n) = v₂(3n + 1) = number of times 2 divides 3n+1

| T value | Effect | Probability |
|---------|--------|-------------|
| 1 | Growth (~1.5×) | ~50% |
| 2 | Shrink (~0.75×) | ~25% |
| ≥3 | Strong shrink | ~25% |

### Mersenne Numbers

M_k = 2^k - 1 have T(M_k) = k (maximum possible for their size)

### The 4:1 Asymmetry

- q ≡ 3 (mod 8): Strong contraction (-1.97 log factor)
- q ≡ 5 (mod 8): Expansion (+0.52 log factor)
- One q≡3 visit cancels four q≡5 visits

---

## File Structure

```
collatz_research/
├── COLLATZ_UNIFIED_KNOWLEDGE.md  ← START HERE
├── proofs/
│   ├── NO_CYCLES_PROOF.md        ← Publishable
│   ├── T_CASCADE_AND_TB2.md
│   └── DIVERGENCE_PROGRESS.md
├── research/
│   ├── PAPERS_NEEDED.md
│   ├── RESEARCH_ASSIGNMENTS.md
│   └── FAILED_APPROACHES.md
├── workflow/
│   ├── SESSION_BRIEFING.md       ← You are here
│   ├── STUDYING.md
│   ├── SOLVING.md
│   └── WORK_IN_PROGRESS.md
├── archive/                       ← Historical docs
├── scripts/                       ← Python tools
└── pdfs/                          ← Reference papers
```

---

## Do's and Don'ts

**DO**:
- Read COLLATZ_UNIFIED_KNOWLEDGE.md first
- Check WORK_IN_PROGRESS.md for current state
- Use SOLVING.md for active attempts
- Update files as you make progress

**DON'T**:
- Re-prove no-cycles (it's done)
- Assume TB2 is true (it's false for large n)
- Try simple Lyapunov functions (they don't exist)
- Ignore the probabilistic→deterministic gap (it's real)

---

## Quick Reference

**Key formulas**:
```python
def T(v):  # v must be odd
    return v2(3*v + 1)

def collatz_step(v):
    return (3*v + 1) // (2**T(v))
```

**Key constants**:
- log₂(3) ≈ 1.585
- E[T] = 2
- E[Δlog₂] ≈ -0.415
- Break-even T=1 fraction: 63.1%

---

**Good luck!**
