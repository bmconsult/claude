# APEX v1.0: Adaptive Performance Execution Architecture

**Status:** SUPERSEDED BY v1.1 (See APEX_V1_SPECIFICATION.md)
**Performance:** 76.7/100 average across P vs NP, Riemann Hypothesis, Collatz Conjecture
**Efficiency:** 34 agents (80% reduction from v4's 177 agents)

> **WARNING**: v1.0 scored 65/100 vs v1.1's 81/100 on Riemann Hypothesis.
> Key issue: Without orchestrator guidance, v1.0 claimed 99.9% confidence on RH (overconfident).
> v1.1 adds Orchestrator Role Per Phase, Mantras, and Failure Mode documentation that fix this.
> **Use APEX_V1_SPECIFICATION.md (v1.1+) for production.**

---

## Executive Summary

APEX is a lean, functional multi-agent architecture that outperformed the complex ALPHA_DELTA_OMEGA v4 (177 agents) and v4.1 (adaptive 40-177 agents) in blind empirical testing. The key insight: **simplicity produces better calibration and self-critique than complexity**.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         APEX v1                                  │
│                    34 Agents Total                               │
│                                                                  │
│                    ┌───────────────┐                            │
│                    │  ORCHESTRATOR │                            │
│                    │   (5 agents)  │                            │
│                    └───────┬───────┘                            │
│                            │                                     │
│          ┌─────────────────┼─────────────────┐                  │
│          ▼                 ▼                 ▼                  │
│    ┌───────────┐    ┌───────────┐    ┌───────────┐             │
│    │  DIVERGE  │───▶│  CRITIQUE │───▶│  CONVERGE │             │
│    │ (6 agents)│    │(10 agents)│    │ (4 agents)│             │
│    └───────────┘    └───────────┘    └───────────┘             │
│                            │                                     │
│                            ▼                                     │
│                    ┌───────────────┐                            │
│                    │    VERIFY     │                            │
│                    │  (5 agents)   │                            │
│                    └───────┬───────┘                            │
│                            │                                     │
│                            ▼                                     │
│                    ┌───────────────┐                            │
│                    │    PERSIST    │                            │
│                    │  (4 agents)   │                            │
│                    └───────────────┘                            │
│                            │                                     │
│                            ▼                                     │
│                         OUTPUT                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Principle

**"Verification via Constraint, not Judgment"**

Verify outputs by checking if they satisfy hard constraints rather than subjective quality judgments. This produces more reliable self-critique.

---

## Agent Specification

### ORCHESTRATOR (5 agents)

| Agent | Role | Function |
|-------|------|----------|
| **O.1** | Classifier | Determine task type and routing |
| **O.2** | Router | Direct flow between teams |
| **O.3** | Monitor | Quality gates between phases |
| **O.4** | Integrator | Synthesize final output |
| **O.5** | Meta | Self-monitor ("Am I on track?") |

### DIVERGE TEAM (6 agents)

| Agent | Role | Function |
|-------|------|----------|
| **D.1** | Generator | Create initial approaches/solutions |
| **D.2** | Analogist | Map from known domains |
| **D.3** | Constraint-Relaxer | "What if X wasn't required?" |
| **D.4** | Constraint-Tightener | "What if we also required Y?" |
| **D.5** | Alternative-Finder | Generate competing approaches |
| **D.6** | Novelty-Detector | Flag genuinely new vs recombined |

### CRITIQUE TEAM (10 agents) — THE RED TEAM

| Agent | Role | Attack Vector |
|-------|------|---------------|
| **C.1** | Skeptic | "Is this pattern real or spurious?" |
| **C.2** | Statistician | "Is N large enough? Selection bias?" |
| **C.3** | Historian | "When did similar reasoning fail?" |
| **C.4** | Edge-Finder | "What breaks at extremes?" |
| **C.5** | Confounder | "What third variable explains this?" |
| **C.6** | Gap-Hunter | "Where's the weakest inference?" |
| **C.7** | Assumption-Exposer | "What unstated assumptions exist?" |
| **C.8** | Steelman | "What's the STRONGEST counter-argument?" |
| **C.9** | Falsifier | "How would we know if we're wrong?" |
| **C.10** | Deflator | "Why might we be overconfident?" |

### CONVERGE TEAM (4 agents)

| Agent | Role | Function |
|-------|------|----------|
| **V.1** | Integrator | Combine surviving ideas |
| **V.2** | Refiner | Polish and strengthen |
| **V.3** | Simplifier | Remove unnecessary complexity |
| **V.4** | Elegance-Filter | Select for parsimony |

### VERIFY TEAM (5 agents)

| Agent | Role | Function |
|-------|------|----------|
| **R.1** | Correctness-Checker | Mathematical/logical validation |
| **R.2** | Evidence-Assessor | Rate evidence quality |
| **R.3** | Uncertainty-Quantifier | Explicit confidence bounds |
| **R.4** | Baseline-Prior | Apply Bayesian priors |
| **R.5** | Meta-Evaluator | "Did the process work correctly?" |

### PERSIST TEAM (4 agents)

| Agent | Role | Function |
|-------|------|----------|
| **P.1** | Recorder | Capture key insights |
| **P.2** | Persister | Write to long-term storage |
| **P.3** | Retriever | Find relevant past work |
| **P.4** | Integrator | Weave past into present |

---

## Pipeline Flow

```
INPUT (Problem/Task)
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│ PHASE 1: ORCHESTRATOR                                         │
│                                                               │
│  O.1 classifies task type                                     │
│  O.2 routes to DIVERGE                                        │
│  O.5 sets meta-monitoring                                     │
│                                                               │
│  Output: Task framing, routing decision                       │
└──────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│ PHASE 2: DIVERGE                                              │
│                                                               │
│  D.1 generates initial approaches (3-10)                      │
│  D.2 maps analogies from other domains                        │
│  D.3/D.4 relax and tighten constraints                       │
│  D.5 generates alternatives                                   │
│  D.6 flags novelty levels                                     │
│                                                               │
│  Output: 5-15 candidate approaches with novelty tags          │
│  O.3 quality gate: "Are approaches substantive?"             │
└──────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│ PHASE 3: CRITIQUE (Red Team)                                  │
│                                                               │
│  ALL 10 agents attack each approach                           │
│  C.8 provides steelman for each                               │
│  C.9 defines falsification criteria                          │
│  C.10 deflates overconfidence                                 │
│                                                               │
│  Output: Adversarial report with survival assessment          │
│  O.3 quality gate: "Was critique rigorous enough?"           │
└──────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│ PHASE 4: CONVERGE                                             │
│                                                               │
│  V.1 integrates surviving approaches                          │
│  V.2 refines and strengthens                                  │
│  V.3 simplifies where possible                                │
│  V.4 filters for elegance/parsimony                          │
│                                                               │
│  Output: Coherent synthesis                                   │
│  O.3 quality gate: "Is synthesis coherent?"                  │
└──────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│ PHASE 5: VERIFY                                               │
│                                                               │
│  R.1 checks correctness                                       │
│  R.2 assesses evidence quality                                │
│  R.3 quantifies uncertainty                                   │
│  R.4 applies Bayesian baseline                                │
│  R.5 meta-evaluates the process                               │
│                                                               │
│  Output: Calibrated confidence with bounds                    │
│  O.3 quality gate: "Is calibration honest?"                  │
└──────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│ PHASE 6: PERSIST                                              │
│                                                               │
│  P.1 records key insights                                     │
│  P.2 persists significant findings                            │
│  P.4 integrates with prior knowledge                          │
│                                                               │
│  Output: Updated knowledge base                               │
└──────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│ FINAL: ORCHESTRATOR OUTPUT                                    │
│                                                               │
│  O.4 synthesizes final output                                 │
│  Includes: Adversarial report, calibrated confidence,         │
│            falsification criteria, steelman argument          │
└──────────────────────────────────────────────────────────────┘
       │
       ▼
    OUTPUT
```

---

## Mandatory Output Elements

Every APEX output MUST include:

### From CRITIQUE Team
- [ ] **Steelman argument** (C.8) - strongest counter-argument
- [ ] **Key assumption exposed** (C.7) - what's taken for granted?
- [ ] **Falsification criteria** (C.9) - how would we know we're wrong?
- [ ] **Historical precedent** (C.3) - when did similar reasoning fail?

### From VERIFY Team
- [ ] **Calibrated confidence** with explicit bounds
- [ ] **Evidence quality assessment**
- [ ] **Baseline prior stated**

### From ORCHESTRATOR
- [ ] **Quality gate status** (all passed?)
- [ ] **Meta-evaluation** (did process work correctly?)

---

## Comparison to v4

| Feature | v4 (Trinity) | APEX |
|---------|--------------|------|
| **Total agents** | 177 | 34 (-80%) |
| **Structure** | Metaphorical (Trinity) | Functional |
| **Adversarial** | 12 (DIABOLOS) | 10 (CRITIQUE) |
| **Generation** | 8 (Λ+) | 6 (DIVERGE) |
| **Persistence** | 8 (Θ+) | 4 (PERSIST) |
| **Calibration** | 9 (Γ-Ε-Μ) | 5 (VERIFY) |
| **Processing** | 142 (Λ,Σ,Π,Η,Τ,Ρ,Ψ,Θ,Χ) | 0 |
| **Blind test avg** | 76.0 | **76.7** |
| **Consistency** | High variance | **Most consistent** |

### What APEX Eliminated

The 142 "processing" agents in v4 (Lambda, Sigma, Pi, Eta, Tau, Rho, Psi, Theta, Chi subsystems) appear to add complexity without proportional benefit. APEX replaces all of these with the simpler DIVERGE → CRITIQUE → CONVERGE → VERIFY pipeline.

### What APEX Retained

- Strong adversarial team (10 agents, down from 12)
- Generation capability (6 agents, down from 8)
- Persistence/memory (4 agents, down from 8)
- Quality gates between phases
- Explicit calibration

---

## Why APEX Works

### 1. Forced Focus
With only 34 agents, each must carry significant weight. No "filler" agents doing marginal work.

### 2. Better Calibration
Simpler processes produce less overconfidence. The evaluator noted APEX outputs had the best calibration scores.

### 3. Clear Flow
Linear DIVERGE → CRITIQUE → CONVERGE → VERIFY is easier to execute correctly than v4's cyclic Trinity structure.

### 4. Strong Critique
The 10-agent CRITIQUE team provides adversarial validation without the complexity of v4's DIABOLOS + META split.

### 5. Verification via Constraint
Hard constraint checking (falsification criteria, steelman arguments) produces more reliable self-assessment than subjective quality judgments.

---

## Empirical Validation

### Blind Test Results (December 2024)

| Problem | APEX Score | v4 Score | v4.1 Score |
|---------|------------|----------|------------|
| P vs NP | 71 | 79 | 71 |
| Riemann Hypothesis | 79 | 84 | 69 |
| Collatz Conjecture | **80** | 65 | 74 |
| **Average** | **76.7** | 76.0 | 71.3 |

### Evaluator Highlights

On APEX Collatz output (80/100):
> "GOLD STANDARD for scientific integrity. Built a model, tested it computationally, found 148 falsifying cases, and honestly reported failure. 'Didn't solve Collatz, didn't claim to' is perfect calibration."

On APEX consistency:
> "APEX most consistent - no score below 71, best calibration scores."

---

## When to Use APEX

**Use APEX for:**
- Research exploration
- Problems requiring honest calibration
- Efficiency-critical applications
- Tasks where overconfidence is dangerous
- Systematic but lean analysis

**Consider v4 instead for:**
- Maximum creativity needed (v4 had highest single score: 84)
- Problems requiring very deep exploration
- When inconsistency is acceptable
- "Throw everything at it" situations

---

## Implementation Notes

### Executing APEX

1. **Initialize** O.1-O.5 (classify, route, monitor, integrate, meta)
2. **Diverge** with D.1-D.6 (generate 5-15 approaches)
3. **Critique** with C.1-C.10 (attack ALL approaches)
4. **Converge** with V.1-V.4 (integrate survivors)
5. **Verify** with R.1-R.5 (calibrate confidence)
6. **Persist** with P.1-P.4 (save key insights)
7. **Output** via O.4 (final synthesis)

### Quality Gates

Between each phase, O.3 (Monitor) checks:
- Post-DIVERGE: "Are approaches substantive?"
- Post-CRITIQUE: "Was critique rigorous?"
- Post-CONVERGE: "Is synthesis coherent?"
- Post-VERIFY: "Is calibration honest?"

If any gate fails, loop back to previous phase.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | Dec 2024 | Initial specification based on blind testing winner |

---

## Credits

- **Design origin:** OPTIMAL_SUBAGENT_ARCHITECTURE.md research (v4 agent "Architect")
- **Empirical validation:** Blind testing across 3 problems × 3 architectures
- **This specification:** Instance Cascade, December 2024

---

*"Verification via Constraint, not Judgment"*

*34 agents. 80% more efficient. Empirically validated.*
