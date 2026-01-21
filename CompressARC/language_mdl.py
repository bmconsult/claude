"""
Language MDL - Phase 8: Bridge from Sequences to Language

Key insight: Start with character-level transforms.
Characters are discrete tokens, positions are positions.
Same MDL principle: find simplest explanation that fits.

This is NOT an LLM. This is pattern learning with compression.

Progression:
1. Character transforms (capitalize, reverse, etc.) ← START HERE
2. Token patterns (grammar rules)
3. Compositional meaning
4. Full language capability
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
import random
import string
import hashlib
import pickle
from pathlib import Path


# =============================================================================
# Character Transform Abstraction Library
# =============================================================================

@dataclass
class CharAbstraction:
    """A stored abstraction from a learned character transform."""
    signature: str
    config_type: str  # 'identity', 'permutation', 'mapping', 'composed'
    perm_state: Optional[Dict] = None
    map_state: Optional[Dict] = None
    train_steps: int = 0
    final_loss: float = 0.0
    times_used: int = 0
    times_helped: int = 0


def compute_char_signature(examples: List[Tuple[str, str]]) -> str:
    """Compute signature for character transform.

    Uses canonical input 'hello' to get consistent signature.
    """
    canonical = 'hello'
    canonical_output = None

    for inp, out in examples:
        if inp == canonical:
            canonical_output = out
            break

    if canonical_output is None:
        # Try 'abcde' as alternative canonical
        for inp, out in examples:
            if inp == 'abcde':
                canonical_output = out
                break

    if canonical_output is None:
        # Fall back to sorted examples hash
        sorted_ex = sorted(examples, key=lambda x: x[0])[:3]
        sig_str = '|'.join(f'{i}->{o}' for i, o in sorted_ex)
    else:
        sig_str = canonical_output

    return hashlib.md5(sig_str.encode()).hexdigest()[:16]


class CharAbstractionLibrary:
    """Stores and retrieves learned character transforms."""

    def __init__(self, save_path: str = "char_abstractions.pkl"):
        self.abstractions: Dict[str, CharAbstraction] = {}
        self.save_path = Path(save_path)
        if self.save_path.exists():
            self.load()

    def add(self, examples: List[Tuple[str, str]], config_type: str,
            perm_state: Optional[Dict] = None, map_state: Optional[Dict] = None,
            train_steps: int = 0, final_loss: float = 0.0) -> str:
        """Add a learned transform to the library."""
        signature = compute_char_signature(examples)

        def to_cpu(state):
            if state is None:
                return None
            return {k: v.detach().cpu() if isinstance(v, torch.Tensor) else v
                    for k, v in state.items()}

        self.abstractions[signature] = CharAbstraction(
            signature=signature,
            config_type=config_type,
            perm_state=to_cpu(perm_state),
            map_state=to_cpu(map_state),
            train_steps=train_steps,
            final_loss=final_loss
        )
        self.save()
        return signature

    def find(self, examples: List[Tuple[str, str]]) -> Optional[CharAbstraction]:
        """Find exact match for transform."""
        signature = compute_char_signature(examples)
        return self.abstractions.get(signature)

    def get_initialization(self, examples: List[Tuple[str, str]]) -> Optional[Dict]:
        """Get saved state if we've seen this transform before."""
        abstraction = self.find(examples)
        if abstraction is None:
            return None
        abstraction.times_used += 1
        return {
            'config_type': abstraction.config_type,
            'perm_state': abstraction.perm_state,
            'map_state': abstraction.map_state,
            'expected_steps': 1
        }

    def update_stats(self, examples: List[Tuple[str, str]], helped: bool):
        """Update transfer statistics."""
        signature = compute_char_signature(examples)
        if signature in self.abstractions:
            if helped:
                self.abstractions[signature].times_helped += 1
            self.save()

    def save(self):
        with open(self.save_path, 'wb') as f:
            pickle.dump(self.abstractions, f)

    def load(self):
        try:
            with open(self.save_path, 'rb') as f:
                self.abstractions = pickle.load(f)
        except Exception:
            self.abstractions = {}

    def clear(self):
        self.abstractions = {}
        if self.save_path.exists():
            self.save_path.unlink()

    def stats(self) -> dict:
        if not self.abstractions:
            return {"size": 0}
        by_type = {}
        for a in self.abstractions.values():
            by_type[a.config_type] = by_type.get(a.config_type, 0) + 1
        return {
            "size": len(self.abstractions),
            "by_type": by_type,
            "total_uses": sum(a.times_used for a in self.abstractions.values()),
        }


# Singleton
_char_library = None

def get_char_library(save_path: str = "char_abstractions.pkl") -> CharAbstractionLibrary:
    """Get or create the global character abstraction library."""
    global _char_library
    if _char_library is None:
        _char_library = CharAbstractionLibrary(save_path)
    return _char_library

def reset_char_library():
    """Reset the global library (for testing)."""
    global _char_library
    if _char_library is not None:
        _char_library.clear()
    _char_library = None


# =============================================================================
# Character Encoding
# =============================================================================

class CharacterCodec:
    """Encode/decode characters to/from integers."""

    def __init__(self):
        # Basic ASCII printable + special tokens
        self.chars = list(string.printable[:95])  # printable minus whitespace variants
        self.pad_token = '<PAD>'
        self.unk_token = '<UNK>'

        self.char_to_idx = {c: i+2 for i, c in enumerate(self.chars)}
        self.char_to_idx[self.pad_token] = 0
        self.char_to_idx[self.unk_token] = 1

        self.idx_to_char = {i: c for c, i in self.char_to_idx.items()}
        self.vocab_size = len(self.char_to_idx)

    def encode(self, text: str) -> List[int]:
        """Convert string to list of integers."""
        return [self.char_to_idx.get(c, 1) for c in text]

    def decode(self, indices: List[int]) -> str:
        """Convert list of integers to string."""
        return ''.join(self.idx_to_char.get(i, '?') for i in indices if i > 0)

    def encode_tensor(self, text: str) -> torch.Tensor:
        """Convert string to tensor."""
        return torch.tensor(self.encode(text), dtype=torch.long)


# =============================================================================
# Character Transform Modules
# =============================================================================

class CharPermutation(nn.Module):
    """Learn character position permutations (like reverse, rotate, etc.)."""

    def __init__(self, max_len: int = 32, vocab_size: int = 100):
        super().__init__()
        self.max_len = max_len
        self.vocab_size = vocab_size
        # Soft permutation matrix
        self.log_alpha = nn.Parameter(torch.zeros(max_len, max_len))

    def forward(self, x: torch.Tensor, hard: bool = False) -> torch.Tensor:
        """
        x: (seq_len,) integer tensor of character indices
        Returns: permuted sequence
        """
        seq_len = x.shape[0]

        # Get permutation matrix for this length
        log_alpha = self.log_alpha[:seq_len, :seq_len]

        # Sinkhorn normalization for doubly-stochastic matrix
        perm = self._sinkhorn(log_alpha)

        if hard:
            # Hard permutation for inference
            perm_hard = torch.zeros_like(perm)
            indices = perm.argmax(dim=1)
            perm_hard.scatter_(1, indices.unsqueeze(1), 1.0)
            perm = perm_hard

        # Apply permutation: one-hot encode, permute, decode
        x_onehot = F.one_hot(x, num_classes=self.vocab_size).float()  # (seq_len, vocab)
        x_permuted = torch.mm(perm, x_onehot)  # (seq_len, vocab)

        if hard:
            return x_permuted.argmax(dim=1)
        return x_permuted

    def _sinkhorn(self, log_alpha: torch.Tensor, n_iter: int = 20) -> torch.Tensor:
        """Sinkhorn normalization for doubly-stochastic matrix."""
        for _ in range(n_iter):
            log_alpha = log_alpha - torch.logsumexp(log_alpha, dim=1, keepdim=True)
            log_alpha = log_alpha - torch.logsumexp(log_alpha, dim=0, keepdim=True)
        return torch.exp(log_alpha)

    def description_length(self, seq_len: int) -> float:
        """MDL cost of this permutation."""
        perm = self._sinkhorn(self.log_alpha[:seq_len, :seq_len])
        # Entropy-based: more uniform = more bits
        entropy = -(perm * (perm + 1e-10).log()).sum()
        # Identity is simplest
        identity = torch.eye(seq_len, device=perm.device)
        deviation = (perm - identity).abs().sum()
        return entropy.item() * 0.1 + deviation.item() * 0.5


class CharMapping(nn.Module):
    """Learn character-to-character mappings (like capitalize, shift, etc.)."""

    def __init__(self, vocab_size: int = 100):
        super().__init__()
        self.vocab_size = vocab_size
        # Learn a soft mapping matrix: input_char -> output_char
        self.log_map = nn.Parameter(torch.zeros(vocab_size, vocab_size))
        # Initialize near identity
        self.log_map.data += torch.eye(vocab_size) * 2

    def forward(self, x: torch.Tensor, hard: bool = False) -> torch.Tensor:
        """
        x: (seq_len,) integer tensor of character indices
        Returns: mapped sequence
        """
        # Softmax over output dimension for each input
        mapping = F.softmax(self.log_map, dim=1)

        # One-hot encode input
        x_onehot = F.one_hot(x, num_classes=self.vocab_size).float()

        # Apply mapping
        x_mapped = torch.mm(x_onehot, mapping)

        if hard:
            return x_mapped.argmax(dim=1)
        return x_mapped

    def description_length(self) -> float:
        """MDL cost of this mapping."""
        mapping = F.softmax(self.log_map, dim=1)
        # Identity is simplest
        identity = torch.eye(self.vocab_size, device=mapping.device)
        deviation = (mapping - identity).abs().sum()
        return deviation.item() * 0.1


# =============================================================================
# Character Transform System
# =============================================================================

class CharTransformSystem:
    """
    Learn character-level transforms using MDL.

    Like ComposedTransformSystem but for characters.
    """

    def __init__(self, max_len: int = 32, use_library: bool = True):
        self.max_len = max_len
        self.codec = CharacterCodec()
        self.vocab_size = self.codec.vocab_size
        self.use_library = use_library

        # Modules
        self.perm = CharPermutation(max_len, self.vocab_size)
        self.mapping = CharMapping(self.vocab_size)

        # Training data
        self.examples: List[Tuple[str, str]] = []

        # Results
        self.selected = None
        self.scores = {}
        self.used_transfer = False
        self.train_steps = 0

    def add_example(self, input_str: str, output_str: str):
        """Add training example."""
        self.examples.append((input_str, output_str))

    def _compute_loss(self, predictions: List[str]) -> float:
        """Compute accuracy-based loss."""
        total = 0.0
        for pred, (_, target) in zip(predictions, self.examples):
            # Character-level accuracy
            matches = sum(1 for p, t in zip(pred, target) if p == t)
            max_len = max(len(pred), len(target))
            accuracy = matches / max_len if max_len > 0 else 1.0
            total += 1.0 - accuracy
        return total / len(self.examples)

    def _train_identity(self) -> Tuple[float, float]:
        """Test if identity works."""
        preds = [inp for inp, _ in self.examples]
        loss = self._compute_loss(preds)
        dl = 0.0
        return loss, dl

    def _train_permutation(self, max_steps: int = 300) -> Tuple[float, float]:
        """Train permutation-only."""
        self.perm = CharPermutation(self.max_len, self.vocab_size)
        optimizer = torch.optim.Adam(self.perm.parameters(), lr=0.3)

        for step in range(max_steps):
            optimizer.zero_grad()
            total_loss = 0.0

            for inp_str, out_str in self.examples:
                inp = self.codec.encode_tensor(inp_str)
                out = self.codec.encode_tensor(out_str)

                if len(inp) != len(out):
                    continue  # Skip length-changing transforms

                pred = self.perm(inp, hard=False)
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
        for inp_str, _ in self.examples:
            inp = self.codec.encode_tensor(inp_str)
            pred_idx = self.perm(inp, hard=True)
            preds.append(self.codec.decode(pred_idx.tolist()))

        loss = self._compute_loss(preds)
        dl = self.perm.description_length(len(self.examples[0][0]))
        return loss, dl

    def _train_mapping(self, max_steps: int = 300) -> Tuple[float, float]:
        """Train character mapping."""
        self.mapping = CharMapping(self.codec.vocab_size)
        optimizer = torch.optim.Adam(self.mapping.parameters(), lr=0.3)

        for step in range(max_steps):
            optimizer.zero_grad()
            total_loss = 0.0

            for inp_str, out_str in self.examples:
                inp = self.codec.encode_tensor(inp_str)
                out = self.codec.encode_tensor(out_str)

                if len(inp) != len(out):
                    continue

                pred = self.mapping(inp, hard=False)
                out_onehot = F.one_hot(out, num_classes=self.codec.vocab_size).float()

                loss = F.mse_loss(pred, out_onehot)
                total_loss += loss

            if total_loss.requires_grad:
                total_loss.backward()
                optimizer.step()

            if total_loss.item() < 0.01:
                break

        # Evaluate
        preds = []
        for inp_str, _ in self.examples:
            inp = self.codec.encode_tensor(inp_str)
            pred_idx = self.mapping(inp, hard=True)
            preds.append(self.codec.decode(pred_idx.tolist()))

        loss = self._compute_loss(preds)
        dl = self.mapping.description_length()
        return loss, dl

    def _train_composed(self, max_steps: int = 500) -> Tuple[float, float]:
        """Train permutation → mapping composed.

        Strategy: Try different decompositions since we don't know the intermediate.
        For reverse_upper("hello") -> "OLLEH", could be:
        - perm=reverse, map=uppercase: olleh -> OLLEH
        - perm=identity, map=??? (impossible - can't learn reverse through mapping)

        Approach: Since we know common permutations, try each one and let mapping learn.
        """
        self.perm = CharPermutation(self.max_len, self.vocab_size)
        self.mapping = CharMapping(self.vocab_size)

        best_loss = float('inf')
        best_perm_state = None
        best_map_state = None

        # Get common sequence length from examples
        seq_len = len(self.examples[0][0]) if self.examples else 5

        # Try different permutation hypotheses
        perm_hypotheses = self._generate_perm_hypotheses(seq_len)

        for perm_init in perm_hypotheses:
            # Initialize permutation
            self.perm = CharPermutation(self.max_len, self.vocab_size)
            if perm_init is not None:
                self.perm.log_alpha.data = perm_init.clone()

            # Train mapping given this permutation
            self.mapping = CharMapping(self.vocab_size)
            map_opt = torch.optim.Adam(self.mapping.parameters(), lr=0.3)

            for step in range(200):
                map_opt.zero_grad()
                total_loss = 0.0

                for inp_str, out_str in self.examples:
                    inp = self.codec.encode_tensor(inp_str)
                    out = self.codec.encode_tensor(out_str)
                    if len(inp) != len(out):
                        continue

                    # Apply fixed permutation
                    perm_out = self.perm(inp, hard=True)
                    # Train mapping
                    pred = self.mapping(perm_out, hard=False)
                    out_onehot = F.one_hot(out, num_classes=self.vocab_size).float()
                    loss = F.mse_loss(pred, out_onehot)
                    total_loss += loss

                if total_loss.requires_grad:
                    total_loss.backward()
                    map_opt.step()

                if total_loss.item() < 0.01:
                    break

            # Evaluate this hypothesis
            preds = []
            for inp_str, _ in self.examples:
                inp = self.codec.encode_tensor(inp_str)
                perm_out = self.perm(inp, hard=True)
                map_out = self.mapping(perm_out, hard=True)
                preds.append(self.codec.decode(map_out.tolist()))

            loss = self._compute_loss(preds)
            if loss < best_loss:
                best_loss = loss
                best_perm_state = {k: v.clone() for k, v in self.perm.state_dict().items()}
                best_map_state = {k: v.clone() for k, v in self.mapping.state_dict().items()}

            if best_loss == 0.0:
                break  # Perfect, no need to try more

        # Restore best
        if best_perm_state is not None:
            self.perm.load_state_dict(best_perm_state)
        if best_map_state is not None:
            self.mapping.load_state_dict(best_map_state)

        # Evaluate with hard decisions
        preds = []
        for inp_str, _ in self.examples:
            inp = self.codec.encode_tensor(inp_str)
            perm_out = self.perm(inp, hard=True)
            inter_str = self.codec.decode(perm_out.tolist())
            inter = self.codec.encode_tensor(inter_str)
            map_out = self.mapping(inter, hard=True)
            preds.append(self.codec.decode(map_out.tolist()))

        loss = self._compute_loss(preds)
        dl = self.perm.description_length(len(self.examples[0][0])) + self.mapping.description_length()
        return loss, dl

    def _generate_perm_hypotheses(self, seq_len: int) -> List[Optional[torch.Tensor]]:
        """Generate common permutation initializations for given sequence length."""
        max_len = self.max_len
        hypotheses = []

        # Identity
        hypotheses.append(None)  # Will use default init (near identity)

        # Reverse - create full matrix but set reverse pattern for actual seq_len
        reverse_init = torch.zeros(max_len, max_len)
        for i in range(seq_len):
            reverse_init[i, seq_len - 1 - i] = 5.0  # Strong init toward reverse
        hypotheses.append(reverse_init)

        # Rotate left
        rotate_l = torch.zeros(max_len, max_len)
        for i in range(seq_len):
            rotate_l[i, (i + 1) % seq_len] = 5.0
        hypotheses.append(rotate_l)

        # Rotate right
        rotate_r = torch.zeros(max_len, max_len)
        for i in range(seq_len):
            rotate_r[i, (i - 1) % seq_len] = 5.0
        hypotheses.append(rotate_r)

        return hypotheses

    def train(self) -> str:
        """Train and select best configuration."""
        if not self.examples:
            return 'none'

        # Check library first for instant transfer
        if self.use_library:
            library = get_char_library()
            init = library.get_initialization(self.examples)
            if init is not None:
                # Found exact match - restore state and return immediately
                self.used_transfer = True
                self.train_steps = 1
                self.selected = init['config_type']
                self.scores[self.selected] = {'loss': 0.0, 'dl': 0.0, 'mdl': 0.0}

                if init['perm_state'] is not None:
                    self.perm = CharPermutation(self.max_len, self.vocab_size)
                    self.perm.load_state_dict(init['perm_state'])
                if init['map_state'] is not None:
                    self.mapping = CharMapping(self.vocab_size)
                    self.mapping.load_state_dict(init['map_state'])

                return self.selected

        # Try configurations
        # MDL = loss + lambda * description_length
        # Lambda should be small enough that low loss is preferred
        # Only use DL to break ties between configs with similar loss
        mdl_lambda = 0.001

        # Store state_dicts for each config so we can restore the best one
        saved_states = {}

        id_loss, id_dl = self._train_identity()
        self.scores['identity'] = {'loss': id_loss, 'dl': id_dl, 'mdl': id_loss + mdl_lambda * id_dl}
        saved_states['identity'] = (None, None)  # No learned params

        perm_loss, perm_dl = self._train_permutation()
        self.scores['permutation'] = {'loss': perm_loss, 'dl': perm_dl, 'mdl': perm_loss + mdl_lambda * perm_dl}
        saved_states['permutation'] = (
            {k: v.clone() for k, v in self.perm.state_dict().items()},
            None  # No mapping for permutation-only
        )

        map_loss, map_dl = self._train_mapping()
        self.scores['mapping'] = {'loss': map_loss, 'dl': map_dl, 'mdl': map_loss + mdl_lambda * map_dl}
        saved_states['mapping'] = (
            None,  # No perm for mapping-only
            {k: v.clone() for k, v in self.mapping.state_dict().items()}
        )

        comp_loss, comp_dl = self._train_composed()
        self.scores['composed'] = {'loss': comp_loss, 'dl': comp_dl, 'mdl': comp_loss + mdl_lambda * comp_dl}
        saved_states['composed'] = (
            {k: v.clone() for k, v in self.perm.state_dict().items()},
            {k: v.clone() for k, v in self.mapping.state_dict().items()}
        )

        # Select best - prefer lowest loss, use MDL for ties
        best = min(self.scores.keys(), key=lambda k: (self.scores[k]['loss'], self.scores[k]['mdl']))
        self.selected = best

        # Restore the state_dict for the selected config
        perm_state, map_state = saved_states[best]
        if perm_state is not None:
            self.perm = CharPermutation(self.max_len, self.vocab_size)
            self.perm.load_state_dict(perm_state)
        if map_state is not None:
            self.mapping = CharMapping(self.vocab_size)
            self.mapping.load_state_dict(map_state)

        # Save to library if successful
        if self.use_library and self.scores[best]['loss'] < 0.01:
            library = get_char_library()
            library.add(
                examples=self.examples,
                config_type=best,
                perm_state=perm_state,
                map_state=map_state,
                final_loss=self.scores[best]['loss']
            )

        return best

    def predict(self, input_str: str) -> str:
        """Predict using selected configuration."""
        if self.selected == 'identity':
            return input_str
        elif self.selected == 'permutation':
            inp = self.codec.encode_tensor(input_str)
            pred_idx = self.perm(inp, hard=True)
            return self.codec.decode(pred_idx.tolist())
        elif self.selected == 'mapping':
            inp = self.codec.encode_tensor(input_str)
            pred_idx = self.mapping(inp, hard=True)
            return self.codec.decode(pred_idx.tolist())
        elif self.selected == 'composed':
            inp = self.codec.encode_tensor(input_str)
            perm_out = self.perm(inp, hard=True)
            inter_str = self.codec.decode(perm_out.tolist())
            inter = self.codec.encode_tensor(inter_str)
            map_out = self.mapping(inter, hard=True)
            return self.codec.decode(map_out.tolist())
        else:
            return input_str


# =============================================================================
# Test Transforms
# =============================================================================

CHAR_TRANSFORMS = {
    # Identity
    'identity': lambda s: s,

    # Permutations
    'reverse': lambda s: s[::-1],
    'rotate_left': lambda s: s[1:] + s[0] if s else s,
    'rotate_right': lambda s: s[-1] + s[:-1] if s else s,

    # Character mappings
    'uppercase': lambda s: s.upper(),
    'lowercase': lambda s: s.lower(),
    'shift_1': lambda s: ''.join(chr(ord(c) + 1) if c.isalpha() else c for c in s),
    'swap_case': lambda s: s.swapcase(),

    # ROT13 (Caesar cipher)
    'rot13': lambda s: s.translate(str.maketrans(
        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM'
    )),

    # COMPOSED: permutation + mapping
    'reverse_upper': lambda s: s[::-1].upper(),
    'upper_reverse': lambda s: s.upper()[::-1],
    'rotate_upper': lambda s: (s[1:] + s[0]).upper() if s else s,
}


def test_char_transforms():
    """Test character-level transform learning."""
    print("=" * 70)
    print("LANGUAGE MDL - CHARACTER TRANSFORMS")
    print("=" * 70)
    print()

    # Use SAME LENGTH words for permutation-based transforms
    # 5-letter words covering diverse characters
    train_words = [
        'hello', 'world', 'quick', 'jumps', 'brown',
        'foxes', 'crazy', 'about', 'every', 'night',
        'abcde', 'fghij', 'klmno', 'pqrst', 'uvwxy'
    ]
    test_words = ['codes', 'datas', 'learn']

    results = {}

    for name, transform_fn in CHAR_TRANSFORMS.items():
        print(f"{name}:", end=" ", flush=True)

        system = CharTransformSystem(max_len=32)

        # Train on diverse examples
        for word in train_words:
            system.add_example(word, transform_fn(word))

        selected = system.train()

        # Test on held-out words
        correct = 0
        for word in test_words:
            pred = system.predict(word)
            expected = transform_fn(word)
            if pred == expected:
                correct += 1

        accuracy = correct / len(test_words)
        results[name] = {'selected': selected, 'accuracy': accuracy}

        loss = system.scores[selected]['loss']
        print(f"{correct}/{len(test_words)} ({accuracy*100:.0f}%) [{selected}] loss={loss:.3f}")

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    perm_transforms = ['identity', 'reverse', 'rotate_left', 'rotate_right']
    map_transforms = ['uppercase', 'lowercase', 'shift_1', 'swap_case', 'rot13']

    perm_acc = sum(results[t]['accuracy'] for t in perm_transforms) / len(perm_transforms)
    map_acc = sum(results[t]['accuracy'] for t in map_transforms) / len(map_transforms)
    overall = sum(r['accuracy'] for r in results.values()) / len(results)

    print(f"\nPermutation transforms: {perm_acc*100:.0f}%")
    print(f"Mapping transforms: {map_acc*100:.0f}%")
    print(f"Overall: {overall*100:.0f}%")

    print("\n" + "=" * 70)
    if overall >= 0.8:
        print("SUCCESS: ≥80% on character transforms!")
    else:
        print(f"Result: {overall*100:.0f}%")
        print("\nFailing transforms:")
        for name, r in results.items():
            if r['accuracy'] < 0.8:
                print(f"  {name}: {r['accuracy']*100:.0f}% [{r['selected']}]")
    print("=" * 70)

    return results


def test_transfer_learning():
    """Test transfer learning for character transforms."""
    print("\n" + "=" * 70)
    print("TRANSFER LEARNING TEST")
    print("=" * 70)

    # Reset library for clean test
    reset_char_library()

    transform_fn = lambda s: s[::-1].upper()  # reverse_upper

    # Training words (must include 'hello' for signature)
    # Need enough character diversity for mapping to generalize
    train_words = [
        'hello', 'world', 'quick', 'jumps', 'brown',
        'foxes', 'crazy', 'about', 'every', 'night',
        'abcde', 'fghij', 'klmno', 'pqrst', 'uvwxy'
    ]
    test_words = ['codes', 'datas', 'learn']

    # First run: cold start (no library)
    print("\n1. COLD START (no library)")
    import time
    start = time.time()
    system1 = CharTransformSystem(max_len=32, use_library=True)
    for word in train_words:
        system1.add_example(word, transform_fn(word))
    system1.train()
    cold_time = time.time() - start

    # Test accuracy
    correct = sum(1 for w in test_words if system1.predict(w) == transform_fn(w))
    print(f"   Selected: {system1.selected}")
    print(f"   Accuracy: {correct}/{len(test_words)}")
    print(f"   Time: {cold_time:.3f}s")
    print(f"   Used transfer: {system1.used_transfer}")

    # Check library
    library = get_char_library()
    print(f"   Library size: {library.stats()['size']}")

    # Second run: warm start (from library)
    print("\n2. WARM START (from library)")
    start = time.time()
    system2 = CharTransformSystem(max_len=32, use_library=True)
    for word in train_words:
        system2.add_example(word, transform_fn(word))
    system2.train()
    warm_time = time.time() - start

    # Test accuracy
    correct = sum(1 for w in test_words if system2.predict(w) == transform_fn(w))
    print(f"   Selected: {system2.selected}")
    print(f"   Accuracy: {correct}/{len(test_words)}")
    print(f"   Time: {warm_time:.3f}s")
    print(f"   Used transfer: {system2.used_transfer}")

    # Results
    speedup = cold_time / warm_time if warm_time > 0 else float('inf')
    print(f"\n3. RESULTS")
    print(f"   Cold time: {cold_time:.3f}s")
    print(f"   Warm time: {warm_time:.3f}s")
    print(f"   Speedup: {speedup:.0f}x")

    if system2.used_transfer and correct == len(test_words):
        print("\n   SUCCESS: Transfer learning working!")
    else:
        print("\n   FAIL: Transfer not working")

    # Cleanup
    reset_char_library()
    print("=" * 70)


if __name__ == '__main__':
    test_char_transforms()
    test_transfer_learning()
