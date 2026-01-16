"""
Experiment 17: Modular Value Transforms

Key insight (parallel to permutation discovery):
- Positional transforms ARE permutations → learn permutation matrix
- Value transforms have STRUCTURE → learn the structure, not generic function

Value transform types:
1. POINTWISE: output[i] = f(input[i])
   - increment: output[i] = input[i] + c
   - scale: output[i] = input[i] * c
   - clamp: output[i] = min(max(input[i], lo), hi)

2. CUMULATIVE: output[i] = reduce(input[0:i+1], op)
   - running_max: output[i] = max(input[0:i+1])
   - running_sum: output[i] = sum(input[0:i+1])
   - running_min: output[i] = min(input[0:i+1])

3. PAIRWISE: output[i] = f(input[i], input[pair(i)])
   - mirror_add: output[i] = input[i] + input[N-1-i]
   - mirror_mul: output[i] = input[i] * input[N-1-i]

Architecture:
- Learn which MODULE applies (categorical selection)
- Learn module PARAMETERS (offset, scale, etc.)
- MDL: simpler modules preferred

This is NOT a generic neural network.
It's learning WHICH STRUCTURE + WHAT PARAMETERS.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Tuple, Optional
import random


class PointwiseModule(nn.Module):
    """Pointwise transforms: output[i] = a * input[i] + b"""

    def __init__(self):
        super().__init__()
        # Learn scale and offset
        self.scale = nn.Parameter(torch.tensor(1.0))
        self.offset = nn.Parameter(torch.tensor(0.0))

    def forward(self, x: torch.Tensor, hard: bool = False) -> torch.Tensor:
        # Pointwise is the same for hard/soft
        return self.scale * x + self.offset

    def description_length(self) -> float:
        """MDL: bits to describe this transform."""
        # Identity (scale=1, offset=0) is simplest
        dl = 0.0
        dl += abs(self.scale.item() - 1.0) * 2  # Cost for non-unit scale
        dl += abs(self.offset.item()) * 2       # Cost for non-zero offset
        return dl


class CumulativeModule(nn.Module):
    """Cumulative transforms: output[i] = reduce(input[0:i+1], op)"""

    def __init__(self):
        super().__init__()
        # Soft selection over operations: max, min, sum, mean
        self.op_logits = nn.Parameter(torch.zeros(4))

    def forward(self, x: torch.Tensor, hard: bool = False) -> torch.Tensor:
        seq_len = x.shape[-1]

        # Compute all cumulative operations
        result = torch.zeros_like(x)
        for i in range(seq_len):
            prefix = x[:i+1] if x.dim() == 1 else x[..., :i+1]

            # Cumulative operations
            cum_max = prefix.max()
            cum_min = prefix.min()
            cum_sum = prefix.sum()
            cum_mean = prefix.float().mean()

            if hard:
                # Hard selection for inference
                idx = self.op_logits.argmax().item()
                result[i] = [cum_max, cum_min, cum_sum, cum_mean][idx]
            else:
                # Soft blend for training
                op_probs = F.softmax(self.op_logits, dim=0)
                ops = torch.stack([cum_max, cum_min, cum_sum, cum_mean])
                result[i] = (op_probs * ops).sum()

        return result

    def get_op(self) -> str:
        """Return which operation dominates."""
        idx = self.op_logits.argmax().item()
        return ['max', 'min', 'sum', 'mean'][idx]

    def description_length(self) -> float:
        """MDL: bits to describe operation selection."""
        # Entropy of operation selection
        probs = F.softmax(self.op_logits, dim=0)
        entropy = -torch.sum(probs * torch.log(probs + 1e-10))
        return entropy.item()


class PairwiseModule(nn.Module):
    """Pairwise transforms: output[i] = f(input[i], input[pair(i)])"""

    def __init__(self, max_len: int = 10):
        super().__init__()
        self.max_len = max_len

        # Learn pairing pattern (which position pairs with which)
        # Default: mirror pairing (i pairs with N-1-i)
        self.pair_logits = nn.Parameter(torch.zeros(max_len, max_len))
        # Initialize to mirror pattern
        for i in range(max_len):
            self.pair_logits.data[i, max_len - 1 - i] = 5.0

        # Learn operation: add, subtract, multiply, max, min
        self.op_logits = nn.Parameter(torch.zeros(5))
        self.op_logits.data[0] = 3.0  # Bias toward add

    def forward(self, x: torch.Tensor, hard: bool = False) -> torch.Tensor:
        seq_len = x.shape[-1]

        result = torch.zeros_like(x)
        for i in range(seq_len):
            val_i = x[i].float()

            if hard:
                # Hard selection for inference
                pair_idx = self.pair_logits[i, :seq_len].argmax().item()
                paired_val = x[pair_idx].float()

                op_idx = self.op_logits.argmax().item()
                ops = [
                    val_i + paired_val,
                    val_i - paired_val,
                    val_i * paired_val,
                    torch.max(val_i, paired_val),
                    torch.min(val_i, paired_val),
                ]
                result[i] = ops[op_idx]
            else:
                # Soft selection for training
                pair_probs = F.softmax(self.pair_logits[i, :seq_len], dim=0)
                paired_val = (pair_probs * x.float()).sum()

                op_probs = F.softmax(self.op_logits, dim=0)
                ops = torch.stack([
                    val_i + paired_val,
                    val_i - paired_val,
                    val_i * paired_val,
                    torch.max(val_i, paired_val),
                    torch.min(val_i, paired_val),
                ])
                result[i] = (op_probs * ops).sum()

        return result

    def get_pairing(self, seq_len: int) -> List[int]:
        """Return hard pairing pattern."""
        pair_probs = F.softmax(self.pair_logits[:seq_len, :seq_len], dim=1)
        return pair_probs.argmax(dim=1).tolist()

    def get_op(self) -> str:
        """Return which operation dominates."""
        idx = self.op_logits.argmax().item()
        return ['add', 'subtract', 'multiply', 'max', 'min'][idx]

    def description_length(self) -> float:
        """MDL: bits to describe pairing + operation."""
        # Pairing entropy
        seq_len = 5  # default
        pair_probs = F.softmax(self.pair_logits[:seq_len, :seq_len], dim=1)
        pair_entropy = -torch.sum(pair_probs * torch.log(pair_probs + 1e-10))

        # Op entropy
        op_probs = F.softmax(self.op_logits, dim=0)
        op_entropy = -torch.sum(op_probs * torch.log(op_probs + 1e-10))

        return pair_entropy.item() + op_entropy.item()


class ModularValueSystem(nn.Module):
    """
    Full system: learn which module type + module parameters.

    MDL objective selects simplest explanation.
    """

    def __init__(self, max_len: int = 10):
        super().__init__()
        self.max_len = max_len

        # Module type selection - bias toward pointwise (simplest)
        self.module_logits = nn.Parameter(torch.tensor([2.0, 0.0, 0.0]))

        # The three modules
        self.pointwise = PointwiseModule()
        self.cumulative = CumulativeModule()
        self.pairwise = PairwiseModule(max_len)

    def forward(self, x: torch.Tensor, hard: bool = False) -> torch.Tensor:
        if hard:
            # Hard selection for inference
            idx = self.module_logits.argmax().item()
            if idx == 0:
                return self.pointwise(x, hard=True)
            elif idx == 1:
                return self.cumulative(x, hard=True)
            else:
                return self.pairwise(x, hard=True)
        else:
            # Soft selection for training
            module_probs = F.softmax(self.module_logits, dim=0)

            out_pointwise = self.pointwise(x, hard=False)
            out_cumulative = self.cumulative(x, hard=False)
            out_pairwise = self.pairwise(x, hard=False)

            result = (module_probs[0] * out_pointwise +
                      module_probs[1] * out_cumulative +
                      module_probs[2] * out_pairwise)

            return result

    def get_module(self) -> str:
        """Return which module dominates."""
        idx = self.module_logits.argmax().item()
        return ['pointwise', 'cumulative', 'pairwise'][idx]

    def description_length(self) -> float:
        """Total description length."""
        # Module selection cost
        probs = F.softmax(self.module_logits, dim=0)
        module_dl = -torch.sum(probs * torch.log(probs + 1e-10)).item()

        # Weighted module costs
        dl = module_dl
        dl += probs[0].item() * self.pointwise.description_length()
        dl += probs[1].item() * self.cumulative.description_length()
        dl += probs[2].item() * self.pairwise.description_length()

        return dl


class ValueTransformSystem:
    """
    Learn value transforms using modular architecture.
    """

    def __init__(self, max_len: int = 10):
        self.max_len = max_len
        self.model = ModularValueSystem(max_len)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.3)
        self.examples: List[Tuple[torch.Tensor, torch.Tensor]] = []

    def add_example(self, input_seq: List[int], output_seq: List[int]):
        """Add training example."""
        x = torch.tensor(input_seq, dtype=torch.float32)
        y = torch.tensor(output_seq, dtype=torch.float32)
        self.examples.append((x, y))

    def train_batch(self, max_steps: int = 2000, threshold: float = 0.01) -> int:
        """Train on all examples (batch training for stability)."""
        if not self.examples:
            return 0

        for step in range(max_steps):
            self.optimizer.zero_grad()

            total_loss = 0
            for x, y in self.examples:
                pred = self.model(x)
                recon_loss = F.mse_loss(pred, y)
                mdl_loss = 0.01 * self.model.description_length()
                total_loss += recon_loss + mdl_loss

            total_loss /= len(self.examples)

            if total_loss.item() < threshold:
                return step + 1

            total_loss.backward()
            self.optimizer.step()

        return max_steps

    def predict(self, input_seq: List[int]) -> List[int]:
        """Apply learned transform (hard selection with discretized params)."""
        x = torch.tensor(input_seq, dtype=torch.float32)
        with torch.no_grad():
            # For pointwise, discretize parameters to nearest integer
            module = self.model.get_module()
            if module == 'pointwise':
                scale = round(self.model.pointwise.scale.item())
                offset = round(self.model.pointwise.offset.item())
                pred = scale * x + offset
            else:
                pred = self.model(x, hard=True)
        return [round(v.item()) for v in pred]

    def get_learned_structure(self) -> dict:
        """Return what structure was learned."""
        module = self.model.get_module()
        info = {'module': module}

        if module == 'pointwise':
            info['scale'] = self.model.pointwise.scale.item()
            info['offset'] = self.model.pointwise.offset.item()
        elif module == 'cumulative':
            info['op'] = self.model.cumulative.get_op()
        elif module == 'pairwise':
            info['pairing'] = self.model.pairwise.get_pairing(5)
            info['op'] = self.model.pairwise.get_op()

        return info

    def reset(self):
        """Reset for new transform."""
        self.model = ModularValueSystem(self.max_len)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.3)
        self.examples = []


def apply_transform(name: str, inp: List[int]) -> List[int]:
    """Ground truth transforms."""
    if name == 'identity':
        return inp.copy()
    elif name == 'increment':
        return [x + 1 for x in inp]
    elif name == 'double':
        return [x * 2 for x in inp]
    elif name == 'running_max':
        result = []
        current_max = float('-inf')
        for x in inp:
            current_max = max(current_max, x)
            result.append(int(current_max))
        return result
    elif name == 'running_sum':
        result = []
        total = 0
        for x in inp:
            total += x
            result.append(total)
        return result
    elif name == 'mirror_add':
        n = len(inp)
        return [inp[i] + inp[n - 1 - i] for i in range(n)]
    elif name == 'mirror_max':
        n = len(inp)
        return [max(inp[i], inp[n - 1 - i]) for i in range(n)]
    else:
        raise ValueError(f"Unknown transform: {name}")


def test_transform(system: ValueTransformSystem, transform: str,
                   num_train: int = 15, num_test: int = 10) -> Tuple[int, dict]:
    """Test system on a transform."""
    print(f"\n  Testing {transform}:")
    system.reset()

    # Training
    print(f"    Training on {num_train} examples...")
    for _ in range(num_train):
        inp = random.sample(range(1, 10), 5)
        out = apply_transform(transform, inp)
        system.add_example(inp, out)

    steps = system.train_batch()
    print(f"    Converged in {steps} steps")

    # Show learned structure
    structure = system.get_learned_structure()
    print(f"    Learned: {structure}")

    # Testing
    correct = 0
    for _ in range(num_test):
        inp = random.sample(range(1, 10), 5)
        out = apply_transform(transform, inp)
        pred = system.predict(inp)
        if pred == out:
            correct += 1

    print(f"    Test: {correct}/{num_test} ({correct/num_test*100:.0f}%)")

    return correct, structure


def main():
    """Run Experiment 17: Modular Value Transforms."""
    print("=" * 70)
    print("EXPERIMENT 17: Modular Value Transforms")
    print("=" * 70)
    print("\nKey insight: Value transforms have STRUCTURE")
    print("  - Pointwise: output[i] = f(input[i])")
    print("  - Cumulative: output[i] = reduce(input[0:i+1])")
    print("  - Pairwise: output[i] = f(input[i], input[pair(i)])")
    print("\nLearn which structure + what parameters.")
    print("=" * 70)

    system = ValueTransformSystem(max_len=10)

    transforms = [
        # Pointwise
        'identity',
        'increment',
        'double',
        # Cumulative
        'running_max',
        'running_sum',
        # Pairwise
        'mirror_add',
        'mirror_max',
    ]

    results = {}

    for transform in transforms:
        correct, structure = test_transform(system, transform)
        results[transform] = {
            'accuracy': correct / 10,
            'structure': structure
        }

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    pointwise = ['identity', 'increment', 'double']
    cumulative = ['running_max', 'running_sum']
    pairwise = ['mirror_add', 'mirror_max']

    pw_acc = sum(results[t]['accuracy'] for t in pointwise) / len(pointwise)
    cum_acc = sum(results[t]['accuracy'] for t in cumulative) / len(cumulative)
    pair_acc = sum(results[t]['accuracy'] for t in pairwise) / len(pairwise)
    overall = sum(results[t]['accuracy'] for t in transforms) / len(transforms)

    print(f"\nPointwise (identity, increment, double): {pw_acc*100:.0f}%")
    print(f"Cumulative (running_max, running_sum): {cum_acc*100:.0f}%")
    print(f"Pairwise (mirror_add, mirror_max): {pair_acc*100:.0f}%")
    print(f"\nOverall: {overall*100:.0f}%")

    # Learned structures
    print("\nLearned Structures:")
    for t in transforms:
        print(f"  {t}: {results[t]['structure']}")

    print("\n" + "=" * 70)
    if overall >= 0.8:
        print("SUCCESS: >80% on value transforms!")
    else:
        print(f"Result: {overall*100:.0f}%")
    print("=" * 70)

    return results


if __name__ == '__main__':
    main()
