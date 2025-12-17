"""
Falsification tests for Segment Tree with Lazy Propagation

These tests attempt to break the implementation by:
1. Testing boundary conditions
2. Testing lazy propagation accumulation
3. Testing interleaved queries and updates
4. Testing negative values
5. Testing empty ranges
"""

from segment_tree_lazy import SegmentTreeLazy


def verify_against_naive(st, arr, updates):
    """
    Verify segment tree against naive array implementation.

    Args:
        st: SegmentTreeLazy instance
        arr: Current state of array (after applying updates manually)
        updates: List of (left, right, value) updates to apply

    Returns:
        True if all queries match, False otherwise
    """
    for left, right, value in updates:
        st.range_update(left, right, value)
        # Apply to naive array
        for i in range(left, right + 1):
            arr[i] += value

    # Test all possible range queries
    n = len(arr)
    for i in range(n):
        for j in range(i, n):
            expected = sum(arr[i:j+1])
            actual = st.range_query(i, j)
            if expected != actual:
                print(f"MISMATCH at query [{i}, {j}]: expected {expected}, got {actual}")
                print(f"Array state: {arr}")
                return False
    return True


def test_falsification_suite():
    """Run comprehensive falsification tests."""

    print("=" * 70)
    print("FALSIFICATION TEST SUITE")
    print("=" * 70)

    # Test 1: Empty array edge case
    print("\nTest 1: Empty array")
    try:
        st = SegmentTreeLazy([])
        result = st.range_query(0, 0)
        print(f"  Empty array query: {result}")
        print(f"  ✗ FAIL: Should handle empty arrays gracefully")
    except (IndexError, ZeroDivisionError) as e:
        print(f"  ✓ PASS: Caught expected error: {type(e).__name__}")

    # Test 2: Negative updates and queries
    print("\nTest 2: Negative values")
    arr = [10, -5, 3, -7, 2]
    st = SegmentTreeLazy(arr[:])

    result = st.range_query(0, 4)
    expected = sum(arr)
    print(f"  Sum with negatives: {result} (expected: {expected}) - {'✓' if result == expected else '✗'}")

    st.range_update(1, 3, -10)
    arr_copy = arr[:]
    for i in range(1, 4):
        arr_copy[i] -= 10

    result = st.range_query(0, 4)
    expected = sum(arr_copy)
    print(f"  After negative update: {result} (expected: {expected}) - {'✓' if result == expected else '✗'}")

    # Test 3: Lazy accumulation without queries
    print("\nTest 3: Lazy accumulation stress")
    arr = [1] * 16
    st = SegmentTreeLazy(arr[:])

    # Apply many updates without any queries (forces lazy accumulation)
    updates = [
        (0, 15, 1),
        (0, 7, 2),
        (8, 15, 3),
        (4, 11, 5),
        (2, 13, -1),
    ]

    arr_naive = arr[:]
    for left, right, value in updates:
        st.range_update(left, right, value)
        for i in range(left, right + 1):
            arr_naive[i] += value

    # Now query everything - forces all lazy propagation
    all_match = True
    for i in range(16):
        result = st.point_query(i)
        expected = arr_naive[i]
        if result != expected:
            print(f"  ✗ Index {i}: {result} != {expected}")
            all_match = False

    if all_match:
        print(f"  ✓ PASS: All 16 elements match after lazy accumulation")
    else:
        print(f"  ✗ FAIL: Lazy propagation incorrect")

    # Test 4: Interleaved updates and queries
    print("\nTest 4: Interleaved updates and queries")
    arr = [0] * 10
    st = SegmentTreeLazy(arr[:])
    arr_naive = arr[:]

    operations = [
        ('update', 0, 4, 5),
        ('query', 2, 6, None),
        ('update', 3, 7, -2),
        ('query', 0, 9, None),
        ('update', 5, 9, 3),
        ('query', 4, 8, None),
    ]

    all_match = True
    for op in operations:
        if op[0] == 'update':
            _, left, right, value = op
            st.range_update(left, right, value)
            for i in range(left, right + 1):
                arr_naive[i] += value
        else:  # query
            _, left, right, _ = op
            result = st.range_query(left, right)
            expected = sum(arr_naive[left:right+1])
            if result != expected:
                print(f"  ✗ Query [{left}, {right}]: {result} != {expected}")
                all_match = False

    if all_match:
        print(f"  ✓ PASS: All interleaved operations correct")
    else:
        print(f"  ✗ FAIL: Mismatch in interleaved operations")

    # Test 5: All possible queries after updates
    print("\nTest 5: Exhaustive query verification")
    arr = [1, 2, 3, 4, 5, 6, 7, 8]
    st = SegmentTreeLazy(arr[:])

    updates = [
        (1, 5, 10),
        (3, 6, -5),
        (0, 7, 2),
    ]

    if verify_against_naive(st, arr[:], updates):
        print(f"  ✓ PASS: All {8*(8+1)//2} range queries match naive implementation")
    else:
        print(f"  ✗ FAIL: Mismatch found")

    # Test 6: Single element ranges
    print("\nTest 6: Single element edge cases")
    arr = [5]
    st = SegmentTreeLazy(arr)

    test_cases = [
        (0, 0, 5, "Initial query"),
        ('update', 0, 0, 3, None),
        (0, 0, 8, "After update"),
        ('update', 0, 0, -10, None),
        (0, 0, -2, "After negative update"),
    ]

    all_pass = True
    for case in test_cases:
        if case[0] == 'update':
            st.range_update(case[1], case[2], case[3])
        else:
            result = st.range_query(case[0], case[1])
            expected = case[2]
            desc = case[3]
            if result != expected:
                print(f"  ✗ {desc}: {result} != {expected}")
                all_pass = False

    if all_pass:
        print(f"  ✓ PASS: Single element operations correct")
    else:
        print(f"  ✗ FAIL: Single element operations incorrect")

    # Test 7: Maximum overlap
    print("\nTest 7: Maximum overlap scenario")
    arr = [0] * 8
    st = SegmentTreeLazy(arr[:])
    arr_naive = arr[:]

    # Update every possible range with value = range size
    for left in range(8):
        for right in range(left, 8):
            value = right - left + 1
            st.range_update(left, right, value)
            for i in range(left, right + 1):
                arr_naive[i] += value

    # Verify final state
    all_match = True
    for i in range(8):
        result = st.point_query(i)
        expected = arr_naive[i]
        if result != expected:
            print(f"  ✗ Index {i}: {result} != {expected}")
            all_match = False

    if all_match:
        print(f"  ✓ PASS: Maximum overlap handled correctly")
        print(f"  Final values: {[st.point_query(i) for i in range(8)]}")
    else:
        print(f"  ✗ FAIL: Maximum overlap incorrect")

    # Test 8: Zero updates
    print("\nTest 8: Zero value updates")
    arr = [1, 2, 3, 4, 5]
    st = SegmentTreeLazy(arr[:])

    st.range_update(1, 3, 0)
    result = [st.point_query(i) for i in range(5)]
    expected = arr

    if result == expected:
        print(f"  ✓ PASS: Zero updates don't change values")
    else:
        print(f"  ✗ FAIL: Zero updates changed values: {result} != {expected}")

    print("\n" + "=" * 70)
    print("FALSIFICATION SUITE COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    test_falsification_suite()
