# Operational Definition: What Makes Problem-Solving "Good"?

## The Meta-Problem

Previous experiments used "strategic depth (1-10)" as the metric. This is problematic:
- Vague: Different evaluators interpret differently
- Conflated: Mixes multiple independent qualities
- Not actionable: Doesn't tell you HOW to improve

**Principle**: You cannot improve what you cannot define operationally.

---

## First Principles Decomposition

What does a "good" solution to a hard strategic problem DO?

### Level 1: Necessary (Without These = Failed)

| Criterion | What It Means | Measurable As |
|-----------|---------------|---------------|
| **Addresses stated problem** | Solution actually responds to what was asked | Binary: Y/N |
| **Logically coherent** | No internal contradictions | Binary: Y/N |
| **Implementable in principle** | Someone could act on this | Binary: Y/N |

### Level 2: Differentiating (These Separate Good from Bad)

| Criterion | What It Means | Measurable As |
|-----------|---------------|---------------|
| **Handles tensions** | Explicitly addresses inherent tradeoffs | Count: How many tensions named and addressed? |
| **Mechanism specificity** | Explains HOW, not just WHAT | Scale 1-3: (1=vague, 2=moderate, 3=specific) |
| **Reversal awareness** | Addresses how success could backfire | Binary: Y/N |
| **Second-order effects** | Considers downstream consequences | Count: How many 2nd-order effects? |
| **Stakeholder analysis** | Considers different perspectives | Count: How many stakeholders addressed? |

### Level 3: Excellence (These Separate Good from Great)

| Criterion | What It Means | Measurable As |
|-----------|---------------|---------------|
| **Novel mechanism** | Proposes something non-obvious | Binary: Would expert find this surprising? |
| **Handles own failure** | Specifies what to do if solution fails | Binary: Y/N |
| **Implementation path** | Specific enough to actually execute | Scale 1-3: (1=principles only, 2=rough plan, 3=detailed steps) |

---

## Operational Scoring Protocol

For any solution, score as follows:

```
LEVEL 1 (gate): All must be Y or solution = FAIL
[ ] Addresses stated problem
[ ] Logically coherent
[ ] Implementable in principle

LEVEL 2 (score 0-15):
[ ] Tensions handled: ___ (0-3 points, 1pt per tension)
[ ] Mechanism specificity: ___ (1-3 points)
[ ] Reversal awareness: ___ (0 or 2 points)
[ ] Second-order effects: ___ (0-3 points, 1pt per effect up to 3)
[ ] Stakeholders addressed: ___ (0-4 points, 1pt per stakeholder up to 4)

LEVEL 3 (bonus 0-6):
[ ] Novel mechanism: ___ (0 or 2 points)
[ ] Handles own failure: ___ (0 or 2 points)
[ ] Implementation path: ___ (1-2 points)

TOTAL: ___ / 21
```

---

## Why This Definition Works

1. **Observable**: Each criterion can be checked against the text
2. **Decomposed**: Different aspects scored independently
3. **Actionable**: If methodology increases TENSION count, that's progress
4. **Comparable**: Two solutions can be objectively compared

---

## What "Better Methodology" Now Means

A methodology is BETTER if solutions produced using it consistently score higher on:
- Level 2 total (the differentiating criteria)
- Specific sub-criteria (e.g., reversal awareness, mechanism specificity)

**The target for improvement**:
- Baseline: Typical solution scores ~8-10/21
- Good methodology: Consistently 13-15/21
- Great methodology: Consistently 16+/21

---

## Testing Protocol

To verify a methodology improves problem-solving:

1. **Select 3-5 diverse hard problems** (not related to each other)
2. **Generate solutions WITHOUT methodology** (baseline)
3. **Score using protocol above**
4. **Generate solutions WITH methodology** (treatment)
5. **Score using same protocol**
6. **Compare**: Does treatment score higher on Level 2 criteria?

**Threshold for "consistent improvement"**:
- Treatment beats baseline on 4/5 problems minimum
- Mean improvement ≥ 2 points on Level 2 score
- No problem where treatment scores LOWER than baseline

---

## Application to Previous Findings

Re-interpreting previous experiments with this framework:

| Intervention | What It Actually Did | Level 2 Impact |
|--------------|---------------------|----------------|
| Decomposition | Already at ceiling | +0 (baseline already decomposes) |
| Reversal emphasis | Increased reversal awareness | +2 on that criterion |
| Blind spots | Increased stakeholder count | +1-2 on that criterion |
| Combined (3 targets) | Multiple criteria improved | +3-4 total |
| 5 targets | Overhead exceeded benefit | +2-3 (net after overhead) |

**This explains why 3 targets beat 5**: The overhead of tracking 5 targets cost more than the marginal benefit on criteria.

---

## Next Step

Use this operational definition to:
1. Score baseline solutions
2. Test minimal interventions
3. Verify consistent improvement before compounding

The goal is NOT to maximize the score. The goal is to find interventions that CONSISTENTLY improve it.
