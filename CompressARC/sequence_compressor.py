#!/usr/bin/env python3
"""
SEQUENCE COMPRESSOR - Learning-Based (Like ARCCompressor)

This is a proper learning-based sequence transformation system.
NOT enumeration - actual neural network learning.

Key insight from ARCCompressor:
- cummax and shift are DIFFERENTIABLE positional primitives
- The network LEARNS which operations to apply via gradient descent
- Transfer learning works because most weights are task-independent

Architecture:
- Latent posterior (the "program" being learned)
- Decoder with positional primitives:
  - cummax (propagate info left-to-right or right-to-left)
  - shift (move elements left or right)
  - flip (reverse for bidirectional processing)
- MDL loss: KL + reconstruction

This should generalize to NOVEL transforms, not just in-library ones.
"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Tuple, Dict, Optional
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


# =============================================================================
# DIFFERENTIABLE POSITIONAL PRIMITIVES
# =============================================================================

def cummax_left(x: torch.Tensor) -> torch.Tensor:
    """Cumulative maximum from left to right along last dimension."""
    return torch.cummax(x, dim=-1)[0]


def cummax_right(x: torch.Tensor) -> torch.Tensor:
    """Cumulative maximum from right to left along last dimension."""
    return torch.flip(torch.cummax(torch.flip(x, dims=[-1]), dim=-1)[0], dims=[-1])


def cumsum_left(x: torch.Tensor) -> torch.Tensor:
    """Cumulative sum from left to right."""
    return torch.cumsum(x, dim=-1)


def cumsum_right(x: torch.Tensor) -> torch.Tensor:
    """Cumulative sum from right to left."""
    return torch.flip(torch.cumsum(torch.flip(x, dims=[-1]), dim=-1), dims=[-1])


def shift_left(x: torch.Tensor, fill: float = 0.0) -> torch.Tensor:
    """Shift elements left by 1, pad right with fill."""
    return F.pad(x[..., 1:], (0, 1), value=fill)


def shift_right(x: torch.Tensor, fill: float = 0.0) -> torch.Tensor:
    """Shift elements right by 1, pad left with fill."""
    return F.pad(x[..., :-1], (1, 0), value=fill)


def flip_seq(x: torch.Tensor) -> torch.Tensor:
    """Reverse the sequence."""
    return torch.flip(x, dims=[-1])


# =============================================================================
# SEQUENCE COMPRESSOR MODEL
# =============================================================================

class SequenceCompressor(nn.Module):
    """
    MDL-based sequence compressor with learnable positional operations.

    Like ARCCompressor but for 1D sequences:
    - Latent encodes the "program"
    - Decoder applies positional primitives
    - Network learns WHICH operations to apply
    """

    def __init__(self, vocab_size: int, max_len: int,
                 d_model: int = 64, latent_dim: int = 32, n_layers: int = 4):
        super().__init__()

        self.vocab_size = vocab_size
        self.max_len = max_len
        self.d_model = d_model
        self.latent_dim = latent_dim
        self.n_layers = n_layers

        # Token embedding
        self.embed = nn.Embedding(vocab_size, d_model)

        # Position embedding
        self.pos_embed = nn.Embedding(max_len, d_model)

        # Latent posterior (the "program" being learned)
        # Separate latent per sequence position would allow position-dependent transforms
        self.latent_mean = nn.Parameter(torch.randn(latent_dim) * 0.1)
        self.latent_logvar = nn.Parameter(torch.zeros(latent_dim) - 2)

        # Decoder: latent -> initial hidden state
        self.decode_latent = nn.Linear(latent_dim, d_model)

        # Layers with positional primitives
        # Each layer has:
        # - Learned weights for cummax_left/right combination
        # - Learned weights for shift_left/right combination
        # - Nonlinear mixing

        self.cummax_weights = nn.ParameterList([
            nn.Parameter(torch.zeros(4))  # [cummax_L, cummax_R, cumsum_L, cumsum_R]
            for _ in range(n_layers)
        ])

        self.shift_weights = nn.ParameterList([
            nn.Parameter(torch.zeros(3))  # [identity, shift_L, shift_R]
            for _ in range(n_layers)
        ])

        self.flip_weights = nn.ParameterList([
            nn.Parameter(torch.zeros(2))  # [identity, flip]
            for _ in range(n_layers)
        ])

        # Mixing MLPs per layer
        self.layer_mlps = nn.ModuleList([
            nn.Sequential(
                nn.Linear(d_model * 2, d_model),  # Combine input info with position ops
                nn.LayerNorm(d_model),
                nn.GELU(),
                nn.Linear(d_model, d_model),
            )
            for _ in range(n_layers)
        ])

        # Output head
        self.output_head = nn.Sequential(
            nn.Linear(d_model, d_model),
            nn.GELU(),
            nn.Linear(d_model, vocab_size)
        )

        # Collect all weights for transfer
        self.weights_list = list(self.parameters())

    def sample_latent(self) -> Tuple[torch.Tensor, torch.Tensor]:
        """Sample from latent posterior, compute KL."""
        std = torch.exp(0.5 * self.latent_logvar)
        eps = torch.randn_like(std)
        z = self.latent_mean + eps * std

        # KL from N(0, I)
        kl = -0.5 * torch.sum(1 + self.latent_logvar - self.latent_mean.pow(2) - self.latent_logvar.exp())
        return z, kl

    def apply_positional_ops(self, x: torch.Tensor, layer: int) -> torch.Tensor:
        """Apply learned combination of positional operations."""
        # x: [batch, seq, d_model]

        # Cumulative operations (soft selection)
        cum_logits = self.cummax_weights[layer]
        cum_probs = F.softmax(cum_logits, dim=0)

        x_cummax_l = cummax_left(x)
        x_cummax_r = cummax_right(x)
        x_cumsum_l = cumsum_left(x)
        x_cumsum_r = cumsum_right(x)

        x_cum = (cum_probs[0] * x_cummax_l +
                 cum_probs[1] * x_cummax_r +
                 cum_probs[2] * x_cumsum_l +
                 cum_probs[3] * x_cumsum_r)

        # Shift operations (soft selection)
        shift_logits = self.shift_weights[layer]
        shift_probs = F.softmax(shift_logits, dim=0)

        x_shift_l = shift_left(x_cum)
        x_shift_r = shift_right(x_cum)

        x_shift = (shift_probs[0] * x_cum +
                   shift_probs[1] * x_shift_l +
                   shift_probs[2] * x_shift_r)

        # Flip operation (soft selection)
        flip_logits = self.flip_weights[layer]
        flip_probs = F.softmax(flip_logits, dim=0)

        x_flipped = flip_seq(x_shift)

        x_out = flip_probs[0] * x_shift + flip_probs[1] * x_flipped

        return x_out

    def forward(self, input_seq: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Forward pass.

        Args:
            input_seq: [batch, seq_len] input tokens

        Returns:
            logits: [batch, seq_len, vocab_size]
            kl: KL divergence
        """
        batch_size, seq_len = input_seq.shape

        # Sample latent
        z, kl = self.sample_latent()

        # Embed input
        x = self.embed(input_seq)  # [batch, seq, d_model]
        positions = torch.arange(seq_len, device=input_seq.device)
        x = x + self.pos_embed(positions)

        # Decode latent to initial hidden state
        h = self.decode_latent(z)  # [d_model]
        h = h.unsqueeze(0).unsqueeze(0).expand(batch_size, seq_len, -1)  # [batch, seq, d_model]

        # Process through layers
        for layer in range(self.n_layers):
            # Apply positional operations to hidden state
            h_pos = self.apply_positional_ops(h, layer)

            # Mix with input information
            combined = torch.cat([x, h_pos], dim=-1)  # [batch, seq, d_model * 2]
            h = h + self.layer_mlps[layer](combined)  # Residual connection

        # Project to vocabulary
        logits = self.output_head(h)

        return logits, kl

    def compute_loss(self, input_seq: torch.Tensor, target_seq: torch.Tensor,
                     kl_weight: float = 0.01) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Compute MDL loss."""
        logits, kl = self.forward(input_seq)

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


# =============================================================================
# TRANSFER LEARNING
# =============================================================================

class SequenceLibrary:
    """Library for weight transfer."""

    def __init__(self):
        self.entries: Dict[str, Dict] = {}

    def add(self, task_name: str, weights: List[torch.Tensor], steps: int, loss: float):
        self.entries[task_name] = {
            'weights': [w.detach().clone() for w in weights],
            'steps': steps,
            'loss': loss
        }

    def get_best(self) -> Optional[Dict]:
        if not self.entries:
            return None
        return min(self.entries.values(), key=lambda e: e['loss'])

    def transfer_weights(self, model: SequenceCompressor):
        """Transfer compatible weights to model."""
        entry = self.get_best()
        if not entry:
            return 0

        transferred = 0
        for src, tgt in zip(entry['weights'], model.weights_list):
            if src.shape == tgt.shape:
                tgt.data.copy_(src.data)
                transferred += 1
        return transferred


# =============================================================================
# SOLVER
# =============================================================================

def pad_seq(seq: List[int], max_len: int) -> List[int]:
    """Pad sequence to max_len."""
    return seq + [0] * (max_len - len(seq))


def solve_task(task: SequenceTask, library: Optional[SequenceLibrary] = None,
               max_steps: int = 500, target_loss: float = 0.1,
               verbose: bool = True) -> Dict:
    """Solve a sequence task with learning."""

    model = SequenceCompressor(task.vocab_size, task.max_len)

    # Transfer weights if available
    transferred = 0
    if library:
        transferred = library.transfer_weights(model)

    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    # Prepare data
    inputs = torch.tensor([pad_seq(p[0], task.max_len) for p in task.train_pairs], dtype=torch.long)
    targets = torch.tensor([pad_seq(p[1], task.max_len) for p in task.train_pairs], dtype=torch.long)

    # Train
    model.train()
    start = time.time()

    for step in range(max_steps):
        optimizer.zero_grad()
        loss, kl, recon = model.compute_loss(inputs, targets)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()

        if loss.item() < target_loss:
            break

    elapsed = time.time() - start

    # Test
    test_in = torch.tensor([pad_seq(task.test_pairs[0][0], task.max_len)], dtype=torch.long)
    pred = model.predict(test_in)[0].tolist()
    expected = task.test_pairs[0][1]
    pred_trimmed = pred[:len(expected)]
    correct = pred_trimmed == expected

    if verbose:
        transfer_str = f" (transferred {transferred})" if transferred else " (scratch)"
        print(f"  {step+1} steps, {elapsed:.1f}s{transfer_str}")
        print(f"  Loss: {loss.item():.4f}, Correct: {correct}")
        if not correct:
            print(f"  Pred: {pred_trimmed}")
            print(f"  Exp:  {expected}")

    return {
        'task_name': task.task_name,
        'steps': step + 1,
        'loss': loss.item(),
        'time': elapsed,
        'correct': correct,
        'transferred': transferred,
        'weights': list(model.weights_list)
    }


# =============================================================================
# TEST TASKS - Including NOVEL transforms
# =============================================================================

def make_task(name: str, pairs: List[Tuple[List[int], List[int]]],
              vocab_size: int = 12) -> SequenceTask:
    train = pairs[:-1]
    test = pairs[-1:]
    max_len = max(max(len(p[0]), len(p[1])) for p in pairs)
    return SequenceTask(name, train, test, vocab_size, max_len)


def make_transform_tasks(name: str, transform, n: int, n_examples: int,
                         length: int, seed_offset: int) -> List[SequenceTask]:
    """Generate tasks for a given transform."""
    tasks = []
    for i in range(n):
        np.random.seed(i + seed_offset)
        pairs = []
        for _ in range(n_examples):
            seq = list(np.random.randint(1, 10, size=length))
            try:
                out = transform(seq)
                if isinstance(out, np.ndarray):
                    out = out.tolist()
                pairs.append((seq, out))
            except:
                continue
        if len(pairs) >= 2:
            tasks.append(make_task(f"{name}_{i}", pairs))
    return tasks


if __name__ == "__main__":
    print("=" * 70)
    print("SEQUENCE COMPRESSOR - Learning-Based (Like ARCCompressor)")
    print("=" * 70)
    print("Testing with ACTUAL LEARNING, not enumeration")
    print()

    # Define transforms - including NOVEL ones not in any DSL
    transforms = [
        # Simple transforms
        ("identity", lambda x: x.copy()),
        ("increment", lambda x: [(v + 1) % 10 for v in x]),
        ("reverse", lambda x: x[::-1]),

        # NOVEL transforms that DSL approach couldn't handle
        ("running_max", lambda x: [max(x[:i+1]) for i in range(len(x))]),
        ("swap_pairs", lambda x: [x[i^1] if i^1 < len(x) else x[i] for i in range(len(x))]),
        ("mirror_add", lambda x: [(a+b)%10 for a,b in zip(x, x[::-1])]),
    ]

    all_results = {}

    for transform_name, transform_fn in transforms:
        print(f"\n{'='*60}")
        print(f"[{transform_name}]")
        print("="*60)

        tasks = make_transform_tasks(transform_name, transform_fn,
                                     n=5, n_examples=10, length=5,
                                     seed_offset=hash(transform_name) % 10000)

        library = SequenceLibrary()
        results = []

        for i, task in enumerate(tasks):
            print(f"\n[{i+1}/{len(tasks)}] {task.task_name}")
            print(f"  Example: {task.train_pairs[0][0]} -> {task.train_pairs[0][1]}")

            result = solve_task(task, library if i > 0 else None, verbose=True)

            if result['correct']:
                library.add(task.task_name, result['weights'], result['steps'], result['loss'])

            results.append(result)

        correct = sum(r['correct'] for r in results)
        print(f"\n{transform_name} Summary: {correct}/{len(results)} correct")
        print("Learning curve:", [r['steps'] for r in results])

        all_results[transform_name] = results

    # Overall summary
    print("\n" + "=" * 70)
    print("OVERALL SUMMARY")
    print("=" * 70)

    for name, results in all_results.items():
        correct = sum(r['correct'] for r in results)
        avg_steps = sum(r['steps'] for r in results) / len(results)
        print(f"  {name:15s}: {correct}/{len(results)} correct, avg {avg_steps:.0f} steps")

    total_correct = sum(r['correct'] for results in all_results.values() for r in results)
    total_tasks = sum(len(results) for results in all_results.values())
    print(f"\n  TOTAL: {total_correct}/{total_tasks} correct")
