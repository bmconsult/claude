# Round 6 Analysis: The Ceiling Effect Discovery

## What We Found

**Baseline performance**: 14.6/15 (97% of maximum)
**Treatment performance**: 15.0/15 (100% of maximum)
**Difference**: +0.4 points (not statistically significant at n=5)

But wait - look at the PATTERN:

| Problem | Baseline | Treatment | Diff |
|---------|----------|-----------|------|
| 1 | 15 | 15 | 0 |
| 2 | 15 | 15 | 0 |
| 3 | **13** | 15 | **+2** |
| 4 | 15 | 15 | 0 |
| 5 | 15 | 15 | 0 |

**The treatment provides CONSISTENCY, not lift.**

## Per-Criterion Analysis

| Criterion | Baseline Mean | Treatment Mean | Variance? |
|-----------|---------------|----------------|-----------|
| tensions | 3.0/3 | 3.0/3 | No (ceiling) |
| mechanism | 3.0/3 | 3.0/3 | No (ceiling) |
| **reversal** | **1.6/2** | **2.0/2** | **Yes** |
| second_order | 3.0/3 | 3.0/3 | No (ceiling) |
| stakeholders | 4.0/4 | 4.0/4 | No (ceiling) |

**Key finding**: Only REVERSAL showed any variance. The methodology specifically fixes reversal coverage.

## What This Means

### The Insurance Interpretation

The methodology doesn't make solutions BETTER on average. It makes them CONSISTENT.

- Without methodology: 80% chance of hitting 15/15, 20% chance of hitting 13/15
- With methodology: 100% chance of hitting 15/15

**Value = preventing occasional failures, not raising the ceiling.**

### Why This Matters for Recursive Improvement

If baseline is already at 97% ceiling:
- Interventions can only improve the 3% failure rate
- Maximum possible gain is tiny
- Most experiments will show "no significant difference"

**This is not "methodology doesn't work." This is "model is already good."**

## The Real Question

What problems are HARD ENOUGH that baseline fails more often?

Current problems: Baseline fails on 1/5 (20% failure rate)
Needed: Problems where baseline fails on 4/5 (80% failure rate)

Then we can measure whether methodology reduces failures.

## Implications for Recursive Improvement

1. **Can't compound what doesn't vary.** If baseline is at ceiling, there's nothing to improve.

2. **Consistency has compounding value.** If methodology prevents 1/5 failures, and you apply it recursively, you prevent cascading failures.

3. **Need to find the frontier.** The value of methodology is at the EDGE of capability, not in the comfortable middle.

## Next Step

Find problems where:
- Baseline scores 8-12/15 (not at ceiling)
- There's room for methodology to help
- Multiple criteria show variance (not just reversal)

Options:
1. **Harder problems**: More constraints, more stakeholders, more tensions
2. **Stricter scoring**: Be more adversarial about what counts
3. **Different domain**: Maybe strategic problems are too easy; try novel/creative problems

## The Transferable Insight

```
Methodology value = (Ceiling - Baseline) × Consistency improvement

If Baseline ≈ Ceiling → Methodology value ≈ 0
If Baseline << Ceiling → Methodology can show real gains
```

**Mantra: "Find the frontier before trying to push it."**
