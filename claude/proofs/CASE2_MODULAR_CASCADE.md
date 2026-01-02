# Case 2 Proof Attempt: Modular Cascade Construction

## Setup

**Given:** Coprime speeds v₁ < v₂ < ... < vₙ with some v₀ ≡ 0 (mod n+1).
**Goal:** Find t ≠ 1/(n+1) with ||vᵢt|| ≥ 1/(n+1) for all i.

**Strategy:** Try t = 1/m for m = n+2, n+3, n+4, ... until we find one that works.

---

## Analysis at t = 1/m

At t = 1/m, runner with speed v has distance:
```
||v/m|| = min(r, m-r)/m where r = v mod m
```

For distance ≥ 1/(n+1), we need:
```
min(r, m-r) ≥ m/(n+1)
```

**Good region:** r ∈ [⌈m/(n+1)⌉, m - ⌈m/(n+1)⌉]

**Bad region:** r ∈ {0, 1, ..., ⌊m/(n+1)⌋ - 1} ∪ {m - ⌊m/(n+1)⌋ + 1, ..., m-1}

### Bad Region Size

Let L = ⌈m/(n+1)⌉. The bad region has size approximately:
```
|Bad| ≈ 2L ≈ 2m/(n+1)
```

### Good Region Size
```
|Good| ≈ m - 2m/(n+1) = m(n-1)/(n+1)
```

---

## Key Observation: Speed v is Bad at m ⟺ v mod m is in Bad Region

A speed v is "bad" at modulus m if:
```
v mod m ∈ [0, L-1] ∪ [m-L+1, m-1]
```

---

## Attempt 1: Pigeonhole Argument

**Claim:** As m varies over {n+2, n+3, ...}, coprimality prevents all n speeds from being bad simultaneously.

**Problem:** This needs to be proven, not assumed.

Let me analyze the structure more carefully...

---

## Attempt 2: Coprimality Leverage

**Key fact:** gcd(v₁, ..., vₙ) = 1 means there exist integers aᵢ with:
```
∑ᵢ aᵢvᵢ = 1
```

**Question:** Can we use this to show that for some m, the residues vᵢ mod m can't all be bad?

### Analysis

At modulus m, the bad regions are:
- Near 0: {0, 1, ..., L-1}
- Near m: {m-L+1, ..., m-1}

For ALL speeds to be bad, each vᵢ mod m must land in one of these two intervals.

**Constraint from coprimality:** ???

This is where I'm stuck. The Bezout identity ∑ aᵢvᵢ = 1 is an additive constraint, but badness at m is a multiplicative constraint (residue class membership).

---

## Attempt 3: Alternative t = j/(n+1)

Instead of t = 1/m, try t = j/(n+1) for j = 2, 3, ..., n.

**Recall:** Some v₀ = (n+1)k, so at t = j/(n+1):
```
v₀t = (n+1)k · j/(n+1) = jk
```

This is an integer, so ||v₀t|| = 0. **FAILS for v₀.**

So this approach doesn't work either - v₀ will always be at distance 0 for any t = j/(n+1).

---

## Attempt 4: Coprime-to-m Construction

**New idea:** Find m such that gcd(vᵢ, m) = 1 for all i.

If all speeds are coprime to m, then at t = 1/m, each vᵢ mod m is nonzero and could potentially avoid the bad regions.

**Problem:** We need m such that:
1. gcd(vᵢ, m) = 1 for all i
2. vᵢ mod m ∈ Good region for all i

Condition 1 is achievable (take m to be a prime larger than all speeds). But condition 2 is exactly the arc intersection problem that's already known to be hard.

---

## OBSTACLE IDENTIFIED

All approaches reduce to the same fundamental problem:

**For some modulus m, prove that the residues {v₁ mod m, ..., vₙ mod m} can't all land in the bad region of size ~2m/(n+1).**

This is equivalent to the arc intersection problem at primes, which is the known blocker.

---

## Status: BLOCKED

The Modular Cascade approach does not bypass the fundamental obstacle. It reformulates the problem but doesn't solve it.

**What's needed:** A way to leverage coprimality (additive structure) to constrain residue placement (multiplicative structure).

This is the "additive-multiplicative bridge" that LRC_MASTER.md identifies as the core missing piece.

---

*Analysis completed: January 2, 2026*
*Cascade: Status BLOCKED - reduces to arc intersection*
