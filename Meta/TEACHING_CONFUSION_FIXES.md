# Teaching Confusion Fixes - Problem-Solving Methodology v4.0

**Status**: Operational clarifications for three specific teaching confusions

**Purpose**: Add to STEP 0, STEP 1, and Meta-Rule sections of v4.0 methodology documentation

---

## FIX 61: Frame Revisiting Loop - Clear Exit Conditions and Cycling Logic

**Confusion**: "Frame revisiting loop is unclear - when to exit vs loop back, whether probing/articulating happens once or continuously"

### The Problem

Current text says: "If stuck at any point → you're solving the wrong problem → return to Step 0"

But this creates ambiguity:
- How many times can you revisit the frame?
- When do you STOP reframing and accept "this IS the right frame"?
- Is step 0 a one-time activity or continuous?
- How do you know reframing will help vs. just spinning?

### The Operational Fix

**ADD THIS DECISION LOGIC TO THE META-RULE SECTION:**

```
THE FRAME REVISITING LOOP (Operational Protocol)

RULE: STEP 0 (Frame) happens twice:
  - ONCE at the start (mandatory)
  - ONCE if stuck (conditional)

INITIAL FRAME (First Pass):
1. State what type of problem this is
2. Note which tools apply (Assumption Audit is ALWAYS applied)
3. Optional: Note if you're uncertain about classification
   [If uncertain, apply tools anyway - they'll clarify]

STUCK DETECTION (Triggers reframing):
You are stuck if:
  □ You've applied all relevant tools AND
  □ No clear path forward exists AND
  □ You've spent >2 minutes without progress

NOT stuck if:
  □ You're still discovering new constraints (keep going)
  □ The problem is genuinely complex (complexity ≠ stuck)
  □ You found blockers but haven't traced 3+ levels deep yet

REFRAME DECISION (When stuck):
1. Go back to STEP 0
2. Ask: "What if I classified this wrong?"
3. Try ONE different classification
   - If was Analytical → try Systems or Wicked
   - If was Systems → try Adversarial or Wicked
   - If was Adversarial → try Systems or Wicked
   - If was Wicked → break into subproblems (each with its own frame)
4. Apply relevant tools under NEW classification
5. STOP REFRAMING after this second pass

EXIT REFRAMING WHEN:
  ✓ The new frame reveals the path forward (use it)
  ✓ Both frames suggest same solution (original frame was fine)
  ✓ Problem decomposes into smaller subproblems (frame each separately)
  ✓ You've reframed once already and still stuck (problem may be ill-defined - escalate or accept ambiguity)

CONTINUOUS vs ONCE:
- STEP 0 framing: Happens exactly twice (initial + one reframe maximum)
- Tool application (Steps 1-4): Continuous until solution found
- Verification (Step 4): Happens at end, not continuously
```

### Implementation Note

The frame is NOT continuously revisited. Think of it as:

```
Frame once → Apply tools (1-4) → Stuck? → Reframe once → Apply tools again

              ↓ if stuck again

         Accept current understanding
         and solve under ambiguity OR
         escalate problem as ill-defined
```

---

## FIX 62: STEP 0 (FRAME) - Operational Protocol for Finding Unknown Unknowns and IDEALITY CHECK

**Confusion**: "Step 0 (FRAME) is operationally vague - HOW to find unknown unknowns, what IDEALITY CHECK concretely means"

### The Problem

Current STEP 0 text says: "What type of problem is this? [list types]"

But practitioners ask:
- How do I KNOW what type it is? I might be blind to something.
- What's an "IDEALITY CHECK"? (This term wasn't even in the current docs)
- How do I surface assumptions about the problem FRAME itself, not just the problem?
- What unknown unknowns am I missing about how I'm classifying this?

### The Operational Fix

**REPLACE STEP 0 WITH THIS EXPANDED PROTOCOL:**

```
STEP 0: FRAME THE PROBLEM (Operational Protocol)

PART A: INITIAL CLASSIFICATION (2 minutes)

1. State your problem statement in one sentence
   Example: "We need to decide whether to hire for this role"

2. Ask: "What type IS this?"
   □ Analytical: Clear constraints, decomposable, one answer
   □ Systems: Feedback loops, dynamics, delays, interdependencies
   □ Adversarial: Other agents who respond to your moves
   □ Wicked: Multiple stakeholders, value conflicts, no single answer
   □ Hybrid: Multiple of the above

3. State your classification
   Example: "Hiring decision is Analytical (clear criteria) + Wicked (culture fit)"

---

PART B: IDEALITY CHECK - Finding Unknowns About Your Frame (2-3 minutes)

Purpose: Surface what you don't know about the problem ITSELF

For EACH of these questions, answer YES/NO:

1. SCOPE UNCERTAINTY
   "Do I know what decisions fall within THIS problem vs outside?"
   □ YES - scope is clear
   □ NO - answer: What would happen if scope changed?

2. STAKEHOLDER AWARENESS
   "Have I identified ALL people affected by this decision?"
   □ YES - complete list
   □ NO - who might I be missing? (hidden stakeholders, future users, external parties)

3. CONSTRAINT VISIBILITY
   "Do I know ALL hard constraints (budget, time, legal, technical)?"
   □ YES - complete list
   □ NO - what if a major constraint emerges later?

4. SUCCESS DEFINITION
   "Can I define what 'right answer' looks like?"
   □ YES - success metrics clear
   □ NO - answer: Who decides if this is right? (If no clear answer → Wicked)

5. REVERSIBILITY
   "Can this decision be undone, or is it irreversible?"
   □ REVERSIBLE - Can test, iterate, change later
   □ IRREVERSIBLE - Demands high confidence, may need Tier 3
   □ PARTIALLY - Some aspects reversible, some not

6. HIDDEN ASYMMETRIES
   "Are there obvious imbalances in information, power, or stakes?"
   □ YES - who has more information/power/at stake?
   □ NO - double-check: am I blind to asymmetries?

SCORING THE IDEALITY CHECK:
- If ≥ 4 answered YES → Your frame is well-formed. Proceed.
- If < 4 answered YES → You have unknown unknowns. Before applying tools:

  FOR EACH NO ANSWER:
  1. Investigate for 1-2 minutes
  2. Either: Resolve the uncertainty OR
  3. Accept uncertainty and note it explicitly
  4. This becomes an assumption for Step 1

Example: "Success Definition is unclear. Assumption: CEO's preference = success."

---

PART C: UNKNOWN UNKNOWNS PROTOCOL (If Ideality Check score < 4)

These are things you don't know you don't know:

1. INVERSION TEST
   Ask: "If I was completely wrong about this problem's type, what would I miss?"
   - If Analytical but actually Wicked → Missing stakeholder complexity
   - If Systems but actually Adversarial → Missing response dynamics
   - If Adversarial but actually Systems → Missing feedback loops

   Write: "If I'm wrong about [type], the consequence would be..."

2. CONSTRAINT SHADOW TEST
   Ask: "What constraint, if I discovered it tomorrow, would change everything?"

   Examples that surprise people:
   - Hidden legal/regulatory requirement
   - Stakeholder with veto power
   - Technical impossibility discovered during implementation
   - Funding cut mid-project
   - Key person leaving

   Write 2-3: "If [constraint] emerged, we'd have to..."

3. TIME HORIZON TEST
   Ask: "What time horizon matters here?"
   - Next day decision? (Different than next year)
   - Is this urgent or can it wait? (Changes leverage)
   - Does urgency match problem type? (Wicked problems under pressure get worse)

4. REVERSIBILITY TEST (Above in #5, but deepen it)
   Ask: "If this goes wrong, what's our backup?"
   - No backup → Wicked problem, needs deliberation
   - Backup exists → Analytical problem, can move faster
   - Partial backup → Hybrid, manage the non-reversible parts carefully

STOP IDEALITY CHECK WHEN:
  ✓ You've scored ≥ 4 on certainty
  ✓ You've identified 2-3 major unknowns and documented them
  ✓ You've reframed at least once (if the checks revealed misclassification)
```

### Ideality Check - Quick Reference

Use this table to quickly assess frame quality:

| Check | Green (Clear) | Yellow (Unclear) | Red (Unknown) |
|-------|---------------|-----------------|---------------|
| Scope | Boundaries explicit | Fuzzy edges | Don't know where edge is |
| Stakeholders | Complete list | Missing some | Don't know who matters |
| Constraints | All hard constraints stated | Some soft constraints | Don't know what limits exist |
| Success | Metrics defined | Vague | Who decides if right? |
| Reversibility | Clear if reversible | Partially clear | Unclear what sticks |
| Asymmetries | Visible imbalances | Some hidden | Completely blind |

**If ≥ 3 are Yellow/Red: Spend 2-3 minutes investigating before moving to Step 1.**

---

## FIX 63: Stuck/Iterate/Stop Decision Tree - Concrete Logic for Loop Management

**Confusion**: "Stuck/Iterate/Stop decision point is underspecified - need decision logic, not just concepts"

### The Problem

Current methodology says: "If stuck → return to Step 0"

But this creates confusion:
- What IS "stuck"? (ambiguous)
- How do I know which action to take: Reframe? Try different tool? Escalate? Stop?
- How many times can I iterate?
- When do I accept "I can't solve this"?

### The Operational Fix

**ADD THIS DECISION TREE TO METHODOLOGY:**

```
STUCK/ITERATE/STOP DECISION TREE (Operational)

TRIGGER: "I don't know what to do next"

├─ LEVEL 1: DIAGNOSE THE STUCK STATE (1 minute)
│
├─ Question 1: "Have I finished all mandatory steps?"
│  │
│  ├─ NO → "I haven't finished Steps 1-4 yet"
│  │   └─ ACTION: Pick up where you stopped. You're not stuck; you're in progress.
│  │
│  └─ YES → Continue to Question 2
│
├─ Question 2: "Am I stuck because I'm finding new information?"
│  │
│  ├─ YES → "New constraints/stakeholders/details keep appearing"
│  │   └─ ACTION: Keep going. This is discovery, not stuck.
│  │       Add new info to assumptions, keep applying tools.
│  │
│  └─ NO → Continue to Question 3
│
├─ Question 3: "Have I applied ALL relevant tools for my frame?"
│  │
│  ├─ NO → "I know a tool applies but haven't used it yet"
│  │   │   (Example: This is adversarial but I haven't traced responses)
│  │   └─ ACTION: Apply missing tool. You're not stuck; you're incomplete.
│  │
│  └─ YES → Continue to Question 4
│
├─ Question 4: "Do I have a solution that passes Step 4 verification?"
│  │
│  ├─ YES → "I have an answer that meets constraints"
│  │   └─ ACTION: STOP. You're done. (See EXIT CRITERIA below)
│  │
│  └─ NO → Continue to Question 5
│
└─ Question 5: "Have I applied tools but found no path forward?"
   │
   ├─ YES → TRULY STUCK (Problem classification may be wrong)
   │
   └─ NO → Go back to Question 1 (you're in a loop, check what's missing)

---

LEVEL 2: IF TRULY STUCK (All tools applied, no forward path)

Decision: REFRAME or ESCALATE?

Ask: "What would change if I reclassified this problem?"

┌─ REFRAME PATH (Problem type might be wrong)
│
├─ Condition: You're confident tools were applied correctly
│           AND You notice the problem resists your classification
│           (Example: "This looks analytical but resists decomposition")
│
└─ Action: Try ONE different classification
   - Apply tools for NEW type
   - If it opens a path → Use new frame
   - If it still stuck → Proceed to ESCALATE PATH

┌─ ESCALATE PATH (Problem is well-classified but intractable)
│
├─ Condition: Multiple frames suggest same stuck conclusion
│           OR Problem may be fundamentally unsolvable under constraints
│
└─ Actions: (Choose ONE)
   □ Relax a constraint (is there flexibility?)
   □ Decompose (break into smaller, solvable subproblems)
   □ Reframe as Wicked + convene stakeholders (decision requires consensus)
   □ Gather more information (what data would unstick this?)
   □ Accept decision under uncertainty (proceed anyway, manage risks)

---

LEVEL 3: ITERATION LIMITS

Question: "How many times can I loop?"

ANSWER:

| Loop Iteration | Action | When to Stop |
|---|---|---|
| 0 (Initial) | Frame once, apply tools | Standard path |
| 1 (Reframe) | Reclassify once, apply tools to new frame | After first stuck diagnosis |
| 2+ (Multi-reframe) | STOP. Looping suggests: |  |
| | □ Problem is actually Wicked (needs stakeholder input, not more analysis) | |
| | □ Problem is unsolvable (constraints are contradictory) | |
| | □ Problem statement is wrong (reframe the META-problem) | |

```
IF you've reframed more than once:
  STOP REFRAMING
  CHOOSE ONE ACTION:
  - Accept ambiguity and solve under it
  - Escalate for human decision
  - Decompose into clearer subproblems
```

---

LEVEL 4: EXIT CRITERIA (When to STOP)

You've solved the problem when:

NECESSARY CONDITIONS (All must be true):
  □ Solution passes Step 4 verification (constraints, answers question)
  □ You've stated confidence level explicitly
  □ You've identified what could make it wrong

OPTIONAL CONDITIONS (At least one should be true):
  □ Solution is reversible (can change later if wrong)
  □ Confidence is HIGH (you're certain)
  □ Cost of deciding now < cost of waiting for more info
  □ Sufficient time/resources to implement

STOP CONDITIONS (Can exit with confidence limits):
  ✓ Solution is GOOD ENOUGH for confidence level + time constraints
  ✓ Further analysis has diminishing returns
  ✓ Decision deadline is near
  ✓ You have a reversible path (test and iterate)

DON'T STOP IF:
  ✗ You haven't verified against constraints
  ✗ Confidence is unknown (you said "probably" but didn't quantify)
  ✗ Problem might be Wicked but treated as Analytical
  ✗ A critical stakeholder hasn't been consulted (if multi-stakeholder problem)

---

FULL DECISION TREE (Compact Version)

                    "I'm Stuck"
                         │
                    ┌────┴────┐
                    │          │
          Have you finished  Have you applied
          Steps 1-4?         all relevant tools?
             │                  │
            NO                 NO
             │                  │
          Continue            Apply tools
          working              then reassess
             │                  │
             └────┬─────────────┘
                  │
                 YES (All steps done, all tools used, still stuck)
                  │
        ┌─────────┴──────────┐
        │                    │
   REFRAME               ESCALATE
   (Try new type)    (Change constraints
   │                  or decompose)
   │
   └─ Still stuck? → ACCEPT AMBIGUITY
                     + choose action
                     + or escalate
                     + or decompose

---

STUCK/ITERATE/STOP - Checklist Form

WHEN YOU SAY "I'M STUCK":

□ Step 1: Check if you've actually completed mandatory steps
□ Step 2: Check if new information is emerging (not stuck, discovering)
□ Step 3: Check if you've applied ALL tools for your frame
□ Step 4: Check if you have a solution at all
□ Step 5: If all above YES and still no path → TRULY STUCK

IF TRULY STUCK:
□ Try reframing ONCE (different problem type)
□ If that fails, ESCALATE (don't loop more than twice)

WHEN TO STOP:
□ Verification passes (Step 4)
□ Confidence stated (high/medium/low)
□ Known unknowns documented
□ Decision deadline or diminishing returns reached
```

---

## Integration Instructions

### Where to Add These Fixes

1. **FIX 61** → Add to "META-RULE" section of v4.0 methodology
   - Replaces the vague "If stuck, return to Step 0" statement
   - Provides clear loop exit conditions

2. **FIX 62** → Replace current STEP 0 text
   - Expands from 5 lines to operational 2-part protocol
   - Includes IDEALITY CHECK section
   - Provides unknown unknowns discovery

3. **FIX 63** → Add new section "STUCK/ITERATE/STOP DECISION LOGIC"
   - Provides concrete decision tree
   - Includes iteration limits
   - Clarifies exit criteria

### Testing These Fixes

Apply to a real decision:
- Use FIX 62 (IDEALITY CHECK) first → reveals unknowns
- Use FIX 63 (STUCK/ITERATE/STOP) if you hit any confusion state
- Use FIX 61 (FRAME LOOP) if you need to reframe

If these fixes eliminate the ambiguity, include them in the official v4.0 documentation.

---

## Validation

These fixes address:

| Confusion | Fix | Status |
|-----------|-----|--------|
| 61: Frame loop unclear | Clear loop count + exit conditions | ✓ Operational |
| 62: Step 0 operationally vague | IDEALITY CHECK protocol + unknown unknowns process | ✓ Operational |
| 63: Stuck/Iterate/Stop underspecified | Decision tree + iteration limits + exit criteria | ✓ Operational |

All three fixes maintain compatibility with v4.0 methodology (+46% improvement).
