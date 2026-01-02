# Lonely Runner Conjecture: Proof Structure

## Theorem

For any n distinct positive integers v₁ < v₂ < ... < vₙ with gcd(v₁, ..., vₙ) = 1, there exists t > 0 such that ||vᵢt|| ≥ 1/(n+1) for all i.

## Key Insight: Two Cases Based on Residues mod (n+1)

### Case 1: No speed v ≡ 0 (mod n+1)

**Claim:** t = 1/(n+1) satisfies LRC.

**Proof:**
At t = 1/(n+1), runner with speed v has position:
- vt = v/(n+1) (mod 1)
- Distance = ||v/(n+1)|| = min(v mod (n+1), (n+1) - (v mod (n+1))) / (n+1)

Since v ≢ 0 (mod n+1), we have v mod (n+1) ∈ {1, 2, ..., n}.

Let r = v mod (n+1). The numerator is min(r, n+1-r).
- If r ∈ {1, 2, ..., ⌊n/2⌋}: min = r ≥ 1
- If r ∈ {⌈(n+1)/2⌉, ..., n}: min = n+1-r ≥ 1

In all cases, the distance is ≥ 1/(n+1). ∎

### Case 2: Some speed v ≡ 0 (mod n+1)

When some v = k(n+1), t = 1/(n+1) fails (that speed lands at origin).

**Observed behavior (computational):**
- Every tested tuple with v ≡ 0 (mod n+1) has ML > 1/(n+1)
- A different lonely time works
- Examples:
  - (1, 2, 4): ML = 1/3 at t = 1/3
  - (1, 2, 5, 6): ML = 2/7 at t = 2/7
  - (1, 4, 5, 10): ML = 1/3 at t = 1/3

**What needs to be proven:**
For any coprime tuple with some v ≡ 0 (mod n+1), there exists t with ||vᵢt|| ≥ 1/(n+1) for all i.

---

## Tight Cases Analysis

A tuple is "tight" if ML = 1/(n+1) exactly (no slack).

### Computational Finding

Tight coprime tuples include:
- (1, 2, 3): ML = 1/4 at t = 1/4
- (1, 2, 3, 4): ML = 1/5 at t = 1/5
- (1, 3, 4, 7): ML = 1/5 at t = 1/5
- (1, 3, 4, 5, 9): ML = 1/6 at t = 1/6

**Pattern observed:**
- All tight cases have no v ≡ 0 (mod n+1)
- All tight cases achieve optimum at t = 1/(n+1)
- Tight cases all contain 1 and some w with 1 + w = n+1 (where w ∈ {n} or w lands correctly)

### Key Observation

When some v ≡ 0 (mod n+1):
- t = 1/(n+1) fails → FORCES different optimal t
- Different t typically gives slack → ML > 1/(n+1)

This explains why Case 2 tuples have slack.

---

## Complete Proof Strategy

### Step 1: Establish Case 1 (DONE)
For tuples with no v ≡ 0 (mod n+1), t = 1/(n+1) works directly.

### Step 2: Prove Case 2
**Approach A: Show slack exists**
Prove that if some v ≡ 0 (mod n+1), then ML > 1/(n+1).

**Approach B: Construct alternative t**
For v = k(n+1), find t such that:
- k(n+1)·t is far from integers
- All other speeds also have distance ≥ 1/(n+1)

**Approach C: Use equidistribution**
Show that for large primes p, the arc intersection at k/p achieves ML ≥ 1/(n+1).

---

## Gap to Close

The main open problem: **Prove Case 2 algebraically.**

Either:
1. Prove every coprime tuple with v ≡ 0 (mod n+1) has ML > 1/(n+1), OR
2. Construct explicit t for such tuples, OR
3. Use number-theoretic methods (primes, equidistribution) to show t exists

---

## Working Hypothesis

**Conjecture (Residue Dichotomy):**
- If no v ≡ 0 (mod n+1): ML ≥ 1/(n+1) via t = 1/(n+1)
- If some v ≡ 0 (mod n+1): ML > 1/(n+1) via different t

This would complete the proof since both cases imply LRC.

---

## Coverage Analysis Insights

For each speed v, define bad region B_v = {t : ||vt|| < 1/(n+1)}.
LRC ⟺ ∪_v B_v ≠ [0,1], i.e., bad regions don't cover [0,1].

**Empirical findings:**
| Tuple | Good Region % | Type |
|-------|--------------|------|
| (1,2,3) | ~0.1% | Case 1 (tight) |
| (1,2,4) | ~12.6% | Case 2 (slack) |
| (1,2,5,6) | ~12.0% | Case 2 (slack) |
| (2,3,5) | ~5.2% | Case 1 (slack) |

**Key observation:** Case 2 tuples have much larger good regions than Case 1 tight tuples.
This suggests that the "obstruction" at t = 1/(n+1) for Case 2 creates slack elsewhere.

---

## Summary

1. **Case 1 is fully proven:** For tuples with no v ≡ 0 (mod n+1), t = 1/(n+1) satisfies LRC.

2. **Case 2 is empirically verified:** All tested tuples with v ≡ 0 (mod n+1) have ML > 1/(n+1).

3. **Algebraic gap:** Need formal proof that Case 2 tuples have ML ≥ 1/(n+1).

**Potential approaches for Case 2:**
- Diophantine approximation to find suitable m with gcd(v_i, m) = 1 for all i
- Covering congruence arguments
- Prime arc intersection with equidistribution

---

*Status: Case 1 complete. Case 2 empirically verified, algebraic proof open.*
*Round 4 deep attack in progress.*
