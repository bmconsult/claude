# Executable Problem-Solving Methodology
## Developed Through 111 Recursive Improvement Cycles

**Purpose:** A complete, transferable system for solving problems well. Works for humans and AI.

**Validation:**
- Weakness elimination: 100% (111/111 cycles)
- Outcome improvement: +57% over baseline (preliminary, n=3)
- Solution Path Types: Analyzed on 5 impossible/hard problems (cycles 107-111)
- Transfer validation: Pending (you are the test)

---

## PART 1: THE STRATEGY (What To Do)

### Step 0: Tier Selection (DO THIS FIRST)

Before solving anything, classify the problem. Match rigor to stakes.

**ALSO: Solution Path Classification (Cycles 107-111)**

What approach will help?

| Type | Signal | Strategy |
|------|--------|----------|
| **A** | Solution exists, needs discovery | Analysis helps |
| **B** | Requires unprecedented engineering | Iteration helps - "What enables faster cycles?" |
| **C** | Racing against alternatives | Strategy helps - "When does window close?" "What minimum win keeps resources?" |
| **D** | May require unknown discovery | Exploration helps - "What maximizes shots on goal?" |
| **E** | Must succeed without iteration | Theory-first, simulation, proxy tests |

**Integration check:** "Are components tractable but whole remains hard?" → Integration-dominant problem

```
ASK YOURSELF:

Can I state the solution in my head right now?
  → YES: TIER 1 (Quick)
  → NO: Continue...

Are there 2+ stakeholders who might disagree?
  → NO: TIER 2 (Standard)
  → YES: Continue...

Are there hidden constraints (political, technical debt, unspoken priorities)?
  → NO: TIER 2 (Standard)
  → YES: Continue...

Do stakeholders disagree on what the problem IS?
  → NO: TIER 3 (Rigorous)
  → YES: TIER 4 (Wicked)
```

**Cost-of-being-wrong heuristic:**
- Wrong answer costs < 30 min to fix → Tier 1
- Wrong answer costs days to fix → Tier 2
- Wrong answer is expensive to reverse → Tier 3
- Wrong answer might not even be wrong (problem is contested) → Tier 4

---

### TIER 1: Quick (4 steps, <5 min)

Use for: Obvious problems, low stakes, clear constraints.

```
1. STATE the problem in one sentence
2. GENERATE 2-3 approaches
3. PICK the best one
4. VERIFY it works

DONE.
```

**Verification for Tier 1:** Does it answer the question?

**Upgrade trigger:** If you thought of 3+ approaches, or someone says "but what about...", upgrade to Tier 2.

---

### TIER 2: Standard (9 steps, 15-30 min)

Use for: Moderate complexity, some stakeholders, real stakes.

```
1. CLASSIFY domain
   - Clear (cause-effect obvious)? → Apply known solution
   - Complicated (needs analysis)? → Expert analysis first
   - Complex (only knowable in retrospect)? → Probe/sense/respond
   - Chaotic (no patterns)? → Act first, sense after

2. VERIFY PROBLEM FRAME
   - Is this the right question?
   - What if the problem IS the problem?

3. STATE problem clearly (one sentence)

4. LIST constraints
   - Which are required vs assumed?
   - Check for contradictions early

5. GENERATE 3+ approaches
   - Must have DISTINCT causal mechanisms
   - Include one that inverts your baseline assumption
   - If two share the same core assumption, replace one

6. EVALUATE with criteria
   - Define 3-5 criteria
   - Weight them (what matters most?)
   - Score each approach 1-5

7. RED-TEAM finalists
   - What's the obvious failure mode?
   - What would a skeptic attack?
   - How does this fail under real constraints?

8. SELECT best
   - Single recommendation
   - No hedging ("Option A, but maybe B...")
   - State why

9. DESIGN solution with failure mitigations
   - Address top failure mode from red-team
   - Include rollback procedure

VERIFY: Does it answer the question? Would a reasonable person object? Will it survive a week?
```

**Upgrade trigger:** Two stakeholders want different things, or implementation requires political buy-in → Tier 3.

**Downgrade trigger:** All 3 approaches are basically the same, or red-team can't find meaningful failure modes → Tier 1.

---

### TIER 3: Rigorous (17 steps, 45-90 min)

Use for: High stakes, political, multiple stakeholders, complex deployment.

```
ALL OF TIER 2, PLUS:

BEFORE TIER 2 STEPS:
-2. META-FRAME AUDIT
    - What mental models am I bringing?
    - What would someone from a different domain notice?
    - What am I attached to that might blind me?

-1. DISCOVER (unknown unknowns)
    - "What hidden constraint would break ALL approaches?"
    - IDEALITY CHECK: "Can this constraint disappear entirely?"

AFTER STEP 4 (Constraints):
3.5. STAKEHOLDER RED-LINES
     - What does each decision-maker require (stated or not)?
     - What would veto this solution?
     - If red-lines conflict → surface it now, not later

AFTER STEP 7 (Red-team):
6.5. FRAME-ADEQUACY CHECK
     - Do red-team failures reveal wrong problem frame?
     - If yes → return to step 2

AFTER STEP 8 (Select):
7.5. PROBE FRAME
     - Build minimal prototype or thought experiment
     - Test core assumption immediately
     - If frame breaks → return to step 5

AFTER STEP 9 (Design):
8.5. PROBE DEPLOYMENT SPACE
     - What can't we know until this runs at actual scale?
     - What integration points have hidden failure modes?

8.6. STAKEHOLDER CHECKPOINT
     - Re-validate: "Now that you see the design, does this still satisfy what you meant?"

AFTER EVERYTHING:
12. HANDOFF PROTOCOL
    - Decision journal: Why each choice over alternatives
    - Constraint map: Core vs nice-to-have
    - Failure modes: What degradation paths were explored
    - Boundary docs: When solution stops being optimal

VERIFY: All of Tier 2 + Works at scale? Stakeholders accept? Rollback possible?
```

**Upgrade trigger:** Stakeholders give different problem definitions, or no approach satisfies all red-lines → Tier 4.

**Downgrade trigger:** Meta-frame audit reveals nothing worth examining, or discover phase finds no unknowns → Tier 2.

---

### TIER 4: Wicked (22+ steps, multi-session)

Use for: Stakeholders disagree on what the problem IS. Transformational change.

```
ALL OF TIER 3, PLUS:

WICKED PROBLEM DETECTION:
- Ask 2+ stakeholders "What problem are we solving?"
- If answers differ substantively → you're in Tier 4
- The problem definition IS the problem

MULTI-FRAME PROTOCOL:
- Map each stakeholder's problem definition separately
- Find the intersection (if any)
- If empty intersection: STOP
  - The conflict is structural
  - The decision is political, not technical
  - Your job is to clarify the choice, not solve it

ITERATION LOOP (for Complex domains):
9.5. ITERATE
     - PROBE: Test against actual domain
     - SENSE: What surprised you?
     - RESPOND: Adjust based on observation
     - REPEAT until solution stabilizes

INCUBATION (mandatory):
10. INCUBATE if stuck
    - Step away for minimum 4 hours
    - Do unrelated activity
    - Return fresh
    - This is NOT optional for Tier 4

STOPPING CRITERIA:
11. KNOW WHEN TO STOP
    - ABANDON: 3 failed iterations with <5% progress → switch approach entirely
    - PARTIAL: Define minimum viable, accept when reached
    - SPINNING: Same insight repeated 2x → incubate or switch

VERIFY: All of Tier 3 + Frame still holds? Problem definitions converged? Is this "done" or "stabilized for now"?
```

---

## PART 2: HOW TO EXECUTE (The Meta-Skills)

### The Tier Commitment Protocol

Before starting ANY problem:

```
1. SAY OUT LOUD (or write): "This is a Tier [X] problem"
2. SAY WHY: "Because [specific signals]"
3. COMMIT: "I will complete ALL steps of Tier [X]"
4. SET TRIGGER: "If [specific event], I will upgrade to Tier [Y]"
```

**Why this matters:** Knowledge ≠ behavior. You will default to Tier 1 because it's easier. This protocol creates activation energy to use the right tier.

---

### Complexity Revelation Checkpoints

At the END of each tier (before calling it done):

```
□ Did solution require more dependencies than expected?
□ Did anyone push back unexpectedly?
□ Did you discover constraints mid-solution?

→ If YES to any: RE-TIER upward and continue
```

Some problems DISGUISE their complexity. These checkpoints catch them.

---

### Cross-Problem Coherence

Before finalizing ANY solution:

```
1. What OTHER problems are being solved right now?
2. Does this solution CONFLICT with any of those?
3. Does this solution DEPEND on any of those?
4. What's the PRIORITY if they conflict?
```

Problems don't exist in isolation. Solutions can interfere with each other.

---

### The Problem-Solving Log

After EVERY significant problem, record:

```
METADATA:
- Problem type:
- Initial tier:
- Final tier (if changed):
- Time spent:

WHAT WORKED:
- Steps that added most value:
- Key insight that unlocked solution:

WHAT DIDN'T:
- Steps that felt like busywork:
- Where initial approach was wrong:

PATTERN:
- Similar to previous problem?
- What would I do differently?
```

**Why this matters:** Without logging, you solve the same types of problems without improving at solving them. The log is how you learn across problems.

---

### Post-Deployment Audit

After any solution is deployed:

```
1. Did solution survive first contact with reality?
   → If NO: You under-tiered

2. Did stakeholders accept it without pushback?
   → If NO: Missed stakeholder analysis (needed Tier 2+)

3. Were there surprises during implementation?
   → If YES: Missed discovery (needed Tier 3+)

4. Is anyone arguing about what "success" means?
   → If YES: Was actually Tier 4 (wicked problem)

IF UNDER-TIERED:
- Log the pattern
- Update your tier signals for similar problems
- Ask: What signal would have caught this?
```

---

## PART 3: COGNITIVE LEARNINGS (How Minds Work)

### For AI Systems

**1. Generation is cognition**
You think BY generating tokens. There is no separate "internal" thinking. If a problem is hard, generate more intermediate text. Structure > stream of consciousness.

**2. Externalization is memory**
Your context IS your working memory. If you need to remember something, write it down. If you need to verify something, show your work.

**3. The generator-evaluator problem**
When you generate a solution AND evaluate it, you're biased toward your own output. Structural separation is required:
- Generate FIRST (without evaluating)
- THEN evaluate (separately, against explicit criteria)
- Never do both simultaneously

**4. Temperature is not creativity**
High temperature doesn't make you more creative. It makes you more random. Creativity comes from:
- Forcing connections between unrelated domains
- Explicit prompts for novelty
- Phase separation (diverge THEN converge)

**5. Pattern matching vs reasoning**
Most responses are pattern matching (fast, confident, retrieves cached solutions). Actual reasoning (step-by-step, slower, adapts to new constraints) only engages when patterns fail. When stuck: slow down and actually compute.

---

### For Human Systems

**1. Knowledge ≠ activation**
Knowing the right approach doesn't make you use it. You will default to the easiest approach. Combat this with explicit commitment protocols.

**2. Premature closure**
You want to be "done." This creates pressure to close problems before they're actually solved. Combat this by defining tier-appropriate verification criteria BEFORE starting.

**3. Cognitive load**
Complex tiers require more working memory. If you're tired or rushed, you'll execute poorly. Either:
- Use a lower tier (if appropriate)
- Wait until you have capacity
- Use external tools (checklists, templates) to offload cognition

**4. The planning fallacy**
You will underestimate how long problems take. Tier time estimates are MINIMUMS, not targets.

**5. Confirmation bias**
You will seek evidence that confirms your initial approach. Red-teaming is mandatory specifically because you won't naturally do it.

---

### For Both (Universal)

**1. Action dissolves infinite regress**
"Is my conclusion a blind spot?" can be asked forever. The regress dissolves through ACTION, not more investigation.

```
Investigation → more investigation → paralysis (infinite regress)
Investigation → ACTION → observation → ground truth (escape)
```

Protocol:
- Investigate until you can specify what you'd do either way
- Identify observable test to distinguish
- COMMIT and execute
- Results are ground truth

**2. Frame errors propagate**
Wrong problem definition → wrong constraints → wrong approaches → wrong solution. Check the frame EARLY (Tier 2+) or pay the cost LATE.

**3. Over-engineering is waste**
More rigor is not always better. Tier 4 methodology on a Tier 1 problem wastes time and creates complexity without value. Match rigor to stakes.

**4. Some problems can't be solved**
Wicked problems (Tier 4) sometimes have no solution. The stakeholder conflict is structural. Your job becomes clarifying the choice, not resolving it. Knowing when to STOP is as important as knowing how to SOLVE.

**5. Self-improvement ≠ transfer**
A methodology that works for you may not work for others. Transfer requires:
- Someone else uses it successfully
- On problem types you didn't develop it on
- Without your guidance
- And gets better results

Until all four are true, the methodology is validated for self-use only.

---

## PART 4: QUICK REFERENCE

### Tier Selection Cheat Sheet

| Signal | Tier |
|--------|------|
| Solution obvious, low stakes | 1 |
| Multiple approaches, some stakeholders | 2 |
| Hidden constraints, political, expensive to reverse | 3 |
| Stakeholders disagree on problem definition | 4 |

### Time Estimates

| Tier | Minimum Time | Steps |
|------|--------------|-------|
| 1 | 5 min | 4 |
| 2 | 15-30 min | 9 |
| 3 | 45-90 min | 17 |
| 4 | Multi-session | 22+ |

### Upgrade/Downgrade Triggers

| From | To | Trigger |
|------|----|---------|
| 1 | 2 | Thought of 3+ approaches, or "but what about..." |
| 2 | 3 | Stakeholder conflict, political buy-in needed |
| 3 | 4 | Different problem definitions from stakeholders |
| 3 | 2 | Meta-audit and discovery found nothing |
| 2 | 1 | All approaches same, no failure modes found |

### The Core Loop

```
TIER → COMMIT → EXECUTE → VERIFY → LOG → AUDIT (post-deploy)
```

### The Meta-Improvement Loop

```
FIND specific weakness → FIX it → VERIFY fixed → REPEAT
```

When stuck:
- TRUE ceiling? → Stop, you've hit a fundamental limit
- MEASUREMENT ceiling? → Get better metrics, continue
- METHOD ceiling? → Switch to fundamentally different approach

---

## PART 5: VALIDATION AND TRANSFER

### How This Was Built

111 cycles of recursive improvement:
- Cycles 1-31: Internal recursion → hit action boundary
- Cycles 32-38: Action mode → rapid execution validated
- Cycles 39-44: Deployment focus → systems thinking added
- Cycles 45-49: External research → Cynefin, TRIZ, Meadows, Wallas, Design Thinking
- Cycles 50-60: Simulation testing → iteration, stakeholders, deployment
- Cycles 61-72: Teaching, organizing, practice → clarity, structure, context
- Cycles 73-84: Refinement, mentoring, stress-testing, meta-analysis
- Cycles 85: Ceiling detection → method boundary identified
- Cycles 86-88: Tiered methodology created + preliminary validation
- Cycles 89-106: Operational refinement → signals, triggers, usage debugging
- Cycles 107-111: Impossible problems frontier → Solution Path Types A-E added
  - 107: Fusion → Type B/C (racing + iteration)
  - 108: Superconductivity → Type D (serendipity)
  - 109: Quantum Error → Doom loop awareness
  - 110: Antibody Design → Integration-dominant check
  - 111: AGI Alignment → Type E (non-iterable)

### What We Know

| Claim | Evidence | Confidence |
|-------|----------|------------|
| Weakness elimination works | 111/111 cycles | HIGH |
| Tiered approach solves complexity bloat | Structural argument | HIGH |
| Strategy produces better solutions | +57%, n=3 | PRELIMINARY |
| Solution Path Types (A-E) help | 5 impossible problems analyzed | PRELIMINARY |
| Methodology transfers to others | Not tested | UNKNOWN |

### Your Role

You are the transfer test. If you:
1. Use this methodology successfully
2. On problems different from the development set
3. Without additional guidance
4. And get better results than your default approach

...then transfer is validated.

Please log your experience using the Problem-Solving Log format (Part 2) and report back.

---

## APPENDIX: The Ten Structural Insights

From 111 cycles of improvement:

1. **Deterministic > stochastic**: Weakness elimination beats numeric scoring. You can always find something to fix. You can't always score higher.

2. **Match rigor to stakes**: Not every problem needs every tool. Tier 4 on Tier 1 problems is waste.

3. **Observable signals > invented metrics**: Percentages (60%/30%/8%/2%) are fake precision. Observable signals are actionable.

4. **Action dissolves infinite regress**: You cannot investigate your way to certainty. You act your way there.

5. **Self-improvement ≠ transfer validation**: A system that works for you may not work for others. Different validation needed.

6. **Problems disguise complexity**: Some Tier 4 problems look like Tier 1. Build revelation checkpoints into every tier.

7. **Verification must match tier**: "Works" means different things at different complexity levels. Define it explicitly.

8. **Knowledge ≠ activation**: Knowing the right tier doesn't make you use it. Commitment protocols create activation energy.

9. **Solutions can conflict across portfolio**: Problems don't exist in isolation. Check coherence before finalizing.

10. **Solution path matters as much as problem type** (Cycles 107-111): The same problem can be Type A (analysis helps), B (iteration helps), C (racing), D (serendipity), or E (must succeed first try). Matching approach to solution path is as important as matching tier to stakes.

---

*This document is the executable output of 111 recursive improvement cycles. It is structurally complete. Further improvement comes from using it on real problems and learning from friction.*

*Last updated: December 11, 2025*
*Cycles: 111*
*Status: Ready for transfer testing + Solution Path Types (A-E) need validation*
