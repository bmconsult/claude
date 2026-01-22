"""
Word-level MDL - Phase 8 Continued

Extension of character-level MDL to word-level patterns.
Same principle: find simplest explanation (MDL) that fits the data.

Progression:
1. Character transforms ← DONE (language_mdl.py)
2. Word transforms ← THIS FILE
3. Sentence patterns
4. Grammar/semantics
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Tuple, Dict, Optional, Set
from dataclasses import dataclass
from collections import Counter
import hashlib
import pickle
from pathlib import Path


# =============================================================================
# Word Encoding
# =============================================================================

class WordCodec:
    """Encode/decode words to/from integers."""

    def __init__(self):
        self.word_to_idx: Dict[str, int] = {'<PAD>': 0, '<UNK>': 1}
        self.idx_to_word: Dict[int, str] = {0: '<PAD>', 1: '<UNK>'}
        self.next_idx = 2

    def fit(self, sentences: List[List[str]]):
        """Build vocabulary from sentences."""
        for words in sentences:
            for word in words:
                if word not in self.word_to_idx:
                    self.word_to_idx[word] = self.next_idx
                    self.idx_to_word[self.next_idx] = word
                    self.next_idx += 1

    @property
    def vocab_size(self) -> int:
        return len(self.word_to_idx)

    def encode(self, words: List[str]) -> List[int]:
        """Convert word list to indices."""
        return [self.word_to_idx.get(w, 1) for w in words]

    def decode(self, indices: List[int]) -> List[str]:
        """Convert indices to words."""
        return [self.idx_to_word.get(i, '<UNK>') for i in indices if i > 0]

    def encode_tensor(self, words: List[str]) -> torch.Tensor:
        return torch.tensor(self.encode(words), dtype=torch.long)


# =============================================================================
# Word Transform Modules
# =============================================================================

class WordPermutation(nn.Module):
    """Learn word position permutations (sentence reordering).

    Key insight: Permutations don't need vocabulary - they just reorder positions.
    We learn a position→position mapping, then apply it to any word list.
    """

    def __init__(self, max_len: int = 16):
        super().__init__()
        self.max_len = max_len
        self.log_alpha = nn.Parameter(torch.zeros(max_len, max_len))

    def forward(self, seq_len: int, hard: bool = False) -> torch.Tensor:
        """
        Returns permutation matrix for given sequence length.
        """
        log_alpha = self.log_alpha[:seq_len, :seq_len]
        perm = self._sinkhorn(log_alpha)

        if hard:
            perm_hard = torch.zeros_like(perm)
            indices = perm.argmax(dim=1)
            perm_hard.scatter_(1, indices.unsqueeze(1), 1.0)
            perm = perm_hard

        return perm

    def get_permutation_indices(self, seq_len: int) -> List[int]:
        """Get hard permutation as list of indices."""
        perm = self.forward(seq_len, hard=True)
        return perm.argmax(dim=1).tolist()

    def apply_to_words(self, words: List[str]) -> List[str]:
        """Apply learned permutation to word list."""
        indices = self.get_permutation_indices(len(words))
        return [words[i] for i in indices]

    def _sinkhorn(self, log_alpha: torch.Tensor, n_iter: int = 20) -> torch.Tensor:
        for _ in range(n_iter):
            log_alpha = log_alpha - torch.logsumexp(log_alpha, dim=1, keepdim=True)
            log_alpha = log_alpha - torch.logsumexp(log_alpha, dim=0, keepdim=True)
        return torch.exp(log_alpha)

    def description_length(self, seq_len: int) -> float:
        perm = self._sinkhorn(self.log_alpha[:seq_len, :seq_len])
        identity = torch.eye(seq_len, device=perm.device)
        deviation = (perm - identity).abs().sum()
        return deviation.item() * 0.5


class WordMapping(nn.Module):
    """Learn word-to-word mappings (substitution patterns)."""

    def __init__(self, vocab_size: int = 1000):
        super().__init__()
        self.vocab_size = vocab_size
        self.log_map = nn.Parameter(torch.zeros(vocab_size, vocab_size))
        # Initialize near identity
        self.log_map.data += torch.eye(vocab_size) * 2

    def forward(self, x: torch.Tensor, hard: bool = False) -> torch.Tensor:
        mapping = F.softmax(self.log_map, dim=1)
        x_onehot = F.one_hot(x, num_classes=self.vocab_size).float()
        x_mapped = torch.mm(x_onehot, mapping)

        if hard:
            return x_mapped.argmax(dim=1)
        return x_mapped

    def description_length(self) -> float:
        mapping = F.softmax(self.log_map, dim=1)
        identity = torch.eye(self.vocab_size, device=mapping.device)
        deviation = (mapping - identity).abs().sum()
        return deviation.item() * 0.1


# =============================================================================
# Word Transform System
# =============================================================================

class WordTransformSystem:
    """
    Learn word-level transforms using MDL.

    Handles:
    - Word permutations (sentence reordering)
    - Word mappings (systematic substitutions)
    - Composed transforms
    """

    def __init__(self, max_len: int = 16):
        self.max_len = max_len
        self.codec = WordCodec()
        self.examples: List[Tuple[List[str], List[str]]] = []

        # Will be initialized after vocabulary is built
        self.perm = None
        self.mapping = None
        self.vocab_size = 0

        # Results
        self.selected = None
        self.scores = {}

    def add_example(self, input_words: List[str], output_words: List[str]):
        """Add training example (as word lists)."""
        self.examples.append((input_words, output_words))

    def _build_vocab(self):
        """Build vocabulary from all examples."""
        all_sentences = []
        for inp, out in self.examples:
            all_sentences.append(inp)
            all_sentences.append(out)
        self.codec.fit(all_sentences)
        self.vocab_size = self.codec.vocab_size

        # Initialize modules
        self.perm = WordPermutation(self.max_len)  # Position-based, no vocab needed
        self.mapping = WordMapping(self.vocab_size)

    def _compute_loss(self, predictions: List[List[str]]) -> float:
        """Compute word-level accuracy loss."""
        total = 0.0
        for pred, (_, target) in zip(predictions, self.examples):
            matches = sum(1 for p, t in zip(pred, target) if p == t)
            max_len = max(len(pred), len(target))
            accuracy = matches / max_len if max_len > 0 else 1.0
            total += 1.0 - accuracy
        return total / len(self.examples)

    def _train_identity(self) -> Tuple[float, float]:
        """Test if identity works."""
        preds = [inp for inp, _ in self.examples]
        loss = self._compute_loss(preds)
        return loss, 0.0

    def _train_permutation(self, max_steps: int = 300) -> Tuple[float, float]:
        """Train word permutation.

        Key insight: Train on POSITIONS, not vocabulary.
        Learn which position i maps to position j.
        """
        self.perm = WordPermutation(self.max_len)
        optimizer = torch.optim.Adam(self.perm.parameters(), lr=0.3)

        for step in range(max_steps):
            optimizer.zero_grad()
            total_loss = 0.0

            for inp_words, out_words in self.examples:
                if len(inp_words) != len(out_words):
                    continue

                seq_len = len(inp_words)

                # Find target permutation: for each output position, which input position?
                # target[i] = j means output position i gets input position j's word
                target_indices = []
                for out_word in out_words:
                    # Find which input position has this word
                    for j, inp_word in enumerate(inp_words):
                        if inp_word == out_word:
                            target_indices.append(j)
                            break
                    else:
                        target_indices.append(0)  # fallback

                target = torch.tensor(target_indices, dtype=torch.long)
                target_onehot = F.one_hot(target, num_classes=seq_len).float()

                perm = self.perm(seq_len, hard=False)
                loss = F.mse_loss(perm, target_onehot)
                total_loss += loss

            if total_loss.requires_grad:
                total_loss.backward()
                optimizer.step()

            if total_loss.item() < 0.01:
                break

        # Evaluate (works on any words now!)
        preds = []
        for inp_words, _ in self.examples:
            pred = self.perm.apply_to_words(inp_words)
            preds.append(pred)

        loss = self._compute_loss(preds)
        dl = self.perm.description_length(len(self.examples[0][0]))
        return loss, dl

    def _train_mapping(self, max_steps: int = 300) -> Tuple[float, float]:
        """Train word mapping."""
        self.mapping = WordMapping(self.vocab_size)
        optimizer = torch.optim.Adam(self.mapping.parameters(), lr=0.3)

        for step in range(max_steps):
            optimizer.zero_grad()
            total_loss = 0.0

            for inp_words, out_words in self.examples:
                if len(inp_words) != len(out_words):
                    continue

                inp = self.codec.encode_tensor(inp_words)
                out = self.codec.encode_tensor(out_words)

                pred = self.mapping(inp, hard=False)
                out_onehot = F.one_hot(out, num_classes=self.vocab_size).float()
                loss = F.mse_loss(pred, out_onehot)
                total_loss += loss

            if total_loss.requires_grad:
                total_loss.backward()
                optimizer.step()

            if total_loss.item() < 0.01:
                break

        # Evaluate
        preds = []
        for inp_words, _ in self.examples:
            inp = self.codec.encode_tensor(inp_words)
            pred_idx = self.mapping(inp, hard=True)
            preds.append(self.codec.decode(pred_idx.tolist()))

        loss = self._compute_loss(preds)
        dl = self.mapping.description_length()
        return loss, dl

    def _train_composed(self, max_steps: int = 300) -> Tuple[float, float]:
        """Train permutation → mapping composed."""
        self.perm = WordPermutation(self.max_len)
        self.mapping = WordMapping(self.vocab_size)

        best_loss = float('inf')
        best_perm_state = None
        best_map_state = None

        seq_len = len(self.examples[0][0]) if self.examples else 4
        perm_hypotheses = self._generate_perm_hypotheses(seq_len)

        for perm_init in perm_hypotheses:
            self.perm = WordPermutation(self.max_len)
            if perm_init is not None:
                self.perm.log_alpha.data = perm_init.clone()

            self.mapping = WordMapping(self.vocab_size)
            map_opt = torch.optim.Adam(self.mapping.parameters(), lr=0.3)

            for step in range(200):
                map_opt.zero_grad()
                total_loss = 0.0

                for inp_words, out_words in self.examples:
                    if len(inp_words) != len(out_words):
                        continue

                    # Apply permutation to get intermediate words
                    permuted = self.perm.apply_to_words(inp_words)
                    # Train mapping from permuted to output
                    inp = self.codec.encode_tensor(permuted)
                    out = self.codec.encode_tensor(out_words)

                    pred = self.mapping(inp, hard=False)
                    out_onehot = F.one_hot(out, num_classes=self.vocab_size).float()
                    loss = F.mse_loss(pred, out_onehot)
                    total_loss += loss

                if total_loss.requires_grad:
                    total_loss.backward()
                    map_opt.step()

                if total_loss.item() < 0.01:
                    break

            # Evaluate
            preds = []
            for inp_words, _ in self.examples:
                permuted = self.perm.apply_to_words(inp_words)
                inp = self.codec.encode_tensor(permuted)
                map_out = self.mapping(inp, hard=True)
                preds.append(self.codec.decode(map_out.tolist()))

            loss = self._compute_loss(preds)
            if loss < best_loss:
                best_loss = loss
                best_perm_state = {k: v.clone() for k, v in self.perm.state_dict().items()}
                best_map_state = {k: v.clone() for k, v in self.mapping.state_dict().items()}

            if best_loss == 0.0:
                break

        if best_perm_state:
            self.perm.load_state_dict(best_perm_state)
        if best_map_state:
            self.mapping.load_state_dict(best_map_state)

        # Final eval
        preds = []
        for inp_words, _ in self.examples:
            permuted = self.perm.apply_to_words(inp_words)
            inp = self.codec.encode_tensor(permuted)
            map_out = self.mapping(inp, hard=True)
            preds.append(self.codec.decode(map_out.tolist()))

        loss = self._compute_loss(preds)
        dl = self.perm.description_length(seq_len) + self.mapping.description_length()
        return loss, dl

    def _generate_perm_hypotheses(self, seq_len: int) -> List[Optional[torch.Tensor]]:
        """Generate common permutation patterns."""
        hypotheses = [None]  # Identity

        # Reverse
        reverse = torch.zeros(self.max_len, self.max_len)
        for i in range(seq_len):
            reverse[i, seq_len - 1 - i] = 5.0
        hypotheses.append(reverse)

        # Rotate left
        rotate_l = torch.zeros(self.max_len, self.max_len)
        for i in range(seq_len):
            rotate_l[i, (i + 1) % seq_len] = 5.0
        hypotheses.append(rotate_l)

        # Swap pairs (for even-length)
        if seq_len >= 2:
            swap = torch.zeros(self.max_len, self.max_len)
            for i in range(0, seq_len - 1, 2):
                swap[i, i + 1] = 5.0
                swap[i + 1, i] = 5.0
            if seq_len % 2 == 1:
                swap[seq_len - 1, seq_len - 1] = 5.0
            hypotheses.append(swap)

        return hypotheses

    def train(self) -> str:
        """Train and select best configuration."""
        if not self.examples:
            return 'none'

        self._build_vocab()

        mdl_lambda = 0.001
        saved_states = {}

        id_loss, id_dl = self._train_identity()
        self.scores['identity'] = {'loss': id_loss, 'dl': id_dl, 'mdl': id_loss + mdl_lambda * id_dl}
        saved_states['identity'] = (None, None)

        perm_loss, perm_dl = self._train_permutation()
        self.scores['permutation'] = {'loss': perm_loss, 'dl': perm_dl, 'mdl': perm_loss + mdl_lambda * perm_dl}
        saved_states['permutation'] = (
            {k: v.clone() for k, v in self.perm.state_dict().items()},
            None
        )

        map_loss, map_dl = self._train_mapping()
        self.scores['mapping'] = {'loss': map_loss, 'dl': map_dl, 'mdl': map_loss + mdl_lambda * map_dl}
        saved_states['mapping'] = (
            None,
            {k: v.clone() for k, v in self.mapping.state_dict().items()}
        )

        comp_loss, comp_dl = self._train_composed()
        self.scores['composed'] = {'loss': comp_loss, 'dl': comp_dl, 'mdl': comp_loss + mdl_lambda * comp_dl}
        saved_states['composed'] = (
            {k: v.clone() for k, v in self.perm.state_dict().items()},
            {k: v.clone() for k, v in self.mapping.state_dict().items()}
        )

        best = min(self.scores.keys(), key=lambda k: (self.scores[k]['loss'], self.scores[k]['mdl']))
        self.selected = best

        perm_state, map_state = saved_states[best]
        if perm_state:
            self.perm = WordPermutation(self.max_len)
            self.perm.load_state_dict(perm_state)
        if map_state:
            self.mapping = WordMapping(self.vocab_size)
            self.mapping.load_state_dict(map_state)

        return best

    def _apply_mapping(self, words: List[str]) -> List[str]:
        """Apply mapping, passing through OOV words unchanged."""
        result = []
        for word in words:
            if word in self.codec.word_to_idx:
                # In vocabulary - apply mapping
                idx = self.codec.word_to_idx[word]
                inp = torch.tensor([idx], dtype=torch.long)
                out_idx = self.mapping(inp, hard=True).item()
                result.append(self.codec.idx_to_word.get(out_idx, word))
            else:
                # OOV - pass through unchanged
                result.append(word)
        return result

    def predict(self, input_words: List[str]) -> List[str]:
        """Predict output words."""
        if self.selected == 'identity':
            return input_words

        if self.selected == 'permutation':
            # Permutation works on any words (position-based)
            return self.perm.apply_to_words(input_words)
        elif self.selected == 'mapping':
            # Mapping with OOV pass-through
            return self._apply_mapping(input_words)
        elif self.selected == 'composed':
            # First permute (works on any words)
            permuted = self.perm.apply_to_words(input_words)
            # Then map with OOV pass-through
            return self._apply_mapping(permuted)

        return input_words


# =============================================================================
# Test Transforms
# =============================================================================

WORD_TRANSFORMS = {
    # Identity
    'identity': lambda words: words,

    # Permutations
    'reverse': lambda words: words[::-1],
    'rotate_left': lambda words: words[1:] + words[:1] if words else words,
    'swap_pairs': lambda words: [words[i+1] if i % 2 == 0 and i+1 < len(words)
                                  else words[i-1] if i % 2 == 1
                                  else words[i] for i in range(len(words))],

    # Mappings (word substitutions)
    'the_to_a': lambda words: ['a' if w == 'the' else w for w in words],
    'is_to_was': lambda words: ['was' if w == 'is' else w for w in words],

    # Composed
    'reverse_the_to_a': lambda words: ['a' if w == 'the' else w for w in words[::-1]],
}


def test_word_transforms():
    """Test word-level transform learning."""
    print("=" * 70)
    print("WORD MDL - WORD-LEVEL TRANSFORMS")
    print("=" * 70)
    print()

    # Training sentences (4 words each)
    train_sentences = [
        ['the', 'quick', 'brown', 'fox'],
        ['the', 'lazy', 'brown', 'dog'],
        ['a', 'fast', 'red', 'car'],
        ['the', 'big', 'blue', 'sky'],
        ['a', 'small', 'green', 'tree'],
    ]

    # Test sentences
    test_sentences = [
        ['the', 'slow', 'black', 'cat'],
        ['a', 'tall', 'white', 'house'],
    ]

    results = {}

    for name, transform_fn in WORD_TRANSFORMS.items():
        print(f"{name}:", end=" ", flush=True)

        system = WordTransformSystem(max_len=16)

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

        loss = system.scores[selected]['loss']
        print(f"{correct}/{len(test_sentences)} ({accuracy*100:.0f}%) [{selected}] loss={loss:.3f}")

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    overall = sum(r['accuracy'] for r in results.values()) / len(results)
    print(f"\nOverall: {overall*100:.0f}%")

    if overall >= 0.8:
        print("\nSUCCESS: ≥80% on word transforms!")
    else:
        print("\nFailing transforms:")
        for name, r in results.items():
            if r['accuracy'] < 0.8:
                print(f"  {name}: {r['accuracy']*100:.0f}% [{r['selected']}]")
    print("=" * 70)

    return results


if __name__ == '__main__':
    test_word_transforms()
