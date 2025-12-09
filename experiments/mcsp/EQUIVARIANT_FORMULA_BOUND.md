# Equivariant Formula Lower Bounds

**New Angle**: Gap-MCSP is S_n-invariant. Any formula computing it can be "averaged" to an S_n-equivariant formula.

## Setup

Gap-MCSP: {0,1}^N → {0,1} where N = 2^n

**Property**: Gap-MCSP is S_n-invariant:
- For all σ ∈ S_n and all truth tables T: Gap-MCSP(σT) = Gap-MCSP(T)

This is because circuit complexity doesn't change under variable permutation.

## The Averaging Argument

### Claim: If F computes Gap-MCSP with formula size s, then there exists an S_n-equivariant F̄ computing Gap-MCSP with formula size ≤ n! · s.

**Proof**:
Define F̄(T) = majority{F(σT) : σ ∈ S_n}

Wait, this doesn't work directly for Boolean formulas...

Actually, we need a different approach.

### Better Formulation

Since Gap-MCSP is S_n-invariant, it factors through the orbit space:

Gap-MCSP: {0,1}^N → {0,1} factors as:

{0,1}^N → Orbits → {0,1}

where Orbits = {0,1}^N / S_n.

The number of orbits is approximately 2^N / n! (by orbit-counting formula).

**Claim**: Any function f: Orbits → {0,1} lifts to F: {0,1}^N → {0,1} with formula size at most (formula size of f on orbits) × (cost of orbit identification).

**The key question**: What's the formula complexity of "orbit identification"?

## Orbit Identification Complexity

To identify which orbit a truth table T belongs to, we need an orbit-invariant.

### Approach 1: Canonical Representative

Find canonical representative of each orbit (e.g., lexicographically smallest element).

But computing the canonical representative of an S_n-orbit requires comparing n! permuted versions - NOT efficient for formulas!

### Approach 2: Orbit Invariants

Use S_n-invariant functions to distinguish orbits:

1. **Hamming weight distribution**: w_k(T) = #{x : |x| = k, T(x) = 1}
   - This gives (n+1) values
   - Two orbits can share the same Hamming weight distribution!

2. **Fourier level masses**: L_k(T) = Σ_{|S|=k} T̂(S)²
   - Also gives (n+1) values
   - Doesn't distinguish all orbits

3. **Higher-order invariants**: Products, correlations, etc.
   - Need exponentially many to distinguish all orbits

**Claim**: Distinguishing all S_n-orbits requires Ω(2^N / n!) bits of information.

Since there are ~2^N / n! orbits, any formula must compute ~log(2^N / n!) = N - log(n!) bits to identify the orbit.

For n ≥ 20: N - log(n!) ≈ N - n log n ≈ N - n log n

This is still almost N bits!

## The Lower Bound Approach

### Observation 1: Gap-MCSP factors through orbits

Gap-MCSP(T) depends only on which orbit T belongs to.

### Observation 2: Identifying orbits is hard

To distinguish ~2^N / n! orbits requires ~N - n log n bits.

### Observation 3: Formulas have limited "output entropy"

A formula of size s can encode at most s bits of information about its input.

(Actually, a formula computes a single bit, so this isn't directly applicable.)

### Better Approach: Communication Complexity

Think of Gap-MCSP as a promise problem:
- YES: T is in an orbit with complexity ≤ s
- NO: T is in an orbit with complexity ≥ 2s

The formula must distinguish YES orbits from NO orbits.

How many YES orbits are there? How many NO orbits?

**Claim**: The number of YES orbits (low-complexity functions) is poly(N).
**Claim**: The number of NO orbits (high-complexity functions) is ~2^N / n!.

The formula must accept poly(N) orbits and reject ~2^N / n! orbits.

This is like a "set disjointness" or "membership" problem with huge asymmetry.

## Towards a Lower Bound

### The Structure of Low-Complexity Orbits

Truth tables with circuit complexity ≤ s:
- There are at most 2^{O(s log s)} such functions
- They partition into at most 2^{O(s log s)} / 1 orbits (assuming minimal orbit overlap)

So: |YES orbits| ≤ 2^{O(s log s)}

### The Structure of High-Complexity Orbits

Random truth tables have complexity ≈ N / n (by counting).
Almost all truth tables are high-complexity.

Number of orbits ≈ 2^N / n!

Fraction that are YES: 2^{O(s log s)} / (2^N / n!) = 2^{O(s log s)} · n! / 2^N

For s = N^α with α < 1: this fraction is negligible.

### The Formula Challenge

A formula for Gap-MCSP must:
1. Accept truth tables in the ~2^{O(s log s)} YES orbits
2. Reject truth tables in the remaining ~2^N / n! NO orbits

The YES orbits are a tiny fraction of all orbits.

A formula of size S can:
- Compute a single bit
- But that bit must be 1 iff input is in a YES orbit

**Claim**: This requires the formula to "memorize" information about the YES orbits.

**Key Insight**: The YES orbits are not structurally simple from the formula's perspective!

Low-complexity functions aren't "simple" in the sense of having simple formulas over the truth table bits. A function f may have a small circuit, but its truth table T_f doesn't have any obvious formula structure.

### The Counting Argument

For a formula of size s:
- The formula can be in one of 2^{O(s log n)} configurations
- Each configuration computes one function of the N input bits
- The number of computable functions is 2^{O(s log n)}

But Gap-MCSP must distinguish:
- ~2^{O(s log s)} YES inputs (truth tables of low-complexity functions)
- ~2^N NO inputs (truth tables of high-complexity functions)

For the formula to accept exactly the YES inputs:
2^{O(S log n)} ≥ 2^{O(s log s)}  (can compute enough functions)

This gives S ≥ Ω(s log s / log n) = Ω(s)

For the magnification threshold s = N^α:
S ≥ Ω(N^α)

This only gives polynomial lower bounds, not N^{3+ε}!

## Where's the Super-Polynomial?

The counting argument gives only polynomial bounds.

To get N^{3+ε}, we need a different approach:

1. **Communication complexity**: View Gap-MCSP as a communication problem. If Alice has half the truth table and Bob has the other half, how much communication is needed?

2. **Lifting theorems**: Known connections between formula size and communication.

3. **Isotypic restrictions**: The S_n-invariance might allow stronger bounds.

## The Magnification Connection

Magnification says: Gap-MCSP ∉ U₂-Formula[N^{3+ε}] implies P ≠ NP.

The magnification itself relies on specific properties of Gap-MCSP:
- It's in NP (witness is the small circuit)
- It's "complete" in a certain sense
- Weak lower bounds imply strong lower bounds

The N^{3+ε} threshold comes from the specific reduction used in magnification.

**Key point**: We don't need to prove formula size = N^{3+ε}. We need to prove formula size > N^{3-ε} for some ε > 0. The magnification does the amplification.

Wait, let me re-read the magnification result...

From McKay-Murray-Williams (2019):
- If Gap-MKtP ∉ U₂-Formula[N^{3+ε}], then EXP ⊄ NC¹

The threshold N^{3+ε} is EXACTLY what we need - we can't substitute a weaker bound.

## Conclusion

The equivariant approach gives intuition but doesn't directly give N^{3+ε}.

The gap: counting arguments give polynomial bounds, but we need N^{3+ε}.

Possible ways forward:
1. **Communication complexity lifting**: Use known formula-communication connections
2. **Isotypic spectral bounds**: Use the decomposition more carefully
3. **Algebraic metacomplexity translation**: Adapt the Nov 2024 result to Boolean case
