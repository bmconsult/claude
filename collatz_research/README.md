# Collatz Conjecture Research

Organized research toward proving the Collatz conjecture.

---

## Current Status (December 2024)

| Component | Status |
|-----------|--------|
| **No non-trivial cycles** | **PROVEN** ✓ |
| **No divergence** | OPEN (active research) |

---

## Quick Start

1. **New here?** → Read `workflow/SESSION_BRIEFING.md`
2. **Main reference** → `COLLATZ_UNIFIED_KNOWLEDGE.md`
3. **Active work** → `workflow/WORK_IN_PROGRESS.md`

---

## Folder Structure

```
collatz_research/
│
├── COLLATZ_UNIFIED_KNOWLEDGE.md   # Comprehensive reference
├── README.md                       # This file
│
├── proofs/                         # Formal proofs
│   ├── NO_CYCLES_PROOF.md          # Publishable no-cycles proof
│   ├── T_CASCADE_AND_TB2.md        # T-Cascade theorem + TB2 analysis
│   └── DIVERGENCE_PROGRESS.md      # Divergence work in progress
│
├── research/                       # Research materials
│   ├── PAPERS_NEEDED.md            # References to obtain
│   ├── RESEARCH_ASSIGNMENTS.md     # Active research directions
│   └── FAILED_APPROACHES.md        # What doesn't work (important!)
│
├── workflow/                       # Working documents
│   ├── SESSION_BRIEFING.md         # Quick onboarding
│   ├── STUDYING.md                 # Learning notes
│   ├── SOLVING.md                  # Active problem-solving
│   └── WORK_IN_PROGRESS.md         # Current development state
│
├── archive/                        # Historical source documents
│   ├── COLLATZ_NO_CYCLES_ANALYSIS.md
│   ├── GRADER_CONSULTATION_TB2.md
│   ├── COLLATZ_EXPERT_KNOWLEDGE.md
│   └── (other working papers)
│
├── scripts/                        # Computational tools
│   ├── collatz_cycle_analysis.py
│   └── (other Python files)
│
└── pdfs/                           # Reference papers
    ├── 1909.03562v5.pdf            # Tao's "Almost All"
    ├── 1972-conway.pdf             # Conway's undecidability
    └── (other papers)
```

---

## Key Results

### Proven

| Result | Location |
|--------|----------|
| No non-trivial cycles | `proofs/NO_CYCLES_PROOF.md` |
| T-Cascade theorem | `proofs/T_CASCADE_AND_TB2.md` |
| T_max ≤ log₂(n) + 5 | `proofs/T_CASCADE_AND_TB2.md` |
| Gateway classification | `proofs/T_CASCADE_AND_TB2.md` |

### Falsified

| Claim | Details |
|-------|---------|
| TB2: T_max ≤ log₂(n) + 2 | Counterexample at n ≈ 2^{482.5} |

### Open

| Problem | Status |
|---------|--------|
| No divergence | Active research |

---

## The Remaining Problem

**Part I (No cycles)**: SOLVED

**Part II (No divergence)**: OPEN

The gap is converting probabilistic predictions to deterministic proofs.
See `workflow/SOLVING.md` for current approaches.

---

## Contributing

When making progress:
1. Update `workflow/WORK_IN_PROGRESS.md` with findings
2. If studying, add notes to `workflow/STUDYING.md`
3. If solving, document attempts in `workflow/SOLVING.md`
4. Major results go in `proofs/`
5. Keep `COLLATZ_UNIFIED_KNOWLEDGE.md` current

---

*Last updated: December 2024*
