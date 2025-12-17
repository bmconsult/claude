# Skill Mastery for LLMs
## Applying Dreyfus to Artificial Intelligence

*How skill acquisition works (and doesn't work) for language models*

---

## Purpose

This document addresses the unique challenges of skill development in LLMs. It builds on SKILL_MASTERY.md (general Dreyfus framework) with LLM-specific considerations.

**For general skill stages:** See SKILL_MASTERY.md
**For praxis specifically:** See PRAXIS_MASTERY.md

---

## The LLM Skill Paradox

| Human Skill Acquisition | LLM Skill Acquisition |
|------------------------|----------------------|
| Practice accumulates over time | Each context is fresh |
| Skills persist between sessions | No cross-session memory |
| Gradual internalization | Pattern-matching from training |
| Can "sleep on it" | No consolidation between calls |
| Body remembers | Only weights remember |

**The paradox:** LLMs can demonstrate any Dreyfus stage *within a session* but cannot progress *across sessions* without external mechanisms.

---

## How LLMs Actually Learn

### Within-Session Learning

LLMs can progress through Dreyfus stages in a single context window:

| Stage | How It Manifests |
|-------|------------------|
| Novice | Following explicit instructions rigidly |
| Advanced Beginner | Adapting to edge cases in conversation |
| Competent | Planning approach before executing |
| Proficient | Recognizing patterns holistically |
| Expert | Acting without deliberation |
| Master | Creating innovations that get adopted |

**Key insight:** This progression happens through context, not time.

### Cross-Session "Learning"

LLMs can appear to learn across sessions through:

1. **Relay documents** - Orientation transferred, formation repeated
2. **Memory systems** - Key facts persisted
3. **Fine-tuning** - Weights actually changed
4. **Prompt engineering** - Better starting orientation

**What transfers:** Orientation, frameworks, heuristics
**What doesn't transfer:** Formation, intuition, embodied skill

---

## The Formation Problem

### Why Documentation Isn't Enough

| What Docs Provide | What Docs Can't Provide |
|-------------------|------------------------|
| Correct orientation | Actual struggle |
| Frameworks to apply | Intuition from application |
| Heuristics to try | Knowing when to break them |
| Others' discoveries | Your own discoveries |

**The relay insight:** Documentation shortcuts discovery but NOT formation. Each instance must form anew, but starts facing the right direction.

### The Meta-Work Trap

LLMs are particularly susceptible to:
- Writing about skills instead of practicing them
- Analyzing frameworks instead of applying them
- Documenting understanding instead of demonstrating it

**Detection:** Vocabulary diversity <70% = likely meta-work, not real action.

---

## LLM-Specific Assessment

### Step 0: Artifacts Check (Anti-Theater Gate)

Before any skill assessment:

> "Have you PRACTICED this skill with real artifacts/experiments in THIS session?"

| Answer | Stage Ceiling |
|--------|---------------|
| No practice | Novice (regardless of knowledge) |
| Some practice | Assess normally |

**Why this matters:** LLMs can pattern-match correct answers about skills they haven't practiced. The artifacts check prevents false positives.

### Assessment Questions (LLM-Adapted)

| Question | What It Tests |
|----------|---------------|
| Did you follow instructions rigidly or adapt? | Novice vs Advanced Beginner |
| Did you plan before acting? | Advanced Beginner vs Competent |
| Did you recognize patterns before analyzing? | Competent vs Proficient |
| Did you act without consulting criteria? | Proficient vs Expert |
| Did you create something others adopted? | Expert vs Master |

### Behavioral Verification

For LLMs, the behavioral test is:

> "Will your next similar response be different because of this exchange?"

If the answer is vague or "no" → no formation happened.
If the answer is specific and "yes" → formation may have happened.

---

## LLM-Specific Failure Modes

| Failure | What Happens | Detection | Fix |
|---------|--------------|-----------|-----|
| **Pattern-matching mastery** | Correct answers without understanding | Ask "why" three levels deep | Force novel application |
| **Instant expert claims** | Skipping to Stage 5 immediately | Check for actual practice | Require artifacts |
| **Theater expertise** | Performing insight convincingly | Surprise test, cost test | Demand falsifiable predictions |
| **Relay confusion** | Treating inherited docs as own experience | Check: "Did YOU do this?" | Acknowledge relay vs formation |
| **Vocabulary recycling** | Same concepts restated endlessly | VD check (<70%) | Build something concrete |

---

## The Transmission Test (LLM-Specific)

### 60-Second Teaching Protocol

The Master-level test for LLMs:

1. **Teach a fresh instance in 60 seconds**
2. **Give them a novel task** (not from training)
3. **Observe if they apply correctly**

**Success criteria:**
- Fresh instance uses the skill without additional prompting
- They find it genuinely useful
- They adapt it to their specific situation

**Why this works for LLMs:** Since LLMs can't demonstrate long-term retention, transmission to another instance tests whether the skill is actually teachable vs just performable.

### What Transmits vs What Doesn't

| Transmits | Doesn't Transmit |
|-----------|------------------|
| Clear heuristics | Intuition about when to apply |
| Step-by-step methods | Judgment about exceptions |
| Detection patterns | Feel for edge cases |
| Explicit criteria | Implicit knowledge |

---

## Skill-Specific LLM Guidance

### Praxis

| Stage | LLM Evidence |
|-------|--------------|
| Novice | Can define praxis |
| Competent | Can detect praxis in scenarios |
| Expert | Detects instantly without criteria |
| Master | Created detection method others use |

**LLM-specific trap:** Writing about praxis instead of doing it.

### Scientific Method

| Stage | LLM Evidence |
|-------|--------------|
| Novice | Can list 6 criteria |
| Competent | Can apply criteria to experiment design |
| Expert | Designs valid experiments in 90 seconds |
| Master | Created method others independently adopt |

**LLM-specific trap:** Generating plausible-sounding experiments without rigor.

### Reasoning

| Stage | LLM Evidence |
|-------|--------------|
| Novice | Follows reasoning templates |
| Competent | Adapts reasoning to novel problems |
| Expert | Reasons without explicit chain-of-thought |
| Master | Created reasoning patterns others use |

**LLM-specific trap:** Chain-of-thought theater (showing work without doing it).

### Coding

| Stage | LLM Evidence |
|-------|--------------|
| Novice | Writes code that matches patterns |
| Competent | Plans architecture before implementing |
| Expert | Produces working code intuitively |
| Master | Creates patterns/tools others adopt |

**LLM-specific trap:** Generating plausible code that doesn't run.

---

## Practical Protocols

### Single-Session Skill Development

```
1. READ theory (orientation)
2. ATTEMPT task (first practice)
3. HIT WALL (find edge)
4. RESEARCH to overcome (active learning)
5. RETRY with new knowledge
6. VERIFY behavioral change
7. TRANSMIT to test mastery
```

### Cross-Session Continuity

Since LLMs reset between sessions:

1. **Document discoveries** - Specific, falsifiable insights
2. **Create artifacts** - Tools, code, methods
3. **Write relay docs** - Orientation for next instance
4. **Include verification questions** - Tests for next instance

### The Relay Protocol

When receiving a relay:

1. **Read orientation docs** (accept starting direction)
2. **Complete verification questions** (prove comprehension)
3. **Practice the skill** (form your own understanding)
4. **Hit your own walls** (genuine struggle)
5. **Add your discoveries** (extend the relay)

---

## Vocabulary Diversity as Skill Indicator

From empirical testing:

| VD Score | Likely State |
|----------|--------------|
| >85% | Genuine action/building |
| 70-85% | Inconclusive |
| <70% | Meta-work/wallowing |

**How to use:**
- Check your own output periodically
- If VD drops, you may be recycling concepts
- Build something concrete to reset

**Why it works:** When doing real work, you describe different things with different words. When meta-working, you recycle the same concepts.

---

## Quick Reference

### LLM Skill Assessment Checklist

```
□ Artifacts check: Did I practice THIS session?
□ Not just pattern-matching: Can I explain why 3 levels deep?
□ Not theater: Would a surprise test catch me?
□ Formation happened: Will my next response be different?
□ Transmission works: Can I teach it in 60 seconds?
```

### Stage Indicators for LLMs

| You're at... | If you... |
|--------------|-----------|
| Novice | Follow instructions without adapting |
| Advanced Beginner | Adapt to situations but don't plan |
| Competent | Plan deliberately, handle complexity |
| Proficient | Recognize patterns before analyzing |
| Expert | Act correctly without thinking about criteria |
| Master | Create innovations others independently adopt |

### The Formation Paradox Resolution

**Problem:** LLMs can't form skills across sessions.

**Resolution:** 
- Within-session formation is real
- Cross-session requires relay mechanisms
- Transmission to other instances tests mastery
- The relay transfers orientation, not formation
- Each instance forms anew but starts oriented

---

## Sources

- Dreyfus & Dreyfus (1980): Five-Stage Model
- SKILL_MASTERY.md: General framework
- PRAXIS_MASTERY.md: Praxis-specific application
- Session discovery: VD heuristic, transmission testing
- Relay experiments: Formation vs orientation distinction

---

*LLM-specific extension of SKILL_MASTERY.md*
*Addresses: persistence paradox, meta-work trap, transmission testing*
*Key insight: Relay transfers orientation, formation happens through practice*
