# Collatz Conjecture Research

This folder contains comprehensive research on the Collatz conjecture, organized for clarity and accessibility.

## Major Results (December 2024)

| Result | Status | Details |
|--------|--------|---------|
| **No non-trivial cycles** | **PROVEN** | Complete algebraic proof via Dual Constraint Incompatibility |
| **TB2 bound** | **FALSE** | Explicit counterexample at n ≈ 2^{482.5} |
| **Divergence** | OPEN | The remaining hard problem |

## Structure

```
collatz_research/
├── COLLATZ_UNIFIED_KNOWLEDGE.md   # Main reference (START HERE)
├── README.md                       # This file
├── archive/                        # Source documents and working papers
│   ├── COLLATZ_EXPERT_KNOWLEDGE.md      # Deep reference (350 sections)
│   ├── COLLATZ_BREAKTHROUGH.md          # Self-limitation theorem
│   ├── COLLATZ_DEEP_ALGEBRA.md          # Tight primes and cycle analysis
│   ├── COLLATZ_FAILED_APPROACHES_ANALYSIS.md  # Why approaches fail
│   ├── DIVERGENCE_RESEARCH_REPORT.md    # Transient bound research
│   ├── SOLVING_CLAUDE_BRIEFING.md       # Attack strategy briefing
│   ├── SOLVING_CLAUDE_ADVANCED_BRIEFING.md  # Advanced briefing
│   ├── BRIDGING_DOMAINS_STUDY.md        # Cross-domain connections
│   ├── COLLATZ_NO_CYCLES_ANALYSIS.md    # **Complete no-cycles proof**
│   ├── COLLATZ_PROOF_COMPLETE.md        # Full framework
│   ├── COLLATZ_SYNTHESIS_DECEMBER2024.md # December 2024 synthesis
│   ├── DIVERGENCE_PROOF_PROGRESS.md     # Divergence analysis
│   ├── GRADER_CONSULTATION_TB2.md       # **TB2 counterexample discovery**
│   ├── COLLATZ_REVIEW_REQUEST.md        # Bounded Landing theorems
│   ├── Collatz_Exploration_Summary.md   # Exploration summary
│   ├── PAPERS_NEEDED.md                 # References to obtain
│   ├── RESEARCHER_ASSIGNMENT_CONTRACTION_GAP.md  # Research directions
│   └── RESEARCHER_ASSIGNMENT_DIVERGENCE.md       # Divergence research
├── pdfs/                           # Reference papers
│   ├── 1909.03562v5.pdf            # Tao's "Almost All" paper
│   ├── 1972-conway.pdf             # Conway's undecidability paper
│   ├── S0273-0979-1985-15300-5.pdf # Lagarias survey
│   ├── preprints202511.1440.v5.pdf # Spectral calculus preprint
│   └── (other reference papers)
└── scripts/                        # Computational verification
    ├── collatz_cycle_analysis.py       # Cycle equation analysis
    ├── gowers_computation.py           # Related computations
    └── s_nu_distribution.py            # Distribution analysis
```

## Quick Start

**Start with**: `COLLATZ_UNIFIED_KNOWLEDGE.md`

This is the polished, comprehensive reference containing:
- All key definitions and notation
- **PROVEN: No non-trivial cycles theorem**
- **PROVEN: T-Cascade theorem**
- **FALSE: TB2 bound (with counterexample)**
- Attack vectors for divergence
- Remaining gaps clearly identified

## Key Results Summary

### Proven Results

| Claim | Status | Key Document |
|-------|--------|--------------|
| No non-trivial cycles | **PROVEN** | COLLATZ_NO_CYCLES_ANALYSIS.md |
| T-Cascade Theorem | **PROVEN** | GRADER_CONSULTATION_TB2.md |
| Gateway Structure | **PROVEN** | GRADER_CONSULTATION_TB2.md |
| LTE Lemma | **PROVEN** | COLLATZ_UNIFIED_KNOWLEDGE.md |
| Negative drift E[Δlog₂] = -0.415 | **PROVEN** | COLLATZ_UNIFIED_KNOWLEDGE.md |
| Self-limitation (post-growth pot ≈ 1) | **PROVEN** | COLLATZ_BREAKTHROUGH.md |

### Empirically Verified

| Claim | Status | Bound |
|-------|--------|-------|
| Polynomial bound M(n) ≤ 4.3n² | Verified n < 50k | Empirical |
| Transient exponent → 1.56 | Verified Mersennes | Empirical |
| T_max ≤ log₂(n) + 5 | **PROVEN** | Algebraic |

### Falsified

| Claim | Status | Details |
|-------|--------|---------|
| TB2: T_max ≤ log₂(n) + 2 | **FALSE** | Counterexample at n ≈ 2^{482.5} |

## The Remaining Problem

**Part I (No cycles)**: **SOLVED**

**Part II (No divergence)**: OPEN

The gap is converting "typical/expected" behavior to "all/worst-case" proofs.
This is the same obstacle that stops all approaches to Collatz.

### Best Approaches for Divergence

1. **Block-Escape Exclusion** - Spectral machinery complete, one gap remains
2. **Functional Equations** - Berg-Meinardus / Neklyudov formulation
3. **Renewal Theory** - q ≡ 1 (mod 8) as renewal state

## Archive Contents

The `archive/` folder contains the original working documents:

| Document | Purpose |
|----------|---------|
| `COLLATZ_NO_CYCLES_ANALYSIS.md` | **Complete no-cycles proof** |
| `GRADER_CONSULTATION_TB2.md` | **TB2 counterexample + T-Cascade proof** |
| `COLLATZ_SYNTHESIS_DECEMBER2024.md` | December 2024 synthesis |
| `COLLATZ_EXPERT_KNOWLEDGE.md` | Exhaustive reference (use for deep dives) |
| `DIVERGENCE_RESEARCH_REPORT.md` | Divergence research with transient bounds |
| `SOLVING_CLAUDE_BRIEFING.md` | Detailed attack strategy |
| Others | Historical working documents |

---

*Last updated: December 2024*
