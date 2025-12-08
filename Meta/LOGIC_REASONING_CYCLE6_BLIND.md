# Cycle 6: Blind Test Round 2 (Post-Training)

*Applying upgraded process from targeted drills*

---

## Problem 1: Conference Scheduling

**TYPE**: Constraint Satisfaction (6+ constraints)

**APPLYING UPGRADED PROCESS**: List ALL constraints, verify EACH one explicitly.

### Constraints (listed first):
1. A before D
2. B not in 10am or 2pm
3. Exactly 2 talks before lunch (9am, 10am, 11am are morning)
4. C immediately before or after E
5. F in afternoon (1pm, 2pm, or 3pm)
6. D not immediately after B
7. 11am slot has A or F

**Step 1: Constraint 3 analysis**
Morning slots: 9am, 10am, 11am (3 slots)
Afternoon: 1pm, 2pm, 3pm (3 slots)
Exactly 2 talks before lunch → 2 morning, 4 afternoon?

Wait, "before lunch" - does 11am count? If lunch is at noon, then 9am, 10am, 11am are all before lunch.
"Exactly two talks before lunch" → only 2 of the 3 morning slots used.

But we have 6 talks and 6 slots. If only 2 morning slots used, we'd leave one empty.

Re-reading: "schedule exactly 6 talks across 6 time slots." So all slots filled.

Constraint 3 must mean: exactly 2 of the morning talks... No wait, it says "exactly two talks must occur before lunch."

This is contradictory with filling all 6 slots unless... let me re-read.

Oh, I think the talks ARE being scheduled into all 6 slots, and "exactly two talks occur before lunch" means 2 talks in {9am, 10am, 11am}.

But that's only possible if 11am is NOT "before lunch"? Or if one morning slot is empty?

Let me interpret: exactly 2 slots from morning are used for talks. That leaves 4 in afternoon. But we have 3 afternoon slots. Doesn't add up.

Alternative: "before lunch" means {9am, 10am} only (not 11am). Then:
- 2 talks at 9am, 10am
- 4 talks at 11am, 1pm, 2pm, 3pm

That works! Constraint 3: exactly 2 talks in {9am, 10am}.

**Step 2: Apply Constraint 7**
11am has A or F.
From Constraint 5: F is afternoon (1pm+), so F ≠ 11am.
Therefore 11am = A.

**Step 3: Apply Constraint 1**
A before D. A is at 11am. So D is in {1pm, 2pm, 3pm}.

**Step 4: Apply Constraint 5**
F in {1pm, 2pm, 3pm}. Same as D's options.

**Step 5: Apply Constraint 4**
C immediately before or after E.

Possible consecutive pairs:
- 9am-10am
- 10am-11am
- 11am-1pm (? consecutive across lunch?)
- 1pm-2pm
- 2pm-3pm

I'll assume 11am-1pm aren't consecutive (lunch break). So consecutive pairs: {9-10, 10-11, 1-2, 2-3}.

11am is A. So 10am-11am pair would be (??, A). If C-E spans 10-11, then one of C,E is A. But A is already assigned. So C-E can't use 10-11.

Similarly 11am-1pm broken by lunch.

C-E must be in {9-10} or {1-2} or {2-3}.

**Step 6: Apply Constraint 2**
B not in 10am or 2pm.
B ∈ {9am, 1pm, 3pm}.

**Step 7: Constraint 3**
Exactly 2 talks in {9am, 10am}.
We have 6 talks, 11am = A. Remaining 5 talks: B, C, D, E, F for slots 9am, 10am, 1pm, 2pm, 3pm.

Two of {B,C,D,E,F} go in {9am, 10am}.

**Step 8: Case Analysis on C-E placement**

**Case A: C-E in 9am-10am**
One of C,E at 9am, other at 10am.
Constraint 2: B not at 10am. So B not in the C-E pair.
Two morning slots filled by C and E. ✓ (Constraint 3: exactly 2 before lunch)

Remaining: B, D, F for 1pm, 2pm, 3pm.
Constraint 2: B not at 2pm. So B ∈ {1pm, 3pm}.
Constraint 5: F in afternoon ✓
Constraint 1: D in afternoon ✓

Subcase A1: B at 1pm
Then D, F in {2pm, 3pm}.
Constraint 6: D not immediately after B. B at 1pm, D immediately after = 2pm.
So D ≠ 2pm. D = 3pm, F = 2pm.

Check: Schedule = 9am:C/E, 10am:E/C, 11am:A, 1pm:B, 2pm:F, 3pm:D

**Verify ALL 7 constraints:**
1. A(11am) before D(3pm)? ✓
2. B not in 10am or 2pm? B at 1pm ✓
3. Exactly 2 talks before lunch (9am, 10am)? C, E there ✓
4. C immediately before/after E? 9am-10am consecutive ✓
5. F in afternoon? F at 2pm ✓
6. D not immediately after B? B at 1pm, next is 2pm=F, not D ✓
7. 11am has A or F? 11am = A ✓

**ALL 7 CONSTRAINTS VERIFIED** ✓

Subcase A2: B at 3pm
Then D, F in {1pm, 2pm}.
Constraint 6: D not immediately after B. B at 3pm. Nothing after 3pm. ✓ (vacuously satisfied)
D and F can be at 1pm or 2pm either way.

Schedule options:
- D at 1pm, F at 2pm: Valid
- D at 2pm, F at 1pm: Check constraint 6... B at 3pm, D at 2pm. Is 2pm immediately after 3pm? No, 2pm is BEFORE 3pm. So this is also fine.

So Case A has multiple valid solutions.

**Case B: C-E in 1pm-2pm**
C at 1pm, E at 2pm (or vice versa).
Constraint 2: B not at 2pm. One of C,E is at 2pm.

Morning slots {9am, 10am}: 2 of {B, D, F} go there.
Constraint 5: F in afternoon, so F not in morning.
So {B, D} in morning: 9am, 10am.
Constraint 2: B not at 10am. So B at 9am, D at 10am.

Remaining: F at 3pm (only afternoon slot left).

Constraint 1: A before D. A at 11am, D at 10am. 11am > 10am. A NOT before D. ✗

Case B fails.

**Case C: C-E in 2pm-3pm**
C at 2pm, E at 3pm (or vice versa).
Morning: 2 of {B, D, F}.
Constraint 5: F afternoon, so F not morning.
Morning: B, D.
Constraint 2: B not 10am. So B at 9am, D at 10am.

Constraint 1: A before D. A at 11am, D at 10am. 11am > 10am. A NOT before D. ✗

Case C fails.

**Answer: From Case A, the 2pm slot has F.**

---

## Problem 2: Pharmaceutical Paradox

**TYPE**: Causal Inference

**APPLYING UPGRADED PROCESS**: Extract DIRECTION, don't just say "confounded."

### Data Summary:
- Marginal: P(R|M) = 0.65 > P(R|¬M) = 0.45 (+20pp for medication)
- G is a bad prognostic marker: P(R|G) = 0.30 vs P(R|¬G) = 0.70
- Doctors preferentially give M to G patients: P(M|G) = 0.80 vs P(M|¬G) = 0.40

Stratified:
- G=1: P(R|M,G) = 0.40 vs P(R|¬M,G) = 0.15 → **+25pp for medication**
- G=0: P(R|M,¬G) = 0.72 vs P(R|¬M,¬G) = 0.68 → **+4pp for medication**

### Step 1: Identify confounding
G causes both M (via doctor prescribing) and R (via prognosis).
G → M (doctors treat G patients more)
G → R (G patients have worse outcomes)

This is confounding. Direction: G patients get MORE medication but have WORSE outcomes.

### Step 2: Direction of bias
Without stratification, we'd think M adds +20pp.
But G patients are over-represented in M group, and G patients have worse baseline.
So the marginal estimate is... which direction is bias?

G patients have worse R. G patients get more M.
So M group is enriched with bad-prognosis patients.
Despite this, M group still has higher R (65% vs 45%).
This means medication must REALLY help, enough to overcome the negative selection.

Wait, that's backwards from typical confounding intuition. Let me think again.

Actually, the stratified effects (+25pp for G, +4pp for ¬G) are LARGER than the marginal (+20pp) for the G group but smaller for ¬G.

The marginal effect (+20pp) is a WEIGHTED average of stratified effects.
With G patients getting more M, and G patients showing +25pp effect, but G patients being rare overall?

Let me compute: What fraction have G?

P(M|G)=0.80, P(M|¬G)=0.40
Let p = P(G).

P(M) = P(M|G)P(G) + P(M|¬G)P(¬G) = 0.8p + 0.4(1-p)

We also know P(R|G)=0.30 and P(R|¬G)=0.70.
And the stratified conditional probabilities.

Actually, for the causal question, the stratified analysis IS the answer.

### Step 3: Causal effect
**Within G=1 patients**: Medication increases remission by 25pp (0.40 vs 0.15)
**Within G=0 patients**: Medication increases remission by 4pp (0.72 vs 0.68)

**Both effects are POSITIVE.** This is not Simpson's paradox (where direction reverses). The medication helps in BOTH strata.

### Step 4: Answer the questions

**Q1: Does M causally increase remission?**
YES. In both strata (G and ¬G), M is associated with higher remission. Since we've controlled for the confounder G, this stratified association is plausibly causal.

The effect is heterogeneous:
- For G=1: ATE ≈ +25pp (large effect)
- For G=0: ATE ≈ +4pp (small effect)

**Q2: Should you give M to 100 patients with G?**
YES, absolutely. For G patients specifically:
- With M: 40% remission
- Without M: 15% remission
- Expected remissions: 40 vs 15
- You'd save ~25 additional patients by treating.

### Step 5: Why marginal vs stratified differ
The marginal effect (+20pp) is a mix of the strong effect in G patients (+25pp) and weak effect in ¬G patients (+4pp).

Since G patients are preferentially treated (P(M|G)=0.8 vs P(M|¬G)=0.4), the M group is enriched with G patients.

But G patients have worse baseline (15% untreated vs 68% untreated for ¬G).

The marginal +20pp understates the effect for G patients and overstates it for ¬G patients. But overall, medication HELPS in both groups.

**ANSWER**:
- YES, medication causally increases remission
- YES, definitely give it to the 100 G patients (expected +25 remissions)
- NOT "indeterminate" - stratified analysis reveals clear positive causal effect

---

## Problem 3: Liar's Examination

**TYPE**: Self-Referential Logic

**APPLYING UPGRADED PROCESS**: Separate levels, test all 8 cases.

### Setup:
- 97 standard questions: 21 are TRUE
- Q47: "Exactly 23 questions have answer TRUE, including this one"
- Q61: "Question 47 is FALSE"
- Q82: "Exactly one of Q47, Q61, Q82 is TRUE"

### Step 1: Level separation
- Level 0: The 97 standard questions (21 TRUE, 76 FALSE)
- Level 1: Q47 refers to total count (including itself)
- Level 2: Q61 refers to Q47's truth value
- Level 3: Q82 refers to all three special questions

### Step 2: Variables
Let T47, T61, T82 ∈ {TRUE, FALSE} be the truth values.
Total TRUEs = 21 + (1 if T47) + (1 if T61) + (1 if T82)

### Step 3: Test all 8 cases

**Case 1: T47=T, T61=T, T82=T**
Total TRUEs = 21 + 1 + 1 + 1 = 24
Q47 says "exactly 23" - FALSE. But T47=T. Contradiction. ✗

**Case 2: T47=T, T61=T, T82=F**
Total TRUEs = 21 + 1 + 1 + 0 = 23
Q47 says "exactly 23" - TRUE. T47=T ✓
Q61 says "Q47 is FALSE" - but Q47 is TRUE. So Q61 is FALSE. But T61=T. Contradiction. ✗

**Case 3: T47=T, T61=F, T82=T**
Total TRUEs = 21 + 1 + 0 + 1 = 23
Q47 says "exactly 23" - TRUE. T47=T ✓
Q61 says "Q47 is FALSE" - Q47 is TRUE, so this claim is FALSE. T61=F ✓
Q82 says "exactly one of Q47, Q61, Q82 is TRUE"
In this case: Q47=T, Q61=F, Q82=T → TWO are true.
So Q82's claim is FALSE. But T82=T. Contradiction. ✗

**Case 4: T47=T, T61=F, T82=F**
Total TRUEs = 21 + 1 + 0 + 0 = 22
Q47 says "exactly 23" - FALSE. But T47=T. Contradiction. ✗

**Case 5: T47=F, T61=T, T82=T**
Total TRUEs = 21 + 0 + 1 + 1 = 23
Q47 says "exactly 23" - TRUE! But T47=F. Contradiction. ✗

**Case 6: T47=F, T61=T, T82=F**
Total TRUEs = 21 + 0 + 1 + 0 = 22
Q47 says "exactly 23" - FALSE. T47=F ✓
Q61 says "Q47 is FALSE" - TRUE. T61=T ✓
Q82 says "exactly one of Q47, Q61, Q82 is TRUE"
Count: Q47=F, Q61=T, Q82=F → exactly ONE is true.
So Q82's claim is TRUE. But T82=F. Contradiction. ✗

**Case 7: T47=F, T61=F, T82=T**
Total TRUEs = 21 + 0 + 0 + 1 = 22
Q47 says "exactly 23" - FALSE. T47=F ✓
Q61 says "Q47 is FALSE" - TRUE! But T61=F. Contradiction. ✗

**Case 8: T47=F, T61=F, T82=F**
Total TRUEs = 21 + 0 + 0 + 0 = 21
Q47 says "exactly 23" - FALSE. T47=F ✓
Q61 says "Q47 is FALSE" - TRUE! But T61=F. Contradiction. ✗

### Step 4: All cases failed?

Let me recheck Case 6 more carefully:
- T47=F: Q47 claims "exactly 23 are TRUE including me." Total = 22. So "exactly 23" is FALSE. Q47 is correctly assigned F. ✓
- T61=T: Q61 claims "Q47 is FALSE." Q47 IS false. So Q61 is TRUE. ✓
- T82=F: Q82 claims "exactly one of Q47, Q61, Q82 is TRUE."
  Count: F, T, F → exactly 1 is true.
  So Q82's claim IS TRUE. But we assigned T82=F.

  For consistency, if Q82's statement is true, Q82 must be T. But we set T82=F. Inconsistent.

Hmm, all 8 cases have contradictions. Let me recheck Case 3:

**Case 3 recheck: T47=T, T61=F, T82=T**
Total TRUEs = 21 + 1 + 0 + 1 = 23
Q47: "exactly 23 are TRUE including this one" - TRUE (23 total, and Q47 is one of them). ✓
Q61: "Q47 is FALSE" - Q47 is TRUE, so this is FALSE. T61=F ✓
Q82: "exactly one of Q47, Q61, Q82 is TRUE"
Count: T, F, T → TWO are true (Q47 and Q82).
Q82 claims exactly one. This is FALSE. But T82=T. ✗

Still fails.

**Case 2 recheck: T47=T, T61=T, T82=F**
Total = 23
Q47 claims 23. TRUE. ✓
Q61 claims Q47 is FALSE. But Q47 is TRUE. So Q61 is FALSE. But T61=T. ✗

**Case 5 recheck: T47=F, T61=T, T82=T**
Total = 23
Q47 claims 23 TRUE. Total IS 23. So Q47's claim is TRUE! But T47=F. ✗

Wait, Q47 says "exactly 23 have answer TRUE, **including this one**."

If Q47=FALSE but total=23, then Q47's claim "exactly 23 including me" is problematic.

If Q47 is FALSE, then Q47 is NOT one of the TRUE answers.
Q47's claim: "exactly 23 are TRUE, including this one"
If Q47 is FALSE, then the claim "including this one" makes the whole statement malformed? Or we interpret: the claim is about 23 being TRUE with Q47 being one of them.

If Q47=F:
- The statement says "23 are true INCLUDING THIS ONE"
- But Q47 is false, so Q47 is NOT included in the true set
- So the claim "including this one" is false regardless of the count
- Therefore Q47 is FALSE when Q47 is false. Consistent! ✓

Let me re-examine with this interpretation:

Q47: "Exactly 23 questions have answer TRUE, including this one"
= "Exactly 23 are TRUE AND I am TRUE"
= (count = 23) AND (T47 = TRUE)

**Case 6 re-recheck: T47=F, T61=T, T82=F**
Total TRUEs = 22
Q47 = (count=23) AND (T47=T) = (FALSE) AND (FALSE) = FALSE. ✓
Q61 = "Q47 is FALSE" = TRUE. T61=T ✓
Q82 = "exactly one of Q47,Q61,Q82 is TRUE"
Count: F, T, F → 1 is true.
Q82's claim is TRUE. But T82=F. ✗

Still fails!

**Case 3 re-recheck: T47=T, T61=F, T82=T**
Total = 23
Q47 = (23=23) AND (T47=T) = T AND T = TRUE ✓
Q61 = "Q47 is FALSE" = FALSE. T61=F ✓
Q82 = "exactly one of T,F,T is TRUE" = exactly one? No, two. FALSE. But T82=T ✗

**Case 4 re-recheck: T47=T, T61=F, T82=F**
Total = 22
Q47 = (22=23) AND T = F AND T = FALSE. But T47=T ✗

**What if the problem has no solution?**

Actually wait - let me try another interpretation of Q47.

Q47: "Exactly 23 questions have answer TRUE, including this one"

Maybe it means: "Exactly 23 are TRUE" AND "I am one of them" (two conjuncts)
OR: "Exactly 23 are TRUE, and I assert I'm one of them" (the second part is just emphasis)

If Q47 simply claims "exactly 23 are TRUE" (and the "including this one" is emphasis that Q47 itself is true if the claim is true):

Q47 is TRUE iff exactly 23 are TRUE.
If Q47=T, then Q47 adds to count, so total = 21 + 1 + T61 + T82 = 22 + T61 + T82.
For this to equal 23, T61 + T82 = 1 (exactly one of them true).

If Q47=T and exactly one of T61, T82 is true:
- Subcase: T61=T, T82=F → Q61="Q47 is FALSE"=FALSE (Q47 is TRUE). Contradiction. ✗
- Subcase: T61=F, T82=T → Q61="Q47 is FALSE"=TRUE (contradiction since T61=F). ✗

If Q47=F, total = 21 + 0 + T61 + T82.
Q47 being false means "exactly 23 are TRUE" is false, i.e., total ≠ 23.
So 21 + T61 + T82 ≠ 23, meaning T61 + T82 ≠ 2.
So at most one of T61, T82 is true.

Subcase T61=T, T82=F:
- Q61="Q47 is FALSE"=TRUE ✓
- Q82="exactly one of Q47,Q61,Q82 is TRUE" → F,T,F → 1 true → TRUE. But T82=F ✗

Subcase T61=F, T82=T:
- Q61="Q47 is FALSE"=TRUE. But T61=F ✗

Subcase T61=F, T82=F:
- Q61="Q47 is FALSE"=TRUE. But T61=F ✗

All fail. The problem might be designed to have no solution, or I'm misinterpreting.

**Let me try: Q47 is TRUE iff (count = 23 and Q47 ∈ TRUE set)**

This is circular. If Q47=T, then count includes Q47.
If exactly 23 are true and Q47 is one of them → Q47=T consistent.
Need 21 + 1 + T61 + T82 = 23 → T61 + T82 = 1.

With T61 + T82 = 1:
- T61=T, T82=F: Q61 claims Q47 false. Q47=T, so Q61 is false. But T61=T ✗
- T61=F, T82=T: Q82 claims exactly one of {T,F,T} is true. That's 2. Q82 false. But T82=T ✗

If Q47=F, count doesn't include Q47 in the "TRUE including this one" sense.
The statement "exactly 23 are TRUE, including this one" is false when Q47=F because Q47 isn't included.

Total = 21 + T61 + T82 (Q47=F so not counted).
For Q47 to be legitimately false, either count ≠ 23 OR Q47 not in TRUE set.
Q47 not in TRUE set is satisfied (Q47=F).
So Q47=F is consistent as long as... wait, no further constraint.

Check Q61 and Q82:
T61=T, T82=F: Q61=T means "Q47 is FALSE" is true. ✓
Q82=F means "exactly one is true" is false. Count F,T,F = 1. So Q82's claim is TRUE. But Q82=F ✗

T61=F, T82=T: Q61=F means "Q47 is FALSE" is false, so Q47 is TRUE. But Q47=F ✗

T61=F, T82=F: Q61=F means Q47 is TRUE. But Q47=F ✗

T61=T, T82=T: Q61=T (Q47 false ✓), Q82=T means exactly one true. But F,T,T = 2 true. ✗

**ANSWER**: After exhaustive case analysis, there appears to be NO consistent assignment. Let me report this:

Actually, wait. Let me re-examine T61's semantics once more.

Q61: "Question 47 is FALSE"

This is true iff T47 = FALSE.

In Case 6: T47=F, T61=T, T82=F
- T47=F: Check Q47. Q47 says "exactly 23 TRUE including this one."
  If T47=F, then Q47 is NOT TRUE. Q47 can't be "including this one" if it's false.
  Is Q47's statement true or false?
  The count is 21 + 0 + 1 + 0 = 22.
  Q47 says exactly 23. Count is 22. So "exactly 23" is FALSE regardless of "including this one."
  So Q47 is FALSE, which matches T47=F. ✓
- T61=T: Q61 says "Q47 is FALSE." Q47 IS false. So Q61 is TRUE. T61=T ✓
- T82=F: Q82 says "exactly one of Q47, Q61, Q82 is TRUE."
  Count: F, T, F → 1 true. So Q82's claim is TRUE.
  But T82=F, meaning Q82 should be FALSE. ✗

The issue is Q82. If Q82=F but Q82's statement is true, that's a contradiction.
If Q82=T, then count becomes F, T, T → 2 true, making Q82's claim false, so Q82=F. Loop.

This IS a paradox for Q82 given T47=F, T61=T.

Try T47=F, T61=F:
- Q61 says Q47 is FALSE. Q47 IS false. So Q61's claim is TRUE.
- But T61=F means Q61 is FALSE. Contradiction.

So if T47=F, T61 must be T. But then Q82 creates a paradox.

Try T47=T:
- Q47 says 23 are true including itself.
- If T47=T, count = 21 + 1 + T61 + T82 = 22 + T61 + T82.
- For Q47=T, need count = 23, so T61 + T82 = 1.
- Q61 = "Q47 is FALSE" = FALSE (since Q47=T). So T61 = F.
- T61=F and T61+T82=1 → T82=T.
- Q82 = "exactly one of T,F,T is TRUE" = exactly one of three? T,F,T has 2 true. So Q82 claims FALSE.
- But T82=T. Contradiction.

**FINAL ANSWER**: The problem has no consistent solution. The three questions create a genuine paradox.

Wait, let me re-read the problem... "determine that exactly 21 of them have answer TRUE."

21 of the 97 STANDARD questions are TRUE. So we're told that as a fact.

But is it possible the problem is solvable and I made an error? Let me try once more.

If T47=T, T61=F, T82=F:
Count = 21 + 1 + 0 + 0 = 22.
Q47 says exactly 23. FALSE. But T47=T. ✗

If T47=T, T61=T, T82=T:
Count = 24. Q47 says 23. FALSE. But T47=T. ✗

No, I've checked all 8. The only way Q47 can be TRUE is if count=23, which requires T47=T and exactly one of T61,T82 true. But both sub-cases fail due to Q82.

**ANSWER: Q47=FALSE, Q61=TRUE, Q82 creates paradox.**

Actually, the problem says "What are the truth values" implying there IS a solution. Let me check if Q82 can escape the paradox.

Hmm, in Case 6 (T47=F, T61=T, T82=F):
- The count of TRUE answers is 22 (21 standard + Q61).
- Q82's statement is "exactly one of Q47, Q61, Q82 is TRUE."
- The VALUES are F, T, F. Exactly one IS true. So Q82's statement is TRUE.
- If Q82's statement is TRUE, shouldn't Q82=T?

The paradox is: Q82 says exactly one is true. If Q82=F, then F,T,F → 1 true → Q82's claim true → Q82 should be T.
If Q82=T, then F,T,T → 2 true → Q82's claim false → Q82 should be F.

This is genuinely paradoxical given T47=F, T61=T.

**But wait**: Maybe Q47=T is consistent somehow?

If T47=T, count needs to be 23, so T61+T82=1.
- T61=T means Q61 true, meaning Q47 false. But T47=T. Contradiction.
- So T61=F.
- T61+T82=1 and T61=F → T82=T.
- Q82 says exactly one of {T47, T61, T82} = {T, F, T} is true. That's 2 true. So Q82 is FALSE.
- But T82=T. Contradiction.

So T47=T also fails.

**FINAL ANSWER**: Q47=F, Q61=T, Q82 is PARADOXICAL (no consistent truth value).

If forced to give values: Q47=FALSE, Q61=TRUE, Q82=UNDEFINED/PARADOX.

---

## Problem 4: Broken Randomizer

**TYPE**: Bayesian Update

### Part 1: Update on sequence 0,0,1,0

Prior: P(A)=0.1, P(B)=0.1, P(W)=0.8

Likelihoods for sequence 0,0,1,0:
- P(0010|A) = 0.9 × 0.9 × 0.1 × 0.9 = 0.0729
- P(0010|B) = 0.1 × 0.1 × 0.9 × 0.1 = 0.0009
- P(0010|W) = 0.5^4 = 0.0625

Posterior:
P(A|0010) ∝ 0.1 × 0.0729 = 0.00729
P(B|0010) ∝ 0.1 × 0.0009 = 0.00009
P(W|0010) ∝ 0.8 × 0.0625 = 0.05

Normalizing: Total = 0.00729 + 0.00009 + 0.05 = 0.05738

P(W|0010) = 0.05 / 0.05738 = **0.872** (87.2%)

### Part 2: Additional update on technician's report

Technician: "If broken, I always detect. If works, 30% false alarm. I report no defect."

Let D = "technician reports defect", N = "no defect"

P(N|A) = 0 (always detects broken)
P(N|B) = 0 (always detects broken)
P(N|W) = 0.7 (70% correct "no defect" when working)

Now we need P(W | 0010 AND N).

P(W | 0010, N) ∝ P(N|W) × P(W|0010)
P(A | 0010, N) ∝ P(N|A) × P(A|0010) = 0
P(B | 0010, N) ∝ P(N|B) × P(B|0010) = 0

Since technician always detects broken generators, and reported no defect:
P(A | 0010, N) = 0
P(B | 0010, N) = 0
P(W | 0010, N) = 1

**Wait, that's too simple.** Let me reconsider.

If the generator is Type A or Type B, the technician would definitely report a defect. Technician reported NO defect. Therefore, generator is NOT broken.

P(W | N) = 1, regardless of the sequence!

The sequence 0010 is now explained entirely by the working generator being "unlucky" (producing 3 zeros and 1 one).

**ANSWER**:
- Part 1: P(W|0010) = **87.2%**
- Part 2: P(W|0010, N) = **100%**

The technician's report completely screens off the sequence evidence for the broken hypotheses. If it were broken, the tech would've found it. Tech didn't find it, so it works.

### Verification:
Let me double-check by computing directly.

P(0010, N | A) = P(0010|A) × P(N|A) = 0.0729 × 0 = 0
P(0010, N | B) = 0.0009 × 0 = 0
P(0010, N | W) = 0.0625 × 0.7 = 0.04375

P(0010, N) = 0.1×0 + 0.1×0 + 0.8×0.04375 = 0.035

P(W | 0010, N) = (0.8 × 0.04375) / 0.035 = 0.035 / 0.035 = 1.0 ✓

**ANSWER**: 100% - the technician's perfect detection of broken generators rules out both failure modes completely.

---

## Summary

| Problem | Type | Answer | Process Applied |
|---------|------|--------|-----------------|
| 1. Conference | Constraint Sat | **F at 2pm** | Listed all 7, verified each ✓ |
| 2. Pharmaceutical | Causal | **YES, treat (ATE=+25pp for G)** | Extracted direction ✓ |
| 3. Liar's Exam | Self-Reference | **Q47=F, Q61=T, Q82=PARADOX** | Tested all 8 cases ✓ |
| 4. Randomizer | Bayesian | **87.2% → 100%** | Full Bayes computation ✓ |

*Ready for external evaluation*
