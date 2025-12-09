# Don't Try This - Failed Approaches

**READ THIS BEFORE STARTING ANY NEW APPROACH**

These have been tried and don't work. Don't waste time rediscovering why.

---

## The Five Fundamental Failure Modes

| Mode | What It Looks Like | Why It Fails |
|------|-------------------|--------------|
| **"Almost All"** | Prove for density-1 set | Measure zero ≠ empty. Collatz needs ALL. |
| **Wrong Space** | Extend to 2-adics Z₂ | Z₂ has cycles that Z⁺ doesn't. Results don't transfer. |
| **Local → Global** | Prove for k steps, extend | Can't extend finite bounds to infinity. |
| **Mixing Assumption** | Use equidistribution | Division by 2^T destroys modular structure. |
| **Reformulation** | Find equivalent problem | Still equally hard, just different words. |

---

## Specific Failed Attempts

### For Cycles (Now Solved Anyway)

| Attempt | Why It Failed |
|---------|---------------|
| Coprimality analysis | gcd(S/g, D/g) = 1 is a tautology (always true) |
| p-adic valuations alone | v_p(S) vs v_p(D) doesn't constrain divisibility |
| Modular arithmetic (mod p, p≥5) | No clean pattern emerges |

### For Divergence (Still Relevant!)

| Attempt | Why It Failed |
|---------|---------------|
| **Simple Lyapunov L(n) = log(n)** | Can increase on individual steps |
| **Lyapunov L(n) = n^α** | Same problem - no α works |
| **Lyapunov L(n) = log(n)/T(n)** | Doesn't decrease monotonically |
| **Direct probabilistic** | Proves expected behavior, not worst-case |
| **Gambler's ruin analogy** | Works for random, fails for deterministic |
| **TB2 bound (T_max ≤ log₂n + 2)** | FALSE - counterexample at n ≈ 2^{482} |
| **Clean k / fake cycle approach** | Mod 2^k dynamics ≠ actual values (see below) |

---

## The "Clean k" / Fake Cycle Approach (Near Miss)

**The approach**:
1. Define "clean k" where all odd residues mod 2^k reach class 1 under Syracuse
2. Show clean k values are dense (gaps ≤ 4, verified to k = 100)
3. For any n, choose clean k > log₂(n)
4. Trajectory mod 2^k reaches class 1, then descends

**Why it ALMOST works**:
- Computationally verified: clean k's exist at most 4 apart
- Class 1 descent IS algebraically proven: v ≡ 1 (mod 4), v > 1 ⟹ S(v) < v
- Fake cycles only at k ∈ {10, 11, 12, 20} for k ≤ 100

**Why it FAILS**:
- "Trajectory reaches class 1 mod 2^k" is about RESIDUES
- The ACTUAL VALUES could grow unboundedly before reaching that residue
- The assumption "Let v be the first value with v ≡ 1 (mod 2^k)" presumes bounded growth
- This is the probabilistic → deterministic gap in disguise

**Classification**: Local → Global failure mode. Mod 2^k dynamics don't control actual values.

---

## Specific Bounds That Are FALSE

| Claim | Status | Counterexample |
|-------|--------|----------------|
| T_max(n) ≤ log₂(n) + 2 | **FALSE** | n ≈ 2^{482.5}, j = 485 |
| BL2: T(landing) ≤ constant | **FALSE** | Can be arbitrarily high |

---

## Why Tao's Method Can't Complete

Tao (2019) proved "almost all Collatz orbits attain almost bounded values."

**Why it can't prove "all"**:
- Uses logarithmic density arguments
- Applies to density-1 set only
- The "exceptional set" (measure zero) could still be infinite
- No known way to eliminate the exceptional set

**Don't try**: Extending Tao's method to cover all cases. The gap is fundamental.

---

## Why 2-Adic Methods Don't Transfer

Results in Z₂ (2-adic integers) don't imply results in Z⁺ because:
- Z₂ contains "negative" 2-adic integers
- The Collatz map has cycles in Z₂ that don't exist in Z⁺
- Convergence in 2-adic metric ≠ convergence in usual metric

**Don't try**: Proving things in Z₂ and claiming they hold for positive integers.

---

## Why Automata Theory Doesn't Help

Conway (1972) proved that generalized Collatz-type functions are Turing-complete.

**Implication**: No algorithm can decide convergence for ALL such functions.

**However**: This doesn't prove Collatz itself is undecidable. It might have special structure that makes it decidable.

**Don't try**: Claiming undecidability proves Collatz is unprovable. That's not what Conway showed.

---

## The Core Obstacle

**Every approach hits the same wall**:

> Converting probabilistic/typical behavior to deterministic/worst-case proofs

The probabilistic model says trajectories should contract. The gap is proving that deterministic trajectories CAN'T "stay lucky" forever.

**This is not a bug in the approaches - it's THE hard part of Collatz.**

---

## What MIGHT Work (But Hasn't Yet)

| Approach | Status | Why It Might Work |
|----------|--------|-------------------|
| Block-Escape exclusion | Near-complete (claimed) | Spectral bounds create contradictions |
| Functional equations | Reformulation done | Well-posed complex analysis problem |
| Renewal theory | Partial | If mixing can be proven deterministically |

---

## Before Trying Something New

Ask yourself:
1. Does this fall into one of the five failure modes?
2. Has something similar been tried? (Check this file)
3. Does it handle the probabilistic→deterministic gap?
4. Does it actually prove for ALL n, not just "almost all"?

If you can't answer "no, yes, yes, yes" - it probably won't work.

---

**Last Updated**: December 2024
