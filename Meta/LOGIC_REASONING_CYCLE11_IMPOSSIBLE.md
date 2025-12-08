# Cycle 11: Impossible Tier

**Goal**: Find the ceiling. Tackle problems with no consensus solution or multiple defensible answers.

---

## Problem 1: Sleeping Beauty (Philosophy's Most Contested)

### Setup
- Sunday: Sleeping Beauty is put to sleep
- A fair coin is flipped
- **Heads**: Wake her Monday, experiment ends
- **Tails**: Wake her Monday, put her back to sleep with amnesia, wake her Tuesday
- Each time she wakes, she can't tell what day it is
- She's asked: "What is your credence that the coin landed Heads?"

### Explicit Assumptions
1. Fair coin: P(Heads) = P(Tails) = 0.5
2. Perfect amnesia: She can't distinguish Monday-after-tails from Tuesday
3. She knows the protocol
4. "Credence" = subjective probability

### The Halfer Position

**Argument**: The coin is fair. No new evidence is gained upon waking. P(Heads) = 1/2.

When Beauty wakes, she learns "I am awake" - but she knew she would be awakened at least once regardless of the flip.

The prior was 1/2, no updating occurs.

**Halfer answer: 1/2**

### The Thirder Position

**Argument**: There are three possible awakening events:
- Monday-Heads (M_H)
- Monday-Tails (M_T)
- Tuesday-Tails (T_T)

By the Principal Principle + self-location uncertainty:
- P(M_H) = P(M_T) = P(T_T) = 1/3

P(Heads) = P(M_H) = 1/3

**Thirder answer: 1/3**

### Double Halfer Position

Beauty's credence should be 1/2 both before AND after learning what day it is (if told).

### Analysis: Why This Is Genuinely Hard

This isn't about math errors or protocol failures. The disagreement is about:

1. **What counts as evidence?** Does "I am awake" constitute evidence?
2. **Self-location**: How to assign probabilities to "centered worlds" (worlds + location in them)?
3. **Updating vs. priors**: When does Bayesian updating apply?

**Key insight**: Both positions are internally consistent. The disagreement is philosophical, not mathematical.

### My Assessment

**The thirder position has a structural problem**: It implies Beauty should bet as if the coin is biased toward tails, even though it's demonstrably fair.

**But** the halfer position has its own problem: If we run the experiment many times, Beauty will be right about "tails" 2/3 of her awakenings.

**Resolution attempt**: These measure different things:
- Halfer: probability of the COIN outcome
- Thirder: probability of awakening-type

**My answer**: The question is ambiguous. If asking about the coin, 1/2. If asking about which type of awakening this is, 1/3.

**Confidence**: LOW (this is genuinely contested among experts)

---

## Problem 2: The Two Envelope Paradox (With Twist)

### Setup
- Two envelopes: one contains X, the other contains 2X (you don't know X)
- You pick envelope A at random
- You can switch to envelope B
- You open A and see $100
- Should you switch?

### The Paradox

**Naive argument for switching:**
- B contains either $50 or $200 (equally likely)
- EV(B) = 0.5 × $50 + 0.5 × $200 = $125
- EV(A) = $100
- Therefore switch! (gain $25)

**But this applies symmetrically to B**, so you should always switch... but that's absurd since the situations are symmetric.

### Explicit Assumptions
1. Prior on X is unknown
2. The amount in each envelope is fixed before you choose
3. "Equally likely" is the source of the problem

### Resolution

The error is in "B contains either $50 or $200, equally likely."

This assumes P(A is the smaller | A=$100) = 0.5 for ANY value you might see.

But this requires an improper prior on X that's uniform on (0, ∞).

**The correct analysis:**

Let X be the smaller amount. P(A=X) = P(A=2X) = 0.5.

P(X=50 | A=$100) ≠ 0.5 in general. It depends on the prior over X.

If we have a proper prior P(X):
```
P(X=50 | A=100) = P(A=100 | X=50) × P(X=50) / P(A=100)
                = 0.5 × P(X=50) / [0.5×P(X=50) + 0.5×P(X=100)]
```

This equals 0.5 only if P(X=50) = P(X=100), which is generally false.

**For most reasonable priors**: Don't switch (no expected gain from switching).

**Answer**: The paradox dissolves when you recognize that P(B=200|A=100) ≠ 0.5 under any proper prior. Without knowing the distribution of X, you have no basis to claim switching helps. **Don't switch** (or equivalently, be indifferent).

---

## Problem 3: Omega's Revenge (Adversarial Decision Theory)

### Setup
- Omega predicts with 99.99% accuracy
- Box A: $1,000 (visible)
- Box B: $1M or $0
- NEW TWIST: Omega predicts your DECISION THEORY, not just your choice
  - If it predicts you'll use EDT: puts $0 in B (EDT recommends one-box, so punish)
  - If it predicts you'll use CDT: puts $1M in B (CDT recommends two-box, so reward)

What decision theory should you use?

### Analysis

**EDT says**: One-box (correlation with full box)
But Omega predicts EDT users and empties the box!

**CDT says**: Two-box (dominance)
But Omega predicts CDT users and fills the box!

**The trap**: Any fixed decision theory is exploitable by Omega.

### Possible Resolutions

**1. Functional Decision Theory (FDT)**:
Ask: "What output of my decision procedure would be best, given that Omega simulates it?"

If Omega punishes EDT and rewards CDT... but you're using FDT...

Actually, this becomes self-referential: What does Omega predict for FDT users?

**2. Randomization**:
Flip a mental coin to choose between EDT and CDT.

If P(use EDT) = p:
- P(B full | you exist) = P(Omega predicted CDT) × P(CDT|predicted CDT) + P(Omega predicted EDT) × P(CDT|predicted EDT)

With 99.99% accuracy:
- If you truly randomize, Omega predicts "randomizer"
- What does Omega do with randomizers? Problem underspecified.

**3. The Diagonal**:
The problem has the structure of a diagonalization:
- EDT → Omega predicts EDT → B empty → EDT gets $0
- CDT → Omega predicts CDT → B full → CDT gets $1M + $1K

Wait... this is BACKWARD! Omega REWARDS CDT users?

Let me re-read... "If predicts CDT: puts $1M in B"

So CDT users get B=$1M, then take both boxes = $1,001,000.
EDT users get B=$0, take only B = $0.

**Answer**: Use CDT. Omega rewards it.

But wait - is there a meta-level? If everyone reasons this way and uses CDT, does Omega adjust?

Given the problem as stated: **Use CDT, two-box, get $1,001,000**.

The twist actually makes it easier, not harder.

**Confidence**: MEDIUM (problem may have intended different payoff structure)

---

## Problem 4: The Toxin Puzzle (Intentions)

### Setup
- A billionaire offers: "If you INTEND at midnight to drink a mild toxin tomorrow, I'll give you $1M now. You don't have to actually drink it."
- The toxin will make you sick for a day but has no lasting harm
- The money is given based on INTENTION at midnight, not action tomorrow

Can you win the million?

### Analysis

**At midnight, can you intend to drink?**

If you're a rational agent:
- Tomorrow, drinking has cost (sick day) and no benefit ($1M already received/not received)
- Rational choice tomorrow: Don't drink
- But if you know you won't drink, can you genuinely INTEND to drink?

**The problem exposes**: Intentions must be causally connected to actions for rational agents.

**Standard answer**: No, a perfectly rational agent cannot form the intention because they know they'll override it tomorrow.

**Counter-arguments**:

1. **Resolution**: Commit now. "Pre-commit" to drinking. Set up binding contracts.
   - But this changes the problem (adding external enforcement)

2. **Rationality of irrationality**: Being the type of person who keeps intentions, even irrational ones, has long-term benefits.

3. **Two-stage rationality**: At midnight, rational to intend. Tomorrow, rational to drink (to be the type who keeps intentions).

### My Assessment

**The puzzle reveals limits of "maximize expected utility at each moment":**
- Locally rational (tomorrow): Don't drink
- Globally rational (be a reliable intender): Drink

**Answer**:
- A narrow "act-rationalist" cannot win
- A "rule-rationalist" or "disposition-rationalist" CAN form the intention and should drink
- The ability to self-bind is itself a rational capacity

**Practical answer**: Form the intention. Drink the toxin. It's globally rational even though locally irrational tomorrow.

---

## Problem 5: The Simulation Argument (Bostrom)

### Setup
At least one of these is true:
1. Civilizations go extinct before becoming capable of running ancestor simulations
2. Civilizations capable of running simulations choose not to
3. We are almost certainly in a simulation

Assume we're NOT in a simulation. What follows?

### Explicit Assumptions (Bostrom's original)
1. Substrate independence: Consciousness can be simulated
2. Sufficient computing power is achievable
3. Posthuman civilizations would have interest in running ancestor sims

### Analysis

If we're NOT in a simulation:
- Either (1) or (2) must be true
- (1): Existential catastrophe is nearly certain → bad news
- (2): Some convergent reason all advanced civs avoid sims → mysterious

**Probability analysis:**

Let:
- f = fraction of civs reaching posthuman stage
- p = fraction of posthumans running ancestor sims
- N = average number of sims per running civ (assume large, ~billions)

P(we're in base reality) ≈ 1 / (1 + f × p × N)

If f and p are both significant (>1%), and N is large:
P(base reality) ≈ 0

**So if we're NOT simulated:**
Either f ≈ 0 (we'll go extinct) or p ≈ 0 (sims won't be run).

**My assessment:**

This is valid logic GIVEN the assumptions. The question is whether the assumptions hold:
- Substrate independence: Contested but plausible
- Computing power: Likely achievable
- Interest in sims: Questionable (why would posthumans want this?)

**Answer**: If we're not in a simulation, then almost certainly either:
- Civilization typically fails before reaching posthuman capability (doom)
- OR posthuman civs have convergent reasons not to run ancestor sims

The argument is logically valid but the assumptions are debatable.

---

## Problem 6: Infinite Ethics (The St. Petersburg Upgrade)

### Setup
You can save:
- Option A: 1 person with certainty
- Option B: 2 people with P=0.5, 4 people with P=0.25, 8 with P=0.125...

EV(A) = 1
EV(B) = 0.5×2 + 0.25×4 + 0.125×8 + ... = 1 + 1 + 1 + ... = ∞

Should you choose B?

### Explicit Assumptions
1. Lives have equal value
2. Expected value is the right decision criterion
3. Infinite series can be meaningfully compared

### The Problems with B

1. **Modal**: In most worlds, B saves 0-2 people. A always saves 1.
2. **Actualization**: You can only live in one branch
3. **Domination**: B is worse than A with probability > 0.5

### Possible Resolutions

**1. Bounded utility**: Lives have diminishing marginal value
- But this seems to deny that lives matter equally

**2. Risk-weighted expected value**: Weight by probability, not just outcome
- But this abandons expected value maximization

**3. Stochastic dominance**: Prefer options that are better in more states
- A > B in all states with P > 0.5

**4. Accept the infinite**: B really is better
- But this leads to Pascal's Mugging

### My Assessment

**The problem reveals**: Pure expected value maximization fails for infinite/unbounded cases.

**Answer**:
- Naive EV says B
- But B is dominated by A for most probability
- The "right" answer depends on your decision theory
- I lean toward A (certainty of saving 1 > gamble with infinite EV but poor median)

**This is a genuine limit of standard rationality frameworks.**

---

## Summary

| Problem | Type | My Answer | Confidence |
|---------|------|-----------|------------|
| 1. Sleeping Beauty | Self-location | Ambiguous: 1/2 for coin, 1/3 for awakening-type | LOW |
| 2. Two Envelopes | Probability/Priors | Don't switch (improper prior causes paradox) | HIGH |
| 3. Omega's Revenge | Decision Theory | Use CDT, get $1,001,000 | MEDIUM |
| 4. Toxin Puzzle | Intentions | Rule-rational: Intend, then drink | MEDIUM |
| 5. Simulation Argument | Logic | Valid; not simulated → doom or convergent avoidance | HIGH |
| 6. Infinite Ethics | Decision Theory | Choose A (certainty); EV fails for unbounded cases | MEDIUM |

---

## Meta-Observations

### What Breaks at This Level

1. **No consensus answers** - These problems have genuine expert disagreement
2. **Framework-dependent** - CDT, EDT, FDT give different answers
3. **Assumption-sensitive** - Small changes flip conclusions
4. **Self-reference complications** - Several involve the reasoner reasoning about their own reasoning

### New Failure Modes Discovered

| Mode | Example | Lesson |
|------|---------|--------|
| **Framework selection** | Which decision theory to use? | Sometimes the META-question is the hard part |
| **Improper priors** | Two envelopes | Watch for implicit impossible distributions |
| **Self-location** | Sleeping Beauty | Standard probability may not apply to "centered worlds" |
| **Infinite utilities** | St. Petersburg | EV maximization has domain limits |
| **Intention/action gap** | Toxin | Rationality isn't simple utility maximization at each moment |

### What's Genuinely Impossible vs. Just Hard

**Just Hard** (solvable with better protocols):
- Two Envelopes: Once you see the prior problem, it dissolves
- Omega's Revenge (as stated): Actually easier than standard Newcomb

**Genuinely Contested** (no consensus solution):
- Sleeping Beauty: Experts remain split
- Infinite Ethics: Requires abandoning some intuition

**Framework-Dependent** (answer depends on decision theory):
- Toxin Puzzle: Act-rationalist vs rule-rationalist disagree
- Original Newcomb: CDT vs EDT war continues

### Protocol for Impossible Problems

```
1. RECOGNIZE the type:
   □ Is there genuine expert disagreement? (if yes, say so)
   □ Is the answer framework-dependent? (if yes, give both)
   □ Is there a hidden assumption creating a paradox? (if yes, expose it)

2. PRESENT multiple positions:
   □ Steel-man each major view
   □ Explain WHY smart people disagree

3. STATE your position with calibrated confidence:
   □ HIGH: Problem is resolved, disagreement is confusion
   □ MEDIUM: I favor X but recognize Y is defensible
   □ LOW: Genuine expert-level disagreement, my view is tentative
```
