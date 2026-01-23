"""
Composed Sequence Transform System

Uses EXPLICIT SEARCH over configurations (not soft differentiable pipeline).

Configurations:
1. Identity (no transform)
2. Permutation only
3. Value only
4. Permutation → Value (composed)

MDL objective: pick simplest configuration that fits.

Now with ABSTRACTION LIBRARY integration for transfer learning.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Tuple, Optional
import random

from permutation_learner import SequencePermutationSystem
from value_modules import ValueTransformSystem
from sequence_abstraction_library import get_sequence_library, compute_signature


class ComposedTransformSystem:
    """
    Learns composed transforms via explicit search.

    Strategy:
    1. Check abstraction library for cached solution
    2. If not found, train each configuration independently
    3. Measure loss + description_length for each
    4. Select configuration with best MDL score
    5. Save to library for future transfer
    """

    def __init__(self, max_len: int = 10, use_library: bool = True):
        self.max_len = max_len
        self.use_library = use_library
        self.examples: List[Tuple[List[int], List[int]]] = []

        # Systems for each configuration
        self.perm_system = None
        self.value_system = None
        self.composed_system = None  # Will hold (perm, value) pair

        # Results
        self.selected = None
        self.scores = {}

        # Transfer tracking
        self.train_steps = 0
        self.used_transfer = False

    def add_example(self, input_seq: List[int], output_seq: List[int]):
        """Add training example."""
        self.examples.append((input_seq, output_seq))

    def _compute_loss(self, predictions: List[List[int]]) -> float:
        """Compute average MSE loss."""
        total = 0.0
        for pred, (_, target) in zip(predictions, self.examples):
            loss = sum((p - t) ** 2 for p, t in zip(pred, target)) / len(target)
            total += loss
        return total / len(self.examples)

    def _train_identity(self) -> Tuple[float, float]:
        """Test if identity works."""
        preds = [inp for inp, _ in self.examples]
        loss = self._compute_loss(preds)
        dl = 0.0  # Identity has zero description length
        return loss, dl

    def _train_permutation(self) -> Tuple[float, float, 'SequencePermutationSystem']:
        """Train permutation-only."""
        system = SequencePermutationSystem(self.max_len)
        for inp, out in self.examples:
            system.add_example(inp, out)
        system.train_batch(max_steps=300)

        preds = [system.predict(inp) for inp, _ in self.examples]
        loss = self._compute_loss(preds)
        dl = 1.0  # Base cost for using permutation
        return loss, dl, system

    def _train_value(self) -> Tuple[float, float, 'ValueTransformSystem']:
        """Train value-only."""
        system = ValueTransformSystem(self.max_len)
        for inp, out in self.examples:
            system.add_example(inp, out)
        system.train_batch(max_steps=300)

        preds = [system.predict(inp) for inp, _ in self.examples]
        loss = self._compute_loss(preds)
        dl = 1.0  # Base cost for using value
        return loss, dl, system

    def _train_composed(self) -> Tuple[float, float, Tuple]:
        """Train permutation → value composed."""
        # First learn permutation on input→intermediate
        # We need to figure out the intermediate representation
        #
        # Key insight: for reverse_then_increment, the intermediate is reverse(input)
        # We don't know this, but we can try:
        # 1. Train permutation on input→output (won't fit if value is needed)
        # 2. Apply learned perm to inputs
        # 3. Train value on permuted→output

        perm_sys = SequencePermutationSystem(self.max_len)
        for inp, out in self.examples:
            perm_sys.add_example(inp, out)
        perm_sys.train_batch(max_steps=300)  # Quick training

        # Get intermediate representations (permuted inputs)
        intermediates = [perm_sys.predict(inp) for inp, _ in self.examples]

        # Train value on intermediate→output
        value_sys = ValueTransformSystem(self.max_len)
        for inter, (_, out) in zip(intermediates, self.examples):
            value_sys.add_example(inter, out)
        value_sys.train_batch(max_steps=300)

        # Compute predictions: input → perm → value → output
        preds = []
        for inp, _ in self.examples:
            inter = perm_sys.predict(inp)
            pred = value_sys.predict(inter)
            preds.append(pred)

        loss = self._compute_loss(preds)
        dl = 2.0  # Cost for using both stages
        return loss, dl, (perm_sys, value_sys)

    def train(self, threshold: float = 0.01) -> str:
        """Train and select best configuration."""
        if not self.examples:
            return 'none'

        # Check library for cached solution
        if self.use_library:
            library = get_sequence_library()
            init = library.get_initialization(self.examples)

            if init is not None:
                # We have a cached solution! Use it.
                self.used_transfer = True
                self.train_steps = 1  # Transfer = 1 step
                self.selected = init['config_type']

                # Reconstruct systems from cached state_dicts
                if self.selected == 'permutation' and init['perm_state'] is not None:
                    self.perm_system = SequencePermutationSystem(self.max_len)
                    self.perm_system.learner.load_state_dict(init['perm_state'])
                elif self.selected == 'value' and init['value_state'] is not None:
                    self.value_system = ValueTransformSystem(self.max_len)
                    self.value_system.model.load_state_dict(init['value_state'])
                elif self.selected == 'composed' and init['composed_state'] is not None:
                    perm_state, val_state = init['composed_state']
                    perm_sys = SequencePermutationSystem(self.max_len)
                    perm_sys.learner.load_state_dict(perm_state)
                    value_sys = ValueTransformSystem(self.max_len)
                    value_sys.model.load_state_dict(val_state)
                    self.composed_system = (perm_sys, value_sys)

                library.update_stats(self.examples, helped=True)
                return self.selected

        # No cached solution - train from scratch
        self.train_steps = 0

        # Try all configurations
        id_loss, id_dl = self._train_identity()
        self.scores['identity'] = {'loss': id_loss, 'dl': id_dl, 'mdl': id_loss + 0.1 * id_dl}

        perm_loss, perm_dl, perm_sys = self._train_permutation()
        self.scores['permutation'] = {'loss': perm_loss, 'dl': perm_dl, 'mdl': perm_loss + 0.1 * perm_dl}
        self.perm_system = perm_sys
        self.train_steps += 300

        value_loss, value_dl, value_sys = self._train_value()
        self.scores['value'] = {'loss': value_loss, 'dl': value_dl, 'mdl': value_loss + 0.1 * value_dl}
        self.value_system = value_sys
        self.train_steps += 300

        comp_loss, comp_dl, comp_sys = self._train_composed()
        self.scores['composed'] = {'loss': comp_loss, 'dl': comp_dl, 'mdl': comp_loss + 0.1 * comp_dl}
        self.composed_system = comp_sys
        self.train_steps += 600  # 300 + 300 for composed

        # Select best by MDL (loss + description_length)
        best = min(self.scores.keys(), key=lambda k: self.scores[k]['mdl'])

        # But only if it fits well enough
        if self.scores[best]['loss'] > 1.0:
            # None fit well, pick least bad
            best = min(self.scores.keys(), key=lambda k: self.scores[k]['loss'])

        self.selected = best

        # Save to library for future transfer
        if self.use_library and self.scores[best]['loss'] < 0.01:
            library = get_sequence_library()
            perm_state = None
            value_state = None
            composed_state = None

            if best == 'permutation' and self.perm_system:
                perm_state = self.perm_system.learner.state_dict()
            elif best == 'value' and self.value_system:
                value_state = self.value_system.model.state_dict()
            elif best == 'composed' and self.composed_system:
                perm_sys, val_sys = self.composed_system
                composed_state = (
                    perm_sys.learner.state_dict(),
                    val_sys.model.state_dict()
                )

            library.add(
                examples=self.examples,
                config_type=best,
                perm_state=perm_state,
                value_state=value_state,
                composed_state=composed_state,
                train_steps=self.train_steps,
                final_loss=self.scores[best]['loss']
            )

        return best

    def predict(self, input_seq: List[int]) -> List[int]:
        """Predict using selected configuration."""
        if self.selected == 'identity':
            return input_seq.copy()
        elif self.selected == 'permutation':
            return self.perm_system.predict(input_seq)
        elif self.selected == 'value':
            return self.value_system.predict(input_seq)
        elif self.selected == 'composed':
            perm_sys, value_sys = self.composed_system
            inter = perm_sys.predict(input_seq)
            return value_sys.predict(inter)
        else:
            raise ValueError(f"Unknown configuration: {self.selected}")

    def get_description(self) -> dict:
        """Return what was learned."""
        info = {
            'selected': self.selected,
            'scores': self.scores
        }

        if self.selected == 'permutation' and self.perm_system:
            perm = F.softmax(self.perm_system.learner.log_alpha[:5, :5], dim=1)
            info['permutation'] = perm.argmax(dim=1).tolist()
        elif self.selected == 'value' and self.value_system:
            info['value_module'] = self.value_system.get_learned_structure()
        elif self.selected == 'composed' and self.composed_system:
            perm_sys, value_sys = self.composed_system
            perm = F.softmax(perm_sys.learner.log_alpha[:5, :5], dim=1)
            info['permutation'] = perm.argmax(dim=1).tolist()
            info['value_module'] = value_sys.get_learned_structure()

        return info

    def reset(self):
        """Reset for new transform."""
        self.examples = []
        self.perm_system = None
        self.value_system = None
        self.composed_system = None
        self.selected = None
        self.scores = {}


# All transforms including composed ones
ALL_TRANSFORMS = {
    # Single positional
    'identity': lambda x: x,
    'reverse': lambda x: list(reversed(x)),
    'swap_pairs': lambda x: [x[i+1] if i % 2 == 0 and i+1 < len(x) else x[i-1] if i % 2 == 1 else x[i] for i in range(len(x))],
    'rotate_left': lambda x: x[1:] + [x[0]],
    'rotate_right': lambda x: [x[-1]] + x[:-1],

    # Single value
    'increment': lambda x: [v + 1 for v in x],
    'double': lambda x: [v * 2 for v in x],
    'running_max': lambda x: [max(x[:i+1]) for i in range(len(x))],
    'running_sum': lambda x: [sum(x[:i+1]) for i in range(len(x))],
    'mirror_add': lambda x: [x[i] + x[len(x)-1-i] for i in range(len(x))],

    # COMPOSED: positional → value
    'reverse_then_increment': lambda x: [v + 1 for v in reversed(x)],
    'reverse_then_double': lambda x: [v * 2 for v in reversed(x)],
    'rotate_then_increment': lambda x: [v + 1 for v in (x[1:] + [x[0]])],
}


def test_composed_system():
    """Test the composed transform system."""
    print("=" * 70)
    print("COMPOSED TRANSFORM SYSTEM TEST")
    print("=" * 70)
    print()

    results = {}

    for name, transform_fn in ALL_TRANSFORMS.items():
        print(f"{name}:", end=" ", flush=True)

        system = ComposedTransformSystem(max_len=10)

        # Train on 20 examples
        for _ in range(20):
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
        results[name] = {'selected': selected, 'accuracy': accuracy}

        loss = system.scores[selected]['loss']
        print(f"{correct}/20 ({accuracy*100:.0f}%) [{selected}] loss={loss:.3f}")

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    single_pos = ['identity', 'reverse', 'swap_pairs', 'rotate_left', 'rotate_right']
    single_val = ['increment', 'double', 'running_max', 'running_sum', 'mirror_add']
    composed = ['reverse_then_increment', 'reverse_then_double', 'rotate_then_increment']

    pos_acc = sum(results[t]['accuracy'] for t in single_pos) / len(single_pos)
    val_acc = sum(results[t]['accuracy'] for t in single_val) / len(single_val)
    comp_acc = sum(results[t]['accuracy'] for t in composed) / len(composed)
    overall = sum(r['accuracy'] for r in results.values()) / len(results)

    print(f"\nSingle Positional: {pos_acc*100:.0f}%")
    print(f"Single Value: {val_acc*100:.0f}%")
    print(f"COMPOSED: {comp_acc*100:.0f}%")
    print(f"\nOverall: {overall*100:.0f}%")

    print("\n" + "=" * 70)
    if overall >= 0.9:
        print("SUCCESS: ≥90% on ALL transforms including composed!")
    else:
        print(f"Result: {overall*100:.0f}%")
        print("\nFailing transforms:")
        for name, r in results.items():
            if r['accuracy'] < 0.9:
                print(f"  {name}: {r['accuracy']*100:.0f}% [{r['selected']}]")
    print("=" * 70)

    return results


def test_transfer_learning():
    """Test transfer learning with abstraction library."""
    from sequence_abstraction_library import reset_library, get_sequence_library

    print("=" * 70)
    print("TRANSFER LEARNING TEST")
    print("=" * 70)

    # Reset library for clean test
    reset_library()

    # Test transforms
    test_transforms = ['reverse', 'increment', 'reverse_then_increment']

    print("\n=== COLD START (no library) ===")
    cold_steps = {}
    for name in test_transforms:
        fn = ALL_TRANSFORMS[name]
        system = ComposedTransformSystem(max_len=10, use_library=True)

        # Include canonical input for consistent signature
        system.add_example([1, 2, 3, 4, 5], fn([1, 2, 3, 4, 5]))
        for _ in range(19):
            inp = random.sample(range(1, 10), 5)
            system.add_example(inp, fn(inp))

        system.train()
        cold_steps[name] = system.train_steps

        # Verify accuracy
        correct = sum(1 for _ in range(10)
                     for inp in [random.sample(range(1, 10), 5)]
                     if system.predict(inp) == fn(inp))

        print(f"  {name}: {system.train_steps} steps [{system.selected}] "
              f"(accuracy: {correct}/10, transfer: {system.used_transfer})")

    print(f"\nLibrary size: {get_sequence_library().stats()['size']}")

    print("\n=== WARM START (with library) ===")
    warm_steps = {}
    for name in test_transforms:
        fn = ALL_TRANSFORMS[name]
        system = ComposedTransformSystem(max_len=10, use_library=True)

        # Same canonical input - should match signature
        system.add_example([1, 2, 3, 4, 5], fn([1, 2, 3, 4, 5]))
        for _ in range(19):
            inp = random.sample(range(1, 10), 5)
            system.add_example(inp, fn(inp))

        system.train()
        warm_steps[name] = system.train_steps

        # Verify accuracy
        correct = sum(1 for _ in range(10)
                     for inp in [random.sample(range(1, 10), 5)]
                     if system.predict(inp) == fn(inp))

        print(f"  {name}: {system.train_steps} steps [{system.selected}] "
              f"(accuracy: {correct}/10, transfer: {system.used_transfer})")

    print("\n=== TRANSFER SPEEDUP ===")
    for name in test_transforms:
        speedup = cold_steps[name] / warm_steps[name] if warm_steps[name] > 0 else float('inf')
        print(f"  {name}: {cold_steps[name]} → {warm_steps[name]} steps ({speedup:.0f}× speedup)")

    # Cleanup
    reset_library()

    print("\n" + "=" * 70)
    print("TRANSFER TEST COMPLETE")
    print("=" * 70)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'transfer':
        test_transfer_learning()
    else:
        test_composed_system()
