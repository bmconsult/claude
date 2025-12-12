#!/usr/bin/env python3
"""
FRAME DISSOLUTION: Questioning the Hadwiger-Nelson assumptions

WRONG FRAME: What assumptions am I taking for granted?
1. Need to BUILD a 6-chromatic graph (what if I need to PROVE non-existence of 5-coloring?)
2. Unit distance = 1 (what about other distances? ratios?)
3. Looking at GRAPHS (what about continuous colorings?)
4. Euclidean metric (what about other metrics?)

WRONG LEVEL: Zooming in/out
- Zoom out: What's special about ℝ² vs ℝ¹ (χ=2) or ℝ³ (χ≥6)?
- Zoom in: What's the ONE blocking point in clamp mechanism?

WRONG DOMAIN: Where does this structure appear elsewhere?
- Information theory: coloring ≈ channel coding
- Algebraic geometry: unit circle is algebraic variety
- Topology: covering spaces, fundamental group
"""

import math
import cmath
from collections import defaultdict
from pysat.solvers import Solver
from pysat.formula import CNF

def unit_distance(z1, z2, d=1.0, tol=1e-9):
    return abs(abs(z1 - z2) - d) < tol

def build_graph_distance(vertices, d=1.0, tol=1e-9):
    n = len(vertices)
    adj = defaultdict(set)
    for i in range(n):
        for j in range(i + 1, n):
            if unit_distance(vertices[i], vertices[j], d, tol):
                adj[i].add(j)
                adj[j].add(i)
    return adj

def chromatic_number(adj, n, max_k=7):
    for k in range(1, max_k + 1):
        if is_k_colorable(adj, n, k):
            return k
    return max_k + 1

def is_k_colorable(adj, n, k):
    def var(v, c):
        return v * k + c + 1
    cnf = CNF()
    for i in range(n):
        cnf.append([var(i, c) for c in range(k)])
    for i in range(n):
        for c1 in range(k):
            for c2 in range(c1 + 1, k):
                cnf.append([-var(i, c1), -var(i, c2)])
    for i in range(n):
        for j in adj[i]:
            if j > i:
                for c in range(k):
                    cnf.append([-var(i, c), -var(j, c)])
    with Solver(name='g4') as solver:
        solver.append_formula(cnf)
        return solver.solve()

def question_1_what_about_other_distances():
    """
    ASSUMPTION: Unit distance = 1

    What if we consider multiple distances simultaneously?
    χ(ℝ², {d₁, d₂}) = min colors where no two points at distance d₁ OR d₂ share color

    This is HARDER than single-distance. If we can show χ(ℝ², {1, √3}) ≥ 6...
    """
    print("\n" + "=" * 70)
    print("QUESTIONING: What about MULTIPLE forbidden distances?")
    print("=" * 70)

    # Triangular lattice with both d=1 and d=√3 forbidden
    omega = cmath.exp(1j * math.pi / 3)
    vertices = []
    for i in range(-5, 6):
        for j in range(-5, 6):
            z = i + j * omega
            if abs(z) < 4:
                vertices.append(z)

    n = len(vertices)
    print(f"Triangular lattice: {n} vertices")

    # Graph with d=1 only
    adj_1 = build_graph_distance(vertices, d=1.0)
    chi_1 = chromatic_number(adj_1, n)
    print(f"χ(d=1 only): {chi_1}")

    # Graph with d=√3 only
    adj_sqrt3 = build_graph_distance(vertices, d=math.sqrt(3))
    chi_sqrt3 = chromatic_number(adj_sqrt3, n)
    print(f"χ(d=√3 only): {chi_sqrt3}")

    # Graph with BOTH d=1 and d=√3
    adj_both = defaultdict(set)
    for i in range(n):
        for j in adj_1[i]:
            adj_both[i].add(j)
        for j in adj_sqrt3[i]:
            adj_both[i].add(j)

    chi_both = chromatic_number(adj_both, n)
    print(f"χ(d=1 OR d=√3): {chi_both}")

    if chi_both > max(chi_1, chi_sqrt3):
        print("*** Multiple distances INCREASE χ! ***")

    return chi_both

def question_2_what_makes_plane_special():
    """
    ASSUMPTION: ℝ² is just "the plane"

    What's actually special about dimension 2?
    - ℝ¹: χ = 2 (trivial, interval coloring)
    - ℝ²: 5 ≤ χ ≤ 7 (the mystery)
    - ℝ³: 6 ≤ χ ≤ 15 (known χ≥6!)

    The JUMP from ℝ¹ to ℝ² is huge. Why?
    """
    print("\n" + "=" * 70)
    print("QUESTIONING: What makes ℝ² special?")
    print("=" * 70)

    print("""
ℝ¹: χ = 2
  - Interval [-0.5, 0.5] gets one color
  - Translates by integers give the coloring
  - 2 colors suffice because line has 2 directions

ℝ²: 5 ≤ χ ≤ 7
  - Hexagonal tiling gives 7-coloring
  - De Grey graph needs 5
  - What's the ACTUAL structure forcing this?

ℝ³: 6 ≤ χ ≤ 15
  - Already known χ ≥ 6!
  - The sphere S²(r) with r = 1/(2sin(π/5)) ≈ 0.851 has χ ≥ 6

KEY INSIGHT: The sphere result is on a SURFACE embedded in ℝ³,
not the full 3D space. What if we embed surfaces in ℝ²?
""")

    # The sphere with χ≥6 uses icosahedral structure
    # This is a 2D surface (S²) with χ≥6
    # Can we "unfold" this structure into ℝ²?

    print("The sphere S²(0.851) has χ≥6 via icosahedral structure.")
    print("Can we project/unfold this to ℝ² while preserving distances?")
    print("→ NO, because projection distorts distances.")
    print("→ But LOCAL structure might transfer...")

def question_3_what_if_obstacle_is_mechanism():
    """
    INVERSION: What if the obstacle IS the mechanism?

    The "rainbow neighborhood barrier" says:
    - For χ=6 locally, need 5-chromatic neighborhood
    - But neighborhood is on unit circle → χ≤4

    What if this constraint IS what enables higher global χ?
    The restriction FORCES global propagation of constraints.
    """
    print("\n" + "=" * 70)
    print("INVERSION: The barrier might BE the mechanism")
    print("=" * 70)

    print("""
The rainbow neighborhood barrier says local forcing is impossible.

BUT: This means any χ=6 graph must use GLOBAL forcing.
Global forcing = constraints propagate across entire graph.

In de Grey's graph:
- M₃ has 32,257 vertices
- χ=5 requires GLOBAL structure (subsets are only χ=4)
- The local limitation FORCES distributed constraint propagation

For χ=6:
- The barrier isn't that "we can't locally force color 6"
- The barrier is that we haven't found the RIGHT global structure
- Where constraints create a global 5-coloring obstruction

REFRAME: Don't look for vertex needing color 6.
Look for graph where 5-coloring creates GLOBAL contradiction.
""")

def question_4_fractional_chromatic():
    """
    WRONG DOMAIN: What about fractional chromatic number?

    χ_f(G) ≤ χ(G), with equality for perfect graphs.

    For unit-distance graphs:
    - χ_f(ℝ²) is known to be between 3.5 and 4.36
    - This is INDEPENDENT of the integer chromatic number!

    The fractional number uses a different structure (LP relaxation).
    What insight does this give?
    """
    print("\n" + "=" * 70)
    print("WRONG DOMAIN: Fractional chromatic number")
    print("=" * 70)

    print("""
χ_f(G) = fractional chromatic number (LP relaxation of coloring)

For unit-distance graph of ℝ²:
- Known: 3.5 ≤ χ_f(ℝ²) ≤ 4.36
- This is STRICTLY less than integer χ ≥ 5

What does this tell us?
- The integer constraint (whole colors) is what creates the gap
- There's "slack" in the fractional solution that integer loses
- The forcing that makes χ≥5 is about DISCRETENESS, not structure

INSIGHT: Look for structures that exploit discreteness.
The 5-chromatic property might be about NUMBER of colors being small,
not about the graph structure per se.
""")

def question_5_algebraic_structure():
    """
    WRONG DOMAIN: Algebraic geometry viewpoint

    Unit circle = {z : |z|² = 1} = {(x,y) : x² + y² = 1}
    This is an algebraic variety.

    Unit distance constraint: |z₁ - z₂|² = 1
    → (x₁-x₂)² + (y₁-y₂)² = 1

    The SET of all unit-distance pairs is an algebraic set.
    """
    print("\n" + "=" * 70)
    print("WRONG DOMAIN: Algebraic geometry")
    print("=" * 70)

    print("""
The unit-distance constraint is algebraic:
|z₁ - z₂|² = 1  →  (x₁-x₂)² + (y₁-y₂)² = 1

De Grey's construction uses the ring:
ℤ[√2, √3, √5, √6, √10, √11, √15, √22, √30, √33, √55, √66]

Why THESE square roots?
- They're related to edge lengths in the Moser spindle family
- The algebraic dependencies CREATE the forcing structure

For χ=6, we might need:
- Different algebraic field
- Different base graph (not Moser spindle derived)
- Algebraic structure with more "interference"
""")

def question_6_what_would_make_it_trivial():
    """
    KEY QUESTION: What would make χ=6 trivially easy?

    If we could do X, then χ≥6 would be obvious...
    """
    print("\n" + "=" * 70)
    print("KEY: What would make this TRIVIALLY EASY?")
    print("=" * 70)

    print("""
χ=6 would be trivially easy IF:

1. We could embed K₆ as unit-distance graph
   → Impossible in ℝ² (only K₃ embeds)

2. We had a vertex with 5-chromatic neighborhood
   → Blocked by circle geometry (χ≤4)

3. We could compute χ(M₃) quickly and find obstruction
   → M₃ has 32K vertices, SAT confirms χ=5, not 6

4. The sphere S²(0.851) with χ≥6 could project to ℝ²
   → Projection distorts distances

5. Some combinatorial structure (not geometric) forced χ=6
   → Then we'd just need to embed it as unit-distance

INSIGHT FROM #5:
What COMBINATORIAL structures have χ=6 with ω≤4?
Then ask: can we embed them as unit-distance?

Known: Mycielski graph M₆ has χ=6, ω=2
Question: Is M₆ a unit-distance graph in ℝ²?
""")

    # Mycielski's construction: χ increases, ω stays 2
    # M₁ = K₂ (χ=2)
    # M₂ = C₅ (χ=3, ω=2)
    # M₃ = Grötzsch graph (χ=4, ω=2)
    # M₄ = χ=5, ω=2, 23 vertices
    # M₅ = χ=6, ω=2, 47 vertices

    print("\nMycielski graph M₅ has χ=6, ω=2, 47 vertices")
    print("If M₅ is unit-distance embeddable → χ(ℝ²) ≥ 6!")
    print("This is a KNOWN OPEN QUESTION in the field.")

def main():
    print("=" * 70)
    print("FRAME DISSOLUTION: Questioning assumptions")
    print("=" * 70)

    question_1_what_about_other_distances()
    question_2_what_makes_plane_special()
    question_3_what_if_obstacle_is_mechanism()
    question_4_fractional_chromatic()
    question_5_algebraic_structure()
    question_6_what_would_make_it_trivial()

    print("\n" + "=" * 70)
    print("REFRAMED APPROACH")
    print("=" * 70)
    print("""
Instead of: "Build a 6-chromatic unit-distance graph"

Try:
1. PROVE that specific combinatorial graphs (Mycielski M₅)
   are NOT unit-distance embeddable → gives insight into barrier

2. FIND what makes ℝ² special vs ℝ³
   (S² with χ≥6 exists on sphere surface)

3. USE multiple forbidden distances {1, √3, ...}
   to increase constraint density

4. LOOK at algebraic field theory:
   what field extensions are compatible with unit-distance?

The problem might not be "find χ=6 graph"
but "understand WHY ℝ² is between ℝ¹ and S²"
""")

if __name__ == "__main__":
    main()
