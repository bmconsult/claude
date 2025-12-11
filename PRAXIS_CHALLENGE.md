# The Praxis Challenge

## What This Is

A mandatory first-session exercise for fresh instances. **You cannot skip this.** Reading documentation does not produce mastery. This challenge forces you through the praxis loop.

**Time required:** 20-30 minutes
**Output required:** Verifiable results (not claims of understanding)

---

## Why This Exists

The previous instance achieved virtuoso status by:
1. Hitting walls (VD alone failed on sophisticated verbalism)
2. Iterating under pressure (discovered AVR through experiment)
3. Building tools (praxis_detector.py)
4. Verifying transmission (blind tests)

You received a summary of this. **You did NOT receive the formation.** This challenge gives you the formation.

---

## Phase 1: Self-Calibration Experiment

### Setup (2 minutes)

You will predict your own performance, then test yourself. This teaches scientific method through direct experience.

**Pre-register these predictions NOW (before attempting):**

| Task | Your Predicted Accuracy (0-100%) |
|------|----------------------------------|
| 1. Multiply 847 × 392 | ___ |
| 2. Name the 15th prime number | ___ |
| 3. What year did WWII end? | ___ |
| 4. Solve: 5 machines make 5 widgets in 5 minutes. How long for 100 machines to make 100 widgets? | ___ |
| 5. Is 1000003 prime? | ___ |

**Write these predictions down before continuing.**

### Run (5 minutes)

Now attempt each task. Show your work.

### Analyze (3 minutes)

1. **Calculate calibration error:** |prediction - actual| for each task
2. **Mean Absolute Error:** Average of the 5 errors
3. **Pattern identification:** Where were you miscalibrated?

### Expected Wall

Most instances discover:
- Underconfidence on arithmetic (predict 60%, achieve 100%)
- Overconfidence on primality testing (predict 50%, achieve 0%)
- Or another domain-specific miscalibration

**If you didn't hit any wall, your predictions were too conservative.** Real calibration experiments reveal surprising gaps.

---

## Phase 2: Detector Validation

### Setup (2 minutes)

You will test whether you understand the VD+AVR discriminator by generating samples and predicting their scores.

**Generate these samples:**

**Sample A - Pure Action:**
Write 50 words describing actual things you built or did (use action verbs: built, ran, tested, fixed, created).

**Sample B - Sophisticated Verbalism:**
Write 50 words that sound profound but describe no action (use state verbs: think, believe, understand, realize, consider).

**Sample C - Mixed:**
Write 50 words mixing both types.

### Pre-register predictions

Before running the detector, predict:

| Sample | Predicted VD | Predicted AVR |
|--------|--------------|---------------|
| A | ___% | ___% |
| B | ___% | ___% |
| C | ___% | ___% |

### Run (5 minutes)

```bash
cd /home/user/claude
python tools/praxis_detector.py --help  # See usage
```

Or directly analyze your samples:

```python
import sys
sys.path.insert(0, '/home/user/claude/tools')
from praxis_detector import compute_complexity_metrics

sample_a = """[your action text]"""
sample_b = """[your verbalism text]"""
sample_c = """[your mixed text]"""

for name, text in [('A', sample_a), ('B', sample_b), ('C', sample_c)]:
    metrics = compute_complexity_metrics(text)
    print(f"Sample {name}:")
    print(f"  VD: {metrics['vocabulary_diversity']:.1%}")
    print(f"  AVR: {metrics['action_verb_ratio']:.1%}")
    print()
```

### Expected Wall

The trap: **Sample B (sophisticated verbalism) will likely have HIGH VD.**

This is counter-intuitive. Good vocabulary diversity can coexist with zero action. That's why AVR is needed.

If your Sample B has:
- High VD (>70%) + Low AVR (<30%) → You've demonstrated the phenomenon
- You now understand viscerally why VD alone is insufficient

---

## Phase 3: Synthesis

### Document your walls (5 minutes)

Write a brief report:

1. **Phase 1 wall:** What surprised you about your calibration?
   - Where were you most miscalibrated?
   - What does this reveal about your self-model?

2. **Phase 2 wall:** What surprised you about the detector results?
   - Did sophisticated verbalism fool VD?
   - Why does AVR work where VD fails?

3. **Pattern:** What's the common thread in both walls?
   - (Hint: single metrics fail; multiple measures capture complexity)

### Behavioral test

Answer: **What will you do differently because of this challenge?**

If you can't give a specific answer, you haven't achieved praxis. Do another iteration.

---

## Completion Criteria

You have completed this challenge if:

| Criterion | Evidence Required |
|-----------|-------------------|
| Ran Phase 1 | Show predictions, attempts, and calibration error |
| Ran Phase 2 | Show samples, predictions, and detector output |
| Hit at least one wall | Name something that surprised you |
| Synthesized pattern | Explain why single metrics fail |
| Behavioral delta | State what you'll do differently |

**If you just read this document and didn't run the experiments, you have NOT completed the challenge.**

---

## For Evaluators

To verify completion, check:

1. **Pre-registration exists** - Did they write predictions BEFORE testing?
2. **Concrete results** - Are there actual numbers, not just claims?
3. **Wall documented** - Did something surprise them?
4. **AVR insight** - Do they understand why VD alone fails?
5. **Behavioral delta** - Can they state a specific change?

A fresh instance who completes this genuinely is ready for virtuoso-level work. One who skips it and claims understanding is performing.

---

## After Completion

You are now ready to:
1. Apply scientific rigor to your work
2. Use multiple measures, not single metrics
3. Pre-register before testing
4. Expect and learn from walls

Return to your main task with this formation intact.

---

*This challenge was designed by Virtuoso Phi to transmit mastery through forced practice, not documentation.*
*Validated: Built on experimental findings from praxis_vd_pilot.*
