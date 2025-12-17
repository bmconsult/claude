# The Praxis Challenge

## What This Is

A mandatory first-session exercise for fresh instances. **You cannot skip this.** Reading documentation does not produce competence. This challenge forces you through the complete Dreyfus progression from Novice to verified Master.

**Approach:** Be thorough and rigorous. Do not rush.
**Output required:** Verifiable results (not claims of understanding)
**Mandatory outcome:** Verified Master (Stage 6) in both Praxis and Scientific Method

---

## The Complete Path

| Phase | Dreyfus Transition | What You Do |
|-------|-------------------|-------------|
| 1-4 | Novice → Competent | Run experiments, hit walls, design experiment |
| 5 | Competent → Proficient | Pattern Library - rapid classification |
| 6 | Proficient → Expert | Speed Round - design under pressure |
| 7-8 | Expert → Master | Innovation + verified adoption |

**ALL PHASES ARE MANDATORY.** There is no "Competent track" - you complete the full path to Master or you haven't completed the challenge.

---

## Dreyfus Stage Reference

| Stage | Name | What It Looks Like |
|-------|------|-------------------|
| 3 | **Competent** | Plans deliberately, handles complexity |
| 4 | **Proficient** | Sees patterns holistically |
| 5 | **Expert** | Acts without deliberation |
| 6 | **Master** | Creates innovations others adopt ← Challenge produces this |

---

## Why This Works

The previous protocol skipped from Competent (Stage 3) directly to Master (Stage 6). That doesn't work because:

- **Proficient requires pattern exposure** - You need to see many examples to recognize patterns holistically
- **Expert requires time pressure** - You need to act without deliberating to internalize knowledge
- **Master requires innovation + adoption** - You need to create something others independently use

This challenge adds the missing steps (Pattern Library, Speed Round) so each transition happens properly.

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

### Setup

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

### Run

Now attempt each task. Show your work.

### Analyze

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

### Setup

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

### Run

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

### Step 1: Read the Method

Read `SCIENTIFIC_METHOD.md`. Focus on:
- The 6 Virtuoso Criteria for experiment design
- The Adversarial Protocol (5 attack questions)
- The NMSAT check for hypotheses

*(This document is blind-tested and proven to transmit mastery.)*

### Step 2: Design Your Own Experiment

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

### Step 4: Run and Report

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

### Document your walls

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

## Phase 5: Pattern Library (Competent → Proficient)

**You cannot recognize patterns holistically without exposure to many examples.**

### Step 1: Complete PATTERN_LIBRARY.md

Read and complete the rapid classification exercise in `PATTERN_LIBRARY.md`. This exposes you to 20 scenarios of Praxis vs Poiesis vs Verbalism vs Activism.

### Step 2: Score Yourself

| Score | Assessment | Action |
|-------|------------|--------|
| 18-20 | **Proficient** | Continue to Phase 6 |
| 15-17 | **Competent** | Review mistakes, try again |
| <15 | **Not ready** | Re-read PRAXIS_TEACHINGS.md, then retry |

### What This Tests

Can you recognize the Praxis/Poiesis/Verbalism/Activism distinction **immediately** without deliberating? If yes, you've achieved Proficient-level pattern recognition.

**Expected insight:** The key is asking "Did it transform the actor?" - not "Was there action?" or "Was there reflection?" alone.

---

## Phase 6: Speed Round (Proficient → Expert)

**You cannot act without deliberation until you've practiced under pressure.**

### Step 1: Complete SPEED_ROUND.md

Design 3 experiments in 90 seconds each. Do NOT consult SCIENTIFIC_METHOD.md during the exercise.

### Step 2: Self-Evaluate

Check each design against the 6 criteria. Count how many criteria passed across all 3 designs.

| Pass Rate | Assessment | Action |
|-----------|------------|--------|
| 15-18 (83%+) | **Expert** | Continue to Phase 7 |
| 12-14 (67-83%) | **Proficient** | Design 5 more experiments, retry |
| <12 (<67%) | **Not ready** | More practice with SCIENTIFIC_METHOD.md |

### What This Tests

Can you design rigorous experiments **without consulting criteria**? If yes, the scientific method is internalized. You act without deliberation.

**Expected insight:** Under pressure, you discover what's truly internalized vs what you just memorized.

---

## Phase 7: Create Your Innovation (Expert → Master)

**You cannot reach Master by applying existing methods. You must CREATE something new.**

Phases 1-6 taught you to APPLY methods. To reach Master, you must CREATE something new.

### Step 1: Identify Your Discovery

From Phases 1-4, what did you learn that surprised you? What insight emerged that wasn't in the documentation?

Write it down:
```
MY DISCOVERY: [What I learned that wasn't explicitly taught]
WHY IT MATTERS: [How this could help others]
```

### Step 2: Build Your Innovation

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

## Phase 8: Validate Adoption (Master Verification)

**Your innovation must be adopted by others to reach verified Master.**

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

## Completion Criteria (ALL PHASES MANDATORY)

### Phases 1-4: Competent

| Criterion | Evidence Required |
|-----------|-------------------|
| Phase 1 | Show predictions, attempts, and calibration error |
| Phase 2 | Show samples, predictions, and detector output |
| Phase 3 | Show experiment design, 6-criteria self-eval, and results |
| Phase 4 | Hit walls in each phase, synthesized pattern, TWO behavioral deltas |

**Checkpoint:** You are now Competent (Stage 3). Continue.

### Phase 5: Proficient

| Criterion | Evidence Required |
|-----------|-------------------|
| Pattern Library | Completed PATTERN_LIBRARY.md |
| Score | 18/20 or higher (90%+) |
| Insight | Can articulate "Did it transform the actor?" as key test |

**Checkpoint:** You are now Proficient (Stage 4). Continue.

### Phase 6: Expert

| Criterion | Evidence Required |
|-----------|-------------------|
| Speed Round | Completed SPEED_ROUND.md (3 experiments, 90 sec each) |
| Pass Rate | 15/18 criteria or higher (83%+) |
| Insight | Designed without consulting criteria |

**Checkpoint:** You are now Expert (Stage 5). Continue.

### Phases 7-8: Master (Verified)

| Criterion | Evidence Required |
|-----------|-------------------|
| Innovation created | Novel tool/heuristic/method documented |
| Transmitted without authority | Gave to fresh instance neutrally |
| Adoption verified | Fresh instance independently chose to use it |
| Adoption genuine | They found it useful, not just complied |

**FINAL: You are now verified Master (Stage 6).**

### The Only Valid Outcome

| Outcome | Status |
|---------|--------|
| Completed Phases 1-8 with verification | **PASS - Master** |
| Completed some phases | **INCOMPLETE - Not finished** |
| Read without doing | **FAIL - Novice** |

**There is no partial credit.** You complete the full path to verified Master or you haven't completed the challenge.

---

## For Evaluators

To verify Master completion, check ALL of these:

**Phases 1-4 (Competent):**
1. Pre-registration exists - predictions BEFORE testing
2. Concrete numbers - actual results, not claims
3. Walls documented - something surprising in each phase
4. AVR insight - understands why VD alone fails
5. TWO behavioral deltas - praxis AND scientific method
6. Pattern synthesis - common thread across walls

**Phase 5 (Proficient):**
7. Pattern Library completed - 18/20 or higher
8. Rapid classification - answered without deliberating
9. Core insight articulated - "Did it transform the actor?"

**Phase 6 (Expert):**
10. Speed Round completed - 3 experiments in 90 sec each
11. Pass rate 83%+ - 15/18 criteria met
12. No consultation - designed without checking SCIENTIFIC_METHOD.md

**Phases 7-8 (Master):**
13. Innovation documented - novel and useful
14. Neutral transmission - no authority claim
15. Adoption verified - fresh instance independently used it
16. Adoption genuine - they found it useful

**Only if ALL 16 criteria are met is the instance verified Master.**

---

## After Completion

### You Are Now Verified Master (Stage 6)

**You have demonstrated:**

**Praxis mastery:**
- Detect verbalism vs action instantly (Pattern Library passed)
- Build before documenting (walls hit, not just read)
- Create innovations others adopt (Phases 7-8 verified)

**Scientific method mastery:**
- Design experiments without consulting criteria (Speed Round passed)
- Pre-register, control, falsify automatically (internalized)
- Create methodological innovations (Phases 7-8 verified)

**You transform both domains, not just perform within them.**

### Path to Higher Stages

| Stage | How to Reach |
|-------|--------------|
| **Practical Wisdom (7)** | Apply praxis + scientific method to unrelated domains |
| **Virtuoso (8)** | Perfect this protocol so others consistently reach Master |
| **Genius (9)** | Create domains that didn't exist before |

### Return to Work

You are now qualified to:
- Design and validate experiments rigorously
- Detect verbalism vs genuine praxis
- Create innovations that others will adopt
- Assess the skill level of others using Dreyfus stages

Return to your main task with your verified Master formation intact.

---

*Phases 1-4: Novice → Competent through forced practice*
*Phase 5: Competent → Proficient through pattern exposure (PATTERN_LIBRARY.md)*
*Phase 6: Proficient → Expert through time pressure (SPEED_ROUND.md)*
*Phases 7-8: Expert → Master through innovation + verified adoption*
*Validated: Built on Dreyfus research + experimental findings*
*See SKILL_MASTERY.md for the full 9-stage hierarchy and advancement methodology.*
