#!/usr/bin/env python3
"""
SEQUENCE MDL V4 - Operation Selection (like ARC)

Key insight: ARC Compressor works because it has DISCRETE operations
(cummax, shift, etc.) and the latent SELECTS which to apply.

This version:
- Has a library of discrete sequence operations
- Latent selects/combines operations
- This is program synthesis, not soft permutation learning

Operations:
- identity: x -> x
- reverse: x -> x[::-1]
- rotate_k: x -> x[k:] + x[:k]
- sort_asc: x -> sorted(x)
- sort_desc: x -> sorted(x, reverse=True)
"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Tuple, Dict, Callable
from dataclasses import dataclass
import time

np.random.seed(42)
torch.manual_seed(42)


@dataclass
class SequenceTask:
    task_name: str
    train_pairs: List[Tuple[List[int], List[int]]]
    test_pairs: List[Tuple[List[int], List[int]]]
    vocab_size: int
    max_len: int


def make_task(name: str, pairs: List[Tuple[List[int], List[int]]], vocab_size: int = 12) -> SequenceTask:
    train = pairs[:-1]
    test = pairs[-1:]
    max_len = max(max(len(p[0]), len(p[1])) for p in pairs)
    return SequenceTask(name, train, test, vocab_size, max_len)


# =============================================================================
# OPERATION LIBRARY
# =============================================================================

def op_identity(x: torch.Tensor) -> torch.Tensor:
    """Identity: x -> x"""
    return x.clone()


def op_reverse(x: torch.Tensor) -> torch.Tensor:
    """Reverse: x -> x[::-1]"""
    return x.flip(dims=[-1])


def make_rotate(k: int) -> Callable:
    """Create rotate-by-k operation."""
    def op_rotate(x: torch.Tensor) -> torch.Tensor:
        return torch.roll(x, shifts=-k, dims=-1)
    return op_rotate


def op_sort_asc(x: torch.Tensor) -> torch.Tensor:
    """Sort ascending."""
    return torch.sort(x, dim=-1)[0]


def op_sort_desc(x: torch.Tensor) -> torch.Tensor:
    """Sort descending."""
    return torch.sort(x, dim=-1, descending=True)[0]


# Build operation library
OPERATIONS = {
    'identity': op_identity,
    'reverse': op_reverse,
    'rotate_1': make_rotate(1),
    'rotate_2': make_rotate(2),
    'rotate_3': make_rotate(3),
    'rotate_-1': make_rotate(-1),
    'rotate_-2': make_rotate(-2),
    'sort_asc': op_sort_asc,
    'sort_desc': op_sort_desc,
}

OP_NAMES = list(OPERATIONS.keys())
N_OPS = len(OP_NAMES)


class SequenceMDLv4(nn.Module):
    """
    MDL with operation selection.

    The latent is a distribution over discrete operations.
    Like ARC Compressor, we have hardcoded ops and learned selection.
    """

    def __init__(self, vocab_size: int, max_len: int, d_model: int = 64):
        super().__init__()

        self.vocab_size = vocab_size
        self.max_len = max_len
        self.d_model = d_model
        self.n_ops = N_OPS

        # Latent = log-probabilities over operations
        # Initialized uniform
        self.op_logits = nn.Parameter(torch.zeros(N_OPS))

        # Token embedding for input encoding
        self.embed = nn.Embedding(vocab_size, d_model)

        # Small encoder to process examples
        self.encoder = nn.Sequential(
            nn.Linear(d_model * max_len, d_model),
            nn.GELU(),
            nn.Linear(d_model, N_OPS)
        )

    def encode_examples(self, inputs: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        """Encode training examples to infer operation."""
        batch_size = inputs.size(0)

        # Embed and flatten
        x = self.embed(inputs)  # [batch, len, d_model]
        x = x.view(batch_size, -1)  # [batch, len * d_model]

        # Infer operation from examples
        logits = self.encoder(x)  # [batch, n_ops]

        # Average over examples
        logits = logits.mean(dim=0)  # [n_ops]

        return logits

    def forward(self, inputs: torch.Tensor, targets: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Forward pass: select operation based on examples.

        Returns:
            predictions: [batch, len] predicted tokens
            op_probs: [n_ops] operation probabilities
        """
        # Infer operation from training examples
        op_logits = self.encode_examples(inputs, targets)

        # Softmax to get operation probabilities
        op_probs = F.softmax(op_logits, dim=-1)

        # Apply each operation and blend by probability
        # (Soft selection - allows gradients to flow)
        batch_size, seq_len = inputs.shape
        predictions = torch.zeros(batch_size, seq_len, dtype=torch.float, device=inputs.device)

        for i, (name, op) in enumerate(OPERATIONS.items()):
            op_output = op(inputs.float())  # Apply operation
            predictions = predictions + op_probs[i] * op_output

        return predictions, op_probs

    def compute_loss(self, inputs: torch.Tensor, targets: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Compute reconstruction loss."""
        predictions, op_probs = self.forward(inputs, targets)

        # MSE loss (since we're blending)
        loss = F.mse_loss(predictions, targets.float())

        # KL from uniform prior (encourages using all ops equally by default)
        prior = torch.ones(self.n_ops, device=inputs.device) / self.n_ops
        kl = F.kl_div(op_probs.log(), prior, reduction='sum')

        total = loss + 0.01 * kl
        return total, op_probs

    def predict(self, input_seq: torch.Tensor, train_inputs: torch.Tensor, train_targets: torch.Tensor) -> torch.Tensor:
        """Predict using inferred operation."""
        # First infer the operation from training examples
        op_logits = self.encode_examples(train_inputs, train_targets)
        op_probs = F.softmax(op_logits, dim=-1)

        # Select the most likely operation
        best_op_idx = op_probs.argmax().item()
        best_op_name = OP_NAMES[best_op_idx]
        best_op = OPERATIONS[best_op_name]

        # Apply it
        return best_op(input_seq).long(), best_op_name, op_probs


class SequenceLibraryV4:
    """Library for transfer learning."""
    def __init__(self):
        self.entries = {}

    def add(self, name: str, state_dict: dict, steps: int, op_name: str):
        self.entries[name] = {'state': state_dict, 'steps': steps, 'op': op_name}

    def get_best(self):
        if not self.entries:
            return None
        return min(self.entries.values(), key=lambda e: e['steps'])


def pad_seq(seq: List[int], max_len: int) -> List[int]:
    return seq + [0] * (max_len - len(seq))


def solve_task(task: SequenceTask, library: SequenceLibraryV4 = None,
               max_steps: int = 200, target_loss: float = 0.01,
               verbose: bool = True) -> Dict:
    """Solve a sequence task."""

    model = SequenceMDLv4(task.vocab_size, task.max_len)

    # Transfer if available
    if library:
        entry = library.get_best()
        if entry:
            model.load_state_dict(entry['state'])

    optimizer = torch.optim.Adam(model.parameters(), lr=0.05)

    # Prepare data
    inputs = torch.tensor([pad_seq(p[0], task.max_len) for p in task.train_pairs], dtype=torch.long)
    targets = torch.tensor([pad_seq(p[1], task.max_len) for p in task.train_pairs], dtype=torch.long)

    # Train
    start = time.time()
    solved = False

    for step in range(max_steps):
        optimizer.zero_grad()
        loss, op_probs = model.compute_loss(inputs, targets)
        loss.backward()
        optimizer.step()

        if loss.item() < target_loss:
            solved = True
            break

    elapsed = time.time() - start

    # Test
    test_in = torch.tensor([pad_seq(task.test_pairs[0][0], task.max_len)], dtype=torch.long)
    pred, op_name, op_probs = model.predict(test_in, inputs, targets)
    pred = pred[0].tolist()
    expected = task.test_pairs[0][1]
    pred_trimmed = pred[:len(expected)]
    correct = pred_trimmed == expected

    if verbose:
        transfer_str = " (transferred)" if library and library.get_best() else " (scratch)"
        print(f"  {step+1} steps, {elapsed:.1f}s{transfer_str}")
        print(f"  Loss: {loss.item():.4f}, Selected op: {op_name}")
        print(f"  Op probs: {', '.join(f'{OP_NAMES[i]}:{op_probs[i].item():.2f}' for i in range(N_OPS))}")
        print(f"  Correct: {correct}")
        if not correct:
            print(f"  Pred: {pred_trimmed}")
            print(f"  Exp:  {expected}")

    return {
        'task_name': task.task_name,
        'steps': step + 1,
        'loss': loss.item(),
        'time': elapsed,
        'correct': correct,
        'op_name': op_name,
        'state': model.state_dict()
    }


# =============================================================================
# TEST TASKS
# =============================================================================

def make_reverse_tasks(n: int = 5, length: int = 5, n_examples: int = 10) -> List[SequenceTask]:
    tasks = []
    for i in range(n):
        np.random.seed(i + 100)
        pairs = []
        for _ in range(n_examples):
            seq = list(np.random.randint(1, 10, size=length))
            pairs.append((seq, seq[::-1]))
        tasks.append(make_task(f"reverse_{i}", pairs))
    return tasks


def make_rotate_tasks(n: int = 5, length: int = 5, k: int = 2, n_examples: int = 10) -> List[SequenceTask]:
    tasks = []
    for i in range(n):
        np.random.seed(i + 300)
        pairs = []
        for _ in range(n_examples):
            seq = list(np.random.randint(1, 10, size=length))
            rotated = seq[k:] + seq[:k]
            pairs.append((seq, rotated))
        tasks.append(make_task(f"rotate_{k}_{i}", pairs))
    return tasks


def make_sort_tasks(n: int = 5, length: int = 5, n_examples: int = 10) -> List[SequenceTask]:
    tasks = []
    for i in range(n):
        np.random.seed(i + 200)
        pairs = []
        for _ in range(n_examples):
            seq = list(np.random.randint(1, 10, size=length))
            pairs.append((seq, sorted(seq)))
        tasks.append(make_task(f"sort_{i}", pairs))
    return tasks


def make_identity_tasks(n: int = 5, length: int = 5, n_examples: int = 10) -> List[SequenceTask]:
    tasks = []
    for i in range(n):
        np.random.seed(i + 400)
        pairs = []
        for _ in range(n_examples):
            seq = list(np.random.randint(1, 10, size=length))
            pairs.append((seq, seq.copy()))
        tasks.append(make_task(f"identity_{i}", pairs))
    return tasks


if __name__ == "__main__":
    print("=" * 60)
    print("SEQUENCE MDL V4 - OPERATION SELECTION")
    print("=" * 60)
    print(f"Operations available: {OP_NAMES}")
    print()

    # Test each task type
    for task_type, task_fn, expected_op in [
        ("IDENTITY", make_identity_tasks, "identity"),
        ("REVERSE", make_reverse_tasks, "reverse"),
        ("ROTATE-2", lambda: make_rotate_tasks(k=2), "rotate_2"),
        ("SORT", make_sort_tasks, "sort_asc"),
    ]:
        print("\n" + "=" * 60)
        print(f"[{task_type}] - Expected operation: {expected_op}")
        print("=" * 60)

        tasks = task_fn() if callable(task_fn) else task_fn
        library = SequenceLibraryV4()
        results = []

        for i, task in enumerate(tasks[:5]):
            print(f"\n[{i+1}/5] {task.task_name}")
            print(f"  Example: {task.train_pairs[0][0]} -> {task.train_pairs[0][1]}")

            result = solve_task(task, library if i > 0 else None, verbose=True)

            if result['correct']:
                library.add(task.task_name, result['state'], result['steps'], result['op_name'])

            results.append(result)

        correct = sum(r['correct'] for r in results)
        print(f"\n{task_type} Summary: {correct}/5 correct")
        print("Learning curve:", [r['steps'] for r in results])
        ops_used = [r['op_name'] for r in results]
        print(f"Operations selected: {ops_used}")
