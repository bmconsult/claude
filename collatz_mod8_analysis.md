# Collatz Mod-8 Barrier Analysis

## The Specific Barrier Claim

**User claim**: Numbers n ≡ 7 (mod 8) can stay in "bad set" {3,7}, creating an infinite nested hierarchy.

## Rigorous Verification

For odd n, the Collatz operation (combining 3n+1 and one division by 2):
T(n) = (3n+1)/2

### Dynamics mod 8 for odd numbers:

**n ≡ 1 (mod 8)**:
- 3n+1 ≡ 4 (mod 8)
- Has v₂ ≥ 2 (divisible by at least 4)
- After division: leads to even, further divisions needed
- Status: GOOD (will decrease)

**n ≡ 3 (mod 8)**:
- 3n+1 ≡ 10 ≡ 2 (mod 8)
- v₂ = 1 exactly
- (3n+1)/2 ≡ 5 (mod 8)
- **ESCAPES to good set immediately!**

**n ≡ 5 (mod 8)**:
- 3n+1 ≡ 16 ≡ 0 (mod 8)
- v₂ ≥ 3
- After divisions: leads to even
- Status: GOOD

**n ≡ 7 (mod 8)**:
- 3n+1 ≡ 22 ≡ 6 (mod 8)
- v₂ = 1 exactly
- (3n+1)/2 ≡ 11 ≡ 3 (mod 8)
- **Goes to 3 (mod 8), which then ESCAPES!**

## Wait - The Claim Appears Wrong?

Initial calculation suggests n ≡ 7 (mod 8) → n ≡ 3 (mod 8) → n ≡ 5 (mod 8).

This would mean ALL numbers escape within 2 steps!

## The Refinement - Nested Hierarchy

The issue is that (3n+1)/2 mod 8 depends on finer structure.

For n ≡ 7 (mod 8), we have n = 8k + 7:
- 3n+1 = 24k + 22 = 2(12k + 11)
- (3n+1)/2 = 12k + 11

Now mod 8:
- 12k + 11 ≡ 4k + 3 (mod 8)

This depends on k mod 2:
- If k ≡ 0 (mod 2): 4k + 3 ≡ 3 (mod 8) - **ESCAPES**
- If k ≡ 1 (mod 2): 4k + 3 ≡ 7 (mod 8) - **STAYS BAD**

## The Nested Structure

Refining to mod 16:
- n ≡ 7 (mod 16) means k even: T(n) ≡ 3 (mod 8) → ESCAPES
- n ≡ 15 (mod 16) means k odd: T(n) ≡ 7 (mod 8) → STAYS

Among n ≡ 15 (mod 16), we can refine to mod 32:
- n ≡ 15 (mod 32): T(n) = ?
- n ≡ 31 (mod 32): T(n) = ?

The pattern: At each level 2^m, half of the "bad set" escapes, half stays bad.

## The Hierarchy

- Level 3: B₃ = {n : n ≡ 7 (mod 8)}         - density 1/4
- Level 4: B₄ = {n : n ≡ 15 (mod 16)}       - density 1/8
- Level 5: B₅ = {n : n ≡ 31 (mod 32)}       - density 1/16
- Level k: Bₖ = {n : n ≡ 2^k-1 (mod 2^k)}   - density 1/2^(k-1)

## The Barrier

For an infinite trajectory to NEVER escape:
- n₀ must be in some Bₖ₀
- T(n₀) = n₁ must be in some Bₖ₁ with k₁ ≥ k₀
- T²(n₀) = n₂ must be in some Bₖ₂ with k₂ ≥ k₁
- ...

In the limit, this requires a trajectory that lands in Bₖ for arbitrarily large k.

In ℤ₂ (2-adic integers), the limit ∩ₖ Bₖ is exactly {-1}.

But -1 is not a positive integer!

## The Problem

**Why this doesn't prove the conjecture:**

Even though no FIXED n can be in Bₖ for all k (since n < 2^(⌊log₂(n)⌋+1)), the trajectory can GROW.

The sequence n₀, n₁, n₂, ... might have:
- n₁ ∈ B₅ (so n₁ ≥ 31)
- n₂ ∈ B₆ (so n₂ ≥ 63)
- n₃ ∈ B₇ (so n₃ ≥ 127)
- ...

The trajectory could grow without bound while staying in progressively refined bad sets.

We CANNOT prove this doesn't happen, because:
1. T(n) can be larger than n (specifically, T(n) ≈ 3n/2 for odd n before divisions)
2. The growth could outpace the escape rate
3. Average descent (proven) ≠ universal descent (needed)

## Conclusion

**The barrier is REAL and correctly identified.**

The nested hierarchy exists, has density → 0, but proving ALL trajectories eventually escape requires proving they can't grow fast enough to stay in the hierarchy forever.

This is the "almost all vs all" gap in concrete algebraic form.
