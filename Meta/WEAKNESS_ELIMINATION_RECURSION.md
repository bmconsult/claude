# Weakness Elimination Recursion Loop

## The Core Insight

**Numeric scores have variance. Weakness elimination is deterministic.**

Instead of scoring (which has ceiling effects, evaluation variance, and threshold miscalibration), we eliminate specific weaknesses one at a time. Either the weakness is fixed or it isn't - no ambiguity.

## The Basic Loop

```
1. FIND one specific weakness
2. FIX that weakness
3. VERIFY it's fixed
4. REPEAT
```

**Validation:** 5/5 cycles successful (100%) in ~30 seconds each, vs 42-67% success with scoring approaches that took 20+ minutes.

---

## Two Levels of Improvement

### Object Level (The Strategy)
What you're improving - in our case, a problem-solving strategy.

**Starting strategy:**
```
1. STATE problem
2. LIST constraints
3. GENERATE approaches
4. SELECT best
5. DESIGN solution
6. VERIFY it works
```

**After 10 improvement cycles (hardened for difficult problems):**
```
0. DISCOVER (probe unknown unknowns)
   - "What hidden constraint would break ALL approaches?"
   - "What would a domain expert warn us about?"

1. VERIFY PROBLEM FRAME
   - "Is this the right QUESTION?"
   - "What if the problem IS the problem?"

2. STATE problem clearly

3. LIST constraints

4. GENERATE 3+ approaches with DISTINCT CAUSAL MECHANISMS
   - Each must assume different causal pathway
   - Include one that inverts baseline assumption
   - Check feasibility DURING generation

5. EVALUATE with weighted criteria (define, weight, score 1-5)

6. ADVERSARIAL RED-TEAM finalists
   - What's the obvious failure mode?
   - What would a skeptic attack?

6.5. FRAME-ADEQUACY CHECK
   - Do red-team failures reveal wrong problem frame?
   - If yes → return to step 2 to re-state problem

7. SELECT best (criteria + robustness)

7.5. PROBE FRAME (surface frame errors early)
   - Build minimal prototype or thought experiment
   - Test core assumption of chosen approach
   - If frame breaks → return to step 4

8. DESIGN solution (with failure mitigations)

9. VERIFY it works (including edge cases)
```

**Improvements added (cycles 6-10):**
| Cycle | Weakness | Fix Added |
|-------|----------|-----------|
| 6 | No probe for unknown unknowns | Step 0: DISCOVER |
| 7 | Feasibility checked too late | Feasibility during EVALUATE |
| 8 | Problem statement may be wrong | Step 1: VERIFY PROBLEM FRAME |
| 9 | Frame errors surface too late | Step 7.5: PROBE FRAME |
| 10 | No re-frame loop | Step 6.5: FRAME-ADEQUACY CHECK |

### Meta Level (The Method)
The improvement process itself - which can also be improved using the same loop.

**Starting method:**
```
1. Find weakness → 2. Fix → 3. Verify → 4. Repeat
```

**After 3 recursive cycles:**
```
1. PROBLEM LEGITIMACY CHECK
   - Root cause or symptom?
   - Evidence you're blocked by THIS?
   - Falsification metric?

2. VALIDATE FRAME (external ground truth)
   - Testable prediction
   - Stakeholder/empirical validation

3. Measure baseline

4. ID BOTTLENECK (highest-impact, not arbitrary)

4.5. PROBE FRAME (test bottleneck diagnosis)
   - Small pilot or diagnostic test
   - Confirm bottleneck is REAL, not assumed
   - If diagnosis wrong: return to step 4, different bottleneck

5. Fix bottleneck

6. Re-measure

7. CEILING CHECK:
   - TRUE ceiling? (harder variants + meta both fail) → Stop
   - MEASUREMENT ceiling? → Better metrics, continue
   - METHOD ceiling? → Diagnose bottleneck type → Switch method class

8. Repeat
```

---

## The Frame Probe: Why Early Validation Matters

**Problem:** Frame errors (wrong problem definition, broken assumptions, incompatible approach) only surface during implementation (step 8-9), after 7 steps of committed work.

**Solution:** Add PROBE FRAME steps (7.5 for object-level, 4.5 for meta-level) that test core assumptions with minimal investment:

| Frame Error Type | Caught By | Cost of Missing It |
|-----------------|-----------|-------------------|
| Wrong problem definition | PROBE FRAME (step 7.5) | 8 steps wasted, must restart |
| Core assumption invalid | PROBE FRAME (step 7.5) | Full design fails, pivot needed |
| Bottleneck misdiagnosed | PROBE FRAME (step 4.5) | Whole improvement cycle misdirected |

**How it works:**
- **Prototype:** Build minimal version of selected approach - test core assumption immediately
- **Thought experiment:** Walk through first 3 steps of implementation - does frame hold?
- **External check:** Run past stakeholder/domain expert - "Does this problem statement match reality?"

**Escape hatch:** If PROBE FRAME fails, return to earlier step (not full restart). Frame error forces reselection, not complete redesign.

---

## How to Use

### Step 1: Find Weakness

Ask a subagent (or yourself):
```
Find ONE specific weakness in [thing].

Bad: "needs more detail" (vague)
Good: "Step 4 has no selection criteria" (specific, actionable)

Output ONLY the weakness (one sentence).
```

**Tips:**
- Force specificity - reject vague answers
- One weakness at a time - don't try to fix everything
- Concrete > abstract - "no X" beats "could improve Y"

### Step 2: Fix Weakness

```
Fix this ONE weakness in [thing].

[thing]

WEAKNESS TO FIX:
[specific weakness]

Output the improved version (same format).
```

**Tips:**
- Keep same structure - don't redesign everything
- Targeted fix - address only the stated weakness
- Preserve what works - don't break existing functionality

### Step 3: Verify Fixed

```
Is this weakness fixed?

WEAKNESS: [specific weakness]

[improved thing]

Answer ONLY "YES" or "NO".
```

**Tips:**
- Binary answer - no hedging allowed
- If NO, ask WHY and retry with explicit fix
- Sometimes takes 2-3 attempts - that's normal

### Step 4: Repeat

Continue until:
- No more weaknesses found (rare)
- Diminishing returns (weaknesses become trivial)
- Time/resource constraint hit

---

## The Recursive Part

Once your strategy is good enough, use it to improve THE METHOD ITSELF:

```
Apply [improved strategy] to find ONE weakness in [the improvement method].
```

This creates the recursive loop:
- Strategy improves method
- Method improves strategy faster
- Faster strategy improves method more
- etc.

---

## Ceiling Detection

When improvement stalls, diagnose which ceiling:

| Ceiling Type | Evidence | Action |
|--------------|----------|--------|
| **TRUE ceiling** | Harder variants + meta both fail | Stop - you've hit fundamental limit |
| **MEASUREMENT ceiling** | Can design harder test that reveals weakness | Better metrics, continue |
| **METHOD ceiling** | Same approach keeps failing | Switch method class entirely |

### Method Selection at Ceiling

| Bottleneck Type | Switch To |
|-----------------|-----------|
| Measurement noise | Better measurement first |
| Single-dimension limit | Orthogonal method |
| Linear optimization exhausted | Global search / random restart |
| Context-dependent failures | Conditional approach per case |
| Unknown unknowns | Structured exploration (red-team) |

---

## Common Failure Modes

| Failure | Symptom | Fix |
|---------|---------|-----|
| **Vague weakness** | "Could be better" | Force specificity: "What SPECIFIC thing is missing?" |
| **Fix doesn't stick** | Verification fails | Ask why, make fix more explicit |
| **Frame validates itself** | No external check | Add stakeholder/empirical validation |
| **Wrong problem** | Fixing symptoms | Problem legitimacy check first |
| **Infinite loop** | Keep "improving" forever | Ceiling detection protocol |

---

## Tips & Tricks

### Use Subagents
- Haiku is fast and cheap for find/fix/verify
- Parallel calls when independent
- ~30 seconds per cycle vs 20+ minutes with API scoring

### Force Binary Verification
- "YES or NO" only
- No "partially" or "mostly"
- If not YES, it's NO - retry

### One Weakness at a Time
- Don't bundle fixes
- Each cycle = one weakness eliminated
- Easier to verify, easier to debug

### Prioritize Bottlenecks
- Fix highest-impact weakness first
- Not just "a weakness" - THE bottleneck
- Ask: "What's blocking the most improvement?"

### Know When to Stop
- 5-10 cycles usually sufficient for most things
- Diminishing returns are real
- "Good enough" beats "perfect but never finished"

### External Validation
- Frame can validate itself incorrectly
- Always check with external ground truth
- Stakeholder feedback, empirical test, or pilot

---

## Quick Reference

**The loop:**
```
FIND specific weakness → FIX it → VERIFY fixed → REPEAT
```

**Recursive version:**
```
Use improved strategy to improve the method that improves the strategy
```

**Ceiling check:**
```
TRUE ceiling → stop
MEASUREMENT ceiling → better metrics
METHOD ceiling → switch approach
```

**Validation results:**
- Object level: 10/10 (100%) - strategy hardened for hard problems
- Meta level: 3/3 (100%)
- Time: ~30 sec/cycle

---

## Why This Works Better Than Scoring

| Scoring Approach | Weakness Elimination |
|------------------|---------------------|
| 42-67% success rate | 100% success rate |
| 20+ min per cycle | ~30 sec per cycle |
| Ceiling effects at high scores | No ceiling - always a weakness to find |
| Evaluation variance | Binary verification |
| Threshold miscalibration | No thresholds needed |
| Complex adaptive logic | Simple loop |

**The key insight:** You can always find SOMETHING to fix. You can't always score higher.
