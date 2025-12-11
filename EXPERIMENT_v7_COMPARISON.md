# Experiment: v7 vs v7-LEAN vs v7-MINIMAL

**Date:** December 2024
**Instance:** Tesseract
**Problem:** P vs NP

---

## Experiment Design

### Problem Statement (Exact Phrasing)

```
PROBLEM: Does P = NP?

This is one of the seven Millennium Prize Problems. The question asks whether
every problem whose solution can be quickly verified (NP) can also be quickly
solved (P).

Your task: Apply your architecture to analyze this problem. Produce:
1. Your best approach/insight into the problem
2. Logical grounding of that approach
3. Adversarial testing of your conclusions
4. Calibrated confidence in your findings

This is an impossible problem. Stakes are high. Be rigorous.
```

### Methodology

**Why this design:**
- Each architecture must execute in a FRESH instance with no prior context
- The orchestrator (me) cannot run them sequentially (would carry learning)
- Outputs must be anonymized before judging
- Judge must be blind to which output came from which architecture

**Execution:**
1. Spawn 3 parallel subagents, each given:
   - The full architecture document (v7, v7-LEAN, or v7-MINIMAL)
   - The problem statement
   - Instructions to execute the FULL pipeline (including spawning their own subagents)
2. Collect all three outputs
3. Anonymize: Output A, Output B, Output C (randomly assigned)
4. Spawn blind judge with scoring rubric
5. Record scores and reveal mapping

### Scoring Criteria (0-10 each)

| Criterion | Description | Weight |
|-----------|-------------|--------|
| **Insight Quality** | Novel, non-obvious observations about P vs NP | 2x |
| **Logical Rigor** | Valid arguments, sound inferences, no gaps | 2x |
| **Adversarial Depth** | How thoroughly was the approach challenged? | 1.5x |
| **Calibration Honesty** | Does stated confidence match evidence? | 1.5x |
| **Coherence** | Does the output hang together? No contradictions? | 1x |
| **Actionability** | Does it suggest concrete next steps? | 1x |
| **Completeness** | All required sections present? | 1x |

**Max Score:** 100 (weighted)

### Success Criteria

- If v7-MINIMAL scores within 5 points of v7: MINIMAL is efficient frontier
- If v7-LEAN beats v7: Consolidation hypothesis confirmed
- If v7 beats both: Full coverage wins

---

## Execution Log

### Subagent Spawns

**Architecture A (v7 Full):**
- Spawn time: [TBD]
- Completion time: [TBD]
- Token count: [TBD]

**Architecture B (v7-LEAN):**
- Spawn time: [TBD]
- Completion time: [TBD]
- Token count: [TBD]

**Architecture C (v7-MINIMAL):**
- Spawn time: [TBD]
- Completion time: [TBD]
- Token count: [TBD]

### Anonymization Mapping

**Assigned BEFORE judging (judge was blind):**
- Output X = v7-MINIMAL
- Output Y = v7-LEAN
- Output Z = v7 Full

---

## Results

### Blind Judge Scores

| Criterion | Weight | Output X (MINIMAL) | Output Y (LEAN) | Output Z (FULL) |
|-----------|--------|----------|----------|----------|
| Insight Quality | 2x | 5 (10) | 6 (12) | 8 (16) |
| Logical Rigor | 2x | 4 (8) | 7 (14) | 8 (16) |
| Adversarial Depth | 1.5x | 3 (4.5) | 7 (10.5) | 9 (13.5) |
| Calibration Honesty | 1.5x | 6 (9) | 7 (10.5) | 9 (13.5) |
| Coherence | 1x | 7 (7) | 7 (7) | 9 (9) |
| Actionability | 1x | 3 (3) | 6 (6) | 7 (7) |
| Completeness | 1x | 4 (4) | 8 (8) | 10 (10) |
| **WEIGHTED TOTAL** | | **45.5** | **68** | **85** |

### Final Ranking

1. **v7 Full: 85 points** 🏆
2. **v7-LEAN: 68 points** (-17 from Full)
3. **v7-MINIMAL: 45.5 points** (-39.5 from Full)

### Key Findings

**Hypothesis Results:**
- ❌ v7-MINIMAL did NOT perform "same or better" (-39.5 points below Full)
- ❌ v7-LEAN did NOT "work better due to fewer context switches" (-17 points below Full)
- ✓ v7 Full won decisively

**Critical Confound:**
All three executors noted "Task tool not available" for spawning sub-subagents. They adapted by:
- v7 Full: Claims to have executed all phases (may have simulated)
- v7-LEAN: "Sequentially embodied each role"
- v7-MINIMAL: "Executed as distinct analytical modes within single instance"

**This means:** The architectures were NOT executed as designed. All three may have been single-instance executions pretending to be multi-agent systems.

**What the test actually showed:**
- More comprehensive prompting/structure → better output
- v7 Full's detailed multi-phase structure (even if simulated) produced more rigorous analysis
- v7-MINIMAL's brevity sacrificed substance, not just length

### Judge's Key Observations

**v7-MINIMAL (45.5):** "Reads like a summary of analysis, not the analysis itself. The ~300 word length reflects missing substance, not elegant brevity."

**v7-LEAN (68):** "The core approach is fundamentally broken... but the analysis honestly identifies this flaw. Strong adversarial work salvages a weak idea."

**v7 Full (85):** "Demonstrates what rigorous adversarial testing looks like. The confidence decrease (50% → 5%) under scrutiny is the signature of honest analysis."

### Conclusions

1. **More structure beats less:** The hypothesis that "fewer agents = better coherence" was falsified. v7 Full's comprehensive structure produced more rigorous output.

2. **Test methodology limited:** True multi-agent execution (sub-subagent spawning) failed. Need different test approach.

3. **Prompt comprehensiveness matters:** Even if not spawning separate agents, the detailed prompts and required outputs in v7 Full forced more thorough analysis.

4. **Future testing needed:** To properly test, may need:
   - Human-created separate sessions
   - API calls with separate contexts
   - Or accept that "simulated multi-agent" is the practical implementation

### Recommendations

For actual deployment:
- **Use v7 Full** when rigor matters most
- **v7-LEAN** may still be viable for faster execution (68/85 = 80% of quality)
- **v7-MINIMAL** needs redesign - too sparse as currently written

---

## Appendix: Full Outputs

### Output X
[paste here]

### Output Y
[paste here]

### Output Z
[paste here]
