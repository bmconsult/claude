#!/usr/bin/env python3
"""
SEQUENCE MDL - Minimal Description Length for Sequences

A simpler, more faithful MDL implementation for sequences.

Key insight: The latent must encode the ENTIRE transformation rule.
The decoder should just apply the rule, not learn to memorize.

Architecture:
- Latent: represents the transformation (like a "program")
- Decoder: applies latent to input to produce output
- Loss: KL (program complexity) + reconstruction (program correctness)

This is closer to how ARCCompressor works.
"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Tuple, Dict
from dataclasses import dataclass
import time

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


def make_task(name: str, pairs: List[Tuple[List[int], List[int]]], vocab_size: int = 10) -> SequenceTask:
    """Create a task from input/output pairs."""
    train = pairs[:-1]
    test = pairs[-1:]
    max_len = max(max(len(p[0]), len(p[1])) for p in pairs)
    return SequenceTask(name, train, test, vocab_size, max_len)


class SequenceMDL(nn.Module):
    """
    Minimal MDL for sequences.

    The key is: latent encodes the rule, decoder just applies it.
    Similar to ARCCompressor where multiposteriors encode the solution.
    """

    def __init__(self, vocab_size: int, max_len: int, latent_dim: int = 64, hidden_dim: int = 128):
        super().__init__()

        self.vocab_size = vocab_size
        self.max_len = max_len
        self.latent_dim = latent_dim
        self.hidden_dim = hidden_dim

        # Token embedding
        self.embed = nn.Embedding(vocab_size, hidden_dim)

        # Latent = the "rule" or "program"
        # This is like multiposteriors in ARCCompressor
        self.latent_mean = nn.Parameter(torch.randn(latent_dim) * 0.1)
        self.latent_logvar = nn.Parameter(torch.zeros(latent_dim) - 2)  # Start with low variance

        # Decoder: applies latent to embedded input
        # Simple MLP that transforms each position using the latent
        self.decoder = nn.Sequential(
            nn.Linear(hidden_dim + latent_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, vocab_size)
        )

        # Position-aware transformation
        self.pos_embed = nn.Embedding(max_len, hidden_dim)

        # Collect weights for transfer
        self.weights_list = list(self.parameters())

    def sample_latent(self) -> Tuple[torch.Tensor, torch.Tensor]:
        """Sample latent and compute KL divergence."""
        std = torch.exp(0.5 * self.latent_logvar)
        eps = torch.randn_like(std)
        z = self.latent_mean + eps * std

        # KL from N(0,1)
        kl = -0.5 * torch.sum(1 + self.latent_logvar - self.latent_mean.pow(2) - self.latent_logvar.exp())

        return z, kl

    def forward(self, input_seq: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Transform input sequence using the learned latent rule.

        Args:
            input_seq: [batch, seq_len] token indices

        Returns:
            logits: [batch, seq_len, vocab_size]
            kl: KL divergence
        """
        batch_size, seq_len = input_seq.shape

        # Sample latent (the "rule")
        z, kl = self.sample_latent()

        # Embed input
        x = self.embed(input_seq)  # [batch, seq_len, hidden]

        # Add position info
        positions = torch.arange(seq_len, device=input_seq.device)
        x = x + self.pos_embed(positions)

        # Apply latent to each position
        # Broadcast latent across batch and sequence
        z_expanded = z.unsqueeze(0).unsqueeze(0).expand(batch_size, seq_len, -1)
        x_with_latent = torch.cat([x, z_expanded], dim=-1)

        # Decode to output tokens
        logits = self.decoder(x_with_latent)

        return logits, kl

    def compute_loss(self, inputs: torch.Tensor, targets: torch.Tensor,
                     kl_weight: float = 0.1) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Compute MDL loss = KL + reconstruction."""
        logits, kl = self.forward(inputs)

        recon = F.cross_entropy(
            logits.view(-1, self.vocab_size),
            targets.view(-1),
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


def pad_sequence(seq: List[int], max_len: int, pad_val: int = 0) -> List[int]:
    """Pad sequence to max_len."""
    return seq + [pad_val] * (max_len - len(seq))


def solve_task(task: SequenceTask, max_steps: int = 300,
               target_loss: float = 5.0, verbose: bool = True) -> Dict:
    """
    Solve a sequence task using MDL.
    """
    model = SequenceMDL(task.vocab_size, task.max_len)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.02, betas=(0.5, 0.9))

    # Prepare training data
    inputs = torch.tensor([pad_sequence(p[0], task.max_len) for p in task.train_pairs], dtype=torch.long)
    targets = torch.tensor([pad_sequence(p[1], task.max_len) for p in task.train_pairs], dtype=torch.long)

    # Training loop
    start_time = time.time()
    solved = False
    step = 0

    for step in range(max_steps):
        optimizer.zero_grad()
        loss, kl, recon = model.compute_loss(inputs, targets)
        loss.backward()
        optimizer.step()

        if loss.item() < target_loss:
            solved = True
            break

    elapsed = time.time() - start_time

    # Test
    test_in = torch.tensor([pad_sequence(task.test_pairs[0][0], task.max_len)], dtype=torch.long)
    prediction = model.predict(test_in)[0].tolist()
    expected = task.test_pairs[0][1]

    # Trim to expected length
    prediction = prediction[:len(expected)]
    correct = prediction == expected

    if verbose:
        print(f"  {step + 1} steps, {elapsed:.1f}s")
        print(f"  Loss: {loss.item():.2f} (KL: {kl.item():.2f}, Recon: {recon.item():.2f})")
        print(f"  Input:    {task.test_pairs[0][0]}")
        print(f"  Predict:  {prediction}")
        print(f"  Expected: {expected}")
        print(f"  Correct:  {correct}")

    return {
        'task_name': task.task_name,
        'solved': solved and correct,
        'steps': step + 1,
        'loss': loss.item(),
        'time': elapsed,
        'correct': correct,
        'weights': [w.detach().clone() for w in model.weights_list]
    }


# =============================================================================
# TRANSFER LEARNING
# =============================================================================

class SequenceLibrary:
    """Library of learned sequence transformations for transfer."""

    def __init__(self):
        self.entries = {}

    def add(self, task_name: str, weights: List[torch.Tensor], steps: int):
        self.entries[task_name] = {
            'weights': weights,
            'steps': steps
        }

    def get_best(self):
        """Get entry with lowest steps (best learned)."""
        if not self.entries:
            return None
        return min(self.entries.values(), key=lambda e: e['steps'])


def solve_with_transfer(task: SequenceTask, library: SequenceLibrary,
                        max_steps: int = 300, verbose: bool = True) -> Dict:
    """Solve task with transfer from library."""
    model = SequenceMDL(task.vocab_size, task.max_len)

    # Try to transfer weights
    entry = library.get_best()
    transferred = 0
    transfer_from = None

    if entry:
        for src_w, tgt_w in zip(entry['weights'], model.weights_list):
            if src_w.shape == tgt_w.shape:
                tgt_w.data.copy_(src_w.data)
                transferred += 1
        transfer_from = "library"

        if verbose:
            pct = 100 * transferred / len(model.weights_list)
            print(f"  Transferred {pct:.1f}% weights from library")

    optimizer = torch.optim.Adam(model.parameters(), lr=0.02, betas=(0.5, 0.9))

    # Prepare training data
    inputs = torch.tensor([pad_sequence(p[0], task.max_len) for p in task.train_pairs], dtype=torch.long)
    targets = torch.tensor([pad_sequence(p[1], task.max_len) for p in task.train_pairs], dtype=torch.long)

    # Training loop
    start_time = time.time()
    solved = False
    step = 0

    for step in range(max_steps):
        optimizer.zero_grad()
        loss, kl, recon = model.compute_loss(inputs, targets)
        loss.backward()
        optimizer.step()

        if loss.item() < 5.0:
            solved = True
            break

    elapsed = time.time() - start_time

    # Test
    test_in = torch.tensor([pad_sequence(task.test_pairs[0][0], task.max_len)], dtype=torch.long)
    prediction = model.predict(test_in)[0].tolist()
    expected = task.test_pairs[0][1]
    prediction = prediction[:len(expected)]
    correct = prediction == expected

    if verbose:
        print(f"  {step + 1} steps, {elapsed:.1f}s")
        print(f"  Correct: {correct}")

    return {
        'task_name': task.task_name,
        'solved': solved and correct,
        'steps': step + 1,
        'loss': loss.item(),
        'time': elapsed,
        'correct': correct,
        'transfer_from': transfer_from,
        'weights': [w.detach().clone() for w in model.weights_list]
    }


# =============================================================================
# TEST TASKS
# =============================================================================

def make_identity_tasks(n: int = 5) -> List[SequenceTask]:
    """Identity/copy tasks."""
    tasks = []
    for i in range(n):
        np.random.seed(i)
        pairs = []
        for _ in range(4):
            seq = list(np.random.randint(1, 10, size=5))
            pairs.append((seq, seq.copy()))
        tasks.append(make_task(f"identity_{i}", pairs))
    return tasks


def make_reverse_tasks(n: int = 5) -> List[SequenceTask]:
    """Reversal tasks."""
    tasks = []
    for i in range(n):
        np.random.seed(i + 100)
        pairs = []
        for _ in range(4):
            seq = list(np.random.randint(1, 10, size=5))
            pairs.append((seq, seq[::-1]))
        tasks.append(make_task(f"reverse_{i}", pairs))
    return tasks


def make_increment_tasks(n: int = 5) -> List[SequenceTask]:
    """Increment each element by 1."""
    tasks = []
    for i in range(n):
        np.random.seed(i + 200)
        pairs = []
        for _ in range(4):
            seq = list(np.random.randint(1, 8, size=5))
            pairs.append((seq, [x + 1 for x in seq]))
        tasks.append(make_task(f"increment_{i}", pairs))
    return tasks


if __name__ == "__main__":
    print("=" * 60)
    print("SEQUENCE MDL - TRANSFER LEARNING TEST")
    print("=" * 60)
    print("Testing if sequence transfer works like grid transfer...")
    print()

    # Create tasks of the same type
    tasks = make_increment_tasks(10)

    library = SequenceLibrary()
    results = []

    for i, task in enumerate(tasks):
        print(f"\n[{i+1}/10] {task.task_name}")
        print(f"  Rule: increment each element by 1")
        print(f"  Example: {task.train_pairs[0][0]} -> {task.train_pairs[0][1]}")

        if i == 0:
            # First task: no transfer
            result = solve_task(task, verbose=True)
        else:
            # Subsequent: use transfer
            result = solve_with_transfer(task, library, verbose=True)

        # Add to library if solved
        if result['solved']:
            library.add(task.task_name, result['weights'], result['steps'])

        results.append(result)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Solved: {sum(r['solved'] for r in results)}/{len(results)}")
    print(f"Correct: {sum(r['correct'] for r in results)}/{len(results)}")

    print("\nLearning curve (steps):")
    for i, r in enumerate(results):
        bar = "#" * min(r['steps'], 50)
        transfer = "TRANSFER" if r.get('transfer_from') else "SCRATCH"
        print(f"  Task {i+1}: {r['steps']:3d} steps ({transfer}) {bar}")
