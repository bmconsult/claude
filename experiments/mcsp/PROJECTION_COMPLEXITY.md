# Computational Complexity of Isotypic Projections

## The Key Question

**How hard is it to compute π_λ(f) for S_n acting on Boolean functions?**

## The Naive Algorithm

For f: {0,1}^n → R and partition λ ⊢ n:

π_λ(f) = (d_λ / n!) Σ_{σ∈S_n} χ_λ(σ) f^σ

where f^σ is f permuted by σ.

**Complexity**:
- n! terms in the sum
- Each term: O(2^n) to compute f^σ from f
- Total: O(n! × 2^n)

This is doubly exponential!

## FFT Over S_n

There's a Fourier transform over non-abelian groups like S_n.

Standard algorithm (Clausen 1989, Diaconis-Rockmore 1990):
- Complexity: O(n² × n!)
- This computes ALL isotypic projections simultaneously

Still exponential in n, but much better than naive.

## Faster Algorithms

**Clausen-Baum algorithm** uses separation of variables:
- Complexity: O(n × n! × d_max²)
- Where d_max ≈ √(n!) is the largest irrep dimension
- Total: O(n × n! × n!) = O(n × (n!)²)

Wait, that's WORSE. Let me reconsider...

**Actually**: The Clausen-Baum algorithm for computing the S_n Fourier transform is:
- O(n² × n!) for the full transform over the group algebra C[S_n]

For our case, we're computing the transform of a function f: {0,1}^n → R, which is a 2^n-dimensional vector, not an n!-dimensional vector.

The action of S_n on {0,1}^n induces a homomorphism:
ρ: C[S_n] → End(C^{2^n})

Computing the induced transform has complexity:
- Apply each σ to the 2^n-dimensional space
- Each σ application is O(2^n) via bit permutation
- Naive: O(n! × 2^n)

Using FFT structure: probably O(n × n! × 2^n / something)

## The Fundamental Issue

**Observation**: 2^n >> n! for n ≥ 13.

| n | 2^n | n! |
|---|-----|-----|
| 5 | 32 | 120 |
| 10 | 1024 | 3.6M |
| 13 | 8192 | 6.2B |
| 20 | 1M | 2.4 × 10^18 |

For n ≥ 13: The space (2^n dims) is smaller than the group (n! elements)!

This means:
- Many group elements act identically on the space
- Projections have inherent redundancy
- Maybe exploitable for efficiency?

## Efficient Computation via Orbit Structure?

The space R^{2^n} decomposes into S_n orbits:
- Each orbit is a set of truth tables related by permutation
- Number of orbits ≈ 2^n / n! (much smaller than 2^n for large n)

If we work orbit-by-orbit:
- Each orbit has ≤ n! elements
- Total work: O(number of orbits × n!) = O(2^n)

**Wait**: This suggests O(2^n) = O(N) might be achievable!

## More Careful Analysis

The projection π_λ(f) for f ∈ R^{2^n} can be computed as:

1. Decompose f by Hamming weight: f = f_0 + f_1 + ... + f_n
   where f_k is supported on weight-k inputs

2. Within each weight class, apply S_n projection

For weight-k inputs:
- Space dimension: (n choose k)
- S_n acts transitively (it's a single orbit!)
- Projection is just averaging + multiplication by character values

**This is polynomial in n for each weight class!**

Total: O(n × poly(n, (n choose n/2))) = O(n × poly(n) × 2^n / √n) = O(2^n × poly(n))

**Conclusion**: Isotypic projection for S_n on Boolean functions is **O(N × polylog(N))** where N = 2^n!

## What This Means

If projections can be computed in O(N × polylog(N)):
- Projections are NOT the bottleneck
- The bottleneck is in how FORMULAS interact with projections

This shifts the question:
- Not "how hard is projection?"
- But "how does formula computation compose with projection?"

## The New Key Question

If F is a formula of size s computing Gap-MCSP:
- Input: truth table T ∈ {0,1}^N
- Output: 1 iff complexity(T) ≤ threshold

How does F "see" the isotypic structure of T?

**Hypothesis**: F can only see O(poly(s)) isotypic "bits" of information about T.

If Gap-MCSP requires Ω(n!) isotypic bits, then:
poly(s) ≥ n!
s ≥ n!^{1/O(1)} >> N^3

**This would prove the lower bound!**

## Next Steps

1. Define "isotypic bits" or "isotypic information" precisely
2. Prove formulas have bounded isotypic information capacity
3. Prove Gap-MCSP requires high isotypic information
