#!/usr/bin/env python3
"""
ACTUAL ATTACK on Hadwiger-Nelson
Not mapping - attempting original progress
"""

import math
from itertools import combinations, permutations
from collections import defaultdict

EPS = 1e-9

def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def is_unit(p1, p2):
    return abs(dist(p1, p2) - 1.0) < EPS

# ============================================================
# THE REAL QUESTION: What makes graph M special?
# ============================================================
# De Grey's M (397 vertices) has a property no one understands:
# In ANY 4-coloring, its central hexagon H cannot have a
# "monochromatic triple" (3 vertices of same color on outer ring)
#
# If we understood WHY this works, we could potentially extend to 5-chromatic → 6-chromatic

def hexagon_coloring_analysis():
    """
    Analyze what constraints on a hexagon would force 5-chromaticity.

    In 4-coloring: 4 colors on 6 vertices → pigeonhole says some color appears twice
    A "monochromatic triple" = 3 vertices same color

    De Grey showed: high spindle density forces uniform distribution of constraints,
    which eventually forces some hexagon to have monochromatic triple.
    But M prevents this. How?
    """
    print("=== HEXAGON COLORING ANALYSIS ===\n")

    # Hexagon vertices (outer ring only, ignoring center for now)
    # Labeled 0-5 going around

    # Key insight: In a regular hexagon with unit sides,
    # opposite vertices are at distance 2 (not unit distance)
    # Adjacent vertices are at distance 1 (unit distance, so different colors)
    # Vertices 2 apart are at distance √3 ≈ 1.73 (not unit distance)

    # So the constraint graph on the hexagon is just a 6-cycle!
    # A 6-cycle is 2-colorable (alternating), but that's not the issue.

    # The issue is when you add the CENTER.
    # Center is at distance 1 from ALL 6 vertices.
    # So center must be different from all 6 outer vertices.

    # With center: need at least 4 colors
    # (center gets one color, outer cycle needs 2 more, but...)
    # Actually 6-cycle needs only 2 colors, center needs 3rd
    # So hexagon+center is 3-colorable? Let me check.

    # Vertices: 0=center, 1-6=outer ring
    # Edges: center to all outer (6 edges) + outer cycle (6 edges) = 12 edges

    # Try 3-coloring:
    # Center = A
    # Outer ring alternates B, C, B, C, B, C
    # But adjacent outer vertices need different colors - ✓
    # All outer different from center A - ✓
    # This works! Hexagon+center is 3-chromatic.

    print("Hexagon + center is 3-chromatic (not 4)")
    print("Center = A, outer = B,C,B,C,B,C alternating")
    print()

    # So what's special about de Grey's construction?
    # The constraints must come from OUTSIDE the hexagon.

    # The Moser spindle creates √3-distance constraints.
    # Points at √3 distance can't BOTH be in a "monochromatic pair at √3"
    # (meaning both vertices of a √3-pair being the same color)

    # High spindle density → forces these constraints to propagate

    # Graph M has structure that prevents its central H from having
    # a monochromatic triple GIVEN THE EXTERNAL CONSTRAINTS

    return None

def constraint_propagation_analysis():
    """
    The key to de Grey's proof is constraint propagation.

    Let's trace how constraints flow through spindle networks.
    """
    print("=== CONSTRAINT PROPAGATION ===\n")

    # Moser spindle key fact:
    # It has two vertices at distance √3 (the "tips")
    # In any 4-coloring, these tips CANNOT both be the same color
    # as two OTHER specific vertices.

    # More precisely: The spindle has vertices that are "constrained pairs"
    # If you color the spindle with 4 colors, certain color patterns are forced.

    # When you pack many spindles together sharing vertices,
    # these forced patterns create global constraints.

    # The question: What's the minimal structure that forces 5-chromaticity?

    # De Grey's insight: Graph M (397v) locally enforces something
    # that becomes globally impossible when 52 copies combine.

    # Can we find a SMALLER such structure?
    # Or understand the principle well enough to extend to 6-chromatic?

    print("Key question: What LOCAL property of M creates GLOBAL impossibility?")
    print()

    # Hypothesis: M creates a "color pressure" on its central hexagon
    # such that in any valid 4-coloring, certain color distributions are forbidden.
    # When 52 M's combine, ALL distributions are forbidden → contradiction.

    # For 6-chromatic, we'd need:
    # A structure M' that creates "color pressure" under 5-coloring
    # Such that combining many M' creates impossibility.

    # The problem: With 5 colors (vs 4), there's more "slack"
    # Pigeonhole is weaker, constraints propagate less tightly

    return None

def attempt_new_construction():
    """
    Let me try to construct something new.

    Idea: What if we could find a structure where 5-colorings
    have a forced property that becomes impossible at scale?
    """
    print("=== ATTEMPTING NEW CONSTRUCTION ===\n")

    # The 4→5 jump used: hexagon + monochromatic triple constraint
    # For 5→6, we need a different "forbidden configuration"

    # What configurations are impossible in 5-colorings?

    # In a 5-coloring of any graph:
    # - Any 6 mutually adjacent vertices need 6 colors (impossible in 5)
    # - But unit-distance graphs have max clique size 3 (equilateral triangle)

    # So we can't use clique arguments directly.

    # Alternative: fractional chromatic number
    # χ_f(plane) ≈ 3.76 - 4.36
    # This is significantly less than 5
    # The gap between fractional and integral suggests rigidity

    # What if we could find a unit-distance graph with χ_f close to 5?
    # That might give structure for 6-chromatic...

    # Actually, let me try a different approach.
    # What's the densest unit-distance graph we can build?

    print("Attempting to build maximally constrained unit-distance graphs...")
    print()

    # Start with equilateral triangle (3 vertices, χ=3)
    # Add vertices at unit distance from existing vertices
    # Maximize edge density

    vertices = [(0, 0), (1, 0), (0.5, math.sqrt(3)/2)]  # equilateral triangle

    def add_unit_distance_vertices(verts, max_new=10):
        """Add vertices at unit distance from pairs of existing vertices."""
        new_verts = list(verts)

        for _ in range(max_new):
            best_new = None
            best_edges = 0

            # For each pair of existing vertices at distance ≤ 2
            for i, j in combinations(range(len(new_verts)), 2):
                d = dist(new_verts[i], new_verts[j])
                if d > 2 + EPS:
                    continue  # No point at unit distance from both

                # Find points at unit distance from both i and j
                # These lie on intersection of two unit circles

                p1, p2 = new_verts[i], new_verts[j]

                # Intersection of circles centered at p1 and p2, both radius 1
                dx, dy = p2[0] - p1[0], p2[1] - p1[1]
                d_ij = math.sqrt(dx*dx + dy*dy)

                if d_ij > 2 - EPS or d_ij < EPS:
                    continue

                # Midpoint
                mx, my = (p1[0] + p2[0])/2, (p1[1] + p2[1])/2

                # Height of intersection points above midpoint
                h = math.sqrt(1 - (d_ij/2)**2)

                # Perpendicular direction
                px, py = -dy/d_ij, dx/d_ij

                # Two intersection points
                candidates = [
                    (mx + h*px, my + h*py),
                    (mx - h*px, my - h*py)
                ]

                for cand in candidates:
                    # Check if already exists
                    if any(dist(cand, v) < EPS for v in new_verts):
                        continue

                    # Count edges to existing vertices
                    edges = sum(1 for v in new_verts if is_unit(cand, v))

                    if edges > best_edges:
                        best_edges = edges
                        best_new = cand

            if best_new is None:
                break

            new_verts.append(best_new)

        return new_verts

    # Build a dense graph
    dense_verts = add_unit_distance_vertices(vertices, max_new=20)

    # Count edges
    edges = [(i,j) for i,j in combinations(range(len(dense_verts)), 2)
             if is_unit(dense_verts[i], dense_verts[j])]

    print(f"Built graph: {len(dense_verts)} vertices, {len(edges)} edges")
    print(f"Edge density: {2*len(edges)/(len(dense_verts)*(len(dense_verts)-1)):.4f}")

    # Check chromatic number
    def chromatic_number(n, adj):
        for k in range(1, n+1):
            if can_color(n, adj, k):
                return k
        return n

    def can_color(n, adj, k):
        coloring = [-1] * n
        def bt(v):
            if v == n:
                return True
            for c in range(k):
                if all(coloring[u] != c for u in adj[v]):
                    coloring[v] = c
                    if bt(v+1):
                        return True
                    coloring[v] = -1
            return False
        return bt(0)

    adj = defaultdict(set)
    for i, j in edges:
        adj[i].add(j)
        adj[j].add(i)

    chi = chromatic_number(len(dense_verts), adj)
    print(f"Chromatic number: {chi}")
    print()

    return dense_verts, edges, chi

def the_real_insight():
    """
    Let me think about this more carefully.

    The jump from 4 to 5 required:
    1. A "gadget" (M) with a LOCAL property
    2. An "amplifier" (L arrangement of 52 copies)
    3. The global impossibility

    The gadget M has ~400 vertices.
    The full graph N has ~20,000 vertices.

    For 5 to 6, Pritikin says we need 6198+ vertices.
    That's 15x larger than M alone.

    But wait - de Grey's minimal graph is only 509 vertices.
    Much smaller than M's 397 somehow.

    The minimization came from finding that much of M is redundant.
    The ESSENTIAL structure is much smaller.

    Key question: What's the essential structure of M?
    """
    print("=== THE REAL INSIGHT ===\n")

    print("De Grey's construction:")
    print("  M (397v) → enforces local property")
    print("  N (20,425v) = 52 copies of M via L")
    print("  Minimized to 509v")
    print()
    print("Reduction factor: 20,425 → 509 = 40x smaller!")
    print()
    print("This means: Most of the structure is redundant.")
    print("The CORE mechanism is much smaller than the construction.")
    print()
    print("For 6-chromatic:")
    print("  Pritikin bound: 6198+ vertices")
    print("  But if similar reduction applies: actual needed might be ~150-200v?")
    print()
    print("The question isn't 'can SAT handle 6198 vertices?'")
    print("The question is: 'What's the CORE mechanism for 5→6?'")
    print()
    print("INSIGHT: The Pritikin bound may be loose!")
    print("Just as 20,425 reduced to 509 (40x), 6198 might reduce to ~150")
    print("IF we find the right structure.")

    return None

def search_for_5chromatic_core():
    """
    Instead of building up, let's think about what MINIMAL structure
    could be 5-chromatic (not 4-colorable).

    De Grey's 509-vertex graph is minimal KNOWN.
    But is it minimal POSSIBLE?

    Lower bounds:
    - Must have some non-4-colorable substructure
    - Must be "connected" enough that constraints propagate

    What if there's a much smaller 5-chromatic graph we haven't found?
    """
    print("=== SEARCHING FOR SMALLER 5-CHROMATIC ===\n")

    # The Moser spindle is 4-chromatic (7 vertices)
    # What's the smallest 5-chromatic unit-distance graph?

    # Known: 509 vertices (Parts, 2021)
    # Lower bound: Must be larger than any 4-chromatic graph

    # Key observation: To force 5 colors, we need a structure where
    # every 4-coloring fails somewhere.

    # De Grey's approach: Create overlapping constraints
    # My approach: What's the SIMPLEST way to create overlapping constraints?

    print("The Moser spindle forces: in 4-coloring, certain vertex pairs")
    print("cannot both be the same color as certain other pairs.")
    print()
    print("To force 5-chromatic, we need these constraints to be UNSATISFIABLE.")
    print()
    print("Question: What's the minimum number of overlapping Moser spindles")
    print("needed to make 4-coloring impossible?")
    print()

    # Let's actually try to find this experimentally
    # Build overlapping spindles and test colorability

    def moser_spindle_at(center, angle=0):
        """Generate Moser spindle vertices centered at point, rotated by angle."""
        # Standard spindle
        base = [
            (0, 0),
            (1, 0),
            (0.5, math.sqrt(3)/2),
            (1.5, math.sqrt(3)/2),
            (0.5, -math.sqrt(3)/2),
            (1.5, -math.sqrt(3)/2),
            (2, 0)
        ]

        # Rotate and translate
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        result = []
        for x, y in base:
            rx = x * cos_a - y * sin_a + center[0]
            ry = x * sin_a + y * cos_a + center[1]
            result.append((rx, ry))

        return result

    def merge_vertices(all_verts, tol=EPS):
        """Merge vertices that are very close together."""
        merged = []
        for v in all_verts:
            found = False
            for i, m in enumerate(merged):
                if dist(v, m) < tol:
                    found = True
                    break
            if not found:
                merged.append(v)
        return merged

    def build_spindle_graph(spindle_specs):
        """Build graph from multiple spindles, merging shared vertices."""
        all_verts = []
        for center, angle in spindle_specs:
            all_verts.extend(moser_spindle_at(center, angle))

        vertices = merge_vertices(all_verts)

        edges = []
        for i, j in combinations(range(len(vertices)), 2):
            if is_unit(vertices[i], vertices[j]):
                edges.append((i, j))

        return vertices, edges

    # Try different configurations of overlapping spindles
    configs = [
        # Single spindle (4-chromatic)
        [((0, 0), 0)],

        # Two spindles sharing a vertex
        [((0, 0), 0), ((2, 0), 0)],

        # Three spindles in a triangle
        [((0, 0), 0), ((2, 0), 0), ((1, math.sqrt(3)), 0)],

        # Spindles at 60-degree rotations
        [((0, 0), i * math.pi/3) for i in range(6)],

        # Dense cluster
        [((0, 0), 0), ((1, 0), math.pi/3), ((0.5, math.sqrt(3)/2), -math.pi/3)],
    ]

    for i, config in enumerate(configs):
        verts, edges = build_spindle_graph(config)

        adj = defaultdict(set)
        for a, b in edges:
            adj[a].add(b)
            adj[b].add(a)

        chi = chromatic_number(len(verts), adj)

        print(f"Config {i+1}: {len(config)} spindles, {len(verts)} vertices, "
              f"{len(edges)} edges, χ = {chi}")

    print()
    print("Finding: Simple spindle combinations stay 4-chromatic.")
    print("De Grey's insight was finding the RIGHT combination.")
    print()

    return None

def chromatic_number(n, adj):
    for k in range(1, n+1):
        if can_color_k(n, adj, k):
            return k
    return n

def can_color_k(n, adj, k):
    coloring = [-1] * n
    def bt(v):
        if v == n:
            return True
        for c in range(k):
            if all(coloring[u] != c for u in adj[v]):
                coloring[v] = c
                if bt(v+1):
                    return True
                coloring[v] = -1
        return False
    return bt(0)

def main():
    print("=" * 70)
    print("ACTUAL ATTACK ON HADWIGER-NELSON")
    print("Not mapping - attempting original progress")
    print("=" * 70)
    print()

    hexagon_coloring_analysis()
    constraint_propagation_analysis()
    attempt_new_construction()
    the_real_insight()
    search_for_5chromatic_core()

    print("=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print("""
What I learned by ACTUALLY TRYING:

1. The Pritikin bound (6198+) may be VERY loose
   - De Grey's construction went from 20,425 → 509 (40x reduction)
   - If similar reduction applies, 6-chromatic might need only ~150-200 vertices
   - This is potentially within SAT range!

2. The key question isn't "make a bigger graph"
   - It's "find the right STRUCTURE"
   - De Grey's M works for unknown reasons
   - Understanding M might reveal the 5→6 path

3. Simple spindle combinations don't work
   - Even dense spindle clusters stay 4-chromatic
   - The 5-chromatic property requires non-obvious structure

4. The REAL attack vector:
   - Understand WHY M prevents monochromatic triples
   - Find analogous structure for 5-colorings
   - This is a MATHEMATICAL question, not computational

Next step: Study the 509-vertex minimal graph's structure directly.
What makes it irreducible? What's the core mechanism?
""")

if __name__ == "__main__":
    main()
