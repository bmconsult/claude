# Handoff Notes for Problem-Solving Validation

## Critical: External Validation Requires API Key

**The current validation is PRELIMINARY because it's self-evaluation.**

To complete rigorous validation, you need to:
1. **ASK THE USER FOR AN API KEY** at the start of the session
2. Use it to call a separate Claude instance for truly blind evaluation
3. Present solutions without indicating which used protocols
4. Have the external instance score using the pre-defined rubric

The user can provide the key when asked. Don't try to do "blind" evaluation yourself - you generated both solutions and know which is which.

---

## Two Meta Folders

There are TWO Meta folders with relevant documentation:

### 1. `.claude/Meta/` (Main research folder)
Contains:
- `LOGIC_AND_REASONING_TECHNICAL_MANUAL.md` - **VALIDATED at 100%** (external blind eval, n=21)
- `VIRTUOSO_EXPERIMENT_DESIGN.md` - **VALIDATED** (d=5.2, 13 cycles)
- `PROBLEM_SOLVING_RIGOROUS_VALIDATION.md` - Current work, PRELIMINARY
- `MASTER_PROBLEM_SOLVING_METHODOLOGY.md` - v2.0 with honest caveats
- `EXPERIMENTAL_METHODOLOGY.md` - Standards for rigorous testing
- `UNIFIED_LLM_METHODOLOGY.md` - GOL framework
- `PROBLEM_SOLVING_AND_STRATEGY.md` - Original research (1200+ lines)

### 2. Check for additional `.claude/` subfolders
The user mentioned there may be another Meta-type folder with proven methodologies.

---

## What's Been Done

1. Created pre-registered validation with:
   - Hypothesis and falsification criteria
   - 5-dimension rubric (Completeness, Correctness, Depth, Practicality, Insight)
   - 6 strategy problems from established frameworks
   - Both baseline and protocol-guided solutions

2. Self-evaluated (limitation acknowledged):
   - Baseline: 31.7/50 (63%)
   - Protocol: 38.3/50 (77%)
   - Improvement: +6.7 pts (+13%)

3. Key finding: Effect varies by problem type
   - Wicked problems: +10 pts
   - Adversarial/systems: +7 pts
   - Clear-answer: +3 pts

---

## What's Needed

1. **External blind evaluation** (with API key from user)
2. Larger sample (n=30+ vs current n=6)
3. Integration of validated methodologies:
   - Logic/Reasoning protocols (100% validated)
   - Experiment design methodology (validated)
   - Recursive learning approach

---

## Protocols to Follow

From CLAUDE.md and validated research:

1. **Pre-register** hypothesis and falsification criteria BEFORE testing
2. **External evaluation** - don't self-evaluate
3. **Document weaknesses** honestly, don't just confirm hypothesis
4. **Task-technique matching** - protocols help more on some problem types
5. **n≥30** for proper validation (we're at n=6)

---

## User Feedback History

User correctly called out that initial "validation" was not rigorous:
- "youre just doing self testing and self verification and moving the goalpost"
- "not bringing to light true weaknesses so we can fix and patch"

This led to the rigorous restart with pre-registration and honest weakness documentation.

---

*Last updated: December 2024*
