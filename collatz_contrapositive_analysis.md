# Collatz Conjecture: Contrapositive Proof Attempt

## Problem Statement

**Collatz Conjecture**: For any positive integer n, the sequence defined by:
- f(n) = n/2 if n is even
- f(n) = 3n+1 if n is odd

eventually reaches 1.

**Contrapositive Approach**: Prove that neither of these can exist:
- A) A number with a divergent trajectory (goes to infinity)
- B) A number that enters a cycle other than 1→4→2→1

---

## Part A: No Divergent Trajectories

### Assumption
Assume ∃ n₀ such that the trajectory {n₀, n₁, n₂, ...} diverges to infinity.

### Properties of Divergent Sequences

For the sequence to diverge, we need:
```
lim(n→∞) nₙ = ∞
```

### Growth vs Shrinkage Analysis

**Operations:**
- Odd n: n ↦ 3n+1 (growth by factor ≈3)
- Even n: n ↦ n/2 (shrinkage by factor 2)

**Key Observation 1:** After any odd number n, we get 3n+1, which is even.

*Proof:* If n is odd, n = 2k+1 for some integer k.
Then 3n+1 = 3(2k+1)+1 = 6k+3+1 = 6k+4 = 2(3k+2), which is even. □

**Consequence:** After every application of the 3n+1 rule, we MUST apply the n/2 rule at least once.

### Trajectory Structure

The trajectory has the form:
```
odd₁ → even → even → ... → even → odd₂ → even → ... → odd₃ → ...
```

Let's denote:
- For the i-th odd number oᵢ in the trajectory, let hᵢ = number of consecutive halvings before the next odd number

So from oᵢ to oᵢ₊₁:
```
oᵢ₊₁ = (3oᵢ + 1) / 2^(hᵢ)
```

where hᵢ ≥ 1.

### Growth Condition for Divergence

For divergence, we need the sequence of odd numbers {o₁, o₂, o₃, ...} to grow unboundedly.

From oᵢ to oᵢ₊₁:
```
oᵢ₊₁ = (3oᵢ + 1) / 2^(hᵢ)
```

For growth: oᵢ₊₁ > oᵢ
```
(3oᵢ + 1) / 2^(hᵢ) > oᵢ
3oᵢ + 1 > oᵢ · 2^(hᵢ)
3oᵢ + 1 > oᵢ · 2^(hᵢ)
1 > oᵢ(2^(hᵢ) - 3)
```

If hᵢ = 1: 2^(hᵢ) - 3 = 2 - 3 = -1, so 1 > -oᵢ (always true)
If hᵢ = 2: 2^(hᵢ) - 3 = 4 - 3 = 1, so 1 > oᵢ (only true for oᵢ = 0, impossible)
If hᵢ ≥ 2: 2^(hᵢ) ≥ 4 > 3, so oᵢ(2^(hᵢ) - 3) > 0, and 1 > oᵢ(2^(hᵢ) - 3) requires oᵢ < 1/(2^(hᵢ) - 3)

**Critical observation:** For oᵢ₊₁ > oᵢ, we need hᵢ = 1.

But wait, let me recalculate. If hᵢ = 1:
```
oᵢ₊₁ = (3oᵢ + 1) / 2
```
For oᵢ₊₁ > oᵢ:
```
(3oᵢ + 1) / 2 > oᵢ
3oᵢ + 1 > 2oᵢ
oᵢ + 1 > 0
```
This is always true! So with hᵢ = 1, we always get growth.

### The Key Question: What determines hᵢ?

After computing 3oᵢ + 1, we get some even number. How many times is it divisible by 2?

Let 3oᵢ + 1 = 2^(hᵢ) · m where m is odd. Then hᵢ is the 2-adic valuation of 3oᵢ + 1.

**Question:** For a divergent trajectory, what must be true about the average value of hᵢ?

### Average Growth Rate Analysis

Over N steps (odd numbers), the ratio is:
```
oₙ / o₁ = ∏ᵢ₌₁ᴺ⁻¹ (3oᵢ + 1)/(oᵢ · 2^(hᵢ))
      ≈ ∏ᵢ₌₁ᴺ⁻¹ 3/2^(hᵢ)   [for large oᵢ]
      = 3^(N-1) / 2^(h₁+h₂+...+hₙ₋₁)
```

For divergence: oₙ / o₁ → ∞ as N → ∞

This requires:
```
3^(N-1) / 2^(H) → ∞  where H = Σhᵢ

Taking logs:
(N-1)log(3) - H·log(2) → ∞
(N-1)log(3) > H·log(2)
H/N < log(3)/log(2) ≈ 1.585
```

**So for divergence, the average number of halvings per odd number must be < 1.585**

### Distribution of hᵢ values

What is hᵢ? It's the number of times 2 divides (3oᵢ + 1).

For odd oᵢ, what's the probability distribution of h where 2^h | (3o + 1)?

This depends on oᵢ mod 2^k for various k.

**Analysis:**
- If oᵢ ≡ 1 (mod 4), then 3oᵢ ≡ 3 (mod 4), so 3oᵢ+1 ≡ 0 (mod 4), thus hᵢ ≥ 2
- If oᵢ ≡ 3 (mod 4), then 3oᵢ ≡ 1 (mod 4), so 3oᵢ+1 ≡ 2 (mod 4), thus hᵢ = 1

So roughly:
- Half of odd numbers have hᵢ ≥ 2
- Half have hᵢ = 1

**But this is heuristic, not rigorous.** The actual distribution depends on the trajectory structure.

### The Gap in the Proof

To prove no divergence rigorously, we would need to show:
1. For ANY sequence of odd numbers following Collatz rules, the average hᵢ must exceed log(3)/log(2)
2. OR show that sequences with low average hᵢ cannot be sustained

**Current status:** Heuristic arguments suggest average hᵢ ≈ 2, which would give shrinkage, but a RIGOROUS proof that this must be true for all trajectories is not established here.

---

## Part B: No Other Cycles

### Cycle Structure

Assume a cycle exists: n₁ → n₂ → ... → nₖ → n₁

The cycle contains both odd and even numbers. Let's track just the odd numbers in the cycle:
```
o₁ → [even numbers] → o₂ → [even numbers] → ... → oₐ → [even numbers] → o₁
```

where a is the number of distinct odd numbers in the cycle.

### Algebraic Conditions

From odd number oᵢ to the next odd number oᵢ₊₁:
```
oᵢ₊₁ = (3oᵢ + 1) / 2^(hᵢ)
```

For a cycle, after going through all a odd numbers, we return:
```
o₁ = (3oₐ + 1) / 2^(hₐ)
o₂ = (3o₁ + 1) / 2^(h₁)
...
oₐ = (3oₐ₋₁ + 1) / 2^(hₐ₋₁)
```

Substituting successively to express o₁ in terms of itself:

Starting from o₁, after one complete cycle:
```
o₂ = (3o₁ + 1) / 2^(h₁)
o₃ = (3o₂ + 1) / 2^(h₂) = (3(3o₁ + 1)/2^(h₁) + 1) / 2^(h₂)
   = (3²o₁ + 3 + 2^(h₁)) / 2^(h₁+h₂)
```

This gets complex. Let me use a different approach.

### Multiplicative Approach

Multiply all cycle equations:
```
o₁·o₂·...·oₐ = [(3o₁+1)·(3o₂+1)·...·(3oₐ+1)] / [2^(h₁)·2^(h₂)·...·2^(hₐ)]
```

Let H = h₁ + h₂ + ... + hₐ (total halvings in cycle)

```
o₁·o₂·...·oₐ · 2^H = (3o₁+1)·(3o₂+1)·...·(3oₐ+1)
```

Expanding the right side:
```
(3o₁+1)·(3o₂+1)·...·(3oₐ+1) = 3^a·o₁·o₂·...·oₐ + [terms with fewer o's] + 1
```

So:
```
o₁·o₂·...·oₐ · 2^H = 3^a·o₁·o₂·...·oₐ + [positive terms]

o₁·o₂·...·oₐ · (2^H - 3^a) = [positive terms] > 0
```

For this to have a solution with positive oᵢ:
```
2^H - 3^a > 0
2^H > 3^a
H > a · log(3)/log(2)
H > 1.585·a
```

**So any cycle must have more than 1.585 halvings per odd number on average.**

### Checking the Known Cycle: 1→4→2→1

- Odd numbers: just o₁ = 1, so a = 1
- From 1: 3(1)+1 = 4 → 4/2 = 2 → 2/2 = 1
- Halvings: h₁ = 2

Check: H = 2, a = 1
```
2^2 = 4 > 3^1 = 3 ✓
```

And 2 > 1.585·1 ✓

### Can Other Cycles Exist?

The condition 2^H > 3^a is necessary but not sufficient.

Let me try to find small cycles systematically.

**For a = 1 (single odd number):**
```
o₁ = (3o₁ + 1) / 2^h
o₁ · 2^h = 3o₁ + 1
o₁(2^h - 3) = 1
o₁ = 1/(2^h - 3)
```

For integer o₁ > 0:
- h = 2: o₁ = 1/(4-3) = 1 ✓ (This is the known cycle!)
- h = 3: o₁ = 1/(8-3) = 1/5 ✗
- h ≥ 3: o₁ < 1 ✗

**So the only 1-odd-number cycle is o₁ = 1, h = 2.**

**For a = 2 (two odd numbers):**
```
o₂ = (3o₁ + 1) / 2^(h₁)
o₁ = (3o₂ + 1) / 2^(h₂)
```

Substituting the first into the second:
```
o₁ = (3(3o₁ + 1)/2^(h₁) + 1) / 2^(h₂)
o₁ = [(3²o₁ + 3 + 2^(h₁))] / 2^(h₁+h₂)
o₁ · 2^(h₁+h₂) = 9o₁ + 3 + 2^(h₁)
o₁(2^(h₁+h₂) - 9) = 3 + 2^(h₁)
o₁ = (3 + 2^(h₁)) / (2^(h₁+h₂) - 9)
```

For this to give integer o₁ > 0:
- We need 2^(h₁+h₂) > 9, so h₁+h₂ ≥ 4
- We need (3 + 2^(h₁)) divisible by (2^(h₁+h₂) - 9)

Let's try h₁ = h₂ = 2 (so H = 4):
```
o₁ = (3 + 4) / (16 - 9) = 7/7 = 1
```

So o₁ = 1. Then:
```
o₂ = (3·1 + 1) / 4 = 4/4 = 1
```

This gives o₁ = o₂ = 1, which is the same as the 1-cycle, not a new 2-cycle.

Let me try h₁ = 1, h₂ = 3 (so H = 4):
```
o₁ = (3 + 2) / (16 - 9) = 5/7
```
Not an integer.

Let me try h₁ = 2, h₂ = 3 (so H = 5):
```
o₁ = (3 + 4) / (32 - 9) = 7/23
```
Not an integer.

**The search space is infinite, and I cannot exhaustively prove no other cycles exist this way.**

### What's Been Proven Computationally

- No cycles other than 1-4-2-1 exist for starting values up to 2^68 ≈ 3×10²⁰
- No divergent trajectories found up to similar bounds

But computational verification ≠ proof.

### The Gap in Part B

To complete this proof, we would need to show that the system of equations:
```
oᵢ₊₁ = (3oᵢ + 1) / 2^(hᵢ)  for i = 1,...,a (with oₐ₊₁ = o₁)
```

has no solutions in positive integers except the known cycle, for ANY choice of a and {h₁,...,hₐ}.

This is a Diophantine equation problem that has not been solved in general.

---

## Conclusion

### What We've Shown:

**Part A (No Divergence):**
- For divergence, average halvings per odd number must be < 1.585
- Heuristically, we expect ≈ 2 halvings on average
- **Gap:** No rigorous proof that all trajectories must have high enough average hᵢ

**Part B (No Other Cycles):**
- Any cycle must satisfy 2^H > 3^a
- The only single-odd-number cycle is 1→4→2→1
- **Gap:** Cannot exhaustively rule out multi-odd-number cycles via this approach

### Why This Isn't a Complete Proof:

1. The growth rate analysis in Part A is heuristic, not rigorous
2. The cycle analysis in Part B cannot exhaustively cover infinite cases
3. Both approaches have been explored extensively in the literature without resolution

### What Would Be Needed:

- **For Part A:** A rigorous bound on the 2-adic valuation of (3n+1) that holds for all trajectories
- **For Part B:** A number-theoretic result about the system of Diophantine equations, possibly using algebraic number theory or modular arithmetic constraints

This is why the Collatz Conjecture remains open despite its simple statement.
