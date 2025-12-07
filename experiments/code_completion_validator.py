#!/usr/bin/env python3
"""
Code Completion Validator
Validates that generated code is syntactically complete and runnable.
"""

import ast
import sys
from typing import Tuple, List


def validate_code_completion(code: str) -> Tuple[bool, List[str]]:
    """
    Validates that code is syntactically complete and valid.
    
    Args:
        code: String containing Python code to validate
        
    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []
    
    # Check for basic completeness indicators
    if not code.strip():
        issues.append("Code is empty")
        return False, issues
    
    # Check for unclosed brackets/parentheses/braces
    stack = []
    pairs = {'(': ')', '[': ']', '{': '}'}
    for i, char in enumerate(code):
        if char in pairs:
            stack.append(char)
        elif char in pairs.values():
            if not stack or pairs[stack[-1]] != char:
                issues.append(f"Unmatched closing bracket at position {i}")
            else:
                stack.pop()
    
    if stack:
        issues.append(f"Unclosed brackets: {stack}")
    
    # Check for unclosed quotes
    in_single = False
    in_double = False
    in_triple_single = False
    in_triple_double = False
    i = 0
    while i < len(code):
        if code[i:i+3] == '"""' and not in_single and not in_triple_single:
            in_triple_double = not in_triple_double
            i += 3
            continue
        elif code[i:i+3] == "'''" and not in_double and not in_triple_double:
            in_triple_single = not in_triple_single
            i += 3
            continue
        elif code[i] == '"' and not in_single and not in_triple_single and not in_triple_double:
            in_double = not in_double
        elif code[i] == "'" and not in_double and not in_triple_single and not in_triple_double:
            in_single = not in_single
        i += 1
    
    if in_single or in_double or in_triple_single or in_triple_double:
        issues.append("Unclosed string literal")
    
    # Try to parse as AST
    try:
        ast.parse(code)
    except SyntaxError as e:
        issues.append(f"Syntax error: {e.msg} at line {e.lineno}")
        return False, issues
    
    # If we got here with no issues, code is valid
    if not issues:
        return True, ["Code is syntactically valid"]
    
    return False, issues


def test_validator():
    """Test the code completion validator."""
    
    # Test 1: Valid code
    valid_code = """
def hello():
    print("Hello, world!")
    return True
"""
    is_valid, issues = validate_code_completion(valid_code)
    print(f"Test 1 (valid code): {is_valid}")
    print(f"  Issues: {issues}\n")
    
    # Test 2: Unclosed bracket
    invalid_code1 = "def foo():\n    x = [1, 2, 3\n"
    is_valid, issues = validate_code_completion(invalid_code1)
    print(f"Test 2 (unclosed bracket): {is_valid}")
    print(f"  Issues: {issues}\n")
    
    # Test 3: Unclosed string
    invalid_code2 = 'print("Hello world)\n'
    is_valid, issues = validate_code_completion(invalid_code2)
    print(f"Test 3 (unclosed string): {is_valid}")
    print(f"  Issues: {issues}\n")
    
    # Test 4: Empty code
    is_valid, issues = validate_code_completion("")
    print(f"Test 4 (empty code): {is_valid}")
    print(f"  Issues: {issues}\n")


if __name__ == "__main__":
    test_validator()