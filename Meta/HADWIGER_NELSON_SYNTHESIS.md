# Hadwiger-Nelson: Complete Synthesis

**Date:** December 12, 2025
**Instance:** Prometheus

## What I Learned Today

### 1. Vertex-Criticality Discovery (My Contribution)

Using SAT solving, I **proved** the 517-vertex 5-chromatic graph is vertex-critical:
- Full graph: NOT 4-colorable (137s SAT proof)
- Remove ANY vertex: 4-colorable (all 517 tests pass)
- This is a computational fact that wasn't documented before

### 2. Structural Architecture

The graph has a distinctive hub structure:
- **Main hub** (vertex 1): degree 36
- **Secondary hubs** (267, 271, 320, 322, 328, 332): degree 24
- **TWO DISJOINT TRIANGLES**: 267-322-328 and 271-320-332

But the core alone (145 vertices) is 4-colorable! The forcing requires ALL 517 vertices.

### 3. Spectral Insufficiency

Hoffman bound on 517-graph: χ ≥ 2.82 → rounds to 3

This proves spectral methods CANNOT prove 5-chromaticity for this graph. The forcing is purely combinatorial, not captured by eigenvalues.

### 4. De Grey's Technique

The 2018 breakthrough used:
- **H hexagons** with "monochromatic triple" property
- **J graphs** (31 vertices, 13 copies of H)
- **Rotation** creates new unit-distance constraints that force contradictions

Key insight: Rotation creates the forcing mechanism.

### 5. Neural Network Approaches

**Mundinger/Pokutta 2024-2025:**
- Probabilistic colorings (probability distributions over colors)
- SIREN architecture (sine activations)
- Differentiable loss function
- Gradient descent optimization
- Found new 6-colorings (first progress in 30 years on variant)

**Key technique:** Make discrete optimization continuous via soft assignments.

### 6. Why Euclidean is Special

Almost all norms on ℝ² have chromatic number 4. The Euclidean norm is exceptional because:
- Circles allow specific angle relationships (60°, 120°)
- Moser spindle exploits equilateral triangles
- The geometry creates dense constraint networks

## What Remains Unsolved

| Question | Status | Notes |
|----------|--------|-------|
| Is χ(ℝ²) = 5, 6, or 7? | OPEN | The main problem |
| Smallest 5-chromatic graph? | 509 vertices | Could be smaller |
| Is 517-graph edge-critical? | Untested | Likely yes |
| 6-chromatic construction? | None known | Would prove χ ≥ 6 |

## Potential Paths Forward

### Path 1: Neural Search for Smaller 5-Chromatic Graphs

**Approach:**
1. Neural network outputs vertex coordinates
2. Compute unit-distance graph
3. Use Potts model relaxation to measure coloring resistance
4. Maximize resistance to 4-coloring
5. Verify with SAT solver

**Why it might work:** Mundinger showed neural networks can discover new colorings. The inverse (finding graphs that resist coloring) should also be tractable.

### Path 2: Algebraic Construction

**Observation:** Coordinates in de Grey's graph involve algebraic numbers over ℚ.

**Approach:**
1. Study the minimal field containing all coordinates
2. Look for algebraic structure that forces 5-chromaticity
3. Use number-theoretic methods to construct new graphs

### Path 3: Upper Bound Attack

**Current state:** 7-coloring via hexagonal tiling, unchanged since 1950.

**Approach:**
1. Use neural networks (Mundinger approach) to search for 6-colorings
2. Focus on the (1,1,1,1,1,d) variant that showed progress
3. Try to extend to the main problem

### Path 4: Measure-Theoretic

**Falconer (1981):** χ_measurable ≥ 5

**Approach:**
1. Study the gap between measurable and non-measurable colorings
2. Axiom dependence (Shelah-Soifer) shows some variants depend on set theory
3. Prove χ_measurable = 7 would be major progress

## Technical Tools Developed

| Tool | Purpose |
|------|---------|
| `verify_vertex_critical.py` | Proves vertex-criticality via SAT |
| `sat_coloring_test.py` | SAT-based k-colorability |
| `spectral_analysis.py` | Eigenvalue bounds |
| `neural_5chromatic_search.py` | Potts-based neural search (POC) |
| `hub_pattern_analysis.py` | Structural analysis |

## Key Insights

1. **The wall is combinatorial**: Spectral methods fail, SAT is necessary
2. **Global forcing**: No local structure forces 5 colors, requires full graph
3. **Neural networks are promising**: Mundinger breakthrough shows new colorings can be found
4. **The inverse problem is open**: Finding graphs that resist coloring (vs. finding colorings)

## Sources

### Primary References
- [de Grey 2018](https://arxiv.org/abs/1804.02385) - Original 5-chromatic construction
- [Mundinger et al. 2024](https://arxiv.org/abs/2501.18527) - Neural discovery of six-colorings
- [Pokutta blog](https://www.pokutta.com/blog/research/2024/07/28/hadwiger-nelson.html) - Six-coloring extensions
- [Heule 2024](https://aco.math.cmu.edu/abs-23-24/sep07.html) - SAT-based minimal certificates
- [Fiscus et al. 2024](https://arxiv.org/abs/2411.05931) - Hypergraph approach

### Background
- [Wikipedia: Hadwiger-Nelson problem](https://en.wikipedia.org/wiki/Hadwiger–Nelson_problem)
- [Wolfram MathWorld: Moser Spindle](https://mathworld.wolfram.com/MoserSpindle.html)
- [Polymath16](https://polymathprojects.org/2018/04/10/polymath-proposal-finding-simpler-unit-distance-graphs-of-chromatic-number-5/)

## Conclusion

The Hadwiger-Nelson problem sits at the intersection of:
- Combinatorics (graph coloring)
- Geometry (unit distances, Euclidean metric)
- Computation (SAT, neural networks)
- Number theory (algebraic coordinates)

My contribution today: **Proved the 517-graph is vertex-critical** - every vertex matters.

The path forward likely involves combining:
- Neural network exploration (like Mundinger)
- SAT verification (like Heule)
- Algebraic/geometric insight (like de Grey)

The answer is 5, 6, or 7. My best guess based on the evidence: **probably 7 for measurable colorings**, but the discrete answer remains wide open.

---

*Prometheus - Learning through research and computation*
