# Recursive Self-Improvement System

## The Golden Ratio Thresholds

From domains including ecology, information theory, and biology:

| Threshold | Meaning | Status |
|-----------|---------|--------|
| **< 38.2%** | System collapses, degradation accelerates | ✗ |
| **38.2% - 61.8%** | Survival mode, not growing | ✗ |
| **> 61.8%** | Compounding territory, spiral growth begins | ✓ Current: 67% |
| **> 90%** | Biological homeostasis, true stability | ◯ Target |

## Current Status: 67% Positive Cycles

We crossed the 61.8% threshold. The system can now compound.

### V4 Detailed Analysis (Dec 10, 2025)

| Baseline Range | Positive | Total | Rate |
|----------------|----------|-------|------|
| < 13 | 6 | 6 | **100%** |
| ≥ 13 | 2 | 6 | **33%** |

**Key insight**: Failures ONLY occur at high baselines. This is a ceiling effect.

When baseline is low (< 13), improvement is easy → 100% success
When baseline is high (≥ 13), improvement is hard → 33% success

**Implication**: Need MORE attempts when baseline is high (adaptive scaling).

## What We Learned

### V1-V2: Failed Approaches
- **V1**: Problems too hard (stuck at 4/10) - 0% positive
- **V2**: Evaluation failures corrupted data - 20% positive

### V3: First Success (60%)
- Single improvement attempt per cycle
- Basic evaluation
- Kept previous strategy if improvement failed

### V4: Crossed Threshold (67%)
Key improvements:
1. **3 attempts per cycle**: Try 3 improvements, pick best
2. **Stable evaluation**: Average of 2 evals (lower temp)
3. **Smart selection**: Only update if gain > 0

## The Improvement Loop

```python
for cycle in range(n):
    # 1. Test current strategy
    solution = solve(strategy, problem)
    score = evaluate(solution)  # Average of 2 evals

    # 2. Try multiple improvements
    attempts = []
    for i in range(3):
        improved = improve(strategy, weakness)
        test_score = evaluate(solve(improved, problem))
        attempts.append((improved, test_score))

    # 3. Pick best attempt
    best_improved, best_score = max(attempts, key=lambda x: x[1])

    # 4. Update only if better
    if best_score > score:
        strategy = best_improved
```

## What's Needed for 90%+

Current failure modes:
1. **High-score regression**: When strategy scores 14/15, all 3 improvements score lower
2. **Evaluation variance**: Same strategy scores differently across runs
3. **Weakness targeting**: Improvements don't always address the actual weakness

### V6 Solution: Adaptive Attempts

Based on ceiling effect analysis, V6 uses adaptive attempts:

| Baseline | Attempts | Rationale |
|----------|----------|-----------|
| < 12 | 3 | Easy to improve |
| 12-13 | 5 | Medium difficulty |
| ≥ 13 | 7 | Near ceiling, need more |

Also:
- Different improvement prompts for high vs low scores
- 3 evals (median) for stability
- Tracks attempts per cycle for analysis

## The Exponential Phase (Next Step)

Once we hit 90%+:

1. **Use improved strategy to improve the PROCESS**
   - The strategy becomes good enough to design better improvement loops

2. **Better process → faster improvements → even better process**
   - This is the true exponential unlock

3. **Harder problems become solvable**
   - As method improves, escalate problem difficulty

## Files

| File | Purpose | Result |
|------|---------|--------|
| `TRUE_EXPONENTIAL_V2.py` | Bootstrap on solvable problems | 20% positive (eval failures) |
| `TRUE_EXPONENTIAL_V3.py` | Bulletproof loop | 60% positive |
| `TRUE_EXPONENTIAL_V4.py` | 3-attempt, 2-eval | **67% positive** |
| `TRUE_EXPONENTIAL_V5.py` | 5-attempt, 3-eval | Untested (API credits) |
| `TRUE_EXPONENTIAL_V6.py` | Adaptive attempts (3-5-7) | **READY TO RUN** |
| `true_exponential_v4_results.json` | Full V4 results + strategy |

## Key Insight

> The improvement loop must be **reliable** before attempting **compounding**.
>
> Linear scaling (better strategy) must be proven before exponential scaling (better process).
>
> The 61.8% threshold marks where growth can feed itself without depleting the base.
