# The Fractional-Integral Chromatic Gap for the Plane: A Structural Analysis

**Research Date**: 2025-12-12
**Focus**: What the gap between χf(ℝ²) and χ(ℝ²) reveals about geometric structure

---

## Executive Summary

The gap between the fractional chromatic number (~4.0-4.36) and integral chromatic number (5-7) of the plane is **not unusually large** in absolute terms, but it is **structurally revealing**. This gap tells us that the unit distance graph of the plane has a specific kind of rigidity: it admits efficient fractional colorings through weighted independent sets, but these fractional solutions cannot be "rounded" to integral solutions without significant cost. This is a signature of geometric constraint, not combinatorial freedom.

---

## I. Current Bounds

### Fractional Chromatic Number of the Plane

**Historical progression**:
- **Pre-2015**: χf(ℝ²) ≥ 32/9 ≈ 3.556 (from various constructions)
- **2015-2017**: χf(ℝ²) ≥ 76/21 ≈ 3.619 (Cranston and Rabern)
- **2018-2021**: χf(ℝ²) ≥ 383/102 ≈ 3.755 (Polymath16 project)
- **~2021**: χf(ℝ²) ≥ 3.8991 (Bellitto, Pêcher, and Sédillot)
- **~2021**: χf(ℝ²) ≥ 3.9898 (Jaan Parts, unpublished)
- **2023**: **χf(ℝ²) ≥ 4** (breakthrough - proved via geometric fractional chromatic number)

**Upper bound**: χf(ℝ²) ≤ 4.3599 (Hochberg and O'Donnell, 1993)

### Integral Chromatic Number of the Plane

**Known**: 5 ≤ χ(ℝ²) ≤ 7

- **Lower bound**: 5 (de Grey 2018, minimized to 509 vertices by Parts 2021)
- **Upper bound**: 7 (known since 1950)

### The Gap

**Minimum gap**: 5 - 4.36 = **0.64**
**Maximum gap**: 7 - 4.0 = **3.0**
**Most likely gap** (if χ(ℝ²) = 6): 6 - 4.0 = **2.0**

This represents a **12.5% to 75%** relative increase from fractional to integral, depending on the true chromatic number.

---

## II. Comparison with Other Graphs

### Kneser Graphs: The Canonical Example

**Definition**: KG(n,k) has as vertices all k-element subsets of {1,2,...,n}, with edges between disjoint sets.

**Chromatic numbers**:
- χ(KG(n,k)) = n - 2k + 2 (Lovász 1978, using Borsuk-Ulam theorem)
- χf(KG(n,k)) = n/k (from vertex-transitivity and Erdős-Ko-Rado theorem)

**Example gaps**:
- **KG(5,2)** (Petersen graph): χ = 3, χf = 2.5, **gap = 0.5 (20%)**
- **KG(8,2)**: χ = 5, χf = 4, **gap = 1 (25%)**
- **KG(17,3)**: χ = 13, χf = 17/3 ≈ 5.67, **gap ≈ 7.33 (129%)**
- **KG(100,10)**: χ = 82, χf = 10, **gap = 72 (720%)**

**Key insight**: Kneser graphs show that fractional-integral gaps can be **arbitrarily large**. The plane's gap is modest by comparison.

### Mycielski Graphs: Triangle-Free with High Chromatic Number

**Construction**: Mycielski's construction M(G) creates triangle-free graphs with arbitrarily high chromatic number.

**Chromatic numbers**:
- χ(Mₙ) = n (by construction)
- χf(Mₙ) ~ √(2n) as n → ∞ (Larsen et al. 1995)

**Specific values**:
- M₂ = K₂: χ = 2, χf = 2, **gap = 0**
- M₃ = C₅: χ = 3, χf = 2.5, **gap = 0.5 (20%)**
- M₄ (Grötzsch graph): χ = 4, χf = 29/10 = 2.9, **gap = 1.1 (38%)**
- M₅: χ = 5, χf = 941/290 ≈ 3.24, **gap = 1.76 (54%)**
- As n → ∞: χ = n, χf ~ √(2n), **gap ~ n - √(2n) → ∞**

**Key insight**: Triangle-free graphs can have large chromatic numbers with much smaller fractional chromatic numbers. The **gap grows without bound**.

### The Plane in Context

The plane's gap of **0.64 to 3.0** is:
- **Similar to small Kneser graphs** (KG(5,2), KG(8,2))
- **Larger than small Mycielski graphs** (M₃, M₄)
- **Much smaller than large Kneser or Mycielski graphs**

**Conclusion**: The plane's gap is **moderate**, not extreme. What makes it interesting is **what it reveals about geometry**, not its size.

---

## III. What Causes Large Fractional-Integral Gaps?

### Fundamental Relationship

For any graph G:
- χf(G) = min { k/j : G has a j-fold k-coloring }
- χf(G) ≥ n/α(G), with equality for vertex-transitive graphs
- ω(G) ≤ χf(G) ≤ χ(G) (clique number ≤ fractional ≤ integral)

The fractional chromatic number is the **LP relaxation** of the chromatic number:
- **Integral**: Assign each vertex to exactly one color
- **Fractional**: Assign each vertex a weighted combination of independent sets

### Three Structural Causes of Large Gaps

#### 1. **Many Small Independent Sets, No Large Ones** (Kneser Graph Pattern)

**Mechanism**:
- The graph has many independent sets of size α
- But no "near-independent" sets (sets with only a few edges)
- Fractional solutions use many small independent sets with balanced weights
- Integral solutions cannot merge these without violating independence

**Example**: KG(17,3)
- Maximum independent set size: α = C(16,3) = 560
- Total vertices: n = C(17,3) = 680
- χf = 17/3 ≈ 5.67 (very efficient fractional packing)
- χ = 13 (integral coloring requires many more colors)
- **Why the gap?**: The combinatorial structure forces 13 colors, but fractional solutions can "overlap" independent sets in ways that integral solutions cannot.

#### 2. **Local Constraints that Don't Compose Globally** (Mycielski Pattern)

**Mechanism**:
- Local structure allows efficient fractional colorings
- But global structure has no large independent sets
- The graph is constructed to maximize chromatic number while minimizing clique number

**Example**: Mycielski graphs
- Triangle-free (ω = 2), so χf ≥ n/α is the only constraint
- But χ grows linearly while χf grows sub-linearly
- **Why the gap?**: The construction creates long-range dependencies that block large independent sets without creating large cliques.

#### 3. **Geometric Rigidity with Continuous Symmetry** (Plane Pattern)

**Mechanism**:
- The plane has continuous symmetry (translations, rotations)
- Unit-distance constraints create rigid local structure
- Fractional colorings can use "density-based" coloring (measurable sets)
- Integral colorings must respect discrete combinatorial constraints

**Example**: The plane
- Fractional colorings can use Lebesgue-measurable sets with density-based optimization
- Recent proof that χf(ℝ²) ≥ 4 uses **geometric fractional chromatic number** (continuous optimization)
- But integral colorings must partition the entire plane into discrete color classes
- **Why the gap?**: Continuous geometric optimization allows solutions that discrete combinatorics cannot achieve.

---

## IV. What the Gap Reveals About the Plane's Structure

### The LP Integrality Gap Perspective

The fractional chromatic number is the solution to a **linear program**:
```
Minimize: Σ w(S) over all independent sets S
Subject to: For each vertex v, Σ_{S containing v} w(S) ≥ 1
            w(S) ≥ 0 for all S
```

The integral chromatic number is the **integer program** (IP) version where w(S) ∈ {0,1}.

**Integrality gap** = χ(G) / χf(G)

For the plane:
- **Best case**: 5 / 4.36 ≈ 1.15 (15% gap)
- **Worst case**: 7 / 4.0 = 1.75 (75% gap)
- **Likely case**: 6 / 4.0 = 1.5 (50% gap)

### What This Means Structurally

#### 1. **The Plane Has No "Easy Rounding"**

If the fractional optimum were close to integral, standard LP rounding techniques would work:
- Randomized rounding
- Deterministic rounding
- Iterative rounding

But the gap of 1.5-1.75× means **no simple rounding strategy exists**. The fractional solution uses independent sets in a way that cannot be made integral without significant cost.

#### 2. **Independent Sets Are "Incompatible" in a Strong Sense**

A fractional 4-coloring of the plane uses independent sets with weights summing to 4. If these could be "merged" into 5 or 6 colors without much loss, the gap would be small.

The gap reveals that **the independent sets used in the fractional solution overlap in complex ways**:
- They cannot be partitioned into a small number of color classes
- There are no "almost independent" sets (sets with few edges) that could serve as approximate color classes
- The geometric constraints create a rigid structure where fractional overlap is easy but discrete partition is hard

#### 3. **Continuous vs. Discrete: A Fundamental Tension**

The plane's unit-distance graph is **geometrically defined** but **combinatorially structured**:
- **Geometric**: Points in ℝ², continuous symmetries (translation, rotation), density-based sets
- **Combinatorial**: Graph with vertices and edges, discrete colorings, finite constructions

The fractional chromatic number lives in the **geometric world**:
- Can use Lebesgue-measurable sets
- Optimizes over continuous densities
- Exploits symmetry through integration

The integral chromatic number lives in the **combinatorial world**:
- Must use discrete partitions
- Cannot "blend" colors
- Limited by finite constructions

**The gap is the cost of moving from continuous to discrete.**

#### 4. **The "Missing Structure" Between 4 and 5-7**

If χf(ℝ²) = 4 and χ(ℝ²) ∈ {5,6,7}, this suggests:
- **4 colors**: Achievable with fractional/measurable methods, but not combinatorially
- **5 colors**: Combinatorially impossible (de Grey 2018)
- **6-7 colors**: Combinatorially sufficient (Pritikin 1998, Isbell 1950)

There is a **"gap regime"** where:
- Fractional solutions exist (4-4.36 colors)
- But they cannot be realized as finite graph colorings
- Until we jump to 5+ colors

**This gap is where geometric optimization outperforms combinatorial optimization.**

---

## V. Connections to Other Structural Invariants

### The Lovász Theta Function

The Lovász theta function ϑ(G) satisfies:
- ω(Ḡ) ≤ ϑ(G) ≤ χ(G) for any graph G (Ḡ = complement)
- ϑ(G) is computable in polynomial time via semidefinite programming
- For perfect graphs, ϑ(G) = χ(G) (no gap)

The fractional chromatic number relates to ϑ via:
- χf(G) ≤ χ(G) always
- ϑ(Ḡ) ≥ χf(G) in general
- For vertex-transitive graphs: χf(G) = n/α(G)

**For the plane**: Computing ϑ(unit-distance graph) is intractable (infinite graph), but the fractional chromatic number provides a **lower bound on any polyhedral relaxation**.

### The Independence Number and Density

For finite unit-distance graphs:
- χf(G) ≥ n/α(G) (always)
- χf(G) = n/α(G) for vertex-transitive graphs (e.g., Kneser graphs)

For the plane:
- The "independence density" is the maximum density of a 1-avoiding set
- Recent results: maximum density ≤ 0.247 (improving Erdős conjecture of 1/4)
- This gives χf(ℝ²) ≥ 1/0.247 ≈ 4.05

**The gap between χf and χ reflects the gap between "density optimization" (continuous) and "graph coloring" (discrete).**

### Measurable vs. Combinatorial Chromatic Number

**Variants of the chromatic number**:
- **χ(ℝ²)**: Chromatic number (arbitrary Borel sets)
- **χm(ℝ²)**: Measurable chromatic number (Lebesgue-measurable sets)
- **χmap(ℝ²)**: Map chromatic number (finite polygons)
- **χf(ℝ²)**: Fractional chromatic number (weighted independent sets)

**Known bounds**:
- χf(ℝ²) ≥ 4 (2023)
- χm(ℝ²) ≥ 5 (Falconer 1981)
- χmap(ℝ²) ≥ 7 for arbitrary polygons (2025)
- 5 ≤ χ(ℝ²) ≤ 7

**Hierarchy**:
```
χf(ℝ²) ≤ χm(ℝ²) ≤ χ(ℝ²) ≤ χmap(ℝ²)
  ≥4        ≥5        5-7        ≥7
```

The gaps between these variants reflect **increasing levels of structure**:
- Fractional → Measurable: Discretization cost (~0-1 colors)
- Measurable → Combinatorial: Unknown (~0-2 colors)
- Combinatorial → Map: Polygonal constraint (~0-2 colors)

---

## VI. The Deep Structural Question

### What Does the Gap Tell Us About the True Value of χ(ℝ²)?

**Hypothesis 1: χ(ℝ²) = 5**
- Gap: 5 - 4 = 1 (25%)
- Interpretation: The fractional optimum is close to tight. Rounding cost is minimal.
- **Problem**: No construction achieves 5 colors, despite intense search.
- **Likelihood**: Low (mounting evidence suggests χ(ℝ²) ≥ 6)

**Hypothesis 2: χ(ℝ²) = 6**
- Gap: 6 - 4 = 2 (50%)
- Interpretation: Significant rounding cost. The geometric structure resists discrete partition.
- **Evidence**:
  - Measurable chromatic number ≥ 5 (Falconer)
  - Best 6-colorings of the plane have improved properties (Mundinger et al. 2024)
  - Pritikin's bound: any 6-chromatic graph needs >6,197 vertices (structural threshold)
- **Likelihood**: High

**Hypothesis 3: χ(ℝ²) = 7**
- Gap: 7 - 4 = 3 (75%)
- Interpretation: Large rounding cost. The plane is combinatorially rigid in a strong way.
- **Evidence**:
  - Map chromatic number ≥ 7 for arbitrary polygons
  - 7-colorings have been known since 1950 (easy upper bound)
- **Likelihood**: Moderate

### The Structural Signature

The gap of **1-3 colors** (25-75%) suggests:
- The plane is **not perfect** (perfect graphs have χf = χ)
- The plane is **not Kneser-like** (Kneser graphs have much larger gaps for similar sizes)
- The plane is **geometrically constrained** (continuous optimization ≠ discrete optimization)

**Key insight**: The plane sits in a **"middle regime"** where:
- Fractional methods are powerful (χf ≈ 4)
- But discrete methods require significantly more resources (χ ∈ {6,7} likely)
- The gap is **not extreme** but **structurally revealing**

---

## VII. Open Questions Highlighted by the Gap

### 1. Can We Close the Fractional Upper Bound?

**Current**: 4.0 ≤ χf(ℝ²) ≤ 4.3599

If χf(ℝ²) = 4.0 exactly, this would be a **remarkable coincidence** (rational value for a geometric constant). More likely χf(ℝ²) is irrational and somewhere in (4, 4.36).

**Tightening this bound would reveal**:
- How much "slack" is in the fractional relaxation
- Whether 4.0 is the true value (special structure) or just a lower bound

### 2. Is There a "Gap Theorem"?

**Question**: For unit-distance graphs, is there a structural theorem relating the fractional-integral gap to other graph invariants?

**Possible form**:
```
χ(G) / χf(G) ≤ f(ω(G), Δ(G), girth(G), ...)
```
where f is some function of clique number, max degree, girth, etc.

**For the plane**:
- ω(unit-distance graph) = ∞ (infinite cliques exist)
- Δ(unit-distance graph) = ∞ (vertices can have infinite degree)
- But local properties might still constrain the gap

### 3. Can Fractional Insights Guide Integral Constructions?

**Current approach**: Try to find finite 6-chromatic graphs by brute force (blocked by Pritikin's 6,197-vertex bound).

**Alternative**: Use the fractional 4-coloring structure to **guide construction**:
- Identify which independent sets are used in the optimal fractional solution
- Understand why they cannot be merged into 5 colors
- Construct graphs that "force" the separation

**This could reveal**:
- What makes a graph 6-chromatic (structural principles)
- Whether the gap is "continuous" (can we get graphs with χf approaching 4 from below while χ → 6?)

### 4. What Is the Geometric Fractional Chromatic Number?

The 2023 proof that χf(ℝ²) ≥ 4 uses a new concept: **geometric fractional chromatic number** χgf(G):
- For geometric graphs, considers "density-avoiding sets" instead of just independent sets
- Relates to measurable colorings and density bounds

**Question**: What is χgf(ℝ²) exactly, and how does it relate to χf(ℝ²)?

If χgf(ℝ²) < χf(ℝ²), this reveals a **new layer of structure** between continuous and discrete.

---

## VIII. Synthesis: The Mathematical Insight

### The Gap as a Diagnostic

The fractional-integral chromatic gap is **not just a number**—it is a **structural diagnostic** that reveals:

1. **Rounding Hardness**: How difficult is it to convert continuous optimization to discrete?
2. **Independent Set Structure**: Are there many small independent sets (wide gap) or few large ones (narrow gap)?
3. **Geometric vs. Combinatorial**: How much does continuous symmetry help vs. discrete structure?

For the plane, a gap of **1-3 colors** tells us:
- **Moderate rounding hardness**: Not trivial (like perfect graphs) but not extreme (like large Kneser graphs)
- **Complex independent set structure**: No simple partition of fractional solutions into integral colors
- **Geometric optimization wins**: Continuous methods outperform discrete by 25-75%

### Why This Matters

The Hadwiger-Nelson problem is not just "what is χ(ℝ²)?"—it is **"what is the relationship between geometric and combinatorial structure in Euclidean space?"**

The fractional-integral gap is a **window into this relationship**:
- It shows that geometry provides "fractional resources" (density, symmetry, continuity)
- But combinatorics imposes "discrete costs" (partitioning, no overlaps)
- The gap measures this cost

### The Plane Is Not Special—It's Typical

Compared to other graphs:
- Kneser graphs: Larger gaps (combinatorial structure)
- Mycielski graphs: Larger gaps (triangle-free + high chromatic)
- The plane: **Moderate gap** (geometric structure)

What makes the plane **interesting** is not the size of the gap, but **what it reveals**:
- A 1-3 color gap for an infinite geometric graph
- Arising from continuous vs. discrete optimization
- Reflecting deep constraints in how Euclidean space can be partitioned

### The Central Mystery

**Why does the plane need 5-7 colors when fractional methods suggest ~4?**

The gap tells us: **because discrete combinatorial structure cannot capture the full power of continuous geometric optimization.**

The fractional chromatic number of 4 reflects what is possible with:
- Weighted independent sets
- Continuous densities
- Geometric symmetry

The integral chromatic number of 5-7 reflects what is required when:
- Each point gets exactly one color
- Colors partition the plane into discrete regions
- Finite constructions must work

**The gap is the price of discretization in geometric space.**

---

## IX. Conclusion

The fractional-integral chromatic gap for the plane (0.64 to 3.0 colors, likely ~2) is **structurally revealing, not statistically unusual**.

**What it tells us**:
1. **The LP relaxation is loose**: Fractional solutions cannot be easily rounded to integral solutions.
2. **Independent sets are incompatible**: The independent sets used in fractional colorings overlap in complex, geometrically constrained ways.
3. **Continuous ≠ Discrete**: Geometric optimization (densities, symmetry) outperforms combinatorial optimization (discrete partitions) by 25-75%.
4. **The plane is in a middle regime**: Not perfect (no gap) but not extreme (Kneser-like). The gap reflects geometric rigidity, not combinatorial freedom.

**What it predicts**:
- χ(ℝ²) is likely **6 or 7** (not 5), given the substantial gap
- Any proof will need to **bridge continuous and discrete** methods
- The structure that forces ≥5 colors is **qualitatively different** from the structure that allows ~4 fractional colors

**The deep insight**: The gap is not a curiosity—it is a **signature of how Euclidean geometry resists discrete combinatorial partition**. Understanding this gap is understanding the Hadwiger-Nelson problem.

---

## References and Sources

### Fractional Chromatic Number Bounds
- [The fractional chromatic number of the plane is at least 4 (2023)](https://arxiv.org/html/2311.10069)
- [The Fractional Chromatic Number of the Plane (Hochberg & O'Donnell)](https://landon.github.io/graphdata/Papers/plane-fractional-chromatic.pdf)
- [The fractional chromatic number of the plane | Combinatorica](https://link.springer.com/article/10.1007/s00493-016-3380-3)

### Kneser Graphs
- [Kneser graph - Wikipedia](https://en.wikipedia.org/wiki/Kneser_graph)
- [Fractional coloring - Wikipedia](https://en.wikipedia.org/wiki/Fractional_coloring)
- [Kneser Graphs and the EKR Theorem](https://smahesh.com/kneser-graphs/)

### Mycielski Graphs
- [The fractional chromatic number of mycielski's graphs (Larsen et al. 1995)](https://onlinelibrary.wiley.com/doi/abs/10.1002/jgt.3190190313)
- [Mycielskian - Wikipedia](https://en.wikipedia.org/wiki/Mycielskian)

### Independence Number and Structure
- [Fractional Chromatic Number, Maximum Degree, and Girth](https://epubs.siam.org/doi/10.1137/20M1382283)
- [On the independence ratio of distance graphs](https://arxiv.org/abs/1401.7183)

### Lovász Theta Function
- [Lovász number - Wikipedia](https://en.wikipedia.org/wiki/Lov%C3%A1sz_number)
- [Geometric Ramifications of the Lovász Theta Function](https://uwspace.uwaterloo.ca/handle/10012/7812)

### Integrality Gaps
- [Linear programming relaxation - Wikipedia](https://en.wikipedia.org/wiki/Linear_programming_relaxation)
- [Integrality Gap of the Vertex Cover LP](https://ar5iv.labs.arxiv.org/html/1907.11209)

### General Hadwiger-Nelson
- [Hadwiger–Nelson problem - Wikipedia](https://en.wikipedia.org/wiki/Hadwiger–Nelson_problem)
- [The chromatic number of the plane is at least 5 (de Grey 2018)](https://arxiv.org/abs/1804.02385)
- [Hadwiger-Nelson Problem - Polymath Wiki](https://michaelnielsen.org/polymath/index.php?title=Hadwiger-Nelson_problem)
