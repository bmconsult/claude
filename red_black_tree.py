#!/usr/bin/env python3
"""Red-Black Tree implementation with insertion and rotations."""

from enum import Enum
from typing import Optional

class Color(Enum):
    RED = 0
    BLACK = 1

class Node:
    def __init__(self, key: int):
        self.key = key
        self.color = Color.RED  # New nodes are always red
        self.left: Optional['Node'] = None
        self.right: Optional['Node'] = None
        self.parent: Optional['Node'] = None

class RedBlackTree:
    def __init__(self):
        self.NIL = Node(0)
        self.NIL.color = Color.BLACK
        self.root = self.NIL

    def left_rotate(self, x: Node):
        """Left rotation around node x."""
        y = x.right
        x.right = y.left

        if y.left != self.NIL:
            y.left.parent = x

        y.parent = x.parent

        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def right_rotate(self, y: Node):
        """Right rotation around node y."""
        x = y.left
        y.left = x.right

        if x.right != self.NIL:
            x.right.parent = y

        x.parent = y.parent

        if y.parent is None:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x

        x.right = y
        y.parent = x

    def insert(self, key: int):
        """Insert a key into the red-black tree."""
        node = Node(key)
        node.left = self.NIL
        node.right = self.NIL

        parent = None
        current = self.root

        # BST insertion - find position
        while current != self.NIL:
            parent = current
            if node.key < current.key:
                current = current.left
            else:
                current = current.right

        node.parent = parent

        if parent is None:
            self.root = node
        elif node.key < parent.key:
            parent.left = node
        else:
            parent.right = node

        # Fix red-black properties
        self._fix_insert(node)

    def _fix_insert(self, node: Node):
        """Fix red-black tree violations after insertion."""
        while node.parent and node.parent.color == Color.RED:
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right

                if uncle.color == Color.RED:
                    # Case 1: Uncle is red - recolor
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        # Case 2: Node is right child - left rotate
                        node = node.parent
                        self.left_rotate(node)
                    # Case 3: Node is left child - right rotate
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self.right_rotate(node.parent.parent)
            else:
                # Mirror cases for right subtree
                uncle = node.parent.parent.left

                if uncle.color == Color.RED:
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self.left_rotate(node.parent.parent)

        self.root.color = Color.BLACK

    def inorder(self, node: Optional[Node] = None) -> list:
        """Return inorder traversal."""
        if node is None:
            node = self.root
        result = []
        if node != self.NIL:
            result.extend(self.inorder(node.left))
            result.append((node.key, 'R' if node.color == Color.RED else 'B'))
            result.extend(self.inorder(node.right))
        return result

    def _verify_properties(self, node: Optional[Node] = None) -> tuple[bool, int]:
        """Verify red-black properties. Returns (valid, black_height)."""
        if node is None:
            node = self.root

        if node == self.NIL:
            return True, 1

        # Property: Red nodes have black children
        if node.color == Color.RED:
            if (node.left != self.NIL and node.left.color == Color.RED) or \
               (node.right != self.NIL and node.right.color == Color.RED):
                return False, 0

        left_valid, left_black = self._verify_properties(node.left)
        right_valid, right_black = self._verify_properties(node.right)

        if not left_valid or not right_valid:
            return False, 0

        # Property: Equal black height on all paths
        if left_black != right_black:
            return False, 0

        return True, left_black + (1 if node.color == Color.BLACK else 0)

    def is_valid(self) -> bool:
        """Check if tree satisfies all red-black properties."""
        if self.root == self.NIL:
            return True
        if self.root.color != Color.BLACK:
            return False
        valid, _ = self._verify_properties()
        return valid


def test_red_black_tree():
    """Test the red-black tree implementation."""
    print("Testing Red-Black Tree Implementation")
    print("=" * 50)

    tree = RedBlackTree()

    # Test 1: Insert sequence that triggers all rotation cases
    test_values = [41, 38, 31, 12, 19, 8]
    print(f"\nInserting: {test_values}")

    for val in test_values:
        tree.insert(val)
        valid = tree.is_valid()
        print(f"  After inserting {val}: valid={valid}")
        if not valid:
            print("    VIOLATION DETECTED!")
            return False

    print(f"\nInorder traversal: {tree.inorder()}")

    # Test 2: Larger sequence
    tree2 = RedBlackTree()
    large_test = [50, 25, 75, 10, 30, 60, 90, 5, 15, 27, 35, 55, 65, 85, 95]
    print(f"\nLarger test - Inserting: {large_test}")

    for val in large_test:
        tree2.insert(val)

    valid = tree2.is_valid()
    print(f"Tree valid after all insertions: {valid}")
    print(f"Inorder: {tree2.inorder()}")

    # Test 3: Sequential insertion (worst case for BST)
    tree3 = RedBlackTree()
    sequential = list(range(1, 16))
    print(f"\nSequential insertion (BST worst case): {sequential}")

    for val in sequential:
        tree3.insert(val)

    valid = tree3.is_valid()
    print(f"Tree valid: {valid}")
    print(f"Inorder: {tree3.inorder()}")

    # Calculate approximate height
    def get_height(tree, node):
        if node == tree.NIL:
            return 0
        return 1 + max(get_height(tree, node.left), get_height(tree, node.right))

    height = get_height(tree3, tree3.root)
    print(f"Height: {height} (theoretical max for 15 nodes: ~2*log2(16) ≈ 8)")

    print("\n" + "=" * 50)
    print("ALL TESTS PASSED" if valid else "TESTS FAILED")
    return valid


if __name__ == "__main__":
    success = test_red_black_tree()
    exit(0 if success else 1)
