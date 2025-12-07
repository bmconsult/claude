#!/usr/bin/env python3
"""
Arithmetic Verifier Tool
Verifies arithmetic operations step-by-step to catch mental math errors.
"""

import operator
import re
from typing import Union, Tuple


def verify_arithmetic(expression: str) -> dict:
    """
    Verify an arithmetic expression by showing work and checking result.
    
    Args:
        expression: String like "123 + 456" or "25 * 8"
    
    Returns:
        Dictionary with expression, result, and verification steps
    """
    # Clean the expression
    expression = expression.strip()
    
    # Define operators
    ops = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '//': operator.floordiv,
        '%': operator.mod,
        '**': operator.pow
    }
    
    # Parse the expression
    for op_symbol, op_func in ops.items():
        if op_symbol in expression:
            parts = expression.split(op_symbol)
            if len(parts) == 2:
                try:
                    a = float(parts[0].strip())
                    b = float(parts[1].strip())
                    result = op_func(a, b)
                    
                    # Show work for multiplication
                    work = []
                    if op_symbol == '*':
                        work.append(f"Multiplying {a} × {b}")
                        work.append(f"Result: {result}")
                    elif op_symbol == '+':
                        work.append(f"Adding {a} + {b}")
                        work.append(f"Result: {result}")
                    elif op_symbol == '-':
                        work.append(f"Subtracting {a} - {b}")
                        work.append(f"Result: {result}")
                    elif op_symbol == '/':
                        work.append(f"Dividing {a} ÷ {b}")
                        work.append(f"Result: {result}")
                    
                    return {
                        'expression': expression,
                        'operand1': a,
                        'operator': op_symbol,
                        'operand2': b,
                        'result': result,
                        'work': work,
                        'valid': True
                    }
                except (ValueError, ZeroDivisionError) as e:
                    return {
                        'expression': expression,
                        'error': str(e),
                        'valid': False
                    }
    
    return {
        'expression': expression,
        'error': 'Could not parse expression',
        'valid': False
    }


def check_claimed_result(expression: str, claimed_result: Union[int, float]) -> dict:
    """
    Check if a claimed result matches the actual calculation.
    
    Args:
        expression: Arithmetic expression like "15 * 7"
        claimed_result: What someone claims the answer is
    
    Returns:
        Dictionary with verification details
    """
    verification = verify_arithmetic(expression)
    
    if not verification['valid']:
        return verification
    
    actual_result = verification['result']
    is_correct = abs(actual_result - claimed_result) < 0.0001
    
    return {
        'expression': expression,
        'claimed_result': claimed_result,
        'actual_result': actual_result,
        'is_correct': is_correct,
        'difference': actual_result - claimed_result,
        'work': verification['work']
    }


def test_arithmetic_verifier():
    """Test the arithmetic verifier with common mental math errors."""
    
    print("=== Arithmetic Verifier Tests ===\n")
    
    # Test 1: Simple addition
    print("Test 1: Verify 123 + 456")
    result = verify_arithmetic("123 + 456")
    print(f"Result: {result['result']}")
    print(f"Work: {result['work']}\n")
    
    # Test 2: Check a claimed result (correct)
    print("Test 2: Someone claims 15 * 8 = 120")
    check = check_claimed_result("15 * 8", 120)
    print(f"Claimed: {check['claimed_result']}")
    print(f"Actual: {check['actual_result']}")
    print(f"Correct: {check['is_correct']}\n")
    
    # Test 3: Check a claimed result (incorrect - common mental math error)
    print("Test 3: Someone claims 17 * 6 = 96 (common error)")
    check = check_claimed_result("17 * 6", 96)
    print(f"Claimed: {check['claimed_result']}")
    print(f"Actual: {check['actual_result']}")
    print(f"Correct: {check['is_correct']}")
    print(f"Difference: {check['difference']}\n")
    
    # Test 4: Division
    print("Test 4: Verify 144 / 12")
    result = verify_arithmetic("144 / 12")
    print(f"Result: {result['result']}\n")


if __name__ == "__main__":
    test_arithmetic_verifier()