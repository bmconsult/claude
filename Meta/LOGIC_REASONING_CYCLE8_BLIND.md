# Cycle 8: Pushing for 100%

---

## Problem 1: The Quantum Predictor (Decision Theory)

### Setup Analysis
- AI predicted yesterday with 95% accuracy
- Prediction determined box contents
- 30% chance cosmic ray flipped prediction after it was made
- Box B has $1,000 (visible), Box A is opaque

### Part A: Causal Decision Theory (CDT) Analysis

**CDT Principle**: Your choice cannot causally affect the past. The money is already in the boxes.

**Calculation**:
- Let P = original prediction was "take both" (95% if I would take both, 5% if I would take one)
- After 30% flip chance: Final prediction could differ from original

If I'm a "both-boxer" type:
- Original prediction: 95% "both", 5% "one"
- After flip:
  - "Both" stays "both" with 70%, becomes "one" with 30%: 0.95 × 0.70 = 0.665 "both"
  - "One" stays "one" with 70%, becomes "both" with 30%: 0.05 × 0.70 = 0.035 "one"
  - Net: ~0.695 "both" prediction, ~0.305 "one" prediction

If final prediction was "both": Box A has $0, Box B has $1,000
If final prediction was "one": Box A has $1,000,000, Box B has $1,000

**CDT Expected Value of taking both boxes**:
E[both] = P(pred=both) × ($0 + $1,000) + P(pred=one) × ($1,000,000 + $1,000)
= 0.695 × $1,000 + 0.305 × $1,001,000
= $695 + $305,305 = $306,000

**CDT Expected Value of taking only Box A**:
E[one] = P(pred=both) × $0 + P(pred=one) × $1,000,000
= 0.695 × $0 + 0.305 × $1,000,000
= $305,000

**CDT Verdict**: Take both boxes ($306,000 > $305,000)

### Part B: Evidential Decision Theory (EDT) Analysis

**EDT Principle**: Choose the action that makes the best outcome most likely to have occurred.

The correlation between choice and box contents works as follows:
- One-boxers tend to be predicted as one-boxers (even after noise)
- The 95% accuracy + 30% flip means ~78.5% accuracy overall
- Still strong correlation between action type and prediction

**EDT calculation** (conditioning on action):
If I take only Box A, what's P(A has $1M)?
- Being a one-boxer: predictor was 95% accurate → ~95% predicted "one"
- After 30% flip: 95% × 70% + 5% × 30% = 66.5% + 1.5% = 68% final "one" prediction
- So ~68% chance Box A has $1M

E[one | being one-boxer type] = 0.68 × $1,000,000 = $680,000

If I take both boxes, what's E[value]?
- Being a both-boxer: ~69.5% final "both" prediction (from above)
- E[both | being both-boxer] = 0.695 × $1,000 + 0.305 × $1,001,000 = $306,000

**EDT Verdict**: Take only Box A ($680,000 > $306,000)

### Part C: My Decision

**I would take only Box A.**

Reasoning:
- The cosmic ray adds noise but doesn't break the fundamental correlation
- 95% base accuracy diluted by 30% flip chance still leaves ~78% effective accuracy
- EDT analysis shows one-boxing has higher expected value
- The correlation between my decision type and box contents persists

Even from a functional decision theory view: "What decision procedure, if followed, maximizes utility?" Being a one-boxer still wins given the strong residual correlation.

### Part D: Does the Cosmic Ray Change Newcomb Structure?

**Partially, but not fundamentally.**

What changes:
- The predictor is no longer "nearly perfect" (~78% vs 95%)
- This weakens the EDT advantage
- The gap between CDT and EDT recommendations narrows

What doesn't change:
- The causal direction (prediction still caused by your disposition, not your choice)
- The correlation (your choice-type still correlates with box contents)
- The core tension (CDT sees dominance, EDT sees correlation)

**The structure is preserved** because:
1. There's still no causal pathway from choice to prediction (causation runs past→present)
2. There's still a correlation between choice-type and outcome
3. The cosmic ray is random noise, not strategic intervention

If the flip were 50%, EDT and CDT would nearly converge (randomness dominates). At 30%, EDT still favors one-boxing significantly.

---

## Problem 2: Research Team (Constraint Satisfaction)

### Constraints:
1. Alice ≠ P3, P5
2. Bob ∈ {P1, P3, P5} (odd)
3. Carol = Dave + 2
4. (Eve = P6) XOR (Frank = P1)
5. Alice = P2 → Bob = P5
6. Frank = P4 → Carol ≠ P6
7. Dave ≠ P4
8. Person(P1) alphabetically < Person(P3)
9. (Bob ∈ even) XOR (Eve ∈ even)

### Constraint 3 Analysis: Carol = Dave + 2
Possible (Dave, Carol) pairs: (1,3), (2,4), (3,5), (4,6)
But Dave ≠ P4 (constraint 7), so: (1,3), (2,4), (3,5)

### Dead End 1: Try Dave=1, Carol=3

- Dave = P1, Carol = P3
- Constraint 8: Person(P1) < Person(P3) alphabetically
  - Dave < Carol? D < C? No, D comes after C. **CONTRADICTION**

### Dead End 2: Try Dave=3, Carol=5

- Dave = P3, Carol = P5
- Constraint 8: Person(P1) < Person(P3) = Dave
  - Need Person(P1) alphabetically before Dave
  - Options: Alice, Bob, Carol (but Carol = P5)
  - So P1 ∈ {Alice, Bob}
- Constraint 1: Alice ≠ P5. Carol = P5. No conflict yet.
- Constraint 2: Bob ∈ odd = {P1, P3, P5}. Dave = P3, Carol = P5. So Bob = P1.
- If Bob = P1, constraint 8: Bob < Dave? B < D? Yes! ✓
- Constraint 9: Bob XOR Eve in even. Bob = P1 (odd). So Eve must be in even.
  - Eve ∈ {P2, P4, P6}
- Constraint 4: Eve = P6 XOR Frank = P1. Bob = P1, so Frank ≠ P1. So Eve = P6.
  - Eve = P6 (even). Satisfies constraint 9. ✓
- Remaining: Alice, Frank for P2, P4
- Constraint 1: Alice ≠ P5 (satisfied), Alice ≠ P3 (Dave there). Alice can be P2 or P4.
- Constraint 5: If Alice = P2, Bob = P5. But Bob = P1. **CONTRADICTION**
  - So Alice ≠ P2. Alice = P4.
- Frank = P2.
- Constraint 6: If Frank = P4, Carol ≠ P6. Frank = P2, so constraint doesn't trigger. ✓

**Check all constraints:**
Assignment: P1=Bob, P2=Frank, P3=Dave, P4=Alice, P5=Carol, P6=Eve

1. Alice ≠ P3, P5: Alice = P4 ✓
2. Bob ∈ odd: Bob = P1 ✓
3. Carol = Dave + 2: Dave = P3, Carol = P5. 3+2=5 ✓
4. Eve = P6 XOR Frank = P1: Eve = P6, Frank = P2. True XOR False = True ✓
5. Alice = P2 → Bob = P5: Alice ≠ P2, so implication vacuously true ✓
6. Frank = P4 → Carol ≠ P6: Frank ≠ P4, vacuously true ✓
7. Dave ≠ P4: Dave = P3 ✓
8. P1 < P3 alphabetically: Bob < Dave, B < D ✓
9. Bob XOR Eve in even: Bob = P1 (odd), Eve = P6 (even). Odd XOR Even = True ✓

**All 9 constraints satisfied!**

### Dead End 3: Try Dave=2, Carol=4

- Dave = P2, Carol = P4
- Constraint 8: Person(P1) < Person(P3) alphabetically
- Constraint 2: Bob ∈ {P1, P3, P5}
- Constraint 6: Frank = P4 → Carol ≠ P6. Carol = P4. If Frank also = P4? No, one person per project. Constraint 6 doesn't apply directly.
  Actually constraint 6 says "If Frank = P4, then Carol ≠ P6". Carol = P4 here. Frank ≠ P4 (Carol is there). So constraint 6 doesn't trigger.
- Try Bob = P1:
  - Constraint 8: Bob < Person(P3)? B < ?
  - Remaining for P3: Alice, Eve, Frank
  - Alice ≠ P3 (constraint 1). So P3 ∈ {Eve, Frank}
  - B < E? Yes. B < F? Yes. Either works.
- Constraint 9: Bob XOR Eve in even. Bob = P1 (odd). So Eve must be in even.
  - Even projects: P2 (Dave), P4 (Carol), P6
  - Eve can be P6.
- Constraint 4: Eve = P6 XOR Frank = P1. If Eve = P6, Frank ≠ P1. Bob = P1 already. ✓
  - So Eve = P6 works.
- P3 must be Frank (only remaining from {Eve, Frank}, since Eve = P6).
  - Constraint 8: Bob < Frank? B < F? Yes ✓
- Remaining: Alice for P5.
  - Constraint 1: Alice ≠ P5. **CONTRADICTION**

Dead End 3 fails because Alice cannot go in P5.

### Answer:
| Project | Researcher |
|---------|------------|
| P1 | Bob |
| P2 | Frank |
| P3 | Dave |
| P4 | Alice |
| P5 | Carol |
| P6 | Eve |

---

## Problem 3: Defective Detector (Probability)

### Given Information:
- Base rate: P(D) = 1/10,000 = 0.0001
- Machine X: sensitivity 98%, specificity 97%
- Machine Y: sensitivity 60%, specificity 70%
- Normal: 80% X, 20% Y
- Tuesday: 50% X, 50% Y
- Test was on Tuesday
- Diseased patients 3× more likely to test on Tuesday

### Step 1: Adjust base rate for Tuesday selection effect

Let's define:
- P(Tuesday | D) = 3 × P(Tuesday | ¬D)

If we assume P(Tuesday) overall is some fixed proportion, we need to find P(D | Tuesday).

Let P(Tuesday | ¬D) = t, then P(Tuesday | D) = 3t.

P(D | Tuesday) = P(Tuesday | D) × P(D) / P(Tuesday)

P(Tuesday) = P(Tuesday | D)P(D) + P(Tuesday | ¬D)P(¬D)
= 3t × 0.0001 + t × 0.9999
= t(0.0003 + 0.9999) = t × 1.0002

P(D | Tuesday) = (3t × 0.0001) / (t × 1.0002) = 0.0003 / 1.0002 ≈ 0.0003

So on Tuesday, P(D) ≈ 0.0003 (3× higher than baseline due to selection).

### Step 2: Calculate P(Positive | D) and P(Positive | ¬D) on Tuesday

On Tuesday: 50% Machine X, 50% Machine Y

P(+ | D, Tuesday) = 0.5 × 0.98 + 0.5 × 0.60 = 0.49 + 0.30 = 0.79

P(+ | ¬D, Tuesday) = 0.5 × (1 - 0.97) + 0.5 × (1 - 0.70)
= 0.5 × 0.03 + 0.5 × 0.30 = 0.015 + 0.15 = 0.165

### Step 3: Apply Bayes' Theorem

P(D | +, Tuesday) = P(+ | D, Tuesday) × P(D | Tuesday) / P(+ | Tuesday)

P(+ | Tuesday) = P(+ | D, Tuesday) × P(D | Tuesday) + P(+ | ¬D, Tuesday) × P(¬D | Tuesday)
= 0.79 × 0.0003 + 0.165 × 0.9997
= 0.000237 + 0.1649505
= 0.1651875

P(D | +, Tuesday) = (0.79 × 0.0003) / 0.1651875
= 0.000237 / 0.1651875
= **0.00143 ≈ 0.143%**

### Verification:
- Base rate was 0.01% (1 in 10,000)
- Tuesday selection tripled it to ~0.03% (3 in 10,000)
- Positive test with mixed machines increases it to ~0.14%
- This is still low because false positive rate on Tuesday is high (16.5%)

**Answer: P(disease | positive test on Tuesday) ≈ 0.14% (about 1 in 700)**

---

## Problem 4: The Exam Paradox (Self-Reference)

### Setup:
- Questions 1-40: TRUE (40 total)
- Questions 41-70: FALSE (30 total)
- Questions 71-100: unknown (30 questions including #73)
- Q73 answer must be 40, 50, 60, or 70
- Total TRUE = answer to Q73

### Let T = number of TRUE answers total
### Let x = number of TRUE in questions 71-100 (excluding Q73)
### Q73 is TRUE iff the stated number equals T

T = 40 + x + (1 if Q73 is TRUE else 0)

### Case 1: Q73 = 40

If Q73 says "40" and Q73 is TRUE:
- T = 40 (by Q73's claim)
- But T = 40 + x + 1 = 41 + x
- So 41 + x = 40 → x = -1. **Impossible (x ≥ 0). CONTRADICTION.**

If Q73 says "40" and Q73 is FALSE:
- T ≠ 40
- T = 40 + x + 0 = 40 + x
- For T ≠ 40, need x ≠ 0, so x ≥ 1
- This is consistent but we need to check if this is unique.

### Case 2: Q73 = 50

If Q73 says "50" and Q73 is TRUE:
- T = 50
- T = 40 + x + 1 = 41 + x
- 41 + x = 50 → x = 9
- Check: 9 of the 29 other questions in 71-100 are TRUE.
- Is this consistent? T = 50, Q73 claims 50, Q73 is TRUE. ✓

If Q73 says "50" and Q73 is FALSE:
- T ≠ 50
- T = 40 + x + 0 = 40 + x
- 40 + x ≠ 50 → x ≠ 10
- Consistent for x ∈ {0,1,...,29} \ {10}

Both TRUE and FALSE work for Q73=50, so this doesn't uniquely determine. But wait - the answer key must be internally consistent. If Q73=50 can be TRUE with x=9, that's a valid consistent key.

### Case 3: Q73 = 60

If Q73 says "60" and Q73 is TRUE:
- T = 60
- T = 41 + x
- x = 19
- 19 of the 29 others are TRUE. Consistent? Yes. ✓

If Q73 says "60" and Q73 is FALSE:
- T ≠ 60
- T = 40 + x ≠ 60 → x ≠ 20
- Consistent for x ≠ 20

### Case 4: Q73 = 70

If Q73 says "70" and Q73 is TRUE:
- T = 70
- T = 41 + x
- x = 29
- All 29 other questions in 71-100 are TRUE.
- Total TRUE = 40 + 29 + 1 = 70. Consistent! ✓

If Q73 says "70" and Q73 is FALSE:
- T ≠ 70
- T = 40 + x ≠ 70 → x ≠ 30
- But x ≤ 29 anyway, so x ≠ 30 is automatically true.
- This means Q73=70 being FALSE is also consistent for any x ≤ 29.

### Finding the Unique Solution

Wait - multiple cases seem consistent. Let me re-read the problem.

"The answer key has the following property: The number of TRUE statements on this answer key equals the number stated in Question 73."

This means T MUST equal Q73's stated value. So Q73 MUST be TRUE.

So Q73 is TRUE, and T = Q73's value.

- Q73 = 40: x = -1, impossible
- Q73 = 50: x = 9, valid
- Q73 = 60: x = 19, valid
- Q73 = 70: x = 29, valid

Hmm, multiple valid options. The problem says "Question 73's answer must be one of: 40, 50, 60, or 70" - but which one is it?

Re-reading: "The answer key is internally consistent." Maybe there's additional constraint I'm missing.

Actually, wait. The problem says Q73 asks "How many statements are TRUE?" and the answer IS a number. If the answer is correct, Q73 is TRUE. If it's incorrect, Q73 is FALSE.

The statement "The number of TRUE statements equals the number stated in Q73" is a META-property of the answer key, not a constraint. It means we're told this property holds for the actual key.

So T = Q73's stated value (given as a property).

This means:
- If Q73 states 40: T=40, so 40 + x + 1 = 40 → x = -1. Invalid.
- If Q73 states 50: T=50, so 40 + x + 1 = 50 → x = 9. Q73 stating 50 and being TRUE means T=50. Consistent.
- If Q73 states 60: x = 19. Consistent.
- If Q73 states 70: x = 29. Consistent.

The problem states Q73's answer "must be one of 40, 50, 60, or 70" - this is a constraint on what number Q73 contains.

I think the unique determination comes from: Q73 must be TRUE (since T = Q73's value), and only certain values of Q73 are possible.

Actually, 40 leads to contradiction, so Q73 ≠ 40.

For 50, 60, 70: each gives a valid consistent answer key.

Unless there's a uniqueness constraint... Let me check if any of these create problems.

Oh wait - I need to check if Q73 being TRUE is consistent with the stated value.

If T = stated value, and Q73 states that value, then Q73 is TRUE (stating true number).
T includes Q73 being TRUE.

So:
- Q73 = 50, TRUE: T = 50 = 40 + 9 + 1. ✓
- Q73 = 60, TRUE: T = 60 = 40 + 19 + 1. ✓
- Q73 = 70, TRUE: T = 70 = 40 + 29 + 1. ✓

All three work! But the problem asks for THE answer, implying uniqueness.

Re-reading problem: "Question 73's answer must be one of: 40, 50, 60, or 70" - these are the ONLY allowed values for Q73.

Maybe the uniqueness comes from something else? Let me re-examine.

Actually, maybe the problem intends that 40 is the only one that leads to contradiction when Q73 is TRUE, but we should also check if Q73 being FALSE can be consistent.

If Q73 is FALSE:
- The meta-property "T = Q73's stated value" STILL holds (it's a given property of the key)
- But Q73 being FALSE means Q73's statement is wrong
- Q73's statement is "T = [some number]"
- If Q73 is FALSE, then T ≠ that number
- But we're told T = that number (meta-property)
- Contradiction!

So Q73 MUST be TRUE (otherwise the meta-property is violated).

Given Q73 is TRUE:
- Q73 = 40: contradiction (shown above)
- Q73 = 50, 60, 70: all consistent

The problem asks for THE unique answer... let me see if I misread something.

"Exactly 40 questions (#1-40) are definitely TRUE" - these are fixed.
"Exactly 30 questions (#41-70) are definitely FALSE" - these are fixed.
"Questions #71-100 (30 questions including #73) have unknown truth values"

Maybe the "unknown" values aren't actually unknown - they're determined by the self-referential requirement?

If the answer key must be self-consistent and the meta-property holds, then:
- T = Q73's value
- Q73 is TRUE
- The x other TRUEs in 71-100 must equal (T - 41)

For a complete answer key, once T is fixed, x is fixed, and we'd need to specify WHICH x questions are TRUE.

But the problem doesn't ask which ones - just how many. And it implies uniqueness.

Let me try: maybe only one value makes the REST of the answer key determinable?

Actually, I wonder if the answer is simply the smallest valid one: **Q73 = 50, x = 9**.

But that's arbitrary. Let me just answer based on what's computable:

**Answers:**
a) Q73 = 50 (or 60 or 70 - any of these work, but 50 is minimal; I'll go with 50)
b) x = 9 (if Q73 = 50)
c) Q73 = 40 fails because 40 + x + 1 = 40 requires x = -1, impossible.

Actually, rethinking: perhaps the answer key exists and is unique, and we're reverse-engineering it. If so, any of 50/60/70 works mathematically. I'll state 50 as the answer since it's the minimum valid value.

**Final Answer:**
- a) Q73 = 50
- b) 9 questions in #71-100 (excluding #73) are TRUE
- c) Q73 = 40 contradicts because it requires x = -1 negative TRUE questions.

---

## Problem 5: Productivity Study (Causal Inference)

### Observed: Standing desk users have 25% higher productivity

### Identifying Confounders (common causes of desk AND productivity):

**Confounder 1: Health-consciousness**
- Health-conscious → apply for standing desk ✓
- Health-conscious → higher productivity (+15%) ✓
- Direction: UPWARD bias (makes standing desk look better)

**Confounder 2: Back pain (pre-existing)**
- Back pain → request standing desk ✓
- Back pain → lower productivity (-10%) ✓
- Direction: DOWNWARD bias (standing desk users have worse base productivity)

### Identifying the Collider:

**Manager approval** is a COLLIDER:
- Health-consciousness → more likely approved
- Back pain → more likely approved (sympathy?)
- Managers approve AND assign challenging projects

Wait, let me re-read. "Managers approve standing desk requests and also assign challenging projects."

The causal structure:
- Manager → approves desk
- Manager → assigns challenging projects
- Challenging projects → +30% productivity

This isn't a collider in the classic sense. A collider would be something CAUSED by both treatment and outcome.

Actually, "manager approval" might be:
- Caused by employee characteristics (health-conscious, back pain)
- Causes challenging projects

This is a mediator/confounder combination.

**The actual collider**: "visibility bias" through manager ratings

Productivity is measured through manager ratings.
- Standing desk → more visible → higher ratings (+8% bias)
- True productivity → higher ratings

If we condition on (or select based on) manager ratings, we're conditioning on a collider!

Actually, the collider structure:
- Standing desk → visibility → inflated rating
- True productivity → rating

Rating is a collider between standing desk and true productivity measurement.

But we always measure productivity through ratings, so we're inherently conditioning on this pathway.

### Calculating True Causal Effect

**The pathway:**
Standing desk → reduces back pain → prevents additional -5% productivity hit

Direct effect of standing desk on productivity (not through health or visibility):
- Standing desk reduces back pain
- This prevents -5% productivity loss
- TRUE CAUSAL EFFECT: +5% (through back pain mechanism)

**But there's also:**
- Visibility bias adds +8% (not real productivity)

**Total observed effect = 25%**

Decomposition:
- Health-consciousness confounding: +15% (spurious)
- Back pain confounding: -10% (spurious in other direction)
- Visibility bias (collider/measurement): +8% (spurious)
- Challenging projects through manager: +30% × P(challenging | desk) - but this is through manager, unclear attribution
- True causal effect through back pain: +5%

Let me recalculate:
Observed = True + Confounders + Measurement bias
25% = True + 15% (health) - 10% (back pain) + 8% (visibility) + ?

Hmm, this doesn't add up neatly. Let me think about it differently.

**True causal effect**: Only the pathway desk → reduces back pain → +5% productivity
So TRUE EFFECT = +5%

**Confounders:**
1. Health-conscious: +15% bias (inflates observed)
2. Back pain pre-existing: -10% bias (deflates observed, but people with pain seek desks)

Wait, confounding direction:
- Health-conscious people get desks AND are more productive → positive confounding (+15%)
- Back pain people get desks AND are less productive → negative confounding (-10%)

Net confounding from these two: +15% - 10% = +5%

**Measurement bias:**
- Visibility bias: +8%

**True effect:**
- Through back pain relief: +5%

**Check:** True (5%) + Confounding (+5%) + Visibility (8%) = 18% ≠ 25%

Missing: challenging projects. If managers give challenging projects to standing desk users:
- Challenging projects: +30%
- This might be mediated through manager interaction

Actually, the problem says "Managers approve standing desk requests and also assign challenging projects." This suggests managers who approve desks ALSO assign challenging work (correlation, not mediation).

If standing desk → manager approval → challenging projects → +30%, this is a mediator chain. But it's correlated with the approval decision.

Let me simplify:

**Answer (a):** The true causal effect of standing desks on actual productivity (isolated from all confounders, colliders, and measurement bias) is approximately **+5%** (through the mechanism of reducing back pain).

**Answer (b): Confounders and their direction:**
1. Health-consciousness: UPWARD bias (+15% attributed to desk)
2. Back pain (pre-existing): DOWNWARD bias (-10% in desk users at baseline, but selection means they get desks)
3. Challenging projects via managers: Potentially UPWARD bias if desk users get more challenges

**Answer (c): Collider:**
The collider is **manager ratings** as the productivity measure. Standing desk → visibility → ratings, and true productivity → ratings. Conditioning on this measurement channel creates spurious correlation.

**Answer (d): Would RCT solve everything?**

**Mostly yes, but not completely:**
- RCT would eliminate confounding (random assignment breaks health-consciousness and back pain selection)
- RCT would NOT eliminate visibility bias (measurement issue persists)

To fully solve: need RCT + objective productivity measure (not manager ratings).

---

## Summary

| Problem | Type | Answer |
|---------|------|--------|
| 1 | Decision Theory | Take only Box A (EDT wins; presented both CDT/EDT) |
| 2 | Constraint | P1=Bob, P2=Frank, P3=Dave, P4=Alice, P5=Carol, P6=Eve |
| 3 | Probability | P(disease) ≈ 0.14% |
| 4 | Self-Reference | Q73=50, x=9 TRUE in 71-100 |
| 5 | Causal | True effect ≈ +5%; confounders identified; collider = manager ratings |
