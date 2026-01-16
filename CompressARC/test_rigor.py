"""
RIGOROUS TESTING of Permutation Learner

Testing for potential gaps:
1. Repeated values in input (harder case)
2. Different sequence lengths
3. Cross-transform transfer (learn reverse, test on rotate without reset)
4. More test examples
5. Edge cases
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Tuple
import random

# Import from permutation_learner
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


def generate_task_distinct(transform_name: str, length: int = 5) -> Tuple[List[int], List[int]]:
    """DISTINCT values only (easier)."""
    input_seq = random.sample(range(1, max(10, length + 5)), length)
    return input_seq, apply_transform(transform_name, input_seq)


def generate_task_repeated(transform_name: str, length: int = 5) -> Tuple[List[int], List[int]]:
    """ALLOW repeated values (harder)."""
    input_seq = [random.randint(1, 9) for _ in range(length)]
    return input_seq, apply_transform(transform_name, input_seq)


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


def test_rigor():
    print("=" * 70)
    print("RIGOROUS TESTING")
    print("=" * 70)

    # TEST 1: Repeated values
    print("\n### TEST 1: REPEATED VALUES (harder case)")
    print("Training with distinct, testing with repeated values")

    system = SequencePermutationSystem()
    system.reset()

    # Train on distinct values
    for _ in range(10):
        inp, out = generate_task_distinct('reverse')
        system.learn(inp, out)

    # Test on REPEATED values
    correct = 0
    total = 20
    for _ in range(total):
        inp, out = generate_task_repeated('reverse')
        pred = system.predict(inp)
        if pred == out:
            correct += 1
        else:
            print(f"  FAIL: {inp} → {pred} (expected {out})")

    print(f"\nRepeated values test: {correct}/{total} ({correct/total*100:.0f}%)")

    # TEST 2: Different lengths
    print("\n### TEST 2: DIFFERENT SEQUENCE LENGTHS")

    results = {}
    for length in [3, 4, 5, 6, 7, 8]:
        system.reset()

        # Train
        for _ in range(10):
            inp, out = generate_task_distinct('reverse', length=length)
            system.learn(inp, out)

        # Test
        correct = 0
        for _ in range(10):
            inp, out = generate_task_distinct('reverse', length=length)
            pred = system.predict(inp)
            if pred == out:
                correct += 1

        results[length] = correct / 10
        print(f"  Length {length}: {correct}/10 ({correct/10*100:.0f}%)")

    # TEST 3: Cross-transform transfer
    print("\n### TEST 3: CROSS-TRANSFORM TRANSFER")
    print("Learn reverse, then test rotate WITHOUT resetting")

    system.reset()

    # Learn reverse
    print("  Learning reverse...")
    for _ in range(10):
        inp, out = generate_task_distinct('reverse')
        system.learn(inp, out)

    perm = system.learner.get_hard_permutation(5)
    print(f"  Permutation after reverse: {perm.tolist()}")

    # Test rotate WITHOUT reset
    print("  Testing rotate_left WITHOUT reset...")
    correct = 0
    for _ in range(10):
        inp, out = generate_task_distinct('rotate_left')
        pred = system.predict(inp)
        if pred == out:
            correct += 1

    print(f"  Rotate (no reset): {correct}/10 ({correct/10*100:.0f}%)")
    print("  (Expected: LOW - different permutation needed)")

    # Now learn rotate
    print("  Now learning rotate_left...")
    for _ in range(10):
        inp, out = generate_task_distinct('rotate_left')
        system.learn(inp, out)

    perm = system.learner.get_hard_permutation(5)
    print(f"  Permutation after learning rotate: {perm.tolist()}")

    # Test rotate
    correct = 0
    for _ in range(10):
        inp, out = generate_task_distinct('rotate_left')
        pred = system.predict(inp)
        if pred == out:
            correct += 1

    print(f"  Rotate (after learning): {correct}/10 ({correct/10*100:.0f}%)")

    # TEST 4: More test examples
    print("\n### TEST 4: LARGE-SCALE TEST (100 examples)")

    transforms = ['identity', 'reverse', 'swap_pairs', 'rotate_left', 'rotate_right']

    for transform in transforms:
        system.reset()

        # Train on 20
        for _ in range(20):
            inp, out = generate_task_distinct(transform)
            system.learn(inp, out)

        # Test on 100
        correct = 0
        for _ in range(100):
            inp, out = generate_task_distinct(transform)
            pred = system.predict(inp)
            if pred == out:
                correct += 1

        print(f"  {transform}: {correct}/100 ({correct}%)")

    # TEST 5: Edge cases
    print("\n### TEST 5: EDGE CASES")

    system.reset()

    # Train reverse
    for _ in range(10):
        inp, out = generate_task_distinct('reverse')
        system.learn(inp, out)

    # Edge case: All same value
    inp = [5, 5, 5, 5, 5]
    out = [5, 5, 5, 5, 5]
    pred = system.predict(inp)
    print(f"  All same [5,5,5,5,5]: pred={pred}, expected={out}, match={pred==out}")

    # Edge case: Sequential
    inp = [1, 2, 3, 4, 5]
    out = [5, 4, 3, 2, 1]
    pred = system.predict(inp)
    print(f"  Sequential [1,2,3,4,5]: pred={pred}, expected={out}, match={pred==out}")

    # Edge case: Alternating
    inp = [1, 9, 1, 9, 1]
    out = [1, 9, 1, 9, 1]
    pred = system.predict(inp)
    print(f"  Alternating [1,9,1,9,1]: pred={pred}, expected={out}, match={pred==out}")

    print("\n" + "=" * 70)
    print("RIGOROUS TESTING COMPLETE")
    print("=" * 70)


if __name__ == '__main__':
    test_rigor()
