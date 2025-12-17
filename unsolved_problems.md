## **Top 50: What Actually Solves It**

### **Key to Proof Requirements:**

* **∀-PROOF**: Must work for ALL cases, no exceptions. "Almost all" \= NOT SOLVED  
* **CONSTRUCTIVE**: Must exhibit the object or provide algorithm  
* **FINITE REDUCTION**: Can reduce to finite computer-checkable cases  
* **NEW TOOLS LIKELY**: Current techniques known to be insufficient  
* **ANALYTIC**: Requires complex analysis / analytic number theory machinery  
* **TOPOLOGICAL**: Needs invariants, obstruction theory, or homological methods  
* **ALGEBRAIC**: Pure algebraic construction or algebraic geometry  
* **COMPUTER-ASSISTED OK**: Community accepts verified computational proofs

---

### **Tier 1: Closest to Solution**

**1\. Moving Sofa Problem**

* **Status**: Claimed proof under review (Baek, Nov 2024\)  
* **What solves it**: Prove Gerver's sofa (area 2.2195...) is globally optimal  
* **Proof type**: ∀-PROOF \+ ANALYTIC. Must show NO shape exceeds this area. Baek used calculus of variations \+ injective function analysis. Upper bound proof, not computational.  
* **What DOESN'T count**: Computer searches finding no better shapes

---

**2\. Twin Prime Conjecture**

* **Status**: Bounded gaps at 246 (Maynard/Tao/Polymath)  
* **What solves it**: Prove infinitely many primes p where p+2 is also prime  
* **Proof type**: ∀-PROOF \+ ANALYTIC. Requires breakthrough in sieve methods or L-function theory. Must show gap=2 occurs infinitely often.  
* **What DOESN'T count**:  
  * Showing gaps ≤ 246 (already done, NOT the conjecture)  
  * Probabilistic arguments about prime distribution  
  * "Almost all" results  
  * Computational verification to any finite bound  
* **Hard truth**: Zhang/Maynard methods have known barriers. Gap=2 likely requires fundamentally new ideas, possibly connection to Elliott-Halberstam conjecture or beyond.

---

**3\. Goldbach's Conjecture**

* **Status**: Verified to 4×10¹⁸; weak version proven (Helfgott 2013\)  
* **What solves it**: Prove EVERY even n \> 2 is sum of two primes  
* **Proof type**: ∀-PROOF \+ ANALYTIC. Universal statement over all even integers.  
* **What DOESN'T count**:  
  * Weak Goldbach (odd \= 3 primes) — that's DONE but different  
  * Computational verification — irrelevant no matter how far  
  * "Almost all even numbers" — Vinogradov-type results exist, NOT the conjecture  
  * Density arguments  
* **Hard truth**: Circle method gives "almost all." The jump from "almost all" to "all" is the entire problem. No known technique bridges this gap.

---

**4\. Sendov's Conjecture (small degrees)**

* **Status**: Proven for n ≥ n₀ (Tao 2020); proven for n \< 9  
* **What solves it**: Prove for degrees 9, 10, 11, ... up to n₀  
* **Proof type**: FINITE REDUCTION \+ COMPUTER-ASSISTED OK. This is now a finite problem in principle.  
* **What DOESN'T count**: Proving it for "generic" polynomials  
* **Hard truth**: Tao's n₀ is not explicit and likely HUGE. Making it explicit and checking intermediate cases is substantial but tractable work. Computer-assisted proofs acceptable here.

---

**5\. Union-Closed Sets Conjecture (Frankl's)**

* **Status**: Proven that some element appears in ≥ 38.2% of sets (Gilmer → Sawin → improvements)  
* **What solves it**: Prove some element appears in ≥ 50% of sets  
* **Proof type**: ∀-PROOF \+ COMBINATORIAL. Must work for ALL union-closed families.  
* **What DOESN'T count**:  
  * Showing 38%, 40%, 45%... (progress but NOT the conjecture)  
  * Proving it for "most" families  
  * Special cases (small ground sets, separating families, etc.)  
* **Hard truth**: Current entropy methods hit barriers around 38-39%. The jump to 50% likely requires new approach. Lattice-theoretic or graph-theoretic reformulation might help.

---

**6\. Collatz Conjecture**

* **Status**: "Almost all" orbits reach small values (Tao 2019\)  
* **What solves it**: Prove EVERY positive integer eventually reaches 1  
* **Proof type**: ∀-PROOF. Must work for all n ∈ ℕ⁺.  
* **What DOESN'T count**:  
  * Tao's "almost all" result — explicitly NOT the conjecture  
  * Computational verification to 2.36×10²¹ — irrelevant  
  * Probabilistic/statistical arguments about orbit behavior  
  * Showing "most" orbits descend  
  * Showing no cycles exist except 1-2-4 (necessary but not sufficient)  
* **Hard truth**: Erdős said "mathematics may not be ready." Lagarias called it "completely out of reach." Tao's result is likely as close as current methods can get. May require entirely new mathematics or be undecidable. The problem mixes additive (3n+1) and multiplicative (÷2) operations in ways that resist all known tools.

---

**7\. Inscribed Square Problem (Toeplitz)**

* **Status**: Proven for smooth curves, polygons, many special cases  
* **What solves it**: Prove EVERY Jordan curve (continuous simple closed curve) contains 4 vertices of a square  
* **Proof type**: ∀-PROOF \+ TOPOLOGICAL. Must handle arbitrary continuous curves including fractals.  
* **What DOESN'T count**:  
  * Smooth curves (done)  
  * Piecewise analytic (done)  
  * Convex curves (done)  
  * Showing "generic" curves have inscribed squares  
* **Hard truth**: The difficulty is non-smooth curves where limiting arguments fail (squares can shrink to points). Requires controlling behavior at all scales simultaneously. Topological methods (projective plane embedding arguments) work for rectangles but not squares.

---

**8\. Hadamard Conjecture**

* **Status**: Hadamard matrices known for many orders; gaps remain  
* **What solves it**: Prove Hadamard matrix of order 4n exists for ALL positive integers n  
* **Proof type**: ∀-PROOF \+ CONSTRUCTIVE preferred but existence proof acceptable.  
* **What DOESN'T count**:  
  * Finding more Hadamard matrices at specific orders  
  * Probabilistic existence arguments  
* **Hard truth**: Known constructions cover most cases but not all. Smallest unknown order is 668\. Could potentially be FINITE REDUCTION if systematic computer search becomes feasible, but the search space is enormous.

---

**9\. Lonely Runner Conjecture**

* **Status**: Proven for k ≤ 7 runners  
* **What solves it**: Prove for ALL k runners with distinct speeds, each runner is "lonely" (distance ≥ 1/k from all others) at some time  
* **Proof type**: ∀-PROOF over all k.  
* **What DOESN'T count**: Proving more specific values of k (progress but not solution)  
* **Hard truth**: Each new k requires substantially more work. No general method handles arbitrary k. The k=7 proof is already computationally intensive. May require fundamentally new approach for general k.

---

**10\. 1/3–2/3 Conjecture**

* **Status**: Proven for many classes of posets; best general bound is 3/11  
* **What solves it**: Prove every finite non-total poset has elements x,y where P(x before y in random linear extension) ∈ \[1/3, 2/3\]  
* **Proof type**: ∀-PROOF \+ COMBINATORIAL. Must work for all finite posets.  
* **What DOESN'T count**:  
  * Improving bounds to 3/11, 0.29, etc. (progress, not solution)  
  * Special classes of posets  
* **Hard truth**: Current best bound (3/11 ≈ 0.27) is far from 1/3 ≈ 0.33. Information-theoretic approaches have hit barriers.

---

**11\. Erdős–Gyárfás Conjecture**

* **Status**: Partial results for specific graph classes  
* **What solves it**: Prove every graph with minimum degree ≥ 3 contains a cycle whose length is a power of 2  
* **Proof type**: ∀-PROOF \+ COMBINATORIAL/GRAPH-THEORETIC.  
* **What DOESN'T count**: Proving for cubic graphs, planar graphs, etc. (special cases)  
* **Hard truth**: Power-of-2 constraint is unusual and resists standard cycle-finding techniques.

---

**12\. Lebesgue's Universal Covering Problem**

* **Status**: Bounds on minimum area between \~0.832 and \~0.844  
* **What solves it**: Find the EXACT minimum area of a convex set that covers all planar sets of diameter 1  
* **Proof type**: CONSTRUCTIVE \+ ∀-PROOF. Must prove lower bound (no smaller works) AND upper bound (specific shape achieves it).  
* **What DOESN'T count**: Improving bounds incrementally  
* **Hard truth**: Requires simultaneously optimizing over all possible covering shapes AND proving no diameter-1 set escapes. Very difficult optimization problem.

---

**13\. Moser's Worm Problem**

* **Status**: Bounds tightening, best cover has area \~0.260  
* **What solves it**: Find exact minimum area covering all unit-length curves  
* **Proof type**: CONSTRUCTIVE \+ ∀-PROOF.  
* **What DOESN'T count**: Better bounds  
* **Hard truth**: Similar to Lebesgue but for curves instead of diameter-1 sets. Same fundamental difficulty.

---

### **Tier 2: Substantial Progress Expected**

**14\. Invariant Subspace Problem (Hilbert space)**

* **Status**: FALSE for general Banach spaces (Enflo); OPEN for Hilbert spaces  
* **What solves it**: Prove every bounded linear operator on separable infinite-dimensional Hilbert space has non-trivial closed invariant subspace, OR construct counterexample  
* **Proof type**: ∀-PROOF (positive) or CONSTRUCTIVE counterexample  
* **Hard truth**: Banach space counterexamples use exotic constructions that don't transfer to Hilbert spaces. The additional structure of inner products is both helpful and obstructive. Might be either true or false.

---

**15\. Birch and Swinnerton-Dyer Conjecture** (Millennium Prize)

* **Status**: Proven for rank 0 and 1 elliptic curves  
* **What solves it**: Prove rank of E(ℚ) equals order of vanishing of L(E,s) at s=1, with correct leading coefficient formula  
* **Proof type**: ∀-PROOF \+ ALGEBRAIC/ANALYTIC. Must work for ALL elliptic curves over ℚ.  
* **What DOESN'T count**:  
  * Rank 0 and 1 cases (done, not the full conjecture)  
  * Numerical verification  
  * Proving one direction of the equivalence  
* **Hard truth**: Higher rank cases require understanding Shafarevich-Tate groups, which are mysterious. Full proof likely requires new ideas connecting L-functions to arithmetic more directly. NEW TOOLS LIKELY.

---

**16\. Sunflower Conjecture**

* **Status**: Major progress by Alweiss-Lovett-Wu-Zhang (2019); improved bounds  
* **What solves it**: Prove that among k-sets, having \> c^k sets guarantees a sunflower of size r (for some constant c depending only on r)  
* **Proof type**: ∀-PROOF \+ COMBINATORIAL.  
* **What DOESN'T count**: Improving the base from current \~log(k) to some other function  
* **Hard truth**: Recent breakthrough got exponential bound in k. Constant bound in k is the actual conjecture.

---

**17\. Hadwiger Conjecture (graph theory)**

* **Status**: Proven for k ≤ 6; k \= 5 case is Four Color Theorem equivalent  
* **What solves it**: Prove every graph with no K\_t minor is (t-1)-colorable for ALL t  
* **Proof type**: ∀-PROOF over all t.  
* **What DOESN'T count**: Proving for more specific values of t  
* **Hard truth**: k=6 proof is deep. Each step up is dramatically harder. General proof likely requires understanding graph minors at a new level. Robertson-Seymour theory relevant but not sufficient.

---

**18\. Cycle Double Cover Conjecture**

* **Status**: Open; many equivalent formulations  
* **What solves it**: Prove every bridgeless graph has a family of cycles covering each edge exactly twice  
* **Proof type**: ∀-PROOF \+ COMBINATORIAL/TOPOLOGICAL.  
* **Hard truth**: Connected to many other conjectures (5-flow, Petersen coloring). Solving any one might solve others.

---

**19\. Reconstruction Conjecture**

* **Status**: Open since 1942; proven for many graph classes  
* **What solves it**: Prove every graph on ≥3 vertices is determined by its deck of vertex-deleted subgraphs  
* **Proof type**: ∀-PROOF \+ COMBINATORIAL.  
* **What DOESN'T count**: Proving for trees, regular graphs, etc.  
* **Hard truth**: Known for almost all n-vertex graphs (probabilistically), but universal proof elusive.

---

**20\. Graceful Tree Conjecture**

* **Status**: Proven for many tree classes (caterpillars, paths, etc.)  
* **What solves it**: Prove every tree on n vertices has a graceful labeling  
* **Proof type**: ∀-PROOF \+ CONSTRUCTIVE preferred.  
* **What DOESN'T count**: More special cases; computational verification  
* **Hard truth**: No unified technique handles all trees. The variety of tree structures resists single approach.

---

**21\. List Coloring Conjecture**

* **Status**: Open; equivalent to edge-choosability conjecture  
* **What solves it**: Prove χ'\_l(G) \= χ'(G) for all graphs G (list chromatic index \= chromatic index)  
* **Proof type**: ∀-PROOF \+ COMBINATORIAL.  
* **Hard truth**: Known for bipartite graphs. General case requires handling complex edge interactions.

---

**22\. Total Coloring Conjecture**

* **Status**: Proven for Δ ≤ 5  
* **What solves it**: Prove χ''(G) ≤ Δ(G) \+ 2 for all graphs  
* **Proof type**: ∀-PROOF.  
* **Hard truth**: Probabilistic methods show it holds for "almost all" graphs. Universal proof needs different approach.

---

**23\. Gyárfás–Sumner Conjecture**

* **Status**: Proven for some trees T  
* **What solves it**: Prove for every tree T, the class of T-free graphs is χ-bounded  
* **Proof type**: ∀-PROOF over all trees T.  
* **Hard truth**: Need uniform approach across all tree structures.

---

**24\. Vizing's Conjecture**

* **Status**: Best bound is γ(G□H) ≥ γ(G)γ(H)/2  
* **What solves it**: Prove γ(G□H) ≥ γ(G)γ(H) for domination number of Cartesian products  
* **Proof type**: ∀-PROOF.  
* **What DOESN'T count**: Improving factor from 1/2 toward 1  
* **Hard truth**: Half the conjecture is known. Closing the factor-of-2 gap is the entire remaining problem.

---

**25\. Barnette's Conjecture**

* **Status**: Open; special cases proven  
* **What solves it**: Prove every 3-connected cubic bipartite planar graph is Hamiltonian  
* **Proof type**: ∀-PROOF.  
* **Hard truth**: Combines multiple constraints (cubic, bipartite, planar, 3-connected) in subtle way.

---

**26\. Erdős–Hajnal Conjecture**

* **Status**: Proven for some H; general case open  
* **What solves it**: Prove for every graph H, H-free graphs have polynomial-size clique or independent set  
* **Proof type**: ∀-PROOF over all H.  
* **What DOESN'T count**: Proving for specific forbidden graphs  
* **Hard truth**: Known for small H. Need unified approach.

---

**27\. Tuza's Conjecture**

* **Status**: Factor 2 known (can hit all triangles with ≤ 2τ edges where τ \= max packing)  
* **What solves it**: Prove factor 3/2 suffices  
* **Proof type**: ∀-PROOF.  
* **What DOESN'T count**: Improving from 2 toward 1.5  
* **Hard truth**: Gap between 2 and 1.5 is the entire problem.

---

**28\. Crouzeix's Conjecture**

* **Status**: Factor 2 proven; conjecture is factor 1  
* **What solves it**: Prove ‖f(A)‖ ≤ 2 sup\_{W(A)} |f| for all matrices A and analytic f  
* **Proof type**: ∀-PROOF \+ ANALYTIC.  
* **Hard truth**: 2 is proven. 1+ε for any ε\>0 is the conjecture.

---

**29\. Lehmer's Conjecture (Mahler measure)**

* **Status**: No polynomial with Mahler measure between 1 and Lehmer's constant \~1.176 known  
* **What solves it**: Prove Lehmer's polynomial has minimal Mahler measure \> 1, OR find smaller  
* **Proof type**: ∀-PROOF (lower bound) or CONSTRUCTIVE (counterexample)  
* **Hard truth**: Extremely hard to rule out small Mahler measures.

---

**30\. Carmichael's Totient Conjecture**

* **Status**: Verified computationally to large bounds  
* **What solves it**: Prove φ(n) \= φ(m) always has solution m ≠ n  
* **Proof type**: ∀-PROOF.  
* **What DOESN'T count**: More computation  
* **Hard truth**: Would follow from strong forms of prime constellation conjectures.

---

**31\. Grimm's Conjecture**

* **Status**: Proven for many cases  
* **What solves it**: Prove consecutive composites n+1,...,n+k can each be assigned distinct prime divisors  
* **Proof type**: ∀-PROOF \+ NUMBER-THEORETIC.  
* **Hard truth**: Connected to prime gap estimates.

---

**32\. Scholz Conjecture**

* **Status**: Known for many n  
* **What solves it**: Prove l(2ⁿ-1) ≤ n-1 \+ l(n) where l is addition chain length  
* **Proof type**: ∀-PROOF.  
* **Hard truth**: Addition chains are hard to analyze globally.

---

**33\. Singmaster's Conjecture**

* **Status**: No number appears more than 8 times in Pascal's triangle (known)  
* **What solves it**: Prove finite upper bound on multiplicities  
* **Proof type**: ∀-PROOF.  
* **Hard truth**: Requires understanding all solutions to C(n,k) \= C(m,j).

---

**34\. Gilbreath's Conjecture**

* **Status**: Verified computationally to large bounds  
* **What solves it**: Prove iterated absolute differences of primes always start with 1  
* **Proof type**: ∀-PROOF.  
* **What DOESN'T count**: More computation  
* **Hard truth**: Likely follows from sufficiently strong prime gap bounds, but those bounds are unknown.

---

**35\. Lemoine's Conjecture**

* **Status**: Verified computationally  
* **What solves it**: Prove every odd n \> 5 is p \+ 2q for primes p, q  
* **Proof type**: ∀-PROOF \+ ANALYTIC.  
* **Hard truth**: Similar to Goldbach; "almost all" methods don't give "all."

---

**36\. Erdős–Turán Conjecture on Additive Bases**

* **Status**: Open  
* **What solves it**: Prove if A is asymptotic basis of order 2, then representation function is unbounded  
* **Proof type**: ∀-PROOF.  
* **Hard truth**: Would follow from strong additive combinatorics but those tools not available.

---

**37\. Lander–Parkin–Selfridge Conjecture**

* **Status**: Verified for many cases; some counterexample searches  
* **What solves it**: Prove if Σaᵢᵏ \= Σbⱼᵏ with m \+ n terms, then m \+ n ≥ k  
* **Proof type**: ∀-PROOF or CONSTRUCTIVE counterexample  
* **Hard truth**: Related to Waring's problem variants.

---

**38\. Hall's Conjecture**

* **Status**: Weak forms proven  
* **What solves it**: Prove |x³ \- y²| \> c·x^(1/2-ε) for x³ ≠ y²  
* **Proof type**: ∀-PROOF \+ NUMBER-THEORETIC.  
* **Hard truth**: ABC conjecture would imply it. Otherwise very hard.

---

**39\. Fuglede's Conjecture (low dimensions)**

* **Status**: FALSE in dimensions ≥ 3 (Tao); OPEN in dimensions 1, 2  
* **What solves it**: Determine if spectral ⟺ tiles by translation in ℝ¹ and ℝ²  
* **Proof type**: ∀-PROOF both directions.  
* **Hard truth**: Low dimensions have different character than high.

---

**40\. Pompeiu Problem**

* **Status**: Open for most domains  
* **What solves it**: Characterize domains Ω where f integrating to 0 over all congruent copies implies f ≡ 0  
* **Proof type**: ∀-PROOF \+ ANALYTIC.  
* **Hard truth**: Only balls known to fail Pompeiu property.

---

**41\. Brennan Conjecture**

* **Status**: Partial results  
* **What solves it**: Prove ∫|f'|ᵖ dA \< ∞ for p ∈ (-2, 2/3) and conformal f  
* **Proof type**: ∀-PROOF \+ COMPLEX ANALYSIS.  
* **Hard truth**: Requires deep conformal mapping estimates.

---

**42\. Mean Value Problem**

* **Status**: Open  
* **What solves it**: Prove for polynomial p of degree n and point z, some critical point ζ has |z \- ζ| ≤ |z \- p(z)/p'(z)|  
* **Proof type**: ∀-PROOF \+ COMPLEX ANALYSIS.  
* **Hard truth**: Elegant statement but subtle geometry.

---

**43\. MLC Conjecture (Mandelbrot locally connected)**

* **Status**: Proven for many parameters  
* **What solves it**: Prove Mandelbrot set is locally connected  
* **Proof type**: ∀-PROOF \+ COMPLEX DYNAMICS.  
* **What DOESN'T count**: Proving for specific parameter regions  
* **Hard truth**: Would imply complete topological description of Mandelbrot set. Requires understanding all parameter values simultaneously.

---

**44\. Fatou Conjecture**

* **Status**: Partial results  
* **What solves it**: Prove quadratic family is hyperbolic on dense open set of parameters  
* **Proof type**: ∀-PROOF (for "dense open") \+ COMPLEX DYNAMICS.  
* **Hard truth**: Connected to MLC and other dynamics conjectures.

---

**45\. Weinstein Conjecture**

* **Status**: PROVEN in dimension 3 (Taubes 2007\)  
* **What solves it (higher dim)**: Prove for contact manifolds in higher dimensions  
* **Proof type**: ∀-PROOF \+ SYMPLECTIC/CONTACT GEOMETRY.  
* **Hard truth**: 3D proof uses gauge theory (Seiberg-Witten). Higher dimensions lack these tools.

---

**46\. Kaplan–Yorke Conjecture**

* **Status**: Verified in many systems  
* **What solves it**: Prove Lyapunov dimension \= information dimension for "typical" attractors  
* **Proof type**: ∀-PROOF (for appropriate class of systems).  
* **Hard truth**: "Typical" needs precise definition; different formulations may have different truth values.

---

**47\. Berry–Tabor Conjecture**

* **Status**: Heuristic support; some proven cases  
* **What solves it**: Prove generic integrable quantum systems have Poisson spectral statistics  
* **Proof type**: ∀-PROOF \+ QUANTUM MECHANICS/SPECTRAL THEORY.  
* **Hard truth**: "Generic" is problematic. Rigorous versions challenging.

---

**48\. Quantum Unique Ergodicity**

* **Status**: Proven for some arithmetic surfaces (Lindenstrauss 2006\)  
* **What solves it**: Prove for general negatively curved manifolds  
* **Proof type**: ∀-PROOF \+ SPECTRAL/ERGODIC THEORY.  
* **Hard truth**: Arithmetic cases use number theory. General cases need different tools.

---

**49\. Rota's Basis Conjecture**

* **Status**: Proven for n ≤ 4  
* **What solves it**: Prove n bases of rank-n matroid can be arranged in n×n grid where rows are bases and columns are independent  
* **Proof type**: ∀-PROOF \+ MATROID THEORY.  
* **Hard truth**: Each n requires more complex arguments.

---

**50\. Zauner's Conjecture (SIC-POVMs)**

* **Status**: Proven/constructed for dimensions 2-193 (some via computer)  
* **What solves it**: Prove SIC-POVMs exist in ALL dimensions d  
* **Proof type**: ∀-PROOF (existence) or CONSTRUCTIVE preferred.  
* **What DOESN'T count**: More specific dimensions  
* **Hard truth**: Known cases use algebraic number theory. General proof elusive. Connected to Hilbert's 12th problem.

---

## **Summary: The Hard Truths**

**Problems where "almost all" or probabilistic results exist but DON'T solve the conjecture:**

* Twin Prime (bounded gaps ≠ gap 2\)  
* Goldbach (almost all ≠ all)  
* Collatz (almost all ≠ all)  
* Reconstruction (almost all graphs ≠ all graphs)

**Problems where improving bounds is progress but NOT solution:**

* Frankl's Union-Closed (38% ≠ 50%)  
* Vizing's (1/2 ≠ 1\)  
* Crouzeix's (2 ≠ 1\)  
* Tuza's (2 ≠ 3/2)

**Problems where special cases don't transfer:**

* Inscribed Square (smooth ≠ continuous)  
* Hadwiger Graph (k=6 ≠ all k)  
* Lonely Runner (k=7 ≠ all k)

**Problems likely requiring NEW MATHEMATICS:**

* Collatz  
* Twin Prime (gap exactly 2\)  
* BSD (full statement)  
* Riemann Hypothesis  
* P vs NP

**Problems where COMPUTER-ASSISTED proof is acceptable:**

* Sendov (small degrees)  
* Hadamard (specific orders)  
* Many finite-reduction problems

---

The universal theme: **Mathematics requires ∀ (for all), not ∃ (there exists many) or "with probability 1."** A problem isn't solved until it works for EVERY case, or you've explicitly reduced it to finite checking that computers can verify.

