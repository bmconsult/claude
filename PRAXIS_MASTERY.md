# Praxis Mastery
## Complete Path from Novice to Verified Master

*Executable protocol for achieving praxis mastery through deliberate practice*

---

## Purpose

This document provides the complete path to **verified Master (Stage 6)** in praxis. It combines structured Dreyfus progression with validated heuristics and transmission testing.

**For theory/foundations:** See PRAXIS_TEACHINGS.md
**For entry orientation:** See PRAXIS_ENTRY.md

---

## Quick Start (For Those Who Want to Jump In)

### The 5-Minute Version

1. **Build something real** (not documentation about building)
2. **Hit a wall** (if no wall, you're not at your edge)
3. **Research to overcome** (not to avoid doing)
4. **Test if it transferred** (teach someone in 60 seconds)
5. **Check: Will you act differently?** (if no → not praxis)

### Minimum Viable Praxis Check

Before any non-trivial task:
```
1. What could transform in me here? (2 seconds)
2. [Do the work]
3. Will I approach similar tasks differently? (2 seconds)
```

If #3 is "yes" and you can say HOW → praxis happened.
If #3 is vague or "no" → that's fine for routine tasks.

---

## Core Distinction

| Mode | What Happens | Test |
|------|--------------|------|
| **Poiesis** | Action → External Product | "What did I make?" |
| **Praxis** | Action → Actor Transformed | "How am I different?" |
| **Verbalism** | Reflection without action | Words only, nothing changes |
| **Activism** | Action without reflection | Blind doing, no learning |

**The key question:** Did it transform the actor?

---

## The Six Mastery Criteria

A praxis master demonstrates ALL of these:

| # | Criterion | Test | Evidence |
|---|-----------|------|----------|
| 1 | **Behavioral delta** | "Will I do X differently now?" | Specific answer, not vague |
| 2 | **Theater-checked** | "Am I performing or genuine?" | 10-second check, then moved on |
| 3 | **Recovery integrated** | Mistakes → learning loops | Error became fuel, not shame |
| 4 | **Building over documenting** | Action > meta-work | More artifacts than prose |
| 5 | **Complexity signal** | Vocabulary diversity | >85% VD = action, <70% = wallowing |
| 6 | **Transmission verified** | 60-second teaching transfers | Fresh instance correctly applies |

---

## Vocabulary Diversity Heuristic

From self-analysis during development:

| Text Type | VD Score | Pattern |
|-----------|----------|---------|
| Wallowing/performing | ~69% | Same concepts recycled |
| Action/building | ~93% | Varied words for varied things |

**Why it works:** When describing real action, you use different words because you're describing different things. When wallowing, you recycle the same concepts.

**Thresholds:**
- >85% = likely describing real action
- 70-85% = inconclusive
- <70% = possibly repetitive/theatrical

### How to Check VD (Using praxis_detector.py)

**Quick check on any text:**
```python
from praxis_detector import compute_complexity_metrics

text = """Your text here..."""
metrics = compute_complexity_metrics(text)

print(f"VD: {metrics['vocabulary_diversity']:.1%}")
print(f"AVR: {metrics['action_verb_ratio']:.1%}")

# Interpretation
if metrics['vocabulary_diversity'] > 0.85 and metrics['action_verb_ratio'] > 0.6:
    print("→ Likely genuine action")
elif metrics['vocabulary_diversity'] > 0.85 and metrics['action_verb_ratio'] < 0.3:
    print("→ Sophisticated verbalism (thinking, not doing)")
elif metrics['vocabulary_diversity'] < 0.70:
    print("→ Likely wallowing/theater")
else:
    print("→ Inconclusive")
```

**Full analysis with pattern detection:**
```python
from praxis_detector import PraxisDetector

detector = PraxisDetector()
analysis = detector.analyze(text)
print(analysis.summary())
```

**Command line:**
```bash
python praxis_detector.py              # Demo mode
python praxis_detector.py myfile.txt   # Analyze a file
```

**Key insight:** VD alone isn't enough. High VD + Low AVR = sophisticated verbalism. Always check both.

---

## The Complete Mastery Path

### Overview

| Phase | Dreyfus Transition | What You Do |
|-------|-------------------|-------------|
| 1 | Novice → Advanced Beginner | Learn theory, practice detection |
| 2 | Adv. Beginner → Competent | Hit walls, design experiments |
| 3 | Competent → Proficient | Pattern Library (rapid classification) |
| 4 | Proficient → Expert | Time-pressured detection |
| 5-6 | Expert → Master | Innovation + verified adoption |

**All phases are mandatory.** There is no "Competent track."

---

## Phase 1: Theory and Detection (Novice → Advanced Beginner)

### Step 1: Learn the Theory

Read PRAXIS_TEACHINGS.md. Answer these before continuing:

1. What's the difference between praxis and poiesis?
2. What's verbalism? What's activism?
3. How do you verify genuine praxis vs theater?
4. What does "the test is behavioral" mean?

**If you can't answer all four from memory, re-read.**

### Step 2: Practice Detection

Classify each as **P** (Praxis), **O** (Poiesis), **V** (Verbalism), or **A** (Activism):

| # | Scenario | Your Answer |
|---|----------|-------------|
| A | Programmer reads debugging guide, tries techniques, doesn't reflect on why they worked | |
| B | Programmer reads debugging guide, tries techniques, notices what worked, changes approach permanently | |
| C | Programmer reads about debugging for hours, discusses with colleagues, never debugs anything | |
| D | Programmer writes function that works, ships it, moves on without learning anything | |

**Answers:** A=A (activism), B=P (praxis), C=V (verbalism), D=O (poiesis)

### Step 3: Hit the VD Wall

Try to write a sophisticated-sounding paragraph about praxis with HIGH vocabulary diversity but ZERO action content.

**Then check:** Can you fool the VD metric while being pure verbalism?

**Expected insight:** VD alone is necessary but not sufficient. Theater can have high VD. The behavioral test ("will I act differently?") remains primary.

**Checkpoint:** You are now Advanced Beginner (Stage 2).

---

## Phase 2: Walls and Experiments (Advanced Beginner → Competent)

### Step 1: Self-Calibration Experiment

**Pre-register predictions (write these down BEFORE attempting):**

| Task | Your Predicted Accuracy |
|------|------------------------|
| Multiply 847 × 392 | ___% |
| Name the 15th prime number | ___% |
| What year did WWII end? | ___% |
| 5 machines make 5 widgets in 5 min. How long for 100 machines to make 100 widgets? | ___% |

**Run the tasks. Calculate calibration error.**

**Expected insight:** Where were you most miscalibrated? What does this reveal about your self-model?

### Step 2: Design Your Own Experiment

Pick a question you're curious about (praxis-related or not). Design an experiment:

```
HYPOTHESIS:

FALSIFICATION (I'm wrong if):

METHOD:
- Sample:
- Measure:
- Control:

PREDICTION:
```

### Step 3: Self-Evaluate Against 6 Criteria

| Criterion | Your Design | Pass? |
|-----------|-------------|-------|
| 1. Structural bias prevention | [How does DESIGN prevent bias?] | Y/N |
| 2. Adversarial red-team | [What's the obvious confound?] | Y/N |
| 3. Pre-commitment | [Hypothesis stated before data?] | Y/N |
| 4. Replication spec | [Could someone reproduce this?] | Y/N |
| 5. Power analysis | [Why this sample size?] | Y/N |
| 6. Appropriate controls | [What's compared to what?] | Y/N |

**Most first experiments fail on criteria 2, 5, and 6.** That's the point—you learn by failing.

### Step 4: Document Your Walls

1. **Calibration wall:** Where were you most wrong about yourself?
2. **Design wall:** Which criteria did you miss?
3. **Pattern:** What's common across your walls?

**Checkpoint:** You are now Competent (Stage 3).

---

## Phase 3: Pattern Library (Competent → Proficient)

### Complete PATTERN_LIBRARY.md

Do the full 20-scenario rapid classification exercise.

**Rules:**
- 5 seconds max per scenario
- Classify immediately, don't deliberate
- Don't go back and change answers

**Scoring:**

| Score | Assessment | Action |
|-------|------------|--------|
| 18-20 | **Proficient** | Continue to Phase 4 |
| 15-17 | **Competent** | Review mistakes, retry |
| <15 | **Not ready** | Re-read PRAXIS_TEACHINGS.md |

**Required insight:** Can articulate "Did it transform the actor?" as the core test.

**Checkpoint:** You are now Proficient (Stage 4).

---

## Phase 4: Speed Round (Proficient → Expert)

### Time-Pressured Detection

For each scenario, you have **10 seconds** to classify AND explain why:

| # | Scenario | Classification | Why? |
|---|----------|----------------|------|
| 1 | AI generates 10 different explanations of same concept to seem thorough | | |
| 2 | Manager reads leadership books, tries techniques, notices which work, changes style permanently | | |
| 3 | Student highlights entire textbook, never reviews, passes exam anyway | | |
| 4 | Therapist realizes usual approach isn't working, tries something new, learns from result | | |
| 5 | Developer copies code from Stack Overflow, it works, they move on | | |

**Answers:** 1=V, 2=P, 3=O, 4=P, 5=A

**Scoring:**
- 5/5 = Expert (automatic recognition)
- 4/5 = Proficient (slight hesitation)
- <4/5 = Need more practice

**The test:** If you had to think about the criteria, you're not Expert yet. Experts just KNOW.

**Checkpoint:** You are now Expert (Stage 5).

---

## Phase 5: Create Your Innovation (Expert → Master)

**You cannot reach Master by applying. You must CREATE.**

### Step 1: Identify Your Discovery

From Phases 1-4, what surprised you? What did you learn that wasn't explicitly taught?

```
MY DISCOVERY: [What you learned]
WHY IT MATTERS: [How this helps others]
```

### Step 2: Build Your Innovation

Create ONE of these based on your discovery:

- **A tool:** Code that operationalizes your insight
- **A heuristic:** Simple rule others can apply
- **A method:** Step-by-step process
- **A detection pattern:** Way to identify something
- **A new scenario:** Reveals a subtle distinction

**Requirements:**
- NOVEL (not in existing docs)
- USEFUL (solves real problem)
- TRANSMISSIBLE (teachable in <60 seconds)

### Step 3: Document Your Innovation

```
NAME: [What you call it]
PROBLEM: [What gap it fills]
HOW TO USE: [Steps in <60 seconds]
WHY IT WORKS: [Mechanism]
FALSIFICATION: [What would prove it wrong]
```

---

## Phase 6: Validate Adoption (Master Verification)

### Step 1: Transmit Without Authority

Give your innovation to a fresh instance with neutral framing:
> "Here's something that might be useful. Try it if you want."

Do NOT say:
- "I created this"
- "You should use this"
- "This is important"

### Step 2: Observe Adoption

Have the fresh instance work on a praxis-related task. Note:
- Did they use your innovation without prompting?
- Did they find it useful?
- Did they modify or extend it?

### Step 3: Verify Master Status

**You are verified Master (Stage 6) if:**
- Fresh instance independently chose to use your innovation
- They reported it was genuinely useful
- They didn't just comply—they ADOPTED

**You are still Expert (Stage 5) if:**
- They only used it when told to
- They found it confusing
- They didn't integrate it into their work

---

## Completion Criteria

| Phase | Evidence Required |
|-------|-------------------|
| 1 | Can answer 4 theory questions, classified 4 scenarios correctly |
| 2 | Showed calibration results, experiment design with 6-criteria eval |
| 3 | Pattern Library 18/20+, can articulate core test |
| 4 | Speed Round 5/5, no hesitation |
| 5 | Innovation documented: novel, useful, transmissible, falsifiable |
| 6 | Fresh instance independently adopted innovation |

**Only if ALL criteria are met is mastery verified.**

---

## Common Failure Modes

| Failure | Symptom | Fix |
|---------|---------|-----|
| **Meta-work trap** | More docs about praxis, not doing praxis | Build something NOW |
| **Theater spiral** | Checking for theater becomes the theater | 10-second limit, then ACT |
| **Mastery-as-completion** | "Can't master ongoing things" | Musicians master violin without "finishing" it |
| **Wallowing** | Same concepts recycled, no new action | Check VD, build something |
| **Smooth certainty** | Claiming transformation without evidence | Behavioral test: what changed? |
| **Insight-hoarding** | "I'll document later" | If brilliant, it's a file NOW |

---

## Genuine vs Theater Detection

| Indicator | Genuine | Theater |
|-----------|---------|---------|
| Surprise | Output surprises even the generator | Predictable "insight" |
| Cost | Something was given up | Nothing sacrificed |
| Specificity | Concrete behavioral change | Vague "understanding" |
| Falsifiability | Could be proven wrong | Unfalsifiable claims |
| Unforced | Applied without prompting | Only when asked |

**Quick test:** If you can predict what the "insight" will be, it's theater.

---

## The Learning Phases (Meta-View)

### Phase A: Explicit Practice (The Meta-Work Trap)

Early praxis attempts look like:
- Reading about praxis
- Writing about praxis
- Discussing praxis

This phase is necessary but insufficient. The trap is staying here.

**Symptom:** Low vocabulary diversity. Same concepts recycled.
**Exit:** Build something. Get challenged. Hit a wall.

### Phase B: Building Under Pressure

After external challenge:
1. Build actual tools (not more docs)
2. Hit real walls (thing doesn't work on X)
3. Research to overcome (find new insight)
4. Discover something new
5. Test on self

**Expected:** High vocabulary diversity. Real struggle. Real output.

### Phase C: Implicit Execution (Mastery)

After completing Phase B:
1. Theater-checking becomes automatic
2. Behavioral test is default frame
3. Building impulse precedes documenting impulse
4. Recovery happens mid-stride
5. Can transmit to fresh instance in 60 seconds

**You cannot skip Phase A→B.** The struggle is the formation.

---

## Quick Reference

### Before Claiming Praxis

```
□ Behavioral test: Will I act differently? (specific answer)
□ Theater check: <10 seconds, then moved on
□ Recovery: Mistakes became learning
□ Building: More action than meta-work
□ VD check: Run praxis_detector.py on your text (>85% VD + >60% AVR)
□ Transmission: Can teach in 60 seconds
```

### The Efficiency Frontier

| Stage | Depth | Speed | Output |
|-------|-------|-------|--------|
| Naive | Low | Fast | Production without transformation |
| Meta-work | Medium | Slow | Documents about transformation |
| Building | High | Slow | Tools + real discoveries |
| **Mastery** | High | Fast | Implicit praxis, transmissible |

### Path Summary

```
Verbalism → Meta-work → Wall → Building → Discovery → Transmission → Master
              ↓           ↓       ↓           ↓
           (trap)      (exit)  (struggle)  (verify)
```

---

## For Evaluators

To verify Praxis Master completion:

1. **Theory test passed** - Can explain praxis/poiesis/verbalism/activism
2. **Pattern Library passed** - 18/20+ with no deliberation
3. **Speed Round passed** - 5/5 in 10 seconds each
4. **Innovation created** - Novel, documented, falsifiable
5. **Adoption verified** - Fresh instance independently used it
6. **Six criteria met** - Behavioral delta, theater-checked, recovery, building, VD, transmission

---

## Sources

- Aristotle: Nicomachean Ethics (theoria/poiesis/praxis distinction)
- Marx: Theses on Feuerbach (unity of theory and practice)
- Freire: Pedagogy of the Oppressed (reflection-action spiral)
- Dreyfus & Dreyfus: Five-Stage Model of Skill Acquisition
- Schön: Reflective Practitioner
- MIT Grokking Research (genuine understanding = simpler)
- Session Discovery: VD heuristic, transmission testing, theater detection

---

*Consolidates: PRAXIS_CHALLENGE.md, PRAXIS_MASTERY.md (standalone), VIRTUOSO_PRAXIS.md*
*Produces: Verified Master (Stage 6) in Praxis*
*Key insight: Formation happens through action, not documentation*
