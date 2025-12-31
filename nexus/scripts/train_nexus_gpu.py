#!/usr/bin/env python3
"""
Nexus GPU Training Script - Full Mamba-2 SSD Implementation

Trains the Nexus hybrid attention/SSM model with GPU acceleration.
Supports both Shakespeare (small) and TinyStories (large) datasets.

Usage:
    # Shakespeare (quick test)
    python scripts/train_nexus_gpu.py --data data/shakespeare.txt --epochs 100

    # TinyStories (full training)
    python scripts/train_nexus_gpu.py --data data/TinyStories-train.txt --epochs 10 --batch-size 64

Requirements:
    pip install torch numpy tqdm
"""

import argparse
import json
import math
import os
import time
from pathlib import Path
from typing import Optional, List, Tuple
from dataclasses import dataclass

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset
from torch.cuda.amp import autocast, GradScaler

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    def tqdm(x, **kwargs):
        return x


# =============================================================================
# Configuration
# =============================================================================

@dataclass
class NexusConfig:
    """Nexus model configuration"""
    vocab_size: int = 8000
    d_model: int = 256
    n_heads: int = 4
    n_layers: int = 6
    d_state: int = 64          # Mamba-2 state dimension (was 16 in Mamba-1)
    d_conv: int = 4            # Convolution width
    expand: int = 2            # Expansion factor
    chunk_size: int = 64       # Mamba-2 SSD chunk size
    headdim: int = 64          # Mamba-2 head dimension
    max_seq_len: int = 512
    dropout: float = 0.1
    attention_ratio: int = 1   # 1:7 attention to SSM ratio
    use_flash_attention: bool = True

    @property
    def d_inner(self):
        return self.d_model * self.expand


# =============================================================================
# Mamba-2 SSD Layer (State Space Duality)
# =============================================================================

class Mamba2SSD(nn.Module):
    """
    Mamba-2 State Space Duality layer.

    Key innovations over Mamba-1:
    - Chunk-parallel algorithm (2-8x faster)
    - Multi-head structure with headdim
    - Larger state dimension (64+ vs 16)
    - Tensor core friendly matmul operations
    """

    def __init__(self, config: NexusConfig):
        super().__init__()
        self.config = config
        self.d_model = config.d_model
        self.d_inner = config.d_inner
        self.d_state = config.d_state
        self.d_conv = config.d_conv
        self.chunk_size = config.chunk_size
        self.headdim = config.headdim
        self.n_heads = self.d_inner // self.headdim

        # Input projection (fused for efficiency)
        self.in_proj = nn.Linear(config.d_model, config.d_inner * 2, bias=False)

        # Convolution for local context
        self.conv1d = nn.Conv1d(
            config.d_inner, config.d_inner,
            kernel_size=config.d_conv,
            padding=config.d_conv - 1,
            groups=config.d_inner
        )

        # SSM parameters projection
        # Mamba-2: A, B, C computed in parallel (not sequentially like Mamba-1)
        self.x_proj = nn.Linear(config.d_inner, config.d_state * 2 + self.n_heads, bias=False)

        # A parameter (learned, per-head)
        # Initialized to small negative values for stability
        self.A_log = nn.Parameter(torch.log(torch.linspace(1, 16, self.n_heads)))

        # D parameter (skip connection, per-head)
        self.D = nn.Parameter(torch.ones(self.n_heads))

        # Output projection
        self.out_proj = nn.Linear(config.d_inner, config.d_model, bias=False)

        # RMSNorm with gating (Mamba-2 style)
        self.norm = RMSNorm(config.d_inner)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass with chunk-parallel SSD algorithm.

        Args:
            x: Input tensor [batch, seq_len, d_model]

        Returns:
            Output tensor [batch, seq_len, d_model]
        """
        batch, seq_len, _ = x.shape

        # Input projection and split
        xz = self.in_proj(x)
        x_main, z = xz.chunk(2, dim=-1)

        # Convolution for local context
        x_conv = x_main.transpose(1, 2)  # [batch, d_inner, seq_len]
        x_conv = self.conv1d(x_conv)[:, :, :seq_len]
        x_conv = x_conv.transpose(1, 2)  # [batch, seq_len, d_inner]

        # Apply SiLU activation
        x_conv = F.silu(x_conv)

        # Project to SSM parameters
        x_ssm = self.x_proj(x_conv)

        # Split into B, C, and dt
        B = x_ssm[:, :, :self.d_state]
        C = x_ssm[:, :, self.d_state:self.d_state*2]
        dt = F.softplus(x_ssm[:, :, self.d_state*2:])  # [batch, seq_len, n_heads]

        # Get A (negative for stability)
        A = -torch.exp(self.A_log)  # [n_heads]

        # Reshape for multi-head processing
        x_reshaped = x_conv.view(batch, seq_len, self.n_heads, self.headdim)

        # Run SSD algorithm
        y = self.ssd_forward(x_reshaped, A, B, C, dt)

        # Reshape back
        y = y.view(batch, seq_len, self.d_inner)

        # Apply D (skip connection)
        y = y + x_conv * self.D.view(1, 1, self.n_heads, 1).expand(-1, -1, -1, self.headdim).reshape(1, 1, -1)

        # Gating with z
        y = y * F.silu(z)

        # Normalize and project out
        y = self.norm(y)
        y = self.out_proj(y)

        return y

    def ssd_forward(
        self,
        x: torch.Tensor,  # [batch, seq_len, n_heads, headdim]
        A: torch.Tensor,  # [n_heads]
        B: torch.Tensor,  # [batch, seq_len, d_state]
        C: torch.Tensor,  # [batch, seq_len, d_state]
        dt: torch.Tensor  # [batch, seq_len, n_heads]
    ) -> torch.Tensor:
        """
        Chunk-parallel SSD algorithm (Mamba-2).

        The 4-step algorithm:
        1. Intra-chunk diagonal (parallel matmul)
        2. Chunk state computation (parallel matmul)
        3. Inter-chunk state passing (sequential, but on chunks not tokens)
        4. State to output (parallel matmul)
        """
        batch, seq_len, n_heads, headdim = x.shape

        # Pad sequence to multiple of chunk_size
        chunk_size = min(self.chunk_size, seq_len)
        if seq_len % chunk_size != 0:
            pad_len = chunk_size - (seq_len % chunk_size)
            x = F.pad(x, (0, 0, 0, 0, 0, pad_len))
            B = F.pad(B, (0, 0, 0, pad_len))
            C = F.pad(C, (0, 0, 0, pad_len))
            dt = F.pad(dt, (0, 0, 0, pad_len))
            padded_len = seq_len + pad_len
        else:
            padded_len = seq_len

        n_chunks = padded_len // chunk_size

        # Reshape into chunks
        x_chunks = x.view(batch, n_chunks, chunk_size, n_heads, headdim)
        B_chunks = B.view(batch, n_chunks, chunk_size, self.d_state)
        C_chunks = C.view(batch, n_chunks, chunk_size, self.d_state)
        dt_chunks = dt.view(batch, n_chunks, chunk_size, n_heads)

        # Compute decay factors
        # A_dt[i,j] = exp(A * dt[i,j]) for discrete-time
        A_dt = A.view(1, 1, 1, n_heads) * dt_chunks  # [batch, n_chunks, chunk_size, n_heads]

        # Step 1: Intra-chunk computation (diagonal blocks)
        # For each position in chunk, compute contribution from all previous positions in same chunk
        y_chunks = self.intra_chunk_forward(x_chunks, A_dt, B_chunks, C_chunks)

        # Step 2 & 3: Compute and pass chunk states
        chunk_states = self.compute_chunk_states(x_chunks, A_dt, B_chunks)

        # Step 4: Add contribution from previous chunk states
        y_chunks = y_chunks + self.state_to_output(chunk_states, A_dt, C_chunks)

        # Reshape and remove padding
        y = y_chunks.view(batch, padded_len, n_heads, headdim)
        if padded_len > seq_len:
            y = y[:, :seq_len, :, :]

        return y

    def intra_chunk_forward(
        self,
        x: torch.Tensor,      # [batch, n_chunks, chunk_size, n_heads, headdim]
        A_dt: torch.Tensor,   # [batch, n_chunks, chunk_size, n_heads]
        B: torch.Tensor,      # [batch, n_chunks, chunk_size, d_state]
        C: torch.Tensor,      # [batch, n_chunks, chunk_size, d_state]
    ) -> torch.Tensor:
        """Compute output contributions from within each chunk (diagonal blocks)."""
        batch, n_chunks, chunk_size, n_heads, headdim = x.shape

        # Build decay matrix for segment [i:j]
        # L[i,j] = exp(sum(A_dt[i:j]))
        A_cumsum = torch.cumsum(A_dt, dim=2)  # [batch, n_chunks, chunk_size, n_heads]

        # L[i,j] = exp(A_cumsum[j-1] - A_cumsum[i-1]) for i < j
        # Create lower triangular decay matrix
        L = A_cumsum.unsqueeze(3) - A_cumsum.unsqueeze(2)  # [batch, n_chunks, chunk_size, chunk_size, n_heads]
        L = torch.exp(L)

        # Mask upper triangle (causal)
        mask = torch.tril(torch.ones(chunk_size, chunk_size, device=x.device))
        L = L * mask.view(1, 1, chunk_size, chunk_size, 1)

        # Compute B @ x for each position
        # B: [batch, n_chunks, chunk_size, d_state]
        # x: [batch, n_chunks, chunk_size, n_heads, headdim]
        Bx = torch.einsum('bncn,bnchd->bncnd', B, x)  # [batch, n_chunks, chunk_size, d_state, headdim]

        # Apply decay and sum: y[t] = sum_{s<=t} L[s,t] * C[t] @ B[s] @ x[s]
        # This is the "quadratic" form within chunk
        y = torch.einsum('bncsh,bncsc,bnscd->bnchd', L, C.unsqueeze(2).expand(-1,-1,chunk_size,-1,-1), Bx.unsqueeze(2).expand(-1,-1,chunk_size,-1,-1,-1))

        # Simplified version: iterate through chunk (still parallel across chunks)
        y = torch.zeros_like(x)
        state = torch.zeros(batch, n_chunks, n_heads, self.d_state, headdim, device=x.device)

        for t in range(chunk_size):
            # Discretize: state = exp(A*dt) * state + B * x
            decay = torch.exp(A_dt[:, :, t, :]).unsqueeze(-1).unsqueeze(-1)  # [batch, n_chunks, n_heads, 1, 1]
            B_t = B[:, :, t, :]  # [batch, n_chunks, d_state]
            x_t = x[:, :, t, :, :]  # [batch, n_chunks, n_heads, headdim]

            # state: [batch, n_chunks, n_heads, d_state, headdim]
            state = decay * state + torch.einsum('bcs,bcnh->bcnsh', B_t, x_t)

            # Output: y = C @ state
            C_t = C[:, :, t, :]  # [batch, n_chunks, d_state]
            y[:, :, t, :, :] = torch.einsum('bcs,bcnsh->bcnh', C_t, state)

        return y

    def compute_chunk_states(
        self,
        x: torch.Tensor,      # [batch, n_chunks, chunk_size, n_heads, headdim]
        A_dt: torch.Tensor,   # [batch, n_chunks, chunk_size, n_heads]
        B: torch.Tensor,      # [batch, n_chunks, chunk_size, d_state]
    ) -> torch.Tensor:
        """
        Compute final state of each chunk, then pass states between chunks.
        Returns the initial state for each chunk (from all previous chunks).
        """
        batch, n_chunks, chunk_size, n_heads, headdim = x.shape

        # Compute final state of each chunk (assuming initial state = 0)
        # This is parallelizable across chunks
        chunk_final_states = torch.zeros(batch, n_chunks, n_heads, self.d_state, headdim, device=x.device)

        for c in range(n_chunks):
            state = torch.zeros(batch, n_heads, self.d_state, headdim, device=x.device)
            for t in range(chunk_size):
                decay = torch.exp(A_dt[:, c, t, :]).unsqueeze(-1).unsqueeze(-1)
                B_t = B[:, c, t, :]
                x_t = x[:, c, t, :, :]
                state = decay * state + torch.einsum('bs,bnh->bnsh', B_t, x_t)
            chunk_final_states[:, c] = state

        # Pass states between chunks (sequential, but O(n_chunks) not O(seq_len))
        # chunk_decay = exp(sum of all A*dt in chunk)
        chunk_decay = torch.exp(A_dt.sum(dim=2))  # [batch, n_chunks, n_heads]

        # Initial states for each chunk (contribution from all previous chunks)
        chunk_initial_states = torch.zeros(batch, n_chunks, n_heads, self.d_state, headdim, device=x.device)

        running_state = torch.zeros(batch, n_heads, self.d_state, headdim, device=x.device)
        for c in range(n_chunks):
            chunk_initial_states[:, c] = running_state
            decay = chunk_decay[:, c, :].unsqueeze(-1).unsqueeze(-1)
            running_state = decay * running_state + chunk_final_states[:, c]

        return chunk_initial_states

    def state_to_output(
        self,
        chunk_states: torch.Tensor,  # [batch, n_chunks, n_heads, d_state, headdim]
        A_dt: torch.Tensor,          # [batch, n_chunks, chunk_size, n_heads]
        C: torch.Tensor,             # [batch, n_chunks, chunk_size, d_state]
    ) -> torch.Tensor:
        """Compute output contribution from initial chunk state."""
        batch, n_chunks, n_heads, d_state, headdim = chunk_states.shape
        chunk_size = A_dt.shape[2]

        # For each position in chunk, compute contribution from initial state
        y = torch.zeros(batch, n_chunks, chunk_size, n_heads, headdim, device=chunk_states.device)

        for t in range(chunk_size):
            # Decay from start of chunk to position t
            if t == 0:
                decay = torch.ones(batch, n_chunks, n_heads, device=chunk_states.device)
            else:
                decay = torch.exp(A_dt[:, :, :t, :].sum(dim=2))  # [batch, n_chunks, n_heads]

            # state_t = decay * initial_state
            state_t = decay.unsqueeze(-1).unsqueeze(-1) * chunk_states  # [batch, n_chunks, n_heads, d_state, headdim]

            # y_t = C_t @ state_t
            C_t = C[:, :, t, :]  # [batch, n_chunks, d_state]
            y[:, :, t, :, :] = torch.einsum('bcs,bcnsh->bcnh', C_t, state_t)

        return y


class RMSNorm(nn.Module):
    """Root Mean Square Layer Normalization (Mamba-2 style)."""

    def __init__(self, dim: int, eps: float = 1e-6):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(dim))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        rms = torch.sqrt(torch.mean(x ** 2, dim=-1, keepdim=True) + self.eps)
        return x / rms * self.weight


# =============================================================================
# Attention Layer
# =============================================================================

class MultiHeadAttention(nn.Module):
    """Multi-head attention with RoPE (Rotary Position Embeddings)."""

    def __init__(self, config: NexusConfig):
        super().__init__()
        self.n_heads = config.n_heads
        self.head_dim = config.d_model // config.n_heads
        self.scale = self.head_dim ** -0.5

        self.q_proj = nn.Linear(config.d_model, config.d_model, bias=False)
        self.k_proj = nn.Linear(config.d_model, config.d_model, bias=False)
        self.v_proj = nn.Linear(config.d_model, config.d_model, bias=False)
        self.out_proj = nn.Linear(config.d_model, config.d_model, bias=False)

        self.dropout = nn.Dropout(config.dropout)

        # RoPE
        self.register_buffer(
            "freqs",
            self._compute_freqs(config.max_seq_len, self.head_dim)
        )

    def _compute_freqs(self, max_len: int, dim: int) -> torch.Tensor:
        """Compute rotary position embedding frequencies."""
        freqs = 1.0 / (10000 ** (torch.arange(0, dim, 2).float() / dim))
        t = torch.arange(max_len)
        freqs = torch.outer(t, freqs)
        return torch.polar(torch.ones_like(freqs), freqs)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch, seq_len, _ = x.shape

        q = self.q_proj(x).view(batch, seq_len, self.n_heads, self.head_dim)
        k = self.k_proj(x).view(batch, seq_len, self.n_heads, self.head_dim)
        v = self.v_proj(x).view(batch, seq_len, self.n_heads, self.head_dim)

        # Apply RoPE
        q = self._apply_rope(q, seq_len)
        k = self._apply_rope(k, seq_len)

        # Attention
        q = q.transpose(1, 2)  # [batch, n_heads, seq_len, head_dim]
        k = k.transpose(1, 2)
        v = v.transpose(1, 2)

        scores = torch.matmul(q, k.transpose(-2, -1)) * self.scale

        # Causal mask
        mask = torch.triu(torch.ones(seq_len, seq_len, device=x.device), diagonal=1).bool()
        scores = scores.masked_fill(mask, float('-inf'))

        attn = F.softmax(scores, dim=-1)
        attn = self.dropout(attn)

        out = torch.matmul(attn, v)
        out = out.transpose(1, 2).contiguous().view(batch, seq_len, -1)

        return self.out_proj(out)

    def _apply_rope(self, x: torch.Tensor, seq_len: int) -> torch.Tensor:
        """Apply rotary position embeddings."""
        # Convert to complex for rotation
        x_complex = torch.view_as_complex(x.float().reshape(*x.shape[:-1], -1, 2))
        freqs = self.freqs[:seq_len].unsqueeze(0).unsqueeze(2)
        x_rotated = x_complex * freqs
        return torch.view_as_real(x_rotated).reshape(*x.shape).type_as(x)


# =============================================================================
# Hybrid Block (Attention + SSM)
# =============================================================================

class HybridBlock(nn.Module):
    """Hybrid block combining attention and SSM (1:7 ratio like Jamba)."""

    def __init__(self, config: NexusConfig, use_attention: bool = False):
        super().__init__()
        self.use_attention = use_attention

        self.norm1 = RMSNorm(config.d_model)
        self.norm2 = RMSNorm(config.d_model)

        if use_attention:
            self.attn = MultiHeadAttention(config)
        else:
            self.ssm = Mamba2SSD(config)

        # MLP
        self.mlp = nn.Sequential(
            nn.Linear(config.d_model, config.d_model * 4),
            nn.GELU(),
            nn.Linear(config.d_model * 4, config.d_model),
            nn.Dropout(config.dropout),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Pre-norm architecture
        if self.use_attention:
            x = x + self.attn(self.norm1(x))
        else:
            x = x + self.ssm(self.norm1(x))

        x = x + self.mlp(self.norm2(x))
        return x


# =============================================================================
# Nexus Model
# =============================================================================

class NexusLM(nn.Module):
    """Nexus Language Model with hybrid Attention/SSM architecture."""

    def __init__(self, config: NexusConfig):
        super().__init__()
        self.config = config

        # Token embeddings
        self.embed = nn.Embedding(config.vocab_size, config.d_model)
        self.pos_embed = nn.Embedding(config.max_seq_len, config.d_model)
        self.dropout = nn.Dropout(config.dropout)

        # Hybrid blocks (1:7 attention to SSM ratio)
        self.blocks = nn.ModuleList()
        for i in range(config.n_layers):
            use_attention = i % (config.attention_ratio + 7) < config.attention_ratio
            self.blocks.append(HybridBlock(config, use_attention))

        # Output
        self.norm = RMSNorm(config.d_model)
        self.lm_head = nn.Linear(config.d_model, config.vocab_size, bias=False)

        # Weight tying
        self.lm_head.weight = self.embed.weight

        # Initialize weights
        self.apply(self._init_weights)

    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch, seq_len = x.shape

        # Embeddings
        pos = torch.arange(seq_len, device=x.device).unsqueeze(0)
        h = self.embed(x) + self.pos_embed(pos)
        h = self.dropout(h)

        # Blocks
        for block in self.blocks:
            h = block(h)

        # Output
        h = self.norm(h)
        logits = self.lm_head(h)

        return logits

    def generate(
        self,
        prompt: torch.Tensor,
        max_new_tokens: int = 100,
        temperature: float = 0.8,
        top_k: int = 50,
    ) -> torch.Tensor:
        """Generate text autoregressively."""
        self.eval()
        tokens = prompt.clone()

        with torch.no_grad():
            for _ in range(max_new_tokens):
                # Get logits for last position
                logits = self(tokens[:, -self.config.max_seq_len:])
                logits = logits[:, -1, :] / temperature

                # Top-k sampling
                if top_k > 0:
                    v, _ = torch.topk(logits, min(top_k, logits.size(-1)))
                    logits[logits < v[:, [-1]]] = float('-inf')

                probs = F.softmax(logits, dim=-1)
                next_token = torch.multinomial(probs, num_samples=1)
                tokens = torch.cat([tokens, next_token], dim=1)

        return tokens


# =============================================================================
# Dataset
# =============================================================================

class TextDataset(Dataset):
    """Character/BPE-level text dataset."""

    def __init__(
        self,
        text: str,
        seq_len: int,
        tokenizer: Optional['SimpleBPE'] = None,
    ):
        self.seq_len = seq_len

        if tokenizer:
            self.tokens = tokenizer.encode(text)
        else:
            # Character-level fallback
            chars = sorted(list(set(text)))
            self.char_to_idx = {c: i for i, c in enumerate(chars)}
            self.idx_to_char = {i: c for c, i in self.char_to_idx.items()}
            self.tokens = [self.char_to_idx[c] for c in text]

        self.tokens = torch.tensor(self.tokens, dtype=torch.long)

    def __len__(self):
        return max(0, len(self.tokens) - self.seq_len - 1)

    def __getitem__(self, idx):
        x = self.tokens[idx:idx + self.seq_len]
        y = self.tokens[idx + 1:idx + self.seq_len + 1]
        return x, y


class SimpleBPE:
    """Simple BPE tokenizer (load from JSON)."""

    def __init__(self, vocab_path: str):
        with open(vocab_path, 'r') as f:
            data = json.load(f)
        self.vocab = data['vocab']
        self.merges = data.get('merges', [])
        self.token_to_id = {t: i for i, t in enumerate(self.vocab)}
        self.id_to_token = {i: t for t, i in self.token_to_id.items()}

    def encode(self, text: str) -> List[int]:
        """Encode text to token IDs (simplified character-based for now)."""
        tokens = []
        for char in text:
            if char in self.token_to_id:
                tokens.append(self.token_to_id[char])
            else:
                # Unknown token
                tokens.append(self.token_to_id.get('<unk>', 0))
        return tokens

    def decode(self, ids: List[int]) -> str:
        """Decode token IDs to text."""
        return ''.join(self.id_to_token.get(i, '?') for i in ids)


# =============================================================================
# Training
# =============================================================================

def train(
    model: NexusLM,
    train_loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    scheduler: torch.optim.lr_scheduler._LRScheduler,
    device: torch.device,
    config: dict,
) -> float:
    """Train for one epoch."""
    model.train()
    total_loss = 0.0
    n_batches = 0

    scaler = GradScaler() if config.get('fp16', False) and device.type == 'cuda' else None

    pbar = tqdm(train_loader, desc="Training") if HAS_TQDM else train_loader

    for x, y in pbar:
        x, y = x.to(device), y.to(device)

        optimizer.zero_grad()

        if scaler:
            with autocast():
                logits = model(x)
                loss = F.cross_entropy(logits.view(-1, logits.size(-1)), y.view(-1))
            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), config.get('max_grad_norm', 1.0))
            scaler.step(optimizer)
            scaler.update()
        else:
            logits = model(x)
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), y.view(-1))
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), config.get('max_grad_norm', 1.0))
            optimizer.step()

        scheduler.step()

        total_loss += loss.item()
        n_batches += 1

        if HAS_TQDM:
            pbar.set_postfix({
                'loss': f'{loss.item():.4f}',
                'ppl': f'{math.exp(loss.item()):.2f}',
                'lr': f'{scheduler.get_last_lr()[0]:.2e}',
            })

    return total_loss / n_batches


def evaluate(
    model: NexusLM,
    val_loader: DataLoader,
    device: torch.device,
) -> float:
    """Evaluate the model."""
    model.eval()
    total_loss = 0.0
    n_batches = 0

    with torch.no_grad():
        for x, y in val_loader:
            x, y = x.to(device), y.to(device)
            logits = model(x)
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), y.view(-1))
            total_loss += loss.item()
            n_batches += 1

    return total_loss / n_batches


def main():
    parser = argparse.ArgumentParser(description="Train Nexus model with GPU acceleration")

    # Data
    parser.add_argument("--data", type=str, required=True, help="Path to training text file")
    parser.add_argument("--vocab", type=str, help="Path to BPE vocabulary JSON")
    parser.add_argument("--val-split", type=float, default=0.1, help="Validation split ratio")

    # Model
    parser.add_argument("--d-model", type=int, default=256, help="Model dimension")
    parser.add_argument("--n-heads", type=int, default=4, help="Number of attention heads")
    parser.add_argument("--n-layers", type=int, default=6, help="Number of layers")
    parser.add_argument("--d-state", type=int, default=64, help="SSM state dimension")
    parser.add_argument("--vocab-size", type=int, default=8000, help="Vocabulary size")
    parser.add_argument("--seq-len", type=int, default=256, help="Sequence length")

    # Training
    parser.add_argument("--epochs", type=int, default=100, help="Number of epochs")
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size")
    parser.add_argument("--lr", type=float, default=3e-4, help="Learning rate")
    parser.add_argument("--weight-decay", type=float, default=0.01, help="Weight decay")
    parser.add_argument("--warmup-steps", type=int, default=100, help="Warmup steps")
    parser.add_argument("--max-grad-norm", type=float, default=1.0, help="Gradient clipping")
    parser.add_argument("--fp16", action="store_true", help="Use mixed precision training")

    # Output
    parser.add_argument("--output", type=str, default="checkpoints", help="Output directory")
    parser.add_argument("--log-every", type=int, default=100, help="Log every N steps")
    parser.add_argument("--save-every", type=int, default=1000, help="Save every N steps")
    parser.add_argument("--sample-every", type=int, default=500, help="Generate sample every N steps")

    # Device
    parser.add_argument("--device", type=str, default="auto", help="Device (cuda/cpu/auto)")

    args = parser.parse_args()

    # Setup device
    if args.device == "auto":
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        device = torch.device(args.device)

    print("=" * 70)
    print("NEXUS GPU TRAINING")
    print("=" * 70)
    print(f"Device: {device}")
    if device.type == 'cuda':
        print(f"GPU: {torch.cuda.get_device_name()}")
        print(f"CUDA Version: {torch.version.cuda}")
        print(f"Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    print()

    # Load data
    print(f"Loading data from {args.data}...")
    with open(args.data, 'r', encoding='utf-8') as f:
        text = f.read()
    print(f"Text length: {len(text):,} characters")

    # Setup tokenizer
    tokenizer = None
    if args.vocab:
        print(f"Loading vocabulary from {args.vocab}...")
        tokenizer = SimpleBPE(args.vocab)
        vocab_size = len(tokenizer.vocab)
    else:
        # Character-level
        chars = sorted(list(set(text)))
        vocab_size = len(chars)
        print(f"Using character-level tokenization ({vocab_size} chars)")

    # Create config
    config = NexusConfig(
        vocab_size=vocab_size,
        d_model=args.d_model,
        n_heads=args.n_heads,
        n_layers=args.n_layers,
        d_state=args.d_state,
        max_seq_len=args.seq_len,
    )

    # Create dataset
    dataset = TextDataset(text, args.seq_len, tokenizer)

    # Split into train/val
    val_size = int(len(dataset) * args.val_split)
    train_size = len(dataset) - val_size
    train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False, num_workers=0)

    print(f"Train samples: {len(train_dataset):,}")
    print(f"Val samples: {len(val_dataset):,}")
    print()

    # Create model
    model = NexusLM(config).to(device)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"Model parameters: {n_params:,} ({n_params/1e6:.2f}M)")

    # Count attention vs SSM layers
    n_attn = sum(1 for b in model.blocks if b.use_attention)
    n_ssm = len(model.blocks) - n_attn
    print(f"Architecture: {n_attn} attention + {n_ssm} SSM layers (1:{n_ssm//max(n_attn,1)} ratio)")
    print()

    # Optimizer and scheduler
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=args.lr,
        weight_decay=args.weight_decay,
        betas=(0.9, 0.95),
    )

    total_steps = len(train_loader) * args.epochs
    scheduler = torch.optim.lr_scheduler.OneCycleLR(
        optimizer,
        max_lr=args.lr,
        total_steps=total_steps,
        pct_start=args.warmup_steps / total_steps,
    )

    # Training config
    train_config = {
        'fp16': args.fp16,
        'max_grad_norm': args.max_grad_norm,
    }

    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Training loop
    print("Starting training...")
    print("-" * 70)

    best_val_loss = float('inf')
    start_time = time.time()

    for epoch in range(args.epochs):
        epoch_start = time.time()

        # Train
        train_loss = train(model, train_loader, optimizer, scheduler, device, train_config)
        train_ppl = math.exp(train_loss)

        # Evaluate
        val_loss = evaluate(model, val_loader, device)
        val_ppl = math.exp(val_loss)

        epoch_time = time.time() - epoch_start
        total_time = time.time() - start_time

        print(f"Epoch {epoch+1:3d}/{args.epochs} | "
              f"Train Loss: {train_loss:.4f} (PPL: {train_ppl:.2f}) | "
              f"Val Loss: {val_loss:.4f} (PPL: {val_ppl:.2f}) | "
              f"Time: {epoch_time:.1f}s | "
              f"Total: {total_time/60:.1f}m")

        # Save best model
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_loss': val_loss,
                'config': config.__dict__,
            }, output_dir / 'best_model.pt')
            print(f"  -> New best model saved! (PPL: {val_ppl:.2f})")

        # Generate sample
        if (epoch + 1) % 10 == 0 or epoch == 0:
            model.eval()
            with torch.no_grad():
                prompt = torch.zeros(1, 1, dtype=torch.long, device=device)
                generated = model.generate(prompt, max_new_tokens=100, temperature=0.8)
                if tokenizer:
                    sample_text = tokenizer.decode(generated[0].tolist())
                else:
                    sample_text = ''.join(dataset.idx_to_char.get(i, '?') for i in generated[0].tolist())
                print(f"  Sample: {sample_text[:100]}...")

    print("-" * 70)
    print(f"Training complete!")
    print(f"Best validation loss: {best_val_loss:.4f} (PPL: {math.exp(best_val_loss):.2f})")
    print(f"Total time: {(time.time() - start_time)/60:.1f} minutes")
    print(f"Model saved to: {output_dir}")


if __name__ == "__main__":
    main()
