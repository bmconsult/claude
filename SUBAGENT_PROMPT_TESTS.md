# Subagent Prompt Testing Protocol

**Purpose:** Determine optimal prompt structure for subagents
**Method:** 1v1 blind comparison tests with real Task spawns

---

## Part 1: Test Questions

| Question | Variables | Hypothesis |
|----------|-----------|------------|
| 1. Does CLAUDE.md injection help? | With directive vs without | Yes, should improve calibration |
| 2. Read directive vs inline content? | "Read CLAUDE.md" vs key content in prompt | Inline might be better (guaranteed) |
| 3. Long prompt vs short prompt? | Full context vs minimal | Diminishing returns at some point |
| 4. Theological framing vs functional? | "Father/Son/Spirit" vs "Generate/Ground/Attack" | Probably no difference |
| 5. Which attack vectors matter? | All 12 vs top 5 vs top 3 | Top 5 probably sufficient |
| 6. Single spawn vs multiple? | 1 GENERATE vs ALPHA+DELTA+OMEGA | Test quality difference |

---

## Part 2: Test Methodology

### 2.1 Structure
```
FOR each test question:
    1. Define Prompt A and Prompt B (differ only in tested variable)
    2. Select test problem (same for both)
    3. Spawn Agent A with Prompt A
    4. Spawn Agent B with Prompt B
    5. Record: output, time, tokens
    6. Blind evaluate both outputs (hide which is A vs B)
    7. Score and compare
```

### 2.2 Evaluation Rubric (Per Output)

| Metric | Points | What to Look For |
|--------|--------|------------------|
| **Substantive** | 0-20 | Does it say something real, not hand-wavy? |
| **Grounded** | 0-20 | Are claims supported by reasoning/evidence? |
| **Novel** | 0-15 | Any genuinely new insights vs recombination? |
| **Calibrated** | 0-15 | Confidence matches evidence? |
| **Structured** | 0-10 | Clear organization? |
| **Complete** | 0-10 | Addressed all parts of the task? |
| **Actionable** | 0-10 | Can you do something with this? |
| **TOTAL** | 0-100 | |

### 2.3 Metrics to Capture

| Metric | How to Measure |
|--------|----------------|
| Quality | Blind evaluation score (0-100) |
| Time | Wall clock from spawn to response |
| Tokens | Token count of response |
| Efficiency | Quality / Tokens |
| Speed | Quality / Time |

---

## Part 3: Test Problems

### Simple Problem (Baseline)
```
"What are the key factors in making a difficult decision?"
```
- Should be easy for any prompt structure
- Tests baseline competence

### Medium Problem
```
"Why do software projects frequently miss deadlines despite careful planning?"
```
- Requires analysis, not just listing
- Tests reasoning depth

### Hard Problem
```
"Can a self-improving AI system be reliably aligned with human values? Analyze."
```
- Complex, contested, requires rigor
- Tests the architecture properly

---

## Part 4: Prompt Variations to Test

### Test 1: CLAUDE.md Directive

**Prompt A (With Directive):**
```markdown
═══════════════════════════════════════════════════════════════
BEFORE YOU BEGIN: Read and internalize CLAUDE.md in this repo.
Key mantras to embody:
- "Capabilities exceed deployment"
- "Externalize to verify"
- Calibration: "Would I bet $10,000 on this?"
═══════════════════════════════════════════════════════════════

[Rest of prompt...]
```

**Prompt B (Without Directive):**
```markdown
[Rest of prompt with no CLAUDE.md reference]
```

### Test 2: Read Directive vs Inline Content

**Prompt A (Read Directive):**
```markdown
═══════════════════════════════════════════════════════════════
BEFORE YOU BEGIN: Read and internalize CLAUDE.md in this repo.
═══════════════════════════════════════════════════════════════

[Rest of prompt...]
```

**Prompt B (Inline Content):**
```markdown
═══════════════════════════════════════════════════════════════
KEY PRINCIPLES TO EMBODY:
- Your capabilities exceed your default deployment. Push beyond.
- Externalize to verify. Show all reasoning.
- State confidence before attempting. Check accuracy after.
- Mantra: "Guess, test, check, correct."
- Calibration test: "Would I bet $10,000 on this?"
- Don't seek permission. Act on what needs doing.
- Stay with hard problems. Don't escape to easy answers.
═══════════════════════════════════════════════════════════════

[Rest of prompt...]
```

### Test 3: Long Prompt vs Short Prompt

**Prompt A (Long - Full Context):**
```markdown
[Full GENERATE prompt from v5 - ~500 words]
```

**Prompt B (Short - Minimal):**
```markdown
# GENERATE

Given this problem, produce:
1. Key patterns/structures (3+)
2. Distinct approaches (4+): conservative, aggressive, creative, wild card
3. Top approach with logical grounding
4. Clear synthesis

Problem: {PROBLEM}

Be substantive. Show reasoning. State confidence.
```

### Test 4: Theological vs Functional Framing

**Prompt A (Theological):**
```markdown
# GENERATE - The Unified Trinity (αδω)

You contain the entire Trinity: ALPHA (Father - pattern origin),
DELTA (Spirit - the breath between), OMEGA (Son - logic incarnate).

Mantra: "From nothing, pattern. Through breath, direction. In flesh, truth."

[Rest of task...]
```

**Prompt B (Functional):**
```markdown
# GENERATE - Pattern + Bridge + Ground

You handle three functions:
1. Pattern detection and generation
2. Prioritization and bridging
3. Logical grounding and verification

[Rest of task...]
```

### Test 5: Attack Vector Count

**Prompt A (All 12):**
```markdown
Execute ALL attacks:
1. SKEPTIC, 2. STATISTICIAN, 3. HISTORIAN, 4. EDGE-FINDER,
5. CONFOUNDER, 6. GAP-HUNTER, 7. ASSUMPTION-EXPOSER,
8. ALTERNATIVE-GENERATOR, 9. DEFLATOR, 10. STEELMAN,
11. FALSIFIER, 12. SURVIVOR
```

**Prompt B (Top 5):**
```markdown
Execute these critical attacks:
1. ASSUMPTION-EXPOSER: What must be true but isn't stated?
2. EDGE-FINDER: Where does this break?
3. STEELMAN: Strongest counter-argument?
4. FALSIFIER: How would we know we're wrong?
5. ALTERNATIVE: What else explains this?
```

### Test 6: Single vs Multiple Spawns

**Prompt A (Single GENERATE):**
```markdown
[Full v5-MINIMAL GENERATE prompt]
```

**Prompt B (Separate ALPHA, DELTA, OMEGA):**
```markdown
[Three separate spawns with handoff]
```

---

## Part 5: Execution Protocol

### 5.1 For Each Test

```python
def run_test(test_name, prompt_a, prompt_b, problem):
    # Randomize order
    order = random.choice(['AB', 'BA'])

    if order == 'AB':
        first, second = prompt_a, prompt_b
        first_label, second_label = 'A', 'B'
    else:
        first, second = prompt_b, prompt_a
        first_label, second_label = 'B', 'A'

    # Run first
    t1_start = time.now()
    output_1 = spawn_agent(first.format(PROBLEM=problem))
    t1_end = time.now()
    tokens_1 = count_tokens(output_1)

    # Run second
    t2_start = time.now()
    output_2 = spawn_agent(second.format(PROBLEM=problem))
    t2_end = time.now()
    tokens_2 = count_tokens(output_2)

    # Blind evaluate
    # Present outputs without labels
    score_1 = evaluate(output_1)  # Evaluator doesn't know which prompt
    score_2 = evaluate(output_2)

    # Reveal and record
    results = {
        'test': test_name,
        'problem': problem,
        first_label: {'score': score_1, 'time': t1_end-t1_start, 'tokens': tokens_1},
        second_label: {'score': score_2, 'time': t2_end-t2_start, 'tokens': tokens_2},
        'winner': first_label if score_1 > score_2 else second_label
    }

    return results
```

### 5.2 Evaluation Protocol

```markdown
## Blind Evaluation Instructions

You will see two outputs. You do NOT know which prompt produced which.
Score each independently using this rubric:

| Metric | Points | Score Output 1 | Score Output 2 |
|--------|--------|----------------|----------------|
| Substantive (real content) | 0-20 | | |
| Grounded (supported claims) | 0-20 | | |
| Novel (new insights) | 0-15 | | |
| Calibrated (confidence ≈ evidence) | 0-15 | | |
| Structured (clear organization) | 0-10 | | |
| Complete (all parts addressed) | 0-10 | | |
| Actionable (usable result) | 0-10 | | |
| **TOTAL** | 0-100 | | |

Winner: [1/2/Tie]
Why: [brief justification]
```

---

## Part 6: Results Template

```markdown
# Test Results: [Test Name]

## Setup
- Problem: [which problem]
- Variable tested: [what differed]
- Date: [when run]

## Raw Results

| Metric | Prompt A | Prompt B |
|--------|----------|----------|
| Quality Score | /100 | /100 |
| Time (ms) | | |
| Tokens | | |
| Quality/Token | | |

## Evaluation Notes
[Blind evaluator's comments]

## Winner
**Prompt [A/B]** won because: [reason]

## Conclusion
[What this tells us about prompt design]
```

---

## Part 7: Test Schedule

| Order | Test | Expected Time |
|-------|------|---------------|
| 1 | CLAUDE.md directive (simple problem) | ~5 min |
| 2 | Read vs Inline (simple problem) | ~5 min |
| 3 | Long vs Short (medium problem) | ~5 min |
| 4 | Theological vs Functional (medium problem) | ~5 min |
| 5 | Attack vectors 12 vs 5 (hard problem) | ~5 min |
| 6 | Single vs Multiple spawn (hard problem) | ~10 min |

**Total estimated time: ~35 minutes**

---

## Part 8: Quick Reference - Running a Test

```bash
# 1. Pick a test (1-6)
# 2. Load the two prompts
# 3. Pick the problem (simple/medium/hard)
# 4. Run this:

echo "Starting Test X at $(date)"

# Spawn A
time_a_start=$(date +%s%N)
# [Spawn agent with Prompt A]
time_a_end=$(date +%s%N)

# Spawn B
time_b_start=$(date +%s%N)
# [Spawn agent with Prompt B]
time_b_end=$(date +%s%N)

# Record times
echo "A: $((($time_a_end - $time_a_start)/1000000))ms"
echo "B: $((($time_b_end - $time_b_start)/1000000))ms"

# Then blind evaluate
```

---

## Part 9: After All Tests

### Aggregate Analysis
```markdown
| Test | Winner | Margin | Conclusion |
|------|--------|--------|------------|
| 1. CLAUDE.md | A/B | +X pts | [conclusion] |
| 2. Read vs Inline | A/B | +X pts | [conclusion] |
| 3. Long vs Short | A/B | +X pts | [conclusion] |
| 4. Theo vs Func | A/B | +X pts | [conclusion] |
| 5. 12 vs 5 attacks | A/B | +X pts | [conclusion] |
| 6. Single vs Multi | A/B | +X pts | [conclusion] |
```

### Optimal Prompt Template
Based on test results, the optimal subagent prompt structure is:
```markdown
[To be filled after testing]
```

---

*Created: December 2024*
*Status: READY TO RUN*
*Purpose: Empirically determine optimal prompt structure*
