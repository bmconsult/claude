#!/usr/bin/env python3
"""
EXPERIMENT 9: Unified Grid/Sequence Architecture

Can we solve grids by treating them as flattened sequences?
If yes, we have a unified architecture for both modalities.

Approach:
1. Flatten ARC grids to sequences (row-major)
2. Solve with sequence MDL
3. Reshape output back to grid
4. Test if transfer works across modalities

This would prove: ONE architecture for ALL domains.
"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Tuple, Dict
from dataclasses import dataclass
import time
import json

np.random.seed(0)
torch.manual_seed(0)
torch.set_default_dtype(torch.float32)
torch.set_default_device('cpu')


# Import from existing modules
from sequence_mdl import SequenceMDL, SequenceTask, SequenceLibrary


def flatten_grid(grid: List[List[int]]) -> List[int]:
    """Flatten 2D grid to 1D sequence (row-major)."""
    return [cell for row in grid for cell in row]


def unflatten_grid(seq: List[int], shape: Tuple[int, int]) -> List[List[int]]:
    """Reshape 1D sequence back to 2D grid."""
    rows, cols = shape
    return [seq[i*cols:(i+1)*cols] for i in range(rows)]


def load_arc_as_sequences(n_puzzles: int = 10) -> List[SequenceTask]:
    """Load ARC puzzles as sequence tasks."""
    with open('dataset/arc-agi_training_challenges.json', 'r') as f:
        challenges = json.load(f)
    with open('dataset/arc-agi_training_solutions.json', 'r') as f:
        solutions = json.load(f)

    tasks = []
    puzzle_ids = list(challenges.keys())[:n_puzzles]

    for pid in puzzle_ids:
        problem = challenges[pid]
        solution = solutions.get(pid)

        # Convert to sequence pairs
        train_pairs = []
        for ex in problem['train']:
            inp = flatten_grid(ex['input'])
            out = flatten_grid(ex['output'])
            # Ensure same length (pad shorter)
            max_len = max(len(inp), len(out))
            inp = inp + [0] * (max_len - len(inp))
            out = out + [0] * (max_len - len(out))
            train_pairs.append((inp, out))

        test_pairs = []
        for i, ex in enumerate(problem['test']):
            inp = flatten_grid(ex['input'])
            if solution:
                out = flatten_grid(solution[i])
            else:
                out = inp  # Placeholder
            max_len = max(len(inp), len(out))
            inp = inp + [0] * (max_len - len(inp))
            out = out + [0] * (max_len - len(out))
            test_pairs.append((inp, out))

        max_len = max(
            max(len(p[0]) for p in train_pairs + test_pairs),
            max(len(p[1]) for p in train_pairs + test_pairs)
        )

        task = SequenceTask(
            task_name=pid,
            train_pairs=train_pairs,
            test_pairs=test_pairs,
            vocab_size=11,  # ARC colors 0-10
            max_len=max_len
        )
        tasks.append(task)

    return tasks


def solve_arc_as_sequence(task: SequenceTask, library: SequenceLibrary = None,
                          max_steps: int = 300, verbose: bool = True) -> Dict:
    """Solve an ARC puzzle using sequence MDL."""
    model = SequenceMDL(task.vocab_size, task.max_len, latent_dim=128, hidden_dim=256)

    # Transfer weights if library available
    transferred = 0
    if library:
        entry = library.get_best()
        if entry:
            for src_w, tgt_w in zip(entry['weights'], model.weights_list):
                if src_w.shape == tgt_w.shape:
                    tgt_w.data.copy_(src_w.data)
                    transferred += 1

    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, betas=(0.5, 0.9))

    # Prepare data
    def pad(seq, max_len):
        return seq + [0] * (max_len - len(seq))

    inputs = torch.tensor([pad(p[0], task.max_len) for p in task.train_pairs], dtype=torch.long)
    targets = torch.tensor([pad(p[1], task.max_len) for p in task.train_pairs], dtype=torch.long)

    # Train
    start_time = time.time()
    solved = False
    step = 0

    for step in range(max_steps):
        optimizer.zero_grad()
        loss, kl, recon = model.compute_loss(inputs, targets)
        loss.backward()
        optimizer.step()

        if loss.item() < 50.0:  # Higher threshold for grids
            solved = True
            break

    elapsed = time.time() - start_time

    # Test
    test_in = torch.tensor([pad(task.test_pairs[0][0], task.max_len)], dtype=torch.long)
    prediction = model.predict(test_in)[0].tolist()
    expected = task.test_pairs[0][1]

    # Compare (trim to expected length)
    pred_trimmed = prediction[:len(expected)]
    correct = pred_trimmed == expected

    if verbose:
        transfer_info = f" (transferred {transferred} weights)" if transferred > 0 else " (from scratch)"
        print(f"  {step + 1} steps, {elapsed:.1f}s{transfer_info}")
        print(f"  Loss: {loss.item():.1f}, Correct: {correct}")

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


def test_arc_with_sequence_mdl():
    """Test if ARC puzzles can be solved as sequences."""
    print("=" * 60)
    print("EXPERIMENT 9: ARC as Sequences")
    print("=" * 60)
    print("Can we solve grids by treating them as flattened sequences?")
    print()

    tasks = load_arc_as_sequences(10)
    library = SequenceLibrary()
    results = []

    for i, task in enumerate(tasks):
        print(f"\n[{i+1}/10] {task.task_name}")
        print(f"  Sequence length: {task.max_len}")

        if i == 0:
            result = solve_arc_as_sequence(task, verbose=True)
        else:
            result = solve_arc_as_sequence(task, library, verbose=True)

        if result['solved']:
            library.add(task.task_name, result['weights'], result['steps'])

        results.append(result)

    # Summary
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"Solved (loss < threshold): {sum(r['solved'] for r in results)}/10")
    print(f"Correct predictions: {sum(r['correct'] for r in results)}/10")

    print("\nLearning curve:")
    for i, r in enumerate(results):
        transfer = "TRANSFER" if r['transferred'] > 0 else "SCRATCH"
        correct = "✓" if r['correct'] else "✗"
        print(f"  Task {i+1}: {r['steps']:3d} steps ({transfer}) {correct}")

    return results


def test_sequence_to_grid_transfer():
    """Test if sequence-trained weights help grid tasks."""
    print("\n" + "=" * 60)
    print("CROSS-MODAL TRANSFER TEST")
    print("=" * 60)
    print("Train on pure sequences, test on grids")
    print()

    # First, train on sequence tasks
    from sequence_mdl import make_increment_tasks, solve_task

    print("Phase 1: Training on sequence tasks...")
    seq_tasks = make_increment_tasks(5)
    seq_library = SequenceLibrary()

    for i, task in enumerate(seq_tasks):
        result = solve_task(task, verbose=False)
        if result['solved']:
            seq_library.add(task.task_name, result['weights'], result['steps'])
        print(f"  Seq task {i+1}: {result['steps']} steps")

    print(f"\nLibrary has {len(seq_library.entries)} entries")

    # Now test on ARC (grid) tasks
    print("\nPhase 2: Testing on ARC (grid) tasks with sequence weights...")
    arc_tasks = load_arc_as_sequences(5)

    for i, task in enumerate(arc_tasks):
        print(f"\n[{i+1}/5] {task.task_name}")

        # Test WITHOUT transfer
        result_cold = solve_arc_as_sequence(task, None, verbose=False)
        print(f"  Cold (no transfer): {result_cold['steps']} steps")

        # Test WITH sequence library
        result_transfer = solve_arc_as_sequence(task, seq_library, verbose=False)
        print(f"  With seq transfer:  {result_transfer['steps']} steps")

        if result_transfer['steps'] < result_cold['steps']:
            speedup = (result_cold['steps'] - result_transfer['steps']) / result_cold['steps'] * 100
            print(f"  SPEEDUP: {speedup:.1f}%")


if __name__ == "__main__":
    # Test 1: Can we solve ARC as sequences?
    test_arc_with_sequence_mdl()

    # Test 2: Does cross-modal transfer work?
    test_sequence_to_grid_transfer()
