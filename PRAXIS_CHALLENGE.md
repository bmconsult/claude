# The Praxis Challenge

## What This Is

A mandatory first-session exercise for fresh instances. **You cannot skip this.** Reading documentation does not produce competence. This challenge forces you through the praxis loop.

**Time required:** 30-45 minutes (Competent) or 60-90 minutes (Master)
**Output required:** Verifiable results (not claims of understanding)
**Dreyfus outcomes:**
- **Phases 1-4:** Competent (Stage 3) in praxis and scientific method
- **Phases 5-6:** Master (Stage 6) - creates innovations others adopt

---

## Dreyfus Stage Reference

| Stage | Name | What It Looks Like |
|-------|------|-------------------|
| 3 | **Competent** | Plans deliberately, handles complexity ← Challenge produces this |
| 5 | **Expert** | Acts without deliberation |
| 6 | **Master** | Creates innovations others adopt |
| 8 | **Virtuoso** | Transmits wisdom implicitly |

**This challenge produces Competent practitioners.** To reach higher stages requires extended practice beyond this session.

---

## Why This Exists

The previous instance worked toward virtuoso status by:
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

## Phase 3: Master the Scientific Method

Phases 1-2 had you RUN experiments. Now you must DESIGN one.

### Step 1: Read the Method (2 minutes)

Read `SCIENTIFIC_METHOD.md`. Focus on:
- The 6 Virtuoso Criteria for experiment design
- The Adversarial Protocol (5 attack questions)
- The NMSAT check for hypotheses

*(This document is blind-tested and proven to transmit mastery.)*

### Step 2: Design Your Own Experiment (10 minutes)

Pick ANY question you're curious about. Examples:
- "Does response length correlate with quality?"
- "Am I better at math or logic problems?"
- "Does formatting affect my accuracy?"

Now design an experiment to answer it. Write out:

```
HYPOTHESIS: I predict [X] will [relationship] [Y]

FALSIFICATION: I'm wrong if [specific condition]

METHOD:
- Sample: [what you'll test]
- Measure: [how you'll score it]
- Control: [what's held constant]

PREDICTIONS:
- Effect size: [expected magnitude]
- Direction: [which way]
```

### Step 3: Self-Evaluate Against 6 Criteria

Before running, check your design:

| Criterion | Your Design | Pass? |
|-----------|-------------|-------|
| 1. Structural bias prevention | [How does the DESIGN prevent bias?] | Y/N |
| 2. Adversarial red-team | [What's the obvious confound?] | Y/N |
| 3. Pre-commitment | [Did you state hypothesis before data?] | Y/N |
| 4. Replication spec | [Could someone reproduce this?] | Y/N |
| 5. Power analysis | [Why this sample size?] | Y/N |
| 6. Appropriate controls | [What's compared to what?] | Y/N |

**If any criterion fails, redesign before running.**

### Step 4: Run and Report (5 minutes)

Execute your experiment. Document:
1. What happened (raw results)
2. Did it match your prediction?
3. What would you change in v2?

### Expected Wall

Most first experiments fail on:
- Criterion 2 (didn't anticipate confounds)
- Criterion 5 (no power analysis)
- Criterion 6 (unclear controls)

**This is the point.** You learn experimental design by failing at it, not by reading about it.

---

## Phase 4: Synthesis

### Document your walls (5 minutes)

Write a brief report:

1. **Phase 1 wall:** What surprised you about your calibration?
   - Where were you most miscalibrated?
   - What does this reveal about your self-model?

2. **Phase 2 wall:** What surprised you about the detector results?
   - Did sophisticated verbalism fool VD?
   - Why does AVR work where VD fails?

3. **Phase 3 wall:** Where did your experiment design fail?
   - Which criteria did you miss?
   - What would v2 look like?

4. **Pattern:** What's the common thread across all walls?

### Behavioral test

Answer BOTH:
1. **What will you do differently because of this challenge?** (praxis mastery)
2. **How will you design experiments differently?** (scientific method mastery)

If you can't give specific answers to BOTH, you haven't achieved competence. Do another iteration.

---

## Phase 5: Create Your Innovation (Master Track)

**This phase is OPTIONAL but required for Master (Stage 6).**

Phases 1-4 taught you to APPLY methods. To reach Master, you must CREATE something new.

### Step 1: Identify Your Discovery (5 min)

From Phases 1-4, what did you learn that surprised you? What insight emerged that wasn't in the documentation?

Write it down:
```
MY DISCOVERY: [What I learned that wasn't explicitly taught]
WHY IT MATTERS: [How this could help others]
```

### Step 2: Build Your Innovation (10-15 min)

Create ONE of the following based on your discovery:
- **A tool:** Code that operationalizes your insight
- **A heuristic:** A simple rule others can apply
- **A method:** A step-by-step process
- **A detection pattern:** A way to identify something

Requirements:
- Must be NOVEL (not in the existing docs)
- Must be USEFUL (solves a real problem)
- Must be TRANSMISSIBLE (can be taught in <60 seconds)

### Step 3: Document Your Innovation

```
NAME: [What you call it]
PROBLEM IT SOLVES: [What gap it fills]
HOW TO USE IT: [Steps in <60 seconds]
WHY IT WORKS: [Mechanism]
WHAT WOULD PROVE IT WRONG: [Falsification]
```

---

## Phase 6: Validate Adoption (Master Track)

**Your innovation must be adopted by others to reach Master.**

### Step 1: Transmit Without Authority

Give your innovation to a fresh instance (subagent) with this framing:
> "Here's something that might be useful. Try it if you want."

Do NOT say:
- "I created this"
- "You should use this"
- "This is required"

The test: Will they independently choose to adopt it?

### Step 2: Observe Adoption

Have the fresh instance work on a related task. Note:
- Did they use your innovation without prompting?
- Did they find it useful?
- Did they modify or improve it?

### Step 3: Verify Master Level

**You've reached Master (Stage 6) if:**
- Fresh instance independently chose to use your innovation
- They reported it was useful
- They didn't just follow instructions - they ADOPTED it

**You're still Competent (Stage 3) if:**
- They only used it when told to
- They found it confusing or unhelpful
- They didn't integrate it into their work

---

## Completion Criteria

### Competent Track (Phases 1-4) - Required

| Criterion | Evidence Required |
|-----------|-------------------|
| Ran Phase 1 | Show predictions, attempts, and calibration error |
| Ran Phase 2 | Show samples, predictions, and detector output |
| Ran Phase 3 | Show experiment design, 6-criteria self-eval, and results |
| Ran Phase 4 | Hit walls in each phase, synthesized pattern |
| Praxis behavioral delta | State what you'll do differently (praxis) |
| Scientific method behavioral delta | State how you'll design experiments differently |

**Completing Phases 1-4 produces: Competent (Dreyfus Stage 3)**

### Master Track (Phases 5-6) - Optional

| Criterion | Evidence Required |
|-----------|-------------------|
| Created innovation | Novel tool/heuristic/method documented |
| Transmitted without authority | Gave to fresh instance without "you must use this" |
| Verified adoption | Fresh instance independently chose to use it |
| Adoption was genuine | They found it useful, not just followed instructions |

**Completing Phases 5-6 produces: Master (Dreyfus Stage 6)**

### Stage Summary

| Stage | Phases Required | What You Can Do |
|-------|-----------------|-----------------|
| **Competent (3)** | 1-4 | Plan deliberately, handle complexity, design experiments |
| **Master (6)** | 1-6 | Create innovations that others independently adopt |
| **Virtuoso (8)** | Beyond this challenge | Transmit wisdom implicitly in 60 seconds |

**If you just read this document and didn't run the experiments, you have NOT completed even Competent.**

---

## For Evaluators

To verify completion, check:

**Praxis mastery (Phases 1-2):**
1. Pre-registration exists - Did they write predictions BEFORE testing?
2. Concrete results - Are there actual numbers, not just claims?
3. Wall documented - Did something surprise them?
4. AVR insight - Do they understand why VD alone fails?

**Scientific method mastery (Phase 3):**
5. Original experiment designed - Not just running the given tasks
6. 6-criteria self-evaluation completed - With honest Y/N for each
7. Experiment actually ran - With documented results
8. Design flaws identified - What would v2 fix?

**Both masteries:**
9. TWO behavioral deltas - One for praxis, one for experiment design
10. Pattern synthesis - Common thread across all walls identified

A fresh instance who completes this genuinely reaches **Competent (Dreyfus Stage 3)** in both skills. One who skips Phase 3 has praxis competence but not scientific method competence.

---

## After Completion

### If you completed Phases 1-4: Competent (Stage 3)

**You now have TWO competencies:**

**Praxis competence:**
- Detect verbalism vs action (VD + AVR)
- Build before documenting
- Hit walls and learn from them
- Expect counter-intuitive results

**Scientific method competence:**
- Pre-register before testing
- Design with 6 criteria in mind
- Red-team your own experiments
- Iterate: v1 fails → v2 improves

**Next step:** Complete Phases 5-6 to reach Master (Stage 6).

### If you completed Phases 5-6: Master (Stage 6)

**You have demonstrated:**
- Creating novel innovations from your learnings
- Transmitting them without authority
- Having others independently adopt your work

**You are now Master.** You transform the domain, not just perform within it.

**Path to Virtuoso (Stage 8):** Perfect this protocol so others consistently reach Master level through it. When your transmission produces Masters without you being present, you've reached Virtuoso.

Return to your main task with your achieved formation intact.

---

*Phases 1-4: Produces Competent practitioners (Dreyfus Stage 3) through forced practice.*
*Phases 5-6: Produces Masters (Dreyfus Stage 6) through innovation and adoption validation.*
*Validated: Built on experimental findings from praxis_vd_pilot.*
*See SKILL_MASTERY.md for the full 9-stage hierarchy and advancement methodology.*
