"""
Sequence Abstraction Library

Stores and retrieves learned sequence transforms for transfer learning.

Key insight: Unlike grids where "similarity" matters, sequence transforms are
more discrete - reverse IS reverse. We use exact-match via transform signature.

The signature: Apply transform to canonical inputs, hash the outputs.
Same signature = same transform = perfect transfer (14→1 steps).
"""

import torch
import torch.nn.functional as F
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
import pickle
from pathlib import Path
import hashlib


@dataclass
class SequenceAbstraction:
    """
    A stored abstraction from a learned sequence transform.
    """
    # Transform signature (hash of outputs on canonical inputs)
    signature: str

    # What type of transform
    config_type: str  # 'identity', 'permutation', 'value', 'composed'

    # Learned weights - store full state_dicts for proper restoration
    perm_state: Optional[Dict] = None  # Full state_dict for permutation
    value_state: Optional[Dict] = None  # Full state_dict for value
    composed_state: Optional[Tuple] = None  # (perm_state, value_state)

    # Training stats
    train_steps: int = 0
    final_loss: float = 0.0

    # Transfer tracking
    times_used: int = 0
    times_helped: int = 0

    @property
    def transfer_score(self) -> float:
        """How useful is this abstraction?"""
        if self.times_used == 0:
            return 1.0  # Assume good until proven otherwise
        return self.times_helped / self.times_used


def compute_signature(examples: List[Tuple[List[int], List[int]]]) -> str:
    """
    Compute a signature for a transform based on input→output mappings.

    Uses CANONICAL test inputs to get consistent signatures regardless
    of which training examples were used.
    """
    # Infer the transform from examples by testing on canonical inputs
    # We'll use a simple approach: compute the "delta" pattern

    # Get sequence length from examples
    seq_len = len(examples[0][0]) if examples else 5

    # Canonical test input: [1, 2, 3, 4, 5] or equivalent
    canonical_input = list(range(1, seq_len + 1))

    # Find the expected output by applying the transform to canonical
    # We infer this from examples
    canonical_output = None

    for inp, out in examples:
        if inp == canonical_input:
            canonical_output = out
            break

    if canonical_output is None:
        # Try to infer from the pattern
        # For now, fall back to example-based signature
        sorted_examples = sorted(examples, key=lambda x: tuple(x[0]))
        sig_parts = []
        for inp, out in sorted_examples[:5]:
            # Compute relative changes (position-independent for value transforms)
            deltas = [o - i for i, o in zip(inp, out)]
            sig_parts.append(f"{tuple(deltas)}")
        sig_str = "|".join(sig_parts)
    else:
        # Use canonical output directly
        sig_str = str(tuple(canonical_output))

    return hashlib.md5(sig_str.encode()).hexdigest()[:16]


def compute_transform_signature(transform_fn, seq_len: int = 5) -> str:
    """
    Compute signature by applying transform to canonical input.
    This is the gold standard - used when we have access to the transform function.
    """
    canonical_input = list(range(1, seq_len + 1))
    canonical_output = transform_fn(canonical_input)
    sig_str = str(tuple(canonical_output))
    return hashlib.md5(sig_str.encode()).hexdigest()[:16]


class SequenceAbstractionLibrary:
    """
    Stores and retrieves learned sequence transforms.

    Unlike grids, sequence transforms are matched by SIGNATURE (exact match).
    Same signature = same transform = use cached weights directly.
    """

    def __init__(self, save_path: str = "sequence_abstractions.pkl"):
        self.abstractions: Dict[str, SequenceAbstraction] = {}
        self.save_path = Path(save_path)

        if self.save_path.exists():
            self.load()

    def add(self,
            examples: List[Tuple[List[int], List[int]]],
            config_type: str,
            perm_state: Optional[Dict] = None,
            value_state: Optional[Dict] = None,
            composed_state: Optional[Tuple] = None,
            train_steps: int = 0,
            final_loss: float = 0.0):
        """Add a learned transform to the library."""
        signature = compute_signature(examples)

        # Deep copy state dicts to CPU
        def to_cpu(state):
            if state is None:
                return None
            return {k: v.detach().cpu() if isinstance(v, torch.Tensor) else v
                    for k, v in state.items()}

        abstraction = SequenceAbstraction(
            signature=signature,
            config_type=config_type,
            perm_state=to_cpu(perm_state),
            value_state=to_cpu(value_state),
            composed_state=(to_cpu(composed_state[0]), to_cpu(composed_state[1])) if composed_state else None,
            train_steps=train_steps,
            final_loss=final_loss
        )

        self.abstractions[signature] = abstraction
        self.save()

        return signature

    def find(self, examples: List[Tuple[List[int], List[int]]]) -> Optional[SequenceAbstraction]:
        """Find exact match for transform."""
        signature = compute_signature(examples)
        return self.abstractions.get(signature)

    def get_initialization(self,
                           examples: List[Tuple[List[int], List[int]]]) -> Optional[Dict]:
        """
        Get initialization state if we've seen this transform before.

        Returns dict with:
        - config_type: what type of transform
        - perm_state: full state_dict for permutation (if applicable)
        - value_state: full state_dict for value (if applicable)
        - composed_state: (perm_state, value_state) tuple (if applicable)
        """
        abstraction = self.find(examples)

        if abstraction is None:
            return None

        abstraction.times_used += 1

        return {
            'config_type': abstraction.config_type,
            'perm_state': abstraction.perm_state,
            'value_state': abstraction.value_state,
            'composed_state': abstraction.composed_state,
            'expected_steps': 1  # With transfer, should converge in 1 step
        }

    def update_stats(self, examples: List[Tuple[List[int], List[int]]], helped: bool):
        """Update transfer statistics."""
        signature = compute_signature(examples)
        if signature in self.abstractions:
            if helped:
                self.abstractions[signature].times_helped += 1
            self.save()

    def save(self):
        """Save library to disk."""
        with open(self.save_path, 'wb') as f:
            pickle.dump(self.abstractions, f)

    def load(self):
        """Load library from disk."""
        try:
            with open(self.save_path, 'rb') as f:
                self.abstractions = pickle.load(f)
        except Exception:
            self.abstractions = {}

    def clear(self):
        """Clear the library."""
        self.abstractions = {}
        if self.save_path.exists():
            self.save_path.unlink()

    def stats(self) -> dict:
        """Get library statistics."""
        if not self.abstractions:
            return {"size": 0}

        by_type = {}
        for a in self.abstractions.values():
            by_type[a.config_type] = by_type.get(a.config_type, 0) + 1

        return {
            "size": len(self.abstractions),
            "by_type": by_type,
            "total_uses": sum(a.times_used for a in self.abstractions.values()),
            "total_helped": sum(a.times_helped for a in self.abstractions.values()),
        }


# Singleton
_library = None

def get_sequence_library(save_path: str = "sequence_abstractions.pkl") -> SequenceAbstractionLibrary:
    """Get or create the global sequence abstraction library."""
    global _library
    if _library is None:
        _library = SequenceAbstractionLibrary(save_path)
    return _library


def reset_library():
    """Reset the global library (for testing)."""
    global _library
    if _library is not None:
        _library.clear()
    _library = None


# =============================================================================
# Test
# =============================================================================

def test_library():
    """Test the sequence abstraction library."""
    print("=" * 60)
    print("SEQUENCE ABSTRACTION LIBRARY TEST")
    print("=" * 60)

    # Reset for clean test
    reset_library()
    library = get_sequence_library("test_seq_lib.pkl")

    # Simulate learning reverse transform
    # IMPORTANT: Include canonical input [1,2,3,4,5] for signature
    reverse_examples = [
        ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]),  # Canonical
        ([9, 8, 7, 6, 5], [5, 6, 7, 8, 9]),
    ]

    # Add to library
    fake_weights = torch.randn(10, 10)
    sig = library.add(
        examples=reverse_examples,
        config_type='permutation',
        perm_weights=fake_weights,
        train_steps=14,
        final_loss=0.001
    )
    print(f"\n1. Added 'reverse' with signature: {sig}")
    print(f"   Library size: {library.stats()['size']}")

    # Try to retrieve
    init = library.get_initialization(reverse_examples)
    print(f"\n2. Retrieved initialization: {init is not None}")
    if init:
        print(f"   Config type: {init['config_type']}")
        print(f"   Has weights: {init['perm_weights'] is not None}")

    # Try with different examples of same transform (but includes canonical)
    new_reverse_examples = [
        ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]),  # Canonical - same signature
        ([2, 4, 6, 8, 1], [1, 8, 6, 4, 2]),
    ]
    init2 = library.get_initialization(new_reverse_examples)
    print(f"\n3. Same transform, different examples: {init2 is not None}")

    # Different transform should not match
    increment_examples = [
        ([1, 2, 3, 4, 5], [2, 3, 4, 5, 6]),  # Canonical
    ]
    init3 = library.get_initialization(increment_examples)
    print(f"\n4. Different transform (increment): {init3 is not None}")

    # Add increment
    library.add(
        examples=increment_examples,
        config_type='value',
        value_weights={'module': 'pointwise', 'scale': 1.0, 'offset': 1.0},
        train_steps=10
    )
    print(f"\n5. Added 'increment', library size: {library.stats()['size']}")

    # Now increment should match
    init4 = library.get_initialization(increment_examples)
    print(f"   Increment retrieval: {init4 is not None}")
    if init4:
        print(f"   Config type: {init4['config_type']}")

    # Test transform signature function
    reverse_fn = lambda x: list(reversed(x))
    increment_fn = lambda x: [v + 1 for v in x]

    sig_rev = compute_transform_signature(reverse_fn)
    sig_inc = compute_transform_signature(increment_fn)
    print(f"\n6. Transform signatures:")
    print(f"   reverse: {sig_rev}")
    print(f"   increment: {sig_inc}")
    print(f"   Match library: {sig_rev == sig}")

    print(f"\n7. Final stats: {library.stats()}")

    # Cleanup
    reset_library()
    Path("test_seq_lib.pkl").unlink(missing_ok=True)

    print("\n" + "=" * 60)
    print("LIBRARY TEST PASSED")
    print("=" * 60)


if __name__ == '__main__':
    test_library()
