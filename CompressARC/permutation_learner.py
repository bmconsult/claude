"""
Experiment 15: Learned Permutation Matrix for Positional Transforms

Key insight: reverse, swap_pairs, rotate, etc. are all PERMUTATIONS.
A permutation is just a matrix that maps input positions to output positions.

This is NOT attention:
- No query/key/value projections
- No softmax over content
- Just learns: position i → position j

This is NOT an LLM:
- Tiny (seq_len × seq_len matrix = 25 params for len-5)
- Task-specific
- MDL objective

Method:
1. Learn a soft permutation matrix using Sinkhorn normalization
2. Apply to input sequence
3. MDL loss = reconstruction + description_length(permutation)

Sinkhorn normalization: repeatedly normalize rows and columns
to get a doubly-stochastic matrix (valid soft permutation).
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Tuple
import random


def sinkhorn_normalize(log_alpha: torch.Tensor, n_iters: int = 20) -> torch.Tensor:
    """
    Sinkhorn normalization: convert arbitrary matrix to doubly-stochastic.

    A doubly-stochastic matrix has rows and columns that sum to 1.
    This is a "soft permutation" - can be discretized to hard permutation.

    Args:
        log_alpha: Unnormalized log-weights [N, N]
        n_iters: Number of Sinkhorn iterations

    Returns:
        Doubly-stochastic matrix [N, N]
    """
    for _ in range(n_iters):
        # Normalize rows
        log_alpha = log_alpha - torch.logsumexp(log_alpha, dim=1, keepdim=True)
        # Normalize columns
        log_alpha = log_alpha - torch.logsumexp(log_alpha, dim=0, keepdim=True)

    return torch.exp(log_alpha)


class PermutationLearner(nn.Module):
    """
    Learn a permutation that transforms input to output.

    For each (input, output) pair, we learn a permutation matrix P such that:
        output = P @ input

    The permutation is learned via gradient descent on reconstruction loss.
    MDL regularization encourages simpler permutations (closer to identity or
    known patterns).
    """

    def __init__(self, max_len: int = 10):
        super().__init__()
        self.max_len = max_len

        # Learnable log-weights for permutation matrix
        # Initialize close to identity (diagonal = high)
        self.log_alpha = nn.Parameter(torch.zeros(max_len, max_len))
        nn.init.eye_(self.log_alpha)
        self.log_alpha.data *= 5  # Make identity strong initially

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Apply learned permutation to input.

        Args:
            x: Input sequence [seq_len] or [batch, seq_len]

        Returns:
            Permuted sequence
        """
        seq_len = x.shape[-1]

        # Get permutation matrix for this length
        perm = sinkhorn_normalize(self.log_alpha[:seq_len, :seq_len])

        # Apply permutation: output[i] = sum_j perm[i,j] * input[j]
        if x.dim() == 1:
            return perm @ x.float()
        else:
            return (perm @ x.float().unsqueeze(-1)).squeeze(-1)

    def get_hard_permutation(self, seq_len: int) -> torch.Tensor:
        """Get discrete permutation (argmax each row)."""
        perm = sinkhorn_normalize(self.log_alpha[:seq_len, :seq_len])
        return torch.argmax(perm, dim=1)

    def description_length(self, seq_len: int) -> float:
        """
        MDL: Description length of the permutation.

        Simpler permutations (identity, reverse) have lower DL.
        Complex permutations need more bits to describe.
        """
        perm = sinkhorn_normalize(self.log_alpha[:seq_len, :seq_len])

        # Entropy of the permutation matrix
        # Lower entropy = more deterministic = simpler
        entropy = -torch.sum(perm * torch.log(perm + 1e-10))

        # Distance from identity (identity = simplest)
        identity = torch.eye(seq_len)
        dist_from_identity = torch.sum((perm - identity) ** 2)

        return entropy.item() + 0.1 * dist_from_identity.item()


class SequencePermutationSystem:
    """
    Learn sequence transformations as permutations.

    For each transform type, we learn a permutation matrix.
    Transfer: the learned permutation generalizes to new inputs of same length.

    IMPORTANT: Uses BATCH training for reliable convergence.
    """

    def __init__(self, max_len: int = 10):
        self.max_len = max_len
        self.learner = PermutationLearner(max_len)
        self.optimizer = torch.optim.Adam(self.learner.parameters(), lr=0.5)

        # Store examples for batch training
        self.examples: List[Tuple[torch.Tensor, torch.Tensor]] = []
        self.steps_history = []

    def add_example(self, input_seq: List[int], output_seq: List[int]):
        """Add training example to batch."""
        x = torch.tensor(input_seq, dtype=torch.float32)
        y = torch.tensor(output_seq, dtype=torch.float32)
        self.examples.append((x, y))

    def train_batch(self, max_steps: int = 500, threshold: float = 0.01) -> int:
        """Train on all examples simultaneously (batch training)."""
        if not self.examples:
            return 0

        for step in range(max_steps):
            self.optimizer.zero_grad()

            total_loss = 0
            for x, y in self.examples:
                pred = self.learner(x)
                total_loss += F.mse_loss(pred, y)
            total_loss /= len(self.examples)

            if total_loss.item() < threshold:
                self.steps_history.append(step + 1)
                return step + 1

            total_loss.backward()
            self.optimizer.step()

        self.steps_history.append(max_steps)
        return max_steps

    def learn(self, input_seq: List[int], output_seq: List[int],
              max_steps: int = 100, threshold: float = 0.01) -> int:
        """
        Learn permutation from (input, output) example.

        For reliable results, use add_example() + train_batch() instead.
        This method is kept for backward compatibility.
        """
        self.add_example(input_seq, output_seq)
        return self.train_batch(max_steps, threshold)

    def predict(self, input_seq: List[int]) -> List[int]:
        """Apply learned permutation to new input."""
        x = torch.tensor(input_seq, dtype=torch.float32)

        with torch.no_grad():
            pred = self.learner(x)

        # Round to nearest integer
        return [round(v.item()) for v in pred]

    def reset(self):
        """Reset for new transform type."""
        # Re-initialize permutation to identity
        nn.init.eye_(self.learner.log_alpha)
        self.learner.log_alpha.data *= 5
        self.steps_history = []

        # Reset optimizer
        self.optimizer = torch.optim.Adam(self.learner.parameters(), lr=0.5)


def generate_task(transform_name: str, length: int = 5) -> Tuple[List[int], List[int]]:
    """Generate (input, output) pair for a transform."""
    # Ensure all values are DISTINCT to avoid ambiguity
    input_seq = random.sample(range(1, 10), length)

    if transform_name == 'identity':
        output_seq = input_seq.copy()
    elif transform_name == 'reverse':
        output_seq = input_seq[::-1]
    elif transform_name == 'swap_pairs':
        output_seq = []
        for i in range(0, len(input_seq) - 1, 2):
            output_seq.extend([input_seq[i+1], input_seq[i]])
        if len(input_seq) % 2 == 1:
            output_seq.append(input_seq[-1])
    elif transform_name == 'rotate_left':
        output_seq = input_seq[1:] + [input_seq[0]]
    elif transform_name == 'rotate_right':
        output_seq = [input_seq[-1]] + input_seq[:-1]
    else:
        raise ValueError(f"Unknown transform: {transform_name}")

    return input_seq, output_seq


def test_transform(system: SequencePermutationSystem, transform_name: str,
                   num_train: int = 10, num_test: int = 5) -> Tuple[int, List[int]]:
    """Test system on a transform."""
    print(f"\n  Testing {transform_name}:")

    # Reset for new transform
    system.reset()

    # Training phase
    print(f"    Training on {num_train} examples...")
    for i in range(num_train):
        input_seq, output_seq = generate_task(transform_name)
        steps = system.learn(input_seq, output_seq)
        print(f"      Example {i+1}: {steps} steps | {input_seq} → {output_seq}")

    # Show learned permutation
    perm = system.learner.get_hard_permutation(5)
    print(f"    Learned permutation: {perm.tolist()}")

    # Testing phase
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

    return correct, system.steps_history


def main():
    """Run Experiment 15: Learned Permutation Matrix."""
    print("=" * 70)
    print("EXPERIMENT 15: Learned Permutation Matrix")
    print("=" * 70)
    print("\nKey insight: positional transforms ARE permutations.")
    print("Learn the permutation matrix, apply to any input.")
    print("\nThis is NOT attention, NOT an LLM.")
    print("Just: which position maps to which position.")
    print("=" * 70)

    system = SequencePermutationSystem(max_len=10)

    # Test POSITIONAL transforms (what we've been failing on)
    transforms = [
        'identity',
        'reverse',
        'swap_pairs',
        'rotate_left',
        'rotate_right',
    ]

    results = {}

    for transform in transforms:
        correct, steps = test_transform(system, transform)
        results[transform] = {
            'accuracy': correct / 5,
            'steps': steps
        }
        print(f"\n  Result: {correct}/5 ({correct/5*100:.0f}%)")
        print(f"  Learning curve: {steps}")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    positional = ['reverse', 'swap_pairs', 'rotate_left', 'rotate_right']
    pos_acc = sum(results[t]['accuracy'] for t in positional) / len(positional)

    print(f"\nPositional accuracy: {pos_acc*100:.0f}%")
    print(f"Parameters: {sum(p.numel() for p in system.learner.parameters())}")

    # Learning curve analysis
    print("\nLearning curves (steps per example):")
    for t in transforms:
        print(f"  {t}: {results[t]['steps']}")

    # Verdict
    print("\n" + "=" * 70)
    if pos_acc >= 0.8:
        print("SUCCESS: >80% on positional transforms!")
        print("Permutation learning WORKS.")
    else:
        print(f"Result: {pos_acc*100:.0f}% on positional")
    print("=" * 70)

    return results


if __name__ == '__main__':
    results = main()
