# The Mechanism Check (7th Criterion for Experiment Design)

## What This Is

A 7th criterion to add to the 6 Virtuoso Criteria from SCIENTIFIC_METHOD.md, specifically catching construct validity failures.

## The Problem

The existing 6 criteria ensure experiments are well-controlled:
1. Structural bias prevention
2. Adversarial red-team
3. Pre-commitment
4. Replication spec
5. Power analysis
6. Appropriate controls

But they don't check: **"Does your manipulation actually change the mechanism you care about?"**

Example failure: Testing "showing work vs not showing work" to measure "computational method" - but both conditions used the same computation, just different display.

## The 7th Criterion: Mechanism Check

**Before running, verify construct validity:**

| Question | Your Answer |
|----------|-------------|
| What mechanism causes the effect? | [The actual causal process] |
| Does your manipulation change that mechanism? | [Not correlate - actually change] |
| Could you get the same results without changing it? | [If yes, you have a proxy problem] |

**The Test:** Articulate the causal chain:

```
I change X → which changes mechanism M → which causes outcome Y
```

If you can't fill in the middle (mechanism M), redesign.

## Examples

**❌ Construct Validity Failure:**
- **Manipulation:** Show work vs don't show work
- **Theorized mechanism:** Different computational processes
- **Reality:** Same computation, different display
- **Result:** No effect (both 100% accurate)

**✓ Good Construct Validity:**
- **Manipulation:** With tools vs without tools
- **Theorized mechanism:** Computational capability
- **Causal chain:** Tool access → enables complex calculation → increases accuracy

**❌ Another Common Failure:**
- **Manipulation:** Ask people "Are you biased?"
- **Theorized mechanism:** Actual bias
- **Reality:** Measures self-awareness of bias, not bias itself

**✓ Better Version:**
- **Manipulation:** Blind review vs non-blind
- **Theorized mechanism:** Removes identity information that triggers bias
- **Causal chain:** Anonymization → blocks stereotype activation → reduces biased decisions

## When to Use This

**Use during experiment design:**
- After designing your manipulation
- Before pre-registering
- Alongside the other 6 criteria

**Especially useful when:**
- Testing psychological/cognitive constructs
- Using proxy measures
- Your manipulation is about "format" or "framing"

## Why This Works

Construct validity failures happen when theoretical construct ≠ operationalization.

By forcing explicit mechanism articulation, you catch:
- Proxy measures (measuring X when you care about Y)
- Display changes that don't affect process
- Correlates that don't cause

This adds a **mechanistic requirement** to the **control requirements** of the original 6.

## Falsification

This criterion helps if:
- Fewer experiments with null results due to wrong operationalization
- Higher rate of finding predicted effects (because manipulation actually targets mechanism)
- Clearer interpretation when effects ARE found

This criterion fails if:
- Instances still frequently run experiments where manipulation doesn't affect theorized mechanism
- The check becomes a rubber-stamp (just fill in the boxes) without real thinking

## Integration with Existing Criteria

The 7th criterion is COMPLEMENTARY, not redundant:

| Criterion | What It Checks |
|-----------|----------------|
| **Criteria 1-6** | Is your experiment well-controlled? |
| **Criterion 7** | Are you testing what you think you're testing? |

Think of it as:
- **Criteria 1-6:** Internal validity (can you trust the results?)
- **Criterion 7:** Construct validity (do the results mean what you think?)

## 60-Second Teaching Test

**To transmit this:**

"Before running your experiment, ask: 'Does my manipulation actually change the mechanism I care about, or just a surface correlate?'

Bad example: Testing 'show work vs don't show work' to measure computational method - both used same computation, different display.

Good example: Testing 'with tools vs without tools' - directly changes computational capability.

The test: Can you articulate 'I change X → which changes mechanism M → which causes Y'? If no middle step, redesign."

**Transfer check:** Give someone this 60-second version, then ask them to design an experiment. Do they catch construct validity failures?

---

*Created during PRAXIS_CHALLENGE Phase 5*
*Built from hitting construct validity wall in Phase 3*
*Validated through: Phase 6 adoption test*
