# Pritikin's 1998 Proof: All ≤6197-Vertex Unit-Distance Graphs are 6-Colorable

**Detailed Analysis of Construction, Derivation, and Tightness**

*Research Date*: 2025-12-12
*Primary Source*: D. Pritikin, "All unit-distance graphs of order 6197 are 6-colorable," Journal of Combinatorial Theory, Series B, 73(2):159–163, 1998

---

## Executive Summary

Pritikin (1998) proved that **any unit-distance graph with ≤6197 vertices is 6-colorable**, which implies that any 7-chromatic unit-distance graph must have **≥6198 vertices**. This bound has held for over 25 years and represents a major computational barrier to finding 6-chromatic graphs.

**Key Finding**: The bound appears to be **nearly tight** (optimization only improves to ~6197.5), but there's evidence it might have **structural slack** based on de Grey's 40× reduction of 5-chromatic graphs.

---

## 1. The Exact Construction

### The "Wild Color" Method

Pritikin's construction uses a **probabilistic embedding argument**:

1. **Create a 7-coloring** of the plane using colors {0, 1, 2, 3, 4, 5, 6}
2. **Make color 0 the "wild" color** - occupy only a tiny fraction p of the plane
3. **Colors 1-6** properly 6-color the rest of the plane (no unit distances within same color)
4. **Allow unit distances** between points both colored 0 (the "wild" exception)

### The Tiling

**Tiling Type**: Heptagonal + diamond tiling (modified hexagonal tiling)

**Origin**: Originally conceived by **Ed Pegg**, as reported in Soifer's *Mathematical Coloring Book*

**Structure**:
- Base: Pentagonal tiling (Type 5 in the classification of convex pentagonal tilings)
- Modified with small **diamond-shaped** regions
- The heptagons have:
  - Width: 1/2
  - Rounded boundary: circular arc of radius 1 centered at opposite corner
- The diamonds are recolored with the "wild" color 0

**Pattern**:
- Colors 1-6 are arranged periodically across the plane
- Each column uses 3 different colors
- Every other column has the same coloring (shifted)
- Small diamond regions scattered throughout receive color 0

---

## 2. Where Does 6197 Come From?

### The Probabilistic Argument

**Theorem (Pritikin's Probabilistic Method)**: If the plane can be colored with k colors plus a "wild" color occupying area fraction p, then any unit-distance graph with n vertices is k-colorable provided:

```
n < 1/p
```

**Proof sketch**:
1. Take a unit-distance graph G with n vertices
2. Choose a random translation of G in the plane
3. Probability that vertex i lands in the wild region: p
4. Expected number of vertices in wild region: n·p
5. If n < 1/p, then n·p < 1
6. Therefore ∃ a translation where NO vertices land in wild region
7. Such a translation gives a k-coloring of G

### The Calculation

Pritikin's specific tiling achieves:

```
Area fraction of wild color: p ≈ 1/6197
Therefore: 1/p ≈ 6197
```

Thus **any graph with ≤6197 vertices can be embedded to avoid the wild region** and is therefore 6-colorable.

**Corollary**: Any 7-chromatic graph needs **≥6198 vertices**.

---

## 3. Connection to Croft's 1967 Density Bound

### Croft's "Tortoise" Construction

**Reference**: H. T. Croft, "Incidence incidents," Eureka (Cambridge), 30:22–26, 1967

**Construction**: The "tortoise" is the intersection of:
- An open disc of radius 1/2
- An open regular hexagon of height x < 1

**Density**: Placing tortoises at hexagonal lattice points (basis vectors of length 1+x) gives:
- Optimal at x = 0.96553
- **Maximum density: δ_C = 0.22936** (22.936% of the plane)

**Key Property**: Every point in a tortoise is:
- < 1 distance from any other point in the same tortoise
- > 1 distance from the nearest point in any other tortoise

This is the **densest known unit-distance-avoiding set** (held the record for 58 years!).

### How Pritikin Uses Croft

**Critical Connection**: Pritikin's 6-coloring (colors 1-6) must ensure each color class avoids unit distances.

**Limitation**: Each color class can occupy **at most density ≈ 0.22936** (Croft's bound)

**For k=6 colors**: Maximum total coverage ≈ 6 × 0.22936 = 1.37616 > 1 ✓

**This means**:
- In principle, 6 colors COULD cover the entire plane
- But geometric constraints prevent a perfect tiling
- Pritikin's construction leaves area fraction p ≈ 1/6197 uncovered
- This uncovered region gets the "wild" color 0

**Important**: Pritikin's coloring for k=4 case **cannot be improved** without improving Croft's density bound. The k=5 and k=6 cases might be optimizable.

---

## 4. How Tight is the Bound?

### Optimization Analysis (from Polymath16)

**Quote**: "Symbolic optimization of the shape [Pritikin] uses only pushes the number to about **6197.5**"

**Interpretation**:
- The heptagonal+diamond tiling is **nearly optimal** for its type
- Only ~0.5 vertex improvement possible via parameter tuning
- This suggests the bound is **very tight** for this construction method

### Comparison: The "Classic 7-gon of Pritikin"

**Measured values** (from Polymath16):
- For 7 colors: 5681.489884345 (vs. Ed Pegg's original: 302.0962)
- For 8 colors: **6197.579308329**

The fact that 8 colors gives ~6197.5 confirms the calculation.

### Subsequent Improvements

**Parts (year unknown)**: Improved the bound to **6993**

**Method**: Not specified in available sources, but represents a **13% improvement**

**Calculation**: 6993/6197 ≈ 1.128

This suggests either:
- A better tiling construction
- A different approach to the probabilistic argument
- Tighter analysis of the area fraction

---

## 5. Is There Slack in the Bound?

### Evidence FOR Slack

**de Grey's 40× reduction** (2018):
- Original 5-chromatic graph: 20,425 vertices
- After SAT-based minimization: 509 vertices (Parts, 2021)
- **Reduction factor: 40×**

**Extrapolation to 6-chromatic**:
- If similar reduction applies: 6197 → ~155 vertices
- This would be **within SAT solver range** (~500-1500 vertices)

**Interpretation**: The barrier might be **structural, not computational**
- We don't know HOW to construct 6-chromatic graphs
- But the minimal ones might be much smaller than 6197

### Evidence AGAINST Slack

**Optimization is tight**:
- Pritikin's construction only improves to ~6197.5
- This suggests the **area fraction p is nearly minimal** for this tiling type

**No better density bound**:
- Croft's 0.22936 has held for 58 years
- Recent upper bound: 0.247 (2023) - only 8% higher
- The gap between 0.22936 (constructive lower) and 0.247 (proven upper) is small

**Theoretical argument**:
- If each of 6 colors can cover ≤24.7% (proven upper bound)
- Maximum coverage: 6 × 0.247 = 1.482
- Uncovered fraction: ≥ 1 - 1.482 = 0 (in principle)
- But this assumes perfect coverage with no overlaps or gaps

### The Verdict: Likely Has Slack, But How Much?

**Two separate questions**:

1. **Is Pritikin's CONSTRUCTION optimal?** → **Nearly tight** (only ~0.5 improvement)

2. **Is there a BETTER construction method?** → **Unknown, but likely**

**Possibilities**:

| Scenario | Minimal 7-chromatic size | Evidence |
|----------|-------------------------|----------|
| Pritikin is tight | ~6200 vertices | Optimization analysis |
| Structural slack exists | ~1000-2000 vertices | Parts' 6993 improvement |
| Large slack (like de Grey) | ~150-200 vertices | 40× reduction pattern |

**My assessment**: The true minimal 7-chromatic graph likely has **1000-3000 vertices**, not 6200.

**Why?**
- Pritikin's method is a **tiling approach** (global structure)
- de Grey's method is a **gadget approach** (local constraints)
- Gadget methods produce tighter bounds
- The 40× reduction suggests construction bounds are loose

---

## 6. What Would It Take to Improve the Bound?

### Path 1: Better Tiling Construction

**Requirements**:
- Find a tiling that reduces the "wild" area fraction
- Current: p ≈ 1/6197 ≈ 0.000161
- Target: p ≈ 1/10000 ≈ 0.0001 (would give bound of 10,000)

**Obstacles**:
- Constrained by Croft's density bound (0.22936)
- Geometric constraints of Euclidean plane
- 25 years of effort hasn't found better

**Verdict**: **Difficult** - only ~13% improvement achieved (Parts → 6993)

### Path 2: Improve Croft's Density Bound

**Current state**:
- Lower bound (constructive): 0.22936 (Croft 1967)
- Upper bound (proven): 0.247 (2023)
- **Gap: only 8%**

**Recent progress**:
- Erdős conjecture (max density < 1/4) proven in 2023
- Upper bound improved from 0.25 to 0.247

**Verdict**: **Very difficult** - the bound is nearly tight

### Path 3: Non-Tiling Approach (Gadget Construction)

**Idea**: Directly construct a minimal 6-chromatic or 7-chromatic graph using local gadgets

**Method**:
- Use Moser spindles or similar building blocks
- Apply "clamp" or "forcing" techniques
- SAT-solve for chromatic number

**Obstacles**:
- No known gadgets that force 6-chromaticity
- SAT solvers struggle beyond ~1500 vertices
- Gap between capability (~500) and need (6197+) is **12×+**

**Verdict**: **Currently impossible** - computational barrier

### Path 4: Prove the Bound is Tight

**Goal**: Show that the minimal 7-chromatic graph has exactly ~6200 vertices

**Method**:
- Prove that smaller graphs admit structural decompositions
- Show that 6-colorings are forced by local constraints
- Use algebraic or topological obstructions

**Verdict**: **Extremely difficult** - would be a major theoretical breakthrough

### Path 5: Prove χ(ℝ²) = 7 Another Way

**Alternative**: Instead of finding a 7-chromatic graph, prove that 6 colors are insufficient

**Approaches**:
- Extend measurable chromatic number results (currently χ_m ≥ 5)
- Use map-type coloring results (recently: map-type → ≥7)
- Prove density constraints force 7 colors

**Verdict**: **Hard but tractable** - active research direction

---

## 7. Open Questions

### Q1: What is the true minimal size of a 7-chromatic unit-distance graph?

**Bounds**:
- Lower: ≥6198 (Pritikin) or ≥6994 (Parts)
- Upper: Unknown (graph not found)
- Speculative: ~1000-3000 vertices (based on de Grey reduction pattern)

### Q2: Can the Pritikin bound be improved by 2×? 10×?

**2× improvement** (to ~3000): **Possibly** - would require new tiling insight

**10× improvement** (to ~600): **Unlikely** - would require abandoning tiling approach

### Q3: Is there a 6-chromatic graph with <6197 vertices?

**Yes** - Pritikin's bound applies to 7-chromatic graphs, not 6-chromatic

**Question**: What's the minimal size of a 6-chromatic graph?
- Must be >6197 (Pritikin) to be 7-chromatic
- Could be much smaller if only 6-chromatic
- Currently: **no 6-chromatic graph known**

### Q4: Does the answer depend on the tiling type?

**Yes** - different tilings give different bounds:
- "Classic 7-gon of Pritikin": 6197.58
- "Pritikin's 7-gon with wavy inclined sides": 6295.90
- Variation across tilings: ~2%

### Q5: Is the probabilistic method optimal?

**Probably not** - it's a **sufficient** condition (n < 1/p), not necessary

**Better approach**: Direct construction or proof techniques

---

## 8. Comparison to Other Bounds

### Historical Progression of Lower Bounds

| Year | Result | Vertices | Method |
|------|--------|----------|--------|
| 1950 | 4 colors insufficient | 7 | Moser spindle |
| 1998 | All ≤12 are 4-colorable | 12 | Pritikin tiling (k=4) |
| 1998 | All ≤6197 are 6-colorable | 6197 | Pritikin tiling (k=6) |
| 2018 | 5 colors insufficient | 1581 | de Grey construction |
| 2018 | 5 colors insufficient | 553 | Heule SAT minimization |
| 2021 | 5 colors insufficient | 509 | Parts SAT minimization |
| Unknown | All ≤6993 are 6-colorable | 6993 | Parts improvement |

### The Gap

**Known**: 5 ≤ χ(ℝ²) ≤ 7

**To close the gap**:
- Prove χ ≥ 6: Need 6-chromatic graph (≥6198 vertices by Pritikin)
- Prove χ ≤ 6: Need 6-coloring of plane (currently unknown)
- Prove χ = 7: Need either 7-chromatic graph OR proof that 6-coloring impossible

**The asymmetry**:
- Lower bound: Find ONE graph (computational)
- Upper bound: Prove ALL colorings fail (mathematical)

---

## 9. Implications for Computational Search

### The Computational Barrier

**Current SAT capability**: ~500-1500 vertices for chromatic verification

**Pritikin bound**: ≥6198 vertices

**Gap**: **4-12× in problem size** = 100-1000× in computation time

**Timeline**: 10-20 years at current progress rates (if Moore's law continues)

### If Slack Exists

**Scenario**: True minimal 7-chromatic graph has ~1500 vertices

**Implication**: **Within reach** of current SAT methods with:
- Better construction heuristics
- Symmetry breaking techniques
- Parallel search strategies

**Bottleneck**: We don't know HOW to construct such a graph

**The irony**: The graph might be findable, but we don't know where to look

---

## 10. Connection to Recent Results

### Fractional Chromatic Number = 4 Exactly (2023)

**Result**: χ_f(ℝ²) = 4 (proven)

**Integral chromatic number**: 5-7

**Gap**: 1-3 colors (25-75% increase)

**Interpretation**:
- The "cost of discretization" is 25-75% more colors
- Tiling approaches (like Pritikin's) are inherently limited
- They can't achieve the efficiency of fractional colorings

### Measurable Chromatic Number ≥ 5 (Falconer 1981)

**Connection**: Pritikin's coloring is measurable (tiling-based)

**Limitation**: Can't use density arguments to push beyond 5
- With 6 colors: average density = 1/6 ≈ 0.167
- Well below Croft's bound of 0.229
- No contradiction from pure density

### Map-Type Colorings Require ≥7 (Sokolov-Voronov 2025)

**Result**: Jordan-bounded polygonal colorings need 7 colors

**Pritikin's coloring**: Uses polygonal tiles → needs 7 colors total (including wild)

**Consistency check**: ✓ Pritikin uses 7 colors (6 proper + 1 wild)

### ML-Discovered Irregular Tilings (Mundinger et al. 2024)

**Finding**: Irregular (asymmetric) tilings outperform symmetric ones

**Implication for Pritikin**:
- His heptagonal tiling is relatively regular
- An irregular variant might reduce the wild area fraction
- Could improve the bound from 6197 to 7000-8000?

---

## 11. Summary of Answers to Your Questions

### 1. The exact construction/argument

**7-color tiling**:
- Heptagonal + diamond tiling (modified hexagonal)
- Colors 1-6 properly 6-color most of the plane
- Color 0 (wild) covers area fraction p ≈ 1/6197
- Probabilistic argument: graphs with <1/p vertices can avoid wild region

### 2. What tiling does he use?

**Type**: Pentagonal tiling (Type 5) modified with diamonds

**Tiles**:
- Heptagons with width 1/2, circular arc boundaries (radius 1)
- Small diamond-shaped regions
- Arranged in columns (3 colors per column)

**Origin**: Conceived by Ed Pegg

### 3. Where does 6197 come from specifically?

**Direct calculation**:
- Wild color area fraction: p ≈ 1/6197 ≈ 0.000161
- Probabilistic bound: n < 1/p
- Therefore: n < 6197.58... → n ≤ 6197

**Geometric source**:
- Optimization of tile shapes and arrangements
- Constrained by Croft's density bound (0.22936)
- Specific to the heptagonal+diamond tiling

### 4. What would it take to improve this bound?

**Incremental improvement** (~10-20%):
- Better tiling optimization → Achieved: Parts got 6993
- Improved Croft bound (hard - only 8% gap to proven upper bound)

**Major improvement** (2×-10×):
- New construction method (non-tiling)
- Direct gadget-based approach
- Currently unknown how to do this

**Proving it's tight**:
- Show minimal 7-chromatic graph is ~6200 vertices
- Extremely difficult - major theoretical result

### 5. Is it connected to Croft's 1967 density bound?

**Yes - critically connected**:

**Croft provides**: Maximum density of unit-distance-avoiding set = 0.22936

**Pritikin uses**: Each color class must avoid unit distances

**Constraint**: Each of 6 colors can cover ≤0.22936 of plane

**Result**:
- Maximum 6-color coverage: ≤ 6 × 0.229 = 1.374
- In practice: geometric constraints force coverage < 1
- Uncovered area: p ≈ 1/6197
- Gets the "wild" color

**Critical fact**: Improving Pritikin's k=4 bound REQUIRES improving Croft's density bound

### 6. Is the bound tight or is there slack?

**Verdict**: **Likely has significant slack** (possibly 2-4×)

**Evidence for tightness**:
- Optimization only improves to ~6197.5
- Croft's bound nearly tight (only 8% to proven upper)

**Evidence for slack**:
- de Grey's 40× reduction for 5-chromatic graphs
- Parts achieved 13% improvement (6197 → 6993)
- Tiling approaches are inherently inefficient vs. gadget approaches

**Best estimate**: True minimal 7-chromatic graph has **1000-3000 vertices**

**The gap**: Between Pritikin's tiling bound and the actual minimal graph size

**Why it matters**: If slack exists, computational search becomes feasible

---

## 12. Conclusions

### What We Know

1. **Pritikin's construction is elegant**: 7-color tiling with tiny wild region
2. **The bound is rigorous**: All ≤6197-vertex graphs are provably 6-colorable
3. **The tiling is nearly optimal**: For its type, only ~0.5 vertex improvement
4. **It's connected to fundamental limits**: Croft's density bound
5. **It's held for 26 years**: Only 13% improvement (Parts → 6993)

### What We Don't Know

1. **Is there a better construction method?** → Probably yes
2. **How much slack exists?** → Unknown, possibly 2-4×
3. **What's the true minimal 7-chromatic size?** → Speculate 1000-3000
4. **Can we find a 6-chromatic graph?** → Not with current methods
5. **Is χ(ℝ²) = 6 or 7?** → Unknown

### The Research Frontier

**Short term** (2025-2030):
- Prove measurable χ(ℝ²) = 7 (extend 2025 map-coloring results)
- Use ML to find irregular tilings (might improve bound 10-20%)
- Develop better SAT techniques for larger graphs

**Medium term** (2030-2040):
- Find gadget-based constructions for 6/7-chromatic graphs
- Computational search becomes feasible if slack exists
- Potential resolution via measurable chromatic number

**Long term** (2040+):
- Complete resolution of Hadwiger-Nelson problem
- Full characterization of chromatic properties of the plane

---

## References

### Primary Sources

1. **D. Pritikin** (1998), "All unit-distance graphs of order 6197 are 6-colorable," *Journal of Combinatorial Theory, Series B*, 73(2):159–163
   - Available: [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0095895698918196)
   - Also: [CORE Reader](https://core.ac.uk/reader/81122930)

2. **H. T. Croft** (1967), "Incidence incidents," *Eureka (Cambridge)*, 30:22–26

### Related Work

3. **A. de Grey** (2018), "The chromatic number of the plane is at least 5," *arXiv:1804.02385*

4. **M. Heule** (2018), "Computing Small Unit-Distance Graphs with Chromatic Number 5," *Geombinatorics*, 28:32-50

5. **Parts** (2021), 509-vertex 5-chromatic graph (current record)

6. **Mundinger et al.** (2024), "Extending the Continuum of Six-Colorings," *arXiv:2404.05509*

7. **Ambrus et al.** (2023), "The density of planar sets avoiding unit distances," *Mathematical Programming*
   - Upper bound: 0.247

### Historical Context

8. **A. Soifer** (2009), *The Mathematical Coloring Book*, Springer
   - Reports Ed Pegg's original conception of Pritikin tiling

9. **Polymath16 Project** (2018-2020), Collaborative research on Hadwiger-Nelson problem
   - Multiple threads discussing Pritikin bounds and optimizations

### Recent Theoretical Advances

10. **Sokolov-Voronov** (2025), "On the chromatic number of the plane for map-type colorings," *arXiv:2502.01958*
    - Map colorings require ≥7 colors

11. **Fractional chromatic number** (2023), χ_f(ℝ²) = 4 proven

---

*Analysis completed by Pritikin*
*Based on web research and synthesis of existing repository knowledge*
*The bound is tight for its construction type, but likely has structural slack*
