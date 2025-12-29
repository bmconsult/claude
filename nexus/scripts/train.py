#!/usr/bin/env python3
"""
Nexus Training Script

Usage:
    python scripts/train.py --config config.yaml --data path/to/data --output checkpoints/

Example with PyTorch-style training:
    python scripts/train.py --preset base --epochs 10 --batch-size 32
"""

import argparse
import json
import time
from pathlib import Path
from typing import Optional

import numpy as np

# Try to import Nexus native extension
try:
    import nexus
    NATIVE_AVAILABLE = True
except ImportError:
    NATIVE_AVAILABLE = False
    print("⚠️  Native extension not available. Using PyTorch fallback.")

# Optional: PyTorch integration for training
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import DataLoader, Dataset
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


class SyntheticDataset(Dataset):
    """Synthetic dataset for testing."""

    def __init__(self, n_samples: int, seq_len: int, d_model: int):
        self.n_samples = n_samples
        self.seq_len = seq_len
        self.d_model = d_model

    def __len__(self):
        return self.n_samples

    def __getitem__(self, idx):
        # Generate random embeddings
        x = np.random.randn(self.seq_len, self.d_model).astype(np.float32)
        return torch.from_numpy(x)


def train_with_torch(args):
    """Training loop using PyTorch."""
    print("=" * 60)
    print("NEXUS TRAINING (PyTorch)")
    print("=" * 60)

    # Model configuration
    if args.preset:
        config = nexus.PRESETS.get(args.preset, nexus.PRESETS["base"])
    else:
        config = {
            "d_model": args.d_model,
            "n_heads": args.n_heads,
            "layers_per_block": args.layers,
        }

    print(f"\nConfiguration: {config}")
    print(f"Epochs: {args.epochs}")
    print(f"Batch size: {args.batch_size}")
    print(f"Learning rate: {args.lr}")
    print()

    # Create dataset
    print("Creating synthetic dataset...")
    dataset = SyntheticDataset(
        n_samples=args.n_samples,
        seq_len=args.seq_len,
        d_model=config["d_model"],
    )
    dataloader = DataLoader(
        dataset,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=0,
    )
    print(f"Dataset size: {len(dataset)} samples")
    print(f"Batches per epoch: {len(dataloader)}")
    print()

    # Create simple transformer model for demonstration
    # (In production, this would use the native Nexus model)
    class SimpleTransformer(nn.Module):
        def __init__(self, d_model, n_heads, n_layers):
            super().__init__()
            encoder_layer = nn.TransformerEncoderLayer(
                d_model=d_model,
                nhead=n_heads,
                dim_feedforward=d_model * 4,
                batch_first=True,
            )
            self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=n_layers)
            self.proj = nn.Linear(d_model, d_model)

        def forward(self, x):
            h = self.encoder(x)
            return self.proj(h)

    model = SimpleTransformer(
        d_model=config["d_model"],
        n_heads=config["n_heads"],
        n_layers=config["layers_per_block"],
    )
    n_params = sum(p.numel() for p in model.parameters())
    print(f"Model parameters: {n_params:,}")

    # Optimizer
    optimizer = optim.AdamW(
        model.parameters(),
        lr=args.lr,
        weight_decay=args.weight_decay,
    )

    # Training loop
    print("\nStarting training...")
    print("-" * 60)

    best_loss = float("inf")
    start_time = time.time()

    for epoch in range(args.epochs):
        epoch_loss = 0.0
        n_batches = 0

        for batch in dataloader:
            optimizer.zero_grad()

            # Forward pass (JEPA-style: predict masked positions)
            mask_ratio = 0.3
            seq_len = batch.shape[1]
            n_mask = int(seq_len * mask_ratio)

            # Random mask
            mask_idx = np.random.choice(seq_len, n_mask, replace=False)
            mask = torch.ones(batch.shape[0], seq_len, 1)
            mask[:, mask_idx, :] = 0

            # Masked input
            masked_input = batch * mask

            # Model prediction
            pred = model(masked_input)

            # JEPA loss: reconstruct masked positions in latent space
            loss = nn.functional.mse_loss(
                pred[:, mask_idx, :],
                batch[:, mask_idx, :],
            )

            # Backward pass
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

            epoch_loss += loss.item()
            n_batches += 1

        avg_loss = epoch_loss / n_batches
        elapsed = time.time() - start_time

        print(f"Epoch {epoch + 1}/{args.epochs} | Loss: {avg_loss:.4f} | Time: {elapsed:.1f}s")

        if avg_loss < best_loss:
            best_loss = avg_loss
            if args.output:
                save_path = Path(args.output) / "best_model.pt"
                save_path.parent.mkdir(parents=True, exist_ok=True)
                torch.save(model.state_dict(), save_path)

    print("-" * 60)
    print(f"\nTraining complete!")
    print(f"Best loss: {best_loss:.4f}")
    print(f"Total time: {time.time() - start_time:.1f}s")

    if args.output:
        print(f"Model saved to: {args.output}")


def train_with_native(args):
    """Training loop using native Nexus."""
    print("=" * 60)
    print("NEXUS TRAINING (Native)")
    print("=" * 60)

    # Create configuration
    config = nexus.NexusConfig(
        d_model=args.d_model,
        n_heads=args.n_heads,
        layers_per_block=args.layers,
        memory_size=1024,
    )
    print(f"\nConfiguration: {config}")

    # Create model
    model = nexus.Nexus(config)
    print("Model created!")

    # Create trainer
    train_config = nexus.TrainConfig(
        lr=args.lr,
        batch_size=args.batch_size,
        epochs=args.epochs,
    )
    trainer = nexus.Trainer(config, train_config, args.output or "checkpoints")

    # Generate training data
    print("\nGenerating synthetic data...")
    n_samples = args.n_samples
    seq_len = args.seq_len

    print(f"Training on {n_samples} samples...")

    for epoch in range(args.epochs):
        epoch_loss = 0.0
        n_batches = 0

        for i in range(0, n_samples, args.batch_size):
            # Generate batch
            batch_size = min(args.batch_size, n_samples - i)
            x = np.random.randn(batch_size, seq_len, args.d_model).astype(np.float32)

            # Convert to list for native binding
            x_list = x.tolist()

            # Training step
            total, inv, var, cov = trainer.train_step(model, x_list)

            epoch_loss += total
            n_batches += 1

        avg_loss = epoch_loss / n_batches
        print(f"Epoch {epoch + 1}/{args.epochs} | Loss: {avg_loss:.4f}")

    print("\nTraining complete!")


def main():
    parser = argparse.ArgumentParser(description="Train Nexus model")

    # Model configuration
    parser.add_argument("--preset", type=str, choices=["tiny", "small", "base", "large", "xl"],
                        help="Model preset")
    parser.add_argument("--d-model", type=int, default=512, help="Hidden dimension")
    parser.add_argument("--n-heads", type=int, default=8, help="Number of attention heads")
    parser.add_argument("--layers", type=int, default=8, help="Number of layers")

    # Training configuration
    parser.add_argument("--epochs", type=int, default=10, help="Number of epochs")
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size")
    parser.add_argument("--lr", type=float, default=3e-4, help="Learning rate")
    parser.add_argument("--weight-decay", type=float, default=0.01, help="Weight decay")

    # Data
    parser.add_argument("--n-samples", type=int, default=1000, help="Number of samples")
    parser.add_argument("--seq-len", type=int, default=128, help="Sequence length")

    # Output
    parser.add_argument("--output", type=str, help="Output directory")

    # Backend
    parser.add_argument("--backend", type=str, choices=["native", "torch"], default="torch",
                        help="Training backend")

    args = parser.parse_args()

    if args.backend == "native" and NATIVE_AVAILABLE:
        train_with_native(args)
    elif TORCH_AVAILABLE:
        train_with_torch(args)
    else:
        print("ERROR: No backend available!")
        print("Install PyTorch: pip install torch")
        print("Or build native extension: maturin develop")


if __name__ == "__main__":
    main()
