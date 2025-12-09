# Fourier-Theoretic Analysis of Gap-MCSP

## Key Discovery: Symmetry Structure

### Empirical Finding

The set of "simple" truth tables (circuit complexity ≤ threshold) is:
1. **Complement closed**: If T is simple, so is ¬T
2. **Reversal closed**: If T is simple, so is reversed(T)

### Implication for Fourier Spectrum

**Theorem**: If a Boolean function f: {0,1}^N → {0,1} is "complement-symmetric" (meaning f(T) = f(¬T) for all T), then all odd-level Fourier coefficients are zero.

**Proof**:
- Let S ⊆ [N] with |S| odd
- ĝ(S) = E_T[g(T) × χ_S(T)]
- For complement-symmetric g: g(T) = g(¬T)
- Also: χ_S(¬T) = (-1)^{⊕_{i∈S} (1-T_i)} = (-1)^{|S|} × χ_S(T) = -χ_S(T) (when |S| odd)
- Pairing T with ¬T: g(T)χ_S(T) + g(¬T)χ_S(¬T) = g(T)χ_S(T) - g(T)χ_S(T) = 0
- Sum over all pairs: ĝ(S) = 0 ∎

**Corollary**: Gap-MCSP has Fourier weight only on even levels.

## What This Means for Lower Bounds

For a DNF of size m, the Fourier weight is concentrated at levels ≤ O(log m).

For Gap-MCSP with only even-level weight:
- Weight is at levels 0, 2, 4, ..., N
- For U₂-Formula of size N^{3+ε}, weight should be at levels ≤ (3+ε)·log N

**The question**: Does Gap-MCSP have significant weight at even levels > (3+ε)·log N?

## Asymptotic Analysis

Let n = log N (number of variables in the represented function).
Then N = 2^n is the truth table size.

For N^3 threshold: level threshold = 3 log N = 3n
For N^{3+ε} threshold: level threshold = (3+ε)n

Maximum level = N = 2^n

So we're asking: does Gap-MCSP have weight at even levels in the range [(3+ε)n, 2^n]?

This is an exponentially large range as n grows!

## Structural Analysis

### What Determines High-Level Fourier Weight?

Functions with high-level Fourier weight are those that depend strongly on parity-like combinations of many variables.

Gap-MCSP distinguishes:
- Simple truth tables: compressible, have structure
- Complex truth tables: incompressible, look random

**Key Question**: Do complex truth tables have any systematic relationship with high-level parities?

### Parity Structure of Truth Tables

A truth table T of function f: {0,1}^n → {0,1} has:
- T[x] = f(x) for each x ∈ {0,1}^n

The parity χ_S(T) = (-1)^{⊕_{x∈S} f(x)} for S ⊆ {0,1}^n.

This is the parity of f evaluated on a specific subset of inputs S.

For random f: χ_S(T) is ±1 with equal probability (for |S| > 0).

For structured f: χ_S(T) might be biased depending on S.

### Example: Parity Functions

Let f = XOR of all inputs. Then:
- f(x) = ⊕_i x_i
- T[x] = ⊕_i x_i
- χ_S(T) = (-1)^{⊕_{x∈S} ⊕_i x_i} = (-1)^{⊕_i ⊕_{x∈S} x_i}

This depends on the parity structure of S.

If S contains an even number of inputs for each coordinate value, χ_S(T) is fixed.

### Example: AND Function

Let f = AND of all inputs. Then:
- f(x) = 1 iff x = 1...1
- T = (0,0,...,0,1)
- χ_S(T) = (-1)^{|S ∩ {1...1}|} = (-1)^{[1...1 ∈ S]}

So χ_S(T) = -1 if "all 1s" input is in S, else +1.

This is a simple function, so its Fourier structure relates to Gap-MCSP coefficients.

## The Core Question

**Does the "shape" of simple truth tables imply specific Fourier structure for Gap-MCSP?**

Gap-MCSP(T) = 1 ⟺ T is the truth table of a simple function.

The Fourier coefficient:
ĝ(S) = E_T[Gap-MCSP(T) × χ_S(T)]
     = Pr[T simple, χ_S(T)=1] - Pr[T simple, χ_S(T)=-1]
       - (Pr[T complex, χ_S(T)=1] - Pr[T complex, χ_S(T)=-1])

For random (complex) T: the two terms in the second parentheses are equal, so contribution is 0.

So: ĝ(S) ≈ Pr[T simple, χ_S(T)=1] - Pr[T simple, χ_S(T)=-1]
         = 2 × (Pr[T simple, χ_S(T)=1] - 1/2 × Pr[T simple])

This measures: among simple truth tables, is χ_S biased?

## Hypothesis

**Hypothesis**: For "generic" subsets S of size k, simple truth tables have no systematic χ_S bias. Therefore:
- ĝ(S) ≈ 0 for most S
- Only "structured" S have non-zero coefficients
- Structured S correspond to specific relationships between simple functions

**Consequence**: If this hypothesis is true, Gap-MCSP's Fourier weight might be concentrated on "special" subsets, which could be relatively few even at high levels.

This would mean Gap-MCSP is "Fourier sparse" - a property potentially compatible with small formulas.

## Alternative Hypothesis

**Alternative**: Simple truth tables DO have systematic χ_S biases at high levels, due to their structural properties.

If true, this could imply Gap-MCSP has significant high-level Fourier weight, giving formula lower bounds.

## How to Test

To distinguish these hypotheses:
1. Characterize the "special" subsets S that give non-zero coefficients
2. Count how many such S exist at each level
3. Determine if the count grows faster than the formula size threshold

This requires deeper analysis of the structure of simple Boolean functions.

## Connection to Prior Work

This Fourier analysis connects to:
- **Random restriction method**: Restrictions simplify functions by setting variables
- **Switching lemma**: Bounds on how restrictions simplify DNFs
- **LMN theorem**: AC⁰ functions are Fourier-concentrated on low levels

The locality barrier might be related to the Fourier sparsity of Gap-MCSP.

If Gap-MCSP is Fourier-sparse (few non-zero coefficients), then:
- Local oracles can "handle" the sparse structure
- Lower bound techniques that use Fourier density fail

A non-local technique might need to exploit the SPECIFIC pattern of non-zero coefficients, not just their level.

## Next Steps

1. Compute which subsets S have non-zero ĝ(S) for small n
2. Look for patterns in the structure of these S
3. Determine if the pattern implies Fourier sparsity or density at high levels
4. Connect to the locality barrier: does sparsity/density relate to local oracle computability?
