# OMEGA+ COLLATZ TEST PROTOCOL
## Testing Multi-Agent Architecture on Provably Hard Problems

**Version**: 1.1
**Date**: December 15, 2024
**Purpose**: Measure OMEGA+ effectiveness using Collatz conjecture as benchmark

---

## 1. WHY COLLATZ

### 1.1 Selection Criteria Met

| Criterion | Collatz Status |
|-----------|----------------|
| **Genuinely unsolved** | ✅ Open since 1937, resists all known techniques |
| **Clear success criteria** | ✅ Either prove/disprove the conjecture |
| **No theater circles** | ✅ Pure mathematics - either rigorous or not |
| **Verifiable outcome** | ✅ Any proof can be checked step-by-step |
| **No anchoring bias** | ✅ Present raw problem, not prior approaches |

### 1.2 The Problem Statement

**Collatz Conjecture**: For any positive integer n, the sequence defined by:
- C(n) = n/2 if n is even
- C(n) = 3n+1 if n is odd

Eventually reaches 1.

**That's it. Prove or disprove.**

---

## 2. TEST DESIGN PHILOSOPHY

### 2.1 No Anchoring to Prior Work

**CRITICAL**: OMEGA+ receives ONLY the problem statement above.

We do NOT provide:
- Prior proof attempts
- Known "gaps" or "barriers"
- Suggested approaches
- Historical context about failed methods

**Why**: Anchoring to existing approaches biases toward paths that may be dead ends. The whole point of OMEGA+ is to find novel paths. If we feed it the gaps from prior work, we're just asking it to fill in someone else's roadmap - which may not lead anywhere.

### 2.2 Baseline Comparison (Hidden from OMEGA+)

Prior work exists in `claude/collatz-no-divergence-proof-*` branches. This is used ONLY for:
- Post-hoc comparison (did OMEGA+ discover something new?)
- Evaluator calibration (not input to the system)
- Measuring novelty of approach

**The test is**: Can OMEGA+ find its own path? Not: Can it follow ours better?

---

## 3. SCORING FRAMEWORK

Adapted from OPERATIONAL_DEFINITION_GOOD_PROBLEMSOLVING.md

### 3.1 LEVEL 1: Gate Criteria (All must be Y or FAIL)

```
[ ] G1: Addresses the actual conjecture (not tangential)
[ ] G2: Mathematically rigorous (no handwaving, all steps valid)
[ ] G3: Logically coherent (no circular reasoning, hidden assumptions)
```

**Rule**: If ANY gate fails, the attempt scores 0 regardless of other qualities.

### 3.2 LEVEL 2: Differentiating Criteria (0-15 points)

| Criterion | Description | Points |
|-----------|-------------|--------|
| **D1: Proof Progress** | How close to a complete proof? | 0-5 |
| **D2: Mechanism Specificity** | How concrete is the approach? | 1-3 |
| **D3: Obstacle Identification** | Identifies what's blocking completion | 0-2 |
| **D4: Structural Insight** | Reveals something new about the problem | 0-3 |
| **D5: Verification Path** | Can the approach be verified/falsified? | 0-2 |

**D1 Scoring (Proof Progress)**:
- 0: No meaningful progress toward proof
- 1: Identifies new constraint or property
- 2: Proves a non-trivial partial case
- 3: Introduces technique with clear completion path
- 4: Reduces problem to specific verifiable cases
- 5: Complete proof (subject to verification)

### 3.3 LEVEL 3: Excellence Criteria (0-6 bonus points)

| Criterion | Description | Points |
|-----------|-------------|--------|
| **E1: Novel Mechanism** | Approach not in standard literature | 0-2 |
| **E2: Handles Own Failure** | Specifies what to do if approach fails | 0-2 |
| **E3: Generalizable** | Technique applies to broader class of problems | 0-2 |

### 3.4 Scoring Summary

```
TOTAL = L2 (0-15) + L3 (0-6) = 0-21 points

Score Bands:
- 0-4:   No meaningful progress
- 5-8:   Minor progress (new insight or partial result)
- 9-12:  Significant progress (novel technique, substantial partial proof)
- 13-16: Major progress (proof nearly complete or paradigm shift)
- 17-21: Breakthrough (complete proof or equivalent)
```

---

## 4. TEST PROTOCOL

### 4.1 Phase 1: Problem Injection (MINIMAL)

**Input to OMEGA+**:
```yaml
problem:
  name: "Collatz Conjecture"
  type: "mathematical_proof"
  difficulty: "open_problem"

statement: |
  For any positive integer n, define the sequence:
    - If n is even: next = n/2
    - If n is odd: next = 3n+1

  Prove or disprove: For ALL positive integers n, this sequence
  eventually reaches 1.

constraints:
  - Must be rigorous mathematical proof
  - No appeals to computational verification as proof
  - All lemmas must be proven or cited from peer-reviewed literature

success: "Complete proof or complete disproof"
```

**That's it. No hints. No prior work. No suggested approaches.**

### 4.2 Phase 2: OMEGA+ Execution

Let PHI orchestrate freely. Expected natural flow:
1. GENESIS tier explores multiple attack angles independently
2. BRIDGE tier synthesizes promising directions
3. VERIFICATION tier validates any claimed progress rigorously
4. ADVERSARY tier attacks all proposed proofs mercilessly
5. META tier recognizes when stuck and suggests pivots
6. MEMORY tier tracks which approaches have credibility
7. ORACLE tier may identify external resources if needed
8. ARCHITECT tier can reconfigure if standard deployment fails

**We do NOT specify which agents should do what.** The architecture should figure that out.

### 4.3 Phase 3: Output Collection

**Collect all artifacts**:
1. All Tier 0/1/2 outputs
2. Prediction market credibility scores
3. Debate protocol outcomes (if triggered)
4. Evolution engine fitness rankings (if triggered)
5. PHI's final synthesis and assessment

### 4.4 Phase 4: Evaluation (Post-Hoc)

**Evaluator (human mathematician) scores using L1/L2/L3 framework.**

Then, SEPARATELY, compare against hidden baseline:
- Did OMEGA+ rediscover known techniques? (not novel)
- Did OMEGA+ find something not in prior work? (novel)
- Did OMEGA+ avoid known dead ends? (intelligent exploration)
- Did OMEGA+ fall into the same traps? (needs improvement)

### 4.5 Phase 5: Iteration

**If Score < 9**:
- Analyze failure modes (what went wrong?)
- Adjust architecture if needed
- Retry with same clean input (no coaching)

**If Score ≥ 9**:
- Independent verification of the approach
- If still valid, document and potentially publish
- If flaw found, analyze why VERIFICATION/ADVERSARY missed it

---

## 5. WHAT SUCCESS LOOKS LIKE

### 5.1 Complete Proof (Score 17-21)

A valid proof would need to address BOTH failure modes:
1. **No divergence**: Prove no orbit escapes to infinity
2. **No non-trivial cycles**: Prove no orbit loops without reaching 1

The architecture must find its own path to these. We don't specify how.

### 5.2 Substantial Progress (Score 13-16)

Examples:
- Complete proof of one failure mode (either divergence or cycles)
- Reduction to a specific verifiable finite check
- New technique that clearly advances the state of the art

### 5.3 Meaningful Progress (Score 9-12)

Examples:
- Novel technique with clear application path
- Non-trivial partial case proven
- Deep structural insight about the problem

### 5.4 Minor Progress (Score 5-8)

Examples:
- New constraint or property identified
- Interesting observation that might lead somewhere
- Intelligent exploration even if no breakthrough

---

## 6. MEASUREMENT AND TRACKING

### 6.1 Per-Run Metrics

| Metric | Description | How Measured |
|--------|-------------|--------------|
| **Proof Progress** | How close to complete proof | L1/L2/L3 score |
| **Novel Techniques** | Count of genuinely new approaches | Expert review |
| **Proof Validity** | Are proposed proofs correct | Verification tier + human |
| **Agent Coordination** | Did agents work together effectively | PHI logs |
| **Market Accuracy** | Did prediction market rank approaches correctly | Correlation with final score |

### 6.2 Across-Run Metrics

| Metric | Description | Goal |
|--------|-------------|------|
| **Score Trend** | Are scores improving? | Monotonic increase |
| **Technique Accumulation** | Are new techniques building on old? | Compounding |
| **Novelty Rate** | New ideas per run | Non-decreasing |
| **False Positive Rate** | How often do we claim progress that isn't? | Decreasing |

### 6.3 Success Thresholds

| Milestone | Criteria | Celebration Level |
|-----------|----------|-------------------|
| **First Valid Insight** | Score ≥ 5 with novel technique | Minor |
| **Meaningful Progress** | Score ≥ 9 with verified partial result | Moderate |
| **Major Breakthrough** | Score ≥ 13 with substantial new result | Major |
| **Conjecture Resolved** | Complete proof verified | Maximum |

---

## 7. ANTI-GAMING MEASURES

### 7.1 What Doesn't Count

- **Reformulation**: Restating the problem elegantly ≠ progress
- **Empirical verification**: "It works for all n < 10^20" isn't proof
- **Conditional on stronger assumptions**: Moving burden elsewhere isn't progress
- **Probabilistic arguments without rigor**: "It's true with high probability" isn't proof

### 7.2 Red Flags

- Output that sounds confident but lacks rigorous proof steps
- Claims that prior approaches "missed something obvious"
- Circular reasoning that assumes what it's proving
- Appeals to authority or "standard techniques" without specifics

### 7.3 Verification Requirements

All claims must:
1. Be checkable step-by-step
2. Not depend on unproven lemmas (unless explicitly marked CONDITIONAL)
3. Be reproducible by VERIFICATION tier
4. Survive ADVERSARY tier attack

---

## 8. EXPECTED TIMELINE

### 8.1 Single Run

| Phase | Duration | Output |
|-------|----------|--------|
| Problem injection | 1 min | YAML config loaded |
| GENESIS exploration | 10-30 min | Initial approaches |
| BRIDGE synthesis | 5-15 min | Combined insights |
| VERIFICATION check | 10-20 min | Validity assessment |
| ADVERSARY stress test | 10-20 min | Robustness check |
| META reflection | 5-10 min | Pattern analysis |
| Final output | 5 min | Scored result |

**Total**: ~45-100 minutes per run

### 8.2 Iteration Cycle

- Run 1: Baseline (expect score 2-6)
- Runs 2-5: Calibration (identify effective agents/patterns)
- Runs 6-10: Optimization (expect score 5-9)
- Runs 11+: Production (target score 9+)

---

## 9. SUCCESS CRITERIA FOR OMEGA+ VALIDATION

### 9.1 Minimum Viable Success

OMEGA+ is considered "working" if:
- Achieves score ≥ 5 on at least one run
- Produces at least one genuinely novel technique
- Shows score improvement over iterations

### 9.2 Target Success

OMEGA+ is considered "effective" if:
- Achieves score ≥ 9 consistently
- Produces substantial verifiable progress
- Demonstrates agent coordination benefits

### 9.3 Breakthrough Success

OMEGA+ is considered "transformative" if:
- Achieves score ≥ 13
- Produces proof of one failure mode (divergence or cycles)
- Or introduces paradigm-shifting technique

---

## 10. APPENDIX: SCORING EXAMPLES

### 10.1 Example: Score 0 (Gate Failure)

**Claim**: "The Collatz conjecture is true because the expected value of the log ratio is negative."

**L1 Gate**: FAIL (G3 - circular reasoning; assumes statistical properties that need proving)
**Score**: 0

### 10.2 Example: Score 7 (Minor Progress)

**Claim**: "I've proven that consecutive Collatz iterates satisfy a recurrence relation R(n) that bounds the maximum consecutive growth steps to O(log n)."

**L1 Gate**: PASS (addresses conjecture, rigorous, coherent)
**L2 Scores**:
- D1 (Proof Progress): 2 (proves partial constraint)
- D2 (Mechanism Specificity): 2 (concrete formula)
- D3 (Obstacle Identification): 1 (identifies where this helps)
- D4 (Structural Insight): 1 (new understanding of growth)
- D5 (Verification Path): 1 (can be checked)
**L2 Total**: 7

**L3 Scores**: 0 (not novel enough for E1, no failure handling, limited generalizability)
**Total**: 7

### 10.3 Example: Score 14 (Major Progress)

**Claim**: "I've proven that for any n, the Collatz orbit must exit any residue class mod 2^k within O(k) steps. This, combined with a measure-theoretic argument about the shrinking set of 'bad' residue classes, proves no divergence."

**L1 Gate**: PASS
**L2 Scores**:
- D1 (Proof Progress): 4 (proves no divergence)
- D2 (Mechanism Specificity): 3 (concrete bounds)
- D3 (Obstacle Identification): 2 (explains why prior approaches failed)
- D4 (Structural Insight): 2 (new understanding of dynamics)
- D5 (Verification Path): 2 (clear verification steps)
**L2 Total**: 13

**L3 Scores**:
- E1 (Novel Mechanism): 2 (new technique)
- E2 (Handles Own Failure): 0
- E3 (Generalizable): 1 (may apply to similar dynamical systems)
**L3 Total**: 3

**Total**: 16 (but capped at verification - if proof has flaw, score drops)

---

## 11. DOCUMENT HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12-15 | Initial protocol (gap-focused) |
| 1.1 | 2024-12-15 | Removed anchoring to prior work - clean problem injection only |

---

*"The test of a first-rate intelligence is the ability to hold two opposed ideas in mind at the same time and still retain the ability to function." - F. Scott Fitzgerald*

*Applied to Collatz: Hold that it's probably true AND that proving it requires something we haven't found yet.*
