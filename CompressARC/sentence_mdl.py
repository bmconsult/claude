"""
Sentence-level MDL - Phase 8: Grammar Patterns

Building on word-level MDL to learn sentence-level patterns.
Key insight: Grammar rules are compressible patterns.

Examples:
- Statement → Question: "you are happy" → "are you happy"
- Template fills: "the X is Y" → "a X was Y"
- Structural transforms: subject-verb inversion
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Tuple, Dict, Optional, Callable
from word_mdl import WordCodec, WordPermutation, WordMapping, WordTransformSystem


# =============================================================================
# Sentence Pattern Types
# =============================================================================

class SentencePattern:
    """Base class for sentence-level patterns."""

    def __init__(self, name: str):
        self.name = name

    def match(self, words: List[str]) -> bool:
        """Check if pattern applies to this sentence."""
        raise NotImplementedError

    def apply(self, words: List[str]) -> List[str]:
        """Apply pattern to sentence."""
        raise NotImplementedError


class TemplatePattern(SentencePattern):
    """Pattern based on word templates.

    Example: "the X is Y" → "a X was Y"
    Matches sentences with specific words at specific positions,
    transforms by substituting words.
    """

    def __init__(self, name: str,
                 input_template: List[Optional[str]],
                 output_template: List[Optional[str]]):
        """
        Templates use None for variable positions.
        Example: ["the", None, "is", None] matches "the cat is big"
        """
        super().__init__(name)
        self.input_template = input_template
        self.output_template = output_template

    def match(self, words: List[str]) -> bool:
        if len(words) != len(self.input_template):
            return False
        for word, template in zip(words, self.input_template):
            if template is not None and word != template:
                return False
        return True

    def apply(self, words: List[str]) -> List[str]:
        if not self.match(words):
            return words

        result = []
        for i, out_template in enumerate(self.output_template):
            if out_template is not None:
                result.append(out_template)
            else:
                # Find corresponding input variable
                result.append(words[i])
        return result


class PositionalPattern(SentencePattern):
    """Pattern based on position swapping.

    Example: "X is Y" → "Y is X" (swap positions 0 and 2)
    """

    def __init__(self, name: str, permutation: List[int], required_len: Optional[int] = None):
        super().__init__(name)
        self.permutation = permutation
        self.required_len = required_len

    def match(self, words: List[str]) -> bool:
        if self.required_len is not None:
            return len(words) == self.required_len
        return len(words) == len(self.permutation)

    def apply(self, words: List[str]) -> List[str]:
        if not self.match(words):
            return words
        return [words[i] for i in self.permutation]


class ComposedPattern(SentencePattern):
    """Composed pattern: positional + template."""

    def __init__(self, name: str, positional: PositionalPattern, template: TemplatePattern):
        super().__init__(name)
        self.positional = positional
        self.template = template

    def match(self, words: List[str]) -> bool:
        return self.positional.match(words)

    def apply(self, words: List[str]) -> List[str]:
        # First apply positional
        intermediate = self.positional.apply(words)
        # Then apply template (if it matches)
        if self.template.match(intermediate):
            return self.template.apply(intermediate)
        return intermediate


# =============================================================================
# Sentence Transform System
# =============================================================================

class SentenceTransformSystem:
    """
    Learn sentence-level transforms using MDL.

    Extends WordTransformSystem with pattern detection:
    - Learns which pattern type applies
    - Learns pattern parameters
    """

    def __init__(self, max_len: int = 16):
        self.max_len = max_len
        self.examples: List[Tuple[List[str], List[str]]] = []

        # Pattern library (learned patterns)
        self.patterns: List[SentencePattern] = []
        self.selected_pattern: Optional[SentencePattern] = None

        # Fall back to WordTransformSystem for simple cases
        self.word_system = WordTransformSystem(max_len)

        # Scores
        self.scores = {}

    def add_example(self, input_words: List[str], output_words: List[str]):
        """Add training example."""
        self.examples.append((input_words, output_words))

    def _detect_template_pattern(self) -> Optional[TemplatePattern]:
        """Try to detect a template pattern from examples.

        Look for positions where the same word always appears.
        """
        if not self.examples:
            return None

        # Check all examples have same length
        lengths = set(len(inp) for inp, _ in self.examples)
        if len(lengths) != 1:
            return None
        sent_len = lengths.pop()

        # For each position, check if word is constant
        input_template = []
        output_template = []

        for pos in range(sent_len):
            # Input position
            inp_words_at_pos = set(inp[pos] for inp, _ in self.examples)
            if len(inp_words_at_pos) == 1:
                input_template.append(inp_words_at_pos.pop())
            else:
                input_template.append(None)

            # Output position
            out_words_at_pos = set(out[pos] for _, out in self.examples)
            if len(out_words_at_pos) == 1:
                output_template.append(out_words_at_pos.pop())
            else:
                output_template.append(None)

        # Check if this is a meaningful pattern (not all None)
        if all(t is None for t in input_template) and all(t is None for t in output_template):
            return None

        return TemplatePattern("detected_template", input_template, output_template)

    def _detect_positional_pattern(self) -> Optional[PositionalPattern]:
        """Try to detect a positional pattern from examples.

        Check if output is a permutation of input.
        """
        if not self.examples:
            return None

        # Check all examples have same length
        lengths = set(len(inp) for inp, _ in self.examples)
        if len(lengths) != 1:
            return None
        sent_len = lengths.pop()

        # For each example, find the permutation
        permutations = []
        for inp_words, out_words in self.examples:
            if set(inp_words) != set(out_words):
                return None  # Not a permutation

            perm = []
            for out_word in out_words:
                # Find position in input
                for j, inp_word in enumerate(inp_words):
                    if inp_word == out_word and j not in perm:
                        perm.append(j)
                        break
                else:
                    return None  # Can't find permutation

            permutations.append(tuple(perm))

        # Check if all permutations are the same
        if len(set(permutations)) != 1:
            return None

        return PositionalPattern("detected_permutation", list(permutations[0]), sent_len)

    def _compute_loss(self, predictions: List[List[str]]) -> float:
        """Compute accuracy-based loss."""
        total = 0.0
        for pred, (_, target) in zip(predictions, self.examples):
            matches = sum(1 for p, t in zip(pred, target) if p == t)
            max_len = max(len(pred), len(target))
            accuracy = matches / max_len if max_len > 0 else 1.0
            total += 1.0 - accuracy
        return total / len(self.examples)

    def train(self) -> str:
        """Train and select best pattern/configuration."""
        if not self.examples:
            return 'none'

        # Try to detect patterns
        template = self._detect_template_pattern()
        positional = self._detect_positional_pattern()

        # Test identity
        id_preds = [inp for inp, _ in self.examples]
        id_loss = self._compute_loss(id_preds)
        self.scores['identity'] = {'loss': id_loss, 'dl': 0}

        # Test template pattern
        if template:
            t_preds = [template.apply(inp) for inp, _ in self.examples]
            t_loss = self._compute_loss(t_preds)
            # DL = number of fixed positions
            t_dl = sum(1 for t in template.output_template if t is not None) * 0.1
            self.scores['template'] = {'loss': t_loss, 'dl': t_dl}
            if t_loss == 0:
                self.patterns.append(template)

        # Test positional pattern
        if positional:
            p_preds = [positional.apply(inp) for inp, _ in self.examples]
            p_loss = self._compute_loss(p_preds)
            # DL = deviation from identity permutation
            identity = list(range(len(positional.permutation)))
            p_dl = sum(1 for i, j in zip(positional.permutation, identity) if i != j) * 0.1
            self.scores['positional'] = {'loss': p_loss, 'dl': p_dl}
            if p_loss == 0:
                self.patterns.append(positional)

        # Fall back to WordTransformSystem if no pattern works
        for inp, out in self.examples:
            self.word_system.add_example(inp, out)
        word_selected = self.word_system.train()
        w_preds = [self.word_system.predict(inp) for inp, _ in self.examples]
        w_loss = self._compute_loss(w_preds)
        self.scores['word_system'] = {'loss': w_loss, 'dl': 0.5}  # Higher DL for complex system

        # Select best (prefer lowest loss, then lowest DL)
        best = min(self.scores.keys(), key=lambda k: (self.scores[k]['loss'], self.scores[k]['dl']))

        if best == 'template' and template:
            self.selected_pattern = template
        elif best == 'positional' and positional:
            self.selected_pattern = positional
        elif best == 'word_system':
            self.selected_pattern = None  # Use word_system
        else:
            self.selected_pattern = None  # Identity

        return best

    def predict(self, input_words: List[str]) -> List[str]:
        """Predict output sentence."""
        if self.selected_pattern:
            return self.selected_pattern.apply(input_words)
        elif 'word_system' in self.scores and self.scores.get('word_system', {}).get('loss', 1) == 0:
            return self.word_system.predict(input_words)
        return input_words  # Identity


# =============================================================================
# Test Patterns
# =============================================================================

SENTENCE_TRANSFORMS = {
    # Identity
    'identity': lambda words: words,

    # Simple positional (reordering)
    'reverse': lambda words: words[::-1],
    'swap_first_last': lambda words: [words[-1]] + words[1:-1] + [words[0]] if len(words) > 1 else words,

    # Template-based (word substitution at fixed positions)
    'the_to_a': lambda words: ['a' if w == 'the' else w for w in words],
    'is_to_was': lambda words: ['was' if w == 'is' else w for w in words],

    # Question formation: "X is Y" → "is X Y"
    'statement_to_question': lambda words: [words[1], words[0]] + words[2:] if len(words) >= 2 else words,

    # Composed: reverse then substitute
    'reverse_the_to_a': lambda words: ['a' if w == 'the' else w for w in words[::-1]],
}


def test_sentence_transforms():
    """Test sentence-level transform learning."""
    print("=" * 70)
    print("SENTENCE MDL - SENTENCE PATTERNS")
    print("=" * 70)
    print()

    # Training sentences (4 words each)
    train_sentences = [
        ['the', 'cat', 'is', 'big'],
        ['the', 'dog', 'is', 'small'],
        ['the', 'bird', 'is', 'fast'],
        ['a', 'mouse', 'is', 'tiny'],
        ['the', 'fish', 'is', 'wet'],
    ]

    # Test sentences
    test_sentences = [
        ['the', 'horse', 'is', 'tall'],
        ['a', 'snake', 'is', 'long'],
    ]

    results = {}

    for name, transform_fn in SENTENCE_TRANSFORMS.items():
        print(f"{name}:", end=" ", flush=True)

        system = SentenceTransformSystem(max_len=16)

        # Add training examples
        for words in train_sentences:
            system.add_example(words, transform_fn(words))

        selected = system.train()

        # Test on held-out sentences
        correct = 0
        for words in test_sentences:
            pred = system.predict(words)
            expected = transform_fn(words)
            if pred == expected:
                correct += 1

        accuracy = correct / len(test_sentences)
        results[name] = {'selected': selected, 'accuracy': accuracy}

        loss = system.scores.get(selected, {}).get('loss', -1)
        print(f"{correct}/{len(test_sentences)} ({accuracy*100:.0f}%) [{selected}] loss={loss:.3f}")

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    overall = sum(r['accuracy'] for r in results.values()) / len(results)
    print(f"\nOverall: {overall*100:.0f}%")

    if overall >= 0.8:
        print("\nSUCCESS: ≥80% on sentence transforms!")
    else:
        print("\nFailing transforms:")
        for name, r in results.items():
            if r['accuracy'] < 0.8:
                print(f"  {name}: {r['accuracy']*100:.0f}% [{r['selected']}]")
    print("=" * 70)

    return results


if __name__ == '__main__':
    test_sentence_transforms()
