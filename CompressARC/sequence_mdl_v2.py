#!/usr/bin/env python3
"""
SEQUENCE MDL V2 - Attention-Based Decoder

A more powerful MDL system for sequences that can handle:
- Reversal (positional permutations)
- Sorting
- Complex pattern transformations
- Eventually: real language tasks

Key insight: The latent must CONTROL attention patterns.
The decoder uses latent-conditioned cross-attention.

Architecture:
- Encoder: Embed input sequence
- Latent: Compressed "program" that controls transformation
- Decoder: Latent-conditioned attention over input → output

This is more like a seq2seq with MDL regularization.
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


class PositionalEncoding(nn.Module):
    """Sinusoidal positional encoding."""
    def __init__(self, d_model: int, max_len: int = 100):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x + self.pe[:x.size(1)]


class LatentConditionedAttention(nn.Module):
    """
    Cross-attention where the latent modulates the attention.
    The latent acts as a "program" that controls how input maps to output.
    """
    def __init__(self, d_model: int, n_heads: int, latent_dim: int):
        super().__init__()
        self.d_model = d_model
        self.n_heads = n_heads
        self.head_dim = d_model // n_heads

        # Query comes from output positions + latent
        self.q_proj = nn.Linear(d_model + latent_dim, d_model)
        # Key/Value come from input
        self.k_proj = nn.Linear(d_model, d_model)
        self.v_proj = nn.Linear(d_model, d_model)
        self.out_proj = nn.Linear(d_model, d_model)

    def forward(self, query: torch.Tensor, key: torch.Tensor, value: torch.Tensor,
                latent: torch.Tensor) -> torch.Tensor:
        batch_size, seq_len, _ = query.shape

        # Concatenate latent to query
        latent_expanded = latent.unsqueeze(1).expand(-1, seq_len, -1)
        query_with_latent = torch.cat([query, latent_expanded], dim=-1)

        # Project
        Q = self.q_proj(query_with_latent)
        K = self.k_proj(key)
        V = self.v_proj(value)

        # Reshape for multi-head attention
        Q = Q.view(batch_size, seq_len, self.n_heads, self.head_dim).transpose(1, 2)
        K = K.view(batch_size, -1, self.n_heads, self.head_dim).transpose(1, 2)
        V = V.view(batch_size, -1, self.n_heads, self.head_dim).transpose(1, 2)

        # Attention
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.head_dim)
        attn = F.softmax(scores, dim=-1)
        out = torch.matmul(attn, V)

        # Reshape back
        out = out.transpose(1, 2).contiguous().view(batch_size, seq_len, self.d_model)
        return self.out_proj(out)


class SequenceMDLv2(nn.Module):
    """
    MDL-based sequence transformer.

    The key difference from v1:
    - Latent controls attention patterns (not just concatenated)
    - Full encoder-decoder architecture
    - Can learn positional permutations (reverse, sort)
    """

    def __init__(self, vocab_size: int, max_len: int,
                 d_model: int = 128, n_heads: int = 4, n_layers: int = 3,
                 latent_dim: int = 64):
        super().__init__()

        self.vocab_size = vocab_size
        self.max_len = max_len
        self.d_model = d_model
        self.latent_dim = latent_dim

        # Embeddings
        self.embed = nn.Embedding(vocab_size, d_model)
        self.pos_enc = PositionalEncoding(d_model, max_len + 10)

        # Latent (the "program")
        self.latent_mean = nn.Parameter(torch.randn(latent_dim) * 0.1)
        self.latent_logvar = nn.Parameter(torch.zeros(latent_dim) - 2)

        # Encoder (process input)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model, nhead=n_heads, dim_feedforward=d_model*4,
            batch_first=True, norm_first=True
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=n_layers)

        # Decoder with latent-conditioned attention
        self.decoder_layers = nn.ModuleList()
        for _ in range(n_layers):
            self.decoder_layers.append(nn.ModuleDict({
                'self_attn': nn.MultiheadAttention(d_model, n_heads, batch_first=True),
                'cross_attn': LatentConditionedAttention(d_model, n_heads, latent_dim),
                'ff': nn.Sequential(
                    nn.Linear(d_model, d_model * 4),
                    nn.GELU(),
                    nn.Linear(d_model * 4, d_model)
                ),
                'norm1': nn.LayerNorm(d_model),
                'norm2': nn.LayerNorm(d_model),
                'norm3': nn.LayerNorm(d_model)
            }))

        # Output head
        self.output_head = nn.Linear(d_model, vocab_size)

        # Collect weights
        self.weights_list = list(self.parameters())

    def sample_latent(self) -> Tuple[torch.Tensor, torch.Tensor]:
        """Sample from latent posterior, compute KL."""
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
            target_len: output sequence length (defaults to input length)

        Returns:
            logits: [batch, tgt_len, vocab_size]
            kl: KL divergence
        """
        batch_size, src_len = input_seq.shape
        if target_len is None:
            target_len = src_len

        # Sample latent
        z, kl = self.sample_latent()
        z = z.unsqueeze(0).expand(batch_size, -1)  # [batch, latent_dim]

        # Encode input
        x = self.embed(input_seq)
        x = self.pos_enc(x)
        memory = self.encoder(x)

        # Decode (use positional queries)
        tgt_positions = torch.arange(target_len, device=input_seq.device)
        tgt = self.pos_enc.pe[:target_len].unsqueeze(0).expand(batch_size, -1, -1)

        for layer in self.decoder_layers:
            # Self-attention on output positions
            tgt_norm = layer['norm1'](tgt)
            tgt = tgt + layer['self_attn'](tgt_norm, tgt_norm, tgt_norm)[0]

            # Cross-attention with latent conditioning
            tgt_norm = layer['norm2'](tgt)
            tgt = tgt + layer['cross_attn'](tgt_norm, memory, memory, z)

            # Feedforward
            tgt_norm = layer['norm3'](tgt)
            tgt = tgt + layer['ff'](tgt_norm)

        logits = self.output_head(tgt)
        return logits, kl

    def compute_loss(self, input_seq: torch.Tensor, target_seq: torch.Tensor,
                     kl_weight: float = 0.01) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Compute MDL loss = KL + reconstruction."""
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


class SequenceLibraryV2:
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


def solve_task(task: SequenceTask, library: SequenceLibraryV2 = None,
               max_steps: int = 500, target_loss: float = 5.0,
               verbose: bool = True) -> Dict:
    """Solve a sequence task with MDL v2."""

    model = SequenceMDLv2(task.vocab_size, task.max_len)

    # Transfer weights if available
    transferred = 0
    if library:
        entry = library.get_best()
        if entry:
            for src, tgt in zip(entry['weights'], model.weights_list):
                if src.shape == tgt.shape:
                    tgt.data.copy_(src.data)
                    transferred += 1

    optimizer = torch.optim.Adam(model.parameters(), lr=0.005, betas=(0.9, 0.98))

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

def make_reverse_tasks(n: int = 5, length: int = 5) -> List[SequenceTask]:
    """Reversal tasks."""
    tasks = []
    for i in range(n):
        np.random.seed(i + 100)
        pairs = []
        for _ in range(4):
            seq = list(np.random.randint(1, 10, size=length))
            pairs.append((seq, seq[::-1]))
        tasks.append(make_task(f"reverse_{i}", pairs))
    return tasks


def make_sort_tasks(n: int = 5, length: int = 5) -> List[SequenceTask]:
    """Sorting tasks."""
    tasks = []
    for i in range(n):
        np.random.seed(i + 200)
        pairs = []
        for _ in range(4):
            seq = list(np.random.randint(1, 10, size=length))
            pairs.append((seq, sorted(seq)))
        tasks.append(make_task(f"sort_{i}", pairs))
    return tasks


def make_rotate_tasks(n: int = 5, length: int = 5, k: int = 2) -> List[SequenceTask]:
    """Rotate sequence by k positions."""
    tasks = []
    for i in range(n):
        np.random.seed(i + 300)
        pairs = []
        for _ in range(4):
            seq = list(np.random.randint(1, 10, size=length))
            rotated = seq[k:] + seq[:k]
            pairs.append((seq, rotated))
        tasks.append(make_task(f"rotate_{k}_{i}", pairs))
    return tasks


if __name__ == "__main__":
    print("=" * 60)
    print("SEQUENCE MDL V2 - ATTENTION-BASED")
    print("=" * 60)
    print("Testing complex transforms: reverse, sort, rotate")
    print()

    test_suites = [
        ("REVERSE", make_reverse_tasks(5)),
        ("SORT", make_sort_tasks(5)),
        ("ROTATE", make_rotate_tasks(5, k=2)),
    ]

    for suite_name, tasks in test_suites:
        print(f"\n{'='*60}")
        print(f"[{suite_name}]")
        print(f"{'='*60}")

        library = SequenceLibraryV2()
        results = []

        for i, task in enumerate(tasks):
            print(f"\n[{i+1}/5] {task.task_name}")
            print(f"  Example: {task.train_pairs[0][0]} -> {task.train_pairs[0][1]}")

            result = solve_task(task, library if i > 0 else None, verbose=True)

            if result['correct']:
                library.add(task.task_name, result['weights'], result['steps'])

            results.append(result)

        # Summary
        correct = sum(r['correct'] for r in results)
        print(f"\n{suite_name} Summary: {correct}/5 correct")
        print("Learning curve:", [r['steps'] for r in results])
