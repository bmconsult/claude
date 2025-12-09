"""
SAT-based solver for R(3,3,4) Ramsey problem

Goal: Determine if a 3-coloring of K_n exists where:
- Color 1 (RED) has no triangle
- Color 2 (GREEN) has no triangle
- Color 3 (BLUE) has no K_4

Known: 30 ≤ R(3,3,4) ≤ 31
If n=30 has valid coloring: R(3,3,4) > 30, so R(3,3,4) = 31
If n=30 has no valid coloring: R(3,3,4) = 30
"""

from itertools import combinations
from typing import List, Tuple, Dict, Optional
import subprocess
import os
import tempfile

def edge_to_var(i: int, j: int, color: int, n: int) -> int:
    """
    Convert edge (i,j) with color to variable number.
    i < j always (canonical ordering)
    color in {0, 1, 2} for RED, GREEN, BLUE
    """
    if i > j:
        i, j = j, i
    # Edge index from 0 to n(n-1)/2 - 1
    edge_idx = i * n - (i * (i + 1)) // 2 + (j - i - 1)
    # 3 variables per edge (one per color)
    return 3 * edge_idx + color + 1  # +1 for DIMACS (1-indexed)

def generate_cnf(n: int) -> Tuple[List[List[int]], int]:
    """
    Generate CNF clauses for R(3,3,4) coloring of K_n.

    Returns: (clauses, num_vars)
    """
    clauses = []
    num_edges = n * (n - 1) // 2
    num_vars = 3 * num_edges  # 3 colors per edge

    vertices = list(range(n))

    # Constraint 1: Each edge has exactly one color
    # At least one: (r ∨ g ∨ b)
    # At most one: (¬r ∨ ¬g), (¬r ∨ ¬b), (¬g ∨ ¬b)
    for i, j in combinations(vertices, 2):
        r = edge_to_var(i, j, 0, n)  # RED
        g = edge_to_var(i, j, 1, n)  # GREEN
        b = edge_to_var(i, j, 2, n)  # BLUE

        # At least one color
        clauses.append([r, g, b])
        # At most one color
        clauses.append([-r, -g])
        clauses.append([-r, -b])
        clauses.append([-g, -b])

    # Constraint 2: No RED triangle
    for v1, v2, v3 in combinations(vertices, 3):
        r12 = edge_to_var(v1, v2, 0, n)
        r13 = edge_to_var(v1, v3, 0, n)
        r23 = edge_to_var(v2, v3, 0, n)
        # NOT (r12 AND r13 AND r23)
        clauses.append([-r12, -r13, -r23])

    # Constraint 3: No GREEN triangle
    for v1, v2, v3 in combinations(vertices, 3):
        g12 = edge_to_var(v1, v2, 1, n)
        g13 = edge_to_var(v1, v3, 1, n)
        g23 = edge_to_var(v2, v3, 1, n)
        # NOT (g12 AND g13 AND g23)
        clauses.append([-g12, -g13, -g23])

    # Constraint 4: No BLUE K_4
    for v1, v2, v3, v4 in combinations(vertices, 4):
        # All 6 edges of K_4 must not all be blue
        b12 = edge_to_var(v1, v2, 2, n)
        b13 = edge_to_var(v1, v3, 2, n)
        b14 = edge_to_var(v1, v4, 2, n)
        b23 = edge_to_var(v2, v3, 2, n)
        b24 = edge_to_var(v2, v4, 2, n)
        b34 = edge_to_var(v3, v4, 2, n)
        clauses.append([-b12, -b13, -b14, -b23, -b24, -b34])

    return clauses, num_vars

def write_dimacs(clauses: List[List[int]], num_vars: int, filename: str):
    """Write CNF to DIMACS format file."""
    with open(filename, 'w') as f:
        f.write(f"c R(3,3,4) SAT encoding\n")
        f.write(f"p cnf {num_vars} {len(clauses)}\n")
        for clause in clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")

def solve_with_pysat(clauses: List[List[int]], num_vars: int) -> Tuple[bool, Optional[List[int]]]:
    """Solve using python-sat library."""
    try:
        from pysat.solvers import Glucose3

        solver = Glucose3()
        for clause in clauses:
            solver.add_clause(clause)

        if solver.solve():
            model = solver.get_model()
            solver.delete()
            return True, model
        else:
            solver.delete()
            return False, None
    except Exception as e:
        print(f"Solver error: {e}")
        return False, None

def decode_coloring(assignment: List[int], n: int) -> Dict[Tuple[int, int], str]:
    """Decode SAT assignment to edge coloring."""
    colors = {0: "RED", 1: "GREEN", 2: "BLUE"}
    coloring = {}

    for i, j in combinations(range(n), 2):
        for c in range(3):
            var = edge_to_var(i, j, c, n)
            if var in assignment:
                coloring[(i, j)] = colors[c]
                break

    return coloring

def verify_coloring(coloring: Dict[Tuple[int, int], str], n: int) -> bool:
    """Verify that coloring satisfies R(3,3,4) constraints."""
    vertices = list(range(n))

    # Check no RED triangle
    for v1, v2, v3 in combinations(vertices, 3):
        edges = [(v1, v2), (v1, v3), (v2, v3)]
        if all(coloring.get(e, coloring.get((e[1], e[0]))) == "RED" for e in edges):
            print(f"RED triangle: {v1}, {v2}, {v3}")
            return False

    # Check no GREEN triangle
    for v1, v2, v3 in combinations(vertices, 3):
        edges = [(v1, v2), (v1, v3), (v2, v3)]
        if all(coloring.get(e, coloring.get((e[1], e[0]))) == "GREEN" for e in edges):
            print(f"GREEN triangle: {v1}, {v2}, {v3}")
            return False

    # Check no BLUE K_4
    for v1, v2, v3, v4 in combinations(vertices, 4):
        edges = [(v1, v2), (v1, v3), (v1, v4), (v2, v3), (v2, v4), (v3, v4)]
        if all(coloring.get(e, coloring.get((e[1], e[0]))) == "BLUE" for e in edges):
            print(f"BLUE K_4: {v1}, {v2}, {v3}, {v4}")
            return False

    return True

def print_stats(n: int, clauses: List[List[int]], num_vars: int):
    """Print problem statistics."""
    num_edges = n * (n - 1) // 2
    num_triangles = n * (n - 1) * (n - 2) // 6
    num_k4 = n * (n - 1) * (n - 2) * (n - 3) // 24

    print(f"=== R(3,3,4) SAT Encoding for K_{n} ===")
    print(f"Vertices: {n}")
    print(f"Edges: {num_edges}")
    print(f"Variables: {num_vars} (3 per edge)")
    print(f"Triangles: {num_triangles}")
    print(f"K_4 subgraphs: {num_k4}")
    print(f"Total clauses: {len(clauses)}")
    print(f"  - Edge color constraints: {4 * num_edges}")
    print(f"  - No RED triangle: {num_triangles}")
    print(f"  - No GREEN triangle: {num_triangles}")
    print(f"  - No BLUE K_4: {num_k4}")

def main():
    # Start with smaller n to test
    for n in [10, 15, 20, 25, 29, 30]:
        print(f"\n{'='*50}")
        print(f"Testing n = {n}")

        clauses, num_vars = generate_cnf(n)
        print_stats(n, clauses, num_vars)

        # Try to solve with pysat
        print("Running SAT solver (Glucose3)...")
        sat, assignment = solve_with_pysat(clauses, num_vars)

        if sat:
            print(f"✓ SATISFIABLE: Valid 3-coloring exists for K_{n}")
            if assignment:
                coloring = decode_coloring(assignment, n)
                # Count colors
                counts = {"RED": 0, "GREEN": 0, "BLUE": 0}
                for c in coloring.values():
                    counts[c] += 1
                print(f"  Color distribution: {counts}")
                # Verify
                if verify_coloring(coloring, n):
                    print("  ✓ Coloring verified correct")
                else:
                    print("  ✗ Coloring verification FAILED")
        else:
            print(f"✗ UNSATISFIABLE: No valid 3-coloring for K_{n}")
            print(f"  This would prove R(3,3,4) = {n}")
            break

        if n == 30:
            print("\n" + "="*50)
            if sat:
                print("RESULT: R(3,3,4) > 30, so R(3,3,4) = 31")
            else:
                print("RESULT: R(3,3,4) = 30")

if __name__ == "__main__":
    main()
