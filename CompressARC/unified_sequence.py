"""
Unified Sequence Transform System

Integrates:
1. Permutation learning (for positional transforms like reverse, swap, rotate)
2. Value modules (for value transforms like running_max, mirror_add, increment)

Strategy:
- Try permutation first (simpler, 100 params)
- If loss doesn't converge (>0.1 after training), try value modules
- Return whichever works better
- MDL principle: prefer simpler explanation

This is the complete sequence transform learner.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Tuple, Optional
import random

# Import from existing modules
from permutation_learner import SequencePermutationSystem
from value_modules import ValueTransformSystem, apply_transform as apply_value_transform


class UnifiedSequenceSystem:
    """
    Unified system for learning ANY sequence transform.

    Strategy:
    1. Try permutation learning first (simplest)
    2. If permutation fails, try value modules
    3. Select whichever gives lower loss
    4. MDL prefers simpler models when both work
    """

    def __init__(self, max_len: int = 10):
        self.max_len = max_len
        self.perm_system = None
        self.value_system = None
        self.examples: List[Tuple[List[int], List[int]]] = []
        self.selected_system = None
        self.perm_loss = float('inf')
        self.value_loss = float('inf')

    def add_example(self, input_seq: List[int], output_seq: List[int]):
        """Add training example."""
        self.examples.append((input_seq, output_seq))

    def train(self, max_steps: int = 500, perm_threshold: float = 0.01, value_threshold: float = 0.01) -> str:
        """
        Train the system to learn the transform.

        Returns: 'permutation' or 'value' depending on which system worked.
        """
        if not self.examples:
            return 'none'

        # Try permutation first (simpler)
        print("  Trying permutation learning...")
        self.perm_system = SequencePermutationSystem(self.max_len)
        for inp, out in self.examples:
            self.perm_system.add_example(inp, out)

        perm_steps = self.perm_system.train_batch(max_steps=max_steps, threshold=perm_threshold)
        self.perm_loss = self._compute_loss(self.perm_system)
        print(f"    Permutation: {perm_steps} steps, loss={self.perm_loss:.4f}")

        # If permutation works well, use it (less than 1 error on average)
        if self.perm_loss < 0.5:
            print("    → Selected: PERMUTATION (low loss)")
            self.selected_system = 'permutation'
            return 'permutation'

        # Try value modules (use their default stricter threshold)
        print("  Trying value modules...")
        self.value_system = ValueTransformSystem(self.max_len)
        for inp, out in self.examples:
            self.value_system.add_example(inp, out)

        # Use value module's stricter default threshold
        value_steps = self.value_system.train_batch()
        self.value_loss = self._compute_loss(self.value_system)
        print(f"    Value: {value_steps} steps, loss={self.value_loss:.4f}")

        # Select the one with lower loss
        if self.perm_loss <= self.value_loss and self.perm_loss < 1.0:
            print("    → Selected: PERMUTATION (lower loss)")
            self.selected_system = 'permutation'
            return 'permutation'
        elif self.value_loss < 1.0:
            print("    → Selected: VALUE (lower loss)")
            self.selected_system = 'value'
            return 'value'
        else:
            # Both failed, pick the least bad
            if self.perm_loss <= self.value_loss:
                print("    → Selected: PERMUTATION (least bad)")
                self.selected_system = 'permutation'
                return 'permutation'
            else:
                print("    → Selected: VALUE (least bad)")
                self.selected_system = 'value'
                return 'value'

    def _compute_loss(self, system) -> float:
        """Compute average MSE loss on training examples."""
        total_loss = 0.0
        for inp, out in self.examples:
            pred = system.predict(inp)
            loss = sum((p - o) ** 2 for p, o in zip(pred, out)) / len(out)
            total_loss += loss
        return total_loss / len(self.examples) if self.examples else float('inf')

    def predict(self, input_seq: List[int]) -> List[int]:
        """Predict using the selected system."""
        if self.selected_system == 'permutation':
            return self.perm_system.predict(input_seq)
        elif self.selected_system == 'value':
            return self.value_system.predict(input_seq)
        else:
            raise ValueError("System not trained yet")

    def get_description(self) -> dict:
        """Get description of what was learned."""
        info = {
            'selected': self.selected_system,
            'perm_loss': self.perm_loss,
            'value_loss': self.value_loss
        }

        if self.selected_system == 'permutation' and self.perm_system:
            perm_matrix = self.perm_system.learner.log_alpha[:5, :5]
            hard_perm = F.softmax(perm_matrix, dim=1).argmax(dim=1).tolist()
            info['permutation'] = hard_perm
        elif self.selected_system == 'value' and self.value_system:
            info['value_structure'] = self.value_system.get_learned_structure()

        return info

    def reset(self):
        """Reset for new transform."""
        self.perm_system = None
        self.value_system = None
        self.examples = []
        self.selected_system = None
        self.perm_loss = float('inf')
        self.value_loss = float('inf')


# Test transforms (combination of positional and value)
ALL_TRANSFORMS = {
    # Positional (should use permutation)
    'identity': lambda x: x,
    'reverse': lambda x: list(reversed(x)),
    'swap_pairs': lambda x: [x[i+1] if i % 2 == 0 and i+1 < len(x) else x[i-1] if i % 2 == 1 else x[i] for i in range(len(x))],
    'rotate_left': lambda x: x[1:] + [x[0]],
    'rotate_right': lambda x: [x[-1]] + x[:-1],

    # Value (should use value modules)
    'increment': lambda x: [v + 1 for v in x],
    'double': lambda x: [v * 2 for v in x],
    'running_max': lambda x: [max(x[:i+1]) for i in range(len(x))],
    'running_sum': lambda x: [sum(x[:i+1]) for i in range(len(x))],
    'mirror_add': lambda x: [x[i] + x[len(x)-1-i] for i in range(len(x))],
    'mirror_max': lambda x: [max(x[i], x[len(x)-1-i]) for i in range(len(x))],
}


def test_unified_system():
    """Test the unified system on all transforms."""
    print("=" * 70)
    print("UNIFIED SEQUENCE SYSTEM TEST")
    print("=" * 70)
    print("\nTesting on 12 transforms (5 positional + 7 value)")
    print("-" * 70)

    results = {}

    for name, transform_fn in ALL_TRANSFORMS.items():
        print(f"\n{name}:")

        system = UnifiedSequenceSystem(max_len=10)

        # Train on 15 examples
        for _ in range(15):
            inp = random.sample(range(1, 10), 5)
            out = transform_fn(inp)
            system.add_example(inp, out)

        selected = system.train()

        # Test on 20 new examples
        correct = 0
        for _ in range(20):
            inp = random.sample(range(1, 10), 5)
            out = transform_fn(inp)
            pred = system.predict(inp)
            if pred == out:
                correct += 1

        accuracy = correct / 20
        results[name] = {
            'selected': selected,
            'accuracy': accuracy,
            'description': system.get_description()
        }

        print(f"  Accuracy: {correct}/20 ({accuracy*100:.0f}%)")
        print(f"  Selected: {selected}")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    positional = ['identity', 'reverse', 'swap_pairs', 'rotate_left', 'rotate_right']
    value = ['increment', 'double', 'running_max', 'running_sum', 'mirror_add', 'mirror_max']

    pos_acc = sum(results[t]['accuracy'] for t in positional) / len(positional)
    val_acc = sum(results[t]['accuracy'] for t in value) / len(value)
    overall = sum(r['accuracy'] for r in results.values()) / len(results)

    print(f"\nPositional transforms: {pos_acc*100:.0f}%")
    for t in positional:
        sel = results[t]['selected']
        acc = results[t]['accuracy']
        print(f"  {t}: {acc*100:.0f}% ({sel})")

    print(f"\nValue transforms: {val_acc*100:.0f}%")
    for t in value:
        sel = results[t]['selected']
        acc = results[t]['accuracy']
        print(f"  {t}: {acc*100:.0f}% ({sel})")

    print(f"\nOverall: {overall*100:.0f}%")

    # Check correct selection
    print("\n" + "-" * 70)
    print("System Selection Analysis:")
    print("-" * 70)

    for t in positional:
        sel = results[t]['selected']
        expected = 'permutation'
        match = '✓' if sel == expected else '✗'
        print(f"  {t}: {sel} (expected {expected}) {match}")

    for t in value:
        sel = results[t]['selected']
        # Value transforms might use either if they can be expressed as permutation
        # But increment, running_max, etc. should be value
        if t in ['increment', 'running_max', 'running_sum', 'mirror_add']:
            expected = 'value'
        else:
            expected = 'either'
        match = '✓' if sel == expected or expected == 'either' else '?'
        print(f"  {t}: {sel} (expected {expected}) {match}")

    print("\n" + "=" * 70)
    if overall >= 0.9:
        print("SUCCESS: ≥90% overall accuracy!")
    else:
        print(f"Result: {overall*100:.0f}%")
    print("=" * 70)

    return results


if __name__ == '__main__':
    test_unified_system()
