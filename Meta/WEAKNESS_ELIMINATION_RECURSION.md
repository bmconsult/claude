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

**After 49 improvement cycles (hardened + external research):**
```
-1. CLASSIFY DOMAIN (Cynefin) [MUST DO FIRST]
    - Clear? → Apply known solution
    - Complicated? → Expert analysis
    - Complex? → Probe/sense/respond
    - Chaotic? → Act/sense/respond

0. DISCOVER (probe unknown unknowns)
   - "What hidden constraint would break ALL approaches?"
   - "What would a domain expert warn us about?"
   - IDEALITY CHECK: "Can this constraint disappear entirely?" (TRIZ)

1. VERIFY PROBLEM FRAME
   - "Is this the right QUESTION?"
   - "What if the problem IS the problem?"
   - Target LEVERAGE POINTS: paradigm > goals > rules > info flows (Meadows)

2. STATE problem clearly

3. LIST constraints
   - Check constraint consistency EARLY
   - Question assumed vs required constraints

4. GENERATE 3+ approaches with DISTINCT CAUSAL MECHANISMS
   - Each must assume different causal pathway
   - Include one that inverts baseline assumption
   - Check feasibility DURING generation
   - For NOVEL problems: prototype first, plan later (Design Thinking)

5. EVALUATE with weighted criteria (define, weight, score 1-5)

6. ADVERSARIAL RED-TEAM finalists
   - What's the obvious failure mode?
   - What would a skeptic attack?

6.5. FRAME-ADEQUACY CHECK
   - Do red-team failures reveal wrong problem frame?
   - If yes → return to step 2 to re-state problem

7. SELECT best (criteria + robustness)
   - Single recommendation, no hedging
   - Include zoom ±1 abstraction check

7.5. PROBE FRAME (surface frame errors early)
   - Build minimal prototype or thought experiment
   - Test core assumption of chosen approach
   - If frame breaks → return to step 4

8. DESIGN solution (with failure mitigations)
   - Strategy-problem match diagnostic
   - Include rollback procedure

9. VERIFY it works (including edge cases)
   - Staged deployment check
   - Dependency matrix for deployment order

10. INCUBATE if stuck (Wallas)
    - For complex/creative: MANDATORY rest phase
    - Insight often arrives after stepping away
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

### Step 3.5: Staged Deployment Check

```
Test this fix in a realistic deployment context (not isolated testing).

FIX: [what was fixed]

CHECK:
- Does it integrate with existing system without breakage?
- Do stakeholders/users accept it?
- Any unexpected side effects on adjacent capabilities?
- Would deployment order matter for this fix?
- Is there a safe rollback if needed?

Answer ONLY "DEPLOYABLE" or "NEEDS ADJUSTMENT".
```

**Tips:**
- This is NOT just technical verification - it's real-world fitness
- Integration testing catches fixes that work alone but break together
- Deploy-readiness is different from correctness

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
- Object level: 72/72 (100%) - research + simulation + teaching + organizing + practice
- Meta level: 3/3 (100%)
- Time: ~30 sec/cycle

## Action Mode Cycles (32-38)

After hitting action boundary at cycle 31, applied the insight: ACT don't investigate.

| Cycle | Weakness | Fix |
|-------|----------|-----|
| 32 | Frame check after generation (too late) | Move frame verification BEFORE generating |
| 33 | No backloop rule when red-team fails all | Decision tree: regenerate/reframe/abort (max 2 loops) |
| 34 | Constraint contradictions found too late | Early constraint consistency check |
| 35 | Wrong strategy type applied to problem | Strategy-problem match diagnostic |
| 36 | Hedging with options instead of committing | Single recommendation, no hedging |
| 37 | (Already covered by existing fixes) | - |
| 38 | Frame at wrong granularity level | Zoom ±1 abstraction check |

**Key learning:** Action mode works. 7 cycles in rapid succession, ~30 sec each.

---

## Deployment-Phase Cycles (39-44)

After adding staged deployment check, new weaknesses emerge:

| Cycle | Weakness | Fix |
|-------|----------|-----|
| 39 | No integration point between verify and deployment (staged check added) | Step 3.5: Staged Deployment Check |
| 40 | Fixes verified individually but no dependency tracking for deployment order | Dependency matrix: map which fixes must deploy before others |
| 41 | Acceptance criteria implicit, not explicit; stakeholder agreement is assumed not verified | Pre-define acceptance criteria WITH stakeholders before fix deployment |
| 42 | Side effects on adjacent capabilities only caught by user complaint post-deployment | Systematic impact analysis: list all systems affected by each fix |
| 43 | Failed deployment leaves no rollback specification in the fix itself | Each fix includes: revert procedure + data recovery + rollback trigger |
| 44 | No planned deprecation for dependent systems still expecting old behavior | Deprecation timeline: when old behavior support ends, affected systems notified |

**Key learning:** Deployment readiness requires systems thinking, not just fix correctness.

---

## External Research Breakthrough (Cycles 45-49)

At cycle 44, internal improvement hit ceiling. Applied user's suggestion: external research method.

**Method:** Search expert literature for gaps that internal analysis missed.

| Cycle | Source | Gap Found | Fix Added |
|-------|--------|-----------|-----------|
| 45 | Cynefin (Snowden) | No domain classification before method selection | **STEP -1: CLASSIFY DOMAIN** - Clear/Complicated/Complex/Chaotic? Different domains need fundamentally different approaches |
| 46 | TRIZ (Altshuller) | Optimize within constraints instead of eliminating them | **IDEALITY CHECK**: "Can this constraint disappear entirely?" before optimizing around it |
| 47 | Systems Thinking (Meadows) | Target parameters instead of leverage points | Target **info flows**, **feedback loops**, and **paradigm** - not surface parameters |
| 48 | Cognitive Science (Wallas) | Incubation treated as optional | **MANDATORY INCUBATION** for complex/creative problems - rest phase is productive |
| 49 | Design Thinking (IDEO) | Plan first, prototype later | For NOVEL problems: **PROTOTYPE FIRST**, plan after (learning by doing) |

### Domain Classification (Cynefin) - MUST DO FIRST

| Domain | Characteristics | Approach |
|--------|----------------|----------|
| **Clear** | Cause-effect obvious, best practice exists | Apply known solution |
| **Complicated** | Cause-effect knowable via analysis | Expert analysis → solution |
| **Complex** | Cause-effect only knowable in retrospect | Probe → sense → respond (experiments) |
| **Chaotic** | No cause-effect | Act → sense → respond (stabilize first) |

**Critical insight:** Applying "complicated" methods to "complex" problems GUARANTEES failure. Classify BEFORE selecting approach.

### TRIZ Ideality Principle

Before optimizing within a constraint, ask:
```
"What if this constraint didn't exist at all?"
"What's the IDEAL final result with zero cost?"
"Can we make the constraint solve itself?"
```

Most "constraints" are assumed, not required.

### Meadows Leverage Points (in order of power)

| Rank | Leverage Point | Example |
|------|----------------|---------|
| 1 | Paradigm | "What if we questioned this assumption?" |
| 2 | Goals | "Are we optimizing the right thing?" |
| 3 | Rules | "Can we change the rules?" |
| 4 | Information flows | "Who needs to know what?" |
| 5 | Feedback loops | "What's reinforcing the problem?" |
| 6-12 | Parameters | Adjusting numbers (least leverage) |

**Key insight:** Most problem-solving targets parameters (least powerful). Target paradigm/goals/rules instead.

### Wallas Incubation

The four stages of creative problem-solving:
1. **Preparation** - gather info, attempt solutions
2. **Incubation** - step away, do unrelated activity
3. **Illumination** - insight arrives unexpectedly
4. **Verification** - validate the insight

**Skipping incubation for complex/creative problems guarantees suboptimal solutions.**

### Design Thinking Prototyping

For NOVEL problems (never solved before):
```
Traditional: Define → Plan → Build → Test
Design Thinking: Build → Learn → Redefine → Repeat
```

**Prototyping reveals constraints that planning cannot anticipate.**

---

**Key learning:** External research reveals blind spots that internal recursion cannot find. When stuck, LOOK OUTSIDE.

---

## Simulation Testing Cycles (50-60)

After external research, used simulation method: apply strategy to hard problem, observe where it breaks.

| Cycle | Weakness Found | Fix Added |
|-------|----------------|-----------|
| 50 | No iteration loop for Complex domains (strategy is linear) | **Step 9.5: ITERATE** - Probe/sense/respond loop with exit criteria |
| 51 | No step to surface hidden stakeholder constraints | **Step 3.5: STAKEHOLDER RED-LINES** - What would veto this? Political/cultural constraints? |
| 52 | No deployment-space probing (what breaks at scale) | **Step 8.5: PROBE DEPLOYMENT SPACE** - Test at real scale/load/context |
| 53 | (Same as 52 - combined) | - |
| 54 | No stopping criteria (when to abandon, accept partial, detect spinning) | **Step 11: STOPPING CRITERIA** - Abandon after 3 failed iterations <5% progress; define minimum viable; spinning = same insight 2x |
| 55 | No frame articulation/communication to team | **Step 7.6: FRAME ARTICULATION** - Write: What does frame assume? Why right? What falsifies? Share with team |
| 56 | Solution doesn't persist after creator leaves | **Step 12: HANDOFF PROTOCOL** - Decision journal, constraint map, boundary documentation, failure modes |
| 57 | No audit of solver's unexamined mental models | **Step -2: META-FRAME AUDIT** - What mental models am I bringing? What would different domain notice? |
| 58 | No reframe protocol when problem is structurally unsolvable | **Step 6.6: IMPOSSIBILITY RESPONSE** - Collapse constraints OR reject goal OR partition subproblems |
| 59 | Stakeholder red-lines are point-in-time, not continuous | **Step 8.6: STAKEHOLDER CHECKPOINT** - Re-validate after design: "Does this still satisfy what you meant?" |
| 60 | Red-team lacks psychological safety | **Step 6 addendum: SAFETY PROTOCOL** - Separate idea from person, thank dissenters, safe to kill own ideas |

**Key learning:** Simulation reveals failure modes that pure analysis misses. Test the strategy on real problems.

---

## Complete Strategy (After 60 Cycles)

```
-2. META-FRAME AUDIT
    - What mental models am I bringing?
    - What would someone from radically different domain notice?
    - What am I taking as given that might be a choice?

-1. CLASSIFY DOMAIN (Cynefin) [MUST DO FIRST]
    - Clear? → Apply known solution
    - Complicated? → Expert analysis
    - Complex? → Probe/sense/respond
    - Chaotic? → Act/sense/respond

0. DISCOVER (probe unknown unknowns)
   - "What hidden constraint would break ALL approaches?"
   - IDEALITY CHECK: "Can this constraint disappear entirely?"

1. VERIFY PROBLEM FRAME
   - "Is this the right QUESTION?"
   - Target LEVERAGE POINTS: paradigm > goals > rules > info flows

2. STATE problem clearly

3. LIST constraints
   - Check constraint consistency EARLY
   - Question assumed vs required

3.5. STAKEHOLDER RED-LINES
    - What does each decision-maker require unstated?
    - What would veto this solution?

4. GENERATE 3+ approaches with DISTINCT CAUSAL MECHANISMS
   - For NOVEL problems: prototype first, plan later

5. EVALUATE with weighted criteria

6. ADVERSARIAL RED-TEAM (with SAFETY PROTOCOL)
   - Separate idea from person
   - Thank dissenters first
   - Make it safe to kill your own ideas

6.5. FRAME-ADEQUACY CHECK
   - Do red-team failures reveal wrong frame? → Return to step 1

6.6. IMPOSSIBILITY RESPONSE (if structurally unsolvable)
   - Option A: Return to VERIFY FRAME, collapse constraints
   - Option B: Reject goal, propose new success criteria
   - Option C: Partition into subproblems

7. SELECT best (single recommendation, no hedging)

7.5. PROBE FRAME
   - Minimal prototype or thought experiment
   - If frame breaks → return to step 4

7.6. FRAME ARTICULATION
   - Write: What does this frame assume? Why is it right? What would prove it wrong?
   - Share with team, get explicit acknowledgment

8. DESIGN solution (with failure mitigations)

8.5. PROBE DEPLOYMENT SPACE
   - What can't we know until this runs at actual scale?
   - What integration points have hidden failure modes?

8.6. STAKEHOLDER CHECKPOINT
   - Re-validate red-lines: "Now that you see the design, does this still satisfy what you meant?"

9. VERIFY it works (including edge cases)

9.5. ITERATE (for Complex domains)
   - PROBE: Test against actual domain
   - SENSE: What surprised you?
   - RESPOND: Adjust based on observation
   - EXIT: Solution stabilizes OR <5% improvement

10. INCUBATE if stuck (MANDATORY for complex/creative)

11. STOPPING CRITERIA
    - ABANDON: 3 failed iterations <5% progress → switch approach
    - PARTIAL: Define minimum viable, accept when reached
    - SPINNING: Same insight repeated 2x → incubate or switch

12. HANDOFF PROTOCOL
    - Decision journal: Why each choice over alternatives
    - Constraint map: Core vs nice-to-have
    - Boundary documentation: When solution stops being optimal
    - Failure modes: What degradation paths were explored
```

---

## Teaching & Organizing Cycles (61-66)

Used teaching method (explain to learner, note confusions) and organizing method (find inconsistencies).

| Cycle | Method | Issue Found | Fix |
|-------|--------|-------------|-----|
| 61 | Teaching | Frame loop unclear (when to exit vs keep reframing) | **FRAME LOOP RULE**: Max 2 frames. Exit when: path forward found, frames agree, or reframe quota used |
| 62 | Teaching | DISCOVER step vague (how to find unknown unknowns) | **IDEALITY CHECK PROTOCOL**: 6 questions (scope? stakeholders? constraints? success? reversible? asymmetries?) - if <4 YES, investigate |
| 63 | Teaching | Stuck/Iterate/Stop underspecified | **STUCK DIAGNOSTIC**: 5-level decision tree with iteration limit (max 1 reframe, then decompose/escalate) |
| 64 | Organizing | Redundant frame validation (4 overlapping steps) | Consolidate to 2: VERIFY FRAME (initial) + FRAME VALIDATION (post-selection) |
| 65 | Organizing | Order reversal (CLASSIFY before DISCOVER) | Swap: DISCOVER first, then CLASSIFY |
| 66 | Organizing | INCUBATE in wrong position (after VERIFY) | INCUBATE is CONDITIONAL (triggered when stuck >5 min at any step), not sequential |

**Key learning:** Teaching reveals unclear instructions. Organizing reveals structural issues. Both find different types of weaknesses.

---

## Practice Cycles (67-72)

Used practice method: actually execute strategy on real problem, note friction.

| Cycle | Friction Point | Fix |
|-------|----------------|-----|
| 67 | Stakeholder erasure - problem doesn't specify who commissioned it | **Step -3: STAKEHOLDER IDENTIFICATION** - Who commissioned this? What does success look like for them? If unknown, ASK |
| 68 | Domain misclassification - problem labeled wrong type | Add to CLASSIFY: Verify surface label matches actual type. If mismatch, propose reframe |
| 69 | Frame multiplicity - valid under multiple interpretations | **Step 1.5: FRAME DISAMBIGUATION** - If multiple valid frames, list explicitly and ASK which to optimize |
| 70 | Constraint opacity - missing operational constraints | **CONSTRAINT SUFFICIENCY CHECK** - If <3 operational constraints known, STOP and gather context |
| 71 | Unresolved stakeholder conflict - red-lines contradict | **Step 3.6: RED-LINE CONFLICT RESOLUTION** - Surface conflict, ask for priority ranking, or partition |
| 72 | Approach-stakeholder mismatch - each approach violates someone | Add to EVALUATE: Map approaches to stakeholders violated. If all violate critical stakeholders, escalate |

**Key learning:** Practice reveals context assumptions the strategy implicitly relies on. Real problems often arrive incomplete.

**Pattern discovered:** All fixes convert implicit erasure into explicit checking → decision/escalation.

**Validation: 72/72 cycles (100%)**

---

## Deep Recursion Insights (Cycles 11-31)

| Cycle | Insight |
|-------|---------|
| 11 | Unknown unknowns in SOLUTION space, not just problem |
| 12 | Threshold effects only appear at full scale |
| 13-14 | Understanding constraints ≠ overcoming them → method switch |
| 15-16 | Multiple constraints can make problem unsolvable as stated |
| 17-18 | Reframing can be denial, not progress |
| 21-22 | Some needs require FORMATION (becoming), not solving |
| 23-25 | Reversibility only knowable retrospectively |
| 26-27 | Lock-in can shift from legitimate to parasitic |
| 28-29 | You adapt to lock-in, corrupting self-evaluation |
| 30 | External calibrators may share your blindness |
| **31** | **ACTION BOUNDARY: Investigation → action → observation = ground truth** |

## The Action Boundary (Fundamental Limit)

At cycle 31, hit infinite regress: "Is my conclusion a blind spot?" can be asked forever.

**Resolution:** The regress dissolves through ACTION, not more investigation.

```
Investigation → more investigation → paralysis (infinite regress)
Investigation → ACTION → observation → ground truth (escape)
```

**Protocol:**
1. Investigate until you can specify what you'd do either way
2. Identify observable test to distinguish
3. COMMIT and execute
4. Results are ground truth

**Mantra:** "You cannot investigate your way to certainty. You act your way there."

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
