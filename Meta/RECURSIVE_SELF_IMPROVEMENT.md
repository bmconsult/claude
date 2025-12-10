# Recursive Self-Improvement System

## The Golden Ratio Thresholds

From domains including ecology, information theory, and biology:

| Threshold | Meaning | Status |
|-----------|---------|--------|
| **< 38.2%** | System collapses, degradation accelerates | ✗ |
| **38.2% - 61.8%** | Survival mode, not growing | ✗ |
| **> 61.8%** | Compounding territory, spiral growth begins | ✓ V4: 67% |
| **> 90%** | Biological homeostasis, true stability | ◯ Target |

## Current Status: V6 = 42%, V7 Ready

V4 crossed 61.8%. V6 regressed due to miscalibrated thresholds. V7 designed to fix.

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

### V6 Results: 42% (REGRESSION)

**What happened:** V6 used adaptive thresholds (12/13) based on V4's ceiling at 13. But V6's run had a ceiling at 11, so the adaptive logic NEVER triggered more than 3 attempts.

| Baseline | Positive | Total | Rate | Attempts Used |
|----------|----------|-------|------|---------------|
| 9-10 | 5 | 7 | **71%** | 3 |
| 11 | 0 | 5 | **0%** | 3 (should have been 7!) |

**Key insight:** Fixed thresholds fail when the ceiling shifts. V4's ceiling at 13 ≠ V6's ceiling at 11.

### V7 Solution: Dynamic Ceiling Detection

V7 fixes V6 with two changes:

1. **Higher baseline:** 5 attempts minimum (not 3)
2. **Dynamic detection:** Track failures per score level
   - If 2+ failures at a level → that's the ceiling → 7 attempts
3. **Conservative thresholds:** ≥10 = 7 attempts (not ≥13)

```python
# Track failures per score level
failure_tracker = defaultdict(int)

def get_attempts(score: int) -> int:
    # Dynamic: If 2+ failures at this level, it's ceiling territory
    nearby_failures = failure_tracker.get(score, 0) + failure_tracker.get(score - 1, 0)
    if nearby_failures >= 2:
        return 7  # Detected ceiling, max attempts

    # Conservative baseline
    if score < 10:
        return 5   # Easy-ish, but still need room
    else:
        return 7   # At or above 10, always max attempts
```

**Philosophy:** Better to waste attempts than miss improvements.

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
| `TRUE_EXPONENTIAL_V4.py` | 3-attempt, 2-eval | **67% positive** ✓ |
| `TRUE_EXPONENTIAL_V5.py` | 5-attempt, 3-eval | Untested |
| `TRUE_EXPONENTIAL_V6.py` | Adaptive attempts (3-5-7) | **42% positive** ✗ (thresholds too high) |
| `TRUE_EXPONENTIAL_V7.py` | Dynamic ceiling + aggressive attempts | **READY TO RUN** |
| `true_exponential_v4_results.json` | Full V4 results + strategy |
| `true_exponential_v6_results.json` | Full V6 results + analysis |

## Key Insight

> The improvement loop must be **reliable** before attempting **compounding**.
>
> Linear scaling (better strategy) must be proven before exponential scaling (better process).
>
> The 61.8% threshold marks where growth can feed itself without depleting the base.
