"""
Segment Tree with Lazy Propagation
Supports:
- Range sum queries: O(log n)
- Range updates (add value to range): O(log n)
"""

class SegmentTreeLazy:
    def __init__(self, arr):
        """
        Initialize segment tree from array.

        Args:
            arr: List of integers to build tree from
        """
        self.n = len(arr)
        self.tree = [0] * (4 * self.n) if self.n > 0 else []  # Segment tree array
        self.lazy = [0] * (4 * self.n) if self.n > 0 else []  # Lazy propagation array
        if self.n > 0:
            self._build(arr, 0, 0, self.n - 1)

    def _build(self, arr, node, start, end):
        """
        Build the segment tree recursively.

        Args:
            arr: Source array
            node: Current node index in tree
            start: Start of current range
            end: End of current range
        """
        if start == end:
            # Leaf node
            self.tree[node] = arr[start]
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2

            # Build left and right subtrees
            self._build(arr, left_child, start, mid)
            self._build(arr, right_child, mid + 1, end)

            # Internal node stores sum of children
            self.tree[node] = self.tree[left_child] + self.tree[right_child]

    def _push_down(self, node, start, end):
        """
        Push lazy value down to children.

        Args:
            node: Current node index
            start: Start of current range
            end: End of current range
        """
        if self.lazy[node] != 0:
            # Apply pending update to current node
            range_size = end - start + 1
            self.tree[node] += self.lazy[node] * range_size

            # If not a leaf, propagate to children
            if start != end:
                left_child = 2 * node + 1
                right_child = 2 * node + 2
                self.lazy[left_child] += self.lazy[node]
                self.lazy[right_child] += self.lazy[node]

            # Clear lazy value
            self.lazy[node] = 0

    def range_update(self, left, right, value):
        """
        Add 'value' to all elements in range [left, right].

        Args:
            left: Left boundary (inclusive)
            right: Right boundary (inclusive)
            value: Value to add to each element
        """
        if self.n == 0:
            return
        self._range_update(0, 0, self.n - 1, left, right, value)

    def _range_update(self, node, start, end, left, right, value):
        """
        Internal range update implementation.

        Args:
            node: Current node index
            start: Start of current node's range
            end: End of current node's range
            left: Start of update range
            right: End of update range
            value: Value to add
        """
        # Push down any pending updates first
        self._push_down(node, start, end)

        # No overlap
        if start > right or end < left:
            return

        # Complete overlap - update this node and mark children as lazy
        if start >= left and end <= right:
            range_size = end - start + 1
            self.tree[node] += value * range_size

            # Mark children as lazy if not a leaf
            if start != end:
                left_child = 2 * node + 1
                right_child = 2 * node + 2
                self.lazy[left_child] += value
                self.lazy[right_child] += value
            return

        # Partial overlap - recurse to children
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2

        self._range_update(left_child, start, mid, left, right, value)
        self._range_update(right_child, mid + 1, end, left, right, value)

        # Update current node after children are updated
        self._push_down(left_child, start, mid)
        self._push_down(right_child, mid + 1, end)
        self.tree[node] = self.tree[left_child] + self.tree[right_child]

    def range_query(self, left, right):
        """
        Query sum of elements in range [left, right].

        Args:
            left: Left boundary (inclusive)
            right: Right boundary (inclusive)

        Returns:
            Sum of elements in range
        """
        if self.n == 0:
            return 0
        return self._range_query(0, 0, self.n - 1, left, right)

    def _range_query(self, node, start, end, left, right):
        """
        Internal range query implementation.

        Args:
            node: Current node index
            start: Start of current node's range
            end: End of current node's range
            left: Start of query range
            right: End of query range

        Returns:
            Sum in the query range for this subtree
        """
        # No overlap
        if start > right or end < left:
            return 0

        # Push down any pending updates
        self._push_down(node, start, end)

        # Complete overlap
        if start >= left and end <= right:
            return self.tree[node]

        # Partial overlap - query both children
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2

        left_sum = self._range_query(left_child, start, mid, left, right)
        right_sum = self._range_query(right_child, mid + 1, end, left, right)

        return left_sum + right_sum

    def point_query(self, index):
        """
        Query value at a single index.

        Args:
            index: Index to query

        Returns:
            Value at index
        """
        return self.range_query(index, index)


def test_segment_tree():
    """Test the segment tree implementation."""
    print("=== Testing Segment Tree with Lazy Propagation ===\n")

    # Test 1: Basic construction and queries
    print("Test 1: Basic construction and queries")
    arr = [1, 3, 5, 7, 9, 11]
    st = SegmentTreeLazy(arr)

    print(f"Original array: {arr}")
    print(f"Sum [0, 2]: {st.range_query(0, 2)} (expected: 9)")
    print(f"Sum [1, 4]: {st.range_query(1, 4)} (expected: 24)")
    print(f"Sum [0, 5]: {st.range_query(0, 5)} (expected: 36)")
    print()

    # Test 2: Range updates
    print("Test 2: Range updates")
    st.range_update(1, 3, 10)  # Add 10 to indices 1, 2, 3
    print(f"After adding 10 to range [1, 3]:")
    print(f"Sum [0, 2]: {st.range_query(0, 2)} (expected: 29)")
    print(f"Sum [1, 4]: {st.range_query(1, 4)} (expected: 54)")
    print(f"Point query at index 2: {st.point_query(2)} (expected: 15)")
    print()

    # Test 3: Multiple updates
    print("Test 3: Multiple updates")
    st.range_update(0, 5, 5)  # Add 5 to all elements
    print(f"After adding 5 to range [0, 5]:")
    print(f"Sum [0, 5]: {st.range_query(0, 5)} (expected: 96)")
    print(f"Point query at index 0: {st.point_query(0)} (expected: 6)")
    print(f"Point query at index 3: {st.point_query(3)} (expected: 22)")
    print()

    # Test 4: Overlapping updates
    print("Test 4: Overlapping updates")
    arr2 = [0, 0, 0, 0, 0]
    st2 = SegmentTreeLazy(arr2)
    st2.range_update(0, 2, 5)
    st2.range_update(1, 3, 3)
    st2.range_update(2, 4, 2)
    print(f"Starting with [0, 0, 0, 0, 0]")
    print(f"After updates [0,2]+5, [1,3]+3, [2,4]+2:")
    for i in range(5):
        print(f"  Index {i}: {st2.point_query(i)} (expected: {[5, 8, 10, 5, 2][i]})")
    print()

    # Test 5: Large array
    print("Test 5: Large array performance")
    large_arr = list(range(1000))
    st_large = SegmentTreeLazy(large_arr)

    # Sum of 0..999 = 999*1000/2 = 499500
    result = st_large.range_query(0, 999)
    print(f"Sum of range [0, 999]: {result} (expected: 499500)")

    # Add 10 to range [100, 199] (100 elements)
    st_large.range_update(100, 199, 10)
    # New sum = 499500 + 100*10 = 500500
    result = st_large.range_query(0, 999)
    print(f"After adding 10 to [100, 199]: {result} (expected: 500500)")
    print()

    # Test 6: Edge cases
    print("Test 6: Edge cases")
    single = SegmentTreeLazy([42])
    print(f"Single element query: {single.range_query(0, 0)} (expected: 42)")
    single.range_update(0, 0, 8)
    print(f"After update: {single.range_query(0, 0)} (expected: 50)")
    print()

    print("=== All tests completed ===")


if __name__ == "__main__":
    test_segment_tree()
