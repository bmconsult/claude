# Case 2: Direct Constructive Approach

**New angle:** Instead of proving arc intersection generally, exploit the SPECIFIC structure of Case 2 to construct an explicit working time.

---

## Attack 11: Exploit v₀ Periodicity Directly

### Key observation

When v₀ = k(n+1), the speed v₀ has PERIOD 1/(n+1) in its bad set.

Specifically, B₀ (bad times for v₀) has the property:
```
t ∈ B₀ ⟺ t + 1/(n+1) ∈ B₀ (mod 1)
```

### Partition by v₀ periods

Divide [0, 1) into n+1 intervals:
```
Iⱼ = [j/(n+1), (j+1)/(n+1)) for j = 0, 1, ..., n
```

**Claim:** In each Iⱼ, there exist "safe" times for v₀ (far from boundaries).

Specifically, consider:
```
tⱼ = j/(n+1) + α/(n+1)
```

where α ∈ (0, 1) is chosen to maximize ||v₀·tⱼ||.

At this time:
```
v₀·tⱼ = k(n+1)[j/(n+1) + α/(n+1)]
     = kj + kα (mod 1)
```

Distance to nearest integer:
```
||v₀·tⱼ|| = ||kα|| = min({kα}, 1 - {kα})
```

**For k = 1 and α = 1/2:**
```
||v₀·tⱼ|| = 1/2 ≫ 1/(n+1)
```

Great! So tⱼ = (j + 1/2)/(n+1) = (2j+1)/(2(n+1)) is excellent for v₀.

### Check other speeds at these special times

**Question:** For which j does (2j+1)/(2(n+1)) work for ALL speeds?

We need to check if all vᵢ (i ≠ 0) satisfy:
```
||vᵢ · (2j+1)/(2(n+1))|| ≥ 1/(n+1)
```

**This requires:**
```
min({vᵢ(2j+1)/(2(n+1))}, 1 - {vᵢ(2j+1)/(2(n+1))}) ≥ 1/(n+1)
```

Let rᵢⱼ = {vᵢ(2j+1)/(2(n+1))}.

We need:
```
rᵢⱼ ∈ [1/(n+1), n/(n+1)]
```

**Problem:** Without knowing the vᵢ, can't guarantee this for all i and some j.

### Pigeonhole over j choices

We have n+1 choices of j ∈ {0, 1, ..., n}.

For each vᵢ (i ≠ 0), how many j values work?

The residues {vᵢ(2j+1)/(2(n+1))} for j = 0, ..., n form a sequence.

Since gcd(vᵢ, 2(n+1)) might not be 1 (if vᵢ is even), these residues might not cover all of [0,1).

**Example:** v₁ = 1, n = 3, so n+1 = 4.

For j = 0, 1, 2, 3:
```
v₁·1/(2·4) = 1/8
v₁·3/(2·4) = 3/8
v₁·5/(2·4) = 5/8
v₁·7/(2·4) = 7/8
```

All four values are in [1/4, 3/4] = [1/(n+1), n/(n+1)]. ✓

**But:** For v₂ = n+1 = 4:
```
v₂·1/8 = 4/8 = 1/2 ✓
v₂·3/8 = 12/8 = 3/2 ≡ 1/2 (mod 1) ✓
v₂·5/8 = 20/8 = 5/2 ≡ 1/2 (mod 1) ✓
v₂·7/8 = 28/8 = 7/2 ≡ 1/2 (mod 1) ✓
```

All land at 1/2! Distance = 1/2 ≥ 1/4. ✓

This is promising for small examples, but can we prove it generally?

### Attempt at general proof

**Claim:** For n+1 times tⱼ = (2j+1)/(2(n+1)) where j = 0, ..., n, at least one works for all speeds.

**Proof attempt:**

For speed vᵢ, the bad j values are those where:
```
{vᵢ(2j+1)/(2(n+1))} ∉ [1/(n+1), n/(n+1)]
```

i.e.:
```
{vᵢ(2j+1)/(2(n+1))} ∈ [0, 1/(n+1)) ∪ (n/(n+1), 1)
```

**How many j can be bad?**

The residues vᵢ(2j+1)/(2(n+1)) for j = 0, ..., n are:
```
vᵢ/(2(n+1)), 3vᵢ/(2(n+1)), 5vᵢ/(2(n+1)), ..., (2n+1)vᵢ/(2(n+1))
```

These are an arithmetic sequence mod 1 with common difference 2vᵢ/(2(n+1)) = vᵢ/(n+1).

**Case:** gcd(vᵢ, n+1) = 1

Then vᵢ/(n+1) generates a cyclic group of order n+1 in Z/(n+1)Z.

The n+1 residues are:
```
vᵢ·1/(n+1), vᵢ·3/(n+1), ..., vᵢ·(2n+1)/(n+1) (mod 1)
```

Since gcd(vᵢ, n+1) = 1, the multiples {vᵢ·ℓ/(n+1) : ℓ = 0, ..., n} are a permutation of {0/(n+1), 1/(n+1), ..., n/(n+1)}.

But we have odd ℓ = 1, 3, 5, ..., 2n+1.

**Hmm, this is getting complicated.**

Let me think differently.

### Alternative: Direct case analysis

**For n = 3 (so n+1 = 4):**

Case 2 means some v₀ ≡ 0 (mod 4). Simplest: v₀ = 4.

Tuple: (1, 2, 4) [after removing GCD if needed]

Check times t = 1/8, 3/8, 5/8, 7/8:

**t = 1/8:**
- v₁ = 1: 1/8 → distance = 1/8 < 1/4 ✗

**t = 3/8:**
- v₁ = 1: 3/8 → distance = 3/8 ✓
- v₂ = 2: 6/8 = 3/4 → distance = 1/4 ✓
- v₃ = 4: 12/8 = 1/2 → distance = 1/2 ✓

So t = 3/8 works!

**Can we prove this pattern holds generally?**

**Observation:** For tuple (1, 2, ..., n, n+1), the time t = 3/8 doesn't obviously work in general.

Wait, let me recalculate for (1,2,3,4):

**t = 3/8:**
- v₁ = 1: 3/8 → distance = 3/8 ✓
- v₂ = 2: 6/8 = 3/4 → distance = 1/4 ✓
- v₃ = 3: 9/8 = 1 + 1/8 → distance = 1/8 < 1/5 ✗

Fails!

So the pattern doesn't hold generally.

### Obstacle

Even with the special Case 2 structure and explicit construction candidates, we can't prove one of the n+1 special times works without knowing the specific speeds.

**Conclusion:** BLOCKED - explicit construction requires speed-dependent analysis

---

## Attack 12: Measure + Structure

**Idea:** Combine measure theory with Case 2 structure to show "most" of [0,1) is good.

### Setup

For Case 2 with v₀ = k(n+1), we know:
```
μ(B₀) ≤ 2k/(n+1)
```

If k = 1:
```
μ(B₀) ≤ 2/(n+1)
```

For the other speeds, assuming they're "generic":
```
μ(Bᵢ) ≤ 2vᵢ/(n+1)
```

**Total bad measure:**
```
μ(⋃ Bᵢ) ≤ μ(B₀) + Σᵢ≠₀ μ(Bᵢ) ≤ 2/(n+1) + 2Σᵢ≠₀ vᵢ/(n+1)
```

If Σᵢ≠₀ vᵢ < (n-1)/2, then:
```
μ(⋃ Bᵢ) < 2/(n+1) + (n-1)/(n+1) = (n+1)/(n+1) = 1
```

So good region has positive measure!

**But:** This requires Σᵢ≠₀ vᵢ < (n-1)/2.

For speeds (1, 2, ..., n-1, n+1), we have:
```
Σᵢ≠ₙ vᵢ = 1 + 2 + ... + (n-1) = n(n-1)/2
```

For n = 3: Σ = 3·2/2 = 3 vs (n-1)/2 = 1. Condition fails.

### Refinement: Use correlation

The union bound is loose. Many bad sets overlap.

**Inclusion-exclusion:**
```
μ(⋃ Bᵢ) = Σᵢ μ(Bᵢ) - Σᵢ<ⱼ μ(Bᵢ ∩ Bⱼ) + ...
```

**Question:** What is μ(B₀ ∩ Bᵢ) for i ≠ 0?

Both v₀t and vᵢt must be within 1/(n+1) of an integer.

For v₀ = (n+1):
```
(n+1)t ≈ integer
```

So t ≈ j/(n+1) for some integer j.

Then:
```
vᵢt ≈ vᵢ·j/(n+1) (mod 1)
```

For this to be ≈ integer, we need:
```
vᵢ·j/(n+1) ≈ ℓ (mod 1)
```

i.e.:
```
vᵢj ≈ ℓ(n+1) (mod something)
```

**This depends on vᵢ mod (n+1)!**

### Case 2 special structure

For v₀ ≡ 0 (mod n+1), the bad set B₀ is concentrated near t = j/(n+1).

For other speeds vᵢ, the overlap with B₀ depends on vᵢ mod (n+1).

**Hypothesis:** When v₀ ≡ 0 (mod n+1) and other speeds are diverse mod (n+1), the overlaps are SMALL.

**Can we quantify this?**

If all vᵢ (i ≠ 0) satisfy vᵢ ≢ 0 (mod n+1) (which is typical since gcd = 1), then:
- vᵢ mod (n+1) ∈ {1, 2, ..., n}
- At t = j/(n+1), we have vᵢt = vᵢj/(n+1)
- Fractional part: {vᵢj/(n+1)} = (vᵢj mod (n+1))/(n+1)

For this to be near 0 or 1, we need:
```
vᵢj mod (n+1) ∈ {0, 1, ..., ε(n+1)} ∪ {(1-ε)(n+1), ..., n}
```

**How many j ∈ {0, ..., n} satisfy this?**

Since vᵢ ≢ 0 (mod n+1) and gcd(vᵢ, n+1) divides both vᵢ and n+1:

**Subcase:** gcd(vᵢ, n+1) = 1

Then vᵢj mod (n+1) cycles through {0, 1, ..., n} as j varies over {0, ..., n}.

Fraction that land in bad zone: ~2ε.

With ε = 1/(n+1):
```
Fraction ≈ 2/(n+1)
```

So μ(B₀ ∩ Bᵢ) ≈ μ(B₀) · 2/(n+1) ≈ 2/(n+1) · 2/(n+1) = 4/(n+1)²

**Subcase:** gcd(vᵢ, n+1) = d > 1

Then vᵢj mod (n+1) takes values in d·(Z/(n+1)Z), hitting only (n+1)/d distinct values.

This INCREASES overlap!

### Obstacle

Without restricting the speeds (beyond coprimality), the inclusion-exclusion terms depend on gcd relationships with n+1, which we can't control.

**Conclusion:** BLOCKED - correlation terms depend on arithmetic structure

---

## Summary After 12 Attacks

**Every single approach** reduces to one of three insurmountable obstacles:

1. **Additive-Multiplicative Gap**
2. **Simultaneity** (need one t for all speeds)
3. **Speed-Dependent Structure** (can't prove without knowing speeds)

**The fundamental problem:**

The LRC is a statement that's TRUE for ALL coprime tuples. But different tuples require DIFFERENT times t. There's no universal construction.

Case 1 has a universal construction: t = 1/(n+1).

Case 2 does NOT have a universal construction. Different Case 2 tuples need different t values:
- (1,2,4) works at t = 1/3
- (1,2,5,6) works at t = 2/7
- (1,4,5,10) works at t = 1/3

**Is there an algebraic proof?**

**Hypothesis:** The empirical 100% success rate suggests the answer is YES, but the proof technique required may be:
1. Analytic (Weil bounds, exponential sums) - gives huge p
2. Computational (verify all cases up to some bound)
3. Hybrid (combine structure with computation)

**Pure algebraic proof:** May not exist using current techniques. The additive-multiplicative gap is fundamental.

---

## Recommendations

1. **Accept analytic proof:** The Weil bound approach IS rigorous, just gives large p
2. **Hybrid approach:** Prove for n ≤ N computationally, use analytic bound for n > N
3. **New mathematics:** Wait for someone to discover the additive-multiplicative bridge theorem
4. **Reformulate:** Maybe LRC is not provable algebraically but is provable via other means

---

*Status: 12 attacks completed, all BLOCKED*
*Fundamental obstacles: Additive-multiplicative gap, simultaneity, speed-dependence*
*Recommendation: Pure algebraic proof may not exist with current techniques*
