# Logic and Reasoning Validation - Cycle 1: My Solutions

## PROBLEM 1: DEDUCTIVE (Club Membership)

**Problem:** Alice says "Every member must either play chess or speak French." Bob knows someone with chess, French, AND tennis who isn't a member. Carol concludes Alice's statement doesn't tell us the membership rules.

**MY EXTERNALIZED REASONING:**

Step 1: Translate Alice's statement to formal logic.
"Every member must either play chess or speak French"
= For all x: Member(x) → (Chess(x) ∨ French(x))

Step 2: Identify what kind of condition this is.
This is a NECESSARY condition for membership.
- It tells us: IF member → THEN (chess OR french)
- It does NOT tell us: IF (chess OR french) → THEN member

Step 3: Analyze Bob's counterexample.
Bob's person: Has Chess ∧ French ∧ Tennis but is NOT a member.
This person satisfies (Chess ∨ French) but fails Member.

Step 4: Does this violate Alice's rule?
Alice's rule would be violated by: Member ∧ ¬(Chess ∨ French)
Bob shows: ¬Member ∧ (Chess ∨ French)

These are different! Bob's example is logically consistent with Alice's rule.

Step 5: Evaluate Carol's conclusion.
Carol treats Alice's necessary condition as if it were sufficient.
This is the fallacy of affirming the consequent / confusing necessary and sufficient conditions.

**MY ANSWER:** Carol's conclusion is INVALID. Alice stated a necessary condition for membership. Bob's counterexample (someone who satisfies the condition but isn't a member) doesn't contradict a necessary condition - it would only contradict a sufficient condition. Carol commits the error of confusing necessary and sufficient conditions.

---

## PROBLEM 2: INDUCTIVE (Medical Test)

**Problem:** Test has 95% sensitivity, 90% specificity. Clinic A has 40% prevalence, Clinic B has 0.5% prevalence. Dr. Martinez tells both positive patients they "almost certainly" have the disease.

**MY EXTERNALIZED REASONING:**

Step 1: Define terms.
- Sensitivity = P(Positive | Disease) = 0.95
- Specificity = P(Negative | No Disease) = 0.90
- So P(Positive | No Disease) = 0.10 (false positive rate)

Step 2: Apply Bayes for Clinic A (40% prevalence).
P(Disease) = 0.40
P(No Disease) = 0.60

P(Positive) = P(Pos|D)×P(D) + P(Pos|¬D)×P(¬D)
            = (0.95)(0.40) + (0.10)(0.60)
            = 0.38 + 0.06 = 0.44

P(Disease | Positive) = P(Pos|D)×P(D) / P(Positive)
                      = 0.38 / 0.44 = 0.864 ≈ **86.4%**

Step 3: Apply Bayes for Clinic B (0.5% prevalence).
P(Disease) = 0.005
P(No Disease) = 0.995

P(Positive) = (0.95)(0.005) + (0.10)(0.995)
            = 0.00475 + 0.0995 = 0.10425

P(Disease | Positive) = 0.00475 / 0.10425 = **4.56%**

Step 4: Evaluate Dr. Martinez's reasoning.
Clinic A: 86% - "almost certainly" is reasonably accurate.
Clinic B: 4.6% - "almost certainly" is WRONG. Patient more likely negative!

**MY ANSWER:** Dr. Martinez commits base rate neglect. In Clinic A (86%), the statement is reasonable. In Clinic B (4.6%), it's dramatically wrong - the patient is 20x more likely to NOT have the disease. The same test result means completely different things depending on prevalence.

---

## PROBLEM 3: PROBABILISTIC (Game Show)

**Problem:** Prize placed by die: 1-4 in Red (2/3), 5 in Blue (1/6), 6 in Green (1/6). I choose Red. Host opens Green (empty). Switch to Blue?

**MY EXTERNALIZED REASONING:**

Step 1: Initial probabilities.
P(Red) = 4/6 = 2/3
P(Blue) = 1/6
P(Green) = 1/6

Step 2: Model host's behavior.
Host knows where prize is, opens an empty box (not my choice, not the prize).

P(Opens Green | Prize in Red) = Host can open Blue or Green. Assume random: 1/2
P(Opens Green | Prize in Blue) = Host must open Green (can't open Blue-prize or Red-mine): 1
P(Opens Green | Prize in Green) = Host cannot open Green: 0

Step 3: Calculate P(Opens Green).
P(OG) = (1/2)(2/3) + (1)(1/6) + (0)(1/6)
      = 1/3 + 1/6 + 0 = 2/6 + 1/6 = 3/6 = 1/2

Step 4: Apply Bayes.
P(Red | Opens Green) = P(OG|Red)×P(Red) / P(OG)
                     = (1/2)(2/3) / (1/2) = (1/3)/(1/2) = **2/3**

P(Blue | Opens Green) = P(OG|Blue)×P(Blue) / P(OG)
                      = (1)(1/6) / (1/2) = (1/6)/(1/2) = **1/3**

Step 5: Compare and decide.
P(Red | OG) = 2/3
P(Blue | OG) = 1/3
Red is twice as likely as Blue.

**MY ANSWER:** STAY with Red. Unlike standard Monty Hall (where switching doubles your odds), here Red started with higher probability (2/3) and remains more likely (2/3 vs 1/3) after the reveal. Blue improved from 1/6 to 1/3 (doubling), but still less than Red.

---

## PROBLEM 4: CAUSAL (WFH Productivity)

**Problem:** WFH employees have 25% higher productivity. CEO wants to mandate WFH. Employees self-select, seniors have more WFH flexibility, new junior hires work in-office for training.

**MY EXTERNALIZED REASONING:**

Step 1: Identify the causal claim.
Implicit claim: WFH → Higher Productivity

Step 2: Identify confounders.
PRIMARY CONFOUNDER - Seniority/Experience:
- Senior → More likely to choose WFH (flexibility)
- Senior → Higher productivity (more skilled, efficient)
- Seniority causes BOTH, creating spurious correlation

SELECTION BIAS:
- Self-selection into WFH is not random
- Those choosing WFH may already be more independent/productive
- Those needing supervision may stay in-office

POSSIBLE REVERSE CAUSATION:
- High productivity → Rewarded with WFH privileges

Step 3: Check for Simpson's Paradox potential.
Within seniors only: WFH might show no effect
Within juniors only: In-office might be better (training)
Aggregation hides this.

Step 4: Evaluate the CEO's proposal.
Problems:
1. Removes selection effects (forcing WFH on in-office-choosers)
2. Juniors may need in-person mentoring
3. No causal evidence justifies the mandate
4. Current correlation exists under CHOICE regime

Step 5: What would establish causation?
- RCT: Randomly assign WFH vs in-office
- Matched comparison controlling for seniority, role, tenure
- Natural experiment if policy change created random variation

**MY ANSWER:** The correlation does NOT establish causation. Seniority is an obvious confounder causing both WFH preference and higher productivity. Self-selection bias is present. Mandating WFH based on this data would likely fail because the correlation reflects WHO chooses WFH, not the effect of WFH itself. Need controlled study to establish causation.

---

## PROBLEM 5: ARGUMENT ANALYSIS (Bike Lanes)

**Problem:** Editorial argues against bike lanes using Oak Street data (3% car decrease, 8% increase on parallels) and survey data (78% drivers oppose, 45% cyclists support).

**MY EXTERNALIZED REASONING:**

Step 1: Extract the claims.
Claim 1: Bike lanes don't reduce congestion, they divert traffic
Evidence: Oak Street data
Claim 2: Majority (drivers) opposes, so democracy requires rejection
Evidence: Survey

Step 2: Analyze Claim 1 - Oak Street evidence.
HASTY GENERALIZATION: One street ≠ all streets. Different contexts, designs, etc.
INCOMPLETE EVIDENCE:
- Only measured car traffic, not person-throughput
- Didn't measure bike usage increase
- Didn't measure citywide vehicle-miles traveled
- Short-term vs long-term effects?
CHERRY-PICKED METRIC: "Congestion" could mean time, not just volume

Step 3: Analyze Claim 2 - Survey evidence.
BIASED SAMPLE: Surveyed "drivers" - excludes potential cyclists
NON-PARALLEL QUESTIONS: "Oppose" vs "support" are framed differently
FALSE COMPARISON: 78% of drivers vs 45% of cyclists - different denominators
APPEAL TO MAJORITY: Democratic principles ≠ simple majority on every issue
- Externalities (pollution, safety) affect non-voters
- Minority rights (cyclist safety) matter
- Long-term planning vs short-term preference

Step 4: Identify hidden premises.
- "Road users" = drivers (question-begging - excludes cyclists/pedestrians)
- Current usage should determine future infrastructure
- Short-term convenience > long-term benefits
- Only car metrics matter (ignores health, environment, safety)

Step 5: List all fallacies.
1. Hasty generalization (one street → all)
2. Cherry-picked/incomplete evidence
3. Appeal to majority/popularity
4. Biased survey
5. Question-begging definition ("road users" = drivers)
6. Ignoring externalities

**MY ANSWER:** The argument contains: (1) Hasty generalization from single Oak Street example, (2) Incomplete evidence ignoring bike usage and person-throughput, (3) Biased survey of "drivers" excluding potential cyclists, (4) Appeal to majority that ignores externalities and minority rights, (5) Hidden premise equating "road users" with drivers. The evidence doesn't support the conclusion.

---

## PROBLEM 6: NOVEL (Transparent Prediction Paradox)

**Problem:** AI predicts my choice (100% accuracy), sealed. Option A: $1K guaranteed. Option B: $0, but $1M if AI predicted A. AI argues prediction is independent of my current choice.

**MY EXTERNALIZED REASONING:**

Step 1: Understand the payoff structure.
If AI predicted A and I choose A: $1,000
If AI predicted A and I choose B: $1,000,000
If AI predicted B and I choose A: $1,000
If AI predicted B and I choose B: $0

Step 2: Analyze AI's argument (Causal Decision Theory).
"Prediction is fixed. Your choice now cannot causally affect past."
This is TRUE - I cannot change what's in the envelope.

Step 3: But consider the correlation.
AI has 100% accuracy. This means:
- Everyone who chose A was predicted to choose A
- Everyone who chose B was predicted to choose B
- NO ONE has ever gotten $1M (because anyone choosing B was predicted B)

Step 4: What does 100% accuracy mean?
It means my DECISION TYPE determines the prediction.
If I'm a "choose B type" → AI predicted B → I get $0
If I'm a "choose A type" → AI predicted A → I get $1K

Step 5: The paradox.
The AI's causal independence argument is technically correct but misleading.
- Causally: I can't change the envelope
- Evidentially: My choice reveals/is correlated with what's in envelope
- The $1M is unreachable: anyone who would choose B was predicted B

Step 6: Connect to Newcomb's Problem.
This is a variant of Newcomb's Problem.
- Causal Decision Theory: "Past is fixed, so consider B"
- Evidential Decision Theory: "My choice type determines prediction, so choose A"
- With 100% accuracy, EDT is practically correct.

**MY ANSWER:** Choose A, receive $1,000. The AI's "past is fixed" argument is technically true but practically misleading. With 100% predictive accuracy, the prediction correlates perfectly with my choice type. Anyone who chooses B was predicted to choose B and gets $0. The $1,000,000 is unreachable - it requires choosing B while having been predicted A, which never happens with perfect prediction. This is a Newcomb-like paradox where causal and evidential reasoning diverge.

---

## Summary of My Answers

| Problem | My Answer |
|---------|-----------|
| 1. Deductive | Carol invalid - confused necessary/sufficient conditions |
| 2. Inductive | Base rate neglect - 86% vs 4.6% |
| 3. Probabilistic | Stay with Red (2/3 vs 1/3) |
| 4. Causal | No causation - seniority confounds |
| 5. Argument | Multiple fallacies - hasty generalization, biased survey, appeal to majority, hidden premises |
| 6. Novel | Choose A - $1M unreachable with perfect prediction |
