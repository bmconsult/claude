"""
RIGOROUS TESTING v2 - with proper isolation
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Tuple
import random

def sinkhorn_normalize(log_alpha: torch.Tensor, n_iters: int = 20) -> torch.Tensor:
    for _ in range(n_iters):
        log_alpha = log_alpha - torch.logsumexp(log_alpha, dim=1, keepdim=True)
        log_alpha = log_alpha - torch.logsumexp(log_alpha, dim=0, keepdim=True)
    return torch.exp(log_alpha)


class PermutationLearner(nn.Module):
    def __init__(self, max_len: int = 10):
        super().__init__()
        self.max_len = max_len
        self.log_alpha = nn.Parameter(torch.zeros(max_len, max_len))
        nn.init.eye_(self.log_alpha)
        self.log_alpha.data *= 5

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        seq_len = x.shape[-1]
        perm = sinkhorn_normalize(self.log_alpha[:seq_len, :seq_len])
        return perm @ x.float()

    def get_hard_permutation(self, seq_len: int) -> torch.Tensor:
        perm = sinkhorn_normalize(self.log_alpha[:seq_len, :seq_len])
        return torch.argmax(perm, dim=1)


class SequencePermutationSystem:
    def __init__(self, max_len: int = 10):
        self.max_len = max_len
        self.learner = PermutationLearner(max_len)
        self.optimizer = torch.optim.Adam(self.learner.parameters(), lr=0.5)

    def learn(self, input_seq: List[int], output_seq: List[int],
              max_steps: int = 100, threshold: float = 0.01) -> int:
        x = torch.tensor(input_seq, dtype=torch.float32)
        y = torch.tensor(output_seq, dtype=torch.float32)

        for step in range(max_steps):
            self.optimizer.zero_grad()
            pred = self.learner(x)
            loss = F.mse_loss(pred, y)
            if loss.item() < threshold:
                return step + 1
            loss.backward()
            self.optimizer.step()
        return max_steps

    def predict(self, input_seq: List[int]) -> List[int]:
        x = torch.tensor(input_seq, dtype=torch.float32)
        with torch.no_grad():
            pred = self.learner(x)
        return [round(v.item()) for v in pred]

    def reset(self):
        nn.init.eye_(self.learner.log_alpha)
        self.learner.log_alpha.data *= 5
        self.optimizer = torch.optim.Adam(self.learner.parameters(), lr=0.5)


def apply_transform(transform_name: str, input_seq: List[int]) -> List[int]:
    if transform_name == 'identity':
        return input_seq.copy()
    elif transform_name == 'reverse':
        return input_seq[::-1]
    elif transform_name == 'swap_pairs':
        output = []
        for i in range(0, len(input_seq) - 1, 2):
            output.extend([input_seq[i+1], input_seq[i]])
        if len(input_seq) % 2 == 1:
            output.append(input_seq[-1])
        return output
    elif transform_name == 'rotate_left':
        return input_seq[1:] + [input_seq[0]]
    elif transform_name == 'rotate_right':
        return [input_seq[-1]] + input_seq[:-1]
    else:
        raise ValueError(f"Unknown: {transform_name}")


def test_isolated():
    print("=" * 70)
    print("RIGOROUS ISOLATED TESTING")
    print("=" * 70)

    # TEST 1: Each transform, fresh system, large sample
    print("\n### TEST 1: LARGE-SCALE ISOLATED (fresh system per transform)")

    transforms = ['identity', 'reverse', 'swap_pairs', 'rotate_left', 'rotate_right']

    for transform in transforms:
        # FRESH system
        system = SequencePermutationSystem()

        # Train on 15 distinct examples
        for _ in range(15):
            inp = random.sample(range(1, 10), 5)
            out = apply_transform(transform, inp)
            system.learn(inp, out)

        perm = system.learner.get_hard_permutation(5)

        # Test on 50 novel examples
        correct = 0
        for _ in range(50):
            inp = random.sample(range(1, 10), 5)
            out = apply_transform(transform, inp)
            pred = system.predict(inp)
            if pred == out:
                correct += 1

        print(f"  {transform}: {correct}/50 ({correct*2}%) | perm={perm.tolist()}")

    # TEST 2: Repeated values (harder)
    print("\n### TEST 2: REPEATED VALUES (fresh system)")

    for transform in transforms:
        system = SequencePermutationSystem()

        # Train on distinct
        for _ in range(15):
            inp = random.sample(range(1, 10), 5)
            out = apply_transform(transform, inp)
            system.learn(inp, out)

        # Test on REPEATED values
        correct = 0
        for _ in range(50):
            inp = [random.randint(1, 9) for _ in range(5)]
            out = apply_transform(transform, inp)
            pred = system.predict(inp)
            if pred == out:
                correct += 1

        print(f"  {transform} (repeated): {correct}/50 ({correct*2}%)")

    # TEST 3: Different lengths
    print("\n### TEST 3: DIFFERENT LENGTHS (fresh system per length)")

    for length in [3, 4, 5, 6, 7, 8]:
        system = SequencePermutationSystem()

        # Train reverse at this length
        for _ in range(15):
            inp = random.sample(range(1, max(10, length+5)), length)
            out = apply_transform('reverse', inp)
            system.learn(inp, out)

        perm = system.learner.get_hard_permutation(length)
        expected_perm = list(range(length-1, -1, -1))

        # Test
        correct = 0
        for _ in range(30):
            inp = random.sample(range(1, max(10, length+5)), length)
            out = apply_transform('reverse', inp)
            pred = system.predict(inp)
            if pred == out:
                correct += 1

        match = "✓" if perm.tolist() == expected_perm else "✗"
        print(f"  Length {length}: {correct}/30 ({correct/30*100:.0f}%) | perm={perm.tolist()} {match}")

    # TEST 4: Edge cases with fresh system
    print("\n### TEST 4: EDGE CASES (fresh system)")

    system = SequencePermutationSystem()

    # Train reverse
    for _ in range(15):
        inp = random.sample(range(1, 10), 5)
        out = apply_transform('reverse', inp)
        system.learn(inp, out)

    print(f"  Learned permutation: {system.learner.get_hard_permutation(5).tolist()}")

    # Edge cases
    cases = [
        ([5, 5, 5, 5, 5], "all same"),
        ([1, 2, 3, 4, 5], "sequential"),
        ([1, 9, 1, 9, 1], "alternating"),
        ([9, 8, 7, 6, 5], "descending"),
        ([1, 1, 1, 2, 2], "mostly same"),
    ]

    for inp, name in cases:
        out = apply_transform('reverse', inp)
        pred = system.predict(inp)
        match = "✓" if pred == out else "✗"
        print(f"  {name}: {inp} → {pred} (expected {out}) {match}")

    print("\n" + "=" * 70)


if __name__ == '__main__':
    test_isolated()
