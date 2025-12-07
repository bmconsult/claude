#!/usr/bin/env python3
"""
Verification Engine for N-Queens Solutions
Checks if a proposed solution actually satisfies all constraints
"""

def verify_n_queens(solution):
    """
    Verify if a solution to N-Queens is valid.
    
    Args:
        solution: List where solution[col] = row for queen in that column
                 (0-indexed)
    
    Returns:
        tuple: (is_valid, list_of_violations)
    """
    n = len(solution)
    violations = []
    
    # Check 1: All values should be in valid range
    for col, row in enumerate(solution):
        if row < 1 or row > n:
            violations.append(f"Column {col}: row value {row} out of range [1,{n}]")
    
    # Check 2: No two queens in same row
    row_counts = {}
    for col, row in enumerate(solution):
        if row in row_counts:
            violations.append(f"Row {row} conflict: columns {row_counts[row]} and {col}")
        else:
            row_counts[row] = col
    
    # Check 3: No two queens on same diagonal
    # For diagonal: row - col is constant
    # For anti-diagonal: row + col is constant
    diag_map = {}
    anti_diag_map = {}
    
    for col, row in enumerate(solution):
        # Convert to 0-indexed for diagonal calculation
        col_idx = col
        row_idx = row - 1
        
        diag = row_idx - col_idx
        anti_diag = row_idx + col_idx
        
        if diag in diag_map:
            violations.append(
                f"Diagonal attack: column {col} (row {row}) and "
                f"column {diag_map[diag][0]} (row {diag_map[diag][1]})"
            )
        else:
            diag_map[diag] = (col, row)
        
        if anti_diag in anti_diag_map:
            violations.append(
                f"Anti-diagonal attack: column {col} (row {row}) and "
                f"column {anti_diag_map[anti_diag][0]} (row {anti_diag_map[anti_diag][1]})"
            )
        else:
            anti_diag_map[anti_diag] = (col, row)
    
    is_valid = len(violations) == 0
    return is_valid, violations


def test_verification():
    """Test the verification engine with known cases"""
    
    print("=" * 60)
    print("N-Queens Solution Verification Engine")
    print("=" * 60)
    
    # Test case from the gap: claimed valid but has diagonal attacks
    print("\nTest 1: Solution (2,4,5,1,3) - claimed valid")
    solution1 = [2, 4, 5, 1, 3]
    is_valid, violations = verify_n_queens(solution1)
    print(f"Valid: {is_valid}")
    if violations:
        print("Violations found:")
        for v in violations:
            print(f"  - {v}")
    
    # Test case: Actually valid 5-queens solution
    print("\nTest 2: Solution (1,3,5,2,4) - should be valid")
    solution2 = [1, 3, 5, 2, 4]
    is_valid, violations = verify_n_queens(solution2)
    print(f"Valid: {is_valid}")
    if violations:
        print("Violations found:")
        for v in violations:
            print(f"  - {v}")
    
    # Test case: Row conflict
    print("\nTest 3: Solution (1,1,2,3,4) - row conflict")
    solution3 = [1, 1, 2, 3, 4]
    is_valid, violations = verify_n_queens(solution3)
    print(f"Valid: {is_valid}")
    if violations:
        print("Violations found:")
        for v in violations:
            print(f"  - {v}")


if __name__ == "__main__":
    test_verification()