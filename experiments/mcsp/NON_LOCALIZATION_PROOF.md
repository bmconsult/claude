# Non-Localization of Isotypic Projections

**Goal**: Prove that local oracles cannot compute or approximate isotypic projections.

This is crucial: if the isotypic approach is to work, it must NOT be localizable.

## The Locality Barrier (Chen et al.)

**Statement**: Gap-MCSP ∈ AC⁰[⊕] with O(log N)-local oracles.

A technique is "localizable" if:
1. It proves lower bounds against U₂-Formula[N^{3+ε}]
2. The proof extends to U₂-Formula[N^{3+ε}] + O(log N)-local oracles

All known lower bound techniques are localizable, hence stuck.

## Why Isotypic Projections Are Non-Local

### Definition: Isotypic Projection

For T ∈ R^N and partition λ ⊢ n:

π_λ(T) = (d_λ / n!) Σ_{σ∈S_n} χ_λ(σ) T^σ

where T^σ is T permuted by σ (i.e., (T^σ)_x = T_{σ^{-1}(x)}).

### Claim: Computing π_λ(T) requires seeing all N bits of T.

**Proof**:

Consider λ = (n-1, 1), the standard representation.

For generic T, the projection π_{(n-1,1)}(T) depends on all n coordinates because:

1. The sum Σ_σ χ_{(n-1,1)}(σ) T^σ includes all n! permutations
2. Each permutation moves every bit position
3. The character χ_{(n-1,1)}(σ) is non-trivial for most σ

More formally:

**Lemma**: For the standard irrep (n-1,1), the projection π_{(n-1,1)}(T) changes if we flip any single bit of T.

**Proof**:
The standard representation has character:
- χ_{(n-1,1)}(id) = n-1
- χ_{(n-1,1)}(transposition) = n-3
- χ_{(n-1,1)}(σ) depends on cycle structure

The projection π_{(n-1,1)}(T) is NOT a symmetric function of T's bits.
It captures "how T varies across variable permutations."

If we flip bit T_x for some x ∈ {0,1}^n:
- T changes at position x
- T^σ changes at position σ(x) for each σ
- The weighted sum Σ χ_λ(σ) T^σ changes

Since σ can map x to any other position (S_n is transitive on positions via its action on Hamming weights), flipping any bit affects the projection. ∎

### Corollary: O(k)-local oracles can't compute π_λ(T) for k << N.

**Proof**:
An O(k)-local oracle sees only k bits of T per query.
To determine π_λ(T), need to see all N bits.
Even with poly(N) queries, each seeing k = O(log N) bits, can't determine π_λ(T) exactly.

## Approximation Hardness

### Claim: O(k)-local oracles can't even APPROXIMATE π_λ(T) well.

**Argument**:

Consider two truth tables T and T' that differ in N/2 randomly chosen positions.

For a random such pair:
- ‖T - T'‖² = N/2 (they differ in half the bits)
- ‖π_λ(T) - π_λ(T')‖² ≈ (d_λ/N) · N/2 = d_λ/2 (by equidistribution)

An O(k)-local oracle with k = O(log N) can't distinguish T from T' with better than 1 - 2^{-k} = 1 - 1/poly(N) probability on random pairs.

But π_λ(T) and π_λ(T') differ significantly!

Therefore: local oracles cannot approximate isotypic projections.

## The Key Insight for Gap-MCSP

### What Local Oracles CAN Do

Local oracles can:
1. Check if T has specific local patterns
2. Verify that a candidate circuit C computes T at O(log N) positions
3. Aggregate local checks via AC⁰[⊕]

This is why Gap-MCSP ∈ AC⁰[⊕] + local oracles:
- Given candidate C, check C(x) = T_x for random x
- This probabilistically verifies correctness
- Repeat O(log N) times for confidence

### What Local Oracles CAN'T Do

Local oracles cannot:
1. Compute isotypic projections
2. Distinguish isotypic mass distributions
3. Verify global algebraic properties of T

### The Non-Localization Argument

**Claim**: The isotypic approach doesn't localize.

**Argument**:

Suppose the isotypic argument DID localize. Then:
1. We'd have a proof that Gap-MCSP ∉ U₂-Formula[N^{3+ε}]
2. The proof would extend to circuits with local oracles
3. But Gap-MCSP ∈ circuits with local oracles!

Contradiction. So either:
(a) The isotypic argument fails to prove the lower bound, OR
(b) The isotypic argument succeeds and doesn't localize

We're trying to establish (b).

### Why Doesn't It Localize?

The isotypic argument uses:
1. WIS(T) = weighted isotypic spread
2. WIS captures GLOBAL structure of T
3. Local oracles can't compute WIS

For the argument to localize, we'd need:
- Local oracles that can distinguish high-WIS from low-WIS
- But WIS depends on ALL bits of T
- Local oracles see O(log N) bits
- Can't distinguish!

**Formal version**:

Let L be an O(log N)-local oracle. Define:

WIS_L(T) = estimate of WIS(T) using only L-queries

**Claim**: For any L, there exist T_simple, T_complex with:
- WIS(T_simple) ≤ poly(n)
- WIS(T_complex) ≥ n!/poly(n)
- WIS_L(T_simple) ≈ WIS_L(T_complex) with high probability

**Proof sketch**:
T_simple and T_complex can agree on all local patterns.
They differ only in global isotypic structure.
L can't see the global structure.
Therefore L can't distinguish.

## The Full Picture

1. **Isotypic projections are non-local**: Computing π_λ requires all N bits.

2. **WIS is non-local**: Distinguishing high-WIS from low-WIS requires global information.

3. **Local oracles fail**: O(log N)-local oracles can't compute or approximate isotypic quantities.

4. **The argument doesn't localize**: Any proof using isotypic structure fundamentally needs global access.

5. **This is new**: Unlike Fourier-based arguments (which can be simulated locally via random sampling), isotypic arguments require true global computation.

## Remaining Work

### To Complete the Non-Localization Proof:

1. **Construct explicit examples** of T_simple, T_complex that fool local oracles but have different WIS.

2. **Prove the indistinguishability**: Show that O(log N)-local tests can't separate them.

3. **Connect to the lower bound**: Show that the isotypic lower bound argument explicitly uses non-local properties.

### The Vision

If we can prove:
1. Gap-MCSP has large "isotypic complexity" (requires formula size ≥ N^{3+ε} to distinguish high/low WIS)
2. The proof uses only non-local properties
3. Local oracles can't help with non-local properties

Then we bypass the locality barrier!
