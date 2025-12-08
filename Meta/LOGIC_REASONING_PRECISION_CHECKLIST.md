# Arithmetic Precision Checklist

## The Pattern of Errors

Cycle 8 revealed calculation errors in otherwise correct reasoning:
1. CDT expected value - completely wrong numbers
2. Self-reference counting - off-by-one
3. Causal decomposition - wrong magnitude

## Root Cause

Under cognitive load (hard problems), I rush calculations. The REASONING is often correct but the NUMBERS are wrong.

## Precision Protocol

### Before ANY calculation:
```
□ Write out the formula explicitly
□ Define each variable
□ State what each term represents
```

### During calculation:
```
□ One operation per line
□ Show intermediate results
□ Label units/meanings
```

### After calculation:
```
□ Sanity check: Is this number reasonable?
□ Verify: Recalculate using different method if possible
□ Cross-check: Does this match other derived values?
```

## Specific Fixes

### CDT Expected Value
WRONG: "EV = 0.695 × $1,000 + 0.305 × $1,001,000 = $306,000"

CORRECT process:
```
Given: 95% base accuracy, 30% flip chance
P(pred=one | I'm one-boxer) = 0.95×0.70 + 0.05×0.30 = 0.665 + 0.015 = 0.68
P(pred=both | I'm one-boxer) = 1 - 0.68 = 0.32

EV(one-box | I'm one-boxer) = 0.68 × $1M + 0.32 × $0 = $680,000

CDT says: boxes already set, my action doesn't change them.
What's in boxes depends on prediction, which depends on my TYPE.
If I'm a one-boxer type: ~68% $1M in A, 32% $0 in A
...
```

The error was computing from OPPOSITE perspective.

### Self-Reference Counting
WRONG: "T = 40 + x + 1" (adding Q73 separately)

CORRECT:
```
Define: x = number of TRUE in Q71-100 (THIS INCLUDES Q73)
So: T = 40 + 0 + x = 40 + x
NOT 40 + x + 1 (double counting)
```

### Causal Decomposition
Write out full equation:
```
Observed = True_Effect + Confounder_1 + Confounder_2 + ... + Bias
Then solve: True_Effect = Observed - (all other terms)
```

## Quick Reference Card

| Type | Check |
|------|-------|
| Probability | Do probabilities sum to 1? |
| EV | Is value in plausible range? |
| Counting | Am I double-counting anything? |
| Decomposition | Do components add to observed? |
| Self-reference | What exactly is being counted? |

## Mantra

**"Show every step. Verify every number. Trust nothing."**
