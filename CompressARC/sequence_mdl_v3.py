#!/usr/bin/env python3
"""
SEQUENCE MDL V3 - Pointer Network Style

The key insight: for positional permutations (reverse, sort, rotate),
the transformation IS an attention pattern.

The latent should directly GENERATE the attention pattern,
not just modulate an existing one.

Architecture:
- Latent encodes a "permutation program"
- Permutation program generates position-to-position mappings
- Decoder applies the mapping to get output

This is closer to how ARCCompressor works - the latent
directly controls spatial transformations.
"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
import time
import math

np.random.seed(0)
torch.manual_seed(0)
torch.set_default_dtype(torch.float32)
torch.set_default_device('cpu')


@dataclass
class SequenceTask:
    """A sequence transformation task."""
    task_name: str
    train_pairs: List[Tuple[List[int], List[int]]]
    test_pairs: List[Tuple[List[int], List[int]]]
    vocab_size: int
    max_len: int


def make_task(name: str, pairs: List[Tuple[List[int], List[int]]], vocab_size: int = 12) -> SequenceTask:
    """Create a task from input/output pairs."""
    train = pairs[:-1]
    test = pairs[-1:]
    max_len = max(max(len(p[0]), len(p[1])) for p in pairs)
    return SequenceTask(name, train, test, vocab_size, max_len)


class SequenceMDLv3(nn.Module):
    """
    MDL with pointer-style attention.

    Key idea: The latent generates position queries that directly
    specify which input position each output position should copy from.

    This is explicit positional control - the latent IS the permutation.
    """

    def __init__(self, vocab_size: int, max_len: int,
                 d_model: int = 64, latent_dim: int = None):
        super().__init__()

        self.vocab_size = vocab_size
        self.max_len = max_len
        self.d_model = d_model

        # Latent dimension = max_len * max_len (soft permutation matrix)
        # This directly encodes which position maps to which
        if latent_dim is None:
            latent_dim = max_len * max_len
        self.latent_dim = latent_dim

        # Token embedding
        self.embed = nn.Embedding(vocab_size, d_model)

        # Position embedding for input
        self.pos_embed = nn.Embedding(max_len, d_model)

        # Latent = soft permutation matrix parameters
        # Initialize near identity (each output position attends to same input position)
        init_pattern = torch.eye(max_len).flatten()
        self.latent_mean = nn.Parameter(init_pattern * 2)  # Logits, so 2 gives ~0.9 prob on diagonal
        self.latent_logvar = nn.Parameter(torch.zeros(latent_dim) - 2)

        # Input processor
        self.input_encoder = nn.Sequential(
            nn.Linear(d_model, d_model),
            nn.LayerNorm(d_model),
            nn.GELU(),
            nn.Linear(d_model, d_model)
        )

        # Output head (from attended input to vocabulary)
        self.output_head = nn.Sequential(
            nn.Linear(d_model, d_model),
            nn.GELU(),
            nn.Linear(d_model, vocab_size)
        )

        # Collect weights
        self.weights_list = list(self.parameters())

    def sample_latent(self) -> Tuple[torch.Tensor, torch.Tensor]:
        """Sample permutation pattern from latent, compute KL."""
        std = torch.exp(0.5 * self.latent_logvar)
        eps = torch.randn_like(std)
        z = self.latent_mean + eps * std

        # KL from N(0,1)
        kl = -0.5 * torch.sum(1 + self.latent_logvar - self.latent_mean.pow(2) - self.latent_logvar.exp())
        return z, kl

    def forward(self, input_seq: torch.Tensor, target_len: int = None) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Forward pass.

        Args:
            input_seq: [batch, src_len] input tokens
            target_len: output length (defaults to input length)

        Returns:
            logits: [batch, tgt_len, vocab_size]
            kl: KL divergence
        """
        batch_size, src_len = input_seq.shape
        if target_len is None:
            target_len = src_len

        # Sample latent (the permutation pattern)
        z, kl = self.sample_latent()

        # Reshape to permutation matrix
        perm_logits = z.view(self.max_len, self.max_len)[:target_len, :src_len]

        # Softmax over source positions (each output position picks from input)
        perm_weights = F.softmax(perm_logits, dim=-1)  # [tgt_len, src_len]

        # Embed and encode input
        x = self.embed(input_seq)  # [batch, src_len, d_model]
        positions = torch.arange(src_len, device=input_seq.device)
        x = x + self.pos_embed(positions)
        x = self.input_encoder(x)  # [batch, src_len, d_model]

        # Apply permutation via weighted sum
        # perm_weights[i, j] = how much output position i attends to input position j
        x = x.transpose(0, 1)  # [src_len, batch, d_model]
        output = torch.einsum('ij,jbd->ibd', perm_weights, x)  # [tgt_len, batch, d_model]
        output = output.transpose(0, 1)  # [batch, tgt_len, d_model]

        # Project to vocabulary
        logits = self.output_head(output)

        return logits, kl

    def compute_loss(self, input_seq: torch.Tensor, target_seq: torch.Tensor,
                     kl_weight: float = 0.01) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Compute MDL loss."""
        logits, kl = self.forward(input_seq, target_seq.size(1))

        recon = F.cross_entropy(
            logits.view(-1, self.vocab_size),
            target_seq.view(-1),
            reduction='sum'
        )

        total = kl_weight * kl + recon
        return total, kl, recon

    def predict(self, input_seq: torch.Tensor) -> torch.Tensor:
        """Predict output sequence."""
        self.eval()
        with torch.no_grad():
            logits, _ = self.forward(input_seq)
            return logits.argmax(dim=-1)

    def get_permutation(self) -> torch.Tensor:
        """Get the learned permutation matrix (for visualization)."""
        with torch.no_grad():
            perm_logits = self.latent_mean.view(self.max_len, self.max_len)
            return F.softmax(perm_logits, dim=-1)


class SequenceLibraryV3:
    """Library for transfer learning."""
    def __init__(self):
        self.entries = {}

    def add(self, name: str, weights: List[torch.Tensor], steps: int):
        self.entries[name] = {'weights': weights, 'steps': steps}

    def get_best(self) -> Optional[Dict]:
        if not self.entries:
            return None
        return min(self.entries.values(), key=lambda e: e['steps'])


def pad(seq: List[int], max_len: int) -> List[int]:
    """Pad sequence to max_len."""
    return seq + [0] * (max_len - len(seq))


def solve_task(task: SequenceTask, library: SequenceLibraryV3 = None,
               max_steps: int = 500, target_loss: float = 5.0,
               verbose: bool = True) -> Dict:
    """Solve a sequence task with MDL v3."""

    model = SequenceMDLv3(task.vocab_size, task.max_len)

    # Transfer weights if available
    transferred = 0
    if library:
        entry = library.get_best()
        if entry:
            for src, tgt in zip(entry['weights'], model.weights_list):
                if src.shape == tgt.shape:
                    tgt.data.copy_(src.data)
                    transferred += 1

    optimizer = torch.optim.Adam(model.parameters(), lr=0.02, betas=(0.9, 0.99))

    # Prepare data
    inputs = torch.tensor([pad(p[0], task.max_len) for p in task.train_pairs], dtype=torch.long)
    targets = torch.tensor([pad(p[1], task.max_len) for p in task.train_pairs], dtype=torch.long)

    # Train
    start = time.time()
    solved = False

    for step in range(max_steps):
        optimizer.zero_grad()
        loss, kl, recon = model.compute_loss(inputs, targets)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()

        if loss.item() < target_loss:
            solved = True
            break

    elapsed = time.time() - start

    # Test
    test_in = torch.tensor([pad(task.test_pairs[0][0], task.max_len)], dtype=torch.long)
    pred = model.predict(test_in)[0].tolist()
    expected = task.test_pairs[0][1]
    pred_trimmed = pred[:len(expected)]
    correct = pred_trimmed == expected

    if verbose:
        transfer_str = f" (transferred {transferred})" if transferred else " (scratch)"
        print(f"  {step+1} steps, {elapsed:.1f}s{transfer_str}")
        print(f"  Loss: {loss.item():.2f}, Correct: {correct}")
        if not correct:
            print(f"  Pred: {pred_trimmed}")
            print(f"  Exp:  {expected}")

        # Show learned permutation for first task
        if verbose and step < 100:
            perm = model.get_permutation()[:5, :5]
            print(f"  Permutation pattern (5x5):")
            for i in range(5):
                row = [f"{perm[i,j].item():.2f}" for j in range(5)]
                print(f"    {row}")

    return {
        'task_name': task.task_name,
        'solved': solved,
        'steps': step + 1,
        'loss': loss.item(),
        'time': elapsed,
        'correct': correct,
        'transferred': transferred,
        'weights': [w.detach().clone() for w in model.weights_list]
    }


# =============================================================================
# TEST TASKS
# =============================================================================

def make_reverse_tasks(n: int = 5, length: int = 5, n_examples: int = 20) -> List[SequenceTask]:
    """Reversal tasks with more examples for pattern learning."""
    tasks = []
    for i in range(n):
        np.random.seed(i + 100)
        pairs = []
        for _ in range(n_examples):
            seq = list(np.random.randint(1, 10, size=length))
            pairs.append((seq, seq[::-1]))
        tasks.append(make_task(f"reverse_{i}", pairs))
    return tasks


def make_sort_tasks(n: int = 5, length: int = 5, n_examples: int = 20) -> List[SequenceTask]:
    """Sorting tasks."""
    tasks = []
    for i in range(n):
        np.random.seed(i + 200)
        pairs = []
        for _ in range(n_examples):
            seq = list(np.random.randint(1, 10, size=length))
            pairs.append((seq, sorted(seq)))
        tasks.append(make_task(f"sort_{i}", pairs))
    return tasks


def make_rotate_tasks(n: int = 5, length: int = 5, k: int = 2, n_examples: int = 20) -> List[SequenceTask]:
    """Rotate sequence by k positions."""
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


def make_identity_tasks(n: int = 5, length: int = 5, n_examples: int = 20) -> List[SequenceTask]:
    """Identity (copy) tasks - baseline."""
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
    print("SEQUENCE MDL V3 - POINTER NETWORK STYLE")
    print("=" * 60)
    print("Testing if explicit permutation latent works for:")
    print("  - Identity (baseline)")
    print("  - Reverse")
    print("  - Rotate")
    print()

    # Start with simpler tasks to verify architecture
    print("\n" + "=" * 60)
    print("[IDENTITY - Baseline]")
    print("=" * 60)

    identity_tasks = make_identity_tasks(3)
    for i, task in enumerate(identity_tasks):
        print(f"\n[{i+1}/3] {task.task_name}")
        print(f"  Example: {task.train_pairs[0][0]} -> {task.train_pairs[0][1]}")
        result = solve_task(task, verbose=True)

    print("\n" + "=" * 60)
    print("[REVERSE]")
    print("=" * 60)

    library = SequenceLibraryV3()
    reverse_tasks = make_reverse_tasks(5)
    reverse_results = []

    for i, task in enumerate(reverse_tasks):
        print(f"\n[{i+1}/5] {task.task_name}")
        print(f"  Example: {task.train_pairs[0][0]} -> {task.train_pairs[0][1]}")

        result = solve_task(task, library if i > 0 else None, verbose=True)

        if result['correct']:
            library.add(task.task_name, result['weights'], result['steps'])

        reverse_results.append(result)

    # Summary
    correct = sum(r['correct'] for r in reverse_results)
    print(f"\nREVERSE Summary: {correct}/5 correct")
    print("Learning curve:", [r['steps'] for r in reverse_results])

    print("\n" + "=" * 60)
    print("[ROTATE]")
    print("=" * 60)

    rotate_library = SequenceLibraryV3()
    rotate_tasks = make_rotate_tasks(5, k=2)
    rotate_results = []

    for i, task in enumerate(rotate_tasks):
        print(f"\n[{i+1}/5] {task.task_name}")
        print(f"  Example: {task.train_pairs[0][0]} -> {task.train_pairs[0][1]}")

        result = solve_task(task, rotate_library if i > 0 else None, verbose=True)

        if result['correct']:
            rotate_library.add(task.task_name, result['weights'], result['steps'])

        rotate_results.append(result)

    correct = sum(r['correct'] for r in rotate_results)
    print(f"\nROTATE Summary: {correct}/5 correct")
    print("Learning curve:", [r['steps'] for r in rotate_results])
