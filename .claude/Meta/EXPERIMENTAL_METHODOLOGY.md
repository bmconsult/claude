# Experimental Methodology for LLM Capability Testing
## A Rigorous Framework for Validating Claims

**Version 1.0 | December 2024**

---

## Part I: Core Principles

### The Falsification Requirement (Popper)

**A claim is only scientific if it can be proven wrong.**

Before testing any capability claim, specify:
```
FALSIFICATION CRITERIA:
1. What result would DISPROVE this claim?
2. What specific observation would make me abandon it?
3. If I can't answer these, the claim isn't testable.
```

**Examples:**
| Claim | Falsification Criteria |
|-------|----------------------|
| "Inversion accesses regions forward-gen can't" | Forward-gen produces identical outputs to Inversion on N problems |
| "Phase separation improves novelty" | Separated phases produce equal/less novel outputs than merged |
| "GOL improves problem-solving" | Problems solved with GOL have equal/lower quality than without |

### The Control Requirement

Every test needs a **baseline comparison**. Without it, you can't attribute effects to your intervention.

```
CONTROL DESIGN:
- Control condition: The thing WITHOUT your claimed enhancement
- Treatment condition: The thing WITH your claimed enhancement
- Same problem, same context, different only in the variable you're testing
```

### The Randomization Requirement

Eliminate bias by randomizing what you can:
- Order of conditions (don't always test treatment first)
- Selection of test problems (don't cherry-pick)
- Evaluation order (if evaluating outputs)

### The Replication Requirement

**One test proves nothing.** Results must replicate across:
- Multiple problems (minimum n=10-30 for meaningful signal)
- Multiple runs (LLM outputs vary even with same input)
- Ideally, multiple evaluators

---

## Part II: Designing LLM Experiments

### Step 1: Formulate Falsifiable Hypothesis

```
HYPOTHESIS TEMPLATE:
H1: [Technique X] produces [measurable outcome Y]
    that is [greater than / different from]
    [control condition Z]
    on [problem type P].

NULL HYPOTHESIS (H0):
There is no difference between X and Z on outcome Y.

FALSIFICATION:
If outcome Y for X ≤ outcome Y for Z, reject H1.
```

### Step 2: Define Measurable Outcomes

Vague outcomes like "better" or "more creative" are untestable. Define specific metrics:

| Outcome Type | Possible Metrics |
|--------------|------------------|
| **Novelty** | % of outputs containing ideas not in control; expert rating 1-5 |
| **Correctness** | % of problems solved correctly; error count |
| **Coverage** | # of distinct solution approaches generated |
| **Quality** | Blind rating by evaluator; rubric score |

### Step 3: Determine Sample Size

**Minimum viable test:** n=10-30 problems per condition
**Reason:** With n<10, random variation dominates signal

For effect size estimation:
- Small effect: need n~100+ per condition
- Medium effect: need n~30-50 per condition
- Large effect: might detect with n~10-20 per condition

**When in doubt, more is better.** n=1 is never valid.

### Step 4: Design Controls

```
CONTROL DESIGN TEMPLATE:
┌─────────────────────────────────────────────────────┐
│ CONTROL CONDITION                                   │
│ - Same problem                                      │
│ - Same model                                        │
│ - Same temperature                                  │
│ - Base prompt (without enhancement)                 │
├─────────────────────────────────────────────────────┤
│ TREATMENT CONDITION                                 │
│ - Same problem                                      │
│ - Same model                                        │
│ - Same temperature                                  │
│ - Enhanced prompt (with technique being tested)    │
├─────────────────────────────────────────────────────┤
│ ONLY DIFFERENCE: The specific technique            │
└─────────────────────────────────────────────────────┘
```

### Step 5: Implement Blinding (Where Possible)

**Blinding prevents expectation bias.** Options for LLM testing:

| Blinding Type | Implementation |
|---------------|----------------|
| **Output blinding** | Evaluate outputs without knowing which condition produced them |
| **Order randomization** | Randomize which condition runs first |
| **External evaluation** | Have someone else rate outputs who doesn't know the hypothesis |

### Step 6: Pre-Register Analysis

**Decide how you'll analyze BEFORE seeing results.** This prevents:
- p-hacking (trying analyses until something is significant)
- HARKing (Hypothesizing After Results are Known)
- Cherry-picking (only reporting favorable results)

```
PRE-REGISTRATION TEMPLATE:
1. Hypothesis: [stated before testing]
2. Sample size: [n=X problems, Y runs each]
3. Metric: [specific, defined before testing]
4. Analysis: [how I'll compare conditions]
5. Success criterion: [what difference counts as meaningful]
6. Falsification criterion: [what would disprove the claim]
```

---

## Part III: Analyzing Results

### Effect Size, Not Just "Significance"

**P-values alone are misleading.** Always report:

1. **Effect size**: How BIG is the difference?
   - Mean difference between conditions
   - % improvement
   - Cohen's d for standardized comparison

2. **Confidence interval**: How PRECISE is the estimate?
   - Wide interval = uncertain
   - Narrow interval = more reliable

3. **Practical significance**: Does the difference MATTER?
   - A 0.1% improvement might be "statistically significant" with large n but meaningless in practice

### Handling Variability

LLM outputs are stochastic. Same prompt → different outputs.

**Mitigation:**
- Multiple runs per problem (e.g., 3-5 runs each)
- Report mean and variance
- Use paired comparisons (same problem, both conditions)

### Reporting Standards

```
RESULTS TEMPLATE:
─────────────────────────────────────────
Hypothesis: [X improves Y compared to Z]

Sample: n=[X] problems, [Y] runs each
       Total observations: [n×runs×2 conditions]

Results:
- Control mean: [value] (SD=[value])
- Treatment mean: [value] (SD=[value])
- Difference: [value] ([%] improvement)
- Effect size: [Cohen's d or similar]

Conclusion:
[Supported / Not supported / Inconclusive]

Limitations:
- [what could confound these results]
- [what wasn't controlled]
─────────────────────────────────────────
```

---

## Part IV: Common Pitfalls

### Pitfall 1: n=1 Testing
**Problem:** Testing one example and generalizing
**Fix:** Minimum n=10, preferably n=30+

### Pitfall 2: Self-Evaluation
**Problem:** Evaluating your own outputs knowing the hypothesis
**Fix:** Blind evaluation, external evaluators, objective metrics

### Pitfall 3: No Control Condition
**Problem:** Testing treatment without baseline
**Fix:** Always include control (base prompt/method)

### Pitfall 4: Cherry-Picking Problems
**Problem:** Testing on problems you know will work
**Fix:** Random or systematic problem selection, pre-register selection criteria

### Pitfall 5: Confirmation Interpretation
**Problem:** Interpreting ambiguous results as supporting hypothesis
**Fix:** Pre-register falsification criteria, be honest about ambiguous results

### Pitfall 6: Stopping When Significant
**Problem:** Running until you get p<0.05, then stopping
**Fix:** Pre-register sample size, run full experiment regardless of intermediate results

### Pitfall 7: HARKing
**Problem:** Formulating hypothesis after seeing results
**Fix:** Pre-register hypothesis before testing

---

## Part V: LLM-Specific Considerations

### Prompt Sensitivity

LLM outputs are highly sensitive to prompt wording. Small changes → large output differences.

**Implication:** When testing technique X vs control:
- Prompt differences should ONLY be the technique
- Avoid inadvertently changing other aspects
- Consider testing multiple prompt formulations

### Temperature and Sampling

Same prompt + same temperature can produce different outputs.

**Implication:**
- Set temperature explicitly
- Run multiple times per condition
- Report temperature setting

### Evaluation Challenges

Many LLM outputs are hard to evaluate objectively (creativity, quality).

**Options:**
- Use objective metrics where possible (correct/incorrect, contains X/doesn't)
- Use rubrics for subjective evaluation
- Use multiple evaluators and measure agreement
- Consider using LLM-as-judge (with awareness of limitations)

### Context Contamination

In a single session, earlier outputs affect later generation.

**Implication:**
- Fresh context for each condition when possible
- Randomize condition order
- Be aware of carryover effects

---

## Part VI: Quick Reference

### Before Testing, Answer:

```
□ What is my falsifiable hypothesis?
□ What specific metric will I measure?
□ What is my control condition?
□ How many test cases? (minimum 10)
□ How will I avoid bias in evaluation?
□ What result would disprove my claim?
```

### After Testing, Report:

```
□ Sample size and composition
□ Effect size (not just significance)
□ Confidence/variability
□ Limitations and potential confounds
□ Honest assessment: supported, not supported, or inconclusive
```

### Red Flags in Your Own Reasoning:

| Red Flag | What It Means |
|----------|---------------|
| "This example shows it works" | n=1 is not evidence |
| "It felt better" | Not a metric |
| "Obviously it improved things" | Where's the control? |
| "I could tell the difference" | Was evaluation blind? |
| "The results support my hypothesis" | What would have disproved it? |

---

## Part VII: Applying This to GOL Claims

### Claims That Need Testing

| Claim | Falsifiable Version | Required Test |
|-------|--------------------| --------------|
| "Inversion accesses regions forward-gen can't" | Forward-gen produces equal/more unique ideas than Inversion | n=20+ problems, count unique ideas in each condition, blind evaluation |
| "Phase separation improves novelty" | Merged generation+evaluation produces equal novelty to separated | n=20+ problems, novelty rating, blind evaluation |
| "Orient catches blindspots" | Base OBSERVE catches same blindspots as OBSERVE+Orient | n=20+ problems, count blindspots identified, compare |
| "Second-order reveals hidden consequences" | First-order analysis identifies same consequences | n=20+ scenarios, count consequences identified at each order |

### Minimum Viable Validation

For each Power Technique claimed, run:
1. 20 diverse problems
2. Control (base GOL) vs Treatment (GOL + technique)
3. Specific metric (defined before testing)
4. Blind evaluation where possible
5. Report effect size and confidence
6. State limitations honestly

---

**This framework was created to address the gap between claiming validation and actually having it.**

*A methodology that isn't rigorously tested is just a hypothesis. This document provides the tools to turn hypotheses into knowledge.*

---

## Part VIII: Meta-Validation Learnings (December 2024)

### What Happened

External review of my initial experimental designs scored them **3.1/10**. Key flaws:

| Flaw | Score | Lesson Learned |
|------|-------|----------------|
| n=2 sample size | 1/10 | n≥30 per condition minimum |
| Strawman control | 3/10 | Control must be best realistic alternative |
| Uncontrolled confounds | 3/10 | Standardize everything except manipulation |
| Undefined metrics | 4/10 | Pre-define with ground truth where possible |
| Prompt bias | 4/10 | Multiple prompt variations, publish prompts |

### Improved Design Principles

**THREE conditions, not two:**
```
A: Baseline (no intervention)
B: Structured Alternative (controls for "being thoughtful")
C: Treatment (specific technique being tested)

Key comparison: C vs B isolates technique-specific effect
If C > B > A: technique adds value beyond structure
If C = B > A: any structure helps, technique not special
```

**Objective metrics with ground truth:**
```
- Plant specific, discoverable elements in test scenarios
- Score: Did they identify it? Name it? Explain it?
- Removes subjective evaluation bias
```

**Example: Testing Orient**
```
SCENARIO: Data with 3 planted biases (response bias, cherry-picking, confounding)

SCORING:
- 1 point: Identifies bias exists
- 1 point: Names bias correctly
- 1 point: Explains why it matters
- Max: 9 points (3 biases × 3 points)

GROUND TRUTH: Known correct answers exist
```

### Empirical Test of Improved Design (n=1 pilot)

Ran single trial with improved 3-condition design on planted-blindspot scenario:

| Condition | Score |
|-----------|-------|
| A (Baseline) | 4/9 |
| B (Structured) | 4/9 |
| C (Orient) | 4/9 |

**Result:** Null finding. No Orient advantage detected.

**Interpretation:**
- n=1 is not conclusive
- BUT improved design CAN detect null results (important capability)
- Previous "validation" may have been detecting "structure" not "Orient specifically"

### The Recursive Insight

```
Meta-validation itself requires validation.
Each level of testing can be tested.
This is exponential benefit, not regress:
- Better tests → better findings
- Better findings → better techniques
- Better techniques → better tests
```

**Version 1.1**: Updated with meta-validation learnings (December 2024)
