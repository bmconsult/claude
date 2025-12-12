# Computational Approaches to the Hadwiger-Nelson Problem

**Research Date**: 2025-12-12
**Focus**: SAT-based methods, exhaustive search, and the quest for 6-chromatic unit-distance graphs

## Executive Summary

The Hadwiger-Nelson problem asks: What is the minimum number of colors needed to color the plane such that no two points at unit distance have the same color? Currently known to be 5, 6, or 7.

**Key Finding**: A computational path to finding a 6-chromatic graph exists in theory but is **currently prohibitive**. Pritikin (1998) proved that any 6-chromatic unit-distance graph requires **at least 6,198 vertices**, while current SAT methods struggle with graphs beyond ~500 vertices for chromatic verification.

---

## 1. SAT Encoding of Unit-Distance Graph Coloring

### Basic Encoding

**Assignment Encoding** (standard approach):
- For graph G=(V,E) with k colors, use k|V| Boolean variables: x_{i,j}
- x_{i,j} = true means vertex i gets color j
- Constraints encoded as CNF clauses:
  - **Each vertex has a color**: x_{i,1} ∨ x_{i,2} ∨ ... ∨ x_{i,k}
  - **Adjacent vertices differ**: (¬x_{i,c} ∨ ¬x_{j,c}) for each edge (i,j) and color c
  - **At-most-one color per vertex**: (¬x_{i,c} ∨ ¬x_{i,d}) for c ≠ d

### Symmetry Problem

The assignment encoding contains massive symmetry: any permutation of color classes yields an equivalent solution, creating k! redundant search paths. For k=4 colors, this means 24× redundant search space; for k=6, it's 720×.

### Heule's Approach (2018)

Marijn Heule developed a sophisticated SAT-based minimization procedure:

1. **Encode the property test**: "Does graph M have a 4-coloring where subgraph H avoids property P?"
2. **Generate unsatisfiability proof**: Use CDCL SAT solvers to prove no such coloring exists
3. **Extract minimal core**: Use DRAT-trim tool to identify which vertices were actually needed in the proof
4. **Iterate**: Remove unused vertices, repeat

**Computational Cost**: Finding the 529-vertex 5-chromatic graph required ~100,000 CPU-hours.

### CDCL Solvers Used

All modern approaches use Conflict-Driven Clause Learning (CDCL) solvers:
- MiniSat, Glucose 4, Glucose-syrup (multithreaded)
- MapleLCMDistChronoBT-DLv3
- plingeling, painless-mcomsps
- Kissat

These solvers can emit not just SAT/UNSAT results but also:
- Clausal proofs of unsatisfiability
- Unsatisfiable cores (minimal subgraphs that preserve the property)
- Craig interpolants

---

## 2. State of the Art: Finding Large Chromatic Graphs

### 5-Chromatic Unit-Distance Graphs (Lower Bound Progress)

**Historical trajectory**:
- **2018**: de Grey discovers 1581-vertex 5-chromatic graph (original breakthrough)
- **2018**: Heule reduces to 553 vertices using SAT-based minimization
- **2018**: Heule further reduces to 517 vertices
- **2018**: Heule finds 529-vertex graph after 100,000 CPU-hours
- **2021**: Parts finds **509-vertex** 5-chromatic graph (current record)

All these graphs are based on using many copies of the **Moser spindle** (a 7-vertex 4-chromatic unit-distance graph) as structural building blocks.

**Alternative constructions**: Parts (2021) constructed 5-chromatic graphs with 64,513 vertices that do NOT use the Moser spindle, showing diversity in construction methods.

### 4-Chromatic Bounds

Pritikin (1998) proved: **All unit-distance graphs with ≤12 vertices are 4-colorable**

This tight bound was established via exhaustive search.

### Construction Methodology

**Heule's rotation-union technique**:
1. Start with a vertex set whose unit-distance graph contains many Moser spindles
2. Create a union with a rotated copy around a common symmetry center
3. Verify non-4-colorability via SAT
4. Minimize using proof-based core extraction

---

## 3. Attempts at 6-Chromaticity via Exhaustive Search

### The Fundamental Barrier: Pritikin's 6197-Vertex Lower Bound

**Pritikin (1998)**: "All unit-distance graphs of order 6197 are 6-colorable"

**Method**: Constructed a 6-coloring of nearly all the plane using a heptagonal+diamond tiling (modified hexagonal tiling). This proves:
- Any 7-chromatic unit-distance graph needs **≥6,198 vertices**
- Any 6-chromatic unit-distance graph needs **>6,197 vertices**

**Color density used**: Pritikin relied on Croft's (1967) densest known unit-distance-avoiding sets with density 0.22936. These have held the record for over 55 years.

### Polymath16 Third Thread: "Is 6-Chromatic Within Reach?"

The Polymath16 collaborative project explicitly investigated whether finding a 6-chromatic unit-distance graph was computationally feasible.

**Conclusion**: The methods are "computationally daunting" but theoretically possible. The problem is that:
- Current SAT methods handle ~500 vertices for chromatic verification
- A 6-chromatic graph needs >6,197 vertices
- That's a **12×+ gap** between what we can verify and what we need

**Heuristic argument**: The true chromatic number is likely 6 or 7 (not 5), so a 6-chromatic graph "should" exist, but finding it requires bridging this computational gap.

### 3D Results (Easier Problem)

For comparison: Researchers constructed a **79-vertex 6-chromatic unit-distance graph in ℝ³** by refining Nechushtan's approach. The 3D problem is more tractable because the chromatic number is known to be between 6 and 15.

---

## 4. Computational Limits: How Big a Graph Can We Check?

### Current Capabilities

**SAT-based graph coloring** (exact methods):
- **Sparse graphs**: Up to ~14,000 vertices (but only for easy instances)
- **Dense graphs**: Hundreds of thousands of vertices using hybrid methods
- **Unit-distance chromatic verification**: ~500 vertices is practical; 1,581 vertices required massive parallelization

**The scalability cliff**:
- Exact SAT/CP/ILP methods don't scale beyond a few thousand vertices for hard instances
- The encoding size becomes prohibitively large
- For unit-distance graphs with high chromatic number, even 1,000+ vertices requires extreme computational resources

### Hybrid Approaches for Larger Graphs

**GC-SLIM** (SAT-boosted tabu search, 2023):
- Combines local search (tabu) with SAT solving for small subgraphs
- Scales to graphs with **hundreds of thousands of vertices** and **1.5+ billion edges**
- But this is for general graph coloring, not unit-distance graphs with geometric constraints

### Why Unit-Distance Graphs Are Harder

Unit-distance graphs have special structure:
- Geometric realizability constraints
- Dense local structure (high edge density)
- Chromatic number verification requires proving non-colorability
- Unsatisfiability proofs are exponentially harder than satisfiability proofs

### The 6,197-Vertex Gap

**Current state**:
- We can verify 5-chromatic graphs up to ~1,500 vertices with massive compute
- We need to verify 6-chromatic graphs with >6,197 vertices
- **This is a 4-10× gap in problem size**

**Computational scaling**: SAT solver time typically grows exponentially with problem size. Even a 2× increase in vertices can mean 10-100× longer solving time for hard instances.

---

## 5. Symmetry-Breaking Techniques

### The Color Symmetry Problem

For k colors, there are k! equivalent solutions (permutations of color labels):
- k=4: 24 equivalent solutions per actual coloring
- k=6: 720 equivalent solutions
- k=7: 5,040 equivalent solutions

This massively expands the search space.

### Clique-Based Symmetry Breaking

**Standard technique**:
1. Find a maximum clique in the graph
2. Fix the colors of clique vertices (assign vertex i to color i)
3. This breaks all color permutation symmetries

**For unit-distance graphs**: Finding large cliques is itself hard, but small cliques (3-4 vertices) can still provide significant symmetry reduction.

### Partial Ordering Models

**Alternative encoding** (Mendez-Diaz & Zabala):
- Instead of assigning colors, define a partial order on vertices
- Encode: "vertex i comes before vertex j in the color ordering"
- This naturally breaks color symmetry
- Works well for sparse graphs

### Zykov Tree Encoding

**Recent innovation** (ZykovColor solver):
- Branch on vertex pairs: "Do non-adjacent vertices i,j get the same color?"
  - If YES: contract them (merge into single vertex)
  - If NO: add edge between them (now they're adjacent)
- This encoding has **no color symmetry** inherently
- Requires transitivity constraints (if i≡j and j≡k, then i≡k)
- Uses advanced SAT features (IPASIR-UP interface) for efficient propagation

### Polymath16 Symmetry Breaking

Python code on Polymath wiki converts DIMACS edge lists to CNF with:
- Forced color assignments for up to 3 vertices
- This breaks some (not all) color symmetries
- Trade-off: reduces search space but adds constraints

### Sequential Encoding for At-Most-One

**Technical detail**: To ensure each vertex gets at most one color, use sequential encoding:
- Build a "count-and-compare" circuit in hardware
- Translate to CNF clauses
- More efficient than naive pairwise constraints

---

## 6. Is There a Computational Path to 6-Chromatic?

### Theoretical Obstacles

1. **Size barrier**: Need >6,197 vertices (Pritikin's bound)
2. **Verification barrier**: Current methods struggle at ~500-1,500 vertices
3. **Construction barrier**: No known systematic construction method (unlike 5-chromatic graphs which use Moser spindles)

### Potential Approaches

#### Approach 1: Brute-Force SAT Scaling
- Wait for Moore's law + algorithmic improvements
- Estimate: Need 100-1000× speedup to reach 6,197 vertices
- Timeline: 10-20 years at current progress rates

#### Approach 2: Better Construction Heuristics
- Find structural principles like the Moser spindle for 5-chromatic graphs
- Use geometric or algebraic insights to guide construction
- **Problem**: We don't know what makes a graph 6-chromatic

#### Approach 3: Exploit Measurable Chromatic Number Results
- Falconer (1981): Measurable chromatic number ≥5
- Woodall (1973) / Townsend (1981): Map-type colorings require ≥6 colors
- Recent (2025): Polygonal colorings require ≥7 colors
- **Idea**: Construct graphs that force certain geometric structure

#### Approach 4: Neural Network-Guided Search (2024)
- Mundinger et al. (2024) used neural networks for 6-coloring exploration
- Reformulate as differentiable optimization problem
- Found first improvements to off-diagonal Hadwiger-Nelson in 30 years
- **Extension**: Could guide search for 6-chromatic graphs

#### Approach 5: 3D → 2D Projection
- 6-chromatic graphs exist in ℝ³ (79 vertices)
- Could study which 3D configurations project to difficult 2D graphs
- May provide structural insights

### Verdict on Computational Feasibility

**Short term (2025-2030)**: **Not feasible** with current methods
- The gap between 500-vertex capability and 6,197-vertex requirement is too large
- No known construction principles to guide search

**Medium term (2030-2040)**: **Possibly feasible** with breakthrough insights
- If we discover structural principles (like Moser spindle for 5-chromatic)
- If neural network or other AI-guided methods find promising substructures
- If SAT solvers improve 100× in efficiency (optimistic)

**Long term (2040+)**: **Likely feasible** with sufficient compute
- Quantum computers might help (though unclear how much)
- Continued exponential growth in compute power
- Accumulation of algorithmic improvements

---

## 7. Alternative Research Directions

Given the computational barriers to finding 6-chromatic graphs, researchers have pursued:

### Fractional Chromatic Number
- Prove χ_f(ℝ²) ≥ 4 (achieved 2023)
- Tighter bounds constrain possible integer chromatic number

### Six-Colorings of the Plane
- Mundinger et al. (2024): "Extending the Continuum of Six-Colorings"
- Shows that 6-colorings exist with improved properties
- Suggests χ(ℝ²) might be exactly 6

### Measurable and Map-Type Variants
- Recent (2025): Map colorings require ≥7 colors for arbitrary polygons
- These restrictions might be more tractable than full problem

### Upper Bound Improvements
- Current upper bound is 7 (since 1950!)
- Proving χ(ℝ²) ≤ 6 would solve the problem
- No computational approach to this; requires new mathematical ideas

---

## Key Papers and Resources

### Foundational Results
- **de Grey (2018)**: "The chromatic number of the plane is at least 5" - arXiv:1804.02385
- **Heule (2018)**: "Computing Small Unit-Distance Graphs with Chromatic Number 5" - Geombinatorics 28:32-50
- **Pritikin (1998)**: "All unit-distance graphs of order 6197 are 6-colorable" - J. Combin. Theory Ser. B 73(2):159–163

### Recent Advances
- **Mundinger et al. (2024)**: "Extending the Continuum of Six-Colorings" - arXiv:2404.05509
- **Neural network approaches (2024)**: First improvements to off-diagonal Hadwiger-Nelson in 30 years

### Computational Methods
- **SAT encoding**: Assignment variables, symmetry breaking via cliques, Zykov tree
- **CDCL solvers**: MiniSat, Glucose, Kissat, etc.
- **Hybrid methods**: GC-SLIM (SAT-boosted tabu search)

### Collaborative Efforts
- **Polymath16**: Collaborative project on simplifying 5-chromatic graphs and exploring 6-chromatic feasibility
  - Thread 1: Simplifying de Grey's graph
  - Thread 2: What makes graphs 5-chromatic?
  - Thread 3: Is 6-chromatic within reach?

---

## Conclusion

**Is there a computational path to finding a 6-chromatic unit-distance graph?**

**Yes, but it's currently blocked by a severe computational barrier.**

- We know such graphs must have **>6,197 vertices** (Pritikin 1998)
- We can verify graphs of **~500-1,500 vertices** with massive compute
- This **4-10× size gap** translates to 100-1000× computational gap

**Most promising paths forward**:
1. **Structural insights**: Discover construction principles (like Moser spindle enabled 5-chromatic graphs)
2. **AI-guided search**: Use neural networks to find promising substructures
3. **Moore's law**: Wait 10-20 years for 100× speedup in SAT solving
4. **Hybrid approaches**: Combine geometric insights with computational verification

**Bottom line**: The computational path exists in theory but requires either breakthrough mathematical insights or another 1-2 decades of computational progress. The problem is not impossible, just currently beyond reach.
