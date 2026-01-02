# Case 2 Algebraic Attack Log

**Goal:** Rigorous algebraic proof that Case 2 tuples (some v ≡ 0 mod n+1) always have a lonely time.

**Status:** IN PROGRESS

---

## Attack 1: Continued Fraction Approach

**Idea:** For Case 2 tuple with v₀ = k(n+1), examine convergents of 1/(n+1). Perhaps these provide working denominators.

### Setup

Let v₀ = k(n+1) for some k ≥ 1. The continued fraction of 1/(n+1) is trivial:
```
1/(n+1) = [0; n+1] = 0 + 1/(n+1)
```

Convergents:
- p₀/q₀ = 0/1
- p₁/q₁ = 1/(n+1)

This is too simple - no non-trivial convergents.

### Pivot: Try 1/v₀ instead

v₀ = k(n+1), so 1/v₀ = 1/(k(n+1))

For k = 1: Same as above
For k > 1: Convergents of 1/(k(n+1))...

**Wait.** This isn't the right angle. The continued fraction of 1/(n+1) doesn't help because the problem is finding t that works for ALL speeds simultaneously.

### Reformulation: Simultaneous Approximation

What if we try to approximate ALL speeds simultaneously? For each vᵢ, we want:
```
{vᵢt} ∈ [1/(n+1), n/(n+1)]
```

This is a system of simultaneous Diophantine approximation constraints.

**Known result (Dirichlet):** For any α₁, ..., αₙ and Q, there exists q ≤ Q^n and integers p₁, ..., pₙ such that:
```
|qαᵢ - pᵢ| < 1/Q for all i
```

**Problem:** This doesn't give us control over WHERE the approximations land, just that they're close. We need the residues to land in a specific interval.

### Obstacle Hit

Continued fractions give good approximations, but we need:
1. All residues in a specific interval [L, R]
2. Not just "close" but "in the interval"

This reduces back to the arc intersection problem. Continued fractions don't bypass it.

**Conclusion:** BLOCKED - reduces to arc intersection

---

## Attack 2: Explicit Modulus Construction

**Idea:** If v₀ = k(n+1), try t = j/m for specific m related to v₀ and other speeds.

### Approach 2A: Use m = lcm of small factors

For tuple (v₁, ..., vₙ) with v₀ = k(n+1), consider:
```
m = lcm(small factors of v₁, ..., vₙ)
```

**Example:** (1, 4, 5, 10) where v₂ = 4 ≡ 0 (mod 4)
- n+1 = 5
- v₂ = 4 = 1·4 (not 0 mod 5, so not Case 2 for n=4)

**Correct example:** (1, 2, 5, 6) where n=4, n+1=5
- v₃ = 5 ≡ 0 (mod 5) ✓ This is Case 2
- Empirically works at t = 2/7

Why m = 7?
- 7 is prime
- Not obviously related to speeds (1,2,5,6)
- gcd(7, 1·2·5·6) = 1

### Approach 2B: Use m coprime to problematic speed

For v₀ ≡ 0 (mod n+1), choose m coprime to v₀ and try t = 1/m.

At t = 1/m:
```
vᵢ/m has distance ||vᵢ/m|| = min(vᵢ mod m, m - (vᵢ mod m)) / m
```

Need: min(rᵢ, m-rᵢ) ≥ m/(n+1) where rᵢ = vᵢ mod m

This requires: rᵢ ∈ [⌈m/(n+1)⌉, m - ⌈m/(n+1)⌉]

**Question:** For which m can we guarantee this for all speeds?

If m is chosen such that all vᵢ are coprime to m, then the residues rᵢ = vᵢ mod m are "random-ish" in {1, ..., m-1}.

But we can't force them into the good interval without knowing the speeds.

### Approach 2C: Prime m larger than all speeds

For m = p (prime) > max(vᵢ):
- All vᵢ < p, so rᵢ = vᵢ
- Need: vᵢ ∈ [⌈p/(n+1)⌉, p - ⌈p/(n+1)⌉]

This requires choosing p such that all speeds land in the middle of [1, p-1].

**Can we always find such a p?**

For ANY speeds, we need p such that:
- vᵢ ≥ p/(n+1) for all i
- vᵢ ≤ p - p/(n+1) = p·n/(n+1) for all i

The first constraint gives: p ≤ (n+1)·min(vᵢ) = n+1 (since min is 1)
The second gives: p ≥ (n+1)/n · max(vᵢ)

**Contradiction!** We need:
```
p ≥ (n+1)/n · V  and  p ≤ n+1
```

For V > n, this is impossible.

### Approach 2D: Use k/p for appropriate k

Instead of t = 1/p, try t = k/p for k chosen to shift residues favorably.

For t = k/p, residue of vᵢ is:
```
rᵢ(k) = (k·vᵢ) mod p
```

This is a LINEAR function of k mod p. The residues sweep through [0, p-1] as k varies.

**Key insight:** For each vᵢ, the good k values form an arc of size ~(n-1)p/(n+1).

We need: ∩ᵢ Arc(vᵢ) ≠ ∅

This is exactly the arc intersection problem!

### Obstacle Hit

All explicit constructions reduce to:
1. Choosing p
2. Proving arc intersection is nonempty

We're back to arc intersection.

**Conclusion:** BLOCKED - reduces to arc intersection

---

## Attack 3: Gap Measure Proof

**Idea:** Prove algebraically that when some v ≡ 0 (mod n+1), the bad region has measure strictly < 1 with explicit gaps.

### Setup

Define bad region:
```
B = {t ∈ [0,1) : ∃i with ||vᵢt|| < 1/(n+1)}
```

Write B = ⋃ᵢ Bᵢ where:
```
Bᵢ = {t : ||vᵢt|| < 1/(n+1)}
```

Each Bᵢ is a union of vᵢ intervals of length 2/(n+1).

**Measure calculation:**
```
μ(Bᵢ) = vᵢ · 2/(n+1) (mod 1)
```

If vᵢ ≥ (n+1)/2, the intervals overlap and:
```
μ(Bᵢ) ≤ 1
```

**Union bound:**
```
μ(B) ≤ Σᵢ μ(Bᵢ) ≤ n · 2/(n+1) = 2n/(n+1)
```

For n ≥ 2, this is ≥ 4/3 > 1, so union bound is useless.

### Inclusion-Exclusion

```
μ(B) = Σᵢ μ(Bᵢ) - Σᵢ<ⱼ μ(Bᵢ ∩ Bⱼ) + ...
```

**Computing μ(Bᵢ ∩ Bⱼ):**

Both vᵢt and vⱼt must be within 1/(n+1) of an integer. This gives:
```
{vᵢt} ∈ [0, 1/(n+1)] ∪ [n/(n+1), 1)
{vⱼt} ∈ [0, 1/(n+1)] ∪ [n/(n+1), 1)
```

The intersection depends on the relationship between vᵢ and vⱼ.

**Case:** vⱼ = a·vᵢ for integer a

Then {vⱼt} = a·{vᵢt} (mod 1), so if {vᵢt} ∈ [0, ε], then {vⱼt} cycles through a different residue.

This is getting complicated without using arithmetic structure.

### Key Question

**When v₀ ≡ 0 (mod n+1), does μ(B) < 1?**

If v₀ = k(n+1), then B₀ consists of v₀ = k(n+1) intervals of length 2/(n+1) each.

Since gcd(v₀, n+1) = n+1, these intervals have period 1/(n+1).

The intervals are:
```
[0, 1/(n+1)²] ∪ [1/(n+1) - 1/(n+1)², 1/(n+1) + 1/(n+1)²] ∪ ...
```

No wait, that's not right.

**Correcting:** For speed v and threshold δ = 1/(n+1):
```
Bᵥ = {t : {vt} ∈ [0, δ] ∪ [1-δ, 1)}
```

For v₀ = k(n+1):
```
{v₀t} = {k(n+1)t} = k·{(n+1)t}  (NOT generally true!)
```

Actually {v₀t} = {k(n+1)t} is just the fractional part of k(n+1)t.

Let me restart this more carefully.

### Careful Analysis

For v₀ = n+1 (simplest Case 2 scenario):

B₀ = {t : ||(n+1)t|| < 1/(n+1)}

Since (n+1)t ≡ 0 (mod 1/(n+1)), we have:
```
(n+1)t = j/(n+1) + ε for some integer j and |ε| < 1/(n+1)
```

This gives:
```
t ∈ [j/(n+1)² - 1/(n+1)², j/(n+1)² + 1/(n+1)²] for j = 0, 1, ..., (n+1)² - 1
```

Total measure: (n+1) · 2/(n+1)² = 2/(n+1)

**General v₀ = k(n+1):**
```
μ(B₀) = k(n+1) · 2/(n+1)² = 2k/(n+1)
```

If k ≥ (n+1)/2, then μ(B₀) ≥ 1.

**Hmm.** This doesn't immediately show μ(B) < 1.

### Obstacle

Without using the coprimality structure (gcd = 1), measure bounds are too weak. The union bound fails, and inclusion-exclusion requires understanding correlations between bad sets.

**Conclusion:** BLOCKED - need arithmetic structure, not just measure

---

## Attack 4: Residue Diversity via Coprimality

**Idea:** Use gcd = 1 to force diversity in residues mod some m, ensuring good k exists.

### Setup

Given coprime speeds v₁, ..., vₙ with gcd = 1.

**Bezout identity:** There exist integers c₁, ..., cₙ such that:
```
Σᵢ cᵢvᵢ = 1
```

**Question:** Can we use this to construct a working t?

### Attempt 1: Use Bezout coefficients

Let t = 1/m for some m. At this time:
```
vᵢt = vᵢ/m
```

We need vᵢ/m to have distance ≥ 1/(n+1) from integers.

**Can we choose m using the Bezout coefficients?**

If Σ cᵢvᵢ = 1, then for any m:
```
Σ cᵢvᵢ ≡ 1 (mod m)
```

This tells us the vᵢ span the integers, but doesn't directly control where vᵢ mod m lands.

### Attempt 2: Prime power structure

For prime p, the residues {vᵢ mod p} must satisfy:
```
gcd(v₁ mod p, ..., vₙ mod p, p) = 1
```

If all vᵢ ≡ 0 (mod p), then gcd(v₁, ..., vₙ) ≥ p > 1, contradicting coprimality.

**So:** For any prime p, at least one vᵢ ≢ 0 (mod p).

**Can we use this?**

If we could show: "For any n coprime integers, there exists prime p where the residues are DIVERSE enough that arc intersection occurs," we'd be done.

But "diverse" is vague. Let me make it precise.

### Attempt 3: Collision forcing

**Observation:** If vᵢ ≡ vⱼ (mod p), then the arcs for vᵢ and vⱼ are IDENTICAL.

This reduces the effective number of constraints from n to (# distinct residues mod p).

**Example:** If all vᵢ ≡ 1 (mod p), then all arcs are identical, so intersection is trivial.

**Question:** Can we find p where many speeds collide?

For coprime speeds, the collisions depend on prime factorizations.

**Problem:** We can't FORCE collisions without knowing the speeds.

### Attempt 4: Chinese Remainder Theorem

For coprime speeds, consider the map:
```
φₚ : (Z/(n+1)Z)ⁿ → Z/pZ
φₚ(k) = (v₁k mod p, ..., vₙk mod p)
```

The image of φₚ has size at most p.

**Pigeonhole:** If p < (n+1), then some distinct k₁, k₂ ∈ Z/(n+1)Z map to the same point.

But this doesn't help - we need a k that lands ALL speeds in the good interval.

### Obstacle

Coprimality (additive structure) doesn't obviously force residues (multiplicative structure) into the good interval.

The Bezout identity operates in the wrong "space" - it's about LINEAR COMBINATIONS, not RESIDUES.

**Conclusion:** BLOCKED - additive/multiplicative gap

---

## Attack 5: Covering Obstruction

**Idea:** Prove the bad sets Bᵢ cannot cover all of [0,1] when Case 2 structure exists.

### Setup

Bad set for speed vᵢ:
```
Bᵢ = {t ∈ [0,1) : ||vᵢt|| < 1/(n+1)}
```

This is a union of vᵢ intervals, each of length 2/(n+1).

**Covering question:** Can B₁ ∪ ... ∪ Bₙ = [0,1)?

If NOT, then [0,1) \ B ≠ ∅, so a good time exists.

### When can covering occur?

**Necessary condition:**
```
Σᵢ μ(Bᵢ) ≥ 1
```

We have μ(Bᵢ) ≤ vᵢ · 2/(n+1) (with equality if intervals don't overlap mod 1).

For small speeds:
```
Σᵢ μ(Bᵢ) ≈ 2/(n+1) · Σᵢ vᵢ
```

If Σᵢ vᵢ < (n+1)/2, covering is impossible by measure.

**But:** Speeds can be arbitrarily large, so Σ vᵢ can exceed (n+1)/2.

### Structure of intervals

For speed v, the bad intervals in [0,1) are:
```
[j/v - 1/(v(n+1)), j/v + 1/(v(n+1))] for j = 0, 1, ..., v-1
```

These v intervals have centers at j/v.

**For Case 2:** Some v₀ ≡ 0 (mod n+1).

Let v₀ = k(n+1). The bad intervals for v₀ have centers at:
```
j/(k(n+1)) for j = 0, 1, ..., k(n+1) - 1
```

These are spaced 1/(k(n+1)) apart.

**Key observation:** The interval [0, 1/(k(n+1))] is NOT covered by any interval centered at j/(k(n+1)) for j ≥ 1.

More precisely, the interval centered at 0 is:
```
[-1/(k(n+1)²), 1/(k(n+1)²)]
```

Wait, we need to be mod 1, so this wraps:
```
[0, 1/(k(n+1)²)] ∪ [1 - 1/(k(n+1)²), 1)
```

And the interval centered at 1/(k(n+1)) is:
```
[1/(k(n+1)) - 1/(k(n+1)²), 1/(k(n+1)) + 1/(k(n+1)²)]
```

The gap between these intervals is:
```
[1/(k(n+1)²), 1/(k(n+1)) - 1/(k(n+1)²)]
```

This has length:
```
1/(k(n+1)) - 2/(k(n+1)²) = (n+1-2)/(k(n+1)²) = (n-1)/(k(n+1)²)
```

**So v₀ alone leaves gaps of size ~1/(k(n+1)²).**

**Question:** Can the other speeds cover these gaps?

For another speed vᵢ to cover a point t ∈ [1/(k(n+1)²), 1/(k(n+1)) - 1/(k(n+1)²)], we need:
```
||vᵢt|| < 1/(n+1)
```

If vᵢ is coprime to v₀ = k(n+1), then... what?

### Obstacle

Without knowing the other speeds, I can't prove they don't cover the gaps left by v₀.

The gaps exist (measure theoretically), but could still be covered by n-1 other bad sets.

**Conclusion:** BLOCKED - can't prove gaps survive without arithmetic constraint

---

## Summary After 5 Attacks

All five approaches hit variants of the same obstacle:

**THE ADDITIVE-MULTIPLICATIVE GAP**

| What we have | What we need |
|--------------|--------------|
| gcd(v₁, ..., vₙ) = 1 (additive) | Residues vᵢk mod p in interval (multiplicative) |
| Bezout: Σcᵢvᵢ = 1 | ∃k: all vᵢk mod p ∈ [L, R] |
| Coprimality ensures span | ??? |

**Next steps:**

1. Research if there's a known theorem bridging additive and multiplicative structure
2. Try a completely different mathematical framework (topology? algebraic geometry?)
3. Attack the arc intersection problem with group theory (like Wilson's theorem approach)
4. Look for a probabilistic/counting argument that doesn't require independence

---

*Status: 5 attacks completed, all BLOCKED at additive/multiplicative gap*
*Next: Need fundamentally different approach or bridge theorem*
