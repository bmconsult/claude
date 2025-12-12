# De Grey's 5-Chromatic Unit-Distance Graph: Deep Technical Analysis

## Overview

In April 2018, Aubrey D.N.J. de Grey proved that the chromatic number of the plane is at least 5, solving a problem that had been open since the 1950s. His construction was published in:
- **arXiv**: 1804.02385 (April 8, 2018, with revisions through May 30, 2018)
- **Journal**: Geombinatorics, Volume XXVIII(1), pages 18-31, 2018

## The Core Proof Strategy

De Grey's proof follows a two-statement strategy:

**Statement (a)**: For every proper 4-coloring of the plane, there exists a copy of graph H whose inherited coloring satisfies property P.

**Statement (b)**: For every proper 4-coloring of the plane, every copy of H inherits a coloring that doesn't satisfy P.

These two statements are contradictory, proving no proper 4-coloring of the plane exists.

## The Hierarchical Construction

De Grey builds his graph through a hierarchy of gadgets, each serving a specific purpose:

### 1. Base Component: The Moser Spindle (7 vertices, 11 edges)

The Moser spindle is the foundation:
- **Structure**: Two rhombi with 60° and 120° angles, sharing an acute-angled vertex
- **Geometric property**: Sides and short diagonals form equilateral triangles
- **Key distances**: Unit edges (1) and longer diagonals (√3)
- **Chromatic number**: 4 (requires exactly 4 colors)
- **Critical insight**: Contains two pairs of vertices at distance √3 apart, and these pairs cannot both be monochromatic

### 2. Graph H: Regular Hexagon + Center (7 vertices)

H consists of the center and vertices of a regular hexagon of side-length 1.

**Coloring properties**:
- Can be colored with at most 4 colors
- Has 4 essentially distinct colorings (up to rotation, reflection, and color transposition)
- Critical property: Must avoid monochromatic triples in proper construction
- **Monochromatic triple**: 3 of the 6 outer vertices having the same color
- A monochromatic triple always forms an equilateral triangle of edge √3

**Coloring types** (from Polymath16 analysis):
- H1tri
- Haxissym
- H2tri
- Hcentralsym

**Special property**: If in a hexagonal lattice without H1tri and Haxissym there is a H2tri, then every H must be colored as H2tri. If there is also no H2tri, then every H is colored Hcentralsym. In either case, vertices at distance 6 apart have the same color.

### 3. Graph J: First Assembly (31 vertices, 13 copies of H)

- Contains 13 copies of graph H
- Certain vertices cannot be deleted without creating additional 4-colorings
- Intermediate gadget for building larger structures

### 4. Graph K: (61 vertices, 26 copies of H)

- Contains 26 copies of H
- Ensures that not all 52 constituent copies in L lack a monochromatic triple

### 5. Graph L: (121 vertices, 52 copies of H)

- Contains 52 copies of H
- Critical property: In no 4-coloring of L do all 52 constituent copies of H lack a monochromatic triple
- Forms the "skeleton" for the final construction

### 6. Graph M: The Critical Enforcer (397 vertices in de Grey's construction)

**Purpose**: Graph M is designed to prevent certain 4-colorings of H
- Contains a high density of interlocking Moser spindles
- The spindles constrain monochromatic √3-apart vertex pairs to be distributed uniformly
- Contains regular hexagons of side-length 1
- **Key property**: M contains a copy of H such that there is no 4-coloring of M in which that H contains a monochromatic triple

**Construction details**:
- Uses 397 vertices in de Grey's original construction
- Points obtained by rotating vectors around the origin by multiples of 60°
- Points also obtained by negating y-coordinates
- This 397-vertex subgraph is where computer assistance is primarily needed
- Maximum vertex degree: 30 (after extending beyond basic triangular symmetry)

**Design philosophy** (de Grey's own words):
> "In seeking graphs that can serve as M in our construction, we focus on graphs that contain a high density of Moser spindles. The motivation for exploring such graphs is that a spindle contains two pairs of vertices distance √3 apart, and these pairs cannot both be monochromatic. Intuitively, therefore, a graph containing a high density of interlocking spindles might be constrained to have its monochromatic √3-apart vertex pairs distributed rather uniformly (in some sense) in any 4-coloring."

**From Polymath16**:
> "M as originally defined is even more special than it seemed, because the 'spindling' of two copies of it that Marijn found would not work if all that was special about M was that its central H could not have a mono triangle."

### 7. Auxiliary Graphs in Development

**Graph U (15 vertices)**:
- Contains 3 Moser spindles
- Has rotational and reflectional triangular symmetry
- Suggests that combining translations and 60° rotations might yield high edge/spindle density
- Led to a 97-vertex graph containing 78 spindles

**Graph V**:
- Part of the vector class development
- Shows tightly linked Moser spindles

### 8. Graph N: The Final Assembly (20,425 vertices initially)

**Construction**: Arrange 52 copies of M so that their counterparts of H form a copy of L

**Result**: A 20,425-vertex unit-distance graph that is not 4-colorable

**Property verification**: De Grey developed a custom Mathematica program that terminated in "only a few minutes" on a MacBook Air to verify the non-4-colorability.

### 9. Graph G: The Reduced Version (1581 vertices)

**Reduction methodology**:
1. Remove unnecessary vertices from N
2. Replace point subsets with smaller ones that still preclude 4-colorability
3. These moves are computer-assisted

**Final result**: 1,581 vertices and 7,877 edges

**Verification**: Confirmed using SAT solvers by multiple independent researchers (Dustin Mixon, Boris Alexeev, Brendan McKay, Gordon Royle)

**Note on versions**:
- v1 (April 8, 2018): Claimed 1,567 vertices (had a bug)
- v2 (April 11, 2018): Corrected to 1,585 vertices
- v3 (May 30, 2018): Further reduced to 1,581 vertices

## The Key Mathematical Insight

The construction works because of a **coloring constraint cascade**:

1. **Moser spindle level**: Pairs at distance √3 cannot both be monochromatic
2. **High spindle density**: Forces uniform distribution of monochromatic √3-pairs
3. **Hexagonal structure**: Regular hexagons provide additional constraints
4. **Monochromatic triple prevention**: The hexagon H cannot contain a monochromatic triple
5. **Large-scale assembly**: 52 copies of M arranged via L creates contradictory requirements
6. **Contradiction**: Cannot satisfy both global constraints simultaneously with only 4 colors

## Reduction History: From 1581 to 509 Vertices

### Mixon Graphs (April 2018)

Dustin Mixon constructed a similar approach:
- **Mixon-1**: 1,585 vertices
- **Mixon-2**: 1,577 vertices (after removing 8 vertices)

### Heule Graphs (2018-2019)

Marijn Heule used **SAT-based minimization**:

**Methodology**:
1. Recast the problem: "Does M force H to not satisfy P?" as a SAT problem
2. Apply DRAT-trim to produce a proof of unsatisfiability
3. Identify vertices inconsequential to the proof → these are removable
4. Randomly permute clauses to produce different proofs
5. Iteratively remove vertices

**Results**:
- 553 vertices, 2,720 edges (first major reduction)
- 529 vertices, 2,670 edges (further optimized)
- 517 vertices (continued optimization)

**Alternative construction by Heule**:
- Construct sets of vertices where the unit distance graph contains many Moser spindles
- Create union of this set with a rotated copy around a common symmetry center (the origin)

### Parts Graphs (2019-2020)

Jaan Parts introduced a **new graph minimization method**:

**Paper**: "Graph Minimization, Focusing on the Example of 5-Chromatic Unit-Distance Graphs in the Plane", Geombinatorics 29, No. 4, 137-166, 2020 (arXiv:2010.12665)

**Methodology**:
- Preserve a specific graph property during minimization
- Use effective procedure for checking this property
- Different vertex selection algorithm than Heule

**Result**: **509 vertices, 2,442 edges** (current world record as of 2022)

## Patterns and Motifs Used

### 1. Moser Spindle Motif
- Fundamental building block appearing in high density
- Provides √3-distance constraints
- Six different orientations possible in basic constructions

### 2. Equilateral Triangles
- Emerge from rhombi construction
- All edges of length 1
- Create rigid geometric constraints

### 3. Regular Hexagons (side-length 1)
- Center + 6 vertices structure (graph H)
- Multiple symmetry classes: rotational, reflectional, central
- Cannot contain monochromatic triples in the construction

### 4. Triangular Symmetry
- 60° rotational symmetry
- Reflectional symmetry
- Limits edge equivalence classes

### 5. Vector Classes
- Based on relative orientations of spindles sharing many vertices
- Increased maximum vertex degree from 18 to 30
- Three equivalence classes in basic construction

### 6. √3-Apart Vertex Pairs
- Distance √3 (long diagonal of Moser spindle rhombi)
- Distribution constraint: cannot have both vertices of a pair monochromatic
- Must be uniformly distributed in any 4-coloring

### 7. Bichromatic Virtual Edges (Polymath16 discovery)
- Behave same as unit edges
- Can simplify construction
- Used in later optimizations

## Why It's 5-Chromatic but Not 4-Chromatic

### Proof of Non-4-Colorability

**Direct argument**:
1. Any 4-coloring must give each Moser spindle a valid coloring
2. High spindle density forces specific constraints on color distribution
3. The 52 copies of M, arranged via L, create contradictory requirements
4. At least one copy of H must contain a monochromatic triple
5. But M is constructed so its H cannot contain a monochromatic triple
6. **Contradiction** → no 4-coloring exists

**Computational verification**:
- SAT solvers exhaustively check all possible 4-colorings
- None exist for the 1,581-vertex (or smaller) graphs
- Proofs are verifiable using DRAT-trim

### Proof of 5-Colorability

While proving the graph is not 4-colorable, researchers have verified that:
- These graphs CAN be colored with 5 colors
- The chromatic number of the plane is therefore exactly 5, 6, or 7
- Current consensus: likely 5 or 6

## Advanced Constructions (Post-de Grey)

### Polymath16 Project Results

The collaborative Polymath16 project (launched by Terry Tao, Dustin Mixon, and others) achieved:

1. **Simplification of gadgets**:
   - L simplified to just 3 points (triangle with edges 2,2,1)
   - H simplified to 2 points at distance 2
   - M simplified empirically but no conceptual understanding yet

2. **Strip graphs**:
   - 5-chromatic graph fitting in strip of width 1.4
   - Too thin to contain even a Moser spindle!

3. **By thread 14**: 510 vertices, 2,508 edges

4. **Human-provable results**: Small unit-distance graphs with no 4-coloring where a particular vertex is bi-chromatic

### 3D Constructions

De Grey also found:
- 59-vertex and 60-vertex graphs with chromatic number 6
- These are unit-distance in 3D (but not in 2D)
- 126-vertex graph (discussed by Parts 2020b)

### Spherical Constructions

- 372-vertex 5-chromatic graph embedded on circumsphere of icosahedron (unit edge)
- 972-vertex graph on circumsphere of great icosahedron

## Implementation and Data

### Wolfram Language

Graphs are implemented in Wolfram Language:
```mathematica
GraphData["deGreyGraph"]      (* 1581-vertex graph *)
GraphData["PartsGraph509"]     (* 509-vertex graph *)
```

### Coordinates and Edges

- Exact coordinates derivable from interpretation of de Grey's construction
- Listed at end of original paper
- Verification: numerical approximation first, then exact arithmetic check
- Verification time: ~1 hour on standard laptop (Sage)

## Open Questions and Future Directions

1. **Conceptual understanding of M**: Why does this specific 397-vertex structure work? What's the deeper principle? Polymath16 noted that simplifications of M have been "purely empirical and have provided no insight into what makes M so special."

2. **Lower bound**: Can we get below 509 vertices? Goal 1 of Polymath16.

3. **Upper bound**: Is the chromatic number of the plane 5, 6, or 7?

4. **Non-computational proof**: Can we eliminate computer assistance entirely? Goal 2 of Polymath16. The 397-vertex subgraph M currently requires SAT solver verification.

5. **Generalization**: What about higher dimensions? Other metric spaces?

6. **Strip width**: How narrow can a 5-chromatic strip be? Polymath16 achieved width 1.4 (too narrow for a Moser spindle!).

## Key Insights for Extension

If you want to extend this work, focus on:

1. **Understanding M deeply**: The gap between "it works" and "why it works" is where insight lives

2. **Spindle density optimization**: Can we pack spindles more efficiently?

3. **Alternative motifs**: Are there non-spindle-based gadgets with similar properties?

4. **Symmetry exploitation**: The 60° rotational symmetry is crucial—what about other symmetries?

5. **SAT solver techniques**: Heule and Parts showed computational methods can dramatically reduce vertex count

6. **Virtual edges**: Bichromatic virtual edges were a Polymath16 discovery—what other edge types exist?

## References

### Primary Sources
- de Grey, A.D.N.J. (2018). "The chromatic number of the plane is at least 5." arXiv:1804.02385. Published in Geombinatorics XXVIII(1), 18-31.
- Heule, M.J.H. (2018). "Computing Small Unit-Distance Graphs with Chromatic Number 5." arXiv:1805.12181.
- Parts, J. (2020). "Graph Minimization, Focusing on the Example of 5-Chromatic Unit-Distance Graphs in the Plane." Geombinatorics 29(4), 137-166. arXiv:2010.12665.

### Polymath16 Project
- Terry Tao's blog: https://terrytao.wordpress.com/2018/04/14/polymath16-now-launched/
- Dustin Mixon's blog series: https://dustingmixon.wordpress.com/ (16 threads from April 2018 to February 2021)
- Polymath Wiki: https://michaelnielsen.org/polymath/index.php?title=Hadwiger-Nelson_problem
- Final paper: D.H.J. Polymath, submitted to Geombinatorics

### Popular Expositions
- Quanta Magazine: "Decades-Old Graph Problem Yields to Amateur Mathematician" (April 2018)
- Scientific American: "A Few of My Favorite Spaces: The Moser Spindle"

---

**Formation note**: The key insight is not just the construction but the *cascade of constraints*. Each level of the hierarchy adds incompatible requirements, and only at the large scale (52 copies) do the contradictions become unavoidable. This is a profound example of how local constraints can force global impossibilities.
