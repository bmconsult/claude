# Communication Complexity Attack on Gap-MCSP

## The Karchmer-Wigderson Connection

### Classical KW Games

For a Boolean function f: {0,1}^n → {0,1}:
- Alice gets x ∈ f⁻¹(1)
- Bob gets y ∈ f⁻¹(0)
- Goal: find i where x_i ≠ y_i

**Theorem (Karchmer-Wigderson 1990)**: D(f) = CC(KW_f), where D(f) = formula depth.

This gives **depth** bounds, not size bounds.

### Gap-MCSP KW Game

For Gap-MCSP on N-bit inputs:
- Alice gets T_A with circuit complexity ≤ s (simple)
- Bob gets T_B with circuit complexity ≥ 2s (complex)
- Goal: find position i where T_A[i] ≠ T_B[i]

**Question**: What is CC(KW_{Gap-MCSP})?

### Analysis

Simple T_A has structure; complex T_B looks random.

**Upper bound on communication**:
- Binary search on positions: O(log N) = O(n) bits
- So CC ≤ n

**Lower bound on communication**:
- If T_A and T_B differ in many positions, easy to find one
- If they differ in few positions, harder

**Key insight**: A simple function and a complex function with the same Hamming weight differ in at least ??? positions.

Actually, they could potentially differ in very few positions! A simple function T_A could differ from complex T_B in just 2 positions (flip one 0→1 and one 1→0), and that could change complexity drastically.

So communication is O(n) but the constant might be important.

## Formula Depth vs Size

KW gives: D(Gap-MCSP) = CC(KW_{Gap-MCSP}) ≈ O(n) = O(log N)

This means Gap-MCSP has formula **depth** O(log N).

What does this say about **size**?

Formula size ≥ formula depth (trivially).
Formula size ≤ 2^{formula depth} (worst case).

So: log N ≤ formula size ≤ N.

This doesn't give tight size bounds.

## Lifting to Get Size Bounds

### The Lifting Paradigm

**Query-to-Communication Lifting** (Göös-Pitassi-Watson et al.):
- If f has decision tree complexity D(f),
- Then f ∘ g (composed with gadget g) has communication complexity ≥ D(f) × CC(g)

This "lifts" query lower bounds to communication lower bounds.

### Can We Lift Gap-MCSP?

To use lifting, we need:
1. Query complexity lower bound on Gap-MCSP
2. A gadget g with high communication complexity
3. Formula lower bound from composed communication complexity

**Step 1**: What's the query complexity of Gap-MCSP?

Deterministic query complexity: To determine if T is simple, you might need to read all N bits.
But Gap-MCSP has a gap, so maybe partial reads suffice?

**Claim**: DT(Gap-MCSP) = Ω(N).

**Proof sketch**:
- A simple T could be changed to complex by modifying O(1) bits
- So you need to read almost all bits to be sure
- Therefore query complexity is Ω(N)

**Step 2**: Lifting

Gap-MCSP ∘ g has communication complexity ≥ N × CC(g).

For index gadget g with CC(g) = Ω(log N), we get CC(Gap-MCSP ∘ g) ≥ N log N.

**Step 3**: From Communication to Formula Size

The composed function Gap-MCSP ∘ g operates on N × m variables (where m = |g|).

Its communication complexity is ≥ N log N.

The formula **depth** of Gap-MCSP ∘ g is ≥ N log N.

Formula **size** is ≥ depth, so size ≥ N log N.

But wait - this is for the COMPOSED function, not Gap-MCSP itself!

### The Problem with Lifting

Lifting gives bounds for f ∘ g, not f.

The composed function is different from the original.

**Question**: Does size(f ∘ g) ≥ size(f)?

Generally yes, because the composition adds complexity.

But we can't directly transfer bounds from f ∘ g back to f.

## Partition Communication Complexity

### The Idea

Instead of standard two-party communication, consider **partition communication complexity**.

For each partition of variables into two sets P = (X_1, X_2):
- Alice gets values of X_1
- Bob gets values of X_2
- They compute f(X)

**Best-partition complexity**: min over partitions of CC_P(f).

This relates more directly to circuit structure:
- Low best-partition CC → variable can be "separated"
- High best-partition CC → variables are "entangled"

### Application to Gap-MCSP

What's the best-partition CC of Gap-MCSP?

For ANY partition of the N input bits:
- Alice has T_1 (values of some positions)
- Bob has T_2 (values of other positions)
- They determine if the full truth table T has low complexity

**Key observation**: Circuit complexity depends on the RELATIONSHIP between all positions, not just individual values.

This is a GLOBAL property!

**Conjecture**: For most balanced partitions, CC_P(Gap-MCSP) = Ω(N).

**Reasoning**: Knowing half the truth table tells you almost nothing about circuit complexity. You need the whole structure.

### From Partition CC to Formula Size?

**Known result** (maybe): Best-partition CC relates to formula size through separators.

If f has formula size s, then for some balanced partition, CC_P(f) ≤ ???

Actually, the standard KW theorem uses a SPECIFIC partition (the cut in the formula tree), not all partitions.

So best-partition CC might not directly give formula size bounds.

## A Different Angle: Rectangle Bounds

### The Idea

In communication complexity, a **combinatorial rectangle** is a set R = A × B where Alice's inputs are in A, Bob's in B.

The **rectangle bound** on CC is: CC(f) ≥ log(1/max_R Pr[R accepts]).

### Application

For Gap-MCSP, consider rectangles in the space of (simple T, complex T) pairs.

A rectangle R = A × B where:
- A = set of simple truth tables
- B = set of complex truth tables
- All pairs in R have T_A[i] ≠ T_B[i] for some fixed i

The rectangle bound gives: CC(KW_{Gap-MCSP}) ≥ log(N / max_R |R|).

To get strong bounds, we need small rectangles - i.e., for each fixed differing position i, few (simple, complex) pairs differ ONLY at i.

This seems related to the "boundary" structure of Gap-MCSP!

## Connection to Locality Barrier

The locality barrier says Gap-MCSP can be computed by AC⁰-XOR + local oracles.

Local oracles can answer queries about SMALL subsets of input.

Communication complexity captures how much information must flow GLOBALLY.

**Hypothesis**: The local oracle structure means communication can be "simulated" locally, preventing strong CC lower bounds.

But wait - CC is a property of the function, not the circuit computing it. The local oracle computes the SAME function.

So CC bounds apply to Gap-MCSP regardless of how it's computed.

The issue is: do CC bounds translate to circuit SIZE bounds?

For depth: yes (KW theorem).
For size: unclear, except through composition/lifting.

## Potential Non-Local Technique

### The Structure

1. Prove Gap-MCSP has high partition communication complexity
2. Relate partition CC to formula size (new theorem needed)
3. Get formula lower bound that doesn't localize

### Why It Might Not Localize

Partition CC is a GLOBAL property - it considers how information is distributed across the ENTIRE input.

Local oracles can't help with partition CC because the partition might separate the oracle's inputs.

So a partition-CC-based technique might be non-local!

### The Challenge

No direct theorem relates partition CC to formula size.

Need to develop this connection - potentially a research contribution.

## Summary

| Approach | What It Gives | Locality Status |
|----------|---------------|-----------------|
| Standard KW | Depth bounds | Localizes |
| Lifting | Bounds on composed function | Doesn't transfer |
| Partition CC | Unknown | Potentially non-local |
| Rectangle bounds | KW game CC | Localizes |

**Most promising**: Develop partition communication complexity to formula size connection.

This would give a non-local technique if:
1. Gap-MCSP has high partition CC
2. High partition CC implies large formulas
3. Local oracles don't help with partition CC

All three need verification/proof.
