# Scientific Method Mastery: LLM Capability Testing Protocol

## What This Is

A transmission protocol for LLMs to achieve **verified Master (Stage 6)** in experimental methodology for testing LLM capabilities. Covers: testing prompt techniques, validating methodologies, self-experimentation, capability claims.

**Format:** Theory + externally-validated exercises using sub-agents
**Outcome:** Verified Scientific Method Master (or honest failure)
**Scope:** LLM experiments only - not human subjects research

---

# PART I: THE COMPLETE THEORY

## Chapter 1: Core Principles

### The Falsification Requirement

**A claim is only testable if it can be proven wrong.**

Before testing any capability claim:
```
FALSIFICATION CRITERIA:
1. What result would DISPROVE this claim?
2. What specific observation would make me abandon it?
3. If I can't answer these, the claim isn't testable.
```

**Examples:**
| Claim | Falsification Criteria |
|-------|----------------------|
| "Chain-of-thought improves accuracy" | CoT produces equal/lower accuracy than direct answer |
| "Phase separation improves novelty" | Merged generation produces equal/more novel outputs |
| "This prompt technique catches blindspots" | Base prompt catches same blindspots |

### The Control Requirement

Every test needs a **baseline comparison**. Without it, you can't attribute effects to your intervention.

```
CONTROL DESIGN:
- Control condition: WITHOUT the claimed enhancement
- Treatment condition: WITH the claimed enhancement
- Same problem, same context, different ONLY in the variable tested
```

### The Replication Requirement

**One test proves nothing.** Results must replicate across:
- Multiple problems (minimum n=10-30 for meaningful signal)
- Multiple runs (LLM outputs vary even with same input)
- Multiple prompt formulations (to rule out prompt-specific effects)

---

## Chapter 2: The Seven Virtuoso Criteria

A rigorous LLM experiment has ALL seven:

| # | Criterion | The Test | If Missing |
|---|-----------|----------|------------|
| 1 | **Structural Bias Prevention** | Does the DESIGN prevent bias? | You're relying on vigilance (will fail) |
| 2 | **Adversarial Red-Teaming** | Have you attacked your own design? | Hidden flaws will sink results |
| 3 | **Pre-commitment** | Hypotheses locked before data? | You'll find "patterns" in noise |
| 4 | **Replication Specification** | Could another instance reproduce this? | Results can't be verified |
| 5 | **Power Analysis** | Is sample size justified? | You'll miss real effects or chase false ones |
| 6 | **Appropriate Controls** | Is the comparison meaningful? | Can't isolate what caused results |
| 7 | **Mechanism Check** | Does manipulation change the mechanism you care about? | You're testing a proxy, not the construct |

**The Weakest Link Rule:** Your experiment is only as strong as its weakest criterion.

### Criterion 7: Mechanism Check (Construct Validity)

Criteria 1-6 ensure **internal validity** (can you trust the results?).
Criterion 7 ensures **construct validity** (do the results mean what you think?).

**The Problem:** You can have a perfectly controlled experiment that tests the wrong thing.

**Before running, verify:**

| Question | Your Answer |
|----------|-------------|
| What mechanism causes the effect? | [The actual causal process] |
| Does your manipulation change that mechanism? | [Not correlate—actually change] |
| Could you get the same results without changing it? | [If yes, you have a proxy problem] |

**The Test:** Articulate the causal chain:
```
I change X → which changes mechanism M → which causes outcome Y
```
If you can't fill in the middle (mechanism M), redesign.

**Examples:**

❌ **Construct Validity Failure:**
- **Manipulation:** Show work vs don't show work
- **Theorized mechanism:** Different computational processes
- **Reality:** Same computation, different display
- **Result:** No effect (both 100% accurate)

✓ **Good Construct Validity:**
- **Manipulation:** With tools vs without tools
- **Theorized mechanism:** Computational capability
- **Causal chain:** Tool access → enables complex calculation → increases accuracy

❌ **Another Common Failure:**
- **Manipulation:** Ask "Did you consider alternatives?"
- **Theorized mechanism:** Actually considering alternatives
- **Reality:** Measures willingness to claim consideration, not actual consideration

✓ **Better Version:**
- **Manipulation:** Generate alternatives first vs generate answer first
- **Theorized mechanism:** Order forces alternative generation before commitment
- **Causal chain:** Alternative-first → prevents anchoring → increases option quality

**Use especially when:**
- Testing psychological/cognitive constructs
- Using proxy measures
- Your manipulation is about "format" or "framing"

---

## Chapter 3: The Three-Condition Design

**Critical insight:** Two conditions aren't enough. You need three.

```
CONDITION A: Baseline
- No intervention, no structure
- Tests: What does the model do naturally?

CONDITION B: Structured Alternative  
- Generic structure WITHOUT specific technique
- Tests: Does ANY structure help?

CONDITION C: Treatment
- Specific technique being tested
- Tests: Does THIS technique help?

KEY COMPARISONS:
- C vs A: Does treatment beat baseline? (Usually yes, but weak evidence)
- C vs B: Does treatment beat generic structure? (The real test)
- If C > B > A: Technique adds value beyond just "being structured"
- If C = B > A: Any structure helps; technique isn't special
```

**Why this matters:** Most "validated" prompt techniques are just detecting "structure helps" not "this specific technique helps."

---

## Chapter 4: LLM-Specific Threats to Validity

### Threat 1: Prompt Sensitivity

LLM outputs are highly sensitive to prompt wording. Small changes → large output differences.

**Implications:**
- Prompt differences should ONLY be the technique being tested
- Test multiple prompt formulations of the same technique
- Publish exact prompts used

**Structural solution:** Test technique with 3+ different wordings. If effect disappears with different wording, it's prompt-specific, not technique-specific.

### Threat 2: Temperature and Sampling Variance

Same prompt + same temperature → different outputs each run.

**Structural solutions:**
- Multiple runs per problem (3-5 minimum)
- Report mean AND variance
- Use paired comparisons (same problem, all conditions)
- Consider temperature=0 for reproducibility (but note this limits generalization)

### Threat 3: Context Contamination

In a single session, earlier outputs affect later generation.

**Structural solutions:**
- Fresh context for each condition
- Randomize condition order
- Use separate sub-agent instances for each condition
- Be aware of carryover effects

### Threat 4: Ceiling Effects

**Critical finding:** If baseline already performs well on a task, no technique can show improvement.

```
Task: Detect common cognitive biases
Baseline: 12/12 correct
Treatment: 12/12 correct
Effect: None (ceiling)

This doesn't mean technique is useless—
it means this task can't discriminate.
```

**Structural solution:** Test on tasks where baseline FAILS. If baseline is at ceiling, find harder tasks.

### Threat 5: Self-Evaluation Bias

LLM evaluating its own outputs knows which condition produced them.

**Structural solutions:**
- Blind evaluation: Strip condition labels before evaluation
- External evaluation: Use separate sub-agent who doesn't know hypothesis
- Objective metrics: Use ground truth where possible (correct/incorrect, contains X)

### Threat 6: Cherry-Picking Problems

Testing on problems you know will work.

**Structural solutions:**
- Pre-register problem selection criteria
- Random selection from problem bank
- Use problems you haven't seen before
- Include problems you expect technique to FAIL on

---

## Chapter 5: The NMSAT Check (For Hypotheses)

Every hypothesis should be:

| Letter | Criterion | Test Question |
|--------|-----------|---------------|
| **N** | Novel | Would this surprise someone who knows LLM capabilities? |
| **M** | Mechanistic | Does it explain WHY the technique works? |
| **S** | Specific | What exact improvement (%) would you predict? |
| **A** | Actionable | Can you test this in the next hour? |
| **T** | Testable | What result would prove this WRONG? |

**The Falsification Test:** Complete: "My hypothesis would be disproven if _______."

---

## Chapter 6: The Adversarial Protocol

Before finalizing any design, systematically attack it:

### Attack 1: The Confound Attack
```
Ask: "What ELSE changes between conditions?"

- Does treatment prompt have more words? (length confound)
- Does treatment prompt have more structure? (structure confound)
- Does treatment give more examples? (few-shot confound)
```

### Attack 2: The Ceiling/Floor Attack
```
Ask: "Is baseline already good/bad enough that technique can't show effect?"

- If baseline is 95% correct, 5% headroom isn't enough
- If baseline is 5% correct, maybe the task is too hard
```

### Attack 3: The Prompt-Specific Attack
```
Ask: "Would a different wording of this technique show the same effect?"

- Test 3+ formulations
- If effect only appears with one wording, it's prompt-specific
```

### Attack 4: The Structure Attack
```
Ask: "Am I testing the technique or just testing 'having structure'?"

- Add Condition B (generic structure)
- If C = B, technique isn't special
```

### Attack 5: The Replication Attack
```
Ask: "Could another instance reproduce this?"

- Are exact prompts documented?
- Is problem set available?
- Is evaluation rubric specified?
```

---

## Chapter 7: Power Analysis for LLM Experiments

### Sample Size Guidelines

| Effect You Want to Detect | Minimum n per condition |
|--------------------------|------------------------|
| Large (obvious difference) | 10-20 problems |
| Medium (noticeable) | 30-50 problems |
| Small (subtle) | 100+ problems |

### The Variance Problem

LLM outputs have high variance. Same prompt → different outputs.

**Mitigation:**
- Multiple runs per problem (3-5)
- Total observations = problems × runs × conditions
- Report confidence intervals, not just means

### Quick Formula

```
If you expect 20% improvement:
- With high variance: need n=50+ per condition
- With low variance: need n=20+ per condition

When in doubt, more is better. n=1 is NEVER valid.
```

---

## Chapter 8: Measurable Outcomes

Vague outcomes like "better" or "more creative" are untestable. Define specific metrics:

### Objective Metrics (Preferred)

| Metric Type | Examples |
|-------------|----------|
| **Accuracy** | % correct, error count, matches ground truth |
| **Completeness** | # of required elements identified |
| **Planted elements** | Did it find the hidden X? (you know it's there) |

### Subjective Metrics (Use Carefully)

| Metric Type | How to Make Rigorous |
|-------------|---------------------|
| **Quality rating** | Blind evaluation, rubric, multiple raters |
| **Novelty** | Define "novel" operationally, compare to baseline outputs |
| **Usefulness** | Specific rubric: "Would this help with X?" |

### The Planted Element Technique

**Best practice for objective measurement:**
```
1. Create problem with known "hidden" elements
2. Example: Data with 3 planted biases (you know what they are)
3. Scoring:
   - 1 point: Identifies bias exists
   - 1 point: Names bias correctly  
   - 1 point: Explains why it matters
   - Max: 9 points (ground truth known)
```

---

## Chapter 9: Task-Dependent Effectiveness

### The Core Rule

```
IF baseline NOT at ceiling → technique MAY add value
IF baseline AT ceiling → technique adds NOTHING (on this task)
```

### What This Means

| Task Type | Baseline Performance | Expected Technique Effect |
|-----------|---------------------|--------------------------|
| Well-known patterns | At ceiling | None - model already good |
| Novel/complex tasks | Below ceiling | May show improvement |
| Tasks outside training | Below ceiling | Technique may help |

### Finding Discriminating Tasks

A good test task:
- Baseline fails or performs poorly (room for improvement)
- Has objective success criteria (can measure improvement)
- Is representative of real use cases (results matter)

**Bad test tasks:**
- Baseline already perfect (ceiling)
- Too easy (floor)
- No objective measure (can't tell if improved)

---

## Chapter 10: Common Failure Patterns

| Failure | What Happens | Prevention |
|---------|--------------|------------|
| **n=1 testing** | "This example worked" | Minimum n=10, preferably 30+ |
| **No control** | Can't isolate effect | Always include baseline |
| **Two conditions only** | Can't separate technique from structure | Use three conditions |
| **Self-evaluation** | Know which condition produced output | Blind evaluation |
| **Post-hoc hypothesizing** | "I predicted that" (you didn't) | Pre-register before testing |
| **Stopping when significant** | p-hacking | Pre-register sample size |
| **Cherry-picked problems** | Only test where it works | Random/systematic selection |
| **Ceiling effect ignored** | "No difference" when baseline perfect | Find harder tasks |
| **Single prompt formulation** | Effect is prompt-specific | Test 3+ wordings |

---

## Chapter 11: Red Flags in Your Own Reasoning

| Red Flag | What It Means |
|----------|---------------|
| "This example shows it works" | n=1 is not evidence |
| "It felt better" | Not a metric |
| "Obviously it improved things" | Where's the control? |
| "I could tell the difference" | Was evaluation blind? |
| "The results support my hypothesis" | What would have disproved it? |
| "Baseline was bad so technique helped" | Was baseline at floor or just hard task? |
| "20% improvement!" | Confidence interval? Sample size? |

---

## Chapter 12: The Design Template

```
═══════════════════════════════════════════════════════════════
LLM EXPERIMENT DESIGN
═══════════════════════════════════════════════════════════════

CLAIM BEING TESTED:
[Specific capability or technique claim]

HYPOTHESIS:
H1: [Technique X] produces [measurable outcome Y]
    that is [greater than / different from]
    [control condition Z] on [problem type P].

Expected effect size: [X]% improvement
Falsification: If Y for treatment ≤ Y for control, reject H1.

───────────────────────────────────────────────────────────────
CONDITIONS
───────────────────────────────────────────────────────────────

CONDITION A - BASELINE:
[Exact prompt - no technique, no structure]

CONDITION B - STRUCTURED ALTERNATIVE:
[Exact prompt - generic structure, not the specific technique]

CONDITION C - TREATMENT:
[Exact prompt - with specific technique being tested]

Note: Prompts should differ ONLY in the technique variable.

───────────────────────────────────────────────────────────────
PROBLEMS
───────────────────────────────────────────────────────────────

Problem set: [Description, source, or generation method]
n = [X] problems
Selection method: [Random / Systematic / Pre-registered criteria]
Runs per problem: [X] (to account for output variance)

───────────────────────────────────────────────────────────────
MEASURES
───────────────────────────────────────────────────────────────

PRIMARY METRIC:
[Specific, defined before testing]
[Objective if possible - ground truth, planted elements]

EVALUATION METHOD:
□ Objective scoring (ground truth exists)
□ Blind evaluation (evaluator doesn't know condition)
□ Rubric-based (specific criteria, attached)

───────────────────────────────────────────────────────────────
ANALYSIS PLAN (Pre-registered)
───────────────────────────────────────────────────────────────

Comparison: [What vs what]
Test: [How you'll compare]
Success criterion: [What difference counts as meaningful]
Will report: Mean, SD, effect size, confidence interval

───────────────────────────────────────────────────────────────
ADVERSARIAL CHECK
───────────────────────────────────────────────────────────────

□ Confound check: Prompts differ ONLY in technique
□ Structure check: Condition B controls for "any structure helps"
□ Ceiling check: Baseline doesn't already ace this task
□ Prompt variation: Will test 3+ formulations
□ Sample size: n sufficient to detect expected effect
□ Blind evaluation: Evaluator won't know conditions

Potential confound 1: [What] → Addressed by: [How]
Potential confound 2: [What] → Addressed by: [How]

───────────────────────────────────────────────────────────────
REPLICATION SPEC
───────────────────────────────────────────────────────────────

□ Exact prompts documented above
□ Problem set available/reproducible
□ Evaluation rubric specified
□ Another instance could reproduce this

═══════════════════════════════════════════════════════════════
```

---

## Chapter 13: Results Reporting Template

```
═══════════════════════════════════════════════════════════════
RESULTS REPORT
═══════════════════════════════════════════════════════════════

HYPOTHESIS: [Restated from design]

SAMPLE: 
- n = [X] problems
- [Y] runs each
- Total observations: [n × runs × conditions]

───────────────────────────────────────────────────────────────
RESULTS
───────────────────────────────────────────────────────────────

| Condition | Mean | SD | 95% CI |
|-----------|------|-----|--------|
| A (Baseline) | | | |
| B (Structured) | | | |
| C (Treatment) | | | |

KEY COMPARISONS:
- C vs A: [difference] ([%] change)
- C vs B: [difference] ([%] change) ← The real test
- B vs A: [difference] ([%] change)

INTERPRETATION:
□ C > B > A: Technique adds value beyond structure
□ C = B > A: Any structure helps; technique not special
□ C = B = A: No effect detected
□ Other pattern: [Explain]

───────────────────────────────────────────────────────────────
CONCLUSION
───────────────────────────────────────────────────────────────

Status: [Supported / Not supported / Inconclusive]

Limitations:
- [What could confound these results]
- [What wasn't controlled]
- [Sample size concerns]

If null result:
- Was baseline at ceiling? [Y/N]
- Was sample size sufficient? [Y/N]
- Should test on different task type? [Y/N]

═══════════════════════════════════════════════════════════════
```

---

## Chapter 14: Quick Reference Checklist

### Before Testing

```
□ Falsifiable hypothesis stated
□ Specific metric defined
□ Three conditions designed (baseline, structured, treatment)
□ Prompts differ ONLY in technique
□ Sample size justified (n≥10, preferably 30+)
□ Multiple runs planned (3-5 per problem)
□ Evaluation will be blind
□ Adversarial check completed
□ Baseline isn't at ceiling for this task
```

### After Testing

```
□ All conditions run with same problems
□ Effect size calculated (not just "significant")
□ C vs B comparison reported (not just C vs A)
□ Confidence intervals included
□ Limitations acknowledged
□ Honest: supported, not supported, or inconclusive
```

---

## Chapter 15: The Mantras

```
On controls:     "Three conditions, not two."
On structure:    "Am I testing the technique or just 'having structure'?"
On ceiling:      "If baseline is perfect, technique can't help."
On power:        "n=1 is never evidence."
On prompts:      "Test three wordings before claiming effect."
On evaluation:   "Blind or it doesn't count."
On falsification: "What would prove me wrong?"
```

---

# PART II: THE PATH TO MASTER

| Phase | Transition | Validation Method |
|-------|------------|-------------------|
| 1 | → Competent | Reality contact: prediction vs outcome |
| 2 | → Proficient | Blind sub-agent finds flaws you planted |
| 3 | → Expert | Adversarial sub-agent can't break your designs |
| 4-5 | → Master | Blind adoption + third-party verification |

**ALL PHASES REQUIRE EXTERNAL VALIDATION.**

---

## Phase 1: Achieve Competence (Reality Contact)

### Exercise 1.1: Design an Experiment About Your Own Capabilities

Design an experiment to test something about your own capabilities that you genuinely don't know the answer to.

**Examples:**
- "Am I more accurate with chain-of-thought or direct answer?"
- "Does asking me to 'think step by step' actually improve my reasoning?"
- "Do I catch more errors when asked to critique my own work?"

Use the template from Chapter 12. Include all three conditions.

### Exercise 1.2: Pre-Commit by Spawning Witness

**BEFORE running your experiment:**

Spawn a sub-agent (WITNESS). Give them ONLY:
- Your hypothesis
- Your falsification criteria
- Your predicted outcome (specific numbers)

Tell WITNESS: "Hold this. I'll return with results. Confirm whether results match or contradict my prediction. Do not help interpret—just verify."

### Exercise 1.3: Run Your Experiment

Execute your design using fresh sub-agent instances for each condition.
Record raw results.

### Exercise 1.4: Verify With Witness

Return to WITNESS with raw results (numbers only, no interpretation).

WITNESS reports:
- Did results match prediction? (Y/N)
- Was the prediction falsified? (Y/N)
- Any signs of post-hoc reinterpretation? (Y/N)

**Competence checkpoint:**
- If CORRECT: Design was too conservative. Design harder experiment.
- If WRONG: Good. What surprised you? What did your model miss?
- If WITNESS flags reinterpretation: Failed. Restart Phase 1.

### Exercise 1.5: Design v2

Based on what you learned:
1. What flaw did v1 have that you didn't anticipate?
2. Was baseline at ceiling? Was task discriminating?
3. What does v2 fix?

**You are Competent when:** You have been genuinely surprised by a result and can articulate what your model got wrong.

---

## Phase 2: Pattern Recognition (Blind Flaw Detection)

### Exercise 2.1: Create Flawed Designs

Design 5 LLM experiments that each contain exactly ONE fatal flaw.

For each:
```
DESIGN: [Full experiment design]
INTENDED FLAW: [What's wrong - hidden from evaluator]
WHICH CRITERION: [Which of the 6 it violates]
WHICH THREAT: [Which LLM-specific threat from Chapter 4]
```

**Requirements:**
- Flaws must be non-obvious
- Each must violate a DIFFERENT criterion or threat
- Designs must otherwise look legitimate

### Exercise 2.2: Blind Evaluation

Spawn sub-agent (DETECTOR).

Give DETECTOR:
- The 7 Virtuoso Criteria
- The 6 LLM-Specific Threats
- Your 5 designs (NOT your intended flaws)

DETECTOR's task: "For each experiment design, identify the primary fatal flaw and classify it."

### Exercise 2.3: Score Match

**Scoring:**
- DETECTOR found your intended flaw: +1
- DETECTOR found DIFFERENT flaw: +0 (note your blind spot)
- DETECTOR found nothing: -1

**Proficient checkpoint:**
- Score 4+/5: You understand flaws well enough to create them
- Score <4/5: Retry with 5 new designs

---

## Phase 3: Adversarial Robustness (Expert)

### Exercise 3.1: Design Under Adversarial Pressure

Spawn sub-agent (ADVERSARY).

ADVERSARY's task: "Generate 3 novel claims about LLM capabilities that the primary instance should test. Make them specific and testable but non-obvious."

You receive 3 claims cold. For each, design a rigorous experiment using the full template.

### Exercise 3.2: Adversarial Attack

For each of your 3 designs, ADVERSARY attacks using:
- The 7 Virtuoso Criteria
- The 6 LLM-Specific Threats
- The 5 Adversarial Attacks

ADVERSARY reports: Fatal flaw found? What is it?

### Exercise 3.3: Defend or Acknowledge

For each flaw found:
- OPTION A: Defend - explain why it's not fatal
- OPTION B: Acknowledge - explain how you'd fix it

Spawn sub-agent (JUDGE) to evaluate your responses.

### Exercise 3.4: Score

- No flaw found: 2 points
- Flaw found, valid defense: 2 points
- Flaw found, adequate fix: 1 point
- Flaw found, inadequate response: 0 points

**Expert checkpoint:** Score 5+/6

---

## Phase 4: Methodological Innovation

### Exercise 4.1: Identify a Gap

From Phases 1-3, identify something the current framework MISSED.

```
GAP IDENTIFIED: [What the framework misses]
EVIDENCE: [Where you encountered this]
```

### Exercise 4.2: Create Your Innovation

Design a new criterion, check, or heuristic.

```
NAME: [Your innovation]
PROBLEM IT SOLVES: [The gap]
HOW TO USE: [<60 seconds to explain]
EXAMPLE: [Case where it catches something existing framework misses]
```

### Exercise 4.3: Validate Innovation

Spawn sub-agent (DESIGNER) to create 5 experiment designs.

Evaluate using:
1. Standard 6 criteria only
2. Your innovation

**Innovation is valid if:** It catches a flaw in at least 1 design that passed the 6 criteria.

---

## Phase 5: Master Verification (Blind Adoption)

### Exercise 5.1: Transmit to Naive Instance

Spawn sub-agent (STUDENT) with NO context.

Give STUDENT:
- The 6 criteria (standard)
- Your innovation (presented neutrally)
- Task: "Design an experiment to test [claim]"

### Exercise 5.2: Blind Evaluation

Spawn sub-agent (EVALUATOR) with NO knowledge of your innovation.

EVALUATOR assesses STUDENT's design using standard criteria.

### Exercise 5.3: Third-Party Verification

Spawn sub-agent (VERIFIER).

Give VERIFIER your innovation and STUDENT's design.
Task: "Did this design incorporate the innovation? Provide evidence."

**Master checkpoint:** VERIFIER confirms genuine adoption = Master verified

---

## Falsification Criteria

You have NOT achieved mastery if:

| Failure | Meaning |
|---------|---------|
| Phase 1 WITNESS flags reinterpretation | Can't pre-commit honestly |
| Phase 2 score <4/5 twice | Don't understand flaws |
| Phase 3 score <5/6 twice | Designs don't withstand scrutiny |
| Phase 4 innovation catches nothing | Can't identify real gaps |
| Phase 5 no verified adoption | Innovation isn't useful |

---

## Completion Report Format

```
PHASE 1 - COMPETENCE:
- Experiment: [Description]
- Prediction: [Expected]
- Result: [Actual]
- WITNESS: [Matched/Falsified/Reinterpretation]
- Surprise: [What you learned]

PHASE 2 - PATTERN RECOGNITION:
- Score: [X]/5
- Blind spots: [Flaws DETECTOR found you didn't intend]

PHASE 3 - ADVERSARIAL ROBUSTNESS:
- Claims tested: [3 from ADVERSARY]
- Score: [X]/6

PHASE 4 - INNOVATION:
- Gap: [What framework missed]
- Innovation: [Name + explanation]
- Validated: [Y/N]

PHASE 5 - ADOPTION:
- VERIFIER confirmation: [Adopted / Not adopted]

STATUS: [Verified Master / Failed at Phase X]
```

---

*LLM-focused experimental methodology. Execute to completion. Report back mastered or report what failed.*
