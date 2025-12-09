# What Quasipolynomial Blowup Would Mean

## The Algebraic Metacomplexity Result

From the Nov 2024 paper (arXiv:2411.03444):
- Isotypic decomposition of metapolynomials has **quasipolynomial blowup**
- Specifically: circuit size s → isotypic circuit size s^{O(log n)}

This is MUCH better than my exponential bounds!

## If Boolean Analog Holds

Suppose we can prove for Boolean formulas:
- Formula size s → "isotypic reach" ≤ s^{O(log n)}

Then for Gap-MCSP to distinguish n!/poly(n) vs poly(n) isotypic structures:

s^{O(log n)} ≥ n!/poly(n)

Taking logs:
O(log n) × log s ≥ n log n - O(log n)

Solving:
log s ≥ (n log n - O(log n)) / O(log n) = n - O(1)

Therefore:
s ≥ 2^{n - O(1)} = N^{1-o(1)}

## This Would Give N^{1-o(1)} Bounds!

Not yet N^{3+ε}, but MUCH closer than polylog(N).

## The Gap: 1 vs 3+ε

Current algebraic result (if it translated): N^{1-o(1)}
Magnification threshold: N^{3+ε}

Gap: factor of N^{2+ε}

## Possible Paths to Close

### Path 1: Better Isotypic-Formula Connection
Maybe the Boolean case is better than algebraic?
- Algebraic: GL_n action on polynomials
- Boolean: S_n action on truth tables
- S_n is finite (n! elements), GL_n is infinite
- This might give tighter bounds for Boolean!

### Path 2: Combine With Other Techniques
Use isotypic bounds to get N^{1-o(1)}, then combine with:
- Communication complexity lifting
- Depth reduction arguments
- Magnification-specific structure

### Path 3: Different Isotypic Measure
Instead of "reach" (number of components), use:
- Total dimension of touched components
- Weighted sum by irrep dimensions
- Spectral properties of projections

### Path 4: Exploit Gap-MCSP Specifics
Gap-MCSP has specific structure:
- Input is a truth table T
- Output depends on circuit complexity of T
- Maybe this specific structure gives stronger bounds

## Key Question for the Papers

1. What exactly is "quasipolynomial blowup" in the algebraic paper?
   - Circuit computing isotypic projection?
   - Or formula distinguishing isotypic components?

2. Does their technique use:
   - The specific structure of GL_n?
   - Or general representation theory that applies to S_n too?

3. What are PBW theorem and Gelfand-Tsetlin theory?
   - Do they have Boolean analogs?

## Optimistic Scenario

If the Boolean analog gives n^{O(1)} blowup (polynomial, not quasipolynomial):

s^{O(1)} ≥ n!/poly(n) = n^{n-O(1)} (by Stirling)
s ≥ n^{(n-O(1))/O(1)} = n^{Ω(n)} = 2^{Ω(n log n)}

For n ≥ some constant: 2^{Ω(n log n)} > 2^{(3+ε)n} = N^{3+ε}

This would WORK! But needs the Boolean blowup to be polynomial, not quasipolynomial.

## Pessimistic Scenario

If the Boolean case has worse blowup than algebraic (say exponential):

s^{n^{O(1)}} ≥ n!/poly(n)
log s × n^{O(1)} ≥ n log n
log s ≥ n log n / n^{O(1)} = n^{1-O(1)} log n

s ≥ 2^{n^{1-O(1)} log n} = subexponential but not polynomial

This would NOT give N^{3+ε}.

## Conclusion

The key technical question is:
**What is the Boolean analog of the algebraic metacomplexity blowup?**

- Polynomial blowup → N^{3+ε} achievable!
- Quasipolynomial blowup → N^{1-o(1)}, need additional technique
- Exponential blowup → approach fails

The papers should clarify what blowup is achievable and why.
