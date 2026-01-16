"""
Experiment 16: Value Transforms (not just permutations)

Permutation learner handles: reverse, swap, rotate (position changes)
But some transforms also change VALUES: running_max, mirror_add, increment

This system learns BOTH:
1. Permutation matrix (which position maps where)
2. Value transformation (what happens to the value)

Architecture:
- Permutation layer (Sinkhorn normalization)
- Value layer (small MLP that transforms values based on context)
- Combined with MDL objective

Still NOT an LLM:
- Tiny: ~1000 parameters
- Task-specific
- MDL-regularized
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Tuple
import random


def sinkhorn_normalize(log_alpha: torch.Tensor, n_iters: int = 20) -> torch.Tensor:
    """Convert matrix to doubly-stochastic (soft permutation)."""
    for _ in range(n_iters):
        log_alpha = log_alpha - torch.logsumexp(log_alpha, dim=1, keepdim=True)
        log_alpha = log_alpha - torch.logsumexp(log_alpha, dim=0, keepdim=True)
    return torch.exp(log_alpha)


class ValueTransformLearner(nn.Module):
    """
    Learn sequence transformations that involve BOTH:
    - Position changes (permutation)
    - Value changes (computation)

    Examples:
    - running_max: output[i] = max(input[0:i+1])
    - mirror_add: output[i] = input[i] + input[N-1-i]
    - increment: output[i] = input[i] + 1
    """

    def __init__(self, max_len: int = 10, hidden_dim: int = 32):
        super().__init__()
        self.max_len = max_len
        self.hidden_dim = hidden_dim

        # Permutation matrix (for position transforms)
        self.log_alpha = nn.Parameter(torch.zeros(max_len, max_len))
        nn.init.eye_(self.log_alpha)
        self.log_alpha.data *= 3

        # Value transformation network
        # Input: position, value, and context (neighboring values)
        self.value_net = nn.Sequential(
            nn.Linear(max_len + 1, hidden_dim),  # all values + position
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )

        # Blend between permutation-only and value-transform
        self.use_value_transform = nn.Parameter(torch.tensor(0.0))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Apply learned transformation."""
        seq_len = x.shape[-1]

        # Get permutation matrix
        perm = sinkhorn_normalize(self.log_alpha[:seq_len, :seq_len])

        # Apply permutation
        permuted = perm @ x.float()

        # Apply value transformation
        # For each position, compute new value based on all input values
        value_transformed = torch.zeros_like(x, dtype=torch.float32)

        for i in range(seq_len):
            # Input to value net: all values + position indicator
            pos_indicator = torch.zeros(self.max_len)
            pos_indicator[i] = 1.0
            full_input = torch.zeros(self.max_len)
            full_input[:seq_len] = x.float()
            net_input = torch.cat([full_input, torch.tensor([i / seq_len])])
            value_transformed[i] = self.value_net(net_input).squeeze()

        # Blend permutation and value transform based on learned weight
        blend = torch.sigmoid(self.use_value_transform)
        output = (1 - blend) * permuted + blend * value_transformed

        return output

    def get_hard_permutation(self, seq_len: int) -> torch.Tensor:
        """Get discrete permutation."""
        perm = sinkhorn_normalize(self.log_alpha[:seq_len, :seq_len])
        return torch.argmax(perm, dim=1)


class FullSequenceSystem:
    """
    Complete system for all sequence transforms.

    Handles:
    - Pure permutations (reverse, swap, rotate)
    - Value transforms (increment, running_max, mirror_add)
    """

    def __init__(self, max_len: int = 10):
        self.max_len = max_len
        self.learner = ValueTransformLearner(max_len)
        self.optimizer = torch.optim.Adam(self.learner.parameters(), lr=0.1)
        self.steps_history = []

    def learn(self, input_seq: List[int], output_seq: List[int],
              max_steps: int = 200, threshold: float = 0.5) -> int:
        """Learn from example."""
        x = torch.tensor(input_seq, dtype=torch.float32)
        y = torch.tensor(output_seq, dtype=torch.float32)

        for step in range(max_steps):
            self.optimizer.zero_grad()

            pred = self.learner(x)
            loss = F.mse_loss(pred, y)

            if loss.item() < threshold:
                self.steps_history.append(step + 1)
                return step + 1

            loss.backward()
            self.optimizer.step()

        self.steps_history.append(max_steps)
        return max_steps

    def predict(self, input_seq: List[int]) -> List[int]:
        """Apply learned transform."""
        x = torch.tensor(input_seq, dtype=torch.float32)
        with torch.no_grad():
            pred = self.learner(x)
        return [round(v.item()) for v in pred]

    def reset(self):
        """Reset for new transform."""
        self.learner = ValueTransformLearner(self.max_len)
        self.optimizer = torch.optim.Adam(self.learner.parameters(), lr=0.1)
        self.steps_history = []


def generate_task(transform_name: str, length: int = 5) -> Tuple[List[int], List[int]]:
    """Generate (input, output) pair."""
    input_seq = random.sample(range(1, 10), length)

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
    elif transform_name == 'rotate_left':
        output_seq = input_seq[1:] + [input_seq[0]]
    else:
        raise ValueError(f"Unknown transform: {transform_name}")

    return input_seq, output_seq


def test_transform(system: FullSequenceSystem, transform_name: str,
                   num_train: int = 15, num_test: int = 5) -> Tuple[int, List[int]]:
    """Test on a transform."""
    print(f"\n  Testing {transform_name}:")
    system.reset()

    # Training
    print(f"    Training on {num_train} examples...")
    for i in range(num_train):
        input_seq, output_seq = generate_task(transform_name)
        steps = system.learn(input_seq, output_seq)
        if i < 3 or i >= num_train - 2:
            print(f"      Example {i+1}: {steps} steps")

    # Testing
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
    """Run Experiment 16: Full value transform learning."""
    print("=" * 70)
    print("EXPERIMENT 16: Full Value Transform Learning")
    print("=" * 70)
    print("\nHandles BOTH permutation AND value transforms:")
    print("  - Permutations: reverse, swap, rotate")
    print("  - Value changes: increment, running_max, mirror_add")
    print("=" * 70)

    system = FullSequenceSystem(max_len=10)

    transforms = [
        'identity',
        'increment',
        'reverse',
        'swap_pairs',
        'rotate_left',
        'running_max',
        'mirror_add',
    ]

    results = {}

    for transform in transforms:
        correct, steps = test_transform(system, transform)
        results[transform] = {
            'accuracy': correct / 5,
            'steps': steps
        }
        print(f"\n  Result: {correct}/5 ({correct/5*100:.0f}%)")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    permutation = ['reverse', 'swap_pairs', 'rotate_left']
    value = ['increment', 'running_max', 'mirror_add']

    perm_acc = sum(results[t]['accuracy'] for t in permutation) / len(permutation)
    val_acc = sum(results[t]['accuracy'] for t in value) / len(value)
    overall = sum(results[t]['accuracy'] for t in transforms) / len(transforms)

    print(f"\nPermutation transforms: {perm_acc*100:.0f}%")
    print(f"Value transforms: {val_acc*100:.0f}%")
    print(f"Overall: {overall*100:.0f}%")

    params = sum(p.numel() for p in system.learner.parameters())
    print(f"\nParameters: {params}")

    print("\n" + "=" * 70)
    if overall >= 0.8:
        print("SUCCESS: >80% overall!")
    else:
        print(f"Result: {overall*100:.0f}%")
    print("=" * 70)

    return results


if __name__ == '__main__':
    main()
