# Collatz Conjecture Research

This folder contains comprehensive research on the Collatz conjecture, organized for clarity and accessibility.

## Structure

```
collatz_research/
├── COLLATZ_UNIFIED_KNOWLEDGE.md   # Main reference (start here)
├── README.md                       # This file
├── archive/                        # Source documents and working papers
│   ├── COLLATZ_EXPERT_KNOWLEDGE.md     # Deep reference (350 sections, 1.2MB)
│   ├── COLLATZ_BREAKTHROUGH.md         # Self-limitation theorem discovery
│   ├── COLLATZ_DEEP_ALGEBRA.md         # Tight primes and cycle analysis
│   ├── COLLATZ_FAILED_APPROACHES_ANALYSIS.md  # Why approaches fail
│   ├── DIVERGENCE_RESEARCH_REPORT.md   # Transient bound research
│   ├── SOLVING_CLAUDE_BRIEFING.md      # Attack strategy briefing
│   ├── SOLVING_CLAUDE_ADVANCED_BRIEFING.md  # Advanced briefing
│   └── BRIDGING_DOMAINS_STUDY.md       # Cross-domain connections
└── scripts/                        # Computational verification
    ├── collatz_cycle_analysis.py       # Cycle equation analysis
    ├── gowers_computation.py           # Related computations
    └── s_nu_distribution.py            # Distribution analysis
```

## Quick Start

**Start with**: `COLLATZ_UNIFIED_KNOWLEDGE.md`

This is the polished, comprehensive reference containing:
- All key definitions and notation
- Verified theorems with computational proof
- Attack vectors ranked by feasibility
- Remaining gaps clearly identified

## Key Results

| Claim | Status |
|-------|--------|
| LTE Lemma | ✓ Verified |
| Negative drift E[Δlog₂] = -0.415 | ✓ Verified |
| Self-limitation (post-growth pot ≈ 1) | ✓ Verified |
| Polynomial bound M(n) ≤ 4.3n² | ✓ Verified for n < 50k |
| Transient exponent → 1.56 | ✓ Verified for Mersenne |

## The Two Proof Goals

1. **No non-trivial cycles** - Best approach: Dual constraint method
2. **No divergence** - Best approach: Block-Escape analysis

## Archive Contents

The `archive/` folder contains the original working documents:

| Document | Purpose |
|----------|---------|
| `COLLATZ_EXPERT_KNOWLEDGE.md` | Exhaustive reference (use for deep dives) |
| `DIVERGENCE_RESEARCH_REPORT.md` | Latest divergence research with transient bounds |
| `SOLVING_CLAUDE_BRIEFING.md` | Detailed attack strategy |
| Others | Historical working documents |

## Status

**Current state**: Strong empirical evidence, algebraic closure elusive.

**The unified obstruction**: Converting "typical/expected" results to "all/worst-case" proofs.

---

*Last updated: December 2024*
