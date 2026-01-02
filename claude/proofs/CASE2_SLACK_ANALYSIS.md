# Case 2: Exploiting the Slack Phenomenon

## Empirical Observation

**Key finding from LRC_MASTER.md:**
- ALL tight cases (ML = exactly 1/(n+1)) are Case 1 tuples
- Case 2 tuples empirically have ML > 1/(n+1) (strict inequality!)

**Examples:**
- (1,2,4): Case 2 (4 ≡ 0 mod 3), ML = 1/3 > 1/4 ✓
- (1,2,5,6): Case 2 (5 ≡ 0 mod 5), ML = 2/7 > 1/5 ✓
- (1,4,5,10): Case 2 (10 ≡ 0 mod 4), ML = 1/3 > 1/5 ✓

**Hypothesis:** The obstruction at t = 1/(n+1) forces alternative optimal times that achieve BETTER than 1/(n+1).

---

## Attempt: Prove ML ≥ 1/n for Case 2

If we could prove Case 2 tuples satisfy ML ≥ 1/n instead of 1/(n+1), we'd be done!

**Strategy:** Show that when v₀ = (n+1)k fails at t = 1/(n+1), there must exist t achieving distance ≥ 1/n.

### Analysis

At t = 1/(n+1), we have:
- v₀ lands at origin (distance 0)
- Other n-1 speeds have distances ≥ 1/(n+1) (if they're not in S₀)

**Question:** Can we perturb t slightly to lift v₀ off the origin without hurting the others too much?

Let t = 1/(n+1) + ε for small ε > 0.

For v₀ = (n+1)k:
```
v₀t = (n+1)k · (1/(n+1) + ε) = k + (n+1)kε
Distance ≈ ||(n+1)kε|| ≈ (n+1)kε for small ε
```

For other speeds vᵢ ≢ 0 (mod n+1):
```
vᵢt = vᵢ/(n+1) + vᵢε
Distance changes by ≈ vᵢε
```

**Problem:** The change for v₀ is proportional to (n+1)k, while for others it's vᵢ. We can't control all simultaneously without knowing specific values.

This perturbation approach is too fragile.

---

## Attempt: Use Symmetric Time t = 1/n

**Observation:** At t = 1/n, the "bad region" threshold is:
```
Distance < 1/(n+1) means min(r, n-r)/n < 1/(n+1)
⟺ min(r, n-r) < n/(n+1)
⟺ min(r, n-r) = 0 (since min is an integer < 1)
⟺ r = 0
```

So at t = 1/n, a speed v is bad ⟺ v ≡ 0 (mod n).

**Key insight:** The bad residue class at m = n is just {0}, not the two intervals we had before!

**Question:** In Case 2, do we have any speed v ≡ 0 (mod n)?

This depends on the specific tuple. Not all Case 2 tuples have a speed divisible by n.

**Counterexample:** (1, 2, 3, 5, 6) has 5 ≡ 0 (mod 5), but no speed is divisible by 4.

So t = 1/n doesn't universally work for Case 2.

---

## Attempt: Systematic Search of Small Denominators

**Claim:** For any Case 2 tuple, at least one of t = 1/m for m ∈ {n, n+1, n+2, ..., 2n} works.

**Why?** The heuristic probability that ALL these (n+1) values fail is very small.

**Problem:** This is a probabilistic heuristic, not a proof. We need rigorous argument.

### Inclusion-Exclusion Approach

Let B_m = event that all speeds are bad at t = 1/m.

We want to show: ∩_{m=n}^{2n} B_m = ∅ (at least one m works).

By inclusion-exclusion:
```
P(∪_m B_m^c) = 1 - P(∩_m B_m)
```

If we could show P(∩_m B_m) < 1 for the events defined by residue constraints...

**Problem:** The events B_m are not independent. Speed values are fixed; only m varies. This is dependency nightmare.

---

## Attempt: Counting Good (m,k) Pairs

For fixed speeds v₁, ..., vₙ, consider all rationals t = k/m with m ≤ M and 1 ≤ k < m.

Total # of such rationals: ∑_{m=2}^M (m-1) ≈ M²/2.

For each t = k/m, we can check if all speeds are lonely.

**Question:** Can we show that # lonely times grows faster than linearly in M?

**Heuristic:** Each (m,k) pair has probability ((n-1)/(n+1))ⁿ ≈ e^{-2/n} of being lonely.

Expected # lonely times ≈ M²/2 · e^{-2/n} → ∞ as M → ∞.

**Problem:** This shows many lonely times exist in (0, M] as M → ∞, but doesn't prove one exists in (0, 1] or any bounded interval.

The problem is we can't bound M apriori.

---

## Back to First Principles

Why does Case 2 seem harder than Case 1?

**Case 1:** Direct construction t = 1/(n+1) works because ALL speeds avoid r = 0 mod (n+1).

**Case 2:** Direct construction fails because AT LEAST ONE speed has r = 0 mod (n+1).

**Insight:** Case 1 is "uniform" (all speeds behave similarly mod n+1). Case 2 is "non-uniform" (different residue classes).

Maybe the non-uniformity is actually HELPFUL because it creates diversity in how speeds interact with different moduli?

**Hypothesis:** The more diverse the speed residues (across different moduli), the easier it is to find a working modulus.

**Maximum diversity:** All speeds have different residues mod every small modulus.

**Minimum diversity:** All speeds have same residue mod many moduli (but this violates coprimality for large enough moduli).

Can we formalize "diversity implies working modulus exists"?

---

## Coprimality as Diversity

**Theorem (Folklore):** gcd(v₁, ..., vₙ) = 1 ⟺ for every prime p, at least one vᵢ ≢ 0 (mod p).

This means coprime speeds are "diverse" in the sense that they don't all vanish at any prime.

**Question:** Does this diversity of "not all zero mod p" imply diversity of "not all bad mod p"?

**Intuition:** "Not all zero" is a very weak constraint (just one needs to be nonzero). "Not all bad" is stronger (enough need to be good that their good arcs intersect).

The gap between these is where the difficulty lies.

---

## Status: Explored Multiple Angles

All angles attempted:
1. ✗ Perturbation of t = 1/(n+1)
2. ✗ Universal t = 1/n
3. ✗ Systematic small denominator search (no proof)
4. ✗ Counting argument (no bounded interval guarantee)
5. ✗ Diversity hypothesis (couldn't formalize bridge to arc intersection)

**Conclusion:** The slack observation is empirically true but I cannot prove it implies LRC algebraically.

The fundamental wall remains: **coprimality (additive diversity) ⇏ residue diversity (multiplicative)**.

---

*Analysis completed: January 2, 2026*
*Slack angle: Empirically promising but algebraically elusive*
