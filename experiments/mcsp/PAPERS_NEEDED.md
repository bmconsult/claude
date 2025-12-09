# Papers Needed to Close the Isotypic Gap

## The Core Problem

Current isotypic bounds give formula size ≥ polylog(N), but we need N^{3+ε}.

The gap is ~10^16× for realistic parameters (n=20).

## Critical Papers

### 1. Algebraic Metacomplexity (Nov 2024) ⭐ MOST CRITICAL
**"Algebraic metacomplexity and representation theory"**
- Authors: van den Berg, Dutta, Gesmundo, Ikenmeyer, Lysikov
- **Key result**: Isotypic decomposition of metapolynomials has quasipolynomial blowup
- Uses Poincaré-Birkhoff-Witt theorem and Gelfand-Tsetlin theory
- Accepted to CCC 2025
- **Need**: Full paper - their technique might translate to Boolean!
- **Link**: https://arxiv.org/abs/2411.03444

### 2. Hardness Magnification for Gap-MCSP
**"Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations"**
- Authors: McKay, Murray, Williams (STOC 2019)
- **Key result**: n^{1+ε} lower bounds for MCSP imply NP ⊄ P/poly
- **Need**: Exact statement of the N^{3+ε} threshold for formulas
- **Link**: STOC 2019 proceedings (also cited in ECCC TR19-118)

### 3. Locality Barrier ⭐ MUST UNDERSTAND
**"Beyond Natural Proofs: Hardness Magnification and Locality"**
- Authors: Chen, Hirahara, Oliveira, Pich, Rajgopal, Santhanam
- **Key result**: Existing lower bound techniques "localize" - extend to circuits with local oracles
- Shows magnification sidesteps natural proofs but hits locality barrier
- **Need**: Exact definition of "local oracle" and why techniques localize
- **Link**: https://eccc.weizmann.ac.il/report/2019/168/ (also ITCS 2020, JACM 2022)

### 4. Occurrence Obstructions Fail
**"No occurrence obstructions in geometric complexity theory"** (2019)
- Authors: Bürgisser, Ikenmeyer, Panova
- Proves GCT occurrence obstructions fail
- **Need**: To understand why this approach failed and what's different about multiplicity obstructions
- **Link**: Journal of AMS or arXiv

### 5. Kronecker Coefficients
**"Computing Kronecker Coefficients"** or related
- Various authors (Briand, Orellana, Rosas, etc.)
- For better bounds on tensor product decomposition
- **Need**: Asymptotic bounds on number of nonzero Kronecker coefficients
- **Links**: arXiv search "Kronecker coefficients bounds"

### 6. Query-to-Communication Lifting
**"Query-to-Communication Lifting for BPP"** or similar
- Authors: Göös, Pitassi, Watson, etc.
- Techniques for lifting query complexity to communication complexity
- **Need**: Maybe adaptable to lift isotypic bounds to formula bounds
- **Link**: STOC/FOCS proceedings

### 7. Natural Proofs Barrier
**"Natural Proofs"** (1997)
- Authors: Razborov, Rudich
- The classic barrier paper
- **Need**: To verify isotypic techniques are NOT natural (hence escape the barrier)
- **Link**: ACM DL (JCSS) or online

## Secondary Papers (Nice to Have)

### 8. Representation Theory of S_n
**"The Symmetric Group"** - Sagan
- Standard textbook for S_n representation theory
- **Need**: For clean proofs of dimension formulas, character theory

### 9. Boolean Function Analysis
**"Analysis of Boolean Functions"** - O'Donnell
- Standard reference for Fourier analysis
- **Need**: For precise statements of LMN and related
- **Link**: Free online at https://www.cs.cmu.edu/~odonnell/boolean-analysis.pdf

### 10. GCT Overview
**"Geometric Complexity Theory: An Introduction"**
- Authors: Mulmuley (various survey papers)
- **Need**: Big picture of GCT program
- **Link**: arXiv

## Priority Order

1. **Ikenmeyer Nov 2024** - Most critical, might have the key technique
2. **McKay-Murray-Williams** - Need exact magnification theorem
3. **Chen et al.** - Need exact locality barrier statement
4. **Lifting papers** - Might provide the technical tool

## What I'm Looking For

Specifically, I need to find:

1. **A "tight" formula-isotypic theorem**: Something that says "formula size s ⟺ isotypic complexity poly(s)" (not n^{poly(s)})

2. **A communication complexity connection**: Isotypic structure → communication lower bound → formula size

3. **Why algebraic works but Boolean is hard**: The Nov 2024 paper works for algebraic circuits - what's different about Boolean?

4. **Barrier escape verification**: Confirmation that isotypic techniques don't "naturalize"
