# Case 2: Structural Analysis

## Key Structural Insight

**Case 2 Condition:** At least one speed v₀ ≡ 0 (mod n+1).

**Coprimality:** gcd(v₁, ..., vₙ) = 1.

### Critical Observation

If v₀ ≡ 0 (mod n+1) and gcd = 1, then:
1. NOT all speeds can be divisible by (n+1) (else gcd ≥ n+1)
2. Therefore, at least one speed vⱼ ≢ 0 (mod n+1)

**This means:** Every Case 2 tuple is a "mixed" tuple - some speeds divisible by (n+1), others not.

---

## Hypothesis: Residue-Based Partition

Partition the n speeds by their residues mod (n+1):
```
For r ∈ {0, 1, ..., n}, let S_r = {i : vᵢ ≡ r (mod n+1)}
```

**Case 2 condition:** |S₀| ≥ 1 (at least one speed in residue class 0)
**Coprimality:** Not all speeds in S₀ (else gcd ≥ n+1)

---

## New Construction Idea: Exploit Mixed Structure

**Observation:** If we could find t such that:
- Speeds in S₀ are handled differently than other speeds
- The "mixing" is what creates the opportunity

### Attempt: t = 1/p for prime p with specific properties

Choose prime p such that:
1. p > max(vᵢ) (all speeds coprime to p)
2. p ≡ 1 (mod n+1) (ensures certain symmetry)

**Why p ≡ 1 (mod n+1)?**

If p ≡ 1 (mod n+1), then (n+1) | (p-1), which means:
- The multiplicative group (Z/pZ)* has order p-1 ≡ 0 (mod n+1)
- This creates symmetry in how residues distribute

### Analysis at p ≡ 1 (mod n+1)

At t = k/p, speed vᵢ has distance ||vᵢk/p||.

For vᵢ ∈ S₀ (so vᵢ = (n+1)mᵢ for some mᵢ):
```
vᵢk/p = (n+1)mᵢk/p
```

The residue (n+1)mᵢk mod p depends on:
- mᵢ mod p
- k mod p
- How (n+1) behaves mod p

**Key:** Since p ≡ 1 (mod n+1), we have (n+1)⁻¹ exists mod p!

---

## Refined Approach: Two-Stage Construction

**Stage 1:** For speeds NOT in S₀ (i.e., vᵢ ≢ 0 mod n+1):
- These are exactly the speeds that work at t = 1/(n+1) in Case 1
- They ALREADY satisfy the lonely condition at any t = j/(n+1)

**Stage 2:** For speeds IN S₀ (i.e., vᵢ ≡ 0 mod n+1):
- These fail at t = j/(n+1)
- Need to find t that makes THESE lonely while preserving Stage 1 speeds

**Problem:** How to preserve Stage 1 while fixing Stage 2?

This is still hard because changing t affects all speeds simultaneously.

---

## Attempt: Weighted Average Construction

**Idea:** Instead of t = 1/(n+1), try:
```
t = (a·1/(n+1) + b·1/m) / (a+b)
```
for some carefully chosen m, a, b.

**Problem:** This becomes t = (a·m + b·(n+1)) / ((a+b)·m·(n+1)), which is just another rational number. We're back to finding the right rational.

---

## Fundamental Issue Re-Emerges

Every construction attempt reduces to:
**Find a rational t = k/M such that all speeds avoid bad regions.**

This IS the arc intersection problem.

---

## PIVOT: What if the answer is NOT constructive?

Maybe Case 2 for arbitrary n CANNOT be proven by explicit construction. Maybe it requires:
1. Existence argument (not construction)
2. Prime density argument (infinitely many primes work, so at least one must)
3. Counting argument (# good times > 0)

But all of these have been tried (listed as BLOCKED in LRC_MASTER.md).

---

## Status: Multiple Angles Explored, All Hit Same Wall

- Modular cascade → arc intersection
- Alternative j/(n+1) → fails for v₀
- Coprime-to-m → arc intersection
- Mixed structure exploitation → no leverage found
- Two-stage construction → simultaneous constraints still hard
- Weighted average → reduces to finding right rational

**Fundamental obstacle confirmed:** Additive structure (coprimality) doesn't constrain multiplicative structure (residues) in known ways.

---

*Analysis completed: January 2, 2026*
*Cascade: Multiple construction angles attempted, all blocked*
