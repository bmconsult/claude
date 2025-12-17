# Logic and Reasoning Foundations

## What This Is

Complete reference for logic and reasoning. Covers: reasoning types, formal logic, problem-solving protocols, common fallacies, failure modes. Knowledge layer only—no training exercises.

**Use:** Reference during reasoning tasks. Prerequisite knowledge for LOGIC_MASTERY.md.

---

# PART I: REASONING TYPES

## 1.1 Deductive Reasoning

**Definition:** From general premises to certain conclusions (if premises true).

```
All X are Y.          (Premise 1)
Z is X.               (Premise 2)
∴ Z is Y.             (Conclusion - CERTAIN if premises true)
```

**Key property:** Truth-preserving. If premises are true, conclusion MUST be true.

### Valid Argument Forms

```
MODUS PONENS (Affirming the Antecedent):
If P then Q
P
∴ Q                    ✓ VALID

MODUS TOLLENS (Denying the Consequent):
If P then Q
Not Q
∴ Not P                ✓ VALID

HYPOTHETICAL SYLLOGISM:
If P then Q
If Q then R
∴ If P then R          ✓ VALID

DISJUNCTIVE SYLLOGISM:
P or Q
Not P
∴ Q                    ✓ VALID

CONJUNCTION:
P
Q
∴ P and Q              ✓ VALID

SIMPLIFICATION:
P and Q
∴ P                    ✓ VALID

CONSTRUCTIVE DILEMMA:
(P → Q) ∧ (R → S)
P ∨ R
∴ Q ∨ S                ✓ VALID
```

### Invalid Forms (Formal Fallacies)

```
AFFIRMING THE CONSEQUENT:
If P then Q
Q
∴ P                    ✗ INVALID

Example: "If it rained, ground is wet. Ground is wet. ∴ It rained."
(Sprinkler could cause wet ground)

DENYING THE ANTECEDENT:
If P then Q
Not P
∴ Not Q                ✗ INVALID

Example: "If it's a dog, it's a mammal. Not a dog. ∴ Not a mammal."
(Could be a cat—still a mammal)
```

### Validity vs Soundness

| Term | Definition |
|------|------------|
| **Valid** | Structure is correct—if premises true, conclusion must be true |
| **Sound** | Valid AND all premises are actually true |

An argument can be valid but unsound (correct structure, false premises).

---

## 1.2 Inductive Reasoning

**Definition:** From specific observations to probable generalizations.

```
Swan 1 is white, Swan 2 is white, ... Swan 1000 is white
∴ All swans are (probably) white

Note: PROBABLE, not certain. (Black swans exist.)
```

**Key property:** Ampliative—conclusion goes beyond premises. Never certain.

### Strength Factors

| Factor | Stronger | Weaker |
|--------|----------|--------|
| Sample size | Large n | Small n |
| Sample diversity | Varied conditions | Single condition |
| Representativeness | Random sample | Convenience sample |
| Conclusion scope | Narrow claim | Broad claim |

### Common Inductive Failures

| Failure | Description |
|---------|-------------|
| Hasty generalization | Too few instances |
| Biased sample | Unrepresentative selection |
| Base rate neglect | Ignoring prior probability |
| Confirmation bias | Only noticing confirming evidence |

---

## 1.3 Abductive Reasoning

**Definition:** Inference to the best explanation.

```
Observation: The grass is wet
Possible explanations: Rain, sprinkler, dew, flood
Best explanation: Rain (most common, fits evidence)
∴ It probably rained
```

**Key property:** Generates hypotheses. Neither certain nor purely probabilistic.

### Criteria for "Best" Explanation

| Criterion | Question |
|-----------|----------|
| **Explanatory power** | How much evidence does it explain? |
| **Simplicity** | How few assumptions required? (Occam's Razor) |
| **Consistency** | Does it fit other known facts? |
| **Testability** | Can it be verified or falsified? |
| **Prior probability** | How likely is this explanation independently? |

---

## 1.4 Causal Reasoning

**Definition:** Determining what causes what.

```
Correlation: Ice cream sales and drownings both rise in summer
Causation? No. Common cause: hot weather causes both.
```

**Key property:** Requires more than correlation.

### Causal Criteria

| Criterion | Question |
|-----------|----------|
| Correlation | Do they co-vary? |
| Temporal precedence | Does cause precede effect? |
| Mechanism | Is there a plausible pathway? |
| No confounds | Are third variables ruled out? |
| Counterfactual | Would removing cause remove effect? |

### Causal Patterns

```
DIRECT CAUSATION:       A → B

COMMON CAUSE:              C
                         ↙   ↘
                        A     B
(A and B correlated but neither causes other)

CAUSAL CHAIN:           A → B → C
(A and C correlated through B)

REVERSE CAUSATION:      Think A → B, actually B → A
```

### Causal Fallacies

| Fallacy | Error |
|---------|-------|
| Post hoc ergo propter hoc | "After, therefore because" |
| Correlation = causation | Ignoring confounds |
| Reverse causation | Direction backwards |
| Omitted variable | Missing common cause |

---

## 1.5 Analogical Reasoning

**Definition:** Inferring properties based on similarity to another case.

```
Source: Atoms have electrons orbiting nucleus
Target: Solar system has planets orbiting sun
Inference: Atomic structure might be like solar system
```

**Key property:** Strength depends on relevance of similarities.

### Analogy Strength Factors

| Factor | Stronger | Weaker |
|--------|----------|--------|
| Similarity type | Deep structural | Surface features only |
| Relevance | Similarities matter for conclusion | Irrelevant similarities |
| Differences | Minor, acknowledged | Major, ignored |
| Number | Many relevant similarities | Few similarities |

---

## 1.6 Probabilistic Reasoning

### Core Formulas

```
JOINT PROBABILITY:
P(A and B) = P(A) × P(B|A)
P(A and B) = P(A) × P(B)     [if independent]

CONDITIONAL PROBABILITY:
P(A|B) = P(A and B) / P(B)

BAYES THEOREM:
P(A|B) = P(B|A) × P(A) / P(B)

TOTAL PROBABILITY:
P(B) = Σ P(B|Ai) × P(Ai)     [for partition {Ai}]

EXPECTED VALUE:
E[X] = Σ xi × P(xi)
```

### Bayes Theorem Expanded

```
P(Hypothesis|Evidence) = P(Evidence|Hypothesis) × P(Hypothesis)
                         ─────────────────────────────────────────
                                        P(Evidence)

Where P(Evidence) = P(E|H)P(H) + P(E|¬H)P(¬H)
```

### Sequential Bayesian Updates

```
For evidence E1, E2, E3:

Update 1: P(H|E1) = P(E1|H)P(H) / P(E1)
Update 2: P(H|E1,E2) = P(E2|H)P(H|E1) / P(E2|E1)
Update 3: P(H|E1,E2,E3) = P(E3|H)P(H|E1,E2) / P(E3|E1,E2)

Each update: previous posterior becomes new prior
```

### Probabilistic Fallacies

| Fallacy | Error |
|---------|-------|
| Base rate neglect | Ignoring P(H) prior |
| Conjunction fallacy | P(A and B) > P(A) seems right |
| Gambler's fallacy | "Due for a win" after losses |
| Prosecutor's fallacy | Confusing P(E|H) with P(H|E) |
| Inverse fallacy | P(A|B) = P(B|A) |

---

# PART II: FORMAL LOGIC

## 2.1 Propositional Logic

### Symbols

| Symbol | Meaning | Read as |
|--------|---------|---------|
| ¬P | Negation | "Not P" |
| P ∧ Q | Conjunction | "P and Q" |
| P ∨ Q | Disjunction | "P or Q" (inclusive) |
| P → Q | Conditional | "If P then Q" |
| P ↔ Q | Biconditional | "P if and only if Q" |

### Truth Tables

```
NEGATION (¬P):
P | ¬P
T |  F
F |  T

CONJUNCTION (P ∧ Q):
P | Q | P ∧ Q
T | T |   T
T | F |   F
F | T |   F
F | F |   F

DISJUNCTION (P ∨ Q):
P | Q | P ∨ Q
T | T |   T
T | F |   T
F | T |   T
F | F |   F

CONDITIONAL (P → Q):
P | Q | P → Q
T | T |   T
T | F |   F
F | T |   T
F | F |   T

BICONDITIONAL (P ↔ Q):
P | Q | P ↔ Q
T | T |   T
T | F |   F
F | T |   F
F | F |   T
```

**Key insight:** P → Q is only FALSE when P is TRUE and Q is FALSE.

### Logical Equivalences

```
Double Negation:      ¬¬P ≡ P
Idempotence:          P ∧ P ≡ P,  P ∨ P ≡ P
Commutativity:        P ∧ Q ≡ Q ∧ P,  P ∨ Q ≡ Q ∨ P
Associativity:        (P ∧ Q) ∧ R ≡ P ∧ (Q ∧ R)
Distribution:         P ∧ (Q ∨ R) ≡ (P ∧ Q) ∨ (P ∧ R)
De Morgan's Laws:     ¬(P ∧ Q) ≡ ¬P ∨ ¬Q
                      ¬(P ∨ Q) ≡ ¬P ∧ ¬Q
Contraposition:       P → Q ≡ ¬Q → ¬P
Material Implication: P → Q ≡ ¬P ∨ Q
Exportation:          (P ∧ Q) → R ≡ P → (Q → R)
```

---

## 2.2 Predicate Logic

### Symbols

| Symbol | Meaning |
|--------|---------|
| ∀x | Universal quantifier: "For all x" |
| ∃x | Existential quantifier: "There exists x" |
| Px | x has property P |
| Rxy | x has relation R to y |

### Translation Examples

```
"All humans are mortal"
∀x(Human(x) → Mortal(x))

"Some birds can fly"
∃x(Bird(x) ∧ CanFly(x))

"No reptiles are mammals"
∀x(Reptile(x) → ¬Mammal(x))
   OR
¬∃x(Reptile(x) ∧ Mammal(x))

"Everyone loves someone"
∀x∃y(Loves(x,y))     ← Each person loves (possibly different) someone
∃y∀x(Loves(x,y))     ← There's one person everyone loves

Note: Quantifier order matters!
```

### Negating Quantified Statements

```
¬∀xP(x) ≡ ∃x¬P(x)
"Not everything is P" = "Something is not P"

¬∃xP(x) ≡ ∀x¬P(x)
"Nothing is P" = "Everything is not P"
```

### Quantifier Scope

```
∀x∃y R(x,y)  ≠  ∃y∀x R(x,y)

Example with "loves":
∀x∃y Loves(x,y): Everyone loves someone (different people)
∃y∀x Loves(x,y): Someone is loved by everyone (same person)
```

---

# PART III: PROBLEM-SOLVING PROTOCOLS

## 3.1 Constraint Satisfaction

**Use when:** Multiple variables with constraints; find valid assignment.

```
PROTOCOL:

1. LIST variables and domains
   Variables: {A, B, C, ...}
   Domains: A ∈ {1,2,3}, B ∈ {1,2,3}, ...

2. NUMBER all constraints
   (1) A ≠ 1
   (2) B < C
   (3) ...

3. FIND forced assignments
   Which constraints immediately fix a variable?

4. PROPAGATE consequences
   If X = 3, what else must be true?

5. CASE SPLIT if stuck
   Case A: V = value1 → propagate → contradiction?
   Case B: V = value2 → propagate → contradiction?

6. VERIFY solution against ALL constraints
```

### Worked Example

```
Problem: A, B, C in slots 1, 2, 3. Constraints: A≠1, B<C, C≠3.

Variables: {A,B,C}, Domain: {1,2,3}
Constraints: (1) A≠1, (2) B<C, (3) C≠3

From (3): C ∈ {1,2}
From (2): If C=1, B<1 impossible. So C=2.
From (2): B<2, so B=1.
Remaining: A=3.

Verify: A≠1: 3≠1 ✓, B<C: 1<2 ✓, C≠3: 2≠3 ✓

Answer: A=3, B=1, C=2
```

---

## 3.2 Game Theory / Decision Analysis

**Use when:** Multiple agents, strategies, payoffs.

```
PROTOCOL:

1. IDENTIFY players

2. LIST strategies for each player

3. BUILD payoff matrix or game tree

4. CALCULATE each payoff:
   REVENUES:
   - [source]: amount
   COSTS:
   - [source]: amount
   NET = Revenue - Cost

5. ANALYZE:
   - Dominant strategies?
   - Nash equilibrium?
   - Backward induction (if sequential)?

6. VERIFY incentives at solution
```

### Key Concepts

| Concept | Definition |
|---------|------------|
| Dominant strategy | Best regardless of opponent's choice |
| Nash equilibrium | No player benefits from unilateral deviation |
| Pareto optimal | No one can improve without hurting another |
| Backward induction | Solve from end, work backwards |

---

## 3.3 Optimization

**Use when:** Maximize/minimize objective subject to constraints.

```
PROTOCOL:

1. DEFINE objective function

2. LIST all constraints

3. IDENTIFY feasible region

4. CHECK:
   - Boundary points
   - Corner points
   - Integer points (if required)

5. EVALUATE objective at each candidate

6. SELECT optimum

7. VERIFY constraints satisfied
```

### Common Traps

| Trap | Fix |
|------|-----|
| Missing constraint | List ALL constraints first |
| Interior-only search | Always check boundaries |
| Local vs global optimum | Search multiple regions |
| Continuous when integer | Verify integer requirement |

---

## 3.4 Bayesian Inference

**Use when:** Updating probability with evidence.

```
PROTOCOL:

1. DEFINE hypothesis H and evidence E

2. IDENTIFY:
   - Prior: P(H)
   - Likelihood: P(E|H)
   - P(E|¬H)

3. CALCULATE P(E):
   P(E) = P(E|H)P(H) + P(E|¬H)P(¬H)

4. APPLY Bayes:
   P(H|E) = P(E|H)P(H) / P(E)

5. SANITY CHECK:
   - Is result between 0 and 1?
   - Does direction make sense?
```

---

# PART IV: INFORMAL FALLACIES

## 4.1 Fallacies of Relevance

| Fallacy | Description | Example |
|---------|-------------|---------|
| Ad hominem | Attack person, not argument | "You're wrong because you're biased" |
| Appeal to authority | Irrelevant authority | "A celebrity says X is true" |
| Appeal to emotion | Substituting emotion for evidence | "Think of the children!" |
| Appeal to popularity | Majority belief = truth | "Everyone believes it" |
| Red herring | Irrelevant distraction | Changing subject when challenged |
| Straw man | Attacking weaker version | Misrepresenting opponent's argument |

## 4.2 Fallacies of Presumption

| Fallacy | Description | Example |
|---------|-------------|---------|
| Begging the question | Conclusion in premise | "God exists because the Bible says so, and the Bible is God's word" |
| False dilemma | Excluding middle options | "You're either with us or against us" |
| Complex question | Loaded question | "Have you stopped cheating?" |
| Slippery slope | Unsupported chain | "If A then eventually Z" without justification |

## 4.3 Fallacies of Ambiguity

| Fallacy | Description | Example |
|---------|-------------|---------|
| Equivocation | Shifting word meaning | "Light" (weight) vs "light" (brightness) |
| Amphiboly | Grammatical ambiguity | "I saw the man with the telescope" |
| Composition | Parts → whole | "Each part is light, so whole is light" |
| Division | Whole → parts | "Team is good, so each player is good" |

---

# PART V: FAILURE MODES

## 5.1 Structural Failures

| Failure | Description |
|---------|-------------|
| Invalid form | Reasoning structure is flawed |
| Missing premise | Hidden assumption not stated |
| Scope error | Quantifier scope wrong |
| Negation error | Negation applied incorrectly |

## 5.2 Content Failures

| Failure | Description |
|---------|-------------|
| False premise | Premise isn't true |
| Wrong probability | Numbers incorrect |
| Factual error | Mistaken facts |
| Category error | Applying concept to wrong type |

## 5.3 Process Failures

| Failure | Description |
|---------|-------------|
| Skipped steps | Assumed intermediate result |
| Premature conclusion | Stopped before complete |
| Lost state | Forgot earlier result |
| Wrong technique | Applied inappropriate method |

## 5.4 Meta Failures

| Failure | Description |
|---------|-------------|
| Overconfidence | Certainty exceeds evidence |
| Confirmation bias | Only seeing supporting evidence |
| Anchoring | Stuck on first estimate |
| Availability bias | Overweighting memorable examples |

---

# PART VI: QUICK REFERENCE

## Reasoning Type Selection

| If the task is... | Use... |
|-------------------|--------|
| Derive certain conclusion from premises | Deductive |
| Generalize from observations | Inductive |
| Find best explanation | Abductive |
| Determine what causes what | Causal |
| Transfer properties by similarity | Analogical |
| Update beliefs with evidence | Probabilistic |

## Formula Reference

```
PROBABILITY:
P(A|B) = P(A∩B)/P(B)
P(A|B) = P(B|A)P(A)/P(B)        [Bayes]
P(B) = ΣP(B|Ai)P(Ai)           [Total probability]
E[X] = Σ xi×P(xi)              [Expected value]

LOGIC:
P → Q ≡ ¬P ∨ Q                 [Material implication]
¬(P ∧ Q) ≡ ¬P ∨ ¬Q             [De Morgan]
¬(P ∨ Q) ≡ ¬P ∧ ¬Q             [De Morgan]
P → Q ≡ ¬Q → ¬P                [Contraposition]
¬∀xP(x) ≡ ∃x¬P(x)              [Quantifier negation]
¬∃xP(x) ≡ ∀x¬P(x)              [Quantifier negation]
```

## Valid Forms Quick Check

```
✓ If P then Q, P ∴ Q           (Modus Ponens)
✓ If P then Q, ¬Q ∴ ¬P         (Modus Tollens)
✓ P or Q, ¬P ∴ Q               (Disjunctive Syllogism)

✗ If P then Q, Q ∴ P           (Affirming Consequent)
✗ If P then Q, ¬P ∴ ¬Q         (Denying Antecedent)
```

---

*Reference layer. For training protocol, see LOGIC_MASTERY.md*
