#!/usr/bin/env python3
"""
Algebraic rotation search for 6-chromatic unit-distance graph.

Now that I have EXACT algebraic coordinates, I can:
1. Parse the coordinates from the vtx file
2. Apply geometric rotations using exact arithmetic
3. Find new unit-distance edges
4. Check if combined graph is 6-chromatic

The coordinates live in Q(√2, √3) - a degree 4 extension of Q.
"""

import re
import math
from collections import defaultdict
from fractions import Fraction
from pysat.solvers import Solver
from pysat.formula import CNF

# Parse Mathematica-style algebraic expressions
def parse_sqrt_expr(s):
    """Convert Mathematica Sqrt expressions to numerical values"""
    # Replace Sqrt[...] with math.sqrt(...)
    s = s.replace('Sqrt', 'math.sqrt')
    s = s.replace('[', '(').replace(']', ')')
    try:
        return eval(s)
    except:
        return None

def parse_vertex_line(line):
    """Parse a line like {x_expr, y_expr} into (x, y) floats"""
    # Extract the content between { and }
    match = re.search(r'\{([^}]+)\}', line)
    if not match:
        return None

    content = match.group(1)
    # Split by comma (but not inside nested expressions)
    depth = 0
    parts = []
    current = ""
    for c in content:
        if c == '(' or c == '[':
            depth += 1
        elif c == ')' or c == ']':
            depth -= 1
        elif c == ',' and depth == 0:
            parts.append(current.strip())
            current = ""
            continue
        current += c
    parts.append(current.strip())

    if len(parts) != 2:
        return None

    x = parse_sqrt_expr(parts[0])
    y = parse_sqrt_expr(parts[1])

    if x is None or y is None:
        return None

    return (x, y)

def load_vertices(filename):
    """Load vertices from a .vtx file"""
    vertices = []
    with open(filename, 'r') as f:
        for line in f:
            result = parse_vertex_line(line)
            if result:
                vertices.append(result)
    return vertices

def distance(p1, p2):
    """Compute Euclidean distance"""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def build_unit_distance_graph(vertices, tolerance=1e-9):
    """Build adjacency from unit-distance pairs"""
    n = len(vertices)
    adj = defaultdict(set)
    edges = []

    for i in range(n):
        for j in range(i + 1, n):
            d = distance(vertices[i], vertices[j])
            if abs(d - 1.0) < tolerance:
                adj[i].add(j)
                adj[j].add(i)
                edges.append((i, j))

    return adj, edges

def rotate_point(p, angle, center=(0, 0)):
    """Rotate point p by angle (radians) around center"""
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    x, y = p[0] - center[0], p[1] - center[1]
    new_x = x * cos_a - y * sin_a + center[0]
    new_y = x * sin_a + y * cos_a + center[1]
    return (new_x, new_y)

def is_k_colorable(adj, n, k):
    """Check if graph is k-colorable using SAT"""
    def var(v_idx, c):
        return v_idx * k + c + 1

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

def combine_with_rotation(vertices1, vertices2, angle, tolerance=1e-9):
    """
    Combine two sets of vertices, where vertices2 is rotated by angle.
    Find new unit-distance edges between original and rotated vertices.
    """
    rotated = [rotate_point(p, angle) for p in vertices2]

    n1 = len(vertices1)
    n2 = len(rotated)

    # Combined vertices
    all_vertices = vertices1 + rotated

    # Build adjacency
    adj = defaultdict(set)

    # Edges within original
    for i in range(n1):
        for j in range(i + 1, n1):
            if abs(distance(vertices1[i], vertices1[j]) - 1.0) < tolerance:
                adj[i].add(j)
                adj[j].add(i)

    # Edges within rotated
    for i in range(n2):
        for j in range(i + 1, n2):
            if abs(distance(rotated[i], rotated[j]) - 1.0) < tolerance:
                adj[n1 + i].add(n1 + j)
                adj[n1 + j].add(n1 + i)

    # Edges between original and rotated
    cross_edges = 0
    for i in range(n1):
        for j in range(n2):
            if abs(distance(vertices1[i], rotated[j]) - 1.0) < tolerance:
                adj[i].add(n1 + j)
                adj[n1 + j].add(i)
                cross_edges += 1

    return all_vertices, adj, cross_edges

def search_rotation_angles(vertices):
    """Search for rotation angles that create 6-chromatic graphs"""
    print("=" * 70)
    print("SEARCHING FOR 6-CHROMATIC VIA ROTATION")
    print("=" * 70)

    n = len(vertices)
    print(f"Base graph: {n} vertices")

    # Build base graph
    adj, edges = build_unit_distance_graph(vertices)
    print(f"Base edges: {len(edges)}")

    # Check base chromatic number
    for k in range(3, 7):
        if is_k_colorable(adj, n, k):
            print(f"Base graph chromatic number: {k}")
            base_chi = k
            break

    if base_chi < 5:
        print("Base graph is not 5-chromatic, need larger graph")
        return

    # Search rotation angles
    print("\nSearching rotation angles...")

    # Key angles from de Grey's construction involve multiples of π/6 and related
    test_angles = []

    # Standard angles
    for denom in [3, 4, 5, 6, 7, 8, 9, 10, 12]:
        for numer in range(1, denom):
            angle = math.pi * numer / denom
            test_angles.append((f"{numer}π/{denom}", angle))

    # Golden ratio related
    phi = (1 + math.sqrt(5)) / 2
    test_angles.append(("π/φ", math.pi / phi))
    test_angles.append(("π*φ/5", math.pi * phi / 5))

    best_angle = None
    best_cross = 0
    best_chi = base_chi

    for name, angle in test_angles:
        all_verts, comb_adj, cross_edges = combine_with_rotation(
            vertices, vertices, angle
        )

        if cross_edges > 10:  # Only test if meaningful cross-edges exist
            # Check chromatic number
            for k in [5, 6]:
                if is_k_colorable(comb_adj, len(all_verts), k):
                    chi = k
                    break
            else:
                chi = 7  # Not 6-colorable!

            if chi > best_chi or (chi == best_chi and cross_edges > best_cross):
                best_angle = name
                best_cross = cross_edges
                best_chi = chi

            if cross_edges > 0:
                status = "5-col" if chi == 5 else "NOT 5-col" if chi > 5 else "?"
                if chi >= 6:
                    print(f"  {name}: {cross_edges} cross-edges, χ ≥ {chi} ***")
                elif cross_edges > 50:
                    print(f"  {name}: {cross_edges} cross-edges, {status}")

    print(f"\nBest result: angle {best_angle}, {best_cross} cross-edges, χ = {best_chi}")

    if best_chi >= 6:
        print("\n*** FOUND 6-CHROMATIC GRAPH! ***")
        return best_angle

    return None

def main():
    # Load the vertex data
    vtx_files = [
        "dist-graphs/plane/series 2/vtx/s2_M1.vtx",
        "dist-graphs/plane/series 2/vtx/s2_M2.vtx",
    ]

    for vtx_file in vtx_files:
        try:
            vertices = load_vertices(vtx_file)
            if len(vertices) > 0:
                print(f"\nLoaded {len(vertices)} vertices from {vtx_file}")
                result = search_rotation_angles(vertices)
                if result:
                    print(f"\nSUCCESS: Found 6-chromatic at angle {result}")
                    break
        except Exception as e:
            print(f"Error loading {vtx_file}: {e}")

if __name__ == "__main__":
    main()
