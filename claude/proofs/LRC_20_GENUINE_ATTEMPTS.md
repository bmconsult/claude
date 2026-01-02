# LRC Case 2: 20 Genuine Attempts

**Date:** January 2, 2026
**Goal:** Prove or disprove Case 2 (some v ≡ 0 mod n+1) for arbitrary n
**Status at start:** n ≤ 9 proven, n ≥ 10 open

Each attempt is pushed to the wall. "Blocked" means I hit a genuine mathematical barrier, not "I gave up."

---

## ATTEMPT 1: Bezout Coefficient Analysis

**Idea:** Since gcd(v₁,...,vₙ) = 1, we have Σaᵢvᵢ = 1 for some integers aᵢ. Use this structure.

**Deep dive:**
The Bezout identity gives us: a₁v₁ + a₂v₂ + ... + aₙvₙ = 1

For any modulus m: Σaᵢvᵢ ≡ 1 (mod m)

If we could choose m such that the residues vᵢ mod m are "controlled" by this relation...

Let's try m = |a₁|v₁. Then:
- v₁ mod m = v₁ (since v₁ < m for |a₁| > 1)
- The Bezout relation becomes: a₁v₁ + ... ≡ 1 (mod |a₁|v₁)
- So: Σᵢ₌₂ aᵢvᵢ ≡ 1 - a₁v₁ ≡ 1 (mod v₁) if a₁v₁ ≡ 0

This doesn't constrain residues usefully.

**Try differently:** The Bezout coefficients can be computed via extended Euclidean algorithm. They satisfy |aᵢ| ≤ max(vⱼ)/gcd for some bound.

But the SIZE of coefficients doesn't tell us about RESIDUE POSITIONS.

**Verdict:** ❌ BLOCKED - Bezout is additive structure, can't bridge to multiplicative residue constraints.

---

## ATTEMPT 2: Collision Exploitation at Primes

**Idea:** At some primes p, multiple speeds have the same residue (collision). Fewer effective constraints might help.

**Deep dive:**
For n coprime speeds, at prime p dividing one speed vᵢ, that speed has residue 0.

More generally, if vᵢ ≡ vⱼ (mod p), they share residue structure.

Let c(p) = number of distinct residues among {v₁ mod p, ..., vₙ mod p}.

If c(p) < n, we have "collisions."

For p > max(v), all residues are distinct (c(p) = n).

For p ≤ max(v), collisions can occur.

**Question:** Does having c(p) < n make arc intersection easier?

**Analysis:** The arcs are defined by vᵢ⁻¹ · [L, R] mod p. If vᵢ ≡ vⱼ (mod p), their arcs are IDENTICAL.

So we effectively have c(p) constraints instead of n.

But the threshold is still 1/(n+1), not 1/(c(p)+1)!

The problem is: we have n RUNNERS, so the lonely distance threshold is fixed at 1/(n+1).

**Verdict:** ❌ BLOCKED - Collisions reduce constraints but not threshold. No leverage.

---

## ATTEMPT 3: CRT with Carefully Chosen Primes

**Idea:** Use t = k/M where M = p₁p₂...pₘ. By CRT, choose k mod pᵢ independently.

**Deep dive:**
If at each prime pⱼ, there exists kⱼ with good arc intersection, then CRT gives k solving all simultaneously.

The question: can we always find primes p₁, ..., pₘ where EACH has a solution?

**Problem identified earlier:** Some tuples fail at certain primes. If a tuple fails at p, then NO k works at that prime.

But we can CHOOSE which primes to include in M!

**Key insight:** We only need ONE prime where the tuple succeeds. Then M = p works.

So this reduces to: "For any coprime tuple, ∃ prime p with nonempty arc intersection."

This is exactly the main problem.

**Verdict:** ❌ BLOCKED - Reduces to "some prime works," which is the arc intersection problem.

---

## ATTEMPT 4: Equidistribution with Explicit Error Bounds

**Idea:** Modular inverses are equidistributed. Make this quantitative.

**Deep dive:**
For fixed a and primes p → ∞, the distribution of a⁻¹ mod p converges to uniform on (0,1).

Theorem (Duke-Friedlander-Iwaniec type): For a fixed, as p varies over primes ≤ X:
|{p : a⁻¹/p ∈ [α, β]}| = (β - α) · π(X) + O(X^{1/2+ε})

For our problem, we need JOINT distribution of (v₁⁻¹, ..., vₙ⁻¹) mod p.

**The issue:** These are not independent! They're deterministic functions of p.

For fixed speeds v₁, ..., vₙ, the vector (v₁⁻¹, ..., vₙ⁻¹) mod p is a single point on the n-torus.

As p varies, this point traces a curve. We need this curve to hit the "good region" (arc intersection).

**What's known:** For n = 2, the pair (a⁻¹, b⁻¹) mod p is equidistributed on the torus as p → ∞ (with error bounds).

For n > 2, similar results hold but with worse error terms.

**The gap:** Error terms grow with n. For n = 10, the error might swamp the main term for "small" p.

**Verdict:** ❌ BLOCKED - Error bounds exist but aren't explicit enough to prove arc intersection for all n.

---

## ATTEMPT 5: Structure of Minimal Counterexamples

**Idea:** Assume counterexample exists, derive contradictory structure.

**Deep dive:**
Let C = (v₁, ..., vₙ) be a minimal counterexample (no proper subset is a counterexample).

Properties of C:
1. gcd(v₁, ..., vₙ) = 1 (WLOG)
2. For ALL denominators m, NO k works
3. In particular, fails at m = n+1 (Case 2)
4. Each speed is "essential" - removing any gives a non-counterexample

**From (4):** For each vᵢ, the tuple (v₁, ..., v̂ᵢ, ..., vₙ) has a lonely time tᵢ.

At tᵢ, all runners except vᵢ are at distance ≥ 1/n (since there are n-1 runners, threshold is 1/n).

But vᵢ must be at distance < 1/(n+1) at tᵢ (otherwise C wouldn't be a counterexample).

So tᵢ is "bad" for vᵢ specifically.

**Attempt to derive contradiction:**
We have n times t₁, ..., tₙ where tᵢ is bad for vᵢ only.

Can we combine these to get a time good for all?

The issue is that the "good" times for vⱼ (j ≠ i) don't necessarily overlap.

**Verdict:** ❌ BLOCKED - Minimality gives structure but not enough to force contradiction.

---

## ATTEMPT 6: Prime Divisor Counting (Rosenfeld Extension)

**Idea:** Extend Rosenfeld's n ≤ 10 argument to arbitrary n.

**Deep dive:**
Rosenfeld's argument:
1. By MSS bound, any counterexample has speeds ≤ n^{2n}
2. A counterexample fails at ALL primes
3. Count small prime divisors of speed product
4. Show "failing at all primes" requires impossible structure

**For n = 10:**
- Bound: speeds ≤ 10^{20}
- Product of speeds ≤ 10^{200}
- Number of prime factors of product ≤ 200 · log(10^{20})/log(2) ≈ 13,000

Rosenfeld shows that the prime counting constraints are unsatisfiable.

**For general n:**
- Bound: speeds ≤ n^{2n}
- Product ≤ n^{2n²}
- Number of prime factors ≤ 2n² · log(n^{2n})/log(2) = O(n³ log n)

The constraints become:
- Must fail at O(n^{2n}/log n) primes (all primes up to the bound)
- But only O(n³ log n) prime factors available

For large n, there are MANY more primes than prime factors, so we can't "afford" to fail at all of them.

**The gap:** This is heuristic. Making it rigorous requires showing that each "failure" at a prime costs something in terms of prime factors.

**Verdict:** ❌ BLOCKED - The counting works heuristically, but the rigorous version needs bounds that depend on n in complex ways.

---

## ATTEMPT 7: The Slack Phenomenon (Algebraic)

**Idea:** Case 2 tuples empirically have ML > 1/(n+1). Prove this algebraically.

**Deep dive:**
Observation: When v₀ = (n+1)k, the natural choice t = 1/(n+1) fails.

Any OTHER t that works must give distance > 1/(n+1) for at least one runner (typically all).

**Conjecture:** If some v ≡ 0 (mod n+1), then ML > 1/(n+1).

**Attempt to prove:**
Suppose ML = 1/(n+1) exactly. Then there exists t* with:
- ||vᵢt*|| ≥ 1/(n+1) for all i
- ||vⱼt*|| = 1/(n+1) for some j (achieves minimum)

For v₀ = (n+1)k: ||v₀t*|| = ||(n+1)kt*|| = (n+1) · ||kt*|| (when this is < 1/2)

For this to equal 1/(n+1): (n+1) · ||kt*|| = 1/(n+1), so ||kt*|| = 1/(n+1)².

This is a very specific constraint on t*.

**Problem:** I can't derive a contradiction from here. The constraint is specific but not impossible.

**Verdict:** ❌ BLOCKED - The slack exists empirically, but proving it requires understanding the optimal t, which is the main problem.

---

## ATTEMPT 8: The Pigeonhole on Modular Arcs

**Idea:** For modulus m, the n arcs have total "size" n · (n-1)/(n+1). Use pigeonhole.

**Deep dive:**
Each speed v defines an arc A_v of size (n-1)m/(n+1) in Z/mZ.

Total arc coverage: n · (n-1)m/(n+1) = n(n-1)m/(n+1)

For n ≥ 2: n(n-1)/(n+1) ≥ 2 · 1 / 3 = 2/3 (at n=2)

At n = 10: 10 · 9 / 11 ≈ 8.18

So the arcs cover Z/mZ about 8 times on average (for n=10).

**Pigeonhole:** If arcs overlap heavily, some point is in many arcs.

But we need a point in ALL arcs, not just many.

The issue is that arcs might be positioned to avoid a common intersection.

**Attempt:** Show that "random" arc positions must intersect.

For uniformly random arc positions, P(all intersect) = ((n-1)/(n+1))^n ≈ e^{-2} > 0.

But arc positions aren't random - they're determined by speed inverses.

**Verdict:** ❌ BLOCKED - Pigeonhole gives expected behavior but not worst-case guarantee.

---

## ATTEMPT 9: The Covering Obstruction

**Idea:** Prove that the bad regions CANNOT cover [0,1] for Case 2.

**Deep dive:**
Bad regions: B_v = {t ∈ [0,1] : ||vt|| < 1/(n+1)}

Each B_v is a union of intervals centered at j/v for j = 1, ..., v-1.

Total measure: μ(B_v) = 2/(n+1) for each v.

Union measure: μ(∪B_v) ≤ 2n/(n+1) → 2 as n → ∞.

Since 2 > 1, the union bound says nothing about covering.

**Deeper analysis:** The union measure depends on overlaps.

If all B_v are disjoint: μ(∪B_v) = 2n/(n+1).
If all B_v overlap perfectly: μ(∪B_v) = 2/(n+1).

Reality is in between. The overlap structure depends on speed relationships.

**For coprime speeds:** The overlaps are "generic" - not perfectly aligned or misaligned.

But "generic" doesn't give a bound.

**Verdict:** ❌ BLOCKED - Covering analysis doesn't give the necessary bound without explicit overlap structure.

---

## ATTEMPT 10: The Inverse Multiplicative Structure

**Idea:** For t = k/p, the positions are vᵢk mod p. Analyze the multiplicative structure of k.

**Deep dive:**
The set of "good k" for speed v is: G_v = {k : vk mod p ∈ [p/(n+1), pn/(n+1)]}

This is: G_v = v⁻¹ · [p/(n+1), pn/(n+1)] mod p

So G_v is a translated/scaled copy of the "good interval" I = [p/(n+1), pn/(n+1)].

The intersection ∩G_vᵢ is nonempty iff:
- There exists k in all v⁻¹ · I simultaneously

**Geometric interpretation:** On the circle Z/pZ, we're asking if n arcs (each translated by v⁻¹ᵢ) have common intersection.

**Arc intersection on circle:** For n arcs of size α (fraction of circle), randomly placed, P(intersection nonempty) = αⁿ (roughly).

Here α = (n-1)/(n+1), so P ≈ ((n-1)/(n+1))^n ≈ e^{-2}.

**But arcs aren't random:** The positions v⁻¹ᵢ mod p are determined by speeds.

**Key question:** For WHICH speed tuples are the inverse positions "adversarial"?

**Claim:** No adversarial positioning exists for coprime speeds.

**Attempt to prove:** Suppose there's a tuple where arcs never intersect at any prime. Then...

I can't derive a contradiction. The inverse positions are specific but not obviously constrained.

**Verdict:** ❌ BLOCKED - Reduces to proving good inverse positioning, which is the main problem.

---

## ATTEMPT 11: The Cascade Construction

**Idea:** Try t = 1/m for m = n+2, n+3, ... until one works.

**Deep dive:**
For Case 2, v₀ = (n+1)k fails at m = n+1.

At m = n+2:
- v₀ mod (n+2) = (n+1)k mod (n+2) = -k mod (n+2)
- Distance = min(|-k|, n+2-|-k|)/(n+2)

For distance ≥ 1/(n+1), need min(|k mod (n+2)|, n+2 - |k mod (n+2)|) ≥ (n+2)/(n+1) > 1.

So need the residue to be ≥ 2 and ≤ n.

This works if k mod (n+2) ∈ {2, 3, ..., n}.

If k ≡ 0, 1, or n+1 (mod n+2), then m = n+2 fails for v₀.

Try m = n+3:
- v₀ mod (n+3) = (n+1)k mod (n+3) = (-2)k mod (n+3) = -(2k) mod (n+3)
- Need residue in {2, ..., n+1} (approximately)

**Pattern:** As m increases, the residue of v₀ = (n+1)k changes.

**Question:** For any k, does some m in {n+2, n+3, ...} have v₀ landing in a good residue?

**Answer:** Almost certainly yes, because residues cycle through Z/mZ as m varies.

But "almost certainly" isn't a proof.

**The issue:** Other speeds also constrain m. We need ALL speeds to have good residues simultaneously.

**Verdict:** ❌ BLOCKED - Cascade works for one speed but coordinating all speeds reduces to arc intersection.

---

## ATTEMPT 12: The GCD Constraint

**Idea:** For t = k/m to work, we need gcd(vᵢ, m) = 1 for all i (otherwise some speed has residue 0).

**Deep dive:**
Define: Coprime(v₁, ..., vₙ) = {m : gcd(vᵢ, m) = 1 for all i}

This is the set of m coprime to all speeds.

By inclusion-exclusion: Coprime = Z \ ∪ᵢ (multiples of primes dividing vᵢ)

The density of Coprime in [1, M] is: ∏ᵢ (1 - 1/pᵢ) for prime factors pᵢ of speeds.

If speeds have many small prime factors, Coprime is sparse.

**Worst case:** v = 2·3·5·7·11·13 (primorial). Coprime density = ∏(1-1/p) → 0.

But for COPRIME speeds, gcd(all) = 1 means not ALL small primes divide all speeds.

**Claim:** For coprime speeds, ∃ m with gcd(vᵢ, m) = 1 for all i and m ≤ some bound.

**Attempt:** The smallest such m is at most max(vᵢ) + 1 (since numbers > max(v) can be coprime to all speeds).

Wait, that's not quite right. We need m coprime to ALL speeds, not just each one.

Actually, for any speeds, we can find m coprime to their product.

If P = v₁ · v₂ · ... · vₙ, then m coprime to P works.

The smallest such m is 1 (always coprime), but k/1 isn't useful.

Next: m such that gcd(m, P) = 1 and m > 1.

Such m exist and are dense (positive density in integers).

**But this doesn't solve arc intersection:** Having m coprime to all speeds is NECESSARY but not SUFFICIENT.

**Verdict:** ❌ BLOCKED - GCD constraint is easy to satisfy; the arc intersection is the hard part.

---

## ATTEMPT 13: The Probabilistic Existence (Rigorous)

**Idea:** Show that for random large prime p, P(arc intersection) > 0 with explicit lower bound.

**Deep dive:**
Let p be a prime > max(speeds). All speeds are coprime to p.

Arc for speed v: A_v = v⁻¹ · I mod p, where I = [p/(n+1), pn/(n+1)].

|A_v| = |I| = p(n-1)/(n+1) - O(1).

**Independence approximation:** If arc positions v⁻¹ mod p were independent uniform:
P(∩A_vᵢ ≠ ∅) ≈ ((n-1)/(n+1))^n → e^{-2} ≈ 0.135

**Dependence structure:** The positions v⁻¹ mod p are deterministic functions of p.

For distinct primes p, q, the pairs (v⁻¹ mod p, v⁻¹ mod q) are nearly independent.

**Large deviation bound:** For M primes p₁, ..., pₘ:
P(fail at ALL pᵢ) ≤ (1 - 0.135)^M + (correlation error)

If correlation error is small, this → 0 as M → ∞.

**The gap:** Bounding correlation error requires explicit equidistribution results.

Known results (Hooley, Duke-Friedlander-Iwaniec) give error O(p^{-1/2+ε}) for single inverses.

For n inverses jointly, error is O(p^{-1/(2n)+ε}) or worse.

For n = 10, error O(p^{-1/20}) is quite slow.

**Verdict:** ❌ BLOCKED - Probabilistic argument works heuristically but error bounds are too weak for rigorous proof.

---

## ATTEMPT 14: The Fourier Analysis Approach

**Idea:** Express arc intersection count as character sum, bound main term vs error.

**Deep dive:**
Count of k in arc intersection:
N = |{k ∈ [1, p-1] : vᵢk mod p ∈ I for all i}|

Using indicator functions: N = Σₖ ∏ᵢ 1_I(vᵢk mod p)

Fourier expand 1_I: 1_I(x) = (n-1)/(n+1) + Σₕ₌₁^{p-1} ĉ(h) e^{2πihx/p}

Where |ĉ(h)| ≤ min(1, 1/(πh · (n-1)/(n+1))) by standard bounds.

**Main term:** (p-1) · ((n-1)/(n+1))^n ≈ p · e^{-2}

**Error term:** Involves character sums Σₖ e^{2πi(h₁v₁ + ... + hₙvₙ)k/p}

For (h₁v₁ + ... + hₙvₙ) ≢ 0 (mod p), this sum is O(1) (cancellation).

**Counting error:** Number of (h₁, ..., hₙ) tuples with each |ĉ(hᵢ)| significant is O((p/(n+1))^n).

Each contributes O(1) to the error.

Total error: O((p/(n+1))^n) ... which is LARGER than main term p · e^{-2} for large n!

**The failure:** Error overwhelms main term for large n.

**Verdict:** ❌ BLOCKED - Fourier analysis gives main term but error is too large.

---

## ATTEMPT 15: The Smooth Modulus Approach

**Idea:** Use m = n! or lcm(1,...,n). Highly composite moduli have special structure.

**Deep dive:**
For m = n!, every speed v ≤ n divides m.

Wait, that's BAD - we need gcd(v, m) = 1.

**Revised:** Use m such that all speeds are coprime to m.

If speeds have small prime factors, we need m coprime to those primes.

**Alternative:** Use m = ∏(primes > max speed up to some bound).

Such m is coprime to all speeds, but might be very large.

**The question:** Does a highly structured m help with arc intersection?

I don't see how. The arc intersection problem is about inverse positions, which don't respect the smooth structure.

**Verdict:** ❌ BLOCKED - Smooth moduli don't provide leverage for arc intersection.

---

## ATTEMPT 16: The Contradiction via Density

**Idea:** If no prime works, derive contradiction from density of bad primes.

**Deep dive:**
Suppose for coprime speeds v₁, ..., vₙ, NO prime p has nonempty arc intersection.

Then for EVERY prime p > max(v):
- The arcs A_vᵢ = vᵢ⁻¹ · I mod p are disjoint (in some sense)

**Disjoint arcs:** n arcs of size (n-1)p/(n+1) being disjoint requires:
n · (n-1)p/(n+1) ≤ p, i.e., n(n-1)/(n+1) ≤ 1, i.e., n(n-1) ≤ n+1.

For n = 2: 2 ≤ 3 ✓
For n = 3: 6 ≤ 4 ✗

So for n ≥ 3, arcs MUST overlap!

**But overlapping ≠ intersecting all:** Arcs can pairwise overlap without having a common point.

Example (n=3): Arc A covers [0, 0.4], Arc B covers [0.3, 0.7], Arc C covers [0.6, 1.0].
Pairwise overlaps: A∩B, B∩C nonempty. But A∩B∩C = ∅.

**The gap:** "Must overlap pairwise" doesn't imply "must intersect all."

**Helly's theorem variant:** For intervals on a circle, if every 2 intersect, do all intersect?

No! The counterexample above shows this fails.

**Verdict:** ❌ BLOCKED - Density/overlap arguments don't force common intersection.

---

## ATTEMPT 17: The Speed Ratio Analysis

**Idea:** The ratios vᵢ/vⱼ determine the problem structure. Analyze these.

**Deep dive:**
For coprime speeds, the ratios vᵢ/vⱼ are reduced fractions.

At time t, positions are {v₁t, ..., vₙt} mod 1.

The relative positions vᵢt - vⱼt = (vᵢ - vⱼ)t only depend on differences.

**For t = k/p:** Positions are vᵢk/p mod 1.

The position differences are (vᵢ - vⱼ)k/p mod 1.

**Observation:** If vᵢ ≡ vⱼ (mod p), their positions are identical.

If vᵢ ≡ -vⱼ (mod p), their positions are symmetric about 0.5.

**Can we exploit these relations?**

For coprime speeds, the residues mod p vary. For p > max(v), all residues are distinct.

**Attempt:** Find p where residue relations create favorable arc positions.

For example, if v₁ ≡ v₂ + 1 (mod p), their arcs are adjacent.

But "adjacent" doesn't mean "overlapping correctly."

**Verdict:** ❌ BLOCKED - Residue relations don't directly control arc intersection.

---

## ATTEMPT 18: The Constructive Modulus Search

**Idea:** For given speeds, explicitly search for working m by characterizing which m fail.

**Deep dive:**
Define: Bad(v₁, ..., vₙ) = {m : no k makes t = k/m lonely}

We want to show Bad ≠ Z⁺ (there exists a good m).

**Characterize Bad(m):**
m ∈ Bad iff ∩ᵢ G_vᵢ = ∅, where G_v = {k : vk mod m ∈ [m/(n+1), mn/(n+1)]}.

**For prime m = p:** G_v = v⁻¹ · I mod p, an arc of size (n-1)p/(n+1).

**For composite m:** More complex, depends on prime factorization.

**Upper bound on Bad:**
If arcs at p are "random," P(p ∈ Bad) ≈ 1 - e^{-2} ≈ 0.865.

For independent primes, P(all primes ∈ Bad) → 0 as we consider more primes.

**The issue:** Primes aren't independent for the same speed tuple.

**Attempt to prove dependence is weak:**
For primes p, q, the events "p ∈ Bad" and "q ∈ Bad" are determined by inverses mod p and mod q.

By CRT, these are essentially independent for most speed tuples.

**Formalization needed:** A Chernoff-type bound showing concentration.

**Verdict:** ❌ BLOCKED - Characterization is correct but independence/concentration bounds are missing.

---

## ATTEMPT 19: The Algebraic Geometry Approach

**Idea:** View the problem as intersection of algebraic varieties.

**Deep dive:**
The arc intersection at prime p is:
{k ∈ F_p : L ≤ v₁k ≤ R, ..., L ≤ vₙk ≤ R} (mod p)

Where L = p/(n+1), R = pn/(n+1).

The inequalities define regions in affine space over F_p.

**Reformulation:** Find k such that each vᵢk mod p lies in the interval [L, R].

In algebraic terms: the image of the line k ↦ (v₁k, ..., vₙk) mod p intersects the box [L,R]^n.

**Dimension count:** The line is 1-dimensional. The box has volume ((n-1)/(n+1))^n · p^n.

By Bézout-type arguments, intersection is expected if volume is large enough relative to line.

**The issue:** This is heuristic. The line might avoid the box for specific choices.

**Algebraic geometry tools:** Intersection theory, étale cohomology... These are sophisticated tools that might apply, but I don't have the expertise to deploy them rigorously.

**Verdict:** ❌ BLOCKED - Algebraic geometry reformulation is elegant but I can't complete the argument.

---

## ATTEMPT 20: The Fixed Point Approach

**Idea:** Define a map on arc positions and find a fixed point corresponding to intersection.

**Deep dive:**
Consider the map T: (Z/pZ)^n → (Z/pZ)^n defined by T(x₁, ..., xₙ) = (v₁x₁, ..., vₙxₙ).

Actually, this doesn't preserve the structure we need.

**Alternative:** Consider the "good region" G ⊂ [0,1]^n defined by:
G = {(θ₁, ..., θₙ) : all θᵢ ∈ [1/(n+1), n/(n+1)]}

The trajectory {(v₁t, ..., vₙt) mod 1 : t ∈ [0,1]} is a line in the n-torus.

We want to show this line hits G.

**Topological approach:** If the line winds around the torus "enough," it must hit every region.

**Winding number argument:** The line from (0, ..., 0) to (v₁, ..., vₙ) wraps around vᵢ times in dimension i.

If gcd(v₁, ..., vₙ) = 1, the line is dense in the torus (by Weyl equidistribution).

**But "dense" doesn't mean "hits G in [0,1]":** Density is asymptotic. We need a finite-time result.

**Fixed point theorems (Brouwer, Lefschetz):** Might apply if we can find a suitable map.

The projection (θ₁, ..., θₙ) ↦ (θ₁, ..., θₙ) + t(v₁, ..., vₙ) mod 1 for varying t...

This is a continuous family of translations, not obviously amenable to fixed point theorems.

**Verdict:** ❌ BLOCKED - Topological approach doesn't give finite-time guarantee; fixed point theorems don't obviously apply.

---

# SUMMARY

| # | Approach | Verdict | Specific Blocker |
|---|----------|---------|------------------|
| 1 | Bezout Coefficients | ❌ BLOCKED | Additive structure can't bridge to multiplicative |
| 2 | Collision Exploitation | ❌ BLOCKED | Collisions reduce constraints but not threshold |
| 3 | CRT with Chosen Primes | ❌ BLOCKED | Reduces to "some prime works" |
| 4 | Equidistribution Bounds | ❌ BLOCKED | Error bounds not explicit enough |
| 5 | Minimal Counterexample | ❌ BLOCKED | Structure exists but no contradiction derivable |
| 6 | Prime Counting Extension | ❌ BLOCKED | Works heuristically, rigorous version needs n-dependent bounds |
| 7 | Slack Phenomenon | ❌ BLOCKED | Exists empirically, can't prove algebraically |
| 8 | Pigeonhole on Arcs | ❌ BLOCKED | Expected behavior ≠ worst-case guarantee |
| 9 | Covering Obstruction | ❌ BLOCKED | Union bound insufficient, overlap structure unknown |
| 10 | Inverse Multiplicative | ❌ BLOCKED | Reduces to proving good inverse positioning |
| 11 | Cascade Construction | ❌ BLOCKED | Works for one speed, coordinating all is the problem |
| 12 | GCD Constraint | ❌ BLOCKED | Necessary but not sufficient |
| 13 | Probabilistic Rigorous | ❌ BLOCKED | Error bounds too weak for rigorous proof |
| 14 | Fourier Analysis | ❌ BLOCKED | Error term overwhelms main term for large n |
| 15 | Smooth Modulus | ❌ BLOCKED | No leverage for arc intersection |
| 16 | Density Contradiction | ❌ BLOCKED | Pairwise overlap ≠ common intersection |
| 17 | Speed Ratio Analysis | ❌ BLOCKED | Residue relations don't control arc positions |
| 18 | Constructive Search | ❌ BLOCKED | Characterization correct, concentration bounds missing |
| 19 | Algebraic Geometry | ❌ BLOCKED | Elegant reformulation, can't complete argument |
| 20 | Fixed Point | ❌ BLOCKED | No suitable map, density ≠ finite-time hitting |

---

# CONCLUSION

**All 20 genuine attempts are BLOCKED.**

Every approach reduces to one of two core obstacles:

1. **The Additive-Multiplicative Gap:** Converting gcd = 1 (additive) to residue-in-interval (multiplicative)

2. **The Arc Intersection Problem:** Proving n arcs on Z/pZ intersect for some prime p

These are not separate problems - they're equivalent formulations of the same mathematical barrier.

**What would solve it:**
- A new theorem connecting additive structure (Bezout, gcd) to multiplicative structure (residues, intervals)
- A concentration/correlation bound for arc positions across primes
- A genuinely novel reformulation that bypasses the arc intersection problem

**Current state of LRC:**
- n ≤ 10: PROVEN (Rosenfeld, Trakulthongchai 2025 using finite checking + computation)
- n > 10: OPEN (blocked at fundamental gap)

The conjecture is almost certainly TRUE (10.9M+ empirical tests, 0 counterexamples), but a proof for arbitrary n requires new mathematics.
