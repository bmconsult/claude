"""
WEIGHT TRANSFER v3

Now that we KNOW similar puzzles train similarly, let's actually transfer weights.

Key insight: We need puzzles with IDENTICAL structure (same sizes) for direct
weight transfer. Our similarity metric found these - now we use them.

THE TEST:
1. Train puzzle A to completion
2. Use A's weights to initialize puzzle B (where B is structurally identical)
3. Does B train faster?
"""

import time
import numpy as np
import torch
from copy import deepcopy

import preprocessing
import arc_compressor
from puzzle_similarity import extract_features, compute_similarity, PuzzleFeatures


def find_identical_pairs(tasks, min_similarity=0.95):
    """
    Find pairs of puzzles that are nearly structurally identical.
    These are the best candidates for direct weight transfer.
    """
    features = [extract_features(t) for t in tasks]
    pairs = []

    for i in range(len(tasks)):
        for j in range(i + 1, len(tasks)):
            sim = compute_similarity(features[i], features[j])
            if sim >= min_similarity:
                # Check if sizes match exactly (required for weight transfer)
                f1, f2 = features[i], features[j]
                if (f1.input_size == f2.input_size and
                    f1.output_size == f2.output_size and
                    f1.num_colors == f2.num_colors):
                    pairs.append({
                        'i': i,
                        'j': j,
                        'puzzle_a': tasks[i].task_name,
                        'puzzle_b': tasks[j].task_name,
                        'similarity': sim,
                        'sizes_match': True
                    })

    return pairs


def train_puzzle(task, max_steps=200, init_weights=None):
    """
    Train a puzzle, optionally with transferred weights.
    """
    model = arc_compressor.ARCCompressor(task)
    optimizer = torch.optim.Adam(model.weights_list, lr=0.01, betas=(0.5, 0.9))

    # Apply transferred weights if provided
    weights_applied = False
    if init_weights is not None:
        try:
            # Try to copy weights from init_weights to model
            for i, (src, dst) in enumerate(zip(init_weights, model.weights_list)):
                if src.shape == dst.shape:
                    dst.data.copy_(src.data)
                    weights_applied = True
        except Exception as e:
            print(f"    Warning: Could not apply weights: {e}")

    target_loss = 50.0
    for step in range(max_steps):
        optimizer.zero_grad()
        logits, x_mask, y_mask, KL_amounts, KL_names = model.forward()
        logits = torch.cat([torch.zeros_like(logits[:, :1, :, :]), logits], dim=1)

        total_KL = sum(torch.sum(kl) for kl in KL_amounts)
        loss = total_KL

        loss.backward()
        optimizer.step()

        if loss.item() < target_loss:
            return {
                'solved': True,
                'steps': step,
                'loss': loss.item(),
                'weights': [w.detach().clone() for w in model.weights_list],
                'weights_applied': weights_applied
            }

    return {
        'solved': False,
        'steps': max_steps,
        'loss': loss.item(),
        'weights': [w.detach().clone() for w in model.weights_list],
        'weights_applied': weights_applied
    }


def run_transfer_experiment():
    """
    THE CRITICAL TEST:
    - Find puzzle pairs with identical structure
    - Train puzzle A from scratch
    - Train puzzle B with A's weights
    - Compare steps to solve
    """
    print("=" * 60)
    print("WEIGHT TRANSFER TEST v3")
    print("=" * 60)
    print("Testing actual weight transfer between identical-structure puzzles")
    print("=" * 60)

    # Get puzzles
    print("\n1. Loading puzzles...")
    tasks = preprocessing.preprocess_tasks('training', list(range(100)))
    print(f"   Loaded {len(tasks)} puzzles")

    # Find identical pairs
    print("\n2. Finding identical-structure pairs...")
    pairs = find_identical_pairs(tasks, min_similarity=0.95)
    print(f"   Found {len(pairs)} pairs with matching structure")

    if not pairs:
        print("\n   No matching pairs found. Trying lower threshold...")
        pairs = find_identical_pairs(tasks, min_similarity=0.90)
        print(f"   Found {len(pairs)} pairs at 0.90 threshold")

    if not pairs:
        print("\n   Still no pairs. Cannot test weight transfer.")
        return

    # Show found pairs
    for p in pairs[:5]:
        print(f"   - {p['puzzle_a']} <-> {p['puzzle_b']} (sim={p['similarity']:.3f})")

    # Test transfer on first 3 pairs
    print("\n3. Testing weight transfer...")
    results = []

    for pair in pairs[:3]:
        print(f"\n   Pair: {pair['puzzle_a']} <-> {pair['puzzle_b']}")

        task_a = tasks[pair['i']]
        task_b = tasks[pair['j']]

        # Train A from scratch
        print(f"   Training {pair['puzzle_a']} from scratch...")
        start = time.time()
        result_a = train_puzzle(task_a, max_steps=200)
        time_a = time.time() - start
        print(f"      -> {result_a['steps']} steps, {time_a:.1f}s")

        # Train B from scratch (baseline)
        print(f"   Training {pair['puzzle_b']} from scratch (baseline)...")
        start = time.time()
        result_b_baseline = train_puzzle(task_b, max_steps=200)
        time_b_baseline = time.time() - start
        print(f"      -> {result_b_baseline['steps']} steps, {time_b_baseline:.1f}s")

        # Train B with A's weights (transfer)
        print(f"   Training {pair['puzzle_b']} WITH transfer from A...")
        start = time.time()
        result_b_transfer = train_puzzle(task_b, max_steps=200, init_weights=result_a['weights'])
        time_b_transfer = time.time() - start
        print(f"      -> {result_b_transfer['steps']} steps, {time_b_transfer:.1f}s")
        print(f"      -> Weights applied: {result_b_transfer['weights_applied']}")

        # Calculate speedup
        if result_b_baseline['steps'] > 0:
            speedup = (result_b_baseline['steps'] - result_b_transfer['steps']) / result_b_baseline['steps'] * 100
        else:
            speedup = 0

        results.append({
            'pair': pair,
            'a_steps': result_a['steps'],
            'b_baseline_steps': result_b_baseline['steps'],
            'b_transfer_steps': result_b_transfer['steps'],
            'speedup': speedup,
            'weights_applied': result_b_transfer['weights_applied']
        })

        print(f"   SPEEDUP: {speedup:.1f}%")

    # Summary
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)

    avg_speedup = np.mean([r['speedup'] for r in results])
    print(f"\nAverage speedup: {avg_speedup:.1f}%")

    if avg_speedup > 20:
        print("\n✓ TRANSFER WORKS! Significant speedup achieved.")
    elif avg_speedup > 0:
        print("\n~ MARGINAL - Some speedup but not conclusive.")
    else:
        print("\n✗ NO TRANSFER - Weights didn't help.")

    print("\nPer-pair breakdown:")
    for r in results:
        print(f"  {r['pair']['puzzle_a']} -> {r['pair']['puzzle_b']}")
        print(f"    Baseline: {r['b_baseline_steps']} steps")
        print(f"    Transfer: {r['b_transfer_steps']} steps")
        print(f"    Speedup:  {r['speedup']:.1f}%")

    return results


if __name__ == "__main__":
    results = run_transfer_experiment()
