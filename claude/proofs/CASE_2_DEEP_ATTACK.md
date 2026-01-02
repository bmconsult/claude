# Case 2: Deep Attack with Novel Frameworks

**Mission:** Find algebraic proof that Case 2 tuples (some v ≡ 0 mod n+1) always have lonely time.

**Key empirical fact:** 100% of 373,824 tested Case 2 tuples work, typically at small primes p < 50.

---

## Attack 6: Group Action on Residue Classes

**Inspiration:** Wilson's theorem proof used group actions. Can we find a group action that proves arc intersection?

### Setup

For prime p and speeds v₁, ..., vₙ, define:
```
Gᵢ = {k ∈ (Z/pZ)* : vᵢk mod p ∈ [⌈p/(n+1)⌉, p - ⌈p/(n+1)⌉]}
```

We need to prove |∩ᵢ Gᵢ| > 0.

**Group:** G = (Z/pZ)* acts on itself by multiplication.

**Action:** For g ∈ G and k ∈ G, define:
```
g · k = gk mod p
```

**Question:** How do the arcs Gᵢ transform under this action?

For k ∈ Gᵢ, we have vᵢk mod p ∈ [L, R].

Then g·k ∈ Gᵢ iff vᵢ(gk) mod p ∈ [L, R].

Let m = vᵢk mod p ∈ [L, R]. Then vᵢ(gk) = g·m mod p.

**So:** g·k ∈ Gᵢ iff g·m ∈ [L, R].

This means:
```
g·Gᵢ = {k' : vᵢk' mod p = g·(vᵢk₀ mod p) for some k₀ ∈ Gᵢ}
```

The set Gᵢ is NOT INVARIANT under multiplication in general.

### Different action: Translation

**Action:** G acts on itself by translation: g · k = g + k mod p.

For k ∈ Gᵢ, we have vᵢk ∈ [L, R].

Then vᵢ(g+k) = vᵢg + vᵢk mod p.

**So:** g + Gᵢ shifts the arc by vᵢg.

The intersection ∩ᵢ Gᵢ is also shifted:
```
g + (∩ᵢ Gᵢ) = ∩ᵢ (g + Gᵢ)
```

But this doesn't help - we're trying to prove the intersection is nonempty in the first place.

### Orbit counting?

For Wilson's theorem, orbit counting under conjugation gave the result.

**Can we count something here?**

Define:
```
X = {(k, i) : k ∈ Gᵢ}
```

This is the set of (k value, speed index) pairs where k is good for speed vᵢ.

Size: |X| = Σᵢ |Gᵢ| ≈ n · (n-1)p/(n+1).

**Question:** What group action on X reveals structure?

G = (Z/pZ)* acts on X by:
```
g · (k, i) = (gk mod p, i)
```

But gk ∈ Gᵢ only if g maps the arc Gᵢ to itself, which doesn't generally happen.

### Obstacle

I don't see a natural group action that preserves the relevant structure. Unlike Wilson's theorem where conjugation preserved the set of p-cycles, here multiplication/translation don't preserve arcs in a useful way.

**Conclusion:** BLOCKED - no useful group action found

---

## Attack 7: Explicit Gap Structure for Case 2

**Idea:** When v₀ ≡ 0 (mod n+1), the bad set B₀ has SPECIAL STRUCTURE that creates exploitable gaps.

### Case 2 structure: v₀ = k(n+1)

At t = j/(n+1) for integer j:
```
v₀ · j/(n+1) = kj (mod 1)
```

So v₀ lands EXACTLY at integers when t = j/(n+1).

These are the "worst" times for v₀ (distance 0).

**Key observation:** The bad set B₀ has PERIOD 1/(n+1).

Explicitly, B₀ consists of intervals around t = j/(n+1) for j = 0, 1, ..., n.

### Systematic gaps

Consider the interval [a/(n+1), (a+1)/(n+1)] for any integer a.

The center t = (2a+1)/(2(n+1)) is MAXIMALLY FAR from both a/(n+1) and (a+1)/(n+1).

At this t:
```
v₀t = k(n+1) · (2a+1)/(2(n+1)) = k(2a+1)/2 (mod 1)
```

If k is odd:
```
v₀t = (odd)/2 (mod 1)
```

Distance to nearest integer = 1/2 (maximum possible).

**So:** t = (2a+1)/(2(n+1)) gives ||v₀t|| = 1/2 for odd k.

This is MUCH better than the required 1/(n+1).

### Can other speeds fail here?

We need to check if the other n-1 speeds also satisfy the bound at these special times.

**Problem:** Without knowing the other speeds, can't guarantee they all succeed.

### Counting gaps

For v₀ = k(n+1), the "safe" times (far from v₀'s bad regions) have measure at least:
```
1 - 2k/(n+1)
```

For k = 1: measure ≥ (n-1)/(n+1)

This is LARGE! More than half the interval.

**Heuristic:** If the other n-1 speeds have "random" bad sets, the probability all of them avoid a specific safe point is:
```
∏ᵢ≠₀ (1 - 2/(n+1)) ≈ ((n-1)/(n+1))^{n-1} > 0
```

But this is probabilistic, not rigorous.

### Can we make it rigorous?

**Attempt:** Partition [0,1) into (n+1) intervals:
```
Iⱼ = [j/(n+1), (j+1)/(n+1)) for j = 0, ..., n
```

For v₀ = k(n+1), the time t = j/(n+1) + 1/(2(n+1)) = (2j+1)/(2(n+1)) is in the MIDDLE of Iⱼ.

At this time:
- v₀ has distance 1/(2(n+1)) (plenty of slack since 1/(2(n+1)) > 1/(n+1) for n ≥ 1)

Wait, let me recalculate:
```
v₀t = k(n+1) · (2j+1)/(2(n+1)) = k(2j+1)/2 (mod 1)
```

For k = 1:
```
= (2j+1)/2 (mod 1)
```

Fractional part = 1/2 (for all j since 2j is even).

Distance to nearest integer = 1/2 ≥ 1/(n+1) for n ≥ 1. ✓

**For other speeds vᵢ:**
```
vᵢ · (2j+1)/(2(n+1)) = vᵢ(2j+1)/(2(n+1)) (mod 1)
```

We need ||vᵢ(2j+1)/(2(n+1))|| ≥ 1/(n+1).

**Hmm.** This depends on the specific vᵢ and j. Can't guarantee it without knowing the speeds.

### Obstacle

Even with Case 2 structure creating systematic gaps, we can't prove the other speeds don't fall into bad regions at those specific times without using arithmetic constraints.

**Conclusion:** BLOCKED - need to control all speeds simultaneously

---

## Attack 8: Small Modulus Forcing

**Idea:** For Case 2, prove that a SMALL modulus m ≤ poly(n, V) must work.

### Why this helps

If we can prove "some m ≤ M works" for explicit M, that's constructive and rigorous.

The current analytic bound gives M = C·V^{2n}·n^{O(n)}, which is huge.

Empirically, M < 50 for speeds up to 30. Can we prove M ≤ poly(n, V)?

### Approach: Exclusion counting

For modulus m, let:
```
N_m = # of k ∈ {1, ..., m-1} where all vᵢk mod m are in good interval
```

If N_m > 0, we're done.

**Claim to prove:** For Case 2 tuples, some m ≤ M has N_m > 0.

**Contrapositive:** If all m ≤ M have N_m = 0, derive contradiction with coprimality.

### Pigeonhole over moduli

Consider all moduli m ∈ {2, 3, ..., M}.

For each m, we have N_m = 0 (assuming failure).

This means: For every m ≤ M and every k ∈ {1, ..., m-1}, at least one speed vᵢ fails.

**Counting failures:** For each (m, k) pair, at least one i has vᵢk mod m outside good interval.

Total (m, k) pairs: Σ_{m=2}^M (m-1) ≈ M²/2.

Total (m, k, i) failures: At least M²/2 (since each (m,k) has ≥1 failure).

**But:** Each speed vᵢ can fail at most M times (one per modulus).

Wait, that's not right. For each vᵢ, how many (m, k) pairs can it fail at?

For fixed vᵢ and m, it fails at k values where vᵢk mod m ∈ bad interval.

The bad interval has size ~2m/(n+1).

So vᵢ fails at ~2m/(n+1) values of k (mod m).

**Across all m ≤ M:**
```
# failures for vᵢ ≈ Σ_{m=2}^M 2m/(n+1) ≈ M²/(n+1)
```

**Total failures across all speeds:**
```
≈ n · M²/(n+1)
```

**But we need at least M²/2 failures (from (m,k) pairs).**

So:
```
n · M²/(n+1) ≥ M²/2
```

This gives:
```
n/(n+1) ≥ 1/2
```

Which is true for n ≥ 1. So no contradiction!

### Obstacle

Counting argument doesn't give tight enough bounds. The failures can be distributed across speeds without contradiction.

**Conclusion:** BLOCKED - counting too loose

---

## Attack 9: Case 2 => Slack => Smaller Threshold

**Idea:** Case 2 tuples empirically have ML > 1/(n+1). Prove this algebraically, then show slack makes problem easier.

### Empirical observation

All tested Case 2 tuples have ML > 1/(n+1). Examples:
- (1,2,4): ML = 1/3 > 1/(3+1) = 1/4
- (1,2,5,6): ML = 2/7 > 1/(4+1) = 1/5
- (1,4,5,10): ML = 1/3 > 1/(4+1) = 1/5

**Hypothesis:** Case 2 structure forces ML > 1/(n+1) + ε for some ε > 0.

**If true:** We could prove existence of t with all distances ≥ 1/(n+1) by proving existence of t with all distances ≥ 1/(n+1) - ε/2.

But proving existence at threshold 1/(n+1) - ε/2 is still hard!

### Why does Case 2 have slack?

**Intuition:** The tuple (1,2,...,n) achieves exactly ML = 1/(n+1) at t = 1/(n+1).

This tight case has NO speed divisible by n+1.

For Case 2 with v₀ ≡ 0 (mod n+1), we can't use t = 1/(n+1) (it fails for v₀).

We must use a DIFFERENT t, which empirically achieves better distances.

**Can we prove this?**

**Lemma (attempted):** If (v₁, ..., vₙ) has v₀ ≡ 0 (mod n+1) and achieves ML exactly 1/(n+1), then gcd(v₁, ..., vₙ) > 1.

**Proof attempt:**

Suppose ML = 1/(n+1) exactly, achieved at time t.

Then for all i:
```
||vᵢt|| = 1/(n+1)
```

This means vᵢt ≡ ±1/(n+1) (mod 1).

So vᵢt = mᵢ ± 1/(n+1) for integers mᵢ.

For v₀ ≡ 0 (mod n+1), write v₀ = k(n+1).

Then:
```
k(n+1)t = m₀ ± 1/(n+1)
```

So:
```
t = m₀/(k(n+1)) ± 1/(k(n+1)²)
```

For this specific t, the other speeds satisfy:
```
vᵢt = mᵢ ± 1/(n+1)
```

Substituting t:
```
vᵢ[m₀/(k(n+1)) ± 1/(k(n+1)²)] = mᵢ ± 1/(n+1)
```

Multiply through by k(n+1)²:
```
vᵢ[m₀(n+1) ± 1] = (mᵢ ± 1/(n+1)) · k(n+1)²
```

The RHS is an integer times (n+1)², but not generally an integer since mᵢ ± 1/(n+1) is not an integer.

**Wait, this doesn't work.** I'm mixing exact equality with modular arithmetic.

Let me restart more carefully.

### Obstacle

Proving Case 2 has slack requires tight analysis of when ML = 1/(n+1) is achievable, which reduces to the original problem!

**Conclusion:** BLOCKED - circular reasoning

---

## Attack 10: Residue System Completion

**Idea:** For Case 2 with v₀ ≡ 0 (mod n+1), use the OTHER speeds to build a complete residue system mod some m.

### Setup

Coprime speeds v₁, ..., vₙ with v₀ = k(n+1).

**Question:** For which m do the speeds {v₁ mod m, ..., vₙ mod m} form a "diverse" residue system?

**Definition:** Call residues diverse mod m if they're spread across the good interval [⌈m/(n+1)⌉, m - ⌈m/(n+1)⌉].

### Approach A: Choose m coprime to all speeds

If gcd(m, vᵢ) = 1 for all i, then the map k ↦ vᵢk mod m is a bijection on (Z/mZ)*.

So as k varies over {1, ..., m-1}, the residue vᵢk mod m hits each of {1, ..., m-1} exactly once (if m is prime).

**For prime m > max(vᵢ):**
- Each vᵢk sweeps through {1, ..., m-1} as k varies
- The good interval is [⌈m/(n+1)⌉, m - ⌈m/(n+1)⌉]
- Size of good interval: ~(n-1)m/(n+1)

**For each vᵢ separately:**
- Fraction of k that work: ~(n-1)/(n+1)

**For all vᵢ together (assuming independence):**
- Expected fraction: ~((n-1)/(n+1))^n

But the residues are NOT independent - they all depend on the same k!

### Approach B: Chinese Remainder Theorem

Suppose we could find primes p₁, ..., pₙ such that:
- For prime pᵢ, speed vᵢ has a working k value

Then by CRT, we could combine these k values into a working t.

**But:** We need ONE t that works for ALL speeds, not separate k for each speed.

CRT would give us separate solutions mod each pᵢ, but combining them doesn't guarantee a common solution.

### Obstacle

Residue systems don't solve the simultaneity problem. We need ONE k that works for ALL speeds, and building complete residue systems doesn't force this.

**Conclusion:** BLOCKED - doesn't solve simultaneity

---

## Summary After 10 Attacks

**Pattern recognized:** ALL approaches reduce to proving arc intersection is nonempty.

**The three fundamental obstacles:**
1. **Additive-Multiplicative Gap:** Coprimality (additive) doesn't control residues (multiplicative)
2. **Simultaneity:** Need one t for all speeds, not separate t per speed
3. **Correlation:** All speeds depend on same t, no probabilistic independence

**What's been tried:**
- Measure theory → too weak
- Inclusion-exclusion → correlations unclear
- Coprimality forcing → wrong algebraic structure
- Group actions → no useful action found
- Explicit gaps → can't control all speeds
- Counting arguments → too loose
- Slack analysis → circular
- Residue systems → doesn't solve simultaneity

**What's NOT been tried:**
1. Analytic number theory (character sums, Weil bounds) - gives existence but at huge primes
2. Topology/homology - unclear how to apply
3. Extremal combinatorics - unclear what to count
4. Computer-assisted proof - verifies but doesn't explain

---

## The Core Question

**Is there an algebraic bridge from gcd=1 to arc intersection?**

**What would such a bridge look like?**

**Theorem (desired):** If gcd(v₁, ..., vₙ) = 1, then for some prime p ≤ poly(n, max vᵢ), the arcs {k : vᵢk mod p ∈ [L, R]} intersect.

**Current state:** No such theorem known. Analytic number theory gives existence at exponentially large p. Empirically true at tiny p.

**The gap:** Theory says p = exp(poly(n, V)). Reality shows p < 50. Gap is ENORMOUS.

---

## Next Steps

1. **Research:** Search for theorems connecting coprimality to residue distribution
2. **Induction with slack:** Try n-1 speeds, use slack to add nth
3. **Structural analysis:** Why do (1,2,...,n) and Case 2 differ?
4. **Computational patterns:** Analyze which primes work for which tuples, find patterns

---

*Status: 10 deep attacks completed*
*Common blocker: All reduce to arc intersection*
*Fundamental gap: Additive (coprimality) vs Multiplicative (residues)*
