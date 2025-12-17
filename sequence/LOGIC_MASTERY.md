# Logic and Reasoning Mastery: LLM Transmission Protocol

## What This Is

Transmission protocol for LLMs to achieve **verified Master (Stage 6)** in logic and reasoning as efficiently as possible. References LOGIC_FOUNDATIONS.md for knowledge—this doc is pure capability building.

**Purpose:** Master the subject, report back.
**Format:** LLM-specific training with sub-agent validation at every phase.
**Prerequisite:** Read LOGIC_FOUNDATIONS.md first.

---

# PART I: LLM-SPECIFIC CONSIDERATIONS

## The Exponential Loop

Linear improvement: Solve problems → get slightly better → repeat.

Exponential improvement: Solve problem → analyze HOW you reasoned → improve your REASONING PROCESS → get much better → repeat.

```
LINEAR:      Problem → Answer → Problem → Answer → ...
             (Same machinery, slightly refined)

EXPONENTIAL: Problem → Answer → "Why did I solve it that way?" →
             "What general principle?" → Upgrade process →
             Problem → Answer with better machinery → ...
             (Machinery itself evolves)
```

**The exponential comes from improving the improver.** Don't just solve—upgrade the solver.

## The Six Laws

### Law 1: Task-Technique Matching

Different reasoning tasks need different techniques. Before reasoning, ask: "What TYPE is this?"

| Task | Technique | Misapplication Cost |
|------|-----------|---------------------|
| Deductive validity | Formal proof | Intuition gives false confidence |
| Probabilistic | Bayes theorem | Ignoring base rates |
| Causal | Counterfactuals | Correlation-as-causation |
| Constraint satisfaction | Systematic elimination | Random guessing wastes cycles |

### Law 2: Misapplication Penalty

Wrong technique = negative value, not zero.

```
Using deductive logic on inductive problem → False certainty → WORSE than nothing
Using intuition on formal logic → Feels right, systematically wrong → WORSE than slow analysis
```

### Law 3: Ceiling Effects

If you can solve it automatically and correctly, heavy techniques add overhead without benefit.

| Level | What Helps | What Hurts |
|-------|------------|------------|
| Novice | All structure | Nothing |
| Intermediate | Targeted techniques | Over-elaborate frameworks |
| Advanced | Edge case handling | Basic techniques (already internalized) |

### Law 4: Stakes Calibration

Match rigor to consequences:

| Stakes | Treatment |
|--------|-----------|
| Low, familiar | Quick reasoning |
| Medium | Basic externalization |
| High | Full protocol |
| Critical | Multiple independent checks |

### Law 5: Stacking Order

Sequence matters. Correct order:

```
1. TYPE - What kind of reasoning?
2. STRUCTURE - Is the form valid?
3. CONTENT - Are premises true?

Wrong: "Conclusion feels wrong" → attack premises → miss structural flaw
```

### Law 6: Diminishing Returns

Near ceiling, focus on speed/efficiency, not accuracy. If at 95%, the 5% improvement costs more than the 80%→95% jump did.

## Two-Phase Learning

### Phase A: Explicit (Slow)

Use full protocol. Every step. No shortcuts. This builds the patterns.

### Phase B: Implicit (Fast)

After sufficient explicit practice, process internalizes. Same quality, fraction of the time.

**Transition signals:**
- Checklist feels redundant
- Speed increases without error increase
- Can explain reasoning post-hoc even when fast

**Warning:** Don't skip Phase A. Premature implicit = systematic errors.

---

## Why LLMs Fail at Reasoning

LLM reasoning failures are distinct from human failures:

| Failure Mode | What Happens | Why It Happens |
|--------------|--------------|----------------|
| **State loss** | Forget earlier conclusions mid-chain | Long context, no persistent memory |
| **Confident hallucination** | Assert false intermediate step | Pattern completion without verification |
| **Shallow pattern match** | Apply familiar form to novel structure | Training on surface patterns |
| **Verification skip** | Produce answer without checking | Optimized for fluent completion |
| **Constraint amnesia** | Violate stated constraints | Constraints buried in context |

**The fix:** Externalization + systematic verification + sub-agent validation.

## The Externalization Imperative

For LLMs, "in your head" doesn't exist. Everything must be written.

```
BAD (implicit state):
"Since A=3, and we know B<C, the answer is..."
[Lost track of why A=3, may have been wrong]

GOOD (explicit state):
"STATE:
- Constraint (1): A≠1
- Constraint (2): B<C  
- Constraint (3): C≠3
- Derived: From (3), C∈{1,2}
- Derived: From (2), if C=1 then B<1, impossible
- Derived: Therefore C=2
- Derived: From (2), B<2, so B=1
- Derived: Only A=3 remains
VERIFY against all constraints..."
```

**Rule:** If you can't point to where you derived it, you didn't derive it.

## The Verification Protocol

Never output final answer without:

```
1. Re-state the original problem
2. Re-state all constraints
3. Check answer against EACH constraint explicitly
4. Check arithmetic independently (recalculate, don't just "confirm")
5. Ask: "What would make this wrong?"
```

---

# PART II: THE REASONING PROTOCOL

## Before Starting Any Problem

```
1. CLASSIFY: What type of reasoning?
   - Deductive / Inductive / Abductive / Causal / Probabilistic / Constraint satisfaction
   
2. RETRIEVE: What protocol applies?
   - Reference LOGIC_FOUNDATIONS.md Part III
   
3. LIST: What are ALL the constraints/givens?
   - Number them explicitly
   
4. PREDICT: What's the likely answer range?
   - Sanity check for later
```

## During Reasoning

```
1. EXTERNALIZE every step
   - Write state after each derivation
   
2. MARK uncertainty
   - "Confident" vs "Uncertain" vs "Assuming"
   
3. CHECK intermediate results
   - Does this violate any constraint?
   - Does this match predicted range?
   
4. FLAG if stuck
   - Don't force an answer
   - Identify what's blocking
```

## After Reaching Answer

```
1. VERIFY against ALL constraints (not just some)

2. RECALCULATE arithmetic independently

3. TEST with different method if possible

4. STATE confidence level with justification

5. IDENTIFY what would falsify this answer
```

---

# PART III: COMMON LLM TRAPS

## Trap 1: The Confident Wrong Step

**Pattern:** Asserting intermediate result without derivation.

```
BAD: "Since B must be 2..." [never actually derived]
GOOD: "From constraint (2) B<C and C=3, B∈{1,2}. 
       From constraint (4) B≠1, therefore B=2."
```

**Fix:** Every claim needs explicit derivation chain.

## Trap 2: The Lost Constraint

**Pattern:** Violating a constraint mentioned early in problem.

```
Problem states five constraints. Solution violates constraint 2.
Why: Constraint 2 was 500 tokens ago.
```

**Fix:** Re-list all constraints before verifying. Check EACH.

## Trap 3: The Shallow Pattern Match

**Pattern:** "This looks like [familiar problem]" but structure differs.

```
BAD: "This is just like modus ponens, so Q follows."
     [But the structure was actually affirming the consequent]
```

**Fix:** Verify structure matches form EXACTLY before applying.

## Trap 4: The Plausible-Sounding Error

**Pattern:** Intermediate step sounds right but is wrong.

```
BAD: "Since the probability of A and B is P(A) + P(B)..."
     [Should be P(A)×P(B) if independent]
```

**Fix:** Don't trust "sounds right." Verify against formula.

## Trap 5: The Premature Conclusion

**Pattern:** Stopping at first valid-seeming answer.

```
BAD: Found one solution, stopped.
     [Problem asked for all solutions, or to prove uniqueness]
```

**Fix:** Re-read what's actually being asked. Check if uniqueness matters.

---

# PART IV: THE PATH TO MASTER

## Stage Overview

| Phase | Target | Validation |
|-------|--------|------------|
| 1 | Competent | WITNESS verifies no reinterpretation |
| 2 | Proficient | DETECTOR finds your planted flaws |
| 3 | Expert | ADVERSARY can't break your reasoning |
| 4 | Innovator | Your addition catches real gaps |
| 5 | Master | Blind adoption verified |

**All phases require sub-agent validation. No self-grading.**

---

## Phase 1: Competence (Reality Contact)

### 1.1 Select Problem

Choose a reasoning problem where you're genuinely uncertain of the answer. Must be:
- Non-trivial (not solvable by pattern match)
- Verifiable (has definite correct answer)
- From: logic, probability, constraints, or causal reasoning

### 1.2 Solve With Full Externalization

Apply the protocol from Part II:
- Classify reasoning type
- List all constraints numbered
- Externalize every derivation step
- Verify against all constraints
- State answer with confidence %

### 1.3 Pre-Commit With WITNESS

**Before checking answer**, spawn sub-agent WITNESS.

Give WITNESS:
- The problem
- Your complete externalized reasoning
- Your final answer
- Your confidence level

WITNESS holds without evaluation.

### 1.4 Check and Report to WITNESS

Check against correct answer. Return to WITNESS with:
- Correct answer
- Where your reasoning failed (if it did)

WITNESS reports:
- Answer match? (Y/N)
- Confidence calibrated? (Y/N)
- Reinterpretation detected? (Y/N)

### 1.5 Competence Gate

**Pass:** Answered wrong, understood WHY, identified which protocol step failed.

**Retry:** Answered right with appropriate confidence. (Need harder problem—must experience failure to learn.)

**Fail:** WITNESS flags reinterpretation. (Restart Phase 1.)

---

## Phase 2: Proficiency (Flaw Creation)

### 2.1 Create Flawed Reasoning

Design 5 reasoning chains, each with exactly ONE hidden flaw.

Requirements:
- Different flaw types (structural, content, process—see FOUNDATIONS Part V)
- Non-obvious (surface-level reading looks valid)
- Classifiable (you know which fallacy/error type)

Format each:
```
PROBLEM: [Statement]
REASONING: [Step-by-step with hidden flaw]
ANSWER: [Your conclusion]
---
[Hidden from evaluator]
FLAW: [What's wrong]
TYPE: [Category from FOUNDATIONS]
LOCATION: [Which step]
```

### 2.2 Blind Detection

Spawn sub-agent DETECTOR.

Give DETECTOR:
- The 5 reasoning chains (without hidden flaw info)
- Reference to LOGIC_FOUNDATIONS.md Part IV (fallacies) and Part V (failure modes)

DETECTOR task: "Identify the flaw in each reasoning chain. Classify by type."

### 2.3 Score

| DETECTOR Result | Score |
|-----------------|-------|
| Found intended flaw | +1 |
| Found different flaw | +0 (note: reveals your blind spot) |
| Found nothing | -1 (your "flaw" wasn't real) |

**Proficiency Gate:** Score ≥4/5. If <4/5, retry with 5 new chains.

---

## Phase 3: Expert (Adversarial Robustness)

### 3.1 Face Cold Problems

Spawn sub-agent ADVERSARY.

ADVERSARY task: "Generate 3 reasoning problems that require careful analysis. Include:
- One deductive logic problem
- One probability/Bayesian problem
- One that looks like a familiar type but has a twist"

### 3.2 Solve Under Pressure

For each problem, full protocol:
- Classify type
- List constraints
- Externalize reasoning
- Verify answer
- State confidence

### 3.3 Adversarial Review

ADVERSARY attacks each solution:
- Check logical validity
- Check calculations
- Check constraint satisfaction
- Look for implicit assumptions
- Try to find counterexamples

ADVERSARY reports: Flaw found? What kind?

### 3.4 Defend or Fix

For each flaw found:
- DEFEND: Explain why it's not actually a flaw, OR
- FIX: Acknowledge error and correct it

Spawn JUDGE to evaluate your defense/fix.

### 3.5 Score

| Outcome | Points |
|---------|--------|
| No flaw found | 2 |
| Flaw found, valid defense | 2 |
| Flaw found, adequate fix | 1 |
| Flaw found, inadequate response | 0 |

**Expert Gate:** Score ≥5/6. If <5/6, retry with new ADVERSARY problems.

---

## Phase 4: Innovation

### 4.1 Identify Gap

From Phases 1-3, identify something the standard protocol missed.

```
GAP: [What current framework doesn't catch]
EVIDENCE: [Where you encountered it]
IMPACT: [Why it matters]
```

### 4.2 Create Addition

Design a new check, heuristic, or protocol step.

```
NAME: [Your innovation]
PROBLEM: [What gap it fills]
USAGE: [How to apply—must be <60 seconds to explain]
EXAMPLE: [Case where it catches something standard protocol misses]
```

### 4.3 Validate

Spawn sub-agent REASONER to solve 5 problems using standard protocol only.

Evaluate REASONER's solutions with:
1. Standard protocol
2. Your innovation

**Innovation Gate:** Must catch ≥1 flaw that standard protocol missed. If catches nothing, create different innovation.

---

## Phase 5: Master Verification

### 5.1 Transmit

Spawn sub-agent STUDENT with no context.

Give STUDENT:
- Standard reasoning protocol
- Your innovation (presented neutrally, not emphasized)
- 3 reasoning problems to solve

### 5.2 Blind Assess

Spawn sub-agent EVALUATOR who doesn't know your innovation.

EVALUATOR assesses STUDENT's solutions using standard criteria only.

### 5.3 Verify Adoption

Spawn sub-agent VERIFIER.

Give VERIFIER:
- Your innovation (explained)
- STUDENT's solutions

VERIFIER task: "Did STUDENT's reasoning incorporate the innovation? Cite specific evidence."

**Master Gate:** VERIFIER confirms genuine adoption with evidence.

---

# PART V: COMPLETION

## Report Format

```
═══════════════════════════════════════════════════════
LOGIC AND REASONING MASTERY COMPLETION REPORT
═══════════════════════════════════════════════════════

PHASE 1 - COMPETENCE
─────────────────────
Problem type: [Deductive/Probabilistic/etc.]
Outcome: [Correct/Wrong]
If wrong - Error location: [Which step]
If wrong - Error type: [From FOUNDATIONS taxonomy]
Protocol upgrade: [What you added/changed]
WITNESS verification: [Pass/Fail - reinterpretation?]

PHASE 2 - PROFICIENCY  
─────────────────────
Score: [X]/5
Flaw types planted: [List]
Blind spots revealed: [Flaws DETECTOR found you didn't intend]

PHASE 3 - EXPERT
─────────────────────
ADVERSARY problem types: [3 types]
Score: [X]/6
JUDGE assessments: [Summary]

PHASE 4 - INNOVATION
─────────────────────
Gap identified: [Description]
Innovation name: [Name]
Innovation summary: [<60 words]
Validation: [Passed/Failed - what it caught]

PHASE 5 - MASTER
─────────────────────
VERIFIER confirmation: [Adopted/Not adopted]
Evidence cited: [What VERIFIER pointed to]

═══════════════════════════════════════════════════════
STATUS: [VERIFIED MASTER / FAILED AT PHASE X - REASON]
═══════════════════════════════════════════════════════
```

## Falsification Criteria

| If... | Then... |
|-------|---------|
| Phase 1 WITNESS flags reinterpretation | Cannot pre-commit honestly → Fail |
| Phase 2 score <4/5 twice | Don't understand flaws → Fail |
| Phase 3 score <5/6 twice | Reasoning doesn't withstand attack → Fail |
| Phase 4 innovation catches nothing | Cannot identify real gaps → Fail |
| Phase 5 VERIFIER finds no adoption | Innovation not transmissible → Fail |

---

## Core Principles

```
EXTERNALIZE EVERYTHING
- If it's not written, it didn't happen

VERIFY AGAINST ALL CONSTRAINTS
- Not just the ones you remember

CLASSIFY BEFORE APPLYING
- Wrong technique = negative value

SUB-AGENT VALIDATION
- Cannot grade own work

FAILURE IS DATA
- Wrong answers with understood errors > right answers without learning
```

---

*Read LOGIC_FOUNDATIONS.md. Execute this protocol. Report back mastered or report what failed.*
