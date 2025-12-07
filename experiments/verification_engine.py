"""
Verification Engine

The problem: Claude makes errors in constraint verification even when asked to verify.
The solution: Actually compute whether solutions satisfy constraints.

This is not "reasoning better" - it's offloading verification to code.
"""

from typing import List, Tuple, Callable, Dict, Any
from dataclasses import dataclass


@dataclass
class ConstraintResult:
    """Result of checking a constraint."""
    satisfied: bool
    constraint_name: str
    details: str


def verify_nqueens(positions: List[Tuple[int, int]],
                   no_corners: bool = False,
                   sum_rows: int = None) -> List[ConstraintResult]:
    """
    Verify an N-Queens solution.

    Args:
        positions: List of (row, col) tuples, 1-indexed
        no_corners: If True, no queen can be in a corner
        sum_rows: If set, sum of row positions must equal this

    Returns:
        List of constraint check results
    """
    results = []
    n = len(positions)

    # Check 1: All positions unique (one per row, one per col)
    rows = [p[0] for p in positions]
    cols = [p[1] for p in positions]

    rows_unique = len(set(rows)) == n
    cols_unique = len(set(cols)) == n

    results.append(ConstraintResult(
        satisfied=rows_unique,
        constraint_name="unique_rows",
        details=f"Rows: {rows}, unique: {rows_unique}"
    ))

    results.append(ConstraintResult(
        satisfied=cols_unique,
        constraint_name="unique_cols",
        details=f"Cols: {cols}, unique: {cols_unique}"
    ))

    # Check 2: No diagonal attacks
    diagonal_ok = True
    diagonal_details = []

    for i in range(n):
        for j in range(i + 1, n):
            r1, c1 = positions[i]
            r2, c2 = positions[j]

            if abs(r1 - r2) == abs(c1 - c2):
                diagonal_ok = False
                diagonal_details.append(f"({r1},{c1}) and ({r2},{c2}) are diagonal")

    results.append(ConstraintResult(
        satisfied=diagonal_ok,
        constraint_name="no_diagonal_attacks",
        details="; ".join(diagonal_details) if diagonal_details else "No diagonal attacks"
    ))

    # Check 3: No corners (if specified)
    if no_corners:
        grid_size = max(max(rows), max(cols))  # Assume square
        corners = [(1, 1), (1, grid_size), (grid_size, 1), (grid_size, grid_size)]
        corner_violations = [p for p in positions if p in corners]

        results.append(ConstraintResult(
            satisfied=len(corner_violations) == 0,
            constraint_name="no_corners",
            details=f"Corner violations: {corner_violations}" if corner_violations else "No corners"
        ))

    # Check 4: Row sum (if specified)
    if sum_rows is not None:
        actual_sum = sum(rows)
        results.append(ConstraintResult(
            satisfied=actual_sum == sum_rows,
            constraint_name="row_sum",
            details=f"Expected sum: {sum_rows}, actual: {actual_sum}"
        ))

    return results


def verify_solution(solution: Any,
                    constraints: List[Callable[[Any], ConstraintResult]]) -> Dict:
    """
    Generic verification: apply a list of constraint functions to a solution.
    """
    results = []
    all_satisfied = True

    for constraint_fn in constraints:
        result = constraint_fn(solution)
        results.append(result)
        if not result.satisfied:
            all_satisfied = False

    return {
        "valid": all_satisfied,
        "results": results
    }


def print_verification(results: List[ConstraintResult]):
    """Pretty print verification results."""
    print("\n=== VERIFICATION RESULTS ===\n")

    all_passed = True
    for r in results:
        status = "✓" if r.satisfied else "✗"
        print(f"{status} {r.constraint_name}: {r.details}")
        if not r.satisfied:
            all_passed = False

    print()
    if all_passed:
        print("SOLUTION VALID")
    else:
        print("SOLUTION INVALID")

    return all_passed


if __name__ == "__main__":
    # Test the Claude-generated solution that was wrong
    print("Testing Claude's claimed solution (2,4,5,1,3):")
    print("Positions: [(1,2), (2,4), (3,5), (4,1), (5,3)]")

    solution = [(1, 2), (2, 4), (3, 5), (4, 1), (5, 3)]
    results = verify_nqueens(solution, no_corners=True, sum_rows=15)

    valid = print_verification(results)

    print("\n" + "="*50)
    print("\nNow let's find ACTUAL valid solutions:")

    # Brute force search for valid solutions
    from itertools import permutations

    valid_solutions = []
    for perm in permutations(range(1, 6)):  # All column arrangements
        positions = [(row, col) for row, col in enumerate(perm, start=1)]
        results = verify_nqueens(positions, no_corners=True, sum_rows=15)

        if all(r.satisfied for r in results):
            valid_solutions.append(positions)

    print(f"\nFound {len(valid_solutions)} valid solutions:")
    for sol in valid_solutions:
        cols = [c for r, c in sol]
        print(f"  Columns: {cols} -> Positions: {sol}")
