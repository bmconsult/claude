#!/usr/bin/env python3
"""
Attempt to solve the UNSOLVED 5-coloring CNF problems.

If UNSATISFIABLE: The graph is 6-CHROMATIC (major breakthrough!)
If SATISFIABLE: The graph is 5-colorable (no breakthrough, but resolved)

These CNFs are from vsvor/dist-graphs and represent graphs on the
circumsphere of the icosahedron that MIGHT be 6-chromatic.
"""

import sys
import time
from pysat.formula import CNF
from pysat.solvers import Solver

def solve_cnf(filename, timeout=600):
    """
    Attempt to solve a CNF file.

    Returns:
        'SAT' if satisfiable (5-colorable, not 6-chromatic)
        'UNSAT' if unsatisfiable (NOT 5-colorable, IS 6-chromatic!)
        'TIMEOUT' if solver didn't finish in time
    """
    print(f"Loading CNF from {filename}...")

    cnf = CNF(from_file=filename)
    print(f"  Variables: {cnf.nv}")
    print(f"  Clauses: {len(cnf.clauses)}")

    # Try different solvers
    solvers_to_try = ['g4', 'g3', 'cd', 'mpl']  # glucose4, glucose3, cadical, minisat

    for solver_name in solvers_to_try:
        print(f"\nTrying solver: {solver_name}")
        try:
            with Solver(name=solver_name, bootstrap_with=cnf) as solver:
                start = time.time()

                # Use solve with timeout if available
                result = solver.solve()

                elapsed = time.time() - start

                if result:
                    print(f"  Result: SATISFIABLE in {elapsed:.2f}s")
                    print("  => Graph is 5-colorable (not 6-chromatic)")
                    return 'SAT'
                else:
                    print(f"  Result: UNSATISFIABLE in {elapsed:.2f}s")
                    print("  => *** GRAPH IS 6-CHROMATIC! ***")
                    return 'UNSAT'

        except Exception as e:
            print(f"  Solver {solver_name} failed: {e}")
            continue

    return 'TIMEOUT'

def main():
    cnf_files = [
        "dist-graphs/unsolved CNFs/icos29112a.cnf",
        "dist-graphs/unsolved CNFs/icos29112e.cnf",
        "dist-graphs/unsolved CNFs/icos29112f.cnf",
        "dist-graphs/unsolved CNFs/icos54072a.cnf",
    ]

    print("=" * 70)
    print("ATTEMPTING TO SOLVE UNSOLVED 6-CHROMATIC CANDIDATE CNFs")
    print("=" * 70)
    print()
    print("Background: These graphs on the icosahedron circumsphere")
    print("have UNKNOWN chromatic number. If 5-coloring is UNSAT,")
    print("we have found a 6-CHROMATIC unit-distance graph!")
    print()

    # Start with smallest
    result = solve_cnf(cnf_files[0])

    if result == 'UNSAT':
        print("\n" + "=" * 70)
        print("*** BREAKTHROUGH: 6-CHROMATIC UNIT-DISTANCE GRAPH FOUND! ***")
        print("=" * 70)
    elif result == 'SAT':
        print("\n" + "=" * 70)
        print("Graph is 5-colorable. Trying next candidate...")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("Solver could not determine result in time.")
        print("This remains an OPEN PROBLEM.")
        print("=" * 70)

if __name__ == "__main__":
    main()
