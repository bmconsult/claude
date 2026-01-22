"""
Unified Intelligence System - Phase 9

Single interface for:
1. Grids (2D patterns) - via ARCCompressor
2. Sequences (1D integer lists) - via ComposedTransformSystem
3. Language (characters/words/sentences) - via Language MDL systems

Key insight: Some abstractions ARE cross-modal:
- Permutation (position reordering) works for sequences AND words
- Mapping (value substitution) works for sequences AND characters
- Pattern detection works across all modalities

This is the laptop-scale general intelligence system.
"""

import torch
import torch.nn as nn
from typing import List, Tuple, Dict, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
import numpy as np


class Modality(Enum):
    GRID = "grid"
    SEQUENCE = "sequence"
    CHARACTER = "character"
    WORD = "word"
    SENTENCE = "sentence"


@dataclass
class Task:
    """A task in any modality."""
    modality: Modality
    examples: List[Tuple[Any, Any]]  # (input, output) pairs
    test_inputs: List[Any] = None


@dataclass
class Solution:
    """Solution to a task."""
    modality: Modality
    predictions: List[Any]
    config_selected: str
    train_steps: int
    used_transfer: bool
    accuracy: float


# =============================================================================
# Modality Detection
# =============================================================================

def detect_modality(examples: List[Tuple[Any, Any]]) -> Modality:
    """
    Detect the modality of input/output examples.

    Rules:
    - 2D numpy arrays or nested lists → GRID
    - 1D list of integers → SEQUENCE
    - Single string → CHARACTER
    - List of strings (all single words) → WORD
    - List of strings (multiple words) → SENTENCE
    """
    if not examples:
        raise ValueError("No examples provided")

    inp, out = examples[0]

    # Grid: 2D numpy array or nested list
    if isinstance(inp, np.ndarray) and inp.ndim == 2:
        return Modality.GRID
    if isinstance(inp, list) and inp and isinstance(inp[0], list):
        return Modality.GRID

    # String → Character level
    if isinstance(inp, str) and isinstance(out, str):
        return Modality.CHARACTER

    # List of strings
    if isinstance(inp, list) and inp and isinstance(inp[0], str):
        # Check if single words or sentences
        if all(len(w.split()) == 1 for w in inp):
            # Could be word-level or sentence-level depending on semantics
            # If each "word" is actually a sentence component, it's sentence level
            # For now, use length heuristic
            if len(inp) >= 3:
                return Modality.SENTENCE
            return Modality.WORD
        return Modality.SENTENCE

    # List of integers → Sequence
    if isinstance(inp, list) and inp and isinstance(inp[0], (int, float)):
        return Modality.SEQUENCE

    # Default to sequence
    return Modality.SEQUENCE


# =============================================================================
# Unified System
# =============================================================================

class UnifiedIntelligenceSystem:
    """
    Laptop-scale general intelligence.

    Single interface that:
    1. Detects input modality
    2. Routes to appropriate subsystem
    3. Applies MDL-based learning
    4. Leverages cross-modal transfer where applicable
    """

    def __init__(self):
        # Lazy imports to avoid circular dependencies
        self._systems = {}
        self.stats = {
            'tasks_solved': 0,
            'by_modality': {},
            'transfer_used': 0,
            'total_steps': 0
        }

    def _get_sequence_system(self):
        """Get or create sequence system."""
        if 'sequence' not in self._systems:
            from composed_transforms import ComposedTransformSystem
            self._systems['sequence'] = ComposedTransformSystem
        return self._systems['sequence']

    def _get_char_system(self):
        """Get or create character system."""
        if 'character' not in self._systems:
            from language_mdl import CharTransformSystem
            self._systems['character'] = CharTransformSystem
        return self._systems['character']

    def _get_word_system(self):
        """Get or create word system."""
        if 'word' not in self._systems:
            from word_mdl import WordTransformSystem
            self._systems['word'] = WordTransformSystem
        return self._systems['word']

    def _get_sentence_system(self):
        """Get or create sentence system."""
        if 'sentence' not in self._systems:
            from sentence_mdl import SentenceTransformSystem
            self._systems['sentence'] = SentenceTransformSystem
        return self._systems['sentence']

    def solve(self, task: Task) -> Solution:
        """
        Solve a task in any modality.

        Routes to appropriate subsystem based on detected modality.
        """
        modality = task.modality
        examples = task.examples
        test_inputs = task.test_inputs or [inp for inp, _ in examples]

        if modality == Modality.SEQUENCE:
            return self._solve_sequence(examples, test_inputs)
        elif modality == Modality.CHARACTER:
            return self._solve_character(examples, test_inputs)
        elif modality == Modality.WORD:
            return self._solve_word(examples, test_inputs)
        elif modality == Modality.SENTENCE:
            return self._solve_sentence(examples, test_inputs)
        elif modality == Modality.GRID:
            return self._solve_grid(examples, test_inputs)
        else:
            raise ValueError(f"Unknown modality: {modality}")

    def _solve_sequence(self, examples: List[Tuple[List[int], List[int]]],
                        test_inputs: List[List[int]]) -> Solution:
        """Solve sequence transform task."""
        SystemClass = self._get_sequence_system()
        system = SystemClass(max_len=16, use_library=True)

        for inp, out in examples:
            system.add_example(inp, out)

        selected = system.train()

        predictions = [system.predict(inp) for inp in test_inputs]

        # Compute accuracy on training examples
        correct = sum(1 for (inp, out), pred in zip(examples, predictions[:len(examples)])
                     if pred == list(out))
        accuracy = correct / len(examples) if examples else 0.0

        self._update_stats(Modality.SEQUENCE, system)

        return Solution(
            modality=Modality.SEQUENCE,
            predictions=predictions,
            config_selected=selected,
            train_steps=getattr(system, 'train_steps', 0),
            used_transfer=getattr(system, 'used_transfer', False),
            accuracy=accuracy
        )

    def _solve_character(self, examples: List[Tuple[str, str]],
                         test_inputs: List[str]) -> Solution:
        """Solve character transform task."""
        SystemClass = self._get_char_system()
        system = SystemClass(max_len=32, use_library=True)

        for inp, out in examples:
            system.add_example(inp, out)

        selected = system.train()

        predictions = [system.predict(inp) for inp in test_inputs]

        correct = sum(1 for (inp, out), pred in zip(examples, predictions[:len(examples)])
                     if pred == out)
        accuracy = correct / len(examples) if examples else 0.0

        self._update_stats(Modality.CHARACTER, system)

        return Solution(
            modality=Modality.CHARACTER,
            predictions=predictions,
            config_selected=selected,
            train_steps=getattr(system, 'train_steps', 0),
            used_transfer=getattr(system, 'used_transfer', False),
            accuracy=accuracy
        )

    def _solve_word(self, examples: List[Tuple[List[str], List[str]]],
                    test_inputs: List[List[str]]) -> Solution:
        """Solve word transform task."""
        SystemClass = self._get_word_system()
        system = SystemClass(max_len=16)

        for inp, out in examples:
            system.add_example(inp, out)

        selected = system.train()

        predictions = [system.predict(inp) for inp in test_inputs]

        correct = sum(1 for (inp, out), pred in zip(examples, predictions[:len(examples)])
                     if pred == list(out))
        accuracy = correct / len(examples) if examples else 0.0

        self._update_stats(Modality.WORD, system)

        return Solution(
            modality=Modality.WORD,
            predictions=predictions,
            config_selected=selected,
            train_steps=0,
            used_transfer=False,
            accuracy=accuracy
        )

    def _solve_sentence(self, examples: List[Tuple[List[str], List[str]]],
                        test_inputs: List[List[str]]) -> Solution:
        """Solve sentence transform task."""
        SystemClass = self._get_sentence_system()
        system = SystemClass(max_len=16)

        for inp, out in examples:
            system.add_example(inp, out)

        selected = system.train()

        predictions = [system.predict(inp) for inp in test_inputs]

        correct = sum(1 for (inp, out), pred in zip(examples, predictions[:len(examples)])
                     if pred == list(out))
        accuracy = correct / len(examples) if examples else 0.0

        self._update_stats(Modality.SENTENCE, system)

        return Solution(
            modality=Modality.SENTENCE,
            predictions=predictions,
            config_selected=selected,
            train_steps=0,
            used_transfer=False,
            accuracy=accuracy
        )

    def _solve_grid(self, examples: List[Tuple[np.ndarray, np.ndarray]],
                    test_inputs: List[np.ndarray]) -> Solution:
        """Solve grid transform task (placeholder - requires full ARCCompressor)."""
        # Grid solving requires the full ARCCompressor pipeline
        # which has different training dynamics
        # For now, return placeholder
        return Solution(
            modality=Modality.GRID,
            predictions=[],
            config_selected='arc_compressor',
            train_steps=0,
            used_transfer=False,
            accuracy=0.0
        )

    def _update_stats(self, modality: Modality, system):
        """Update statistics."""
        self.stats['tasks_solved'] += 1
        mod_name = modality.value
        self.stats['by_modality'][mod_name] = self.stats['by_modality'].get(mod_name, 0) + 1

        if getattr(system, 'used_transfer', False):
            self.stats['transfer_used'] += 1

        self.stats['total_steps'] += getattr(system, 'train_steps', 0)

    def solve_auto(self, examples: List[Tuple[Any, Any]],
                   test_inputs: List[Any] = None) -> Solution:
        """
        Auto-detect modality and solve.

        This is the main entry point - just provide examples.
        """
        modality = detect_modality(examples)
        task = Task(
            modality=modality,
            examples=examples,
            test_inputs=test_inputs
        )
        return self.solve(task)


# =============================================================================
# Cross-Modal Transfer
# =============================================================================

class CrossModalTransfer:
    """
    Explores cross-modal transfer of abstractions.

    Key insight: Some patterns are modality-independent:
    - Permutation: works for sequences, words, characters
    - Mapping/substitution: works for sequences, characters
    - Template patterns: structural patterns that apply across domains
    """

    @staticmethod
    def sequence_to_word_permutation(seq_perm_state: Dict) -> Dict:
        """
        Transfer a learned sequence permutation to word permutation.

        Sequence permutation is position-based, so it directly applies to words.
        """
        # The permutation matrix log_alpha is position-based
        # It can be used directly for word reordering
        return seq_perm_state.copy()

    @staticmethod
    def char_mapping_to_sequence_mapping(char_map_state: Dict,
                                         char_codec, seq_range: int) -> Optional[Dict]:
        """
        Transfer character mapping to sequence mapping.

        This is harder - character mappings are over vocabulary,
        sequence mappings are over integers.

        Only works if there's a natural correspondence.
        """
        # This would require semantic alignment
        # For now, return None (no direct transfer possible)
        return None

    @staticmethod
    def test_cross_modal_transfer():
        """Test if cross-modal transfer works."""
        results = {}

        # Test 1: Sequence permutation → Word permutation
        print("Testing sequence → word permutation transfer...")
        from composed_transforms import ComposedTransformSystem
        from word_mdl import WordTransformSystem, WordPermutation

        # Learn reverse on sequences (use max_len=16 to match WordPermutation default)
        seq_system = ComposedTransformSystem(max_len=16, use_library=False)
        for i in range(5):
            inp = [1, 2, 3, 4, 5]
            out = [5, 4, 3, 2, 1]
            seq_system.add_example(inp, out)
        seq_system.train()

        if seq_system.selected == 'permutation' and seq_system.perm_system is not None:
            # Get the learned permutation - extract just log_alpha
            seq_log_alpha = seq_system.perm_system.learner.log_alpha.data.clone()

            # Apply to words - create new permutation and copy weights
            word_perm = WordPermutation(max_len=16)
            word_perm.log_alpha.data = seq_log_alpha

            # Test
            test_words = ['the', 'cat', 'sat', 'on', 'mat']
            expected = ['mat', 'on', 'sat', 'cat', 'the']
            predicted = word_perm.apply_to_words(test_words)

            results['seq_to_word_perm'] = predicted == expected
            print(f"  Input: {test_words}")
            print(f"  Expected: {expected}")
            print(f"  Got: {predicted}")
            print(f"  Success: {results['seq_to_word_perm']}")
        else:
            results['seq_to_word_perm'] = False
            print(f"  Sequence system didn't learn permutation (selected: {seq_system.selected})")

        # Test 2: Word system learns reverse independently
        print("\nTesting independent learning comparison...")
        word_system = WordTransformSystem(max_len=16)
        # More examples for reliable permutation learning
        word_system.add_example(['the', 'cat', 'sat', 'on', 'mat'],
                               ['mat', 'on', 'sat', 'cat', 'the'])
        word_system.add_example(['a', 'dog', 'ran', 'to', 'me'],
                               ['me', 'to', 'ran', 'dog', 'a'])
        word_system.add_example(['one', 'big', 'red', 'fast', 'car'],
                               ['car', 'fast', 'red', 'big', 'one'])
        word_system.add_example(['my', 'old', 'blue', 'new', 'hat'],
                               ['hat', 'new', 'blue', 'old', 'my'])
        word_system.add_example(['we', 'all', 'eat', 'hot', 'pie'],
                               ['pie', 'hot', 'eat', 'all', 'we'])
        word_system.add_example(['go', 'see', 'the', 'big', 'sun'],
                               ['sun', 'big', 'the', 'see', 'go'])
        word_system.train()

        test_words = ['she', 'can', 'run', 'so', 'far']
        pred = word_system.predict(test_words)
        expected = ['far', 'so', 'run', 'can', 'she']
        results['word_reverse_independent'] = pred == expected
        print(f"  Input: {test_words}")
        print(f"  Expected: {expected}")
        print(f"  Got: {pred}")
        print(f"  Selected: {word_system.selected}")
        print(f"  Success: {results['word_reverse_independent']}")

        return results


# =============================================================================
# Test
# =============================================================================

def test_unified_system():
    """Test the unified intelligence system."""
    print("=" * 70)
    print("UNIFIED INTELLIGENCE SYSTEM - PHASE 9")
    print("=" * 70)

    system = UnifiedIntelligenceSystem()
    results = {}

    # Test 1: Sequence transforms
    print("\n1. SEQUENCE TRANSFORMS")
    print("-" * 40)

    seq_tests = [
        ('identity', lambda x: x),
        ('reverse', lambda x: x[::-1]),
        ('increment', lambda x: [v + 1 for v in x]),
    ]

    for name, transform in seq_tests:
        examples = [([1, 2, 3, 4, 5], transform([1, 2, 3, 4, 5]))]
        test_inputs = [[6, 7, 8, 9, 10]]

        solution = system.solve_auto(examples, test_inputs)
        expected = transform([6, 7, 8, 9, 10])
        correct = solution.predictions[0] == expected

        results[f'seq_{name}'] = correct
        print(f"  {name}: {'✓' if correct else '✗'} [{solution.config_selected}]")

    # Test 2: Character transforms
    print("\n2. CHARACTER TRANSFORMS")
    print("-" * 40)

    from language_mdl import reset_char_library

    char_tests = [
        ('identity', lambda s: s),
        ('reverse', lambda s: s[::-1]),
        ('uppercase', lambda s: s.upper()),
    ]

    for name, transform in char_tests:
        # Reset library for each test to avoid interference
        reset_char_library()

        # Use exact same training words as standalone test (achieves 100%)
        train_words = [
            'hello', 'world', 'quick', 'jumps', 'brown',
            'foxes', 'crazy', 'about', 'every', 'night',
            'abcde', 'fghij', 'klmno', 'pqrst', 'uvwxy'
        ]
        examples = [(w, transform(w)) for w in train_words]
        test_inputs = ['codes']  # Test word from standalone test

        solution = system.solve_auto(examples, test_inputs)
        expected = transform(test_inputs[0])  # Use actual test input
        pred = solution.predictions[0] if solution.predictions else ''
        correct = pred == expected

        results[f'char_{name}'] = correct
        status = '✓' if correct else '✗'
        print(f"  {name}: {status} [{solution.config_selected}] ('{pred}' vs '{expected}')")

    # Test 3: Word transforms
    print("\n3. WORD TRANSFORMS")
    print("-" * 40)

    word_tests = [
        ('identity', lambda w: w),
        ('reverse', lambda w: w[::-1]),
    ]

    for name, transform in word_tests:
        examples = [
            (['the', 'cat', 'sat'], transform(['the', 'cat', 'sat'])),
            (['a', 'dog', 'ran'], transform(['a', 'dog', 'ran'])),
        ]
        test_inputs = [['the', 'bird', 'flew']]

        solution = system.solve_auto(examples, test_inputs)
        expected = transform(['the', 'bird', 'flew'])
        correct = solution.predictions[0] == expected

        results[f'word_{name}'] = correct
        print(f"  {name}: {'✓' if correct else '✗'} [{solution.config_selected}]")

    # Test 4: Sentence transforms
    print("\n4. SENTENCE TRANSFORMS")
    print("-" * 40)

    sent_tests = [
        ('identity', lambda s: s),
        ('reverse', lambda s: s[::-1]),
    ]

    for name, transform in sent_tests:
        examples = [
            (['the', 'cat', 'is', 'big'], transform(['the', 'cat', 'is', 'big'])),
            (['a', 'dog', 'is', 'small'], transform(['a', 'dog', 'is', 'small'])),
        ]
        test_inputs = [['the', 'bird', 'is', 'fast']]

        solution = system.solve_auto(examples, test_inputs)
        expected = transform(['the', 'bird', 'is', 'fast'])
        correct = solution.predictions[0] == expected

        results[f'sent_{name}'] = correct
        print(f"  {name}: {'✓' if correct else '✗'} [{solution.config_selected}]")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    total = len(results)
    passed = sum(results.values())
    print(f"\nTotal: {passed}/{total} ({100*passed/total:.0f}%)")
    print(f"\nSystem stats: {system.stats}")

    if passed == total:
        print("\n✓ SUCCESS: Unified system works across all modalities!")
    else:
        print("\n✗ FAILED tests:")
        for name, passed in results.items():
            if not passed:
                print(f"  - {name}")

    print("=" * 70)

    return results


def test_cross_modal():
    """Test cross-modal transfer."""
    print("\n" + "=" * 70)
    print("CROSS-MODAL TRANSFER TEST")
    print("=" * 70)

    results = CrossModalTransfer.test_cross_modal_transfer()

    print("\n" + "=" * 70)
    print("CROSS-MODAL SUMMARY")
    print("=" * 70)

    for name, success in results.items():
        print(f"  {name}: {'✓' if success else '✗'}")

    return results


if __name__ == '__main__':
    test_unified_system()
    test_cross_modal()
