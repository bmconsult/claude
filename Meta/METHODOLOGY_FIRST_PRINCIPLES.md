# Problem-Solving Methodology: First Principles Derivation

## The Meta-Problem

**Goal**: Create the best possible problem-solving methodology for LLMs.

**Recursive requirement**: The method for creating methods must itself improve with each iteration, producing literal exponential growth.

---

## STEP 1: First Principles - What IS Problem-Solving?

### Definition
```
Problem-solving = transforming (Problem State) → (Solution State)
                  subject to (Constraints)
                  through (Operations)
```

### Decomposition

| Component | What It Is | LLM Analog |
|-----------|------------|------------|
| Problem State | Current situation + what's wrong | Input context |
| Solution State | Desired outcome | Generated output |
| Constraints | Rules that must be satisfied | Evaluation criteria |
| Operations | Valid transformations | Reasoning steps |

### The Core Question
**What determines whether an LLM produces a good solution?**

Possible factors:
1. **Information access** - Does it have all relevant facts?
2. **Constraint awareness** - Does it know all the rules?
3. **Operation selection** - Does it choose the right reasoning steps?
4. **Verification** - Does it check its work?
5. **Search strategy** - Does it explore the right parts of solution space?

---

## STEP 2: Dimensions of Methodology Quality

A methodology is "good" if it improves problem-solving. But on WHAT dimensions?

### Candidate Dimensions

| Dimension | Definition | Measurement |
|-----------|------------|-------------|
| **Accuracy** | Correct solutions | % correct on test set |
| **Depth** | Considers non-obvious factors | Expert rating 1-10 |
| **Breadth** | Covers multiple angles | Count of distinct considerations |
| **Robustness** | Works across problem types | Variance across domains |
| **Efficiency** | Minimal wasted effort | Token count / quality |
| **Transferability** | Works for other LLMs | Cross-model validation |

### Which Dimensions Matter Most?

**Hypothesis**: Accuracy and Depth are primary; others are secondary.

**Rationale**:
- A methodology that's fast but wrong is useless
- A methodology that's shallow misses the point
- Breadth without depth is superficial coverage

**Testable prediction**: Improvements on Accuracy and Depth will correlate with improvements on secondary dimensions.

---

## STEP 3: Theoretical Mechanism - WHY Do Prompts Help?

### The Fundamental Question
Why would adding text to a prompt change the quality of reasoning?

### Candidate Mechanisms

#### Mechanism 1: Attention Steering
**Theory**: Prompts direct attention to specific features that would otherwise be ignored.

**Prediction**: Effective prompts will name specific features to attend to (e.g., "reversals", "second-order effects").

**Test**: Compare prompts that name features vs. prompts that give general instructions.

#### Mechanism 2: Constraint Activation
**Theory**: Prompts activate latent knowledge about constraints that isn't triggered by the problem alone.

**Prediction**: Prompts work by making implicit constraints explicit.

**Test**: Compare solutions with/without constraint prompts; measure constraint satisfaction.

#### Mechanism 3: Search Space Shaping
**Theory**: Prompts shape which parts of solution space get explored.

**Prediction**: Effective prompts will direct search toward high-value regions.

**Test**: Analyze solution diversity with different prompts.

#### Mechanism 4: Verification Forcing
**Theory**: Prompts force verification steps that wouldn't happen by default.

**Prediction**: Prompts that require explicit checking will catch more errors.

**Test**: Compare error rates with/without verification prompts.

### Most Likely Mechanism

**Working hypothesis**: Mechanism 1 (Attention Steering) + Mechanism 4 (Verification Forcing) are primary.

**Evidence from v5.2-VR**: The "reversal" prompt worked by steering attention to a specific feature (how success creates opposite outcomes) that wasn't being considered by default.

---

## STEP 4: Derivation of Optimal Methodology Structure

### From First Principles

If problem-solving = (State → State) through (Operations) subject to (Constraints), then a methodology should:

1. **Ensure complete problem representation** - All relevant state is captured
2. **Activate all relevant constraints** - Nothing is forgotten
3. **Guide operation selection** - Right reasoning steps in right order
4. **Force verification** - Check that constraints are satisfied

### Structural Requirements

| Requirement | Derived From | Implementation |
|-------------|--------------|----------------|
| Problem decomposition | Complete representation | "Break into components" |
| Constraint enumeration | Constraint activation | "List all constraints" |
| Multi-step reasoning | Operation selection | "Consider X, then Y, then Z" |
| Explicit checking | Verification | "Verify against each constraint" |

### What's Missing in Current v5.2?

Analyzing v5.2 against these requirements:

| Requirement | v5.2 Status | Gap |
|-------------|-------------|-----|
| Problem decomposition | Implicit | Not explicitly prompted |
| Constraint enumeration | Partial | Only some constraints named |
| Multi-step reasoning | Good | CLARIFY → DEPTH → VERIFY |
| Explicit checking | Good | Verification step exists |

**Hypothesis**: Adding explicit problem decomposition will improve accuracy.

---

## STEP 5: Generating Hypotheses

Using the validated Hypothesis Generation protocol (Novel, Mechanistic, Specific, Actionable, Testable):

### Hypothesis 1: Decomposition Prompt
**Claim**: Adding "Break the problem into independent sub-problems before solving" will increase accuracy by 10-20%.

**Mechanism**: Reduces cognitive load, ensures no component is missed.

**Test**: A/B test with/without decomposition prompt on 20 problems.

**Falsification**: If accuracy doesn't improve OR decreases, hypothesis is wrong.

### Hypothesis 2: Constraint Enumeration
**Claim**: Adding "List ALL constraints (explicit and implicit) before generating solutions" will increase accuracy by 5-15%.

**Mechanism**: Activates constraint knowledge that would otherwise be dormant.

**Test**: A/B test, measure constraint violation rate.

**Falsification**: If constraint violations don't decrease, mechanism is wrong.

### Hypothesis 3: Feature Attention (Generalized Reversal)
**Claim**: Prompts that name SPECIFIC features to attend to (not general instructions) will outperform vague prompts by 15-25%.

**Mechanism**: Attention steering requires specific targets.

**Test**: Compare "consider consequences" vs "consider how success creates failure".

**Falsification**: If specific and vague perform equally, mechanism is wrong.

### Hypothesis 4: Verification Granularity
**Claim**: Fine-grained verification ("check each constraint individually") will outperform coarse verification ("make sure solution is good") by 10-20%.

**Mechanism**: Coarse verification misses specific failures.

**Test**: A/B test verification styles on problems with multiple constraints.

**Falsification**: If error rates are equal, granularity doesn't matter.

---

## STEP 6: Experiment Design (Six Virtuoso Criteria)

### Experiment 1: Testing Hypothesis 1 (Decomposition)

**Question**: Does explicit decomposition improve problem-solving accuracy?

**Design**: Within-subject, randomized order

**Conditions**:
- Control: v5.2-VR (current best)
- Treatment: v5.2-VR + "First, break this problem into independent sub-problems"

**Measures**:
- Primary: Total score (1-50 scale)
- Secondary: Per-dimension scores

**Controls**:
- Same problems for both conditions
- Randomized presentation order
- Same evaluator prompt
- Blind evaluation (evaluator doesn't know condition)

**N**: 20 problems (power analysis: d=0.5 requires n≈16 for 80% power)

**Pre-registration**:
- H0: No difference in means
- H1: Treatment mean > Control mean
- Alpha: 0.05
- Falsification: If Treatment ≤ Control, reject hypothesis

**Adversarial check**:
- Confound: Longer prompts might help regardless of content → Add length-matched control
- Alternative explanation: More structure helps → Test structure without decomposition

---

## STEP 7: The Recursive Loop

After each experiment round:

1. **Analyze results** - What worked? What didn't?
2. **Update theory** - Revise mechanism understanding
3. **Generate new hypotheses** - Based on updated theory
4. **Improve experiment design** - Learn from methodological issues
5. **Apply improved method to step 1** - The method for analyzing results improves

### The Exponential Part

Each round:
- Better theory → better hypotheses
- Better hypotheses → more targeted experiments
- Better experiments → cleaner results
- Cleaner results → better theory
- Better method-making → faster improvement

**Compounding**: Round N's methodology is better than Round N-1's methodology for MAKING methodologies.

---

---

## ROUND 1 RESULTS: Decomposition Hypothesis

**Experiment completed**: 2025-12-10

### Raw Data

| Condition | Mean | n |
|-----------|------|---|
| Control (v5.2-VR) | 8.15 | 20 |
| Treatment (v5.3-D) | 8.15 | 20 |
| Placebo (length-matched) | 8.05 | 20 |

**Effect: +0.00 points**
**Cohen's d: 0.000**

### Verdict: HYPOTHESIS NOT SUPPORTED

### Analysis

1. **Ceiling effect confirmed**: 16/20 problems scored exactly 8 across all conditions
2. **No length confound**: Placebo (8.05) ≈ Control (8.15)
3. **Decomposition adds no value** at this difficulty level

### Theory Update

The null result requires updating our theoretical model:

**Original assumption**: Decomposition would help by ensuring no component is missed.

**Revised understanding**:
- v5.2-VR already achieves near-ceiling performance (8.15/10)
- At ceiling, additional prompting adds overhead without benefit
- The "reversal" prompt in v5.2-VR may already be capturing the value that decomposition would provide

### Implications for Next Round

1. **Need harder problems** - Current problems don't differentiate
2. **Need different interventions** - Decomposition hypothesis was wrong
3. **Consider measurement granularity** - 1-10 may not be sensitive enough

### The Recursive Improvement

This null result improves the METHOD for making methods:

| Learning | Application |
|----------|-------------|
| Ceiling effects hide differences | Use harder problems in future |
| Theoretical derivation ≠ empirical effect | Always test, never assume |
| Length confound was NOT present | Can simplify future designs |
| 20 problems at 60 API calls is expensive | Consider more efficient designs |

---

## ROUND 2 DESIGN (Updated)

Based on Round 1 learning, Round 2 should:

1. **Use harder problems** that current baseline can't solve at ceiling
2. **Test different mechanisms** - decomposition failed, try constraint enumeration
3. **Improve efficiency** - reduce API calls per round

### Candidate Harder Problems

Problems where the solution is non-obvious and requires synthesis:
- Multi-constraint optimization with tradeoffs
- Temporal dynamics (short vs long term conflict)
- Multi-stakeholder with genuinely opposed interests
- Novel situations with no clear precedent

### Alternative Hypothesis: Constraint Enumeration

Since decomposition failed, test Hypothesis 2:

**Claim**: Adding "List ALL constraints (explicit and implicit) before generating solutions" will improve accuracy on constraint-heavy problems.

**Prediction**: Treatment will beat control on problems with >3 implicit constraints.

**Efficiency improvement**: Test on 10 problems instead of 20 (if effect is real, should be visible at n=10).

---

## Meta-Tracking

| Round | Focus | Result | Method-Making Improvement |
|-------|-------|--------|---------------------------|
| 0 | Ad-hoc v5.2 development | Mixed | None (baseline) |
| 1 | Decomposition hypothesis | NULL (d=0.0) | Learned: ceiling effects, efficiency |
| 2 | TBD | TBD | TBD |

*Each row should show improvement in the rightmost column.*
