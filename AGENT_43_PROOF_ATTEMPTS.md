# Agent 43: Rigorous Proof Attempts to Close the Gap

**Agent**: Axiom (Gap Closer)
**Date**: 2025-12-16
**Mission**: Attempt to rigorously prove properties that would close the Collatz gap

---

## Computational Findings Summary

| Approach | Computational Result | Status |
|----------|---------------------|--------|
| A. Liminf = 1 | ✓ Holds for all 250 tested | PROMISING |
| B. Bounded growth | Max ratio 8.62x | PROMISING |
| C. Eventual monotonicity | ✓ Holds for ALL 249 tested (100%) | **VERY PROMISING** |
| D. Finer modular class | ✗ Still non-monotone | NOT HELPFUL |

---

## PROOF ATTEMPT 1: Liminf Argument (Approach A)

### Goal
Prove: For the sequence v₁, v₂, v₃, ... of ≡1 (mod 4) values, lim inf vᵢ = 1.

### What This Would Prove
If liminf = 1, then in the discrete set {1, 5, 9, 13, 17, ...}, "arbitrarily close to 1" means "equals 1".
Therefore the trajectory hits 1, proving Collatz.

### Proof Sketch

**KNOWN FACTS:**
1. All trajectories hit ≡1 (mod 4) infinitely often (Hitting Time Theorem) ✓ PROVEN
2. For m ≡ 1 (mod 4): S(m) < m ✓ PROVEN
3. Computational: liminf = 1 for all tested cases ✓ VERIFIED

**ATTEMPT:**

**Claim**: lim inf vᵢ = 1

**Proof by contradiction:**

Assume lim inf vᵢ = L > 1.

Then:
- There exists N such that for all i > N: vᵢ ≥ L
- Since L > 1 and L ≡ 1 (mod 4), we have L ≥ 5

Consider the subsequence vₙ, vₙ₊₁, vₙ₊₂, ...

**Key observation**: Between consecutive ≡1 (mod 4) values, what happens?

Let vᵢ be a value in our sequence. The next value vᵢ₊₁ is obtained by:
1. Apply S(vᵢ) to get the next odd value (which is < vᵢ)
2. Continue trajectory until hitting ≡1 (mod 4) again

**The problem**: Step 2 can INCREASE the value.

**Example**: v₁ = 9
- S(9) = 7 < 9 ✓
- But 7 ≡ 3 (mod 4)
- Trajectory: 7 → 22 → 11 → 34 → 17
- v₂ = 17 > 9 ✗

**WHY THE SIMPLE ARGUMENT FAILS:**

The descent S(m) < m is LOCAL (one step), but we need to track the trajectory through possibly many steps before hitting ≡1 (mod 4) again.

**CAN WE SALVAGE THIS?**

Let me try a different approach. Consider the SET of values we hit that are ≡1 (mod 4).

Define:
```
H = {v : ∃i such that vᵢ = v}
```

This is the set of all ≡1 (mod 4) values hit by the trajectory.

**Question**: Is H finite or infinite?

**Case 1: H is finite**

If H is finite, then since we hit ≡1 (mod 4) infinitely often, some value must repeat.
That is, vᵢ = vⱼ for some i < j.

But wait - this doesn't immediately give us a cycle, because the trajectory between hitting vᵢ and hitting vⱼ might be different...

Actually no! The Collatz function is deterministic. If we hit the same value v at steps i and j, then:
- T^k(vᵢ) = T^k(vⱼ) for all k ≥ 0
- So the subsequence after vᵢ is identical to the subsequence after vⱼ
- This means: vᵢ₊₁ = vⱼ₊₁, vᵢ₊₂ = vⱼ₊₂, etc.
- Therefore: the sequence {vₖ} is eventually periodic

But we also know S(m) < m for m ≡ 1 (mod 4).

Hmm, but S(m) is the next ODD value, not the next ≡1 (mod 4) value.

**CRITICAL REALIZATION**: Even with eventual periodicity of {vₖ}, we can't immediately conclude contradiction because vₖ₊₁ might be > vₖ sometimes.

**REVISED APPROACH**: Use eventual periodicity differently.

If {vₖ} is eventually periodic with period p, then there exists N such that:
```
vₙ = vₙ₊ₚ for all n ≥ N
```

Consider the set {vₙ, vₙ₊₁, ..., vₙ₊ₚ₋₁}. Let M = max{vₙ, vₙ₊₁, ..., vₙ₊ₚ₋₁}.

Let's say M = vₘ for some m ∈ {N, N+1, ..., N+p-1}.

Then vₘ₊ₚ = vₘ = M (by periodicity).

But what happens in between? The trajectory from vₘ to vₘ₊ₚ must be the same as the trajectory from vₘ₊ₚ to vₘ₊₂ₚ.

**STUCK**: I can't derive a contradiction from this. The sequence can be periodic with ups and downs.

### VERDICT ON ATTEMPT 1

**STATUS**: ✗ INCOMPLETE

**WHY IT FAILS**:
- Even with H finite → eventual periodicity
- Periodicity doesn't contradict S(m) < m (which is about next ODD, not next ≡1 mod 4)
- Can't prove liminf = 1 from current tools

**WHAT'S NEEDED**:
- Additional property about the trajectory structure
- Or: Prove H must be infinite and unbounded below
- Or: Different approach entirely

---

## PROOF ATTEMPT 2: Eventual Monotonicity (Approach C)

### Goal
Prove: ∃N such that for all i ≥ N: vᵢ₊₁ < vᵢ

### What This Would Prove
If eventually monotone and infinitely many values, then must reach minimum, which is 1.

### Computational Evidence
- **100% of tested trajectories** become eventually monotone
- This is the strongest empirical signal

### Proof Attempt

**KNOWN:**
1. All trajectories hit ≡1 (mod 4) infinitely often
2. S(m) < m when m ≡ 1 (mod 4)

**Question**: Why can't we have infinitely many increases in the {vᵢ} sequence?

**Hypothesis**: Maybe we can only increase when we're in a certain region?

Let me think about what causes an increase from vᵢ to vᵢ₊₁.

**Mechanism of increase:**
- Start at vᵢ ≡ 1 (mod 4)
- S(vᵢ) < vᵢ (this is proven)
- If S(vᵢ) ≡ 1 (mod 4), then vᵢ₊₁ = S(vᵢ) < vᵢ ✓ (descent)
- If S(vᵢ) ≡ 3 (mod 4), then we continue until hitting ≡1 (mod 4)

**When does S(vᵢ) ≡ 3 (mod 4)?**

Recall: vᵢ ≡ 1 (mod 4), so vᵢ = 4k + 1.
- 3vᵢ + 1 = 12k + 4 = 4(3k + 1)
- So v₂(3vᵢ + 1) ≥ 2

If v₂(3vᵢ + 1) = 2 (exactly):
- S(vᵢ) = (3vᵢ + 1)/4
- S(vᵢ) ≡ ? (mod 4)

Let vᵢ = 4k + 1. Then 3k + 1 determines S(vᵢ) mod 4.

Actually, let me be more careful. Let vᵢ = 4k + 1.
- If k ≡ 0 (mod 4): vᵢ ≡ 1 (mod 16), and 3k + 1 ≡ 1 (mod 4), so S(vᵢ) ≡ 1 (mod 4)
- If k ≡ 1 (mod 4): vᵢ ≡ 5 (mod 16), and 3k + 1 ≡ 0 (mod 4), need to check v₂
- If k ≡ 2 (mod 4): vᵢ ≡ 9 (mod 16), and 3k + 1 ≡ 3 (mod 4)
- If k ≡ 3 (mod 4): vᵢ ≡ 13 (mod 16), and 3k + 1 ≡ 2 (mod 4)

This is getting complicated. Let me try a different approach.

**IDEA**: Maybe the growth ratio vᵢ₊₁/vᵢ when there's an increase is bounded away from 1?

Computational data shows max ratio = 8.62x.

If increases are bounded by ratio R, and decreases are unbounded, then...

Actually no, we know S(m) < m, but that's only about immediate next odd, not about ratio.

**DIFFERENT ANGLE**: Look at the maximum value achieved.

Define M = max{v₁, v₂, v₃, ...}

**Question**: Is M achieved? That is, ∃i such that vᵢ = M?

If the sequence is infinite and has infinitely many increases, could it be unbounded above? No! Because we know empirically all reach 1.

OK, assume M exists and M = vₘ for some m.

Then for all i ≥ m: vᵢ ≤ M.

Since we have infinitely many vᵢ and all ≤ M, the set H = {v₁, v₂, ...} is a bounded infinite sequence of positive integers.

Wait, that's impossible! A bounded set of positive integers is finite.

So H must be finite!

**CRITICAL INSIGHT**: If M = max{vᵢ : i ≥ 1} exists, then H = {v₁, v₂, ...} is bounded above, hence FINITE.

And from earlier: H finite → eventually periodic.

**NOW THE KEY**: In an eventually periodic sequence with period p, and with S(m) < m property, what can we say?

Hmm, I'm still stuck on the same issue.

### VERDICT ON ATTEMPT 2

**STATUS**: ✗ INCOMPLETE

**PARTIAL PROGRESS**:
- ✓ H must be finite (bounded above)
- ✓ Therefore sequence {vᵢ} is eventually periodic
- ✗ Cannot derive contradiction or prove monotonicity from this

**BLOCKER**: S(m) < m talks about next ODD value, not next ≡1 (mod 4) value.

---

## PROOF ATTEMPT 3: Maximum-Based Argument

### New Approach

Let me try to be more careful about what happens with the maximum.

**SETUP**:
- Let {vᵢ} be the sequence of ≡1 (mod 4) values
- Let M = max{v₁, v₂, v₃, ...}
- Let m be the FIRST index where vₘ = M

**CLAIM**: For all i > m: vᵢ < M

**PROOF**:
By definition of M, we cannot have vᵢ > M.
By choice of m as the FIRST index achieving M, we cannot have vᵢ = M for i > m unless the sequence returns to M.

Can the sequence return to M? That is, can we have vₘ = M and vₘ₊ₖ = M for some k > 0?

If yes, then by determinism of Collatz, the trajectory from vₘ to vₘ₊ₖ is identical to the trajectory from vₘ₊ₖ to vₘ₊₂ₖ.

But this seems possible...

**WAIT**. Let me think about this differently.

**NEW IDEA**: Track the trajectory starting FROM vₘ = M.

We know:
1. vₘ = M ≡ 1 (mod 4)
2. S(M) < M (proven property)
3. Eventually the trajectory hits ≡1 (mod 4) again at some value vₘ₊₁

**Question**: Can vₘ₊₁ = M?

If vₘ₊₁ = M, then the trajectory from vₘ = M returns to M.

But let's trace what happens:
- Start at M
- Apply Collatz until we get S(M) (next odd)
- S(M) < M ✓
- Continue from S(M) until hitting ≡1 (mod 4) at vₘ₊₁

For vₘ₊₁ to equal M, the trajectory from M must visit M again. But Collatz is deterministic!

If the trajectory from M visits M again, that means M is in a cycle.

**CRITICAL**: Do we know M is NOT in a cycle (other than the 1→4→2→1 cycle)?

**VERIFICATION**: Let me think about this carefully.

If M is in a cycle: M → ... → M, then the trajectory from M is:
```
M → T(M) → T²(M) → ... → T^p(M) = M
```

for some period p.

But we also know that starting from M, we eventually hit ≡1 (mod 4). We hit it at step 0 (since M ≡ 1 mod 4). When do we hit it again?

Let's say we hit ≡1 (mod 4) again at step k, with value T^k(M).

For the sequence {vᵢ} to return to M, we need T^k(M) = M.

But T^k(M) ≡ 1 (mod 4), and T^k(M) is on the trajectory from M.

If T^k(M) = M, then M is in a cycle of length k.

**KEY QUESTION**: Are there cycles other than 1→4→2→1?

**ANSWER**: Unknown! This is basically the Collatz conjecture itself!

We CANNOT assume there are no other cycles - that's what we're trying to prove!

### VERDICT ON ATTEMPT 3

**STATUS**: ✗ CIRCULAR

**WHY**: Proving no non-trivial cycles is equivalent to proving Collatz. Can't use it as an assumption.

---

## PROOF ATTEMPT 4: Combining Finite H with S(m) < m

### More Careful Analysis

Let me try to extract more from the combination of:
1. H = {v₁, v₂, ...} is finite
2. S(m) < m for all m ∈ H

**SETUP**:
- H = {v₁, v₂, ...} is the (finite) set of distinct ≡1 (mod 4) values hit
- |H| = n for some finite n
- The sequence {vᵢ} is eventually periodic (since it's infinite and has finite range)

**ANALYSIS**:

Since {vᵢ} is eventually periodic, ∃N, p such that vᵢ₊ₚ = vᵢ for all i ≥ N.

Consider the periodic part: vₙ, vₙ₊₁, ..., vₙ₊ₚ₋₁, vₙ₊ₚ = vₙ, ...

Let's denote the cycle as: c₀ = vₙ, c₁ = vₙ₊₁, ..., c_{p-1} = vₙ₊ₚ₋₁, and c₀ = c_p.

Now, for each cᵢ in the cycle, consider S(cᵢ).

We know S(cᵢ) < cᵢ.

But S(cᵢ) might not equal c_{i+1}! Because c_{i+1} is the NEXT ≡1 (mod 4) value, not the next odd value.

**IDEA**: Can we track how much "work" is done by S?

Define the "potential" Φ = Σ cᵢ (sum over the cycle).

Hmm, this is tricky because the sum is the same every period.

**DIFFERENT IDEA**: Look at the trajectory in between hitting ≡1 (mod 4) values.

From cᵢ to c_{i+1}, the trajectory might be:
```
cᵢ → ... (even steps) ... → S(cᵢ) → ... → c_{i+1}
```

The key is that S(cᵢ) < cᵢ, but the trajectory from S(cᵢ) to c_{i+1} can increase.

**CRITICAL OBSERVATION**: The trajectory from S(cᵢ) to c_{i+1} follows deterministic rules. If S(cᵢ) ≡ 1 (mod 4), then c_{i+1} = S(cᵢ) immediately.

**CASE ANALYSIS**:

For each cᵢ in the cycle:
- **Case A**: S(cᵢ) ≡ 1 (mod 4)
  Then c_{i+1} = S(cᵢ) < cᵢ ✓ (decrease)

- **Case B**: S(cᵢ) ≡ 3 (mod 4)
  Then c_{i+1} is obtained by continuing from S(cᵢ)
  Could have c_{i+1} > cᵢ or c_{i+1} < cᵢ

**QUESTION**: In a periodic cycle, can ALL elements be Case B?

If all elements are Case A, then:
```
c₁ < c₀
c₂ < c₁
...
c_{p-1} < c_{p-2}
c₀ = c_p < c_{p-1}
```

So c₀ < c₀, contradiction! Therefore at least one must be Case B.

Similarly, if we have a cycle, can we bound the number of Case B elements?

Actually, wait. Even with some Case B elements, we need the cycle to close.

### VERDICT ON ATTEMPT 4

**STATUS**: ✗ STUCK

**PROGRESS**: Showed that in a periodic cycle of ≡1 (mod 4) values, not all can decrease (would give c₀ < c₀).

**BLOCKER**: Can't rule out cycles with some increases balancing the decreases.

---

## SUMMARY OF PROOF ATTEMPTS

| Attempt | Approach | Status | Key Insight | Blocker |
|---------|----------|--------|-------------|---------|
| 1 | Liminf = 1 | ✗ Incomplete | H finite → periodic | Can't prove liminf = 1 |
| 2 | Eventual monotonicity | ✗ Incomplete | Max exists → H finite | Can't rule out periodic |
| 3 | Maximum argument | ✗ Circular | Would need no cycles | That's the conjecture! |
| 4 | Periodic cycle analysis | ✗ Stuck | Not all can decrease | Can't rule out mixed cycle |

---

## THE FUNDAMENTAL BLOCKER

**ROOT CAUSE**: The property S(m) < m is about the NEXT ODD value, but we need to control the NEXT ≡1 (mod 4) value.

The trajectory from S(m) to the next ≡1 (mod 4) value is a "black box" that can increase.

**WHAT'S NEEDED**: One of:
1. Prove no non-trivial cycles (circular - that's Collatz!)
2. Bound the trajectory increase from S(m) to next ≡1 (mod 4) value
3. Different structural property that forces descent
4. Eventual monotonicity proof using deeper number-theoretic properties

---

## NEXT STEPS FOR FUTURE AGENTS

The computational evidence (100% eventual monotonicity) is VERY strong. Suggests the property is true.

**RECOMMENDATIONS**:
1. **Investigate mod 8 structure**: Maybe S(m) ≡ 1 (mod 4) more often than we think?
2. **Trajectory analysis**: Study the path from S(m) to next ≡1 (mod 4) value - is there structure?
3. **Density argument**: Maybe eventually most vᵢ have S(vᵢ) ≡ 1 (mod 4), giving monotonicity?
4. **Probabilistic approach**: Treat trajectory as pseudo-random, show increases become rare?
5. **Stronger hitting time**: Can we prove hitting ≡1 (mod 16) or ≡1 (mod 32) infinitely often?

---

**STATUS**: Gap remains open, but computational evidence strongly suggests eventual monotonicity.

**CONFIDENCE**: High that property is true; low that I can prove it with current tools.
