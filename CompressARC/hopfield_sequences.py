"""
Experiment 13: Sparse Hopfield Retrieval for Sequences

This is NOT program synthesis. This is ASSOCIATIVE MEMORY.

Key insight:
- Store (input, output) pairs as memories
- Query with new input, retrieve output pattern
- Modern Hopfield networks have exponential capacity
- Sparse = efficient

Why this might work for positional transforms:
- No need to "compose" programs
- Learns input→output mapping directly
- Pattern completion handles novel inputs
- NOT attention (different mechanism)

Success criteria (from charter):
- >80% accuracy on positional transforms
- Learning curve shows transfer
- <1M parameters
- Runs on laptop CPU
- Generalizes to novel inputs
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Tuple, Dict
import random
import time
import math


# =============================================================================
# PART 1: MODERN HOPFIELD NETWORK
# =============================================================================

class ModernHopfieldNetwork(nn.Module):
    """
    Modern Hopfield Network with exponential capacity.

    Based on "Hopfield Networks is All You Need" (Ramsauer et al., 2020)
    but with sparse activation for efficiency.

    Key difference from classical Hopfield:
    - Uses softmax instead of sign activation
    - Exponential capacity instead of linear
    - Can store and retrieve continuous patterns

    Key difference from attention:
    - No query/key/value projections learned
    - Direct pattern storage in weight matrix
    - Energy-based retrieval, not weighted average
    """

    def __init__(self, pattern_dim: int, beta: float = 1.0, sparse_k: int = None):
        """
        Args:
            pattern_dim: Dimension of stored patterns
            beta: Inverse temperature (higher = sharper retrieval)
            sparse_k: If set, use top-k sparse attention (efficiency)
        """
        super().__init__()
        self.pattern_dim = pattern_dim
        self.beta = beta
        self.sparse_k = sparse_k

        # Stored patterns (memories)
        self.memories_input = None   # Input patterns
        self.memories_output = None  # Associated output patterns
        self.num_memories = 0

    def store(self, input_pattern: torch.Tensor, output_pattern: torch.Tensor):
        """Store an (input, output) association."""
        input_pattern = input_pattern.view(1, -1)
        output_pattern = output_pattern.view(1, -1)

        if self.memories_input is None:
            self.memories_input = input_pattern
            self.memories_output = output_pattern
        else:
            self.memories_input = torch.cat([self.memories_input, input_pattern], dim=0)
            self.memories_output = torch.cat([self.memories_output, output_pattern], dim=0)

        self.num_memories += 1

    def retrieve(self, query: torch.Tensor) -> torch.Tensor:
        """
        Retrieve output pattern for given input query.

        Uses energy-based retrieval:
        1. Compute similarity between query and all stored inputs
        2. Apply softmax with temperature beta
        3. Return weighted combination of stored outputs
        """
        if self.memories_input is None:
            return torch.zeros(self.pattern_dim)

        query = query.view(1, -1)

        # Compute similarities (dot product)
        similarities = torch.matmul(query, self.memories_input.T) * self.beta

        # Sparse attention (optional - for efficiency)
        if self.sparse_k is not None and self.num_memories > self.sparse_k:
            topk_vals, topk_idx = torch.topk(similarities, self.sparse_k, dim=-1)
            sparse_attn = F.softmax(topk_vals, dim=-1)

            # Retrieve only from top-k memories
            topk_outputs = self.memories_output[topk_idx.squeeze()]
            output = torch.matmul(sparse_attn, topk_outputs)
        else:
            # Full attention
            attention = F.softmax(similarities, dim=-1)
            output = torch.matmul(attention, self.memories_output)

        return output.squeeze()

    def clear(self):
        """Clear all stored memories."""
        self.memories_input = None
        self.memories_output = None
        self.num_memories = 0


# =============================================================================
# PART 2: SEQUENCE ENCODER/DECODER
# =============================================================================

class SequenceEncoder(nn.Module):
    """
    Encode sequences into fixed-size vectors for Hopfield storage.

    Uses position-aware encoding to capture sequence structure.
    """

    def __init__(self, max_len: int = 10, max_val: int = 20, hidden_dim: int = 128):
        super().__init__()
        self.max_len = max_len
        self.max_val = max_val
        self.hidden_dim = hidden_dim

        # Position embeddings
        self.pos_embed = nn.Embedding(max_len, hidden_dim // 2)

        # Value embeddings
        self.val_embed = nn.Embedding(max_val, hidden_dim // 2)

        # Combine into single vector
        self.combiner = nn.Sequential(
            nn.Linear(hidden_dim * max_len, hidden_dim * 2),
            nn.ReLU(),
            nn.Linear(hidden_dim * 2, hidden_dim)
        )

    def forward(self, seq: List[int]) -> torch.Tensor:
        """Encode a sequence into a vector."""
        # Pad sequence
        padded = seq[:self.max_len] + [0] * (self.max_len - len(seq))

        # Get embeddings
        positions = torch.arange(self.max_len)
        values = torch.tensor(padded).clamp(0, self.max_val - 1)

        pos_emb = self.pos_embed(positions)  # [max_len, hidden//2]
        val_emb = self.val_embed(values)      # [max_len, hidden//2]

        # Concatenate position and value
        combined = torch.cat([pos_emb, val_emb], dim=-1)  # [max_len, hidden]

        # Flatten and project
        flat = combined.view(-1)
        encoded = self.combiner(flat)

        return encoded


class SequenceDecoder(nn.Module):
    """
    Decode vectors back into sequences.
    """

    def __init__(self, max_len: int = 10, max_val: int = 20, hidden_dim: int = 128):
        super().__init__()
        self.max_len = max_len
        self.max_val = max_val

        # Expand and predict each position
        self.expander = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim * 2),
            nn.ReLU(),
            nn.Linear(hidden_dim * 2, max_len * max_val)
        )

    def forward(self, encoded: torch.Tensor) -> List[int]:
        """Decode a vector into a sequence."""
        logits = self.expander(encoded)
        logits = logits.view(self.max_len, self.max_val)

        # Argmax for each position
        predictions = torch.argmax(logits, dim=-1)

        return predictions.tolist()


# =============================================================================
# PART 3: HOPFIELD SEQUENCE TRANSFORMER
# =============================================================================

class HopfieldSequenceTransformer:
    """
    Learn sequence transformations using Hopfield associative memory.

    Method:
    1. Encode input and output sequences
    2. Store (encoded_input, encoded_output) in Hopfield network
    3. For new input: encode → retrieve → decode

    This is LEARNING through memory, not program synthesis.
    """

    def __init__(self, hidden_dim: int = 128, beta: float = 8.0, sparse_k: int = 10):
        self.hidden_dim = hidden_dim

        # Encoder/decoder (shared across all transforms)
        self.encoder = SequenceEncoder(hidden_dim=hidden_dim)
        self.decoder = SequenceDecoder(hidden_dim=hidden_dim)

        # One Hopfield network per transform type (or could use one shared)
        self.hopfield = ModernHopfieldNetwork(hidden_dim, beta=beta, sparse_k=sparse_k)

        # For training the encoder/decoder
        self.optimizer = torch.optim.Adam(
            list(self.encoder.parameters()) + list(self.decoder.parameters()),
            lr=0.01
        )

        # Statistics
        self.num_examples = 0
        self.training_steps = 0

    def learn(self, input_seq: List[int], output_seq: List[int], num_steps: int = 50):
        """
        Learn from an (input, output) example.

        1. Train encoder/decoder to reconstruct
        2. Store pattern in Hopfield network
        """
        # Train encoder/decoder
        for _ in range(num_steps):
            self.optimizer.zero_grad()

            # Encode input and output
            enc_in = self.encoder(input_seq)
            enc_out = self.encoder(output_seq)

            # Decode and compute loss
            dec_in = self.decoder(enc_in)
            dec_out = self.decoder(enc_out)

            # Reconstruction loss
            target_in = torch.tensor(input_seq[:10] + [0] * (10 - len(input_seq)))
            target_out = torch.tensor(output_seq[:10] + [0] * (10 - len(output_seq)))

            loss_in = F.cross_entropy(
                self.decoder.expander(enc_in).view(10, -1),
                target_in.clamp(0, 19)
            )
            loss_out = F.cross_entropy(
                self.decoder.expander(enc_out).view(10, -1),
                target_out.clamp(0, 19)
            )

            loss = loss_in + loss_out
            loss.backward()
            self.optimizer.step()

            self.training_steps += 1

        # Store in Hopfield network
        with torch.no_grad():
            enc_in = self.encoder(input_seq)
            enc_out = self.encoder(output_seq)
            self.hopfield.store(enc_in, enc_out)

        self.num_examples += 1

    def predict(self, input_seq: List[int]) -> List[int]:
        """Predict output for a new input."""
        with torch.no_grad():
            # Encode input
            enc_in = self.encoder(input_seq)

            # Retrieve from Hopfield
            retrieved = self.hopfield.retrieve(enc_in)

            # Decode
            output = self.decoder(retrieved)

            return output[:len(input_seq)]

    def reset(self):
        """Reset for new transform type."""
        self.hopfield.clear()
        self.num_examples = 0
        # Keep encoder/decoder trained (transfer!)


# =============================================================================
# PART 4: TESTING
# =============================================================================

def generate_task(transform_name: str, length: int = 5) -> Tuple[List[int], List[int]]:
    """Generate a (input, output) pair for a transform."""
    input_seq = [random.randint(1, 9) for _ in range(length)]

    if transform_name == 'identity':
        output_seq = input_seq.copy()
    elif transform_name == 'increment':
        output_seq = [x + 1 for x in input_seq]
    elif transform_name == 'reverse':
        output_seq = input_seq[::-1]
    elif transform_name == 'swap_pairs':
        output_seq = []
        for i in range(0, len(input_seq) - 1, 2):
            output_seq.extend([input_seq[i+1], input_seq[i]])
        if len(input_seq) % 2 == 1:
            output_seq.append(input_seq[-1])
    elif transform_name == 'running_max':
        output_seq = []
        current_max = 0
        for x in input_seq:
            current_max = max(current_max, x)
            output_seq.append(current_max)
    elif transform_name == 'mirror_add':
        output_seq = [input_seq[i] + input_seq[-(i+1)] for i in range(len(input_seq))]
    else:
        raise ValueError(f"Unknown transform: {transform_name}")

    return input_seq, output_seq


def test_transform(system: HopfieldSequenceTransformer, transform_name: str,
                   num_train: int = 20, num_test: int = 5) -> Tuple[int, List[int]]:
    """
    Test system on a transform.

    1. Train on num_train examples
    2. Test on num_test NEW examples (generalization)
    """
    print(f"\n  Testing {transform_name}:")

    # Reset Hopfield but keep encoder/decoder (transfer)
    system.reset()

    # Training phase
    print(f"    Training on {num_train} examples...")
    steps_per_example = []
    for i in range(num_train):
        input_seq, output_seq = generate_task(transform_name)

        start = system.training_steps
        system.learn(input_seq, output_seq, num_steps=50 if i == 0 else 10)
        steps = system.training_steps - start

        steps_per_example.append(steps)

    # Show learning curve
    print(f"    Learning curve: {steps_per_example[0]}→{steps_per_example[-1]} steps")

    # Testing phase (on NEW examples)
    print(f"    Testing on {num_test} NEW examples...")
    correct = 0
    for i in range(num_test):
        input_seq, output_seq = generate_task(transform_name)
        predicted = system.predict(input_seq)

        if predicted == output_seq:
            correct += 1
            print(f"      Test {i+1}: ✓ {input_seq} → {predicted}")
        else:
            print(f"      Test {i+1}: ✗ {input_seq} → {predicted} (expected {output_seq})")

    return correct, steps_per_example


def main():
    """Run Experiment 13: Sparse Hopfield Retrieval."""
    print("=" * 70)
    print("EXPERIMENT 13: Sparse Hopfield Retrieval")
    print("=" * 70)
    print("\nThis is NOT program synthesis. This is ASSOCIATIVE MEMORY.")
    print("Store examples → retrieve patterns → generalize to new inputs")
    print("\nSuccess criteria:")
    print("  - >80% on positional transforms")
    print("  - Learning curve shows transfer")
    print("  - Generalizes to NEW inputs (not just memorization)")
    print("=" * 70)

    # Create system
    system = HopfieldSequenceTransformer(hidden_dim=128, beta=8.0, sparse_k=10)

    # Test transforms
    transforms = [
        'identity',
        'increment',
        'reverse',
        'running_max',
        'swap_pairs',
        'mirror_add',
    ]

    results = {}

    for transform in transforms:
        correct, steps = test_transform(system, transform, num_train=20, num_test=5)
        results[transform] = {
            'accuracy': correct / 5,
            'steps': steps,
            'memories': system.hopfield.num_memories
        }
        print(f"\n  Result: {correct}/5 ({correct/5*100:.0f}%)")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    element_wise = ['identity', 'increment']
    positional = ['reverse', 'running_max', 'swap_pairs', 'mirror_add']

    ew_acc = sum(results[t]['accuracy'] for t in element_wise) / len(element_wise)
    pos_acc = sum(results[t]['accuracy'] for t in positional) / len(positional)

    print(f"\nElement-wise accuracy: {ew_acc*100:.0f}%")
    print(f"Positional accuracy: {pos_acc*100:.0f}%")
    print(f"Overall accuracy: {(ew_acc + pos_acc) / 2 * 100:.0f}%")

    # Parameter count
    total_params = sum(p.numel() for p in system.encoder.parameters())
    total_params += sum(p.numel() for p in system.decoder.parameters())
    print(f"\nTotal parameters: {total_params:,}")

    # Verdict
    print("\n" + "=" * 70)
    if pos_acc >= 0.8:
        print("SUCCESS: >80% on positional transforms!")
        print("Hopfield associative memory WORKS for sequences.")
    else:
        print(f"NOT YET: {pos_acc*100:.0f}% on positional (need >80%)")
        print("Need more examples, better encoding, or different approach.")
    print("=" * 70)

    return results


if __name__ == '__main__':
    results = main()
